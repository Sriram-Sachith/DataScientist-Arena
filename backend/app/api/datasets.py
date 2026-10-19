"""API routes for dataset operations"""

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Depends
from typing import List
import pandas as pd
import hashlib
from datetime import datetime
import json
import os
from sqlalchemy.orm import Session

from app.schemas.dataset import (
    DatasetMetadata, DatasetDetailResponse, DatasetUploadRequest,
    DatasetListResponse, DatasetQualityReport, ColumnProfile, DataTypeEnum
)
from app.core.config import settings
from app.database import get_db
from app.services.database_service import DatabaseService

router = APIRouter()

# In-memory storage for file data (replace with file storage in production)
DATASET_FILES: dict = {}

def calculate_file_hash(file_bytes: bytes) -> str:
    """Calculate SHA256 hash of file"""
    return hashlib.sha256(file_bytes).hexdigest()

def profile_dataset(df: pd.DataFrame) -> DatasetQualityReport:
    """Generate quality report for dataset"""
    warnings = []
    
    # Check for duplicates
    duplicate_rows = df.duplicated().sum()
    duplicate_percentage = (duplicate_rows / len(df)) * 100 if len(df) > 0 else 0
    
    # Check for missing values
    missing_cells = df.isna().sum().sum()
    total_cells = df.shape[0] * df.shape[1]
    missing_percentage = (missing_cells / total_cells) * 100 if total_cells > 0 else 0
    
    # Profile columns
    columns = []
    for col in df.columns:
        non_null = df[col].notna().sum()
        null_percentage = (df[col].isna().sum() / len(df)) * 100 if len(df) > 0 else 0
        unique_count = df[col].nunique()
        is_constant = unique_count <= 1
        
        # Determine data type
        if pd.api.types.is_numeric_dtype(df[col]):
            dtype = DataTypeEnum.NUMERIC
            profile_col = ColumnProfile(
                name=col,
                dtype=dtype,
                non_null_count=non_null,
                null_percentage=null_percentage,
                unique_count=unique_count,
                constant=is_constant,
                mean=float(df[col].mean()),
                std=float(df[col].std()),
                min=float(df[col].min()),
                max=float(df[col].max())
            )
        else:
            dtype = DataTypeEnum.CATEGORICAL
            top_cats = df[col].value_counts().head(5).index.tolist()
            profile_col = ColumnProfile(
                name=col,
                dtype=dtype,
                non_null_count=non_null,
                null_percentage=null_percentage,
                unique_count=unique_count,
                constant=is_constant,
                top_categories=top_cats,
                cardinality=unique_count
            )
        
        columns.append(profile_col)
        
        # Add warnings
        if null_percentage > 20:
            warnings.append(f"High missing values ({null_percentage:.1f}%) in column '{col}'")
        if is_constant:
            warnings.append(f"Constant column detected: '{col}'")
    
    # Memory usage
    memory_usage = df.memory_usage(deep=True).sum() / (1024 * 1024)
    
    return DatasetQualityReport(
        total_rows=len(df),
        total_columns=len(df.columns),
        memory_usage_mb=memory_usage,
        duplicate_rows=duplicate_rows,
        duplicate_percentage=duplicate_percentage,
        missing_cells_percentage=missing_percentage,
        columns=columns,
        warnings=warnings
    )

@router.post("/datasets", response_model=DatasetMetadata, tags=["datasets"])
async def upload_dataset(
    file: UploadFile = File(...),
    name: str = None,
    description: str = None,
    source: str = "user_upload",
    license: str = "CC0",
    target_column: str = None,
    task_type: str = None,
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
) -> DatasetMetadata:
    """
    Upload a new dataset
    
    - **file**: CSV file to upload
    - **name**: Dataset name
    - **description**: Optional description
    - **source**: Data source
    - **license**: Data license
    - **target_column**: Target column for ML tasks
    - **task_type**: Type of task (classification, regression)
    """
    
    # Read file
    try:
        contents = await file.read()
        df = pd.read_csv(__import__('io').StringIO(contents.decode()))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")
    
    # Validate
    if len(df) == 0:
        raise HTTPException(status_code=400, detail="Dataset is empty")
    
    if len(df) > 1000000:
        raise HTTPException(status_code=400, detail="Dataset too large (>1M rows)")
    
    # Calculate hash
    file_hash = calculate_file_hash(contents)
    
    # Create dataset in database
    dataset = DatabaseService.create_dataset(
        db=db,
        name=name or file.filename,
        owner_id=None,  # TODO: Get from auth
        rows=len(df),
        columns=len(df.columns),
        description=description,
        source=source,
        license=license,
        file_hash=file_hash,
        target_column=target_column,
        task_type=task_type
    )
    
    # Store file data in memory (TODO: Move to file storage)
    DATASET_FILES[dataset.id] = df
    
    return DatasetMetadata(
        id=dataset.id,
        name=dataset.name,
        description=dataset.description,
        source=dataset.source,
        license=dataset.license,
        rows=dataset.rows,
        columns=dataset.columns,
        file_hash=dataset.file_hash,
        created_at=dataset.created_at,
        target_column=dataset.target_column,
        task_type=dataset.task_type
    )

