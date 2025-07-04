import hashlib
import secrets
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import re

# Security configuration
SECRET_KEY = "your-secret-key-change-in-production"  # Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with salt"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}:{password_hash}"

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        salt, password_hash = hashed_password.split(":")
        return hashlib.sha256((password + salt).encode()).hexdigest() == password_hash
    except ValueError:
        return False

def generate_verification_token() -> str:
    """Generate a secure verification token"""
    return secrets.token_urlsafe(32)

def generate_reset_token() -> str:
    """Generate a secure password reset token"""
    return secrets.token_urlsafe(32)

def create_access_token(user_id: str, email: str) -> str:
    """Create a JWT access token"""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": user_id,
        "email": email,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify and decode a JWT access token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check if token is expired
        if datetime.fromtimestamp(payload.get("exp", 0)) < datetime.utcnow():
            return None
            
        # Verify token type
        if payload.get("type") != "access":
            return None
            
        return {
            "user_id": payload.get("sub"),
            "email": payload.get("email"),
            "exp": payload.get("exp"),
            "iat": payload.get("iat")
        }
    except jwt.InvalidTokenError:
        return None

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> Dict[str, Any]:
    """Validate password strength"""
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one number")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }

def validate_name(name: str) -> bool:
    """Validate user name"""
    return len(name.strip()) >= 2 and len(name.strip()) <= 50

# OAuth configuration
OAUTH_CONFIGS = {
    "google": {
        "client_id": "your-google-client-id",
        "client_secret": "your-google-client-secret",
        "redirect_uri": "https://your-domain.com/auth/oauth/google/callback",
        "scope": "openid email profile",
        "auth_url": "https://accounts.google.com/o/oauth2/auth",
        "token_url": "https://oauth2.googleapis.com/token",
        "user_info_url": "https://www.googleapis.com/oauth2/v2/userinfo"
    },
    "github": {
        "client_id": "your-github-client-id",
        "client_secret": "your-github-client-secret",
        "redirect_uri": "https://your-domain.com/auth/oauth/github/callback",
        "scope": "user:email",
        "auth_url": "https://github.com/login/oauth/authorize",
        "token_url": "https://github.com/login/oauth/access_token",
        "user_info_url": "https://api.github.com/user"
    }
}

def get_oauth_auth_url(provider: str, state: str) -> Optional[str]:
    """Generate OAuth authorization URL"""
    config = OAUTH_CONFIGS.get(provider)
    if not config:
        return None
    
    params = {
        "client_id": config["client_id"],
        "redirect_uri": config["redirect_uri"],
        "scope": config["scope"],
        "state": state,
        "response_type": "code"
    }
    
    if provider == "google":
        params["access_type"] = "offline"
        params["prompt"] = "consent"
    
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"{config['auth_url']}?{query_string}"

def generate_oauth_state() -> str:
    """Generate a secure OAuth state parameter"""
    return secrets.token_urlsafe(32)

# Rate limiting (simple in-memory implementation)
class RateLimiter:
    def __init__(self):
        self.attempts: Dict[str, Dict[str, Any]] = {}
    
    def is_rate_limited(self, identifier: str, max_attempts: int = 5, window_minutes: int = 15) -> bool:
        """Check if an identifier is rate limited"""
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=window_minutes)
        
        if identifier not in self.attempts:
            self.attempts[identifier] = {"count": 0, "first_attempt": now}
            return False
        
        attempt_info = self.attempts[identifier]
        
        # Reset if outside window
        if attempt_info["first_attempt"] < window_start:
            self.attempts[identifier] = {"count": 1, "first_attempt": now}
            return False
        
        # Check if over limit
        if attempt_info["count"] >= max_attempts:
            return True
        
        # Increment counter
        attempt_info["count"] += 1
        return False
    
    def clear_attempts(self, identifier: str):
        """Clear rate limit attempts for an identifier"""
        if identifier in self.attempts:
            del self.attempts[identifier]

# Global rate limiter instance
rate_limiter = RateLimiter()