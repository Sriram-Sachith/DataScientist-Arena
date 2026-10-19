"""User and personalization schemas"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    VIEWER = "viewer"


# User Registration & Login
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserProfile"


class UserProfile(BaseModel):
    id: str
    username: str
    email: str
    full_name: Optional[str]
    avatar_url: Optional[str]
    bio: Optional[str]
    organization: Optional[str]
    role: UserRole
    created_at: datetime
    last_login: Optional[datetime]
    is_verified: bool

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    organization: Optional[str] = None
    theme: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None


class UserPreferences(BaseModel):
    auto_save: bool = True
    show_tooltips: bool = True
    default_analysis_approach: str = "independent_verification"
    export_format: str = "pdf"
    notifications_enabled: bool = True
    email_on_completion: bool = True
    dark_mode: bool = True


class UserPreferencesUpdate(BaseModel):
    auto_save: Optional[bool] = None
    show_tooltips: Optional[bool] = None
    default_analysis_approach: Optional[str] = None
    export_format: Optional[str] = None
    notifications_enabled: Optional[bool] = None
    email_on_completion: Optional[bool] = None
    dark_mode: Optional[bool] = None


# API Keys
class APIKeyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    scopes: List[str] = [
        "read:datasets",
        "read:experiments",
        "read:results"
    ]
    expires_in_days: Optional[int] = None
    ip_whitelist: Optional[List[str]] = None


class APIKeyResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    key: str  # Only shown once on creation
    scopes: List[str]
    is_active: bool
    rate_limit: int
    created_at: datetime
    expires_at: Optional[datetime]
    last_used: Optional[datetime]

    class Config:
        from_attributes = True


class APIKeyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    rate_limit: Optional[int] = None


# Workspaces
class WorkspaceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    is_private: bool = True


class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    color_scheme: Optional[str] = None
    is_private: Optional[bool] = None


class WorkspaceResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    slug: str
    owner_id: str
    is_private: bool
    created_at: datetime
    member_count: int = 0

    class Config:
        from_attributes = True


class WorkspaceMemberAdd(BaseModel):
    user_id: str
    role: UserRole = UserRole.ANALYST


class WorkspaceMemberUpdate(BaseModel):
    role: Optional[UserRole] = None
    permissions: Optional[Dict[str, Any]] = None


class WorkspaceMemberResponse(BaseModel):
    id: str
    user_id: str
    role: UserRole
    joined_at: datetime
    user: Optional[UserProfile]

    class Config:
        from_attributes = True


# Notifications
class NotificationCreate(BaseModel):
    title: str
    message: Optional[str] = None
    notification_type: str
    related_entity_type: Optional[str] = None
    related_entity_id: Optional[str] = None
    action_url: Optional[str] = None


class NotificationResponse(BaseModel):
    id: str
    title: str
    message: Optional[str]
    notification_type: str
    is_read: bool
    created_at: datetime
    action_url: Optional[str]

    class Config:
        from_attributes = True


# Activity Logs
class ActivityLogResponse(BaseModel):
    id: str
    action: str
    entity_type: str
    entity_id: str
    success: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Experiment Templates
class ExperimentTemplateCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    category: Optional[str] = None
    default_approach: str
    analysis_steps: List[str]
    recommended_techniques: List[str]
    is_public: bool = False


class ExperimentTemplateResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    category: Optional[str]
    creator_id: str
    is_public: bool
    usage_count: int
    rating: float
    created_at: datetime

    class Config:
        from_attributes = True


# Dashboard Stats
class UserStats(BaseModel):
    total_datasets: int
    total_experiments: int
    completed_experiments: int
    active_experiments: int
    average_accuracy: float
    total_storage_mb: float
    api_calls_today: int
    last_activity: Optional[datetime]


class DashboardData(BaseModel):
    user: UserProfile
    stats: UserStats
    recent_experiments: List[Dict[str, Any]]
    recent_datasets: List[Dict[str, Any]]
    upcoming_notifications: List[NotificationResponse]
    workspace: Optional[WorkspaceResponse]
