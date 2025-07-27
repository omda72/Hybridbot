from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="HybridBot Test API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RegisterRequest(BaseModel):
    email: str
    password: str
    confirmPassword: str
    name: str

class LoginRequest(BaseModel):
    email: str
    password: str

@app.get("/")
async def root():
    return {"message": "HybridBot API is running!", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

@app.post("/auth/register")
async def register(request: RegisterRequest):
    print(f"Registration attempt: {request.email}")
    return {
        "access_token": "demo-token-12345",
        "user": {
            "id": "user-123",
            "email": request.email,
            "name": request.name,
            "provider": "email",
            "isVerified": True,
            "createdAt": "2024-01-01T00:00:00Z",
            "preferences": {
                "theme": "dark",
                "notifications": True,
                "twoFactorEnabled": False
            }
        }
    }

@app.post("/auth/login")
async def login(request: LoginRequest):
    print(f"Login attempt: {request.email}")
    return {
        "access_token": "demo-token-12345",
        "user": {
            "id": "user-123",
            "email": request.email,
            "name": "Demo User",
            "provider": "email",
            "isVerified": True,
            "createdAt": "2024-01-01T00:00:00Z",
            "preferences": {
                "theme": "dark",
                "notifications": True,
                "twoFactorEnabled": False
            }
        }
    }

@app.get("/auth/me")
async def get_current_user():
    return {
        "user": {
            "id": "user-123",
            "email": "demo@example.com",
            "name": "Demo User",
            "provider": "email",
            "isVerified": True,
            "createdAt": "2024-01-01T00:00:00Z",
            "preferences": {
                "theme": "dark",
                "notifications": True,
                "twoFactorEnabled": False
            }
        }
    }

# Mock endpoints for the frontend
@app.get("/bots")
async def get_bots():
    return []

@app.get("/portfolio")
async def get_portfolio():
    return {"totalValue": 0, "totalPnl": 0, "totalPnlPercent": 0, "assets": []}

@app.get("/trades")
async def get_trades():
    return []

@app.get("/signals")
async def get_signals():
    return []

@app.get("/prices")
async def get_prices():
    return []

if __name__ == "__main__":
    print("🚀 Starting HybridBot Test API...")
    print("📍 API will be available at: http://localhost:8000")
    print("🌐 Frontend should connect to: http://localhost:5173")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
