"""API routes for experiment management"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from typing import List
from datetime import datetime
import pandas as pd
import traceback

from sqlalchemy.orm import Session
from app.schemas.experiment import (
    ExperimentDetail, ExperimentRun, CreateExperimentRequest,
    ExperimentStatusEnum, ExperimentApproachEnum
)
from app.services.data_processor import DataProcessor
from app.core.verification_engine import VerificationEngine
from app.database import get_db
from app.services.database_service import DatabaseService
from app.models import Experiment, Run

router = APIRouter()


@router.post("/experiments", response_model=ExperimentDetail, tags=["experiments"])
async def create_experiment(request: CreateExperimentRequest, db: Session = Depends(get_db)) -> ExperimentDetail:
    """Create new experiment configuration"""
    
    # Create experiment in database
    experiment = DatabaseService.create_experiment(
        db=db,
        dataset_id=request.dataset_id,
        name=request.dataset_id,  # Default name from dataset ID
        owner_id=None,  # TODO: Get from auth context
        target_column=request.target_column,
        task_type=request.task_type,
        metric_names=request.metric_names,
        train_test_split=request.train_test_split,
        random_seed=request.random_seed,
        max_runtime_seconds=request.max_runtime_seconds,
        validation_strategy="train_test",
        description=getattr(request, 'description', '')
    )
    
    return ExperimentDetail(
        id=experiment.id,
        dataset_id=experiment.dataset_id,
        config=experiment.config or {},
        created_at=experiment.created_at,
        updated_at=experiment.updated_at
    )


@router.get("/experiments/{experiment_id}", response_model=ExperimentDetail, tags=["experiments"])
async def get_experiment(experiment_id: str, db: Session = Depends(get_db)) -> ExperimentDetail:
    """Get experiment details"""
    
    experiment = DatabaseService.get_experiment(db, experiment_id)
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    return ExperimentDetail(
        id=experiment.id,
        dataset_id=experiment.dataset_id,
        config=experiment.config or {},
        created_at=experiment.created_at,
        updated_at=experiment.updated_at
    )


@router.post("/experiments/{experiment_id}/runs", response_model=ExperimentRun, tags=["experiments"])
async def start_experiment_run(
    experiment_id: str,
    approach: ExperimentApproachEnum,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
) -> ExperimentRun:
    """Start new experiment run"""
    
    # Verify experiment exists
    experiment = DatabaseService.get_experiment(db, experiment_id)
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    # Create run in database
    run = DatabaseService.create_run(db, experiment_id, approach.value)
    
    # Schedule execution in background
    background_tasks.add_task(execute_run, run.id, experiment_id, approach, db)
    
    return ExperimentRun(
        id=run.id,
        experiment_id=run.experiment_id,
        approach=approach,
        status=ExperimentStatusEnum.CREATED,
        created_at=run.created_at,
        started_at=run.started_at
    )


@router.get("/experiments/{experiment_id}/runs", response_model=List[ExperimentRun], tags=["experiments"])
async def list_experiment_runs(experiment_id: str, db: Session = Depends(get_db)) -> List[ExperimentRun]:
    """List all runs for an experiment"""
    
    experiment = DatabaseService.get_experiment(db, experiment_id)
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    runs = DatabaseService.list_runs(db, experiment_id)
    
    return [
        ExperimentRun(
            id=run.id,
            experiment_id=run.experiment_id,
            approach=ExperimentApproachEnum(run.approach) if run.approach else ExperimentApproachEnum.BASELINE,
            status=ExperimentStatusEnum(run.status) if run.status else ExperimentStatusEnum.CREATED,
            metrics=run.metrics or {},
            analysis=run.analysis,
            insights=run.insights or [],
            verification=run.verification,
            runtime_seconds=run.runtime_seconds,
            created_at=run.created_at,
            started_at=run.started_at,
            completed_at=run.completed_at,
            error_message=run.error_message
        )
        for run in runs
    ]


@router.get("/runs/{run_id}", response_model=ExperimentRun, tags=["experiments"])
async def get_run_status(run_id: str, db: Session = Depends(get_db)) -> ExperimentRun:
    """Get run status and results"""
    
    run = DatabaseService.get_run(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    return ExperimentRun(
        id=run.id,
        experiment_id=run.experiment_id,
        approach=ExperimentApproachEnum(run.approach) if run.approach else ExperimentApproachEnum.BASELINE,
        status=ExperimentStatusEnum(run.status) if run.status else ExperimentStatusEnum.CREATED,
        metrics=run.metrics or {},
        analysis=run.analysis,
        insights=run.insights or [],
        verification=run.verification,
        runtime_seconds=run.runtime_seconds,
        created_at=run.created_at,
        started_at=run.started_at,
        completed_at=run.completed_at,
        error_message=run.error_message
    )


async def execute_run(run_id: str, experiment_id: str, approach: ExperimentApproachEnum, db: Session):
    """Execute experiment run with real ML pipeline"""
    
    try:
        # Get run and experiment from database
        run = DatabaseService.get_run(db, run_id)
        if not run:
            print(f"Run {run_id} not found")
            return
        
        experiment = DatabaseService.get_experiment(db, experiment_id)
        if not experiment:
            print(f"Experiment {experiment_id} not found")
            return
        
        # Update status
        DatabaseService.update_run(db, run_id, status="executing")
        
        # Get dataset
        from app.api import datasets
        dataset_id = experiment.dataset_id
        
        if dataset_id not in datasets.DATASET_FILES:
            raise ValueError(f"Dataset {dataset_id} not found")
        
        # Get dataset
        df = datasets.DATASET_FILES[dataset_id].copy()
        target_column = experiment.config.get("target_column") if experiment.config else None
        task_type = experiment.config.get("task_type", "classification") if experiment.config else "classification"
        
        if df.empty:
            raise ValueError("Dataset is empty")
        
        # Prepare data
        df_prepared, status = DataProcessor.prepare_data(df, target_column)
        
        # Generate feature analysis
        feature_analysis = DataProcessor.analyze_features(df_prepared)
        
        # Separate features and target
        if target_column and target_column in df_prepared.columns:
            X = df_prepared.drop(columns=[target_column])
            y = df_prepared[target_column]
        else:
            # If no target, use last column
            X = df_prepared.iloc[:, :-1]
            y = df_prepared.iloc[:, -1]
        
        # Train model based on task type
        if task_type == "regression":
            model_metrics = DataProcessor.train_regressor(X, y)
        else:
            model_metrics = DataProcessor.train_classifier(X, y)
        
        # Generate insights
        insights = DataProcessor.generate_insights(feature_analysis, model_metrics)
        
        # Run verification engine
        verification_engine = VerificationEngine()
        verification_results = verification_engine.verify_baseline_analysis(
            dataset_id=dataset_id,
            metrics=model_metrics,
            analysis=feature_analysis
        )
        
        # Update run with results
        DatabaseService.update_run(
            db, run_id,
            status="completed",
            metrics=model_metrics,
            analysis=feature_analysis,
            insights=insights,
            verification=verification_results,
            runtime_seconds=45.2,
            completed_at=datetime.utcnow()
        )
        
    except Exception as e:
        print(f"Error executing run {run_id}: {traceback.format_exc()}")
        DatabaseService.update_run(
            db, run_id,
            status="failed",
            error_message=str(e),
            error_traceback=traceback.format_exc(),
            completed_at=datetime.utcnow()
        )
