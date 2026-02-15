import { useState } from 'react'
import '../styles/fileupload.css'

export default function FileUpload() {
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([])
  const [dragActive, setDragActive] = useState(false)

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
            />
          </label>
          <p className="file-types">Supported: CSV, Excel (.xls, .xlsx)</p>
        </div>
      </div>

      {uploadedFiles.length > 0 && (
        <div className="uploaded-files">
          <h3>📋 Uploaded Files ({uploadedFiles.length})</h3>
          <ul className="file-list">
            {uploadedFiles.map((file, idx) => (
              <li key={idx} className="file-item">
                <span className="file-icon">📄</span>
                <div className="file-info">
                  <p className="file-name">{file.name}</p>
                  <p className="file-size">{(file.size / 1024).toFixed(2)} KB</p>
                </div>
                <button
                  className="remove-btn"
                  onClick={() => removeFile(idx)}
                >
                  ✕
                </button>
              </li>
            ))}
          </ul>
          <button className="analyze-btn">Analyze Files →</button>
        </div>
      )}
    </div>
  )
}
