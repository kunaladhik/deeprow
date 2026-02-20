# DeepRow Analytics Engine - Backend

This is the Python FastAPI backend for the **Self-Service Data Analytics Engine**.

## 🚀 Quick Start

### 1. Install Python (if not already installed)
Download from https://www.python.org/downloads/ (3.8+)

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Server
```bash
python main.py
```

Server will start at: **http://localhost:8000**

## 📚 API Documentation

Once running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **API Schema**: http://localhost:8000/openapi.json

## 🔌 API Endpoints

### Upload Data
```
POST /upload
- Upload CSV or Excel file
- Returns: file_id, profile, column analysis
```

### Get Profile
```
GET /profile/{file_id}
- Column types, statistics, KPI detection
```

### Get Insights
```
GET /insights/{file_id}
- Aggregations, distributions, trends
```

### Get Templates
```
GET /templates/{file_id}
- Auto-generated visualization templates
```

### Full Analysis (All-in-One)
```
GET /full-analysis/{file_id}
- Profile + Insights + Templates in one call
```

### Sample Data
```
GET /sample-data
- Demo data for testing
```

## 📁 Project Structure

```
backend/
├── main.py                 # FastAPI app
├── requirements.txt        # Dependencies
└── analytics/
    ├── loader.py          # CSV/Excel loading
    ├── profiler.py        # Type detection
    ├── insights.py        # Analytics engine
    └── templates.py       # Visualization templates
```

## 🧠 Core Features

### Data Loader
- Automatically loads CSV and Excel files
- Handles various formats and encodings

### Data Profiler
- Detects column types: numeric, date, categorical, text
- Calculates statistics: min, max, mean, median, std
- Identifies KPIs (sales, revenue, quantity, etc.)
- Detects date columns automatically

### Insights Engine
- **Aggregations**: Sum, count, average, min, max
- **Distributions**: Histograms for numeric data
- **Trends**: Time-series analysis if date column exists
- **Comparisons**: Group-by analysis

### Template Generator
- KPI cards
- Bar charts
- Line charts
- Pie charts
- Histograms
- Auto-recommends charts based on data

## 🔄 How It Works

1. **Upload** → File is loaded and profiled
2. **Analyze** → Data types are detected, KPIs identified
3. **Generate Insights** → Aggregations, trends, distributions calculated
4. **Create Templates** → Visualization templates auto-generated
5. **Render** → Frontend renders the templates

## 📦 Dependencies

- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **pandas** - Data processing
- **numpy** - Numerical computing
- **openpyxl** - Excel support
- **python-dateutil** - Date handling
- **scikit-learn** - Machine learning (future)

## 🛠️ Development

### Adding New Analytics
Edit `analytics/insights.py` to add new analytics functions

### Adding New Chart Types
Edit `analytics/templates.py` to add new visualization templates

### Hot Reload
Server automatically reloads when you save files (development mode)

## 🚀 Production Deployment

When ready to deploy:

```bash
# Build optimized version
uvicorn main:app --host 0.0.0.0 --port 8000

# With Gunicorn (recommended)
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📝 Example Request

```bash
# Upload a file
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -F "file=@data.csv"

# Get full analysis
curl "http://localhost:8000/full-analysis/file_0"
```

## 🐛 Troubleshooting

**Port 8000 already in use?**
```bash
# Use different port
uvicorn main:app --port 8001
```

**Module not found?**
```bash
# Ensure you're in venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

**CORS errors?**
Frontend should be on `http://localhost:5173` (Vite default)

## 📞 Frontend Integration

Frontend connects to backend at `http://localhost:8000`

Example fetch:
```javascript
const response = await fetch('http://localhost:8000/upload', {
  method: 'POST',
  body: formData
});
```

---

**Next Steps**: Connect the frontend to this backend API!
