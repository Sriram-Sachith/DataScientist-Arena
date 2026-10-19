# DataScientist Arena - Personalized API Documentation

## Overview

The Personalized API system extends the DataScientist Arena with:
- **User Authentication** (JWT-based)
- **Role-Based Access Control (RBAC)**
- **API Keys & Programmatic Access**
- **Workspaces** for team collaboration
- **Experiment Templates** for faster workflows
- **Notifications** for real-time updates
- **Activity Logging** for audit trails
- **User Preferences** for customization

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend (React)                       │
│  • Login/Register pages                                 │
│  • Auth Context (manages token + user state)            │
│  • Protected routes with role checking                  │
└─────────────────────────────────────────────────────────┘
                         ↕ HTTP/JSON
┌─────────────────────────────────────────────────────────┐
│                  Backend (FastAPI)                       │
│                                                          │
│  Users Router (/users)                                  │
│  ├─ POST /register - Create account                     │
│  ├─ POST /login - Authenticate user                     │
│  ├─ GET /me - Get current profile                       │
│  ├─ PUT /me - Update profile                            │
│  ├─ GET /me/preferences - User preferences              │
│  ├─ PUT /me/preferences - Update preferences            │
│  ├─ GET /me/stats - User statistics                     │
│  ├─ GET /me/dashboard - Personalized dashboard          │
│  ├─ POST /logout - Logout                               │
│  └─ POST /refresh-token - Refresh JWT token             │
│                                                          │
│  Personalization Router (/personalization)              │
│  ├─ API Keys (CRUD operations)                          │
│  ├─ Workspaces (create, list, join)                     │
│  ├─ Workspace Members (add, remove, permissions)        │
│  ├─ Experiment Templates (create, list, rate)           │
│  └─ Notifications (list, mark read, delete)             │
│                                                          │
│  Auth Module (core/auth.py)                             │
│  ├─ PasswordManager - Hash & verify passwords           │
│  ├─ TokenManager - JWT creation & verification          │
│  ├─ APIKeyManager - API key generation & validation     │
│  └─ RBACManager - Role-based permissions                │
│                                                          │
│  Models (models/user.py)                                │
│  ├─ User - User profiles & settings                     │
│  ├─ APIKey - API key storage & management               │
│  ├─ Workspace - Collaborative workspaces                │
│  ├─ WorkspaceMember - Team membership                   │
│  ├─ ExperimentTemplate - Reusable templates             │
│  ├─ Notification - User notifications                   │
│  └─ ActivityLog - Audit trail                           │
└─────────────────────────────────────────────────────────┘
                         ↕ SQL
┌─────────────────────────────────────────────────────────┐
│                   Database                              │
│  • SQLite (development)                                 │
│  • PostgreSQL (production)                              │
│  • 7 relational tables with constraints                 │
└─────────────────────────────────────────────────────────┘
```

---

## API Endpoints

### Authentication Endpoints

#### 1. Register User
**POST** `/api/v1/users/register`

**Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePassword123",
  "full_name": "John Doe"  // optional
}
```

**Response:** `201 Created`
```json
{
  "id": "user_123abc",
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "avatar_url": null,
  "bio": null,
  "organization": null,
  "role": "researcher",
  "created_at": "2024-10-20T10:30:00Z",
  "last_login": null,
  "is_verified": false
}
```

**Error Cases:**
- `409 Conflict` - Username or email already exists
- `422 Validation Error` - Invalid input

---

#### 2. Login User
**POST** `/api/v1/users/login`

**Request:**
```json
{
  "username": "john_doe",
  "password": "SecurePassword123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": "user_123abc",
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "role": "researcher",
    "created_at": "2024-10-20T10:30:00Z",
    "last_login": "2024-10-20T14:22:15Z",
    "is_verified": true
  }
}
```

**Error Cases:**
- `401 Unauthorized` - Invalid credentials
- `404 Not Found` - User not found

---

