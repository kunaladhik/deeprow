import { useState } from 'react';
import { Line, Bar, Pie, Scatter } from 'react-chartjs-2';
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
} from 'chart.js';
import '../styles/analytics.css';

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
);

export default function Analytics() {
  const [file, setFile] = useState<File | null>(null);
  const [data, setData] = useState<any>(null);
  const [selectedChart, setSelectedChart] = useState('line');
  const [fileName, setFileName] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [dataStats, setDataStats] = useState<any>(null);

  const chartTypes = [
    { id: 'line', name: 'Line Chart', icon: '📈' },
    { id: 'bar', name: 'Bar Chart', icon: '📊' },
    { id: 'pie', name: 'Pie Chart', icon: '🥧' },
    { id: 'scatter', name: 'Scatter Plot', icon: '🔵' },
    { id: 'area', name: 'Area Chart', icon: '🗻' },
    { id: 'doughnut', name: 'Doughnut', icon: '🍩' },
  ];

  // Mock data for demonstration
  const mockChartData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Data Series 1',
        data: [65, 59, 80, 81, 56, 55],
        borderColor: '#6366f1',
        backgroundColor: 'rgba(99, 102, 241, 0.1)',
        fill: true,
        tension: 0.4,
      },
      {
        label: 'Data Series 2',
        data: [45, 39, 60, 61, 36, 45],
        borderColor: '#8b5cf6',
        backgroundColor: 'rgba(139, 92, 246, 0.1)',
        fill: true,
        tension: 0.4,
      },
    ],
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.currentTarget.classList.add('drag-active');
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.currentTarget.classList.remove('drag-active');
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.currentTarget.classList.remove('drag-active');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.length) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const handleFileSelect = (selectedFile: File) => {
    const validTypes = [
      'application/vnd.ms-excel',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'text/csv',
    ];

    if (validTypes.includes(selectedFile.type) || selectedFile.name.endsWith('.csv') || selectedFile.name.endsWith('.xlsx')) {
      setFile(selectedFile);
      setFileName(selectedFile.name);
      analyzeFile(selectedFile);
    } else {
      alert('Please upload a valid Excel or CSV file');
    }
  };

  const analyzeFile = (selectedFile: File) => {
    setIsAnalyzing(true);
    // Simulate analysis
    setTimeout(() => {
      setData(mockChartData);
      setDataStats({
        records: 1250,
        fields: 8,
        quality: 96,
        missingValues: 12,
      });
      setIsAnalyzing(false);
    }, 1500);
  };

  const renderChart = () => {
    if (!data) return null;

    const commonOptions = {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          position: 'top' as const,
        },
      },
    };

    switch (selectedChart) {
      case 'line':
        return <Line data={data} options={commonOptions} />;
      case 'bar':
        return <Bar data={data} options={commonOptions} />;
      case 'pie':
        return <Pie data={mockChartData} options={commonOptions} />;
      case 'scatter':
        return <Scatter data={data} options={commonOptions} />;
      default:
        return <Line data={data} options={commonOptions} />;
    }
  };

  const handleDownload = (format: 'ppt' | 'pdf') => {
    alert(`Downloading as ${format.toUpperCase()}...`);
    // Implementation would call backend API
  };

  return (
    <div className="analytics">
      <div className="analytics-container">
        {/* Header */}
        <div className="analytics-header">
          <div className="header-info">
            <h1>Analytics Dashboard</h1>
            <p>Upload your data and transform it into interactive insights</p>
          </div>
        </div>

        {!data ? (
          // Upload Section
          <div className="upload-section">
            <div
              className="drop-zone"
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
            >
              <div className="drop-zone-content">
                <div className="upload-icon">📁</div>
                <h2>Drop your file here</h2>
                <p>or</p>
                <label className="file-input-label">
                  <span>Choose File</span>
                  <input type="file" onChange={handleFileInput} accept=".csv,.xlsx,.xls" />
                </label>
                <p className="upload-hint">Supports CSV and Excel files</p>
              </div>
            </div>

            {isAnalyzing && (
              <div className="analyzing">
                <div className="spinner"></div>
                <p>Analyzing your data...</p>
              </div>
            )}

            <div className="upload-info">
              <div className="info-card">
                <span className="info-icon">✨</span>
                <h3>Smart Analysis</h3>
                <p>We automatically detect patterns and generate insights</p>
              </div>
              <div className="info-card">
                <span className="info-icon">📊</span>
                <h3>Multiple Formats</h3>
                <p>Choose from 10+ chart types to visualize your data</p>
              </div>
              <div className="info-card">
                <span className="info-icon">⬇️</span>
                <h3>Easy Sharing</h3>
                <p>Download as PDF, PowerPoint, or image instantly</p>
              </div>
            </div>
          </div>
        ) : (
          // Analytics Display Section
          <div className="analytics-display">
            {/* Data Stats */}
            <div className="data-stats">
              <div className="stat-card">
                <div className="stat-label">Records</div>
                <div className="stat-value">{dataStats.records.toLocaleString()}</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Fields</div>
                <div className="stat-value">{dataStats.fields}</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Data Quality</div>
                <div className="stat-value">{dataStats.quality}%</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Missing Values</div>
                <div className="stat-value">{dataStats.missingValues}</div>
              </div>
            </div>

            {/* Chart Type Selector */}
            <div className="chart-selector">
              <h3>Choose Visualization Type</h3>
              <div className="chart-buttons">
                {chartTypes.map((chart) => (
                  <button
                    key={chart.id}
                    className={`chart-btn ${selectedChart === chart.id ? 'active' : ''}`}
                    onClick={() => setSelectedChart(chart.id)}
                  >
                    <span className="chart-btn-icon">{chart.icon}</span>
                    <span className="chart-btn-name">{chart.name}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Chart Display */}
            <div className="chart-container">
              <div className="chart-wrapper">{renderChart()}</div>
            </div>

            {/* Actions */}
            <div className="analytics-actions">
              <div className="action-group">
                <h3>Download Report</h3>
                <div className="action-buttons">
                  <button className="btn-action btn-pdf" onClick={() => handleDownload('pdf')}>
                    📄 Download as PDF
                  </button>
                  <button className="btn-action btn-ppt" onClick={() => handleDownload('ppt')}>
                    📊 Download as PowerPoint
                  </button>
                </div>
              </div>
              <button className="btn-new-analysis" onClick={() => {
                setData(null);
                setFile(null);
                setFileName('');
                setSelectedChart('line');
              }}>
                ➕ New Analysis
              </button>
            </div>

            {/* File Info */}
            <div className="file-info">
              <p>Current file: <strong>{fileName}</strong></p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
