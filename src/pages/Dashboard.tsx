import { useState } from 'react'
import '../styles/dashboard.css'

export default function Dashboard() {
  const [metrics] = useState([
    { title: 'Total Orders', value: '2,543', change: '+12.5%', icon: '📦' },
    { title: 'Revenue', value: '$45.2K', change: '+8.3%', icon: '💰' },
    { title: 'Customers', value: '1,234', change: '+5.2%', icon: '👥' },
    { title: 'Avg Order Value', value: '$178', change: '+3.1%', icon: '💳' },
  ])

  return (
    <div className="dashboard-page">
      <h1>Dashboard Overview</h1>
      
      <div className="metrics-grid">
        {metrics.map((metric, idx) => (
          <div key={idx} className="metric-card">
            <div className="metric-icon">{metric.icon}</div>
            <div className="metric-content">
              <p className="metric-title">{metric.title}</p>
              <p className="metric-value">{metric.value}</p>
              <p className="metric-change positive">{metric.change}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="charts-section">
        <div className="chart-card">
          <h3>Sales Trend (Last 7 Days)</h3>
          <div className="chart-placeholder">
            <p>📊 Chart will be rendered here</p>
            <p style={{fontSize: '12px', color: '#888'}}>Chart.js integration</p>
          </div>
        </div>

        <div className="chart-card">
          <h3>Top Products</h3>
          <div className="chart-placeholder">
            <p>🏆 Top products list</p>
            <p style={{fontSize: '12px', color: '#888'}}>Real-time data</p>
          </div>
        </div>
      </div>

      <div className="ai-insights">
        <h3>🤖 AI Insights</h3>
        <div className="insights-box">
          <p>Your sales increased by 12.5% this week. The top-performing product is "Premium Widget" with 324 sales.</p>
          <p>Recommendation: Consider increasing inventory for the top 3 products to avoid stockouts.</p>
        </div>
      </div>
    </div>
  )
}
