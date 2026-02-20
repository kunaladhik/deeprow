import { useState, useEffect } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
  import { Bar, Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import { useAnalyticsStore } from '../store/analytics'
import analyticsAPI, { VisualizationTemplate } from '../utils/api'
import '../styles/analytics.css'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
)

export default function Analytics() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const fileId = searchParams.get('file') || ''
  
  const { fileId: storedFileId, filename, profile, setAnalysisData } = useAnalyticsStore()
  const currentFileId = fileId || storedFileId
  
  const [templates, setTemplates] = useState<VisualizationTemplate[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedTemplate, setSelectedTemplate] = useState<number>(0)

  // Load data when component mounts
  useEffect(() => {
    if (currentFileId) {
      loadAnalytics()
    } else {
      setError('No file selected. Please upload a file first.')
      setLoading(false)
      // Redirect to upload page after 2 seconds
      const timer = setTimeout(() => {
        navigate('/upload')
      }, 2000)
      return () => clearTimeout(timer)
    }
  }, [currentFileId, navigate])

  const loadAnalytics = async () => {
    setLoading(true)
    setError(null)

    try {
      if (!currentFileId) return
      const data = await analyticsAPI.getFullAnalysis(currentFileId)
      setAnalysisData(data.profile, data.insights, data.templates)
      setTemplates(data.templates)
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Failed to load analytics'
      setError(msg)
    } finally {
      setLoading(false)
    }
  }

  const renderKPICard = (template: VisualizationTemplate) => {
    return (
      <div className="kpi-card">
        <div className="kpi-label">{template.label}</div>
        <div className="kpi-value">
          {typeof template.value === 'number'
            ? template.value.toLocaleString('en-US', {
                maximumFractionDigits: 2,
              })
            : 'N/A'}
        </div>
        {template.unit && <div className="kpi-unit">{template.unit}</div>}
        {template.trend && (
          <div className={`kpi-trend ${template.trend}`}>
            {template.trend === 'up' ? '📈' : template.trend === 'down' ? '📉' : '➡️'}
          </div>
        )}
      </div>
    )
  }

  const renderBarChart = (template: VisualizationTemplate) => {
    if (!template.data || template.data.length === 0) return null

    const data = {
      labels: template.data.map((d: any) => d[template.x_axis || 'category']),
      datasets: [
        {
          label: template.y_axis || 'Value',
          data: template.data.map((d: any) => d[template.y_axis || 'value']),
          backgroundColor: 'rgba(99, 102, 241, 0.7)',
          borderColor: 'rgba(99, 102, 241, 1)',
          borderWidth: 1,
        },
      ],
    }

    return <Bar data={data} options={{ responsive: true }} />
  }

  const renderLineChart = (template: VisualizationTemplate) => {
    if (!template.data || template.data.length === 0) return null

    const data = {
      labels: template.data.map((d: any) => d[template.x_axis || 'date']),
      datasets: [
        {
          label: template.y_axis || 'Value',
          data: template.data.map((d: any) => d[template.y_axis || 'value']),
          borderColor: 'rgba(139, 92, 246, 1)',
          backgroundColor: 'rgba(139, 92, 246, 0.1)',
          tension: 0.4,
          fill: true,
        },
      ],
    }

    return <Line data={data} options={{ responsive: true }} />
  }

  const renderHistogram = (template: VisualizationTemplate) => {
    if (!template.data || template.data.length === 0) return null

    const data = {
      labels: template.data.map((d: any) => 
        d.category || `${d.min}-${d.max}`
      ),
      datasets: [
        {
          label: 'Frequency',
          data: template.data.map((d: any) => d.count),
          backgroundColor: 'rgba(34, 197, 94, 0.7)',
          borderColor: 'rgba(34, 197, 94, 1)',
          borderWidth: 1,
        },
      ],
    }

    return <Bar data={data} options={{ responsive: true }} />
  }

  const renderTemplate = (template: VisualizationTemplate) => {
    switch (template.type) {
      case 'kpi_card':
        return renderKPICard(template)
      case 'bar_chart':
        return renderBarChart(template)
      case 'line_chart':
        return renderLineChart(template)
      case 'histogram':
        return renderHistogram(template)
      default:
        return <div>Unsupported chart type: {template.type}</div>
    }
  }

  if (loading) {
    return (
      <div className="analytics">
        <div className="analytics-container">
          <div className="loading-spinner">
            <div className="spinner"></div>
            <p>Analyzing your data...</p>
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="analytics">
        <div className="analytics-container">
          <div className="error-container">
            <h2>❌ Error</h2>
            <p>{error}</p>
            <button onClick={() => navigate('/upload')}>← Upload Data</button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="analytics">
      <div className="analytics-container">
        <div className="analytics-header">
          <div className="header-info">
            <h1>📊 Analytics Dashboard</h1>
            {filename && <p>File: {filename}</p>}
          </div>
        </div>

        {profile && (
          <div className="data-stats">
            <div className="stat-card">
              <div className="stat-label">Rows</div>
              <div className="stat-value">{profile.row_count.toLocaleString()}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Columns</div>
              <div className="stat-value">{profile.column_count}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">KPIs</div>
              <div className="stat-value">{profile.kpis.length}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Data Types</div>
              <div className="stat-value">{profile.numeric_columns.length}N {profile.categorical_columns.length}C</div>
            </div>
          </div>
        )}

        {templates.length > 0 && (
          <div className="analytics-display">
            <div className="chart-selector">
              <h3>Visualizations</h3>
              <div className="chart-buttons">
                {templates.map((template, idx) => (
                  <button
                    key={idx}
                    className={`chart-btn ${selectedTemplate === idx ? 'active' : ''}`}
                    onClick={() => setSelectedTemplate(idx)}
                  >
                    {template.type === 'kpi_card' && '📈'}
                    {template.type === 'bar_chart' && '📊'}
                    {template.type === 'line_chart' && '📉'}
                    {template.type === 'histogram' && '📊'}
                    {template.title || template.label || `Chart ${idx + 1}`}
                  </button>
                ))}
              </div>
            </div>

            <div className="chart-container">
              <div className="chart-wrapper">
                {templates[selectedTemplate] && renderTemplate(templates[selectedTemplate])}
              </div>
            </div>
          </div>
        )}

        {profile && profile.columns && (
          <div className="data-overview">
            <h3>📋 Data Overview</h3>
            <div className="columns-grid">
              {profile.columns.slice(0, 8).map((col: ColumnInfo, idx: number) => (
                <div key={idx} className="column-card">
                  <div className="column-type">
                    {col.type === 'numeric' && '🔢'}
                    {col.type === 'categorical' && '📂'}
                    {col.type === 'date' && '📅'}
                    {col.type === 'text' && '📝'}
                  </div>
                  <div className="column-name">{col.name}</div>
                  <div className="column-stats">
                    <small>{col.type}</small>
                  </div>
                  {col.is_kpi && <div className="kpi-badge">KPI</div>}
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="analytics-actions">
          <button className="btn-new-analysis" onClick={() => navigate('/upload')}>
            ➕ New Analysis
          </button>
        </div>
      </div>
    </div>
  )
}
