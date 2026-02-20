## Backend Development Guide

### Current Status (Just Completed)

✅ **Database Layer**
- PostgreSQL schema with 10+ tables (users, projects, datasets, profiles, semantic models, etc.)
- SQLAlchemy ORM models for 11 data classes
- Database connection management with pooling

✅ **Authentication**
- JWT token generation/verification
- bcrypt password hashing
- Signup/Login/Me endpoints

✅ **Core Business Logic**
- Data profiling engine (type detection, statistics, issue detection)
- Semantic layer engine (auto-detect metrics, dimensions, time hierarchies)
- File upload with CSV/Excel parsing

✅ **API Routes**
- POST /api/auth/signup
- POST /api/auth/login
- GET /api/auth/me
- POST /api/projects
- GET /api/projects
- GET /api/projects/{id}
- DELETE /api/projects/{id}
- POST /api/datasets/upload/{id}
- GET /api/datasets/{id}

✅ **FastAPI Setup**
- CORS middleware configured
- Database initialization on startup
- All route imports configured

---

### Prerequisites

1. **Python 3.10+** installed
2. **PostgreSQL 12+** running locally
3. **Dependencies installed**: `pip install -r requirements.txt`

---

### Database Setup

#### 1. Create PostgreSQL Database

```bash
# Connect to PostgreSQL as admin
psql -U postgres

# Create database and user
CREATE DATABASE analytics_mvp;
CREATE USER analytics WITH PASSWORD 'password123';
ALTER ROLE analytics SET client_encoding TO 'utf8';
ALTER ROLE analytics SET default_transaction_isolation TO 'read committed';
ALTER ROLE analytics SET default_transaction_deferrable TO off;
ALTER ROLE analytics SET default_transaction_read_only TO off;
ALTER ROLE analytics SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE analytics_mvp TO analytics;

# Exit psql
\q
```

#### 2. Update Database Connection String

**File**: `backend/app/core/database.py`

Change line 12:
```python
DATABASE_URL = "postgresql://analytics:password123@localhost/analytics_mvp"
```

#### 3. Apply Schema

```bash
cd backend
psql -U analytics -d analytics_mvp -f app/sql_schema.sql
```

Or the app will auto-create tables on first startup (see backend/app/core/database.py `init_db()`)

---

### Environment Setup

Create `.env` file in `backend/` directory:

```
# Database
DATABASE_URL=postgresql://analytics:password123@localhost/analytics_mvp

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server
PORT=8000
HOST=0.0.0.0
```

---

### Running the Backend

```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server will start at: **http://localhost:8000**

API Docs available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

---

### Testing Authentication (with curl or Postman)

#### 1. Signup
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "securepassword123",
    "full_name": "Alice Johnson",
    "persona": "teacher"
  }'
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "alice@example.com",
    "full_name": "Alice Johnson",
    "persona": "teacher",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

#### 2. Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "securepassword123"
  }'
```

#### 3. Get Current User (requires token)
```bash
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

---

### Testing Project Management

#### 1. Create Project
```bash
curl -X POST http://localhost:8000/api/projects \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Q4 Sales Analysis",
    "description": "Quarterly sales performance review"
  }'
```

#### 2. List Projects
```bash
curl -X GET http://localhost:8000/api/projects \
  -H "Authorization: Bearer <token>"
```

#### 3. Delete Project
```bash
curl -X DELETE http://localhost:8000/api/projects/1 \
  -H "Authorization: Bearer <token>"
```

---

### Testing File Upload

#### 1. Create a sample CSV
```
sales,region,date,quantity
1200,North,2024-01-15,5
950,South,2024-01-16,3
1500,East,2024-01-17,7
```

#### 2. Upload File
```bash
curl -X POST http://localhost:8000/api/datasets/upload/1 \
  -H "Authorization: Bearer <token>" \
  -F "file=@sales_data.csv"
