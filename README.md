# DataScientist Arena — AI Reliability & Data Science Benchmarking Platform

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Project Overview

**Can AI perform data science correctly?**

DataScientist Arena is a comprehensive research platform that tests whether AI can perform data science tasks correctly, identifies its mistakes, and measures whether independent verification improves results.

### Core Research Question
**Does independent verification substantially reduce errors in AI-generated data science workflows?**

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│    React + TypeScript Frontend (Vite)       │
│  Dashboard, Dataset Explorer, Analysis UI   │
└────────────────┬────────────────────────────┘
                 │
        ┌────────▼────────┐
        │  FastAPI Backend │
        │  Pydantic Schemas│
        └────────┬────────┘
                 │
    ┌────────────┴────────────┐
    │                         │
┌───▼──────────┐    ┌────────▼──────┐
│ Data Engine  │    │  Local LLM    │
│ (Pandas)     │    │  (Ollama)     │
└──────────────┘    └───────────────┘
    │                    │
    └────────┬───────────┘
             │
    ┌────────▼─────────────┐
    │ Verification Engine  │
    │ Independent Checks   │
    └──────────────────────┘
             │
    ┌────────▼─────────────┐
    │   SQLite / Data      │
    │   Artifact Storage   │
    └──────────────────────┘
```

## 📦 Project Structure

```
datascientist-arena/
├── frontend/                      # React + TypeScript UI
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── DatasetUpload.tsx
│   │   │   ├── DataExplorer.tsx
│   │   │   ├── AnalysisConfig.tsx
│   │   │   ├── AILab.tsx
│   │   │   ├── RunMonitor.tsx
│   │   │   ├── VerificationCenter.tsx
│   │   │   ├── Results.tsx
│   │   │   ├── ErrorAnalysis.tsx
│   │   │   └── ReportBuilder.tsx
│   │   ├── layouts/
│   │   │   └── MainLayout.tsx
│   │   ├── types/
│   │   │   └── api.ts
│   │   ├── hooks/
│   │   │   └── useApi.ts
│   │   ├── styles/
│   │   │   └── globals.css
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                       # Python FastAPI
│   ├── app/
│   │   ├── api/
│   │   │   ├── datasets.py
│   │   │   ├── analysis.py
│   │   │   ├── experiments.py
│   │   │   ├── verification.py
│   │   │   └── results.py
│   │   ├── core/
│   │   │   ├── data_engine.py
│   │   │   ├── ai_engine.py
│   │   │   ├── verification_engine.py
│   │   │   └── config.py
│   │   ├── schemas/
│   │   │   ├── dataset.py
│   │   │   ├── experiment.py
│   │   │   ├── analysis.py
│   │   │   └── verification.py
│   │   ├── services/
│   │   │   ├── profiler.py
│   │   │   ├── executor.py
│   │   │   └── reporter.py
│   │   ├── database/
│   │   │   ├── models.py
│   │   │   └── db.py
│   │   └── main.py
│   ├── tests/
│   │   ├── test_profiler.py
│   │   ├── test_executor.py
│   │   └── test_verification.py
│   ├── requirements.txt
│   └── pyproject.toml
│
├── benchmarks/
│   ├── registry/
│   │   └── datasets.json
│   ├── task_definitions/
│   │   └── classification.json
│   └── README.md
│
├── research/
│   ├── methodology.md
│   ├── hypotheses.md
│   ├── analysis_plan.md
│   └── results/
│
├── docs/
│   ├── architecture.md
│   ├── api.md
│   ├── setup.md
│   └── security.md
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Ollama (for local LLM)
- Docker (optional)

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start FastAPI server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Local LLM Setup

```bash
# Install Ollama from https://ollama.ai
# Pull a compact model
ollama pull mistral

# Start Ollama (runs on port 11434)
ollama serve
```

## 📊 Key Features

### 1️⃣ Dataset Intelligence
- CSV upload with drag-and-drop
- Automatic schema detection
- Missing value analysis
- Duplicate detection
- Data quality profiling
- Imbalance warnings

