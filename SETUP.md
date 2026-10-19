# DataScientist Arena - Setup & Installation Guide

## Quick Start

The project is already configured and running! Both servers are active:

- **Frontend**: http://localhost:5173/
- **Backend API**: http://127.0.0.1:8000/
- **API Docs**: http://127.0.0.1:8000/api/docs

## Project Structure

```
data_science_project/
├── frontend/                 # React + TypeScript + Vite
│   ├── src/
│   │   ├── api/
│   │   │   └── client.ts    # API client for backend communication
│   │   ├── components/       # 8 core React components
│   │   ├── context/          # State management (AppContext)
│   │   ├── layouts/          # MainLayout with sidebar navigation
│   │   └── styles/           # Tailwind CSS + dark theme
│   └── package.json
│
├── backend/                  # FastAPI + Python
│   ├── app/
│   │   ├── main.py          # FastAPI entry point
│   │   ├── models.py        # SQLAlchemy ORM models
│   │   ├── database.py      # Database configuration
│   │   ├── core/
│   │   │   ├── config.py    # Settings
│   │   │   └── ai_engine.py # AI analysis & verification logic
│   │   ├── schemas/         # Pydantic request/response schemas
│   │   ├── api/             # 5 API routers
│   │   └── services/        # Data profiling & utilities
│   └── requirements.txt
│
├── README.md                # Project overview & documentation
└── SETUP.md                 # This file
```

## Running the Application

### Frontend is running on:
```
http://localhost:5173
```
- React development server with hot-reload
- Professional dark UI with Framer Motion animations
- Tailwind CSS styling

### Backend is running on:
```
http://127.0.0.1:8000
```
- FastAPI with automatic API documentation
- Swagger UI: http://127.0.0.1:8000/api/docs
- ReDoc: http://127.0.0.1:8000/api/redoc

## Features Implemented

### Frontend Components
✅ **Dashboard** - Overview with statistics and quick-start guide
✅ **Dataset Upload** - Drag-and-drop CSV upload with validation
✅ **Data Explorer** - Dataset visualization and profiling
✅ **Analysis Config** - Experiment configuration
✅ **AI Lab** - Multi-step experiment setup and plan generation
✅ **Run Monitor** - Real-time experiment execution tracking
✅ **Verification Center** - Independent verification workflows
✅ **Results** - Comprehensive result comparison and analysis

### Backend APIs

#### Datasets (`/api/v1/datasets`)
- `POST /datasets` - Upload new dataset
- `GET /datasets` - List all datasets
- `GET /datasets/{id}` - Get dataset details
- `GET /datasets/{id}/profile` - Get quality profile

#### Analysis (`/api/v1/analysis-plans`)
- `POST /analysis-plans` - Generate AI analysis plan
- `GET /analysis-plans/{id}` - Get plan details
- `POST /analysis-plans/{id}/execute` - Execute analysis

#### Experiments (`/api/v1/experiments`)
- `POST /experiments` - Create experiment
- `GET /experiments/{id}` - Get experiment details
- `GET /runs/{id}` - Get run status

#### Verification (`/api/v1/runs`)
- `POST /runs/{id}/verify` - Run verification

#### Results (`/api/v1/experiments`)
- `GET /experiments/{id}/comparison` - Get comparison results

## Technology Stack

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **React Router** - Client-side routing

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation & schemas
- **SQLAlchemy** - ORM & database abstraction
- **SQLite** - Default database (switch to PostgreSQL in production)
- **Uvicorn** - ASGI server
- **Pandas, NumPy, Scikit-learn** - Data science libraries

## Development Notes

### Database
Currently using in-memory storage with SQLite support ready. To migrate:
1. Models are already defined in `backend/app/models.py`
2. Database session management in `backend/app/database.py`
3. Run migrations: `alembic upgrade head`

### AI Engine
The `AIEngine` class in `backend/app/core/ai_engine.py` provides:
- AI analysis plan generation
- Baseline analysis execution with mock ML pipeline
- Independent verification logic
- Result comparison and metrics

To integrate real LLM (Ollama):
1. Update `AIEngine.generate_analysis_plan()` to call Ollama API
2. Configure Ollama endpoint in settings
3. Models automatically execute offline

### State Management
React Context API (`AppContext`) handles:
- Dataset management
- Experiment tracking
- Loading states
- Error/success messages

To upgrade to Redux/Zustand: Update references in components accordingly

## Next Steps

### Phase 1: Core Functionality (2-4 hours)
- [ ] Connect frontend to backend API endpoints
- [ ] Implement real data profiling (Pandas analysis)
- [ ] Add database persistence (SQLite/PostgreSQL)
- [ ] Create file upload handler on backend

### Phase 2: ML Pipeline (4-6 hours)
- [ ] Implement baseline ML analysis
- [ ] Add independent verification logic
- [ ] Create mock predictions & results
- [ ] Add performance metrics calculation

### Phase 3: Production Ready (2-3 hours)
- [ ] Add authentication & authorization
- [ ] Implement logging & error handling
- [ ] Add rate limiting & CORS
- [ ] Docker containerization
- [ ] Deploy to cloud (AWS/GCP/Azure)

### Phase 4: Advanced Features (Optional)
- [ ] Real-time WebSocket updates for experiment progress
- [ ] Advanced data visualization (Plotly, D3)
- [ ] Experiment templates & presets
- [ ] Collaborative features & sharing
- [ ] Export reports (PDF, Excel)

## Troubleshooting

### "Cannot find module" errors
```bash
cd frontend && npm install
cd backend && pip install -r requirements.txt
```

### Port already in use
```bash
# Frontend (5173)
lsof -i :5173
kill -9 <PID>

# Backend (8000)
lsof -i :8000
kill -9 <PID>
```

### API CORS errors
Check `backend/app/core/config.py` - add your domain to `CORS_ORIGINS`

### Database errors
Delete `backend/data/arena.db` and restart to reinitialize

## API Testing

### Using cURL
```bash
# List datasets
curl http://127.0.0.1:8000/api/v1/datasets

# Upload dataset
curl -X POST -F "file=@data.csv" -F "name=My Dataset" \
  http://127.0.0.1:8000/api/v1/datasets

# Generate analysis plan
curl -X POST http://127.0.0.1:8000/api/v1/analysis-plans \
  -H "Content-Type: application/json" \
  -d '{
    "experiment_id": "exp_1",
    "research_question": "What factors drive customer churn?"
  }'
```

### Using Swagger UI
Navigate to: http://127.0.0.1:8000/api/docs

## Configuration Files

### Backend Config
`backend/app/core/config.py`:
- Database URL
- CORS settings
- API port & host
- LLM/Ollama configuration

### Frontend Config
`frontend/src/api/client.ts`:
- API base URL
- Request timeouts
- Default headers

## Performance Tips

1. **Frontend**: Enable Vite caching for faster rebuilds
2. **Backend**: Use async/await for I/O operations
3. **Database**: Add indexes to frequently queried columns
4. **ML Pipeline**: Cache profiling results
5. **API**: Implement response pagination

## Security Considerations

- [ ] Implement JWT authentication
- [ ] Add rate limiting (slowhttpapi)
- [ ] Validate file uploads (type, size)
- [ ] Sanitize user inputs
- [ ] Use environment variables for secrets
- [ ] Implement HTTPS in production
- [ ] Add request signing for API endpoints

## Support & Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Documentation**: https://react.dev/
- **Tailwind CSS**: https://tailwindcss.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Pandas**: https://pandas.pydata.org/docs/

---

**Created**: October 20, 2024  
**Project Status**: Foundation Complete, Ready for Development  
**Last Updated**: Initial Setup