#### 3. Get Current User Profile
**GET** `/api/v1/users/me`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "id": "user_123abc",
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "avatar_url": "https://...",
  "bio": "Data scientist and AI researcher",
  "organization": "Acme Corp",
  "role": "researcher",
  "created_at": "2024-10-20T10:30:00Z",
  "last_login": "2024-10-20T14:22:15Z",
  "is_verified": true
}
```

---

#### 4. Update User Profile
**PUT** `/api/v1/users/me`

**Request:**
```json
{
  "full_name": "John Doe Jr",
  "bio": "Updated bio",
  "organization": "New Org",
  "theme": "dark",
  "timezone": "US/Eastern"
}
```

**Response:** `200 OK`
- Returns updated user profile

---

#### 5. Get User Preferences
**GET** `/api/v1/users/me/preferences`

**Response:** `200 OK`
```json
{
  "auto_save": true,
  "show_tooltips": true,
  "default_analysis_approach": "independent_verification",
  "export_format": "pdf",
  "notifications_enabled": true,
  "email_on_completion": true,
  "dark_mode": true
}
```

---

#### 6. Update User Preferences
**PUT** `/api/v1/users/me/preferences`

**Request:**
```json
{
  "auto_save": false,
  "dark_mode": false,
  "default_analysis_approach": "ai_baseline"
}
```

**Response:** `200 OK`
- Returns updated preferences

---

#### 7. Get User Statistics
**GET** `/api/v1/users/me/stats`

**Response:** `200 OK`
```json
{
  "total_datasets": 12,
  "total_experiments": 45,
  "completed_experiments": 42,
  "active_experiments": 3,
  "average_accuracy": 0.856,
  "total_storage_mb": 5250.75,
  "api_calls_today": 1250,
  "last_activity": "2024-10-20T14:22:15Z"
}
```

---

#### 8. Get Personalized Dashboard
**GET** `/api/v1/users/me/dashboard`

**Response:** `200 OK`
```json
{
  "user": { /* user profile */ },
  "stats": { /* user stats */ },
  "recent_experiments": [
    {
      "id": "exp_1",
      "name": "Churn Prediction Q4",
      "status": "completed",
      "accuracy": 0.89,
      "created_at": "2024-10-20T10:00:00Z"
    }
  ],
  "recent_datasets": [
    {
      "id": "ds_1",
      "name": "Customer Data",
      "rows": 10000,
      "columns": 15,
      "created_at": "2024-10-20T09:00:00Z"
    }
  ],
  "upcoming_notifications": [],
  "workspace": null
}
```

---

#### 9. Refresh Token
**POST** `/api/v1/users/refresh-token`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": { /* updated user profile */ }
}
```

---

#### 10. Logout
**POST** `/api/v1/users/logout`

**Response:** `200 OK`
```json
{
  "message": "Successfully logged out"
}
```

---

### API Key Management

#### Create API Key
**POST** `/api/v1/personalization/api-keys`

**Request:**
```json
{
  "name": "Production API Key",
  "description": "Key for production dashboard",
  "scopes": [
    "read:datasets",
    "read:experiments",
    "read:results",
    "create:experiment"
  ],
  "expires_in_days": 90,
  "ip_whitelist": ["192.168.1.1", "10.0.0.0/8"]
}
```

**Response:** `201 Created`
```json
{
  "id": "key_abc123",
  "name": "Production API Key",
  "description": "Key for production dashboard",
  "key": "dsa_sk_prod_1234567890abcdef...",  // Only shown on creation!
  "scopes": ["read:datasets", "read:experiments", "read:results", "create:experiment"],
  "is_active": true,
  "rate_limit": 1000,
  "created_at": "2024-10-20T10:30:00Z",
  "expires_at": "2025-01-18T10:30:00Z",
  "last_used": null
}
```

---

#### List API Keys
**GET** `/api/v1/personalization/api-keys`

**Response:** `200 OK`
```json
[
  {
    "id": "key_abc123",
    "name": "Production API Key",
    "description": "Key for production dashboard",
    "scopes": ["read:datasets", "read:experiments", "read:results"],
    "is_active": true,
    "rate_limit": 1000,
    "created_at": "2024-10-20T10:30:00Z",
    "expires_at": "2025-01-18T10:30:00Z",
    "last_used": "2024-10-20T14:22:15Z"
  }
]
```

---

#### Update API Key
**PUT** `/api/v1/personalization/api-keys/{key_id}`

**Request:**
```json
{
  "name": "Updated Name",
  "is_active": false,
  "rate_limit": 500
}
```

**Response:** `200 OK`
- Returns updated API key

---

#### Delete API Key
**DELETE** `/api/v1/personalization/api-keys/{key_id}`

**Response:** `204 No Content`

---

### Workspace Management

#### Create Workspace
**POST** `/api/v1/personalization/workspaces`

**Request:**
```json
{
  "name": "Data Science Team",
  "description": "Team workspace for DS projects",
  "is_private": true
}
```

**Response:** `201 Created`
```json
{
  "id": "ws_123abc",
  "name": "Data Science Team",
  "description": "Team workspace for DS projects",
  "slug": "data-science-team-ws123",
  "owner_id": "user_123abc",
  "is_private": true,
  "created_at": "2024-10-20T10:30:00Z",
  "member_count": 1
}
```

---

#### List Workspaces
**GET** `/api/v1/personalization/workspaces`

**Response:** `200 OK`
```json
[
  {
    "id": "ws_123abc",
    "name": "Data Science Team",
    "slug": "data-science-team-ws123",
    "owner_id": "user_123abc",
    "is_private": true,
    "created_at": "2024-10-20T10:30:00Z",
    "member_count": 3
  }
]
```

