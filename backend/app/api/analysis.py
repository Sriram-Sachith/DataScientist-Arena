"""API routes for analysis operations"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

from app.core.ai_engine import AIEngine
from app.services.data_processor import DataProcessor

router = APIRouter()

# In-memory storage
ANALYSIS_PLANS: dict = {}
DATASETS_REF: dict = {}

class AnalysisPlanRequest(BaseModel):
    experiment_id: str
    research_question: str
    dataset_profile: Optional[Dict[str, Any]] = None

class AnalysisPlanResponse(BaseModel):
    id: str
    experiment_id: str
    research_question: str
    proposed_techniques: List[str]
    techniques_rationale: str
    execution_steps: List[str]
    estimated_time_minutes: int
    estimated_cost_credits: int
    risk_assessment: str
    high_correlations: List[Dict] = []
    created_at: datetime

@router.post("/analysis-plans", response_model=AnalysisPlanResponse)
async def create_analysis_plan(request: AnalysisPlanRequest) -> AnalysisPlanResponse:
    """Create an AI-generated analysis plan"""
    
    # Use provided profile or mock one
    dataset_profile = request.dataset_profile or {
        "rows": 1000,
        "columns": 15,
        "numeric_stats": {
            "age": {"mean": 45.2, "std": 15.1, "min": 18, "max": 85},
            "income": {"mean": 65000, "std": 25000, "min": 25000, "max": 150000},
        },
        "categorical_stats": {
            "education": {"unique_values": 5},
            "region": {"unique_values": 10}
        },
        "potential_issues": [],
        "correlations": []
    }
    
    # Generate plan using AI engine
    plan_data = AIEngine.generate_analysis_plan(
        research_question=request.research_question,
        dataset_profile=dataset_profile,
        approach="ai_baseline"
    )
    
    plan_id = f"plan_{len(ANALYSIS_PLANS) + 1}"
    
    plan = AnalysisPlanResponse(
        id=plan_id,
        experiment_id=request.experiment_id,
        research_question=request.research_question,
        proposed_techniques=plan_data.get("proposed_techniques", []),
        techniques_rationale="Automatically generated based on data characteristics and research question",
        execution_steps=plan_data.get("execution_steps", []),
        estimated_time_minutes=25,
        estimated_cost_credits=50,
        risk_assessment=", ".join(plan_data.get("risk_factors", ["None detected"])),
        high_correlations=plan_data.get("correlations", []),
        created_at=datetime.now()
    )
    
    ANALYSIS_PLANS[plan_id] = plan
    return plan

@router.get("/analysis-plans/{plan_id}", response_model=AnalysisPlanResponse)
async def get_analysis_plan(plan_id: str) -> AnalysisPlanResponse:
    """Get an analysis plan"""
    
    if plan_id not in ANALYSIS_PLANS:
        raise HTTPException(status_code=404, detail="Analysis plan not found")
    
    return ANALYSIS_PLANS[plan_id]

@router.post("/analysis-plans/{plan_id}/execute")
async def execute_analysis_plan(plan_id: str):
    """Execute an analysis plan with real ML pipeline"""
    
    if plan_id not in ANALYSIS_PLANS:
        raise HTTPException(status_code=404, detail="Analysis plan not found")
    
    plan = ANALYSIS_PLANS[plan_id]
    
    try:
        # Import datasets at runtime to avoid circular imports
        from app.api import datasets
        
        # Find dataset for this experiment
        if "dataset_id" not in ANALYSIS_PLANS[plan_id].__dict__:
            raise HTTPException(status_code=400, detail="No dataset associated with plan")
        
        # For now, use first available dataset or mock
        available_datasets = list(datasets.DATASET_FILES.keys())
        
        if available_datasets:
            dataset_id = available_datasets[0]
            df = datasets.DATASET_FILES[dataset_id].copy()
            
            # Run real analysis
            feature_analysis = DataProcessor.analyze_features(df)
            insights = DataProcessor.generate_insights(feature_analysis, {})
            
            results = {
                "plan_id": plan_id,
                "status": "executing",
                "feature_analysis": feature_analysis,
                "insights": insights,
                "execution_started": datetime.now().isoformat()
            }
        else:
            # No dataset available, return mock results
            results = {
                "plan_id": plan_id,
                "status": "executing",
                "insights": [
                    "Upload a dataset to execute real analysis",
                    "Supported formats: CSV with numeric and categorical columns"
                ],
                "execution_started": datetime.now().isoformat()
            }
        
        return results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis execution failed: {str(e)}")
