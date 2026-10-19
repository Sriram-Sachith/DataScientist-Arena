"""SQLAlchemy ORM models for DataScientist Arena"""
from sqlalchemy import Column, String, Integer, DateTime, Float, Boolean, JSON, ForeignKey, Text, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
import uuid
from app.database import Base, engine


# ============================================================================
# ENUMS
# ============================================================================

class UserRole(str, PyEnum):
    """User role enumeration"""
    ADMIN = "admin"
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    VIEWER = "viewer"


class ExperimentStatusEnum(str, PyEnum):
    """Experiment status"""
    CREATED = "created"
    VALIDATING = "validating"
    PLANNING = "planning"
    EXECUTING = "executing"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    FAILED = "failed"


# ============================================================================
# USER & ACCOUNT MODELS
# ============================================================================

class User(Base):
    """User account model"""
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
    api_keys = relationship("APIKey", back_populates="user", cascade="all, delete-orphan")
    workspaces = relationship("Workspace", back_populates="owner", cascade="all, delete-orphan")
    workspace_members = relationship("WorkspaceMember", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    activity_logs = relationship("ActivityLog", back_populates="user", cascade="all, delete-orphan")
    saved_templates = relationship("ExperimentTemplate", back_populates="creator", cascade="all, delete-orphan")


class APIKey(Base):
    """API key model for programmatic access"""
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


# ============================================================================
# WORKSPACE & COLLABORATION MODELS
# ============================================================================

class Workspace(Base):
    """Team workspace for collaboration"""
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
    members = relationship("WorkspaceMember", back_populates="workspace", cascade="all, delete-orphan")
    datasets = relationship("Dataset", back_populates="workspace")
    experiments = relationship("Experiment", back_populates="workspace")


class WorkspaceMember(Base):
    """Workspace membership model"""
    __tablename__ = "workspace_members"
    __table_args__ = (
        UniqueConstraint('workspace_id', 'user_id', name='uq_workspace_member'),
    )
    
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


# ============================================================================
# DATASET MODELS
# ============================================================================

class Dataset(Base):
    """Dataset upload and management"""
    __tablename__ = "datasets"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String, ForeignKey("users.id"), nullable=True)
    workspace_id = Column(String, ForeignKey("workspaces.id"), nullable=True)
    
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    file_path = Column(String)
    rows = Column(Integer)
    columns = Column(Integer)
    
    # Metadata
    tags = Column(JSON, default=[])
    source = Column(String)
    license = Column(String)
    file_hash = Column(String, unique=True)
    
    # Data profiling
    profile = Column(JSON)  # Quality report
    
    # Access control
    is_public = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    
    # Task-specific metadata
    target_column = Column(String, nullable=True)
    task_type = Column(String, nullable=True)  # classification, regression
    
    # Status
    status = Column(String, default="ready")  # ready, processing, error
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="owned_datasets", foreign_keys=[owner_id])
    workspace = relationship("Workspace", back_populates="datasets")
    experiments = relationship("Experiment", back_populates="dataset", cascade="all, delete-orphan")


# ============================================================================
# EXPERIMENT MODELS
# ============================================================================

class Experiment(Base):
    """Experiment configuration and setup"""
    __tablename__ = "experiments"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_id = Column(String, ForeignKey("datasets.id"), index=True, nullable=False)
    workspace_id = Column(String, ForeignKey("workspaces.id"), nullable=True)
    owner_id = Column(String, ForeignKey("users.id"), nullable=True)
    
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    research_question = Column(String)
    
    # Configuration
    config = Column(JSON)  # Complete experiment config
    target_column = Column(String)
    task_type = Column(String)  # classification, regression
    
    # Status
    status = Column(String, default="setup")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    dataset = relationship("Dataset", back_populates="experiments")
    workspace = relationship("Workspace", back_populates="experiments")
    owner = relationship("User", back_populates="owned_experiments", foreign_keys=[owner_id])
    runs = relationship("Run", back_populates="experiment", cascade="all, delete-orphan")
    analysis_plans = relationship("AnalysisPlan", back_populates="experiment", cascade="all, delete-orphan")


