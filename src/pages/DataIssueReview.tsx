import '../styles/datareview.css'

export default function DataIssueReview() {
  const issues = [
    { id: 1, type: 'Missing Data', field: 'Customer Email', count: 23, severity: 'medium' },
    { id: 2, type: 'Duplicates', field: 'Order ID', count: 5, severity: 'high' },
    { id: 3, type: 'Invalid Format', field: 'Phone Number', count: 12, severity: 'low' },
    { id: 4, type: 'Type Mismatch', field: 'Price', count: 8, severity: 'high' },
  ]

  return (
    <div className="data-review-page">
      <h1>Data Issue Review</h1>
      <p className="subtitle">Identify and fix data quality issues</p>

      <div className="summary-stats">
        <div className="stat">
          <p className="stat-label">Total Records</p>
          <p className="stat-value">10,000</p>
        </div>
        <div className="stat">
          <p className="stat-label">Issues Found</p>
          <p className="stat-value">48</p>
        </div>
        <div className="stat">
          <p className="stat-label">Quality Score</p>
          <p className="stat-value">92%</p>
        </div>
      </div>

      <div className="issues-table">
        <h3>Issues Detected</h3>
        <table>
          <thead>
            <tr>
              <th>Issue Type</th>
              <th>Field</th>
              <th>Count</th>
              <th>Severity</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {issues.map((issue) => (
              <tr key={issue.id} className={`severity-${issue.severity}`}>
                <td>{issue.type}</td>
                <td>{issue.field}</td>
                <td className="count">{issue.count}</td>
                <td>
                  <span className={`badge severity-${issue.severity}`}>
                    {issue.severity.toUpperCase()}
                  </span>
                </td>
                <td>
                  <button className="action-btn">Review</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="action-buttons">
        <button className="btn btn-primary">Fix All Issues</button>
        <button className="btn btn-secondary">Export Report</button>
      </div>
    </div>
  )
}
