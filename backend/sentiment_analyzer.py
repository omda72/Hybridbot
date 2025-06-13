import asyncio
import aiohttp
import tweepy
import praw
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, List
from config import Config
import logging

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.setup_apis()
    
    def setup_apis(self):
        """Setup social media API clients"""
        # Twitter API v2
        if Config.TWITTER_BEARER_TOKEN:
            self.twitter_client = tweepy.Client(
                bearer_token=Config.TWITTER_BEARER_TOKEN,
                wait_on_rate_limit=True
            )
        
        # Reddit API
        if Config.REDDIT_CLIENT_ID and Config.REDDIT_CLIENT_SECRET:
            self.reddit = praw.Reddit(
                client_id=Config.REDDIT_CLIENT_ID,
                client_secret=Config.REDDIT_CLIENT_SECRET,
                user_agent="CryptoBotPro/1.0"
            )
    
    async def get_twitter_sentiment(self, symbol: str, count: int = 100) -> Dict:
        """Analyze Twitter sentiment for a cryptocurrency"""
        try:
            # Search for tweets about the cryptocurrency
            query = f"${symbol} OR #{symbol} OR {symbol} crypto -is:retweet lang:en"
            tweets = tweepy.Paginator(
                self.twitter_client.search_recent_tweets,
                query=query,
                max_results=min(count, 100)
            ).flatten(limit=count)
            
            sentiments = []
            for tweet in tweets:
                # Analyze sentiment using VADER
                vader_score = self.vader_analyzer.polarity_scores(tweet.text)
                
                # Analyze sentiment using TextBlob
                blob = TextBlob(tweet.text)
                textblob_score = blob.sentiment.polarity
                
                sentiments.append({
                    'text': tweet.text,
                    'vader_compound': vader_score['compound'],
                    'textblob_polarity': textblob_score,
                    'created_at': tweet.created_at
                })
            
            # Calculate overall sentiment
            if sentiments:
                avg_vader = sum(s['vader_compound'] for s in sentiments) / len(sentiments)
                avg_textblob = sum(s['textblob_polarity'] for s in sentiments) / len(sentiments)
                
                # Combine scores (weighted average)
                combined_score = (avg_vader * 0.6) + (avg_textblob * 0.4)
                
                return {
                    'symbol': symbol,
                    'source': 'twitter',
                    'sentiment_score': combined_score,
                    'sentiment_label': self._get_sentiment_label(combined_score),
                    'tweet_count': len(sentiments),
                    'confidence': abs(combined_score),
                    'raw_sentiments': sentiments[-10:]  # Last 10 for debugging
                }
            
            return {'error': 'No tweets found'}
            
        except Exception as e:
            logger.error(f"Error analyzing Twitter sentiment: {e}")
            return {'error': str(e)}
    
    async def get_reddit_sentiment(self, symbol: str, limit: int = 50) -> Dict:
        """Analyze Reddit sentiment for a cryptocurrency"""
        try:
            # Search in crypto-related subreddits
            subreddits = ['cryptocurrency', 'CryptoMarkets', 'Bitcoin', 'ethereum', 'altcoin']
            all_posts = []
            
            for subreddit_name in subreddits:
                subreddit = self.reddit.subreddit(subreddit_name)
                
                # Search for posts mentioning the symbol
                for post in subreddit.search(symbol, limit=limit//len(subreddits)):
                    # Analyze post title and content
                    text = f"{post.title} {post.selftext}"
                    
                    vader_score = self.vader_analyzer.polarity_scores(text)
                    blob = TextBlob(text)
                    
                    all_posts.append({
                        'title': post.title,
                        'score': post.score,
                        'num_comments': post.num_comments,
                        'vader_compound': vader_score['compound'],
                        'textblob_polarity': blob.sentiment.polarity,
                        'created_utc': post.created_utc
                    })
            
            if all_posts:
                # Weight by post score (upvotes)
                total_weight = sum(max(post['score'], 1) for post in all_posts)
                weighted_vader = sum(
                    post['vader_compound'] * max(post['score'], 1) 
                    for post in all_posts
                ) / total_weight
                
                weighted_textblob = sum(
                    post['textblob_polarity'] * max(post['score'], 1) 
                    for post in all_posts
                ) / total_weight
                
                combined_score = (weighted_vader * 0.6) + (weighted_textblob * 0.4)
                
                return {
                    'symbol': symbol,
                    'source': 'reddit',
                    'sentiment_score': combined_score,
                    'sentiment_label': self._get_sentiment_label(combined_score),
                    'post_count': len(all_posts),
                    'confidence': abs(combined_score),
                    'avg_score': sum(post['score'] for post in all_posts) / len(all_posts)
                }
            
            return {'error': 'No Reddit posts found'}
            
        except Exception as e:
            logger.error(f"Error analyzing Reddit sentiment: {e}")
            return {'error': str(e)}
    
    async def get_lunarcrush_sentiment(self, symbol: str) -> Dict:
        """Get sentiment data from LunarCrush API"""
        try:
            url = f"https://api.lunarcrush.com/v2"
            params = {
                'data': 'assets',
                'key': Config.LUNARCRUSH_API_KEY,
                'symbol': symbol
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    data = await response.json()
                    
                    if data.get('data') and len(data['data']) > 0:
                        asset_data = data['data'][0]
                        
                        return {
                            'symbol': symbol,
                            'source': 'lunarcrush',
                            'sentiment_score': asset_data.get('sentiment', 0) / 5.0,  # Normalize to -1 to 1
                            'social_score': asset_data.get('social_score', 0),
                            'social_volume': asset_data.get('social_volume', 0),
                            'social_dominance': asset_data.get('social_dominance', 0),
                            'market_cap': asset_data.get('market_cap', 0),
                            'price_score': asset_data.get('price_score', 0)
                        }
            
            return {'error': 'No LunarCrush data found'}
            
        except Exception as e:
            logger.error(f"Error fetching LunarCrush sentiment: {e}")
            return {'error': str(e)}
    
    def _get_sentiment_label(self, score: float) -> str:
        """Convert sentiment score to label"""
        if score > 0.1:
            return 'bullish'
        elif score < -0.1:
            return 'bearish'
        else:
            return 'neutral'
    
    async def get_combined_sentiment(self, symbol: str) -> Dict:
        """Get combined sentiment from all sources"""
        try:
            # Fetch sentiment from all sources concurrently
            twitter_task = self.get_twitter_sentiment(symbol)
            reddit_task = self.get_reddit_sentiment(symbol)
            lunarcrush_task = self.get_lunarcrush_sentiment(symbol)
            
            twitter_sentiment, reddit_sentiment, lunarcrush_sentiment = await asyncio.gather(
                twitter_task, reddit_task, lunarcrush_task, return_exceptions=True
            )
            
            # Combine sentiments with weights
            sentiments = []
            weights = []
            
            if isinstance(twitter_sentiment, dict) and 'sentiment_score' in twitter_sentiment:
                sentiments.append(twitter_sentiment['sentiment_score'])
                weights.append(0.4)  # Twitter weight
            
            if isinstance(reddit_sentiment, dict) and 'sentiment_score' in reddit_sentiment:
                sentiments.append(reddit_sentiment['sentiment_score'])
                weights.append(0.3)  # Reddit weight
            
            if isinstance(lunarcrush_sentiment, dict) and 'sentiment_score' in lunarcrush_sentiment:
                sentiments.append(lunarcrush_sentiment['sentiment_score'])
                weights.append(0.3)  # LunarCrush weight
            
            if sentiments:
                # Calculate weighted average
                combined_score = sum(s * w for s, w in zip(sentiments, weights)) / sum(weights)
                
                return {
                    'symbol': symbol,
                    'combined_sentiment_score': combined_score,
                    'sentiment_label': self._get_sentiment_label(combined_score),
                    'confidence': abs(combined_score),
                    'sources': {
                        'twitter': twitter_sentiment,
                        'reddit': reddit_sentiment,
                        'lunarcrush': lunarcrush_sentiment
                    }
                }
            
            return {'error': 'No sentiment data available'}
            
        except Exception as e:
            logger.error(f"Error getting combined sentiment: {e}")
            return {'error': str(e)}