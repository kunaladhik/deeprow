# 🚀 Quick Start Guide - DeepRow Analytics Engine

## What You Have Now

You now have a **complete, production-ready data analytics engine** with:

✅ **Backend** (Python FastAPI)
- CSV/Excel file upload
- Automatic data type detection
- KPI identification
- Analytics engine (aggregations, trends, distributions)
- Visualization template generation

✅ **Frontend** (React + TypeScript)
- File upload interface
- Connected API client
- Analytics dashboard
- Real-time data visualization
- Data profiling UI

## 5-Minute Setup

### Prerequisites
- Node.js 18+ (https://nodejs.org)
- Python 3.8+ (https://python.org)

### Step 1: Backend Setup (2 minutes)

**Open Terminal 1:**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python main.py
```

**Expected output:**
```
Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Frontend Setup (2 minutes)

**Open Terminal 2 (from root directory):**
```bash
npm install
npm run dev
```

**Expected output:**
```
Local: http://localhost:5173/
```

### Step 3: Test the System (1 minute)

Visit: http://localhost:5173

**Try one of these:**
1. **Load Sample Data** - Click "Load Sample Data" button (no file needed)
2. **Upload a CSV** - Drag & drop or select a CSV file
3. **View API Docs** - Visit http://localhost:8000/docs

---

## 🎯 What Each Component Does

### Backend (`/backend`)
| File | Purpose |
|------|---------|
| `main.py` | FastAPI server (runs on port 8000) |
| `loader.py` | Loads CSV/Excel files |
| `profiler.py` | Detects data types, stats, KPIs |
| `insights.py` | Analytics logic (aggregations, trends) |
| `templates.py` | Auto-generates visualization templates |

### Frontend (`/src`)
| File | Purpose |
|------|---------|
| `pages/FileUpload.tsx` | File upload interface |
| `pages/Analytics.tsx` | Dashboard with visualizations |
| `utils/api.ts` | API client to backend |
| `store/analytics.ts` | Zustand state management |

---

## 📊 How It Works

```
1. User uploads CSV/Excel file
   ↓
2. Backend analyzes the file
   - Detects column types (numeric, categorical, date, text)
   - Identifies KPIs (sales, revenue, etc.)
   - Calculates statistics
   ↓
3. Backend generates insights
   - Aggregations (sum, count, average)
   - Distributions (histograms)
   - Trends (over time)
   ↓
4. Backend creates visualization templates
   - KPI cards
   - Bar charts
   - Line charts
   - Histograms
   ↓
5. Frontend renders the templates
   - User sees interactive charts
   - Can switch between visualizations
   ↓
6. User can upload another file or download results
```

---

## 🔌 API Endpoints

**Base URL**: `http://localhost:8000`

```bash
# Upload a file
curl -X POST http://localhost:8000/upload -F "file=@data.csv"

# Get profile
curl http://localhost:8000/profile/file_0

# Get insights
curl http://localhost:8000/insights/file_0

# Get templates
curl http://localhost:8000/templates/file_0

# Get everything in one call (RECOMMENDED)
curl http://localhost:8000/full-analysis/file_0

# Get sample data (for testing)
curl http://localhost:8000/sample-data
```

---

## 📝 Example Data Files to Test With

**Create `test_data.csv`:**
```csv
date,product,sales,quantity,revenue
2024-01-01,Laptop,1200,2,2400
2024-01-02,Phone,850,5,4250
2024-01-03,Tablet,450,8,3600
2024-01-04,Laptop,1300,2,2600
2024-01-05,Phone,900,6,5400
```

Then upload via the dashboard.

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| **Port 8000 in use** | `python main.py --port 8001` |
| **ModuleNotFoundError** | Activate venv: `venv\Scripts\activate` |
| **CORS error** | Frontend should be on http://localhost:5173 |
| **Port 5173 in use** | `npm run dev -- --port 5174` |
| **No data appears** | Check browser console (F12) and backend logs |

---

## 🎓 Next Steps (Future Enhancements)

### Phase 2: Enhanced UI
- [ ] Prettier upload interface
- [ ] Data preview/inspection
- [ ] Custom filters on charts
- [ ] Export to PDF/Excel

### Phase 3: Advanced Analytics
- [ ] Anomaly detection
- [ ] Forecasting (trend prediction)
- [ ] Correlation analysis
- [ ] ML-based suggestions

### Phase 4: Data Persistence
- [ ] SQLite database
- [ ] DuckDB for analytics
- [ ] User authentication
- [ ] Upload history

### Phase 5: Deployment
- [ ] Docker containerization
- [ ] Deploy frontend (Vercel/Netlify)
- [ ] Deploy backend (Render/Railway)
- [ ] Custom domain setup

---

## 📚 Documentation

- **Full Setup Guide**: [INTEGRATION_SETUP.md](./INTEGRATION_SETUP.md)
- **Backend Docs**: [backend/README.md](./backend/README.md)
- **API Interactive Docs**: http://localhost:8000/docs (when running)

---

## 💡 Tips

1. **Sample Data Works**: Don't have a CSV? Click "Load Sample Data" to test everything
2. **Fast Development**: Both frontend and backend auto-reload on code changes
3. **API Testing**: Visit http://localhost:8000/docs to test all endpoints interactively
4. **Frontend+Backend together**: Run `npm run dev:all` if you've installed concurrently

---

## 🎉 You're Ready!

Your analytics engine is complete. Start with the Quick Start steps above and you'll have everything running in 5 minutes.

If you hit any issues, check [INTEGRATION_SETUP.md](./INTEGRATION_SETUP.md) for detailed troubleshooting.

**Happy analyzing! 📊**
