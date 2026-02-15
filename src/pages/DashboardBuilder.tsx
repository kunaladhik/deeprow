import { useState } from 'react'
import '../styles/dashboardbuilder.css'

export default function DashboardBuilder() {
  const [widgets, setWidgets] = useState([
    { id: 1, title: 'Sales Overview', type: 'chart', position: 1 },
    { id: 2, title: 'Top Products', type: 'table', position: 2 },
  ])

  const [selectedWidget, setSelectedWidget] = useState<number | null>(null)

  const availableWidgets = [
    { name: 'Line Chart', icon: '📈', type: 'chart' },
    { name: 'Bar Chart', icon: '📊', type: 'chart' },
    { name: 'Pie Chart', icon: '🥧', type: 'chart' },
    { name: 'Table', icon: '📋', type: 'table' },
    { name: 'KPI Card', icon: '🎯', type: 'metric' },
    { name: 'Heatmap', icon: '🔥', type: 'chart' },
  ]

  const addWidget = (type: string) => {
    const newWidget = {
      id: Math.max(...widgets.map((w) => w.id), 0) + 1,
      title: `New Widget ${widgets.length + 1}`,
      type,
      position: widgets.length + 1,
    }
    setWidgets([...widgets, newWidget])
  }

  const removeWidget = (id: number) => {
    setWidgets(widgets.filter((w) => w.id !== id))
  }

  return (
    <div className="builder-page">
      <h1>Dashboard Builder</h1>
      <p className="subtitle">Drag & drop widgets to customize your dashboard</p>

      <div className="builder-container">
        <aside className="widget-panel">
          <h3>Available Widgets</h3>
          <div className="widget-list">
            {availableWidgets.map((widget, idx) => (
              <button
                key={idx}
                className="widget-btn"
                onClick={() => addWidget(widget.type)}
              >
                <span className="icon">{widget.icon}</span>
                <span>{widget.name}</span>
              </button>
            ))}
          </div>
        </aside>

        <main className="canvas">
          <div className="canvas-header">
            <h3>Canvas</h3>
            <button className="save-btn">💾 Save Dashboard</button>
          </div>
          <div className="widgets-grid">
            {widgets.length === 0 ? (
              <div className="empty-state">
                <p>Select widgets from the left to get started</p>
              </div>
            ) : (
              widgets.map((widget) => (
                <div
                  key={widget.id}
                  className={`widget-card ${selectedWidget === widget.id ? 'selected' : ''}`}
                  onClick={() => setSelectedWidget(widget.id)}
                >
                  <div className="widget-header">
                    <h4>{widget.title}</h4>
                    <button
                      className="delete-btn"
                      onClick={(e) => {
                        e.stopPropagation()
                        removeWidget(widget.id)
                      }}
                    >
                      ✕
                    </button>
                  </div>
                  <div className="widget-preview">
                    <p>Widget Preview ({widget.type})</p>
                  </div>
                </div>
              ))
            )}
          </div>
        </main>
      </div>
    </div>
  )
}
