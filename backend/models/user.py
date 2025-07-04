from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid
import json

class UserProvider(str, Enum):
    EMAIL = "email"
    GOOGLE = "google"
    GITHUB = "github"

class UserPreferences:
    def __init__(self, theme: str = "dark", notifications: bool = True, two_factor_enabled: bool = False):
        self.theme = theme
        self.notifications = notifications
        self.two_factor_enabled = two_factor_enabled

    def to_dict(self) -> Dict[str, Any]:
        return {
            "theme": self.theme,
            "notifications": self.notifications,
            "twoFactorEnabled": self.two_factor_enabled
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserPreferences':
        return cls(
            theme=data.get("theme", "dark"),
            notifications=data.get("notifications", True),
            two_factor_enabled=data.get("twoFactorEnabled", False)
        )

class User:
    def __init__(
        self,
        id: str = None,
        email: str = "",
        name: str = "",
        password_hash: str = "",
        avatar: Optional[str] = None,
        provider: UserProvider = UserProvider.EMAIL,
        provider_id: Optional[str] = None,
        is_verified: bool = False,
        verification_token: Optional[str] = None,
        reset_token: Optional[str] = None,
        reset_token_expires: Optional[datetime] = None,
        preferences: Optional[UserPreferences] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        last_login: Optional[datetime] = None
    ):
        self.id = id or str(uuid.uuid4())
        self.email = email
        self.name = name
        self.password_hash = password_hash
        self.avatar = avatar
        self.provider = provider
        self.provider_id = provider_id
        self.is_verified = is_verified
        self.verification_token = verification_token
        self.reset_token = reset_token
        self.reset_token_expires = reset_token_expires
        self.preferences = preferences or UserPreferences()
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.last_login = last_login

    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        data = {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "avatar": self.avatar,
            "provider": self.provider.value,
            "isVerified": self.is_verified,
            "preferences": self.preferences.to_dict(),
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "lastLogin": self.last_login.isoformat() if self.last_login else None
        }
        
        if include_sensitive:
            data.update({
                "password_hash": self.password_hash,
                "provider_id": self.provider_id,
                "verification_token": self.verification_token,
                "reset_token": self.reset_token,
                "reset_token_expires": self.reset_token_expires.isoformat() if self.reset_token_expires else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None
            })
        
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        return cls(
            id=data.get("id"),
            email=data.get("email", ""),
            name=data.get("name", ""),
            password_hash=data.get("password_hash", ""),
            avatar=data.get("avatar"),
            provider=UserProvider(data.get("provider", UserProvider.EMAIL.value)),
            provider_id=data.get("provider_id"),
            is_verified=data.get("isVerified", False),
            verification_token=data.get("verification_token"),
            reset_token=data.get("reset_token"),
            reset_token_expires=datetime.fromisoformat(data["reset_token_expires"]) if data.get("reset_token_expires") else None,
            preferences=UserPreferences.from_dict(data.get("preferences", {})),
            created_at=datetime.fromisoformat(data["createdAt"]) if data.get("createdAt") else None,
            updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else None,
            last_login=datetime.fromisoformat(data["lastLogin"]) if data.get("lastLogin") else None
        )

    def update_login_time(self):
        """Update the last login timestamp"""
        self.last_login = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def update_preferences(self, preferences: Dict[str, Any]):
        """Update user preferences"""
        if "theme" in preferences:
            self.preferences.theme = preferences["theme"]
        if "notifications" in preferences:
            self.preferences.notifications = preferences["notifications"]
        if "twoFactorEnabled" in preferences:
            self.preferences.two_factor_enabled = preferences["twoFactorEnabled"]
        self.updated_at = datetime.utcnow()

# Simple in-memory user storage (replace with database in production)
class UserStorage:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.email_index: Dict[str, str] = {}  # email -> user_id

    def create_user(self, user: User) -> User:
        """Create a new user"""
        if user.email in self.email_index:
            raise ValueError("User with this email already exists")
        
        self.users[user.id] = user
        self.email_index[user.email] = user.id
        return user

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self.users.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        user_id = self.email_index.get(email)
        return self.users.get(user_id) if user_id else None

    def update_user(self, user: User) -> User:
        """Update existing user"""
        if user.id not in self.users:
            raise ValueError("User not found")
        
        user.updated_at = datetime.utcnow()
        self.users[user.id] = user
        return user

    def delete_user(self, user_id: str) -> bool:
        """Delete user"""
        user = self.users.get(user_id)
        if not user:
            return False
        
        del self.users[user_id]
        del self.email_index[user.email]
        return True

# Global user storage instance
user_storage = UserStorage()