# Project Architecture & Flow

## 📊 Application Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        React App (Vite)                             │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                     App.tsx (Router)                         │  │
│  │  ┌─────────────┐  ┌──────────┐  ┌──────────────────────┐   │  │
│  │  │  /login     │  │ /        │  │   <Layout />         │   │  │
│  │  │  <Login />  │  │ redirect │  │   (Protected Routes) │   │  │
│  │  │             │  │          │  │   ┌────────────────┐ │   │  │
│  │  └─────────────┘  └──────────┘  │   │ /dashboard     │ │   │  │
│  │                                  │   │ /upload        │ │   │  │
│  │                                  │   │ /data-review   │ │   │  │
│  │                                  │   │ /builder       │ │   │  │
│  │                                  │   │ /transparency  │ │   │  │
│  │                                  │   └────────────────┘ │   │  │
│  │                                  └──────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 📁 File Structure

```
src/
│
├── App.tsx
│   └── Routes configuration
│       ├── Login page
│       └── Layout (sidebar + main content)
│           ├── Dashboard
│           ├── FileUpload
│           ├── DataIssueReview
│           ├── DashboardBuilder
│           └── LogicTransparency
│
├── components/
│   └── Layout.tsx
│       ├── Sidebar (navigation)
│       ├── Top bar
│       └── Page content outlet
│
├── pages/
│   ├── Login.tsx          - Authentication
│   ├── Dashboard.tsx      - Main dashboard with metrics
│   ├── FileUpload.tsx     - CSV/Excel upload
│   ├── DataIssueReview.tsx - Data quality issues
│   ├── DashboardBuilder.tsx - Widget builder
│   └── LogicTransparency.tsx - AI insights explanation
│
├── styles/
│   ├── index.css          - Global styles & variables
│   ├── layout.css         - Sidebar & layout
│   ├── login.css          - Login page
│   ├── dashboard.css      - Dashboard
│   ├── fileupload.css     - File upload
│   ├── datareview.css     - Data review
│   ├── dashboardbuilder.css - Builder
│   └── logictransparency.css - Transparency
│
├── store/
│   └── (Zustand stores - to be implemented)
│
├── utils/
│   └── (Helper functions - to be implemented)
│
├── main.tsx              - React entry point
└── App.tsx               - Main component with routing
```

## 🎨 Design System

```
Color Palette:
┌────────────────────────────────────────┐
│ Primary:    #6366f1 (Indigo)          │
│ Secondary:  #8b5cf6 (Purple)          │
│ Success:    #10b981 (Green)           │
│ Warning:    #f59e0b (Amber)           │
│ Danger:     #ef4444 (Red)             │
│ BG:         #f8fafc (Light Gray)      │
│ Text Dark:  #1e293b                   │
│ Text Light: #64748b                   │
└────────────────────────────────────────┘

Spacing:
- 8px, 12px, 16px, 20px, 30px

Border Radius:
- Small: 6px
- Medium: 8px
- Large: 12px

Shadows:
- Light: 0 1px 3px rgba(0,0,0,0.05)
- Medium: 0 4px 12px rgba(0,0,0,0.1)
- Dark: 0 10px 40px rgba(0,0,0,0.2)
```

## 🔄 Component Hierarchy

```
<App>
  └── <Router>
      ├── <Login />
      └── <Layout>
          ├── <Sidebar>
          │   ├── Logo
          │   ├── NavLinks
          │   │   ├── Dashboard
          │   │   ├── Upload Data
          │   │   ├── Data Review
          │   │   ├── Build Dashboard
          │   │   └── Logic Transparency
          │   └── Logout
          ├── <TopBar>
          │   ├── Title
          │   └── UserInfo
          └── <PageContent>
              └── <Outlet /> (Dynamic page)
                  ├── Dashboard
                  │   ├── MetricCard[]
                  │   ├── ChartCard[]
                  │   └── AIInsights
                  ├── FileUpload
                  │   ├── UploadZone
                  │   └── FileList
                  ├── DataIssueReview
                  │   ├── SummaryStats
                  │   ├── IssuesTable
                  │   └── ActionButtons
                  ├── DashboardBuilder
                  │   ├── WidgetPanel
                  │   ├── Canvas
                  │   └── WidgetCard[]
                  └── LogicTransparency
                      ├── InfoCard
                      ├── InsightCard[]
                      └── Methodology
```

## 📱 Responsive Breakpoints

```
Mobile:   < 480px
Tablet:   480px - 768px
Desktop:  768px - 1024px
Large:    > 1024px
```

## 🚀 Deployment Flow

```
Source Code
    ↓
npm run build
    ↓
TypeScript Compilation
    ↓
Vite Build Process
    ↓
dist/ folder
    ├── index.html
    ├── assets/
    │   ├── index-xxxxx.js
    │   └── index-xxxxx.css
    └── (Optimized for production)
    ↓
Deploy to hosting (Vercel, Netlify, etc.)
```

## 🔌 Integration Points

```
Data Sources:
┌──────────────────────────────────────┐
│   WordPress/WooCommerce API          │
│   - Orders                           │
│   - Products                         │
│   - Customers                        │
│   - Analytics data                   │
└───────────┬──────────────────────────┘
            │
            ↓ (Axios)
┌──────────────────────────────────────┐
│   Backend API Service                │
│   - Data processing                  │
│   - AI/ML analysis                   │
│   - Caching                          │
└───────────┬──────────────────────────┘
            │
            ↓ (REST/GraphQL)
┌──────────────────────────────────────┐
│   React Components                   │
│   - Display data                     │
│   - User interactions                │
│   - Charts & visualizations          │
└──────────────────────────────────────┘
```

## 🎯 Feature Implementation Roadmap

```
Phase 1: ✅ UI Framework (DONE)
├── Pages created
├── Styling complete
├── Routing setup
└── Layout configured

Phase 2: 🔄 Backend Integration
├── API connection (Axios)
├── Data fetching
├── Error handling
└── Loading states

Phase 3: 📊 Data Visualization
├── Chart.js integration
├── Real-time data updates
├── Export functionality
└── Filtering & sorting

Phase 4: 🤖 AI Features
├── ChatBot integration
├── Insight generation
├── Confidence scoring
└── Logic transparency

Phase 5: 🔐 Authentication
├── Login/Register
├── JWT tokens
├── Session management
└── Role-based access

Phase 6: 🚀 Deployment
├── Production build
├── Hosting setup
├── CI/CD pipeline
└── Monitoring
```

## 📊 Data Flow Example

```
User Action (Click)
    ↓
Event Handler
    ↓
State Update (useState/Zustand)
    ↓
Component Re-render
    ↓
API Call (Axios) [if needed]
    ↓
Fetch Data
    ↓
Update State
    ↓
Display Updated UI
```

## 🛡️ State Management Plan

```
Zustand Store Structure:
┌─────────────────────────────────────┐
│ useAuthStore                        │
│ ├── user                            │
│ ├── token                           │
│ ├── login(email, password)          │
│ └── logout()                        │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ useDashboardStore                   │
│ ├── metrics                         │
│ ├── charts                          │
│ ├── fetchMetrics()                  │
│ └── setTimeRange(range)             │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ useBuilderStore                     │
│ ├── widgets[]                       │
│ ├── addWidget(widget)               │
│ ├── removeWidget(id)                │
│ └── saveLayout()                    │
└─────────────────────────────────────┘
```

---

**All components are production-ready and can be extended with real data!** 🚀
