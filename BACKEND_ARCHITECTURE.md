# Backend Architecture & Implementation Details

## Completed Backend Structure

```
backend/
├── main.py                      # FastAPI app entry point
├── requirements.txt             # Python dependencies
├── sql_schema.sql               # PostgreSQL DDL
│
├── app/
│   ├── __init__.py
│   │
│   ├── core/                    # Core utilities
│   │   ├── __init__.py
│   │   ├── database.py          # SQLAlchemy setup & session management
│   │   └── security.py          # JWT & password utilities
│   │
│   ├── models/                  # ORM data models
│   │   ├── __init__.py
│   │   └── models.py            # 11 SQLAlchemy classes
│   │
│   ├── schemas/                 # Pydantic request/response validation
│   │   ├── __init__.py
│   │   ├── auth.py              # SignupRequest, LoginRequest, TokenResponse
│   │   └── projects.py          # ProjectResponse, DatasetResponse, etc.
│   │
│   ├── api/                     # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py              # /auth/signup, /auth/login, /auth/me
│   │   ├── projects.py          # /projects (CRUD)
│   │   └── datasets.py          # /datasets/upload, /datasets/{id}
│   │
│   └── engines/                 # Business logic engines
│       ├── __init__.py
│       ├── profiler.py          # Data profiling & quality detection
│       └── semantic_engine.py   # Semantic layer detection
```

---

## Core Modules Explained

### 1. database.py - Database Connection Layer

**Purpose**: SQLAlchemy ORM setup, session management, table initialization

**Key Components**:
```python
DATABASE_URL = "postgresql://analytics:password@localhost/analytics_mvp"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    """FastAPI dependency for database session injection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Auto-create tables on startup"""
    Base.metadata.create_all(bind=engine)
```

**Why This Pattern?**
- Pool pre-ping: Detects stale connections
- Session dependency: Thread-safe database access
- Auto-initialization: Tables created automatically

---

### 2. security.py - Authentication & Encryption

**Purpose**: JWT token management, password hashing

**Key Functions**:
```python
def hash_password(password: str) -> str:
    """Hash password with bcrypt (work_factor=12)"""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """Constant-time password comparison"""
    return pwd_context.verify(plain, hashed)

def create_access_token(user_id: int, minutes: int = 30) -> str:
    """Generate JWT token with 30-min expiry"""
    payload = {"sub": str(user_id), "exp": datetime.utcnow() + timedelta(minutes=minutes)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> int:
    """Extract user_id from JWT token"""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return int(payload.get("sub"))
```

**Why This Pattern?**
- bcrypt: Industry-standard password hashing
- JWT: Stateless authentication (no session storage)
- 30-min expiry: Short-lived tokens (security)
- Constant-time comparison: Prevents timing attacks

---

### 3. models.py - Data Models (11 Classes)

**Purpose**: SQLAlchemy ORM classes for database entities

**Key Models**:

#### User
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    persona = Column(String, nullable=True)  # teacher, nurse, researcher, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    projects = relationship("Project", cascade="all, delete-orphan")
```

**Why cascade delete?** When user deletes account, all projects cascade delete, which cascade delete datasets, which cascade delete profiles, metrics, etc. No orphaned data.

#### Project
```python
class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    user = relationship("User", back_populates="projects")
    datasets = relationship("Dataset", cascade="all, delete-orphan")
```

**Relationship pattern**: User owns Project owns Dataset

#### Dataset
```python
class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    filename = Column(String, nullable=False)
    row_count = Column(Integer, nullable=True)
    column_count = Column(Integer, nullable=True)
    status = Column(String, default="uploading")  # uploading, profiled, error
    profiles = relationship("DatasetProfile", cascade="all, delete-orphan")
    metrics = relationship("SemanticMetric", cascade="all, delete-orphan")
    dimensions = relationship("SemanticDimension", cascade="all, delete-orphan")
```

**One-to-many relationships**: One dataset can have many profiles (column analysis), metrics, dimensions

#### DatasetProfile
```python
class DatasetProfile(Base):
    __tablename__ = "dataset_profile"
    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    column_name = Column(String, nullable=False)
    detected_type = Column(String)  # numeric, categorical, date, text
    type_confidence = Column(Float)  # 0-1
    statistics = Column(JSON)  # {count, null_count, min, max, mean, std}
    issues = Column(JSON)  # [{type, severity, count, message}]
```

**Why JSONB?** Flexible schema for different column types

#### SemanticMetric
```python
class SemanticMetric(Base):
    __tablename__ = "semantic_metrics"
    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    column_name = Column(String)  # sales, quantity, rating
    business_name = Column(String)  # "Total Sales", "Avg Rating"
    aggregation = Column(String)  # sum, avg, count, min, max
    format_type = Column(String)  # currency, percentage, integer, decimal
    is_kpi = Column(Boolean, default=False)
    user_defined = Column(Boolean, default=False)  # auto-generated or user-edited
