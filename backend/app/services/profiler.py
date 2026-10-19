"""Data profiling service for analyzing dataset characteristics"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List
import json

class DataProfiler:
    @staticmethod
    def profile_dataset(file_path: str) -> Dict[str, Any]:
        """Generate comprehensive profile of a dataset"""
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            
            profile = {
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": df.columns.tolist(),
                "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024 / 1024,
                "missing_values": df.isnull().sum().to_dict(),
                "data_types": df.dtypes.astype(str).to_dict(),
                "numeric_stats": {},
                "categorical_stats": {},
                "correlations": [],
                "potential_issues": []
            }
            
            # Numeric statistics
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                profile["numeric_stats"][col] = {
                    "mean": float(df[col].mean()) if not df[col].isna().all() else None,
                    "std": float(df[col].std()) if not df[col].isna().all() else None,
                    "min": float(df[col].min()) if not df[col].isna().all() else None,
                    "max": float(df[col].max()) if not df[col].isna().all() else None,
                    "median": float(df[col].median()) if not df[col].isna().all() else None,
                    "q25": float(df[col].quantile(0.25)) if not df[col].isna().all() else None,
                    "q75": float(df[col].quantile(0.75)) if not df[col].isna().all() else None,
                }
            
            # Categorical statistics
            categorical_cols = df.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                unique_count = df[col].nunique()
                profile["categorical_stats"][col] = {
                    "unique_values": unique_count,
                    "top_values": df[col].value_counts().head(5).to_dict(),
                    "cardinality": "high" if unique_count > 100 else "medium" if unique_count > 10 else "low"
                }
            
            # Correlations for numeric columns
            if len(numeric_cols) > 1:
                corr_matrix = df[numeric_cols].corr()
                high_corr = []
                for i in range(len(corr_matrix.columns)):
                    for j in range(i+1, len(corr_matrix.columns)):
                        corr_val = corr_matrix.iloc[i, j]
                        if abs(corr_val) > 0.7:
                            high_corr.append({
                                "column1": corr_matrix.columns[i],
                                "column2": corr_matrix.columns[j],
                                "correlation": float(corr_val)
                            })
                profile["correlations"] = high_corr
            
            # Detect potential issues
            if df.isnull().sum().sum() > 0:
                profile["potential_issues"].append("Missing values detected")
            if any(df.dtypes == 'object') and df[categorical_cols].nunique().max() > 100:
                profile["potential_issues"].append("High cardinality categorical features")
            if len(df) < 100:
                profile["potential_issues"].append("Small dataset (< 100 rows)")
            
            return profile
            
        except Exception as e:
            return {
                "error": str(e),
                "rows": 0,
                "columns": 0,
            }
    
    @staticmethod
    def get_sample_data(file_path: str, n_rows: int = 10) -> List[Dict]:
        """Get sample rows from dataset"""
        try:
            df = pd.read_csv(file_path)
            return df.head(n_rows).to_dict('records')
        except Exception as e:
            return []
    
    @staticmethod
    def get_column_info(file_path: str) -> List[Dict]:
        """Get detailed column information"""
        try:
            df = pd.read_csv(file_path)
            columns = []
            for col in df.columns:
                col_info = {
                    "name": col,
                    "dtype": str(df[col].dtype),
                    "non_null_count": int(df[col].notna().sum()),
                    "null_count": int(df[col].isna().sum()),
                    "unique_values": int(df[col].nunique())
                }
                columns.append(col_info)
            return columns
        except Exception as e:
            return []
