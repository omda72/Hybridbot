from fastapi import APIRouter, HTTPException, Depends, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import secrets

from ..models.user import User, UserProvider, user_storage
from ..auth.utils import (
    hash_password, verify_password, create_access_token, verify_access_token,
    validate_email, validate_password, validate_name, generate_verification_token,
    generate_reset_token, get_oauth_auth_url, generate_oauth_state, rate_limiter
)

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

# Request/Response Models
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    confirmPassword: str
    name: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

class UserResponse(BaseModel):
    user: Dict[str, Any]

class MessageResponse(BaseModel):
    message: str

class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None

class ResetPasswordRequest(BaseModel):
    email: EmailStr

# Helper Functions
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current authenticated user"""
    token_data = verify_access_token(credentials.credentials)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = user_storage.get_user_by_id(token_data["user_id"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

def get_client_ip(request: Request) -> str:
    """Get client IP address"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host

# Authentication Endpoints
@router.post("/register", response_model=AuthResponse)
async def register(request: RegisterRequest, req: Request):
    """Register a new user"""
    client_ip = get_client_ip(req)
    
    # Rate limiting
    if rate_limiter.is_rate_limited(f"register:{client_ip}", max_attempts=3, window_minutes=60):
        raise HTTPException(status_code=429, detail="Too many registration attempts. Please try again later.")
    
    # Validate input
    if not validate_email(request.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    if not validate_name(request.name):
        raise HTTPException(status_code=400, detail="Name must be between 2 and 50 characters")
    
    password_validation = validate_password(request.password)
    if not password_validation["valid"]:
        raise HTTPException(status_code=400, detail=f"Password validation failed: {', '.join(password_validation['errors'])}")
    
    if request.password != request.confirmPassword:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    # Check if user already exists
    existing_user = user_storage.get_user_by_email(request.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    # Create new user
    try:
        password_hash = hash_password(request.password)
        verification_token = generate_verification_token()
        
        user = User(
            email=request.email,
            name=request.name.strip(),
            password_hash=password_hash,
            provider=UserProvider.EMAIL,
            is_verified=True,  # Auto-verify for demo purposes
            verification_token=verification_token
        )
        
        user_storage.create_user(user)
        
        # Create access token
        access_token = create_access_token(user.id, user.email)
        
        # Clear rate limit on successful registration
        rate_limiter.clear_attempts(f"register:{client_ip}")
        
        return AuthResponse(
            access_token=access_token,
            user=user.to_dict()
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Registration failed")

@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, req: Request):
    """Login user"""
    client_ip = get_client_ip(req)
    
    # Rate limiting
    if rate_limiter.is_rate_limited(f"login:{client_ip}", max_attempts=5, window_minutes=15):
        raise HTTPException(status_code=429, detail="Too many login attempts. Please try again later.")
    
    # Find user
    user = user_storage.get_user_by_email(request.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Update login time
    user.update_login_time()
    user_storage.update_user(user)
    
    # Create access token
    access_token = create_access_token(user.id, user.email)
    
    # Clear rate limit on successful login
    rate_limiter.clear_attempts(f"login:{client_ip}")
    
    return AuthResponse(
        access_token=access_token,
        user=user.to_dict()
    )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(user=current_user.to_dict())

@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    request: UpdateUserRequest,
    current_user: User = Depends(get_current_user)
):
    """Update current user information"""
    try:
        if request.name is not None:
            if not validate_name(request.name):
                raise HTTPException(status_code=400, detail="Name must be between 2 and 50 characters")
            current_user.name = request.name.strip()
        
        if request.preferences is not None:
            current_user.update_preferences(request.preferences)
        
        user_storage.update_user(current_user)
        
        return UserResponse(user=current_user.to_dict())
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to update user")

@router.post("/resend-verification", response_model=MessageResponse)
async def resend_verification(current_user: User = Depends(get_current_user)):
    """Resend email verification"""
    if current_user.is_verified:
        raise HTTPException(status_code=400, detail="Email is already verified")
    
    # Generate new verification token
    current_user.verification_token = generate_verification_token()
    user_storage.update_user(current_user)
    
    # In production, send email here
    
    return MessageResponse(message="Verification email sent")

@router.post("/reset-password", response_model=MessageResponse)
async def request_password_reset(request: ResetPasswordRequest, req: Request):
    """Request password reset"""
    client_ip = get_client_ip(req)
    
    # Rate limiting
    if rate_limiter.is_rate_limited(f"reset:{client_ip}", max_attempts=3, window_minutes=60):
        raise HTTPException(status_code=429, detail="Too many reset attempts. Please try again later.")
    
    user = user_storage.get_user_by_email(request.email)
    if user:
        # Generate reset token
        user.reset_token = generate_reset_token()
        user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        user_storage.update_user(user)
        
        # In production, send email here
    
    # Always return success for security
    return MessageResponse(message="If the email exists, a reset link has been sent")

# OAuth Endpoints
@router.get("/oauth/{provider}")
async def oauth_login(provider: str, req: Request):
    """Initiate OAuth login"""
    if provider not in ["google", "github"]:
        raise HTTPException(status_code=400, detail="Unsupported OAuth provider")
    
    state = generate_oauth_state()
    auth_url = get_oauth_auth_url(provider, state)
    
    if not auth_url:
        raise HTTPException(status_code=500, detail="OAuth configuration error")
    
    # Store state in session/cache (simplified for demo)
    # In production, use proper session management
    
    return {"auth_url": auth_url, "state": state}

@router.get("/oauth/{provider}/callback")
async def oauth_callback(provider: str, code: str, state: str, req: Request):
    """Handle OAuth callback"""
    if provider not in ["google", "github"]:
        raise HTTPException(status_code=400, detail="Unsupported OAuth provider")
    
    # Verify state parameter (simplified for demo)
    # In production, verify against stored state
    
    try:
        # Exchange code for access token
        # Get user info from OAuth provider
        # Create or update user
        # This is a simplified implementation
        
        # For demo purposes, create a mock OAuth user
        oauth_email = f"oauth.user@{provider}.com"
        oauth_name = f"OAuth User ({provider.title()})"
        
        user = user_storage.get_user_by_email(oauth_email)
        if not user:
            user = User(
                email=oauth_email,
                name=oauth_name,
                provider=UserProvider.GOOGLE if provider == "google" else UserProvider.GITHUB,
                provider_id=f"{provider}_123456",
                is_verified=True
            )
            user_storage.create_user(user)
        
        user.update_login_time()
        user_storage.update_user(user)
        
        # Create access token
        access_token = create_access_token(user.id, user.email)
        
        # Redirect to frontend with token
        return {"access_token": access_token, "user": user.to_dict()}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="OAuth authentication failed")

@router.post("/logout", response_model=MessageResponse)
async def logout(current_user: User = Depends(get_current_user)):
    """Logout user (invalidate token on client side)"""
    # In production, you might want to maintain a blacklist of tokens
    return MessageResponse(message="Successfully logged out")