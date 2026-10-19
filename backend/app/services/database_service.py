"""Database persistence service for experiments and datasets"""

from sqlalchemy.orm import Session
from app.models import (
    Dataset, Experiment, Run, ExperimentTemplate,
    Notification, ActivityLog, Workspace, WorkspaceMember,
    User, ExperimentResult, AnalysisPlan, Verification, APIKey
)
from datetime import datetime
from typing import Optional, List, Dict, Any
import json


class DatabaseService:
    """Service for database operations"""
    
    @staticmethod
    def create_dataset(db: Session, name: str, owner_id: Optional[str],
                      rows: int, columns: int, **kwargs) -> Dataset:
        """Create and save dataset metadata"""
        dataset = Dataset(
            name=name,
            owner_id=owner_id,
            rows=rows,
            columns=columns,
            **kwargs
        )
        db.add(dataset)
        db.commit()
        db.refresh(dataset)
        return dataset
    
    @staticmethod
    def create_experiment(db: Session, dataset_id: str, name: str,
                         owner_id: Optional[str], **config) -> Experiment:
        """Create and save experiment"""
        experiment = Experiment(
            dataset_id=dataset_id,
            name=name,
            owner_id=owner_id,
            config=config,
            target_column=config.get("target_column"),
            task_type=config.get("task_type"),
            description=config.get("description", "")
        )
        db.add(experiment)
        db.commit()
        db.refresh(experiment)
        return experiment
    
    @staticmethod
    def create_run(db: Session, experiment_id: str, approach: str) -> Run:
        """Create experiment run"""
        run = Run(
            experiment_id=experiment_id,
            approach=approach,
            status="created",
            created_at=datetime.utcnow()
        )
        db.add(run)
        db.commit()
        db.refresh(run)
        return run
    
    @staticmethod
    def update_run(db: Session, run_id: str, **updates) -> Optional[Run]:
        """Update run with results"""
        run = db.query(Run).filter(Run.id == run_id).first()
        if run:
            for key, value in updates.items():
                if hasattr(run, key):
                    setattr(run, key, value)
            db.commit()
            db.refresh(run)
        return run
    
    @staticmethod
    def get_experiment(db: Session, experiment_id: str) -> Optional[Experiment]:
        """Get experiment by ID"""
        return db.query(Experiment).filter(Experiment.id == experiment_id).first()
    
    @staticmethod
    def get_run(db: Session, run_id: str) -> Optional[Run]:
        """Get run by ID"""
        return db.query(Run).filter(Run.id == run_id).first()
    
    @staticmethod
    def get_dataset(db: Session, dataset_id: str) -> Optional[Dataset]:
        """Get dataset by ID"""
        return db.query(Dataset).filter(Dataset.id == dataset_id).first()
    
    @staticmethod
    def list_experiments(db: Session, limit: int = 100, offset: int = 0) -> List[Experiment]:
        """List experiments with pagination"""
        return db.query(Experiment).limit(limit).offset(offset).all()
    
    @staticmethod
    def list_datasets(db: Session, limit: int = 100, offset: int = 0) -> List[Dataset]:
        """List datasets with pagination"""
        return db.query(Dataset).limit(limit).offset(offset).all()
    
    @staticmethod
    def list_runs(db: Session, experiment_id: str) -> List[Run]:
        """List runs for experiment"""
        return db.query(Run).filter(Run.experiment_id == experiment_id).all()
    
    @staticmethod
    def create_activity_log(db: Session, user_id: str, action: str,
                          entity_type: str, entity_id: str,
                          details: Optional[Dict] = None, success: bool = True) -> ActivityLog:
        """Log user activity"""
        log = ActivityLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details or {},
            success=success,
            created_at=datetime.utcnow()
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    
    @staticmethod
    def create_notification(db: Session, user_id: str, title: str,
                          message: str, notification_type: str,
                          related_entity_type: Optional[str] = None,
                          related_entity_id: Optional[str] = None,
                          action_url: Optional[str] = None) -> Notification:
        """Create notification"""
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            related_entity_type=related_entity_type,
            related_entity_id=related_entity_id,
            action_url=action_url,
            created_at=datetime.utcnow()
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification
    
    @staticmethod
    def create_experiment_result(db: Session, experiment_id: str,
                                **metrics) -> ExperimentResult:
        """Create experiment result"""
        result = ExperimentResult(
            experiment_id=experiment_id,
            **metrics,
            created_at=datetime.utcnow()
        )
        db.add(result)
        db.commit()
        db.refresh(result)
        return result
    
    @staticmethod
    def create_user(db: Session, username: str, email: str,
                   hashed_password: str, **kwargs) -> User:
        """Create user account"""
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            **kwargs
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_user(db: Session, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get user by username"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
