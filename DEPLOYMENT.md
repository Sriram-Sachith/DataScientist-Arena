# DataScientist Arena - Deployment Guide

## Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database migrations completed
- [ ] Frontend build optimized
- [ ] CORS settings updated for production domain
- [ ] API rate limiting enabled
- [ ] Authentication enabled
- [ ] Error logging configured
- [ ] SSL/TLS certificates ready
- [ ] Backup strategy in place

---

## Local Development

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or yarn

### Quick Start
```bash
# Clone and navigate
cd /Users/sriramsachithsp/Desktop/data_science_project

# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

### Access
- Frontend: http://localhost:5173/
- Backend: http://127.0.0.1:8000/
- API Docs: http://127.0.0.1:8000/api/docs

---

## Docker Deployment

### Build Docker Images

#### Backend Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend Dockerfile
```dockerfile
FROM node:18-alpine as builder

WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci

COPY frontend . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/arena
      - DEBUG=false
      - CORS_ORIGINS=https://yourdomain.com
    depends_on:
      - db
    restart: always

  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    ports:
      - "80:80"
    environment:
      - VITE_API_URL=https://api.yourdomain.com
    depends_on:
      - backend
    restart: always

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=arena
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

volumes:
  postgres_data:
```

### Build and Run
```bash
docker-compose build
docker-compose up -d
```

---

## Cloud Deployment

### AWS Deployment

#### Using AWS Elastic Beanstalk

**Backend:**
```bash
cd backend

# Create EB application
eb init -p python-3.10 datascientist-arena

# Create environment
eb create datascientist-arena-env

# Deploy
eb deploy
```

**Frontend:**
```bash
# Build
npm run build

# Deploy to S3 + CloudFront
aws s3 sync dist/ s3://your-bucket-name --delete
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

#### Using AWS RDS
```bash
# Create PostgreSQL database
aws rds create-db-instance \
  --db-instance-identifier datascientist-arena \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password YOUR_PASSWORD \
  --allocated-storage 20
```

#### Environment Variables (.ebextensions/environment.config)
```yaml
option_settings:
  aws:elasticbeanstalk:application:environment:
    DATABASE_URL: postgresql://admin:password@db-instance.amazonaws.com/arena
    DEBUG: false
    CORS_ORIGINS: https://yourdomain.com
    JWT_SECRET: your-secret-key
    ENVIRONMENT: production
```

### Google Cloud Deployment

#### Using Cloud Run

**Backend:**
```bash
gcloud run deploy datascientist-arena \
  --source . \
  --region us-central1 \
  --platform managed \
  --memory 2Gi \
  --set-env-vars DATABASE_URL=postgresql://...
```

**Frontend:**
```bash
# Build
npm run build

# Deploy to Cloud Storage + CDN
gsutil -m cp -r dist/* gs://your-bucket-name/
```

### Azure Deployment

#### Using App Service

**Backend:**
```bash
az webapp create \
  --resource-group myResourceGroup \
  --plan myAppServicePlan \
  --name datascientist-arena \
  --runtime "PYTHON:3.10"

az webapp config appsettings set \
  --resource-group myResourceGroup \
  --name datascientist-arena \
  --settings \
    DATABASE_URL=postgresql://... \
    DEBUG=false
```

**Frontend:**
```bash
npm run build
az storage blob upload-batch \
  --source dist \
  --destination '$web' \
  --account-name yourstorageaccount
```

---

## Database Setup

### PostgreSQL (Production)

```bash
# Create database
createdb arena

# Create user
createuser arena_user
psql -c "ALTER USER arena_user WITH PASSWORD 'secure_password';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE arena TO arena_user;"

# Initialize schema
alembic upgrade head
```

### Run Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Add users table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## Environment Configuration

### Backend (.env)
```env
# Database
DATABASE_URL=postgresql://user:password@localhost/arena

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false

# CORS
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Security
SECRET_KEY=your-super-secret-key-change-this
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Email (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Ollama (for LLM)
OLLAMA_API_BASE=http://localhost:11434

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/arena/app.log
```

### Frontend (.env)
```env
VITE_API_URL=https://api.yourdomain.com
VITE_ENVIRONMENT=production
VITE_LOG_LEVEL=info
```

---

## Monitoring & Logging

### Backend Logging
```python
import logging

logger = logging.getLogger(__name__)
logger.info("Event occurred")
logger.error("Error happened", exc_info=True)
```

### Application Performance Monitoring (APM)

**Using Sentry:**
```bash
pip install sentry-sdk

# In main.py
import sentry_sdk
sentry_sdk.init(
    "https://your-sentry-key@sentry.io/project-id",
    traces_sample_rate=0.1
)
```

