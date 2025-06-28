from fastapi import FastAPI
from backend.routes.exchanges import router as exchange_router

app = FastAPI(title="HybridBot API")

@app.get("/")
async def read_root():
    return {"message": "HybridBot API is running!"}

app.include_router(exchange_router)

# This block is for local development, not directly used by Cloud Run's CMD
if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)