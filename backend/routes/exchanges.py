from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

router = APIRouter(prefix="/exchanges", tags=["exchanges"])

@router.get("/")
async def get_exchanges():
    """Get list of supported exchanges"""
    return {
        "exchanges": [
            "binance",
            "coinbase",
            "kucoin"
        ]
    }

@router.get("/{exchange_name}/status")
async def get_exchange_status(exchange_name: str):
    """Get status of a specific exchange"""
    supported_exchanges = ["binance", "coinbase", "kucoin"]
    
    if exchange_name.lower() not in supported_exchanges:
        raise HTTPException(status_code=404, detail="Exchange not supported")
    
    return {
        "exchange": exchange_name,
        "status": "connected",
        "last_updated": "2024-01-01T00:00:00Z"
    }