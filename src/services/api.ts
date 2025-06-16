import { TradingBot, Portfolio, Signal, Trade, Price } from '../types/trading';

const API_BASE = "https://api-r4eb5eatnq-uc.a.run.app"; // Firebase Function URL

export async function fetchBots(): Promise<TradingBot[]> {
  try {
    const res = await fetch(`${API_BASE}/bots`);
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error('Failed to fetch bots:', err);
    return [];
  }
}

export async function fetchPortfolio(): Promise<Portfolio> {
  try {
    const res = await fetch(`${API_BASE}/portfolio`);
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error('Failed to fetch portfolio:', err);
    return { totalValue: 0, assets: [] };
  }
}

export async function fetchSignals(): Promise<Signal[]> {
  try {
    const res = await fetch(`${API_BASE}/signals`);
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error('Failed to fetch signals:', err);
    return [];
  }
}

export async function fetchPrices(): Promise<Price[]> {
  try {
    const res = await fetch(`${API_BASE}/prices`);
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error('Failed to fetch prices:', err);
    return [];
  }
}

export async function fetchTrades(): Promise<Trade[]> {
  try {
    const res = await fetch(`${API_BASE}/trades`);
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error('Failed to fetch trades:', err);
    return [];
  }
}