---

### Experiment Templates

#### Create Template
**POST** `/api/v1/personalization/templates`

**Request:**
```json
{
  "name": "Customer Churn Prediction",
  "description": "Template for churn prediction models",
  "category": "churn",
  "default_approach": "independent_verification",
  "analysis_steps": [
    "Data cleaning",
    "Feature engineering",
    "Model training",
    "Evaluation"
  ],
  "recommended_techniques": [
    "Logistic Regression",
    "Random Forest",
    "Gradient Boosting"
  ],
  "is_public": true
}
```

**Response:** `201 Created`
```json
{
  "id": "tmpl_abc123",
  "name": "Customer Churn Prediction",
  "category": "churn",
  "creator_id": "user_123abc",
  "is_public": true,
  "usage_count": 0,
  "rating": 0.0,
  "created_at": "2024-10-20T10:30:00Z"
}
```

---

#### List Templates
**GET** `/api/v1/personalization/templates?category=churn`

**Response:** `200 OK`
```json
[
  {
    "id": "tmpl_abc123",
    "name": "Customer Churn Prediction",
    "category": "churn",
    "creator_id": "user_123abc",
    "is_public": true,
    "usage_count": 42,
    "rating": 4.7,
    "created_at": "2024-10-20T10:30:00Z"
  }
]
```

---

### Notifications

#### List Notifications
**GET** `/api/v1/personalization/notifications?unread_only=true`

**Response:** `200 OK`
```json
[
  {
    "id": "notif_123abc",
    "title": "Experiment Completed",
    "message": "Your experiment 'Churn Prediction Q4' has completed",
    "notification_type": "experiment_complete",
    "is_read": false,
    "created_at": "2024-10-20T14:22:15Z",
    "action_url": "/results/exp_1"
  }
]
```

---

#### Mark Notification as Read
**PUT** `/api/v1/personalization/notifications/{notification_id}/read`

**Response:** `200 OK`
- Returns updated notification with `is_read: true`

---

#### Mark All as Read
**PUT** `/api/v1/personalization/notifications/mark-all-read`

**Response:** `200 OK`
```json
{
  "message": "All notifications marked as read"
}
```

---

## Role-Based Access Control (RBAC)

### Roles & Permissions

| Role | Permissions |
|------|-------------|
| **admin** | All permissions + user management + analytics |
| **researcher** | Create/update experiments, run analysis, view results |
| **analyst** | View datasets, run experiments, view results |
| **viewer** | Read-only access to datasets, experiments, results |

### Permission Model

```python
PERMISSIONS = {
  "admin": [
    "create:dataset", "read:dataset", "update:dataset", "delete:dataset",
    "create:experiment", "read:experiment", "update:experiment", "delete:experiment",
    "manage:users", "manage:workspace", "view:analytics"
  ],
  "researcher": [
    "create:dataset", "read:dataset", "update:dataset",
    "create:experiment", "read:experiment", "update:experiment", "run:experiment",
    "read:results"
  ],
  "analyst": [
    "read:dataset", "create:experiment", "read:experiment", "run:experiment",
    "read:results"
  ],
  "viewer": [
    "read:dataset", "read:experiment", "read:results"
  ]
}
```

---

## Authentication Flow

### JWT Token Structure

```
Header:
{
  "alg": "HS256",
  "typ": "JWT"
}

Payload:
{
  "sub": "user_123abc",  // User ID
  "exp": 1634765400,     // Expiration time
  "iat": 1634761800,     // Issued at
  "type": "access"       // Token type
}

Signature:
HMACSHA256(base64UrlEncode(header) + "." + base64UrlEncode(payload), SECRET_KEY)
```

### Token Refresh Flow

```
1. Client sends access token to /users/refresh-token
2. Server verifies token signature & expiration
3. Server creates new access token
4. Client stores new token (replaces old one)
5. Old token remains valid until original expiration
```

---

## Security Best Practices

### For Users
- ✅ Store tokens securely (HttpOnly cookies recommended)
- ✅ Use HTTPS for all requests
- ✅ Rotate API keys regularly
- ✅ Set IP whitelists for API keys
- ✅ Never hardcode tokens in code

### For Developers
- ✅ Validate all inputs server-side
- ✅ Implement rate limiting per user
- ✅ Log all authentication attempts
- ✅ Use password hashing (bcrypt)
- ✅ Implement CORS properly
- ✅ Add audit trails for sensitive operations

### API Key Security
- Keys are hashed before storage (SHA256)
- Raw keys only shown once on creation
- Support IP whitelisting
- Rate limiting per key
- Automatic expiration support

---

## Code Examples

### JavaScript/TypeScript

