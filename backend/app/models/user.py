"""User and personalization models"""
from sqlalchemy import Column, String, Integer, DateTime, Float, Boolean, JSON, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
import uuid
from app.database import Base


class UserRole(str, PyEnum):
    """User role enumeration"""
    ADMIN = "admin"
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    VIEWER = "viewer"


class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)
    
    # Profile
    bio = Column(String)
    avatar_url = Column(String)
    organization = Column(String)
    role = Column(Enum(UserRole), default=UserRole.RESEARCHER)
    
    # Settings
    theme = Column(String, default="dark")  # dark, light
    language = Column(String, default="en")
    timezone = Column(String, default="UTC")
    notifications_enabled = Column(Boolean, default=True)
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Preferences (JSON)
    preferences = Column(JSON, default={
        "auto_save": True,
        "show_tooltips": True,
        "default_analysis_approach": "independent_verification",
        "export_format": "pdf"
    })
    
    # Relationships
    owned_datasets = relationship("Dataset", back_populates="owner", foreign_keys="Dataset.owner_id")
    owned_experiments = relationship("Experiment", back_populates="owner", foreign_keys="Experiment.owner_id")
    api_keys = relationship("APIKey", back_populates="user")
    workspaces = relationship("Workspace", back_populates="owner")
    workspace_members = relationship("WorkspaceMember", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    activity_logs = relationship("ActivityLog", back_populates="user")
    saved_templates = relationship("ExperimentTemplate", back_populates="creator")


class APIKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    key = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    description = Column(String)
    
    # Permissions
    scopes = Column(JSON, default=[
        "read:datasets",
        "read:experiments",
        "read:results"
    ])
    
    # Access control
    is_active = Column(Boolean, default=True)
    rate_limit = Column(Integer, default=1000)  # requests per hour
    last_used = Column(DateTime, nullable=True)
    ip_whitelist = Column(JSON, nullable=True)  # List of allowed IPs
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="api_keys")


class Workspace(Base):
    __tablename__ = "workspaces"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    slug = Column(String, unique=True, index=True)
    
    # Settings
    logo_url = Column(String)
    color_scheme = Column(String)
    settings = Column(JSON, default={})
    
    # Access control
    is_private = Column(Boolean, default=True)
    default_role = Column(Enum(UserRole), default=UserRole.ANALYST)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="workspaces")
    members = relationship("WorkspaceMember", back_populates="workspace")
    datasets = relationship("Dataset", back_populates="workspace")
    experiments = relationship("Experiment", back_populates="workspace")


class WorkspaceMember(Base):
    __tablename__ = "workspace_members"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workspace_id = Column(String, ForeignKey("workspaces.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.ANALYST)
    
    # Permissions (override workspace defaults)
    permissions = Column(JSON, default={})
    
    # Timestamps
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="members")
    user = relationship("User", back_populates="workspace_members")


class ExperimentTemplate(Base):
    __tablename__ = "experiment_templates"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    creator_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    category = Column(String)  # "churn", "fraud", "classification", etc.
    
    # Template configuration
    default_approach = Column(String)
    analysis_steps = Column(JSON)
    recommended_techniques = Column(JSON)
    template_config = Column(JSON)
    
    # Metadata
    is_public = Column(Boolean, default=False)
    usage_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    creator = relationship("User", back_populates="saved_templates")


class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    message = Column(String)
    notification_type = Column(String)  # "experiment_complete", "verification_done", etc.
    
    # Content
    related_entity_type = Column(String)  # "experiment", "dataset", etc.
    related_entity_id = Column(String)
    data = Column(JSON)
    
    # Status
    is_read = Column(Boolean, default=False)
    action_url = Column(String)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    read_at = Column(DateTime, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="notifications")


class ActivityLog(Base):
    __tablename__ = "activity_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    action = Column(String)  # "create", "update", "delete", "view", etc.
    entity_type = Column(String)  # "dataset", "experiment", etc.
    entity_id = Column(String)
    
    # Details
    details = Column(JSON)
    ip_address = Column(String)
    user_agent = Column(String)
    
    # Status
    success = Column(Boolean, default=True)
    error_message = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="activity_logs")