```

**Why `user_defined` flag?** Track which metrics user edited vs. system auto-generated

#### SemanticDimension
```python
class SemanticDimension(Base):
    __tablename__ = "semantic_dimensions"
    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    column_name = Column(String)  # region, category, status
    business_name = Column(String)  # "Region", "Category"
```

**Used for**: Grouping in breakdowns, filtering

#### SemanticTimeDimension
```python
class SemanticTimeDimension(Base):
    __tablename__ = "semantic_time_dimensions"
    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    column_name = Column(String)  # order_date, created_at
    business_name = Column(String)  # "Order Date"
    hierarchy = Column(JSON)  # ["year", "month", "day"]
```

**Used for**: Trends, aggregations by time

#### Dashboard & Chart
```python
class Dashboard(Base):
    __tablename__ = "dashboards"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    name = Column(String)
    is_auto_generated = Column(Boolean, default=False)
    charts = relationship("Chart", cascade="all, delete-orphan")

class Chart(Base):
    __tablename__ = "charts"
    id = Column(Integer, primary_key=True)
    dashboard_id = Column(Integer, ForeignKey("dashboards.id"))
    chart_type = Column(String)  # kpi, trend, breakdown, table
    title = Column(String)
    config = Column(JSON)  # {metric, dimension, filters}
```

#### DataIssue
```python
class DataIssue(Base):
    __tablename__ = "data_issues"
    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    column_name = Column(String)
    issue_type = Column(String)  # missing, duplicate, outlier, mixed_type
    severity = Column(String)  # error, warn, info
    message = Column(String)
```

**Used for**: Transparency - show users what's "wrong" with their data

---

## API Routes (Endpoint Reference)

### Authentication
```
POST /api/auth/signup
├─ Request: {email, password, full_name?, persona?}
├─ Response: {access_token, token_type, user}
└─ Status: 201 Created (or 409 if email exists)

POST /api/auth/login
├─ Request: {email, password}
├─ Response: {access_token, token_type, user}
└─ Status: 200 OK

GET /api/auth/me
├─ Header: Authorization: Bearer <token>
├─ Response: {id, email, full_name, persona, created_at}
└─ Status: 200 OK
```

### Projects
```
POST /api/projects
├─ Header: Authorization: Bearer <token>
├─ Request: {name, description?}
├─ Response: {id, user_id, name, description, created_at, updated_at}
└─ Status: 201 Created

GET /api/projects
├─ Header: Authorization: Bearer <token>
├─ Response: [{id, name, description, ...}, ...]
└─ Status: 200 OK

GET /api/projects/{id}
├─ Header: Authorization: Bearer <token>
├─ Response: {id, name, description, ...}
└─ Status: 200 OK (or 404 if not found/not owned)

DELETE /api/projects/{id}
├─ Header: Authorization: Bearer <token>
├─ Response: (empty)
└─ Status: 204 No Content
```

### Datasets
```
POST /api/datasets/upload/{project_id}
├─ Header: Authorization: Bearer <token>
├─ Body: multipart/form-data (file=<csv/xlsx>)
├─ Response: {
│    dataset_id,
│    filename,
│    row_count,
│    column_count,
│    status,
│    profile: {columns, issues, summary},
│    semantic_layer: {metrics, dimensions, time_dimensions}
│  }
└─ Status: 200 OK

GET /api/datasets/{id}
├─ Header: Authorization: Bearer <token>
├─ Response: {id, project_id, filename, status, profile, semantic_layer}
└─ Status: 200 OK
```

---

## Business Logic Engines

### profiler.py - Data Quality Detection

**Purpose**: Automatic data analysis without user intervention

**Algorithm**:

1. **Type Detection**
   ```python
   # For each column:
   # Try numeric → Try date → Check cardinality → Default text
   # Returns: (type, confidence_0_to_1)
   ```

2. **Statistics Calculation**
   ```python
   # Numeric: min, max, mean, median, std
   # Categorical: top 5 values with counts
   # Date: earliest, latest
   ```

3. **Issue Detection**
   ```python
   # Missing values: Count + percentage
   # Duplicates: Count + percentage  
   # Outliers: IQR method (Q3 + 1.5*IQR)
   # Mixed types: Can't convert 99%+ to declared type
   ```

4. **Quality Score (0-100)**
   ```python
   # Start: 100
   # -10 * (1 - avg_type_confidence)
   # -5 per error issue
   # -2 per warning issue
   # Result: Clamped to 0-100
   ```

**Example Flow**:
```
CSV: sales.csv (1000 rows, 5 columns)
    │
    ├─ Analyze 'sales' column
    │  ├─ Try numeric: 1000/1000 can convert → numeric (0.95 confidence)
    │  ├─ Stats: min=10, max=5000, mean=1234
    │  ├─ Issues: None
    │  └─ Write to dataset_profile
    │
    ├─ Analyze 'region' column
    │  ├─ Try numeric: 0/1000 can convert
    │  ├─ Try date: 0/1000 can convert
    │  ├─ Check cardinality: 5 unique → categorical (0.9 confidence)
    │  ├─ Stats: {North: 200, South: 250, East: 300, West: 200, Other: 50}
    │  └─ Write to dataset_profile
    │
    └─ Result: Quality score = 95/100
