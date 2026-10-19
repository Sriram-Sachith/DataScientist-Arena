"""Authentication and security utilities"""
import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Header
import secrets
import hashlib

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


class PasswordManager:
    """Manage password hashing and verification"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)


class TokenManager:
    """Manage JWT tokens"""
    
    @staticmethod
    def create_access_token(
        data: dict,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(data: dict) -> str:
        """Create a JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> dict:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    @staticmethod
    def get_user_id_from_token(token: str) -> str:
        """Extract user_id from token"""
        payload = TokenManager.verify_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return user_id


class APIKeyManager:
    """Manage API keys"""
    
    @staticmethod
    def generate_api_key() -> str:
        """Generate a secure random API key"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def hash_api_key(api_key: str) -> str:
        """Hash an API key"""
        return hashlib.sha256(api_key.encode()).hexdigest()
    
    @staticmethod
    def verify_api_key(plain_key: str, hashed_key: str) -> bool:
        """Verify an API key against its hash"""
        return APIKeyManager.hash_api_key(plain_key) == hashed_key


class RBACManager:
    """Role-Based Access Control"""
    
    ROLE_PERMISSIONS = {
        "admin": [
            "create:dataset",
            "read:dataset",
            "update:dataset",
            "delete:dataset",
            "create:experiment",
            "read:experiment",
            "update:experiment",
            "delete:experiment",
            "manage:users",
            "manage:workspace",
            "view:analytics",
        ],
        "researcher": [
            "create:dataset",
            "read:dataset",
            "update:dataset",
            "create:experiment",
            "read:experiment",
            "update:experiment",
            "run:experiment",
            "read:results",
        ],
        "analyst": [
            "read:dataset",
            "create:experiment",
            "read:experiment",
            "run:experiment",
            "read:results",
        ],
        "viewer": [
            "read:dataset",
            "read:experiment",
            "read:results",
        ],
    }
    
    @staticmethod
    def has_permission(role: str, permission: str) -> bool:
        """Check if a role has a specific permission"""
        return permission in RBACManager.ROLE_PERMISSIONS.get(role, [])
    
    @staticmethod
    def get_permissions(role: str) -> list:
        """Get all permissions for a role"""
        return RBACManager.ROLE_PERMISSIONS.get(role, [])


# Dependency for getting current user from token
async def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    """Get current user ID from bearer token"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError("Invalid authentication scheme")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return TokenManager.get_user_id_from_token(token)


# Dependency for verifying API key
async def verify_api_key_header(x_api_key: Optional[str] = None) -> Optional[str]:
    """Verify API key from header"""
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required",
        )
    # In production, look up the key in database
    return x_api_key


# Dependency for checking role permissions
def require_role(*allowed_roles: str):
    """Decorator to require specific roles"""
    async def check_role(current_user: str = Depends(get_current_user)):
        # In production, fetch user role from database
        # For now, return user_id for verification in route
        return current_user
    return check_role
