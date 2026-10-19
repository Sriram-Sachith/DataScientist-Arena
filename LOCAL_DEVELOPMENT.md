# Local Development Setup Guide

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn
- Git
- SQLite3 (built-in on macOS/Linux)

---

## Quick Start (5 minutes)

### 1. Clone/Navigate to Project
```bash
cd /Users/sriramsachithsp/Desktop/data_science_project
```

### 2. Install Backend Dependencies
```bash
cd backend
python3 -m pip install -r requirements.txt
```

**Installed packages:**
- fastapi==0.115.6
- uvicorn[standard]
- pydantic with email validation
- sqlalchemy, pandas, numpy, scikit-learn
- pytest, pytest-asyncio
- passlib, python-jose (JWT)
- python-dotenv, python-multipart
- And 15+ more...

### 3. Install Frontend Dependencies
```bash
cd ../frontend
npm install
```

**Installed packages:**
- react@18.3.1
- typescript@5.9.3
- vite@5.4.21
- tailwindcss@3.4.19
- framer-motion@10.18.0
- react-router-dom@6.30.6
- recharts@2.15.4
- And 10+ more...

### 4. Start Backend Server
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete
```

### 5. Start Frontend Server (New Terminal)
```bash
cd frontend
npm run dev
```

**Expected output:**
```
VITE v5.4.21 ready in 537 ms
➜ Local:   http://localhost:5173/
➜ Network: use --host to expose
```

### 6. Access the Application
- **Frontend**: http://localhost:5173/
- **Backend API**: http://127.0.0.1:8000/
- **API Docs**: http://127.0.0.1:8000/api/docs

---

## Environment Configuration

### Backend (.env)
Create `.env` file in backend directory:

```env
# Database
DATABASE_URL=sqlite:///./data/arena.db

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# CORS
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# Security
SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Logging
LOG_LEVEL=INFO
```

### Frontend (.env)
Create `.env` file in frontend directory:

```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_ENVIRONMENT=development
VITE_LOG_LEVEL=debug
```

---

## Database Setup

### Initialize Database
```bash
cd backend
python3 -c "from app.database import init_db; init_db()"
```

This creates:
- `data/arena.db` SQLite database
- 7 tables for users, datasets, experiments, etc.
- Relationships and constraints

### View Database
```bash
# Using sqlite3 CLI
sqlite3 backend/data/arena.db

# Inside sqlite3:
.tables                    # List all tables
.schema users              # View users table schema
SELECT COUNT(*) FROM users;  # Count users
.quit                      # Exit
```

### Database Models

**Tables created:**
1. **users** - User authentication and profiles
2. **api_keys** - API key management
3. **workspaces** - Team workspaces
4. **workspace_members** - Team membership
5. **experiment_templates** - Reusable templates
6. **notifications** - User notifications
7. **activity_logs** - Audit trail

---

## Development Workflow

### Backend Development

#### 1. Create New API Endpoint
```python
# File: backend/app/api/my_feature.py

from fastapi import APIRouter, HTTPException, Depends
from app.core.auth import get_current_user

router = APIRouter(prefix="/my-feature", tags=["my-feature"])

@router.get("/")
async def list_items(current_user_id: str = Depends(get_current_user)):
    """List user's items"""
    return {"items": []}

@router.post("/")
async def create_item(data: dict, current_user_id: str = Depends(get_current_user)):
    """Create new item"""
    return {"id": "item_123", "status": "created"}
```

#### 2. Add to Main App
```python
# File: backend/app/main.py

from app.api import my_feature

app.include_router(my_feature.router, prefix="/api/v1")
```

#### 3. Test with Swagger
1. Visit http://127.0.0.1:8000/api/docs
2. Find your endpoint
3. Click "Try it out"
4. Enter parameters and test

#### 4. Running Tests
```bash
cd backend
pytest tests/
pytest tests/test_auth.py -v        # Single file
pytest tests/test_auth.py::test_login -v  # Single test
pytest -x                           # Stop on first failure
pytest --cov                        # Coverage report
```

### Frontend Development

#### 1. Create New Component
```typescript
// File: src/components/MyComponent.tsx

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { apiClient } from '../api/client';
import { useAuth } from '../context/AuthContext';

export const MyComponent: React.FC = () => {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const result = await apiClient.get('/my-feature');
      setData(result.data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <h2>{user?.username}'s Component</h2>
      {loading ? <p>Loading...</p> : <pre>{JSON.stringify(data, null, 2)}</pre>}
    </motion.div>
  );
};
```

#### 2. Add Route
```typescript
// File: src/App.tsx

import { MyComponent } from './components/MyComponent';

<Route path="/my-component" element={
  <ProtectedRoute>
    <MyComponent />
  </ProtectedRoute>
} />
```

#### 3. Build for Production
```bash
cd frontend
npm run build
npm run preview        # Preview production build
```

---

## Common Development Tasks

### Running Both Servers
```bash
# Terminal 1
cd backend && uvicorn app.main:app --reload --port 8000

# Terminal 2 (new terminal)
cd frontend && npm run dev
```

### Debugging Frontend
```bash
# In browser DevTools (F12)
1. Go to Console tab
2. See logs: console.log(), console.error()
3. Network tab: see all API calls
4. Application tab: inspect localStorage, state
5. React DevTools extension: inspect component state
```

### Debugging Backend
```bash
# Add print statements
import logging
logger = logging.getLogger(__name__)
logger.info("Debug message")
logger.error("Error message")