```typescript
// Login
const response = await fetch('http://localhost:8000/api/v1/users/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'john_doe',
    password: 'SecurePassword123'
  })
});

const { access_token } = await response.json();
localStorage.setItem('token', access_token);

// Make authenticated request
const userResponse = await fetch('http://localhost:8000/api/v1/users/me', {
  headers: {
    'Authorization': `Bearer ${access_token}`
  }
});

// Create API Key
const keyResponse = await fetch('http://localhost:8000/api/v1/personalization/api-keys', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${access_token}`
  },
  body: JSON.stringify({
    name: 'Production Key',
    scopes: ['read:datasets', 'read:experiments']
  })
});

const { key } = await keyResponse.json();
console.log('Store this key safely:', key);
```

### Python

```python
import requests
import json

# Login
response = requests.post(
    'http://localhost:8000/api/v1/users/login',
    json={
        'username': 'john_doe',
        'password': 'SecurePassword123'
    }
)

token = response.json()['access_token']

# Authenticated request
headers = {
    'Authorization': f'Bearer {token}'
}

user = requests.get(
    'http://localhost:8000/api/v1/users/me',
    headers=headers
).json()

print(f"Welcome {user['full_name']}")

# Get stats
stats = requests.get(
    'http://localhost:8000/api/v1/users/me/stats',
    headers=headers
).json()

print(f"Total experiments: {stats['total_experiments']}")
```

### cURL

```bash
# Register
curl -X POST http://localhost:8000/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePassword123"
  }'

# Login
TOKEN=$(curl -X POST http://localhost:8000/api/v1/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePassword123"
  }' | jq -r '.access_token')

# Get profile
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer $TOKEN"

# Create API Key
curl -X POST http://localhost:8000/api/v1/personalization/api-keys \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "My API Key",
    "scopes": ["read:datasets", "read:experiments"]
  }'
```

---

## Migration Guide

### From Anonymous to Authenticated

1. **Add AuthProvider to App**
   ```tsx
   <AuthProvider>
     <AppProvider>
       <App />
     </AppProvider>
   </AuthProvider>
   ```

2. **Protect Routes**
   ```tsx
   <Route 
     path="/dashboard" 
     element={
       <RequireAuth>
         <Dashboard />
       </RequireAuth>
     } 
   />
   ```

3. **Use Auth in Components**
   ```tsx
   const { user, token, logout } = useAuth();
   ```

4. **Include Auth Header in Requests**
   ```tsx
   const headers = {
     'Authorization': `Bearer ${token}`
   };
   ```

---

## Error Handling

### Common Error Responses

| Status | Error | Meaning |
|--------|-------|---------|
| 400 | Bad Request | Invalid input format |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Username/email already exists |
| 422 | Validation Error | Invalid data |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

### Error Response Format

```json
{
  "detail": "Invalid username or password",
  "status_code": 401,
  "error_code": "INVALID_CREDENTIALS"
}
```

---

## Rate Limiting

- **Free Plan**: 100 requests/minute per user
- **Pro Plan**: 1000 requests/minute per user
- **Enterprise**: Custom limits

Headers returned:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1634765400
```

---

## Database Schema

### User
```sql
CREATE TABLE users (
  id VARCHAR PRIMARY KEY,
  username VARCHAR UNIQUE,
  email VARCHAR UNIQUE,
  full_name VARCHAR,
  hashed_password VARCHAR,
  role ENUM('admin', 'researcher', 'analyst', 'viewer'),
  preferences JSON,
  created_at DATETIME,
  updated_at DATETIME,
  last_login DATETIME
);
```

### API Key
```sql
CREATE TABLE api_keys (
  id VARCHAR PRIMARY KEY,
  user_id VARCHAR FOREIGN KEY,
  key VARCHAR UNIQUE,  -- hashed
  scopes JSON,
  rate_limit INT,
  expires_at DATETIME,
  created_at DATETIME
);
```

---

## Testing the API

### Using Swagger UI
Navigate to: http://127.0.0.1:8000/api/docs

### Using Postman
1. Create new request
2. Set Authorization type to "Bearer Token"
3. Paste access token
4. Make requests

### Using Python Requests
```python
import requests

session = requests.Session()
session.headers.update({
    'Authorization': f'Bearer {token}'
})

# All requests will include the token
response = session.get('http://localhost:8000/api/v1/users/me')
```

---

## Future Enhancements

- [ ] OAuth2/SSO integration
- [ ] Two-factor authentication (2FA)
- [ ] WebSocket for real-time notifications
- [ ] Rate limiting per IP
- [ ] IP-based access control
- [ ] Audit logging dashboard
- [ ] API usage analytics
- [ ] Team collaboration features
- [ ] Subscription tiers
- [ ] Email notifications

---

**Documentation Version**: 1.0  
**Last Updated**: October 20, 2024  
**Status**: Production Ready
