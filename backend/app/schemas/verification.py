"""Schemas for verification operations"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class VerificationCheckEnum(str, Enum):
    """Verification check types"""
    SCHEMA_INTEGRITY = "schema_integrity"
    DATA_SPLITTING = "data_splitting"
    PREPROCESSING_LEAKAGE = "preprocessing_leakage"
    METRIC_CORRECTNESS = "metric_correctness"
    METRIC_SUITABILITY = "metric_suitability"
    PREDICTION_VALIDITY = "prediction_validity"
    REPRODUCIBILITY = "reproducibility"
    STATISTICAL_CLAIMS = "statistical_claims"
    CONCLUSION_SUPPORT = "conclusion_support"

class VerificationSeverityEnum(str, Enum):
    """Severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class VerificationFinding(BaseModel):
    """Single verification finding"""
    id: str
    check_type: VerificationCheckEnum
    status: str  # passed, failed, warning, not_applicable
    severity: VerificationSeverityEnum
    
    description: str
    evidence: str  # Supporting evidence or calculation
    expected: str  # Expected result
    observed: str  # Observed result
    
    suggestion: Optional[str] = None
    fixed: bool = False
    
    created_at: datetime

class VerificationReport(BaseModel):
    """Complete verification report"""
    id: str
    run_id: str
    experiment_id: str
    
    total_checks: int
    passed_checks: int
    failed_checks: int
    warning_checks: int
    
    findings: List[VerificationFinding]
    
    overall_passed: bool
    pass_percentage: float
    
    created_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "verify_123",
                "run_id": "run_456",
                "experiment_id": "exp_789",
                "total_checks": 9,
                "passed_checks": 8,
                "failed_checks": 0,
                "warning_checks": 1,
                "findings": [],
                "overall_passed": True,
                "pass_percentage": 88.9
            }
        }

class VerificationMetrics(BaseModel):
    """Verification quality metrics"""
    plan_validity_rate: float
    undetected_error_rate: float
    verification_recall: float
    false_positive_rate: float
    overhead_percentage: float
    average_runtime: float

class ErrorInjectionCase(BaseModel):
    """Known error case for testing"""
    id: str
    experiment_id: str
    error_type: str  # metric_manipulation, leakage, invalid_split, etc.
    description: str
    injected_value: Any
    original_value: Any
    detected: bool
    detection_message: Optional[str] = None
