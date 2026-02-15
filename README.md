# DataFlow AI - Data Analytics Web Application

A modern React.js web application for AI-powered data analytics with an intuitive UI for e-commerce and business analytics.

## 🚀 Features

- **Login/Signup**: Secure authentication page
- **Dashboard**: Real-time metrics and insights
- **File Upload**: Drag-and-drop CSV/Excel file upload
- **Data Issue Review**: Identify and fix data quality issues
- **Dashboard Builder**: Low-code dashboard customization
- **Interactive Charts**: Visualize data with Chart.js
- **Logic Transparency**: Understand how AI insights are generated (Trust Layer)

## 📋 Project Structure

```
src/
├── pages/                    # Page components
│   ├── Login.tsx
│   ├── Dashboard.tsx
│   ├── FileUpload.tsx
│   ├── DataIssueReview.tsx
│   ├── DashboardBuilder.tsx
│   └── LogicTransparency.tsx
├── components/              # Reusable components
│   └── Layout.tsx
├── store/                   # Zustand state management
├── utils/                   # Utility functions
├── styles/                  # CSS files
│   ├── index.css
│   ├── layout.css
│   ├── login.css
│   ├── dashboard.css
│   ├── fileupload.css
│   ├── datareview.css
│   ├── dashboardbuilder.css
│   └── logictransparency.css
├── App.tsx                  # Main app component
└── main.tsx                 # Entry point
```

## 🛠️ Tech Stack

- **Frontend Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Routing**: React Router DOM v6
- **State Management**: Zustand
- **Charting**: Chart.js & react-chartjs-2
- **HTTP Client**: Axios
- **Styling**: CSS3 with CSS Variables
- **CSS Features**: Grid, Flexbox, Gradients, Transitions

## 📦 Dependencies

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "chart.js": "^4.4.0",
    "react-chartjs-2": "^5.2.0",
    "axios": "^1.6.0",
    "zustand": "^4.4.0",
    "tailwindcss": "^3.3.0"
  }
}
```

## 🎨 Design Features

- **Modern UI**: Clean, professional design with gradient accents
- **Responsive**: Mobile-friendly layouts
- **Dark Mode Ready**: CSS variables for easy theme switching
- **Accessibility**: Semantic HTML and proper ARIA labels
- **Performance**: Optimized CSS and lazy loading

## 🔧 Getting Started

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Build for production:
```bash
npm run build
```

4. Preview production build:
```bash
npm run preview
```

## 📱 Pages Overview

### 1. Login Page
- Email/password authentication
- Sign-up link
- Responsive design

### 2. Dashboard
- Key metrics (Orders, Revenue, Customers, AOV)
- Sales trend chart
- Top products list
- AI insights section

### 3. File Upload
- Drag-and-drop file upload
- Support for CSV and Excel files
- File list with removal option
- Analyze button

### 4. Data Issue Review
- Data quality summary
- Issues table (Missing, Duplicates, Type Mismatch)
- Severity badges (Low, Medium, High)
- Fix and export options

### 5. Dashboard Builder
- Widget panel with 6+ widget types
- Canvas with drag-drop support
- Widget customization
- Save dashboard option

### 6. Logic Transparency
- AI insight explanation
- Confidence scores
- Data points used
- AI methodology breakdown

## 🎯 Color Scheme

- **Primary**: #6366f1 (Indigo)
- **Secondary**: #8b5cf6 (Purple)
- **Success**: #10b981 (Green)
- **Warning**: #f59e0b (Amber)
- **Danger**: #ef4444 (Red)
- **Background**: #f8fafc (Light Gray)

## 📝 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Run ESLint
- `npm run preview` - Preview production build

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Submit a pull request

## 📄 License

MIT License

## 🔗 Resources

- [React Documentation](https://react.dev)
- [Vite Documentation](https://vitejs.dev)
- [React Router](https://reactrouter.com)
- [Chart.js](https://www.chartjs.org)
- [Zustand](https://github.com/pmndrs/zustand)

---

**Built with ❤️ for AI-powered analytics**