class Run(Base):
    """Experiment run/execution"""
    __tablename__ = "runs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    experiment_id = Column(String, ForeignKey("experiments.id"), index=True, nullable=False)
    
    approach = Column(String)  # baseline, ai_generated, verified_ai
    
    # Execution
    status = Column(String, default="created")
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    runtime_seconds = Column(Float, nullable=True)
    
    # Results
    metrics = Column(JSON)  # Model metrics (accuracy, precision, etc.)
    analysis = Column(JSON)  # Feature analysis and statistics
    insights = Column(JSON)  # Generated insights
    predictions = Column(JSON, nullable=True)  # Predictions from model
    verification = Column(JSON, nullable=True)  # Verification results
    
    # Error handling
    error_message = Column(String, nullable=True)
    error_traceback = Column(Text, nullable=True)
    
    # Relationships
    experiment = relationship("Experiment", back_populates="runs")
    verifications = relationship("Verification", back_populates="run", cascade="all, delete-orphan")


class AnalysisPlan(Base):
    """AI-generated or manual analysis plan"""
    __tablename__ = "analysis_plans"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    experiment_id = Column(String, ForeignKey("experiments.id"), index=True, nullable=False)
    
    plan_text = Column(Text)
    generated_by = Column(String)  # ai, manual
    approach = Column(String)
    
    # Plan components (JSON)
    preprocessing_steps = Column(JSON)
    candidate_models = Column(JSON)
    metrics = Column(JSON)
    reasoning = Column(String)
    
    # Validation
    validation_status = Column(String)  # valid, invalid, needs_review
    rejection_reason = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    experiment = relationship("Experiment", back_populates="analysis_plans")


# ============================================================================
# VERIFICATION MODELS
# ============================================================================

class Verification(Base):
    """Independent verification of experiment results"""
    __tablename__ = "verifications"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    run_id = Column(String, ForeignKey("runs.id"), index=True, nullable=False)
    
    verified_by = Column(String)  # expert, independent_ai
    
    # Verification results
    accuracy = Column(Float, nullable=True)
    errors_found = Column(Integer, default=0)
    error_details = Column(JSON)
    
    # Status
    status = Column(String, default="completed")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    run = relationship("Run", back_populates="verifications")


class ExperimentResult(Base):
    """Aggregated results for experiment"""
    __tablename__ = "experiment_results"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    experiment_id = Column(String, ForeignKey("experiments.id"), index=True, nullable=False)
    
    # Results from different approaches
    ai_baseline_accuracy = Column(Float, nullable=True)
    verification_accuracy = Column(Float, nullable=True)
    manual_accuracy = Column(Float, nullable=True)
    
    ai_baseline_errors = Column(Integer, nullable=True)
    verification_errors = Column(Integer, nullable=True)
    manual_errors = Column(Integer, nullable=True)
    
    # Analysis
    improvement_percentage = Column(Float, nullable=True)
    insights = Column(JSON)  # Comparative insights
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)


# ============================================================================
# TEMPLATE MODELS
# ============================================================================

class ExperimentTemplate(Base):
    """Reusable experiment template"""
    __tablename__ = "experiment_templates"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    creator_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    name = Column(String, nullable=False)
    description = Column(String)
    category = Column(String)  # churn, fraud, classification, etc.
    
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


# ============================================================================
# NOTIFICATION & ACTIVITY MODELS
# ============================================================================

class Notification(Base):
    """User notification"""
    __tablename__ = "notifications"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    title = Column(String, nullable=False)
    message = Column(String)
    notification_type = Column(String)  # experiment_complete, verification_done, etc.
    
    # Content
    related_entity_type = Column(String)  # experiment, dataset, etc.
    related_entity_id = Column(String)
    data = Column(JSON)
    
    # Status
    is_read = Column(Boolean, default=False)
    action_url = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    read_at = Column(DateTime, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="notifications")


class ActivityLog(Base):
    """User activity audit log"""
    __tablename__ = "activity_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    action = Column(String)  # create, update, delete, view, etc.
    entity_type = Column(String)  # dataset, experiment, etc.
    entity_id = Column(String)
    
    # Details
    details = Column(JSON)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    
    # Status
    success = Column(Boolean, default=True)
    error_message = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationship
    user = relationship("User", back_populates="activity_logs")