```

Response includes:
- Row/column counts
- Data quality profile
- Auto-detected metrics & dimensions
- Data issues (if any)

---

### Project Structure

```
backend/
├── main.py
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── database.py          # SQLAlchemy setup, session management
│   │   └── security.py          # JWT, password hashing
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py            # 11 ORM classes (User, Project, Dataset, etc.)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py              # SignupRequest, LoginRequest, TokenResponse
│   │   └── projects.py          # ProjectResponse, DatasetResponse, etc.
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py              # Signup, login, me endpoints
│   │   ├── projects.py          # Project CRUD endpoints
│   │   └── datasets.py          # File upload, dataset operations
│   └── engines/
│       ├── __init__.py
│       ├── profiler.py          # Auto-detect types, stats, issues
│       └── semantic_engine.py   # Auto-detect metrics, dimensions, time
└── sql_schema.sql               # PostgreSQL DDL (10+ tables)
```

---

### Key Architecture Decisions

1. **Semantic Layer First**: Raw columns → Business objects (metrics, dimensions, time)
2. **Trust Design**: Every metric traces to source column + cleaning rules applied
3. **Domain-Agnostic**: Works for education, healthcare, research, business
4. **Human-in-Loop**: No silent fixes; all data quality issues surfaced to user
5. **One Dataset Per Project (MVP)**: Simplifies initial experience

---

### Next Steps

1. **Frontend Development** (in `/src`)
   - Create login page
   - Project management UI
   - File upload interface
   - Dashboard builder

2. **Dashboard Generation**
   - Create default dashboard from semantic layer
   - Auto-select 4-5 best charts
   - Support for user customization

3. **Query Engine**
   - Convert chart selections → DuckDB SQL
   - Execute queries
   - Return results for visualization

4. **Data Transparency**
   - Show metric formulas
   - Show rows used in calculation
   - Show cleaning rules applied

---

### Common Issues & Fixes

**Issue**: ModuleNotFoundError: No module named 'app'
- **Fix**: Run from `backend/` directory: `cd backend && python -m uvicorn main:app --reload`

**Issue**: psycopg2.OperationalError: could not connect to PostgreSQL
- **Fix**: Check PostgreSQL is running: `pg_isready`
- **Fix**: Check connection string in database.py

**Issue**: JWT decode error
- **Fix**: Make sure SECRET_KEY is set (see .env section)
- **Fix**: Check token hasn't expired (30 minutes default)

---

### Database Schema Reference

**Users**
- id, email, password_hash, full_name, persona, created_at, updated_at

**Projects**
- id, user_id, name, description, created_at, updated_at

**Datasets**
- id, project_id, filename, file_size, row_count, column_count, status, error_message, created_at, updated_at

**DatasetProfile**
- id, dataset_id, column_name, detected_type, type_confidence, statistics (JSONB), issues (JSONB)

**SemanticMetric**
- id, dataset_id, column_name, business_name, aggregation, format_type, is_kpi, user_defined, created_at

**SemanticDimension**
- id, dataset_id, column_name, business_name, created_at

**SemanticTimeDimension**
- id, dataset_id, column_name, business_name, hierarchy (JSONB), created_at

**CleaningRule**
- id, dataset_id, rule_type, rule_config (JSONB), created_at

**Dashboard**
- id, project_id, name, is_auto_generated, created_at, updated_at

**Chart**
- id, dashboard_id, chart_type, title, config (JSONB), created_at, updated_at

**DataIssue**
- id, dataset_id, column_name, issue_type, severity, message, created_at

---

### Performance Notes

- Column profiling: O(n) scan of data
- Type detection: Pandas inference + regex validation
- Semantic detection: Rule-based, not AI (fast & transparent)
- File size limit: 50MB (MVP constraint)
- Row limit: 1M (theoretical, depends on system memory)

---

### Security Notes (MVP→Production)

⚠️ **Before deploying to production:**

1. Change SECRET_KEY to strong random value
2. Use environment variables for database credentials
3. Enable HTTPS
4. Implement rate limiting on auth endpoints
5. Add CSRF protection if using cookies
6. Validate file uploads more strictly
7. Add API key/OAuth for production

---

### Debugging

Enable logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check database connection:
```bash
psql -U analytics -d analytics_mvp -c "SELECT COUNT(*) FROM users;"
```

Test API online: Use Swagger UI at http://localhost:8000/docs

---

### Questions?

See docstrings in each file. Key design explained in:
- `backend/app/engines/semantic_engine.py` - How auto-detection works
- `backend/app/engines/profiler.py` - How data quality scoring works
- `backend/app/core/database.py` - How persistence layer works