### 2️⃣ AI Analysis Lab
- Local LLM-powered analysis planning
- Structured plan generation (JSON format)
- Zero arbitrary code execution
- Model selection reasoning
- Preprocessing recommendations

### 3️⃣ Independent Verifier
- Metric recalculation from saved predictions
- Data split validation
- Preprocessing leakage detection
- Statistical claim verification
- Evidence-backed findings

### 4️⃣ Experiment Orchestration
- Three comparable approaches:
  - **Baseline**: Conventional ML pipeline
  - **AI-Generated**: LLM-proposed workflow
  - **Verified AI**: LLM + independent verification
- Reproducible runs with fixed seeds
- Complete execution timeline
- Resource tracking

### 5️⃣ Results & Visualization
- Side-by-side approach comparison
- Confusion matrices & performance metrics
- Error analysis breakdown
- Verification findings dashboard
- Downloadable reports (HTML/PDF)

## 🧪 Research Methodology

### Error Categories
- **Planning Error**: Invalid analysis strategy
- **Execution Error**: Workflow fails or diverges from plan
- **Numerical Error**: Incorrect metric calculation
- **Evaluation Error**: Data leakage or invalid splitting
- **Interpretation Error**: Conclusions unsupported by evidence
- **Reproducibility Error**: Cannot rerun to standard

### Metrics We Measure
1. **Plan Validity Rate** = Valid Plans / All Attempted Plans
2. **Undetected Error Rate** = Errors Left Undetected / Errors Introduced
3. **Verification Recall** = Known Errors Detected / All Known Errors
4. **False-Positive Rate** = Correct Results Flagged / All Truly Correct Results
5. **Overhead & Reliability** = Runtime, Model Calls, Resource Usage

## 🔒 Security & Privacy

- ✅ File validation & safe CSV parsing
- ✅ LLM input sanitization
- ✅ No code execution from untrusted input
- ✅ Execution sandboxing with timeouts
- ✅ Local data processing (no external AI services)
- ✅ Dependency pinning & lockfiles
- ✅ Reproducibility tracking

## 📈 Implementation Timeline

| Week | Focus | Deliverable |
|------|-------|------------|
| 1 | Foundation & Data Pipeline | Dataset upload + profiling |
| 2 | Baseline ML Engine | Trained baseline classifier |
| 3 | Local LLM Integration | AI Analysis Lab |
| 4 | Verification Engine | Independent verifier |
| 5 | Experiment Framework | Orchestration & runs |
| 6 | Frontend | Professional UI |
| 7 | Results Visualization | Dashboard & reports |
| 8 | Testing & Polish | Security, performance |
| 9 | Benchmarking | Full experiment suite |
| 10 | Analysis | Results interpretation |
| 11 | Documentation | Setup guides |
| 12 | Release | Portfolio-ready |

## 📚 Benchmark Datasets

Initial benchmark suite (3-5 datasets):
- **Iris**: Small multiclass classification
- **Breast Cancer Wisconsin**: Binary classification
- **Wine Quality**: Multiclass with imbalance
- **Adult Census Income**: Fairness considerations
- **Custom Challenge**: Class imbalance case

## 🎓 What This Demonstrates

✨ **AI & LLMs** - Local model integration, structured plan generation  
✨ **Machine Learning** - Pipelines, model selection, metrics  
✨ **Statistics** - Hypothesis testing, evidence evaluation  
✨ **Software Engineering** - Full-stack app, testing, DevOps  
✨ **Research** - Experimental design, rigorous evaluation  

## 📝 License

MIT License - See LICENSE file

## 🤝 Contributing

This is a research project. Contributions welcome for:
- Additional benchmark datasets
- Verification check implementations
- Error categorization refinements
- Documentation improvements

## 📧 Contact & Questions

For questions about the project design, please refer to:
- `research/methodology.md` - Research foundations
- `docs/api.md` - API specifications
- `docs/architecture.md` - System design

---

**Built with ❤️ for rigorous AI evaluation**

*"The strongest AI systems are those that can identify their own limitations."*
