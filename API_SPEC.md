# DataScientist Arena - API Specification

## Base URL
```
http://127.0.0.1:8000/api/v1
```

## Authentication
Currently: None (Open for development)
Production: JWT Bearer token required

## Common Response Format

### Success Response
```json
{
  "status": "success",
  "data": { /* response data */ },
  "timestamp": "2024-10-20T10:30:00Z"
}
```

### Error Response
```json
{
  "detail": "Error message",
  "status_code": 400,
  "error_code": "VALIDATION_ERROR"
}
```

---

## Datasets API

### 1. Upload Dataset
**POST** `/datasets`

**Request:**
```
Content-Type: multipart/form-data

Parameters:
- file: File (required) - CSV file
- name: String (required) - Dataset name
- description: String (optional)
- source: String (optional) - Data source
- license: String (optional) - Data license
- target_column: String (optional) - ML target column
- task_type: String (optional) - 'classification' or 'regression'
```

**Response:** `200 OK`
```json
{
  "id": "ds_1",
  "name": "Customer Churn Data",
  "rows": 1000,
  "columns": 15,
  "file_hash": "abc123...",
  "created_at": "2024-10-20T10:30:00Z",
  "target_column": "churn",
  "task_type": "classification"
}
```

**Error Cases:**
- `400` - Invalid CSV format
- `400` - Empty dataset
- `400` - File too large (>1M rows)

---

### 2. List Datasets
**GET** `/datasets`

**Response:** `200 OK`
```json
[
  {
    "id": "ds_1",
    "name": "Customer Churn Data",
    "rows": 1000,
    "columns": 15,
    "task_type": "classification",
    "created_at": "2024-10-20T10:30:00Z"
  }
]
```

---

### 3. Get Dataset Details
**GET** `/datasets/{dataset_id}`

**Response:** `200 OK`
```json
{
  "metadata": {
    "id": "ds_1",
    "name": "Customer Churn Data",
    "rows": 1000,
    "columns": 15,
    "file_hash": "abc123...",
    "created_at": "2024-10-20T10:30:00Z"
  },
  "quality_report": {
    "total_rows": 1000,
    "total_columns": 15,
    "memory_usage_mb": 2.5,
    "duplicate_rows": 5,
    "duplicate_percentage": 0.5,
    "missing_cells_percentage": 2.1,
    "columns": [
      {
        "name": "age",
        "dtype": "numeric",
        "non_null_count": 980,
        "null_percentage": 2.0,
        "unique_count": 65,
        "constant": false,
        "mean": 45.2,
        "std": 15.1,
        "min": 18,
        "max": 85
      }
    ],
    "warnings": [
      "Constant column detected: 'id'"
    ]
  },
  "preview": {
    "rows": [ /* first 50 rows */ ],
    "count": 50
  }
}
```

---

### 4. Get Dataset Profile
**GET** `/datasets/{dataset_id}/profile`

**Response:** `200 OK`
```json
{
  "total_rows": 1000,
  "total_columns": 15,
  "memory_usage_mb": 2.5,
  "duplicate_rows": 5,
  "duplicate_percentage": 0.5,
  "missing_cells_percentage": 2.1,
  "columns": [ /* column profiles */ ],
  "warnings": [ /* data quality warnings */ ]
}
```

---

## Experiments API

### 1. Create Experiment
**POST** `/experiments`

**Request:**
```json
{
  "dataset_id": "ds_1",
  "name": "Churn Prediction Q4",
  "research_question": "What factors drive customer churn?",
  "target_column": "churn",
  "task_type": "classification"
}
```

**Response:** `200 OK`
```json
{
  "id": "exp_1",
  "dataset_id": "ds_1",
  "name": "Churn Prediction Q4",
  "research_question": "What factors drive customer churn?",
  "status": "setup",
  "created_at": "2024-10-20T10:30:00Z",
  "updated_at": "2024-10-20T10:30:00Z"
}
```

---

### 2. Get Experiment Details
**GET** `/experiments/{experiment_id}`

**Response:** `200 OK`
```json
{
  "id": "exp_1",
  "dataset_id": "ds_1",
  "name": "Churn Prediction Q4",
  "research_question": "What factors drive customer churn?",
  "status": "running",
  "created_at": "2024-10-20T10:30:00Z",
  "runs": [
    {
      "id": "run_1",
      "approach": "ai_baseline",
      "status": "completed",
      "accuracy": 0.78
    }
  ]
}
```

---

## Analysis API

### 1. Generate Analysis Plan
**POST** `/analysis-plans`

**Request:**
```json
{
  "experiment_id": "exp_1",
  "research_question": "What factors drive customer churn?",
  "dataset_profile": {
    "rows": 1000,
    "columns": 15,
    "numeric_stats": { /* statistics */ },
    "categorical_stats": { /* statistics */ }
  }
}
```

**Response:** `200 OK`
```json
{
  "id": "plan_1",
  "experiment_id": "exp_1",
  "research_question": "What factors drive customer churn?",
  "proposed_techniques": [
    "Exploratory Data Analysis with visualization",
    "Categorical feature encoding and analysis",
    "Statistical correlation analysis",
    "Model training and evaluation"
  ],
  "techniques_rationale": "Automatically generated based on data characteristics...",
  "execution_steps": [
    "Data cleaning and validation",
    "Exploratory data analysis",
    "Feature engineering and selection",
    "Model training and evaluation"
  ],
  "estimated_time_minutes": 25,
  "estimated_cost_credits": 50,
  "risk_assessment": "None detected",
  "high_correlations": [
    {
      "column1": "age",
      "column2": "income",
      "correlation": 0.75
    }
  ],
  "created_at": "2024-10-20T10:30:00Z"
}
```

