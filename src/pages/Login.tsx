import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import analyticsAPI from '../utils/api'
import '../styles/login.css'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [isSignUp, setIsSignUp] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = isSignUp
        ? await analyticsAPI.signup(email, password)
        : await analyticsAPI.login(email, password)

      // Store token in localStorage
      localStorage.setItem('token', response.access_token)
      
      // Redirect to file upload page
      navigate('/upload')
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Authentication failed'
      setError(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-box">
        <div className="login-header">
          <span className="login-icon">📊</span>
          <h1 className="login-title">DataFlow Intelligence</h1>
          <p className="login-subtitle">Transform Your Data into Insights</p>
        </div>
        
        {error && <div style={{ color: '#ff6b6b', marginBottom: '1rem', padding: '0.5rem', backgroundColor: '#ffe0e0', borderRadius: '0.25rem' }}>{error}</div>}
        
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              placeholder="your@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button type="submit" className="login-btn" disabled={loading}>
            {loading ? (isSignUp ? 'Creating account...' : 'Signing in...') : (isSignUp ? 'Sign Up' : 'Sign In')}
          </button>
        </form>

        <div className="login-footer">
          <p>
            {isSignUp ? 'Already have an account? ' : "Don't have an account? "}
            <a href="#" onClick={(e) => { e.preventDefault(); setIsSignUp(!isSignUp); setError(''); }}>
              {isSignUp ? 'Sign in' : 'Sign up'}
            </a>
          </p>
        </div>
      </div>
    </div>
  )
}
