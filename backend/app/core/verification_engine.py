"""Real verification engine for independent validation of analysis"""
import random
from typing import Dict, Any, List
from datetime import datetime


class VerificationEngine:
    """Verify analysis results and detect errors"""
    
    # Error types that can be detected
    ERROR_TYPES = {
        "methodology_error": "Incorrect statistical method used",
        "calculation_error": "Mathematical computation error",
        "interpretation_error": "Incorrect interpretation of results",
        "data_handling_error": "Data preprocessing or handling issue",
        "assumption_violation": "Model assumptions not met",
        "feature_scaling_error": "Features not properly scaled",
        "class_imbalance_error": "Unhandled class imbalance",
        "overfitting_error": "Model overfitting detected",
        "underfitting_error": "Model underfitting detected",
        "validation_error": "Cross-validation not performed correctly"
    }
    
    @staticmethod
    def verify_baseline_analysis(
        baseline_results: Dict[str, Any],
        dataset_shape: tuple,
        analysis_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Verify baseline analysis for errors"""
        
        errors_found = []
        warnings = []
        
        # Check 1: Accuracy bounds
        accuracy = baseline_results.get("accuracy", 0)
        if accuracy < 0 or accuracy > 1:
            errors_found.append({
                "type": "calculation_error",
                "severity": "critical",
                "message": f"Invalid accuracy value: {accuracy}. Should be between 0 and 1"
            })
        
        if accuracy < 0.5:
            warnings.append({
                "type": "underfitting_error",
                "severity": "warning",
                "message": "Model performance is below 50%. Model may be underfitting"
            })
        
        if accuracy > 0.99:
            warnings.append({
                "type": "overfitting_error",
                "severity": "warning",
                "message": "Model performance is suspiciously high (>99%). Check for data leakage"
            })
        
        # Check 2: Feature importance
        features = baseline_results.get("feature_importance", [])
        if not features:
            errors_found.append({
                "type": "methodology_error",
                "severity": "major",
                "message": "No feature importance analysis performed"
            })
        
        # Check 3: Cross-validation
        if "cross_val_scores" not in baseline_results:
            warnings.append({
                "type": "validation_error",
                "severity": "warning",
                "message": "Cross-validation not performed. Single train/test split may overestimate performance"
            })
        
        # Check 4: Sample size
        samples = dataset_shape[0]
        if samples < 100:
            warnings.append({
                "type": "data_handling_error",
                "severity": "warning",
                "message": f"Small dataset ({samples} samples). Results may not generalize well"
            })
        
        # Check 5: Metric consistency
        precision = baseline_results.get("precision", 0)
        recall = baseline_results.get("recall", 0)
        
        if precision > 0 and recall > 0:
            if abs(precision - recall) > 0.5:
                warnings.append({
                    "type": "interpretation_error",
                    "severity": "warning",
                    "message": f"High discrepancy between precision ({precision:.2f}) and recall ({recall:.2f}). Investigate class imbalance"
                })
        
        # Calculate confidence score
        confidence = VerificationEngine._calculate_confidence(
            baseline_results,
            len(errors_found),
            len(warnings)
        )
        
        return {
            "verification_status": "completed",
            "errors_found": errors_found,
            "warnings": warnings,
            "total_errors": len(errors_found),
            "total_warnings": len(warnings),
            "critical_errors": len([e for e in errors_found if e["severity"] == "critical"]),
            "confidence_score": confidence,
            "verified_metrics": {
                "accuracy": accuracy,
                "precision": baseline_results.get("precision"),
                "recall": baseline_results.get("recall"),
                "f1_score": baseline_results.get("f1_score")
            },
            "timestamp": datetime.utcnow().isoformat(),
            "assessment": "PASS" if len([e for e in errors_found if e["severity"] == "critical"]) == 0 else "FAIL"
        }
    
    @staticmethod
    def compare_runs(
        baseline_results: Dict[str, Any],
        verification_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare baseline and verification results"""
        
        baseline_acc = baseline_results.get("accuracy", 0)
        verification_acc = verification_results.get("accuracy", 0)
        
        improvement = ((verification_acc - baseline_acc) / (baseline_acc + 0.001)) * 100
        
        differences = {
            "accuracy_difference": verification_acc - baseline_acc,
            "accuracy_improvement_percent": improvement,
            "confidence_improvement": verification_results.get("confidence_score", 0) - 0.75,
        }
        
        # Error reduction
        baseline_errors = baseline_results.get("errors_detected", 0)
        verification_errors = verification_results.get("total_errors", 0)
        
        if baseline_errors > 0:
            error_reduction = ((baseline_errors - verification_errors) / baseline_errors) * 100
        else:
            error_reduction = 0
        
        differences["error_reduction_percent"] = error_reduction
        
        return {
            "comparison": differences,
            "baseline_status": "PASS" if baseline_acc > 0.7 else "NEEDS_REVIEW",
            "verification_status": verification_results.get("assessment", "UNKNOWN"),
            "reliability_improved": verification_acc > baseline_acc,
            "recommendation": VerificationEngine._generate_recommendation(
                baseline_results,
                verification_results,
                improvement
            )
        }
    
    @staticmethod
    def _calculate_confidence(metrics: Dict[str, Any], errors: int, warnings: int) -> float:
        """Calculate confidence score"""
        
        base_confidence = 0.8
        
        # Adjust based on accuracy
        accuracy = metrics.get("accuracy", 0.5)
        confidence = base_confidence + (accuracy - 0.5) * 0.2
        
        # Reduce for errors
        confidence -= errors * 0.1
        
        # Reduce for warnings
        confidence -= warnings * 0.05
        
        # Ensure bounds
        return max(0, min(1, confidence))
    
    @staticmethod
    def _generate_recommendation(
        baseline: Dict[str, Any],
        verification: Dict[str, Any],
        improvement: float
    ) -> str:
        """Generate recommendations based on verification"""
        
        if improvement > 10:
            return "Verification significantly improves results. Recommend using verification approach for similar analyses"
        elif improvement > 5:
            return "Verification provides moderate improvement. Consider using for important decisions"
        elif improvement > 0:
            return "Verification provides minor improvement. Results are reasonably reliable"
        elif improvement > -5:
            return "Results are consistent across methods. Either approach is acceptable"
        else:
            return "Discrepancy detected. Recommend investigating methodology and assumptions"
    
    @staticmethod
    def detect_data_issues(data_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect data quality issues"""
        
        issues = []
        
        # Check missing values
        missing_pct = data_profile.get("missing_values_percent", 0)
        if missing_pct > 20:
            issues.append({
                "type": "missing_data",
                "severity": "critical",
                "message": f"High missing values ({missing_pct:.1f}%). Consider imputation or removal",
                "percentage": missing_pct
            })
        
        # Check duplicates
        duplicate_pct = data_profile.get("duplicate_percentage", 0)
        if duplicate_pct > 5:
            issues.append({
                "type": "duplicate_data",
                "severity": "major",
                "message": f"Duplicate rows detected ({duplicate_pct:.1f}%). Remove before analysis",
                "percentage": duplicate_pct
            })
        
        # Check for constant columns
        if "warnings" in data_profile:
            for warning in data_profile["warnings"]:
                if "constant" in warning.lower():
                    issues.append({
                        "type": "constant_column",
                        "severity": "minor",
                        "message": warning
                    })
        
        return issues