---

### 2. Get Analysis Plan
**GET** `/analysis-plans/{plan_id}`

Returns the same structure as plan generation response.

---

### 3. Execute Analysis Plan
**POST** `/analysis-plans/{plan_id}/execute`

**Response:** `200 OK`
```json
{
  "plan_id": "plan_1",
  "status": "executing",
  "run_id": "run_1",
  "execution_started": "2024-10-20T10:30:00Z",
  "results": {
    "execution_start": "2024-10-20T10:30:00Z",
    "status": "completed",
    "primary_metric": 0.784,
    "secondary_metrics": {
      "precision": 0.81,
      "recall": 0.76,
      "f1_score": 0.785,
      "model_interpretability": 0.89
    },
    "techniques_applied": [
      "Exploratory Data Analysis",
      "Feature Engineering",
      "Logistic Regression"
    ],
    "key_findings": [
      "Contract type is primary churn predictor",
      "Tenure shows strong negative correlation with churn",
      "Monthly charges significant in model decisions"
    ],
    "errors_detected": 3,
    "warnings": [
      "Class imbalance detected (75% vs 25%)",
      "Some features show multicollinearity"
    ],
    "execution_time_seconds": 23.45
  }
}
```

---

## Runs API

### 1. Get Run Status
**GET** `/runs/{run_id}`

**Response:** `200 OK`
```json
{
  "id": "run_1",
  "experiment_id": "exp_1",
  "approach": "ai_baseline",
  "status": "completed",
  "created_at": "2024-10-20T10:30:00Z",
  "started_at": "2024-10-20T10:30:05Z",
  "completed_at": "2024-10-20T10:30:28Z",
  "results": { /* analysis results */ },
  "error_message": null
}
```

---

### 2. Run Verification
**POST** `/runs/{run_id}/verify`

**Request:**
```json
{
  "approach": "independent_verification",
  "verifier_id": "ai_v2"
}
```

**Response:** `200 OK`
```json
{
  "verification_id": "verif_1",
  "run_id": "run_1",
  "status": "completed",
  "verification_approach": "independent_verification",
  "verification_accuracy": 0.89,
  "errors_found": {
    "methodology_errors": 2,
    "calculation_errors": 1,
    "interpretation_errors": 0,
    "data_handling_errors": 1
  },
  "error_breakdown": {
    "Critical": 1,
    "Major": 2,
    "Minor": 1
  },
  "confidence_score": 0.94,
  "recommendations": [
    "Validate feature engineering approach",
    "Review model assumptions",
    "Consider additional cross-validation folds"
  ],
  "verification_time_seconds": 45.23,
  "overall_assessment": "PASS"
}
```

---

## Results API

### 1. Get Experiment Comparison
**GET** `/experiments/{experiment_id}/comparison`

**Response:** `200 OK`
```json
{
  "experiment_id": "exp_1",
  "ai_baseline": {
    "accuracy": 0.784,
    "errors": 12,
    "warnings": 3,
    "execution_time": 23.45
  },
  "independent_verification": {
    "accuracy": 0.89,
    "errors": 5,
    "confidence": 0.94,
    "execution_time": 45.23
  },
  "improvement_metrics": {
    "accuracy_improvement_percent": 13.5,
    "error_reduction": 58.3,
    "reliability_boost": 10.6
  },
  "key_insight": "Independent verification significantly reduces errors and improves reliability",
  "timestamp": "2024-10-20T10:31:00Z"
}
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Access denied |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Duplicate resource |
| 422 | Validation Error - Invalid data format |
| 500 | Server Error - Internal error |

---

## Rate Limiting

- **Free Tier**: 100 requests/minute
- **Pro Tier**: 1000 requests/minute
- **Enterprise**: Unlimited

Headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1635000000
```

---

## Pagination

For list endpoints, use query parameters:
```
?page=1&limit=20&sort=-created_at
```

Response includes:
```json
{
  "data": [ /* results */ ],
  "pagination": {
    "total": 150,
    "page": 1,
    "limit": 20,
    "pages": 8
  }
}
```

---

## WebSocket Events (Future)

```javascript
ws://localhost:8000/api/v1/ws/experiments/{experiment_id}

Events:
- run:started
- run:progress (progress: 0-100)
- run:completed
- verification:started
- verification:completed
- error:occurred
```

---

## Code Examples

### Python (requests)
```python
import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

# Upload dataset
with open('data.csv', 'rb') as f:
    response = requests.post(
        f"{BASE_URL}/datasets",
        files={'file': f},
        data={'name': 'My Dataset'}
    )
    dataset = response.json()
    print(f"Dataset created: {dataset['id']}")

# Create analysis plan
response = requests.post(
    f"{BASE_URL}/analysis-plans",
    json={
        "experiment_id": "exp_1",
        "research_question": "What drives churn?"
    }
)
print(response.json())
```

### JavaScript/TypeScript
```typescript
import { apiClient } from './api/client';

// Upload dataset
const formData = new FormData();
formData.append('file', file);
formData.append('name', 'My Dataset');

const response = await apiClient.uploadDataset(file, {
  name: 'My Dataset'
});

// Generate plan
const plan = await apiClient.createAnalysisPlan({
  experiment_id: 'exp_1',
  research_question: 'What drives churn?'
});
```

---

## Webhook Events (Future)

Register webhooks for:
- `dataset.uploaded`
- `experiment.completed`
- `verification.completed`
- `results.ready`

```json
POST /webhooks
{
  "url": "https://your-app.com/webhooks",
  "events": ["experiment.completed"],
  "secret": "whsec_xxx"
}
```

---

**Last Updated**: October 20, 2024  
**API Version**: v1  
**Status**: Ready for Development
