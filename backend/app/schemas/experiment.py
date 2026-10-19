"""Schemas for experiment management"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ExperimentStatusEnum(str, Enum):
    """Experiment status"""
    CREATED = "created"
    VALIDATING = "validating"
    PLANNING = "planning"
    EXECUTING = "executing"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    FAILED = "failed"

class ExperimentApproachEnum(str, Enum):
    """Experimental approaches"""
    BASELINE = "baseline"
    AI_GENERATED = "ai_generated"
    VERIFIED_AI = "verified_ai"

class ExperimentConfig(BaseModel):
    """Experiment configuration"""
    dataset_id: str
    target_column: str
    task_type: str  # classification, regression
    train_test_split: float = Field(default=0.8, ge=0.5, le=0.95)
    random_seed: int = Field(default=42)
    validation_strategy: str = "train_test"
    metric_names: List[str]
    max_runtime_seconds: int = 300
    
    class Config:
        json_schema_extra = {
            "example": {
                "dataset_id": "dataset_123",
                "target_column": "target",
                "task_type": "classification",
                "train_test_split": 0.8,
                "random_seed": 42,
                "validation_strategy": "train_test",
                "metric_names": ["accuracy", "precision", "recall", "f1"],
                "max_runtime_seconds": 300
            }
        }

class AnalysisPlan(BaseModel):
    """AI-generated analysis plan"""
    id: str
    experiment_id: str
    model_name: str
    model_version: str
    
    # Plan components
    preprocessing_steps: List[str]
    candidate_models: List[str]
    metrics: List[str]
    reasoning: str
    
    validation_status: str  # valid, invalid, needs_review
    rejection_reason: Optional[str] = None
    
    created_at: datetime

class ExperimentRun(BaseModel):
    """Single experiment run result"""
    id: str
    experiment_id: str
    approach: ExperimentApproachEnum
    
    status: ExperimentStatusEnum
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Results
    metrics: Dict[str, Any] = {}
    analysis: Optional[Dict[str, Any]] = None  # Feature analysis and statistics
    insights: List[str] = []  # Generated insights from analysis
    predictions: Optional[List[Any]] = None
    error_message: Optional[str] = None
    
    # Verification (if applicable)
    verification: Optional[Dict[str, Any]] = None  # Full verification results
    verification_passed: Optional[bool] = None
    verification_findings: List[str] = []
    
    # Resource usage
    runtime_seconds: Optional[float] = None
    model_calls: int = 0

class ExperimentDetail(BaseModel):
    """Detailed experiment view"""
    id: str
    dataset_id: str
    config: ExperimentConfig
    analysis_plan: Optional[AnalysisPlan] = None
    runs: List[ExperimentRun] = []
    created_at: datetime
    updated_at: datetime

class CreateExperimentRequest(BaseModel):
    """Request to create experiment"""
    dataset_id: str
    target_column: str
    task_type: str
    metric_names: List[str]
    train_test_split: float = 0.8
    random_seed: int = 42
    max_runtime_seconds: int = 300
