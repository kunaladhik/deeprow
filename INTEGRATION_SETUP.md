# DeepRow Analytics Engine - Complete Setup Guide

## 🎯 What You're Building

A **Self-Service Data Analytics Engine** - like a mini Power BI/Tableau for the web:
- Upload CSV/Excel files
- Automatically detect data types and KPIs
- Generate insights (aggregations, trends, distributions)
- Create interactive visualizations
- No coding required for end-users

## 📋 System Requirements

- **Node.js**: 18+ (for frontend)
- **Python**: 3.8+ (for backend)
- **RAM**: 2GB minimum
- **Disk**: 1GB free space

## 🚀 SETUP INSTRUCTIONS

### STEP 1: Backend Setup (Python)

#### 1.1 Check Python Installation
```bash
python --version
```
Should show Python 3.8 or higher.

If not installed, download from: https://www.python.org/downloads/

#### 1.2 Create Virtual Environment

**Windows (PowerShell)**:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD)**:
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 1.3 Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### 1.4 Run Backend
```bash
python main.py
```

**Success indicator**: You should see:
```
Uvicorn running on http://0.0.0.0:8000
```

Visit http://localhost:8000/docs to see API docs.

---

### STEP 2: Frontend Setup (Node.js)

#### 2.1 Check Node Installation
```bash
node --version
npm --version
```

Should show Node 18+ and npm 9+.

If not installed, download from: https://nodejs.org/

#### 2.2 Install Frontend Dependencies
```bash
# Back in root directory (not backend/)
npm install
```

#### 2.3 Create Environment File
Already created: `.env.local`

Verify it contains:
```
VITE_API_URL=http://localhost:8000
```

#### 2.4 Run Frontend
```bash
npm run dev
```

**Success indicator**: You should see:
```
VITE v5.0.0 ready in 123 ms
Local: http://localhost:5173/
```

---

### STEP 3: Run Both Together (Recommended)

Once both are working separately, you can run them together:

#### Option A: Separate Terminals
Terminal 1:
```bash
npm run dev
```

Terminal 2:
```bash
cd backend
python main.py
```

#### Option B: Single Command (requires concurrently)
```bash
npm install -g concurrently
npm run dev:all
```

---

## ✅ Testing the Full Stack

### Test 1: Backend Working
Visit: http://localhost:8000/docs

API documentation should appear.

### Test 2: Frontend Working
Visit: http://localhost:5173

Dashboard should load.

### Test 3: Full Integration
1. Go to dashboard upload page
2. Upload a CSV file
3. System should analyze and show insights

### Test 4: Sample Data (No Upload Needed)
The `/sample-data` endpoint returns demo data automatically.

---

## 🔥 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Your Computer                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐         ┌──────────────────────────┐ │
│  │  React Frontend  │         │  Python FastAPI Backend  │ │
│  │ (Port 5173)      │────────▶│  (Port 8000)             │ │
│  │                  │         │                          │ │
│  │ - UI Components  │         │ - Data Loader            │ │
│  │ - Visualizations │         │ - Data Profiler          │ │
│  │ - File Upload    │         │ - Analytics Engine       │ │
│  └──────────────────┘         │ - Template Generator     │ │
│                               └──────────────────────────┘ │
│                                          │                 │
│                                          ▼                 │
│                                  ┌─────────────────┐       │
│                                  │  Data Processing│       │
│                                  │                 │       │
│                                  │ • pandas        │       │
│                                  │ • numpy         │       │
│                                  │ • scikit-learn  │       │
│                                  └─────────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
DeepRow UI/
├── frontend/ (React + TypeScript)
│   ├── src/
│   │   ├── pages/      # Dashboard, Upload, Analytics views
│   │   ├── components/ # Reusable UI components
│   │   ├── store/      # Zustand state management
│   │   ├── utils/      # API client
│   │   └── styles/     # CSS files
│   └── package.json
│
├── backend/ (Python + FastAPI)
│   ├── main.py         # FastAPI server
│   ├── analytics/
│   │   ├── loader.py   # CSV/Excel loading
│   │   ├── profiler.py # Type detection
│   │   ├── insights.py # Analytics logic
│   │   └── templates.py # Visualization templates
│   ├── requirements.txt # Python dependencies
│   └── uploads/        # Temporary file storage
```

---

## 🔌 API Endpoints

All endpoints run at: `http://localhost:8000`

### 📤 Data Upload
```
POST /upload
Input: multipart/form-data with file
Returns: { file_id, profile, filename }
```

### 📊 Get Profile
```
GET /profile/{file_id}
Returns: Column types, statistics, KPIs
```

### 📈 Get Insights
```
GET /insights/{file_id}
Returns: Aggregations, distributions, trends
```

### 📱 Get Templates
```
GET /templates/{file_id}
Returns: Array of visualization templates
```

### 🎯 Full Analysis (Recommended)
```
GET /full-analysis/{file_id}
Returns: profile + insights + templates in one call
```

### 🎪 Sample Data
```
GET /sample-data
Returns: Demo analytics for testing (no upload needed)
```

---

## 🐛 Troubleshooting

### Issue: Port 8000 already in use
**Solution**: Kill existing processes or use different port
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### Issue: Python module not found
**Solution**: Ensure virtual environment is activated
```bash
# Activate it again
./venv/Scripts/activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### Issue: CORS error in frontend
**Solution**: Backend is already configured for CORS.
Make sure:
- Frontend runs on `http://localhost:5173`
- Backend runs on `http://localhost:8000`
- `.env.local` has `VITE_API_URL=http://localhost:8000`

### Issue: File upload fails
**Solution**: Check file format (CSV or XLSX) and size

### Issue: "Cannot find module 'main'"
**Solution**: Ensure you're running from root directory
```bash
pwd  # Check current directory
python main.py  # Run from backend/ folder
```

---

## 📚 Next Steps

### Phase 1: Core Features (You are here)
- ✅ Data upload and profiling
- ✅ Basic analytics engine
- ✅ Visualization templates
- ⬜ Frontend components

### Phase 2: Enhanced UI
- [ ] File upload component
- [ ] Real-time chart rendering
- [ ] Data preview/inspection
- [ ] Custom filters

### Phase 3: Advanced Analytics
- [ ] Anomaly detection
- [ ] Forecasting
- [ ] ML-based insights
- [ ] A/B testing

### Phase 4: Data Storage
- [ ] SQLite database
- [ ] DuckDB for analytics
- [ ] Data persistence
- [ ] Query optimization

### Phase 5: Deployment
- [ ] Docker setup
- [ ] Deploy frontend (Vercel/Netlify)
- [ ] Deploy backend (Render/Railway)
- [ ] SSL certificates

---

## 💡 Quick Commands Reference

```bash
# Backend
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py

# Frontend
npm install
npm run dev

# Both together
npm run dev:all

# Check services
curl http://localhost:8000  # Backend health
curl http://localhost:5173  # Frontend health
```

---

## 🎓 Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **React**: https://react.dev/
- **Pandas**: https://pandas.pydata.org/docs/
- **Chart.js**: https://www.chartjs.org/

---

## 💬 Support

If you encounter any issues:
1. Check the troubleshooting section
2. Check backend logs (terminal where backend runs)
3. Check browser console (Press F12)
4. Check network tab (Request/Response)

---

**Ready to build? Start with Step 1: Backend Setup!**
