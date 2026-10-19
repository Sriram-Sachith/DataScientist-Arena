"""Pydantic schemas for dataset operations"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class DataTypeEnum(str, Enum):
    """Data type enumeration"""
    NUMERIC = "numeric"
    CATEGORICAL = "categorical"
    TEMPORAL = "temporal"
    TEXT = "text"

class ColumnProfile(BaseModel):
    """Schema for column profiling information"""
    name: str
    dtype: DataTypeEnum
    non_null_count: int
    null_percentage: float
    unique_count: int
    constant: bool
    
    # Numeric stats
    mean: Optional[float] = None
    std: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None
    
    # Categorical stats
    top_categories: Optional[List[str]] = None
    cardinality: Optional[int] = None

class DatasetQualityReport(BaseModel):
    """Dataset quality assessment"""
    total_rows: int
    total_columns: int
    memory_usage_mb: float
    duplicate_rows: int
    duplicate_percentage: float
    missing_cells_percentage: float
    columns: List[ColumnProfile]
    warnings: List[str] = []
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_rows": 1000,
                "total_columns": 10,
                "memory_usage_mb": 0.5,
                "duplicate_rows": 5,
                "duplicate_percentage": 0.5,
                "missing_cells_percentage": 2.3,
                "columns": [],
                "warnings": ["High missing value percentage in age column"]
            }
        }

class DatasetMetadata(BaseModel):
    """Dataset metadata"""
    id: str
    name: str
    description: Optional[str] = None
    source: str
    license: str
    rows: int
    columns: int
    file_hash: str
    created_at: datetime
    version: int = 1
    target_column: Optional[str] = None
    task_type: Optional[str] = None  # classification, regression, clustering

class DatasetUploadRequest(BaseModel):
    """Request for dataset upload"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    source: str = Field(..., min_length=1, max_length=255)
    license: str = Field(default="CC0", max_length=255)
    target_column: Optional[str] = None
    task_type: Optional[str] = None

class DatasetListResponse(BaseModel):
    """Response for dataset list"""
    id: str
    name: str
    rows: int
    columns: int
    task_type: Optional[str]
    created_at: datetime

class DatasetDetailResponse(BaseModel):
    """Detailed dataset response"""
    metadata: DatasetMetadata
    quality_report: DatasetQualityReport
    preview: Dict[str, Any]  # First 50 rows as JSON