# Or use debugger
import pdb; pdb.set_trace()  # Breakpoint
```

### Reset Database
```bash
# Delete database and reinitialize
rm backend/data/arena.db
python3 -c "from app.database import init_db; init_db()"
```

### Clear Cache
```bash
# Frontend
rm -rf frontend/node_modules/.vite

# Backend
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

### Update Dependencies
```bash
# Backend
pip install -U -r requirements.txt

# Frontend
npm update
npm audit fix  # Fix security vulnerabilities
```

---

## Testing

### Backend Unit Tests
```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_users.py -v

# Run specific test
pytest tests/test_users.py::test_user_registration -v

# Stop on first failure
pytest -x
```

### Frontend Unit Tests
```bash
cd frontend

# Run tests with Vitest
npm run test

# Run in watch mode
npm run test:watch

# Coverage report
npm run test:coverage
```

### Integration Testing
```bash
# 1. Start both servers
# Backend: cd backend && uvicorn app.main:app --reload
# Frontend: cd frontend && npm run dev

# 2. Open browser and manually test:
#    - Register new user
#    - Login with credentials
#    - Create dataset
#    - Run experiment
#    - View results
#    - Check API calls in DevTools

# 3. Verify database
sqlite3 backend/data/arena.db "SELECT COUNT(*) FROM users;"
```

---

## Performance Optimization

### Frontend Optimization
```bash
# Analyze bundle size
npm run build
npm install -g source-map-explorer
source-map-explorer 'dist/**/*.js'

# Production build
npm run build

# Check performance
npm run preview
# Visit http://localhost:4173/
```

### Backend Optimization
```python
# Use async where possible
async def my_endpoint():
    result = await some_async_operation()
    return result

# Enable database connection pooling
from sqlalchemy.pool import QueuePool
engine = create_engine(DATABASE_URL, poolclass=QueuePool, pool_size=10, max_overflow=20)
```

---

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -i :8000
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8001
```

### Module Not Found
```bash
# Backend
pip install -r requirements.txt
pip install --upgrade pip

# Frontend
rm -rf node_modules package-lock.json
npm install
```

### CORS Errors
```python
# Check backend CORS settings
# File: backend/app/core/config.py

CORS_ORIGINS = ["http://localhost:5173", "http://localhost:3000"]
```

### Database Locked
```bash
# Close all connections
# Delete database and reinitialize
rm backend/data/arena.db
python3 -c "from app.database import init_db; init_db()"
```

### Token Expired
```bash
# Clear localStorage and login again
# In browser console:
localStorage.removeItem('token');
location.reload();
```

---

## Git Workflow

### Before Starting
```bash
# Pull latest changes
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name
```

### While Developing
```bash
# Commit frequently
git add .
git commit -m "Add feature X"

# Push to remote
git push origin feature/your-feature-name
```

### Before PR
```bash
# Update main
git fetch origin
git rebase origin/main

# Run tests
pytest
npm run build

# Fix any conflicts/issues
```

### Create PR
```bash
# On GitHub/GitLab
# 1. Create PR from your branch to main
# 2. Add description of changes
# 3. Request review
# 4. Address feedback
# 5. Merge when approved
```

---

## Production Deployment

### Before Deploying
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] Security review completed
- [ ] Performance tested
- [ ] Documentation updated

### Build Artifacts
```bash
# Backend - nothing to build (pure Python)
# Just ensure requirements.txt is current

# Frontend - build static files
cd frontend
npm run build
# Creates dist/ folder with production build
```

### Deploy to Cloud
See DEPLOYMENT.md for:
- AWS Elastic Beanstalk
- Google Cloud Run
- Azure App Service
- Docker & Kubernetes
- Database setup (PostgreSQL)

---

## File Structure Reference

```
project/
├── backend/
│   ├── app/
│   │   ├── main.py              # Entry point
│   │   ├── models.py            # Database models
│   │   ├── database.py          # DB configuration
│   │   ├── core/
│   │   │   ├── config.py        # Settings
│   │   │   ├── auth.py          # Auth utilities
│   │   │   ├── ai_engine.py     # ML logic
│   │   │   └── verification_engine.py  # Verification
│   │   ├── schemas/             # Request/response schemas
│   │   ├── api/                 # Route handlers
│   │   ├── models/
│   │   │   └── user.py          # User models
│   │   └── services/            # Business logic
│   ├── tests/                   # Unit tests
│   ├── requirements.txt         # Dependencies
│   └── .env                     # Environment vars
│
├── frontend/
│   ├── src/
│   │   ├── main.tsx             # Entry point
│   │   ├── App.tsx              # Router
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── context/             # State management
│   │   ├── api/                 # API client
│   │   ├── layouts/             # Layout components
│   │   └── styles/              # CSS/Tailwind
│   ├── public/                  # Static files
│   ├── package.json             # Dependencies
│   ├── vite.config.ts           # Vite config
│   ├── tailwind.config.js       # Tailwind config
│   └── .env                     # Environment vars
│
└── Documentation/
    ├── README.md                # Project overview
    ├── SETUP.md                 # Setup guide
    ├── LOCAL_DEVELOPMENT.md     # This file
    ├── API_SPEC.md              # API reference
    ├── DEPLOYMENT.md            # Deployment guide
    └── PERSONALIZED_API.md      # Auth/personalization
```

---

## Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/
- **Tailwind CSS**: https://tailwindcss.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Scikit-learn**: https://scikit-learn.org/
- **Vite**: https://vitejs.dev/

---

**Last Updated**: October 20, 2024  
**Status**: Production Ready