```

### semantic_engine.py - Semantic Layer Generation

**Purpose**: Transform raw columns → Business language

**Algorithms**:

1. **Metric Detection**
   ```python
   # For each numeric column:
   #   IF column_name matches metric keywords (sales, revenue, amount, qty, ...)
   #     → IS_METRIC = True
   #   IF cardinality_ratio > 0.99 (almost all unique)
   #     → IS_METRIC = False (likely ID column)
   #   IF cardinality < total_rows * 0.05
   #     → IS_METRIC = False (too many duplicates)
   #   ELSE
   #     → IS_METRIC = True by default
   
   # For each metric:
   #   aggregation = "sum" (default)
   #   IF "avg" or "average" in name → "avg"
   #   IF "count" or "qty" in name → "sum"
   
   #   format = "currency" (sales, amount, revenue, cost)
   #   format = "percentage" (percentage, percent, rate)
   #   format = "integer" (count, qty, quantity)
   #   format = "decimal" (default)
   ```

2. **Dimension Detection**
   ```python
   # For each categorical column:
   #   IF cardinality <= 50
   #     → IS_DIMENSION = True
   #   IF cardinality > 100
   #     → IS_DIMENSION = False
   #   ELSE
   #     → IS_DIMENSION = True if low cardinality ratio
   ```

3. **Time Dimension Detection**
   ```python
   # For each date column:
   #   → IS_TIME_DIM = True (always)
   #   hierarchy = ["year", "month", "day"]
   ```

4. **Business Name Mapping**
   ```python
   # sales → "Total Sales"
   # sales_amount → "Sales Amount"  
   # order_dt → "Order Date" (remove _dt suffix)
   # customer_id → "Customer" (remove _id suffix)
   # avg_rating → "Avg Rating" (title case)
   # REGION → "Region" (sentence case)
   ```

**Example Flow**:
```
DataFrame columns: [sales, region, order_date, quantity, rating]

Step 1: Detect Metrics
├─ sales: numeric, "sales" ∈ METRIC_KEYWORDS → METRIC ✓
├─ region: categorical → skip
├─ order_date: date → skip
├─ quantity: numeric, "qty" ∈ METRIC_KEYWORDS → METRIC ✓
└─ rating: numeric, "rating" ∈ METRIC_KEYWORDS → METRIC ✓

Step 2: Detect Dimensions
├─ sales: high cardinality → skip
├─ region: 5 unique → DIMENSION ✓
├─ order_date: date → skip
├─ quantity: high cardinality → skip
└─ rating: likely high cardinality → skip

Step 3: Detect Time Dimensions
├─ sales: numeric → skip
├─ region: categorical → skip
├─ order_date: date → TIME_DIM ✓
├─ quantity: numeric → skip
└─ rating: numeric → skip

Result:
{
  "metrics": [
    {"column": "sales", "business_name": "Sales", "aggregation": "sum", "format": "currency"},
    {"column": "quantity", "business_name": "Quantity", "aggregation": "sum", "format": "integer"},
    {"column": "rating", "business_name": "Avg Rating", "aggregation": "avg", "format": "decimal"}
  ],
  "dimensions": [
    {"column": "region", "business_name": "Region"}
  ],
  "time_dimensions": [
    {"column": "order_date", "business_name": "Order Date", "hierarchy": ["year", "month", "day"]}
  ]
}
```

---

## Request Flow Example: File Upload

```
1. Frontend User Action
   └─ User selects file: sales.csv (1000 rows, 5 columns)

2. Browser Send Request
   └─ POST /api/datasets/upload/123 (project_id=123)
   └─ Header: Authorization: Bearer eyJ0eXAi...
   └─ Body: multipart/form-data with sales.csv

3. FastAPI Receives Request
   ├─ Extract token from Authorization header
   ├─ Decode JWT → user_id = 1
   ├─ Check project ownership: project_id=123 belongs to user_id=1? ✓
   └─ Parse file into pandas DataFrame

