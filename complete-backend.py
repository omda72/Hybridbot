from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from datetime import datetime, timedelta
import random

app = FastAPI(title="HybridBot API", version="1.0.0")

# Add CORS middleware to allow browser requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins including file://
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str

# Mock data
users_db = {
    "test@test.com": {"password": "test123", "name": "Test User", "id": "1"},
    "demo@demo.com": {"password": "demo123", "name": "Demo User", "id": "2"}
}

mock_bots = [
    {"id": "1", "name": "BTC Scalper", "status": "running", "profit": 2.5, "trades": 15},
    {"id": "2", "name": "ETH Grid Bot", "status": "paused", "profit": -0.8, "trades": 8},
    {"id": "3", "name": "Multi-Pair Bot", "status": "running", "profit": 5.2, "trades": 23}
]

mock_prices = [
    {"symbol": "BTCUSDT", "price": 43250.50 + random.uniform(-100, 100), "change": round(random.uniform(-5, 5), 2)},
    {"symbol": "ETHUSDT", "price": 2580.25 + random.uniform(-50, 50), "change": round(random.uniform(-3, 3), 2)},
    {"symbol": "ADAUSDT", "price": 0.485 + random.uniform(-0.01, 0.01), "change": round(random.uniform(-2, 2), 2)}
]

mock_trades = [
    {"id": "1", "symbol": "BTCUSDT", "side": "buy", "amount": 0.01, "price": 43200, "timestamp": datetime.now().isoformat()},
    {"id": "2", "symbol": "ETHUSDT", "side": "sell", "amount": 0.5, "price": 2590, "timestamp": datetime.now().isoformat()}
]

# Root endpoint
@app.get("/")
async def root():
    return {"message": "HybridBot API is running!", "version": "1.0.0", "endpoints": [
        "/auth/login", "/auth/register", "/bots", "/portfolio", "/prices", "/trades", "/signals"
    ]}

# Authentication endpoints
@app.post("/auth/login")
async def login(request: LoginRequest):
    user = users_db.get(request.email)
    if not user or user["password"] != request.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return {
        "access_token": f"fake_token_{user['id']}",
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": request.email,
            "name": user["name"],
            "isEmailVerified": True
        }
    }

@app.post("/auth/register")
async def register(request: RegisterRequest):
    if request.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_id = str(len(users_db) + 1)
    users_db[request.email] = {
        "password": request.password,
        "name": request.name,
        "id": new_id
    }
    
    return {
        "access_token": f"fake_token_{new_id}",
        "token_type": "bearer",
        "user": {
            "id": new_id,
            "email": request.email,
            "name": request.name,
            "isEmailVerified": False
        }
    }

@app.get("/auth/me")
async def get_profile():
    return {
        "id": "1",
        "email": "test@test.com",
        "name": "Test User",
        "isEmailVerified": True
    }

# Trading endpoints
@app.get("/bots")
async def get_bots():
    return {"bots": mock_bots}

@app.get("/portfolio")
async def get_portfolio():
    return {
        "balance": 12450.75,
        "pnl": 6.9,
        "trades": 46,
        "last_updated": datetime.now().isoformat()
    }

@app.get("/prices")
async def get_prices():
    # Update prices with small random changes
    for price in mock_prices:
        price["price"] = round(price["price"] + random.uniform(-5, 5), 2)
        price["change"] = round(random.uniform(-3, 3), 2)
    
    return {"prices": mock_prices}

@app.get("/trades")
async def get_trades():
    return {"trades": mock_trades}

@app.get("/signals")
async def get_signals():
    return {
        "signals": [
            {"symbol": "BTCUSDT", "signal": "BUY", "strength": 0.8, "timestamp": datetime.now().isoformat()},
            {"symbol": "ETHUSDT", "signal": "HOLD", "strength": 0.6, "timestamp": datetime.now().isoformat()}
        ]
    }

# Additional endpoints for completeness
@app.post("/bots")
async def create_bot():
    return {"message": "Bot creation feature coming soon!"}

@app.get("/analytics")
async def get_analytics():
    return {"message": "Analytics feature coming soon!"}

@app.get("/settings")
async def get_settings():
    return {"message": "Settings feature coming soon!"}

if __name__ == "__main__":
    print("🚀 Starting Complete HybridBot API...")
    print("📍 API will be available at: http://localhost:8000")
    print("🌐 Frontend should connect successfully!")
    print("📊 Available endpoints:")
    print("   - GET  /")
    print("   - POST /auth/login")
    print("   - POST /auth/register") 
    print("   - GET  /auth/me")
    print("   - GET  /bots")
    print("   - GET  /portfolio")
    print("   - GET  /prices")
    print("   - GET  /trades")
    print("   - GET  /signals")
    print("\n💡 Test credentials:")
    print("   Email: test@test.com")
    print("   Password: test123")
    print("\n🔧 CORS enabled for all origins")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")