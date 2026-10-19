"""AI engine for generating analysis plans and running experiments"""
import json
from typing import Dict, Any, List
import random
from datetime import datetime

class AIEngine:
    """Generates AI-based analysis plans using LLM or templates"""
    
    @staticmethod
    def generate_analysis_plan(
        research_question: str,
        dataset_profile: Dict[str, Any],
        approach: str = "ai_baseline"
    ) -> Dict[str, Any]:
        """Generate an analysis plan based on research question and dataset"""
        
        # Template-based generation (fallback when LLM unavailable)
        numeric_cols = list(dataset_profile.get("numeric_stats", {}).keys())
        categorical_cols = list(dataset_profile.get("categorical_stats", {}).keys())
        
        techniques = []
        
        # Add techniques based on data types
        if numeric_cols and categorical_cols:
            techniques.extend([
                "Exploratory Data Analysis with visualization",
                "Categorical feature encoding and analysis",
                "Statistical correlation analysis",
                "Feature importance assessment"
            ])
        elif numeric_cols:
            techniques.extend([
                "Descriptive statistics and distribution analysis",
                "Outlier detection and handling",
                "Normalization and scaling techniques",
                "Clustering or dimensionality reduction"
            ])
        elif categorical_cols:
            techniques.extend([
                "Category distribution analysis",
                "Association rule mining",
                "Text feature engineering if applicable",
                "Class imbalance analysis"
            ])
        
        # Add ML techniques
        techniques.extend([
            "Model selection and hyperparameter tuning",
            "Cross-validation strategy",
            "Performance metrics evaluation",
            "Interpretation and insights generation"
        ])
        
        plan = {
            "research_question": research_question,
            "approach": approach,
            "data_summary": {
                "rows": dataset_profile.get("rows"),
                "columns": dataset_profile.get("columns"),
                "numeric_features": len(numeric_cols),
                "categorical_features": len(categorical_cols),
            },
            "proposed_techniques": techniques,
            "execution_steps": [
                "Data cleaning and validation",
                "Exploratory data analysis",
                "Feature engineering and selection",
                "Model training and evaluation",
                "Results interpretation and validation"
            ],
            "estimated_metrics": [
                "Accuracy/R² score",
                "Precision and Recall (for classification)",
                "Feature importance",
                "Model interpretability score"
            ],
            "risk_factors": dataset_profile.get("potential_issues", []),
            "high_correlations": dataset_profile.get("correlations", [])
        }
        
        return plan
    
    @staticmethod
    def execute_baseline_analysis(
        dataset_id: str,
        research_question: str,
        analysis_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute baseline analysis using mock ML pipeline"""
        
        # Simulate baseline execution
        techniques = analysis_plan.get("proposed_techniques", [])
        
        results = {
            "execution_start": datetime.utcnow().isoformat(),
            "status": "completed",
            "primary_metric": round(random.uniform(0.65, 0.92), 3),
            "secondary_metrics": {
                "precision": round(random.uniform(0.60, 0.90), 3),
                "recall": round(random.uniform(0.60, 0.90), 3),
                "f1_score": round(random.uniform(0.60, 0.90), 3),
                "model_interpretability": round(random.uniform(0.70, 0.95), 3)
            },
            "techniques_applied": techniques[:3],
            "key_findings": [
                "Primary feature correlation identified",
                "Model achieves reasonable performance on validation set",
                "Feature interactions present in data"
            ],
            "errors_detected": max(0, random.randint(0, 15)),
            "warnings": [
                "High variance in predictions observed",
                "Some features show data drift"
            ] if random.random() > 0.5 else [],
            "execution_time_seconds": round(random.uniform(5, 45), 2)
        }
        
        return results
    
    @staticmethod
    def verify_analysis(
        run_results: Dict[str, Any],
        analysis_plan: Dict[str, Any],
        verification_approach: str = "independent_verification"
    ) -> Dict[str, Any]:
        """Verify analysis results using independent method"""
        
        baseline_accuracy = run_results.get("primary_metric", 0.75)
        
        # Simulate verification
        verification_results = {
            "verification_start": datetime.utcnow().isoformat(),
            "verification_approach": verification_approach,
            "status": "completed",
            "verification_accuracy": round(baseline_accuracy * random.uniform(0.85, 1.15), 3),
            "errors_found": {
                "methodology_errors": random.randint(0, 5),
                "calculation_errors": random.randint(0, 3),
                "interpretation_errors": random.randint(0, 4),
                "data_handling_errors": random.randint(0, 3)
            },
            "error_breakdown": {
                "Critical": random.randint(0, 2),
                "Major": random.randint(0, 3),
                "Minor": random.randint(2, 6)
            },
            "confidence_score": round(random.uniform(0.75, 0.98), 3),
            "recommendations": [
                "Validate feature engineering approach",
                "Review model assumptions",
                "Consider additional cross-validation folds",
                "Document model limitations clearly"
            ],
            "verification_time_seconds": round(random.uniform(10, 60), 2),
            "overall_assessment": "PASS" if random.random() > 0.2 else "NEEDS_REVIEW"
        }
        
        return verification_results
    
    @staticmethod
    def compare_approaches(
        ai_baseline: Dict[str, Any],
        verification_results: Dict[str, Any],
        manual_results: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Compare results from different approaches"""
        
        baseline_accuracy = ai_baseline.get("primary_metric", 0.75)
        verification_accuracy = verification_results.get("verification_accuracy", 0.75)
        
        improvement = (verification_accuracy - baseline_accuracy) / baseline_accuracy * 100 if baseline_accuracy > 0 else 0
        
        comparison = {
            "ai_baseline": {
                "accuracy": baseline_accuracy,
                "errors": ai_baseline.get("errors_detected", 0),
                "warnings": len(ai_baseline.get("warnings", []))
            },
            "independent_verification": {
                "accuracy": verification_accuracy,
                "errors": sum(verification_results.get("errors_found", {}).values()),
                "confidence": verification_results.get("confidence_score", 0.8)
            },
            "improvement_metrics": {
                "accuracy_improvement_percent": round(improvement, 2),
                "error_reduction": round((ai_baseline.get("errors_detected", 0) - verification_results.get("errors_found", {}).get("Critical", 0)) / max(1, ai_baseline.get("errors_detected", 1)) * 100, 2),
                "reliability_boost": round((verification_accuracy - baseline_accuracy) * 100, 2)
            },
            "key_insight": "Independent verification significantly reduces errors" if abs(improvement) > 5 else "Verification confirms baseline results"
        }
        
        return comparison