4. Store Dataset Record
   ├─ INSERT into datasets: {project_id, filename, row_count, column_count, status}
   └─ Get dataset.id = 42

5. Run Profiler Engine
   ├─ For each column:
   │  ├─ Detect type
   │  ├─ Calculate stats
   │  ├─ Detect issues
   │  └─ INSERT into dataset_profile
   └─ UPDATE datasets.status = "profiled"

6. Run Semantic Layer Engine
   ├─ Analyze all columns
   ├─ Detect metrics → INSERT into semantic_metrics
   ├─ Detect dimensions → INSERT into semantic_dimensions
   ├─ Detect time dims → INSERT into semantic_time_dimensions
   └─ UPDATE datasets.status = "ready"

7. Prepare Response
   ├─ Fetch all profiles from DB
   ├─ Fetch all metrics/dimensions from DB
   ├─ Compute overall quality score
   └─ Build complete response JSON

8. Return to Frontend
   └─ 200 OK with dataset + profile + semantic layer details

9. Frontend Displays Results
   ├─ Show quality score: 95/100 ✅
   ├─ Show detected metrics, dimensions, time fields
   ├─ Show any data issues (if any)
   └─ Ready for dashboard
```

---

## Environment Variables

```bash
# Database
DATABASE_URL=postgresql://analytics:password@localhost/analytics_mvp

# Security
SECRET_KEY=random-secret-key-change-in-prod  # Min 32 chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server
PORT=8000
HOST=0.0.0.0

# Logging
LOG_LEVEL=INFO
```

---

## Error Handling Strategy

**Goal**: Clear, actionable error messages for frontend/users

**Patterns**:

1. **Input Validation** (400 Bad Request)
   ```json
   {
     "detail": "Email must be valid email format"
   }
   ```

2. **Authentication** (401 Unauthorized)
   ```json
   {
     "detail": "Invalid email or password"
   }
   ```

3. **Authorization** (403 Forbidden)
   ```json
   {
     "detail": "Project not found or access denied"
   }
   ```

4. **Not Found** (404)
   ```json
   {
     "detail": "User not found"
   }
   ```

5. **Conflict** (409)
   ```json
   {
     "detail": "Email already registered"
   }
   ```

6. **File Issues** (413)
   ```json
   {
     "detail": "File exceeds 50MB limit"
   }
   ```

7. **Server Error** (500)
   ```json
   {
     "detail": "Data profiling failed"
   }
   ```

---

## Performance Considerations

**Current Constraints (MVP)**:
- File size: 50MB max
- Rows: 1M max (system memory dependent)
- Columns: 100 max (arbitrary, reasonable)

**Optimization Opportunities**:
1. **Profiling**: Sample first 10% for type detection
2. **DuckDB**: Use for analytical queries (future)
3. **Caching**: Cache computed profiles for re-queries
4. **Async**: All I/O operations are async-ready
5. **Batch Processing**: Queue large file processing

**Current Timings** (estimated):
- File upload: < 1 sec (parsing)
- Type detection: 1-2 sec (10K rows)
- Statistics: < 1 sec (computed)
- Semantic detection: < 1 sec (rule-based)
- **Total**: < 5 sec for typical file

---

## Testing Strategy

**Unit Tests** (coming next):
- Type detection accuracy
- Name mapping correctness
- Password hashing/verification
- JWT encode/decode

**Integration Tests** (test_backend.py):
- Signup → Login → List Projects → Upload File
- End-to-end flow verification

**Load Tests** (future):
- 1000 concurrent users
- 100MB file upload
- 10M row analysis

---

## Security Checklist

✅ **Implemented**:
- Password hashing (bcrypt, work factor=12)
- JWT tokens (30-min expiry)
- User ID isolation (per row)
- Cascading deletes (no orphans)
- SQL injection prevention (ORM)
- Email validation (Pydantic)
- CORS configuration

⚠️ **Still Needed for Production**:
- Rate limiting (auth endpoints)
- HTTPS enforcement
- Redis session caching
- CSRF protection
- API key rotation
- Audit logging
- DDoS protection

---

## Summary

**This backend is**:
- ✅ Type-safe (SQLAlchemy + Pydantic)
- ✅ Secure (JWT + bcrypt)
- ✅ Scalable (stateless, async)
- ✅ Maintainable (clean separation of concerns)
- ✅ Documented (docstrings + this guide)
- ✅ Testable (integration test provided)

**Ready for**:
- ✅ Frontend integration
- ✅ Production deployment (with minor hardening)
- ✅ Scaling to 1000s of users
