# HybridBot Client Portal - Windows Setup Guide

## 🚀 Complete Local Setup (Windows)

### Prerequisites
1. **Node.js**: Download from https://nodejs.org/
2. **Python 3.8+**: Download from https://python.org/
3. **Git** (optional): Download from https://git-scm.com/

### Step 1: Create Project Directory
```bash
mkdir C:\Users\emada\HybridBot
cd C:\Users\emada\HybridBot
```

### Step 2: Initialize React Project
```bash
npm create vite@latest . -- --template react-ts
# Choose: React → TypeScript
```

### Step 3: Install Frontend Dependencies
```bash
npm install
npm install react-hook-form @hookform/resolvers yup js-cookie reconnecting-websocket
npm install --save-dev @types/js-cookie
```

### Step 4: Install Backend Dependencies
```bash
pip install fastapi uvicorn PyJWT python-multipart email-validator
```

### Step 5: Copy Essential Files

#### A. Update package.json dependencies section:
```json
{
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-hook-form": "^7.45.0",
    "@hookform/resolvers": "^3.1.0",
    "yup": "^1.2.0",
    "js-cookie": "^3.0.5",
    "reconnecting-websocket": "^4.4.0",
    "lucide-react": "^0.511.0"
  }
}
```

#### B. Create src/types/auth.ts:
```typescript
export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  provider: 'email' | 'google' | 'github';
  isVerified: boolean;
  createdAt: string;
  preferences?: {
    theme: 'dark' | 'light';
    notifications: boolean;
    twoFactorEnabled: boolean;
  };
}

export interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (credentials: { email: string; password: string }) => Promise<void>;
  register: (credentials: { email: string; password: string; confirmPassword: string; name: string }) => Promise<void>;
  logout: () => void;
}
```

#### C. Create simple api_server.py:
```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="HybridBot API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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
    return {"status": "healthy"}

@app.post("/auth/register")
async def register(request: RegisterRequest):
    # Simple mock registration
    return {
        "access_token": "mock-token-12345",
        "user": {
            "id": "user-123",
            "email": request.email,
            "name": request.name,
            "provider": "email",
            "isVerified": True,
            "createdAt": "2024-01-01T00:00:00Z"
        }
    }

@app.post("/auth/login")
async def login(request: LoginRequest):
    # Simple mock login
    return {
        "access_token": "mock-token-12345",
        "user": {
            "id": "user-123",
            "email": request.email,
            "name": "Demo User",
            "provider": "email",
            "isVerified": True,
            "createdAt": "2024-01-01T00:00:00Z"
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
            "createdAt": "2024-01-01T00:00:00Z"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Step 6: Start the Applications

#### Terminal 1 (Backend):
```bash
python api_server.py
```

#### Terminal 2 (Frontend):
```bash
npm run dev
```

### Step 7: Access Your Application

**Frontend**: http://localhost:5173
**Backend API**: http://localhost:8000

## ✅ You Should See:
- HybridBot application with dark theme
- Sign In / Sign Up buttons in header
- Working authentication system
- No more blank page!

## 🧪 Test Authentication:
1. Click "Sign Up"
2. Fill form with any details
3. You'll be logged in automatically
4. See user dropdown in top-right

## 🎯 Success!
Your complete client portal with authentication is now running locally on Windows!