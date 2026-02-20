import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAnalyticsStore } from '../store/analytics'
import analyticsAPI from '../utils/api'
import '../styles/fileupload.css'

export default function FileUpload() {
  const navigate = useNavigate()
  const { setFileId, setProfile } = useAnalyticsStore()
  
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([])
  const [dragActive, setDragActive] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [uploadError, setUploadError] = useState('')
  const [uploadSuccess, setUploadSuccess] = useState('')
  const [projectId, setProjectId] = useState<string | null>(null)
  const [token, setToken] = useState<string | null>(null)

  // Initialize token and get/create default project
  useEffect(() => {
    const storedToken = localStorage.getItem('token')
    if (!storedToken) {
      navigate('/login')
      return
    }
    setToken(storedToken)
    initializeProject(storedToken)
  }, [])

  const initializeProject = async (token: string) => {
    try {
      // Try to get existing projects
      const projects = await analyticsAPI.getProjects(token)
      if (projects.length > 0) {
        // Use first project
        setProjectId(projects[0].id)
      } else {
        // Create a default project
        const newProject = await analyticsAPI.createProject('Default Project', token)
        setProjectId(newProject.id)
      }
    } catch (err) {
      console.error('Failed to initialize project:', err)
      // Create a default project
      try {
        const newProject = await analyticsAPI.createProject('Default Project', token)
        setProjectId(newProject.id)
      } catch (createErr) {
        console.error('Failed to create project:', createErr)
      }
    }
  }

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    const files = e.dataTransfer.files
    if (files && files.length > 0) {
      const newFiles = Array.from(files).filter(
        (f) => f.type === 'text/csv' || f.type === 'application/vnd.ms-excel' || f.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      )
      setUploadedFiles((prev) => [...prev, ...newFiles])
    }
  }

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files) {
      setUploadedFiles((prev) => [...prev, ...Array.from(files)])
    }
  }

  const removeFile = (index: number) => {
    setUploadedFiles((prev) => prev.filter((_, i) => i !== index))
  }

  const handleUpload = async (file: File) => {
    if (!projectId || !token) {
      setUploadError('Project not initialized. Please refresh the page.')
      return
    }

    setUploading(true)
    setUploadError('')
    setUploadSuccess('')

    try {
      const response = await analyticsAPI.uploadFile(file, projectId, token)
      
      if (response.success) {
        setUploadSuccess(`✅ ${file.name} uploaded successfully!`)
        setFileId(response.file_id, response.filename)
        setProfile(response.profile)
        
        // Redirect to analytics view
        setTimeout(() => {
          navigate(`/analytics?file=${response.file_id}`)
        }, 1500)
      }
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Upload failed'
      setUploadError(errorMsg)
    } finally {
      setUploading(false)
    }
  }

  const handleAnalyzeSampleData = async () => {
    setUploading(true)
    setUploadError('')

    try {
      const response = await analyticsAPI.getSampleData()
      setFileId('sample_data', 'Sample E-Commerce Data')
      setProfile(response.profile)
      
      // Redirect to analytics view
      setTimeout(() => {
        navigate(`/analytics?file=sample_data`)
      }, 500)
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to load sample data'
      setUploadError(errorMsg)
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="upload-page">
      <h1>Upload Data Files</h1>
      <p className="subtitle">Upload CSV or Excel files to analyze your data</p>

      <div
        className={`upload-zone ${dragActive ? 'active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <div className="upload-content">
          <p className="upload-icon">📁</p>
          <h2>Drag & Drop Your Files Here</h2>
          <p>or</p>
          <label className="file-input-label">
            Browse Files
            <input
              type="file"
              multiple
              accept=".csv,.xlsx,.xls"
              onChange={handleFileInput}
              style={{ display: 'none' }}
              disabled={uploading}
            />
          </label>
          <p className="file-types">Supported: CSV, Excel (.xls, .xlsx)</p>
        </div>
      </div>

      {uploadError && (
        <div className="error-message">
          ❌ {uploadError}
        </div>
      )}

      {uploadSuccess && (
        <div className="success-message">
          {uploadSuccess}
        </div>
      )}

      {uploadedFiles.length > 0 && (
        <div className="uploaded-files">
          <h3>📋 Files Ready to Upload ({uploadedFiles.length})</h3>
          <ul className="file-list">
            {uploadedFiles.map((file, idx) => (
              <li key={idx} className="file-item">
                <span className="file-icon">📄</span>
                <div className="file-info">
                  <p className="file-name">{file.name}</p>
                  <p className="file-size">{(file.size / 1024).toFixed(2)} KB</p>
                </div>
                <button
                  className="upload-file-btn"
                  onClick={() => handleUpload(file)}
                  disabled={uploading}
                >
                  {uploading ? '⏳ Processing...' : '⬆️ Upload'}
                </button>
                <button
                  className="remove-btn"
                  onClick={() => removeFile(idx)}
                  disabled={uploading}
                >
                  ✕
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="demo-section">
        <h3>🎯 Try Demo Data First</h3>
        <p>No file? Start with our sample e-commerce dataset</p>
        <button 
          className="demo-btn"
          onClick={handleAnalyzeSampleData}
          disabled={uploading}
        >
          {uploading ? '⏳ Loading...' : '📊 Load Sample Data'}
        </button>
      </div>
    </div>
  )
}
