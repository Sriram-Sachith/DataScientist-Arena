"""User authentication and profile management endpoints"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from datetime import datetime, timedelta
import uuid

from app.core.auth import (
    PasswordManager, 
    TokenManager, 
    get_current_user,
    RBACManager
)
from app.schemas.user import (
    UserRegister,
    UserLogin,
    TokenResponse,
    UserProfile,
    UserUpdate,
    UserPreferences,
    UserPreferencesUpdate,
    UserStats,
    DashboardData
)

router = APIRouter(prefix="/users", tags=["users"])

# Mock database for demonstration
USERS_DB = {}
USER_SESSIONS = {}


@router.post("/register", response_model=UserProfile, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister) -> UserProfile:
    """Register a new user"""
    
    # Check if username already exists
    for user in USERS_DB.values():
        if user["username"] == user_data.username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists"
            )
        if user["email"] == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
    
    user_id = str(uuid.uuid4())
    hashed_password = PasswordManager.hash_password(user_data.password)
    
    USERS_DB[user_id] = {
        "id": user_id,
        "username": user_data.username,
        "email": user_data.email,
        "full_name": user_data.full_name,
        "hashed_password": hashed_password,
        "avatar_url": None,
        "bio": None,
        "organization": None,
        "role": "researcher",
        "created_at": datetime.utcnow(),
        "last_login": None,
        "is_verified": False,
        "is_active": True,
        "preferences": {
            "auto_save": True,
            "show_tooltips": True,
            "default_analysis_approach": "independent_verification",
            "export_format": "pdf"
        }
    }
    
    return UserProfile(**USERS_DB[user_id])


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin) -> TokenResponse:
    """Login user and return access token"""
    
    # Find user by username
    user = None
    user_id = None
    for uid, u in USERS_DB.items():
        if u["username"] == credentials.username:
            user = u
            user_id = uid
            break
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Verify password
    if not PasswordManager.verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Update last login
    user["last_login"] = datetime.utcnow()
    
    # Create tokens
    access_token = TokenManager.create_access_token({"sub": user_id})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=1800,
        user=UserProfile(**user)
    )


@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(current_user_id: str = Depends(get_current_user)) -> UserProfile:
    """Get current user profile"""
    
    if current_user_id not in USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserProfile(**USERS_DB[current_user_id])


@router.put("/me", response_model=UserProfile)
async def update_profile(
    user_update: UserUpdate,
    current_user_id: str = Depends(get_current_user)
) -> UserProfile:
    """Update user profile"""
    
    if current_user_id not in USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user = USERS_DB[current_user_id]
    
    # Update fields
    if user_update.full_name is not None:
        user["full_name"] = user_update.full_name
    if user_update.bio is not None:
        user["bio"] = user_update.bio
    if user_update.avatar_url is not None:
        user["avatar_url"] = user_update.avatar_url
    if user_update.organization is not None:
        user["organization"] = user_update.organization
    if user_update.theme is not None:
        user["theme"] = user_update.theme
    if user_update.language is not None:
        user["language"] = user_update.language
    if user_update.timezone is not None:
        user["timezone"] = user_update.timezone
    
    return UserProfile(**user)


@router.get("/me/preferences", response_model=UserPreferences)
async def get_preferences(current_user_id: str = Depends(get_current_user)) -> UserPreferences:
    """Get user preferences"""
    
    if current_user_id not in USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    prefs = USERS_DB[current_user_id]["preferences"]
    return UserPreferences(**prefs)


@router.put("/me/preferences", response_model=UserPreferences)
async def update_preferences(
    prefs_update: UserPreferencesUpdate,
    current_user_id: str = Depends(get_current_user)
) -> UserPreferences:
    """Update user preferences"""
    
    if current_user_id not in USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user = USERS_DB[current_user_id]
    prefs = user["preferences"]
    
    # Update preferences
    update_data = prefs_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            prefs[key] = value
    
    return UserPreferences(**prefs)


@router.get("/me/stats", response_model=UserStats)
async def get_user_stats(current_user_id: str = Depends(get_current_user)) -> UserStats:
    """Get user statistics"""
    
    if current_user_id not in USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Mock statistics
    return UserStats(
        total_datasets=5,
        total_experiments=12,
        completed_experiments=10,
        active_experiments=2,
        average_accuracy=0.847,
        total_storage_mb=1250.5,
        api_calls_today=342,
        last_activity=datetime.utcnow()
    )


@router.get("/me/dashboard", response_model=DashboardData)
async def get_dashboard(current_user_id: str = Depends(get_current_user)) -> DashboardData:
    """Get personalized dashboard data"""
    
    if current_user_id not in USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user = USERS_DB[current_user_id]
    
    # Mock dashboard data
    return DashboardData(
        user=UserProfile(**user),
        stats=UserStats(
            total_datasets=5,
            total_experiments=12,
            completed_experiments=10,
            active_experiments=2,
            average_accuracy=0.847,
            total_storage_mb=1250.5,
            api_calls_today=342,
            last_activity=datetime.utcnow()
        ),
        recent_experiments=[
            {
                "id": "exp_1",
                "name": "Churn Prediction Q4",
                "status": "completed",
                "accuracy": 0.89,
                "created_at": datetime.utcnow()
            }
        ],
        recent_datasets=[
            {
                "id": "ds_1",
                "name": "Customer Data",
                "rows": 10000,
                "columns": 15,
                "created_at": datetime.utcnow()
            }
        ],
        upcoming_notifications=[],
        workspace=None
    )


@router.post("/logout")
async def logout(current_user_id: str = Depends(get_current_user)):
    """Logout user"""
    # In production, invalidate tokens or clear sessions
    return {"message": "Successfully logged out"}


@router.post("/refresh-token", response_model=TokenResponse)
async def refresh_token(current_user_id: str = Depends(get_current_user)) -> TokenResponse:
    """Refresh access token"""
    
    if current_user_id not in USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user = USERS_DB[current_user_id]
    access_token = TokenManager.create_access_token({"sub": current_user_id})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=1800,
        user=UserProfile(**user)
    )
