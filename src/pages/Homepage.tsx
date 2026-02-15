import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/homepage.css';

export default function Homepage() {
  const navigate = useNavigate();
  const [isHovered, setIsHovered] = useState(false);

  const handleGetStarted = () => {
    navigate('/login');
  };

  return (
    <div className="homepage">
      {/* Animated Background */}
      <div className="bg-gradient-animation"></div>
      <div className="grid-background"></div>

      {/* Header */}
      <header className="homepage-header">
        <div className="header-container">
          <div className="logo-section">
            <img src="/deeprow-logo.svg" alt="DeepRow" className="logo-image" />
            <span className="logo-text">DeepRow</span>
          </div>
          <button className="header-signin-btn" onClick={() => navigate('/login')}>
            Sign In
          </button>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <div className="hero-text">
            <h1 className="hero-title">
              Transform Data Into <span className="gradient-text">Intelligence</span>
            </h1>
            <p className="hero-subtitle">
              Enterprise-grade data analytics powered by AI. Upload, analyze, visualize, and share insights in seconds.
            </p>

            <div className="hero-cta">
              <button 
                className="btn-primary" 
                onClick={handleGetStarted}
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
              >
                <span>Get Started Free</span>
                <span className="btn-arrow">→</span>
              </button>
            </div>

            <div className="hero-stats">
              <div className="stat">
                <span className="stat-value">10M+</span>
                <span className="stat-label">Data Points</span>
              </div>
              <div className="stat">
                <span className="stat-value">99.9%</span>
                <span className="stat-label">Uptime</span>
              </div>
              <div className="stat">
                <span className="stat-value">50k+</span>
                <span className="stat-label">Users</span>
              </div>
            </div>
          </div>

          <div className="hero-visual">
            <div className="floating-card card-1">
              <div className="chart-icon">📊</div>
              <p>Real-time Analytics</p>
            </div>
            <div className="floating-card card-2">
              <div className="chart-icon">📈</div>
              <p>Interactive Charts</p>
            </div>
            <div className="floating-card card-3">
              <div className="chart-icon">🎨</div>
              <p>Custom Visuals</p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features">
        <div className="features-header">
          <h2>Powerful Capabilities</h2>
          <p>Everything you need to analyze data like a pro</p>
        </div>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon-bg"></div>
            <div className="feature-icon">⚡</div>
            <h3>Lightning Fast</h3>
            <p>Analyze millions of data points in milliseconds</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon-bg"></div>
            <div className="feature-icon">🔒</div>
            <h3>Enterprise Secure</h3>
            <p>Bank-level encryption and compliance standards</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon-bg"></div>
            <div className="feature-icon">🎯</div>
            <h3>AI-Powered</h3>
            <p>Automatic insights and pattern detection</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon-bg"></div>
            <div className="feature-icon">📱</div>
            <h3>Fully Responsive</h3>
            <p>Works seamlessly on any device</p>
          </div>
        </div>
      </section>

      {/* Use Cases */}
      <section className="use-cases">
        <div className="use-cases-header">
          <h2>Built for Everyone</h2>
          <p>From students to enterprises, DeepRow scales with you</p>
        </div>
        <div className="use-cases-grid">
          <div className="use-case-card">
            <div className="use-case-number">01</div>
            <h4>Professionals</h4>
            <p>Build comprehensive business reports and dashboards</p>
          </div>
          <div className="use-case-card">
            <div className="use-case-number">02</div>
            <h4>Educators</h4>
            <p>Create engaging data visualization projects</p>
          </div>
          <div className="use-case-card">
            <div className="use-case-number">03</div>
            <h4>Researchers</h4>
            <p>Analyze complex datasets with advanced tools</p>
          </div>
          <div className="use-case-card">
            <div className="use-case-number">04</div>
            <h4>Healthcare</h4>
            <p>Track patient outcomes and medical insights</p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="cta-content">
          <h2>Ready to Transform Your Data?</h2>
          <p>Start free, no credit card required. Upgrade anytime.</p>
          <button className="btn-primary-large" onClick={handleGetStarted}>
            Get Started Now
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="homepage-footer">
        <div className="footer-content">
          <div className="footer-section">
            <h4>DeepRow</h4>
            <p>&copy; 2026 DeepRow. All rights reserved.</p>
          </div>
          <div className="footer-links">
            <a href="#privacy">Privacy Policy</a>
            <a href="#terms">Terms</a>
            <a href="#contact">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
}