@router.get("/datasets", response_model=List[DatasetListResponse], tags=["datasets"])
async def list_datasets(db: Session = Depends(get_db)) -> List[DatasetListResponse]:
    """List all uploaded datasets"""
    
    datasets = DatabaseService.list_datasets(db)
    
    return [
        DatasetListResponse(
            id=dataset.id,
            name=dataset.name,
            rows=dataset.rows,
            columns=dataset.columns,
            task_type=dataset.task_type,
            created_at=dataset.created_at
        )
        for dataset in datasets
    ]

@router.get("/datasets/{dataset_id}", response_model=DatasetDetailResponse, tags=["datasets"])
async def get_dataset_details(dataset_id: str, db: Session = Depends(get_db)) -> DatasetDetailResponse:
    """Get detailed information about a dataset"""
    
    dataset = DatabaseService.get_dataset(db, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    if dataset_id not in DATASET_FILES:
        raise HTTPException(status_code=404, detail="Dataset file not found")
    
    df = DATASET_FILES[dataset_id]
    
    # Generate quality report
    quality_report = profile_dataset(df)
    
    # Get preview (first 50 rows)
    preview = df.head(50).to_dict(orient='records')
    
    metadata = DatasetMetadata(
        id=dataset.id,
        name=dataset.name,
        description=dataset.description,
        source=dataset.source,
        license=dataset.license,
        rows=dataset.rows,
        columns=dataset.columns,
        file_hash=dataset.file_hash,
        created_at=dataset.created_at,
        target_column=dataset.target_column,
        task_type=dataset.task_type
    )
    
    return DatasetDetailResponse(
        metadata=metadata,
        quality_report=quality_report,
        preview={"rows": preview, "count": len(preview)}
    )

@router.get("/datasets/{dataset_id}/profile", tags=["datasets"])
async def get_dataset_profile(dataset_id: str, db: Session = Depends(get_db)) -> DatasetQualityReport:
    """Get quality profile of dataset"""
    
    dataset = DatabaseService.get_dataset(db, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    if dataset_id not in DATASET_FILES:
        raise HTTPException(status_code=404, detail="Dataset file not found")
    
    df = DATASET_FILES[dataset_id]
    return profile_dataset(df)

def calculate_file_hash(file_bytes: bytes) -> str:
    """Calculate SHA256 hash of file"""
    return hashlib.sha256(file_bytes).hexdigest()

def profile_dataset(df: pd.DataFrame) -> DatasetQualityReport:
    """Generate quality report for dataset"""
    warnings = []
    
    # Check for duplicates
    duplicate_rows = df.duplicated().sum()
    duplicate_percentage = (duplicate_rows / len(df)) * 100 if len(df) > 0 else 0
    
    # Check for missing values
    missing_cells = df.isna().sum().sum()
    total_cells = df.shape[0] * df.shape[1]
    missing_percentage = (missing_cells / total_cells) * 100 if total_cells > 0 else 0
    
    # Profile columns
    columns = []
    for col in df.columns:
        non_null = df[col].notna().sum()
        null_percentage = (df[col].isna().sum() / len(df)) * 100 if len(df) > 0 else 0
        unique_count = df[col].nunique()
        is_constant = unique_count <= 1
        
        # Determine data type
        if pd.api.types.is_numeric_dtype(df[col]):
            dtype = DataTypeEnum.NUMERIC
            profile_col = ColumnProfile(
                name=col,
                dtype=dtype,
                non_null_count=non_null,
                null_percentage=null_percentage,
                unique_count=unique_count,
                constant=is_constant,
                mean=float(df[col].mean()),
                std=float(df[col].std()),
                min=float(df[col].min()),
                max=float(df[col].max())
            )
        else:
            dtype = DataTypeEnum.CATEGORICAL
            top_cats = df[col].value_counts().head(5).index.tolist()
            profile_col = ColumnProfile(
                name=col,
                dtype=dtype,
                non_null_count=non_null,
                null_percentage=null_percentage,
                unique_count=unique_count,
                constant=is_constant,
                top_categories=top_cats,
                cardinality=unique_count
            )
        
        columns.append(profile_col)
        
        # Add warnings
        if null_percentage > 20:
            warnings.append(f"High missing values ({null_percentage:.1f}%) in column '{col}'")
        if is_constant:
            warnings.append(f"Constant column detected: '{col}'")
    
    # Memory usage
    memory_usage = df.memory_usage(deep=True).sum() / (1024 * 1024)
    
    return DatasetQualityReport(
        total_rows=len(df),
        total_columns=len(df.columns),
        memory_usage_mb=memory_usage,
        duplicate_rows=duplicate_rows,
        duplicate_percentage=duplicate_percentage,
        missing_cells_percentage=missing_percentage,
        columns=columns,
        warnings=warnings
    )

@router.post("/datasets", response_model=DatasetMetadata, tags=["datasets"])
async def upload_dataset(
    file: UploadFile = File(...),
    name: str = None,
    description: str = None,
    source: str = "user_upload",
    license: str = "CC0",
    target_column: str = None,
    task_type: str = None,
    background_tasks: BackgroundTasks = None
) -> DatasetMetadata:
    """
    Upload a new dataset
    
    - **file**: CSV file to upload
    - **name**: Dataset name
    - **description**: Optional description
    - **source**: Data source
    - **license**: Data license
    - **target_column**: Target column for ML tasks
    - **task_type**: Type of task (classification, regression)
    """
    
    # Read file
    try:
        contents = await file.read()
        df = pd.read_csv(__import__('io').StringIO(contents.decode()))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")
    
    # Validate
    if len(df) == 0:
        raise HTTPException(status_code=400, detail="Dataset is empty")
    
    if len(df) > 1000000:
        raise HTTPException(status_code=400, detail="Dataset too large (>1M rows)")
    
    # Generate ID and hash
    dataset_id = f"ds_{len(DATASETS) + 1}"
    file_hash = calculate_file_hash(contents)
    
    # Create metadata
    metadata = DatasetMetadata(
        id=dataset_id,
        name=name or file.filename,
        description=description,
        source=source,
        license=license,
        rows=len(df),
        columns=len(df.columns),
        file_hash=file_hash,
        created_at=datetime.now(),
        target_column=target_column,
        task_type=task_type
    )
    
    # Store
    DATASETS[dataset_id] = metadata
    DATASET_FILES[dataset_id] = df
    
    return metadata

@router.get("/datasets", response_model=List[DatasetListResponse], tags=["datasets"])
async def list_datasets() -> List[DatasetListResponse]:
    """List all uploaded datasets"""
    
    return [
        DatasetListResponse(
            id=meta.id,
            name=meta.name,
            rows=meta.rows,
            columns=meta.columns,
            task_type=meta.task_type,
            created_at=meta.created_at
        )
        for meta in DATASETS.values()
    ]

@router.get("/datasets/{dataset_id}", response_model=DatasetDetailResponse, tags=["datasets"])
async def get_dataset_details(dataset_id: str) -> DatasetDetailResponse:
    """Get detailed information about a dataset"""
    
    if dataset_id not in DATASETS:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    metadata = DATASETS[dataset_id]
    df = DATASET_FILES[dataset_id]
    
    # Generate quality report
    quality_report = profile_dataset(df)
    
    # Get preview (first 50 rows)
    preview = df.head(50).to_dict(orient='records')
    
    return DatasetDetailResponse(
        metadata=metadata,
        quality_report=quality_report,
        preview={"rows": preview, "count": len(preview)}
    )

@router.get("/datasets/{dataset_id}/profile", tags=["datasets"])
async def get_dataset_profile(dataset_id: str) -> DatasetQualityReport:
    """Get quality profile of dataset"""
    
    if dataset_id not in DATASETS:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    df = DATASET_FILES[dataset_id]
    return profile_dataset(df)
