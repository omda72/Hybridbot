from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.exchanges import router as exchange_router
from backend.routes.auth import router as auth_router

app = FastAPI(title="HybridBot API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "HybridBot API is running!", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

# Include routers
app.include_router(auth_router)
app.include_router(exchange_router)

# This block is for local development, not directly used by Cloud Run's CMD
if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)