**Using Datadog:**
```bash
pip install datadog

# In main.py
from datadog import initialize, statsd

options = {
    'statsd_host': '127.0.0.1',
    'statsd_port': 8125
}
initialize(**options)
```

### Health Checks

**Backend:**
```bash
curl http://localhost:8000/health
```

**Docker:**
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

---

## Security Hardening

### CORS Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)
```

### Rate Limiting
```bash
pip install slowapi

# In main.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/api/v1/datasets")
@limiter.limit("100/minute")
async def list_datasets(request: Request):
    ...
```

### HTTPS/SSL
```bash
# Generate SSL certificates
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Uvicorn with SSL
uvicorn app.main:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem
```

### API Key Authentication
```python
from fastapi import Header, HTTPException

async def get_api_key(x_token: str = Header(...)):
    if x_token != "secret-api-key":
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_token
```

---

## Performance Optimization

### Frontend
```bash
# Production build
npm run build

# Analyze bundle
npm run build -- --analyze

# Optimize images
npm install --save-dev @rollup/plugin-image
```

### Backend
```python
# Enable response caching
from fastapi_cache2 import FastAPICache2

@cached(expire=300)
@app.get("/api/v1/datasets")
async def list_datasets():
    ...

# Use async queries
from sqlalchemy.ext.asyncio import AsyncSession

async def get_datasets(db: AsyncSession):
    result = await db.execute(select(Dataset))
    ...
```

### Database
```sql
-- Add indexes
CREATE INDEX idx_dataset_created_at ON datasets(created_at DESC);
CREATE INDEX idx_experiment_status ON experiments(status);

-- Query optimization
EXPLAIN ANALYZE SELECT * FROM datasets WHERE created_at > NOW() - INTERVAL '30 days';
```

---

## Backup & Recovery

### Database Backup
```bash
# PostgreSQL backup
pg_dump arena > backup_$(date +%Y%m%d).sql

# Automated daily backup
0 2 * * * pg_dump arena | gzip > /backups/arena_$(date +\%Y\%m\%d).sql.gz

# Restore
psql arena < backup_20241020.sql
```

### File Uploads Backup
```bash
# Backup uploads directory
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz uploads/

# Restore
tar -xzf uploads_backup_20241020.tar.gz
```

### S3 Backup (AWS)
```bash
# Enable versioning
aws s3api put-bucket-versioning \
  --bucket your-bucket \
  --versioning-configuration Status=Enabled

# Enable Cross-Region Replication
aws s3api put-bucket-replication \
  --bucket your-bucket \
  --replication-configuration file://replication.json
```

---

## Rollback Procedure

```bash
# If deployment fails
docker-compose down
docker-compose up --force-recreate

# Database rollback
alembic downgrade -1

# Git rollback
git revert <commit-hash>
git push origin main
```

---

## Scaling Strategies

### Horizontal Scaling
- Use load balancer (nginx, HAProxy)
- Containerize application
- Use Kubernetes for orchestration
- Scale database with read replicas

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize code & queries
- Cache frequently accessed data

### Database Scaling
```bash
# Connection pooling
pip install psycopg2-pool

# Read replicas (AWS RDS)
aws rds create-db-instance-read-replica \
  --db-instance-identifier arena-replica \
  --source-db-instance-identifier arena
```

---

## Maintenance Tasks

### Daily
- [ ] Monitor error logs
- [ ] Check system resources
- [ ] Verify backups

### Weekly
- [ ] Review performance metrics
- [ ] Update dependencies
- [ ] Check security alerts

### Monthly
- [ ] Database optimization (VACUUM, ANALYZE)
- [ ] Archive old logs
- [ ] Performance review
- [ ] Security audit

---

## Support & Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Check connection string
DATABASE_URL=postgresql://user:password@host:port/dbname

# Test connection
psql postgresql://user:password@host:port/dbname
```

**Port Already in Use**
```bash
# Find process
lsof -i :8000
# Kill process
kill -9 <PID>
```

**Out of Memory**
```bash
# Increase server RAM or use memory-efficient techniques
# Enable swap
fallocate -l 4G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
```

---

## Runbooks

### Emergency Shutdown
```bash
docker-compose down
# Notify stakeholders
# Document reason
```

### Data Loss Recovery
```bash
# Restore from backup
psql arena < latest_backup.sql
# Verify data integrity
SELECT COUNT(*) FROM datasets;
```

### DDoS Mitigation
- Enable CloudFlare/AWS Shield
- Implement rate limiting
- Block suspicious IPs
- Scale resources

---

**Last Updated**: October 20, 2024  
**Deployment Status**: Ready for Production
**Next Review**: November 2024
