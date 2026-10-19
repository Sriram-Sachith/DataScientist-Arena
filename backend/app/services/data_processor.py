"""Real data processing and analysis service"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, mean_squared_error, r2_score
from typing import Dict, Any, Tuple, List
import warnings
warnings.filterwarnings('ignore')


class DataProcessor:
    """Process and analyze datasets with real ML pipeline"""
    
    @staticmethod
    def prepare_data(df: pd.DataFrame, target_column: str = None) -> Tuple[pd.DataFrame, str]:
        """Prepare data for analysis"""
        
        # Handle missing values
        df = df.dropna()
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Identify data types
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        # Encode categorical variables
        le_dict = {}
        for col in categorical_cols:
            if col != target_column:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                le_dict[col] = le
        
        return df, "prepared"
    
    @staticmethod
    def train_classifier(X: pd.DataFrame, y: pd.Series, test_size: float = 0.2) -> Dict[str, Any]:
        """Train classification model"""
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        model.fit(X_train_scaled, y_train)
        
        # Predictions
        y_pred = model.predict(X_test_scaled)
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        # Feature importance
        feature_importance = sorted(
            zip(X.columns, model.feature_importances_),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return {
            "model_type": "RandomForestClassifier",
            "accuracy": float(accuracy),
            "precision": float(precision),
            "recall": float(recall),
            "f1_score": float(f1),
            "feature_importance": [
                {"feature": name, "importance": float(score)}
                for name, score in feature_importance
            ],
            "training_samples": len(X_train),
            "test_samples": len(X_test)
        }
    
    @staticmethod
    def train_regressor(X: pd.DataFrame, y: pd.Series, test_size: float = 0.2) -> Dict[str, Any]:
        """Train regression model"""
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        model.fit(X_train_scaled, y_train)
        
        # Predictions
        y_pred = model.predict(X_test_scaled)
        
        # Metrics
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        mae = np.mean(np.abs(y_test - y_pred))
        
        # Feature importance
        feature_importance = sorted(
            zip(X.columns, model.feature_importances_),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return {
            "model_type": "RandomForestRegressor",
            "r2_score": float(r2),
            "rmse": float(rmse),
            "mae": float(mae),
            "mse": float(mse),
            "feature_importance": [
                {"feature": name, "importance": float(score)}
                for name, score in feature_importance
            ],
            "training_samples": len(X_train),
            "test_samples": len(X_test)
        }
    
    @staticmethod
    def analyze_features(df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze feature characteristics"""
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        analysis = {
            "numeric_features": len(numeric_cols),
            "categorical_features": len(categorical_cols),
            "total_features": len(df.columns),
            "total_rows": len(df),
            "missing_values_percent": float((df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)),
            "correlation_matrix": None,
            "feature_statistics": {}
        }
        
        # Numeric statistics
        for col in numeric_cols[:10]:  # Limit to top 10
            stats = df[col].describe()
            analysis["feature_statistics"][col] = {
                "mean": float(stats['mean']),
                "std": float(stats['std']),
                "min": float(stats['min']),
                "max": float(stats['max']),
                "median": float(df[col].median())
            }
        
        # Correlation
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            # Find highly correlated pairs
            high_corr = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    if abs(corr_matrix.iloc[i, j]) > 0.7:
                        high_corr.append({
                            "feature1": corr_matrix.columns[i],
                            "feature2": corr_matrix.columns[j],
                            "correlation": float(corr_matrix.iloc[i, j])
                        })
            analysis["high_correlations"] = high_corr
        
        return analysis
    
    @staticmethod
    def generate_insights(analysis: Dict[str, Any], metrics: Dict[str, Any]) -> List[str]:
        """Generate human-readable insights"""
        
        insights = []
        
        # Feature insights
        if analysis.get("numeric_features", 0) > 0:
            insights.append(f"Dataset contains {analysis['numeric_features']} numeric features")
        
        if analysis.get("categorical_features", 0) > 0:
            insights.append(f"Dataset contains {analysis['categorical_features']} categorical features")
        
        # Missing values
        missing_pct = analysis.get("missing_values_percent", 0)
        if missing_pct > 5:
            insights.append(f"⚠️ {missing_pct:.1f}% of values are missing")
        
        # Model performance
        if "accuracy" in metrics:
            accuracy = metrics["accuracy"]
            if accuracy > 0.9:
                insights.append(f"✓ Strong classification performance (accuracy: {accuracy:.1%})")
            elif accuracy > 0.7:
                insights.append(f"✓ Good classification performance (accuracy: {accuracy:.1%})")
            else:
                insights.append(f"⚠️ Consider feature engineering or model tuning (accuracy: {accuracy:.1%})")
        
        if "r2_score" in metrics:
            r2 = metrics["r2_score"]
            if r2 > 0.8:
                insights.append(f"✓ Strong regression fit (R²: {r2:.3f})")
            elif r2 > 0.5:
                insights.append(f"✓ Moderate regression fit (R²: {r2:.3f})")
            else:
                insights.append(f"⚠️ Weak regression fit, more features may help (R²: {r2:.3f})")
        
        # Correlation insights
        if analysis.get("high_correlations"):
            insights.append(f"Found {len(analysis['high_correlations'])} highly correlated feature pairs")
        
        return insights
