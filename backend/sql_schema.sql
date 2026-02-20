-- ============================================================================
-- ANALYTICS ENGINE MVP - PostgreSQL Schema
-- Domain-agnostic self-service analytics platform
-- ============================================================================

-- ============================================================================
-- 1. USERS & AUTHENTICATION
-- ============================================================================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    persona VARCHAR(50),  -- 'teacher', 'researcher', 'business_owner', etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- ============================================================================
-- 2. PROJECTS
-- ============================================================================
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_projects_user_id ON projects(user_id);

-- ============================================================================
-- 3. DATASETS (uploaded files)
-- ============================================================================
CREATE TABLE IF NOT EXISTS datasets (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(755),
    file_size_bytes BIGINT,
    row_count INTEGER,
    column_count INTEGER,
    upload_status VARCHAR(50),  -- 'pending', 'processing', 'success', 'error'
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    uploaded_at TIMESTAMP,
    processed_at TIMESTAMP
);

CREATE INDEX idx_datasets_project_id ON datasets(project_id);

-- ============================================================================
-- 4. DATASET PROFILING (data quality & structure)
-- ============================================================================
CREATE TABLE IF NOT EXISTS dataset_profiles (
    id SERIAL PRIMARY KEY,
    dataset_id INTEGER NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    column_name VARCHAR(255) NOT NULL,
    column_position INTEGER,
    data_type VARCHAR(50),  -- 'numeric', 'categorical', 'date', 'text'
    detected_type VARCHAR(50),  -- what the engine detected
    null_count INTEGER,
    null_percentage DECIMAL(5,2),
    unique_count INTEGER,
    min_value VARCHAR(255),
    max_value VARCHAR(255),
    mean_value DECIMAL(10,4),
    median_value DECIMAL(10,4),
    std_dev DECIMAL(10,4),
    sample_values TEXT,  -- JSON array of sample values
    has_duplicates BOOLEAN,
    has_outliers BOOLEAN,
    date_format VARCHAR(50),  -- if date type
    confidence_score DECIMAL(5,2),  -- ML confidence in classification
    profiling_metadata JSONB  -- catch-all for additional data
);

CREATE INDEX idx_dataset_profiles_dataset_id ON dataset_profiles(dataset_id);

-- ============================================================================
-- 5. SEMANTIC LAYER (Metrics, Dimensions, Time)
-- ============================================================================

-- METRICS (numeric measures)
CREATE TABLE IF NOT EXISTS semantic_metrics (
    id SERIAL PRIMARY KEY,
    dataset_id INTEGER NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    column_name VARCHAR(255) NOT NULL,
    business_name VARCHAR(255) NOT NULL,  -- e.g., "Total Sales"
    aggregation VARCHAR(50) DEFAULT 'sum',  -- 'sum', 'avg', 'count', 'min', 'max'
    data_type VARCHAR(50),
    format_type VARCHAR(50),  -- 'currency', 'percentage', 'decimal', 'integer'
    is_kpi BOOLEAN DEFAULT FALSE,
    description TEXT,
    user_defined BOOLEAN DEFAULT FALSE,  -- true if user edited
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_semantic_metrics_dataset_id ON semantic_metrics(dataset_id);

-- DIMENSIONS (categorical & grouping fields)
CREATE TABLE IF NOT EXISTS semantic_dimensions (
    id SERIAL PRIMARY KEY,
    dataset_id INTEGER NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    column_name VARCHAR(255) NOT NULL,
    business_name VARCHAR(255) NOT NULL,  -- e.g., "Region"
    dimension_type VARCHAR(50),  -- 'categorical', 'geographic', 'hierarchical'
    unique_values_count INTEGER,
    sample_values TEXT,  -- JSON array of top values
    user_defined BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_semantic_dimensions_dataset_id ON semantic_dimensions(dataset_id);

-- TIME DIMENSIONS (date hierarchies)
CREATE TABLE IF NOT EXISTS semantic_time_dimensions (
    id SERIAL PRIMARY KEY,
    dataset_id INTEGER NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    column_name VARCHAR(255) NOT NULL,
    business_name VARCHAR(255) NOT NULL,  -- e.g., "Order Date"
    date_format VARCHAR(50),
    has_year BOOLEAN DEFAULT TRUE,
    has_quarter BOOLEAN DEFAULT TRUE,
    has_month BOOLEAN DEFAULT TRUE,
    has_week BOOLEAN DEFAULT FALSE,
    has_day BOOLEAN DEFAULT FALSE,
    time_granularity VARCHAR(50) DEFAULT 'month',  -- default drill level
    user_defined BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_semantic_time_dimensions_dataset_id ON semantic_time_dimensions(dataset_id);

-- ============================================================================
-- 6. DATA CLEANING RULES (user-approved transformations)
-- ============================================================================
CREATE TABLE IF NOT EXISTS cleaning_rules (
    id SERIAL PRIMARY KEY,
    dataset_id INTEGER NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    column_name VARCHAR(255) NOT NULL,
    rule_type VARCHAR(50),  -- 'remove_duplicates', 'fill_missing', 'rename', 'drop_column'
    rule_config JSONB,  -- flexible config for different rule types
    is_applied BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cleaning_rules_dataset_id ON cleaning_rules(dataset_id);

-- ============================================================================
-- 7. DASHBOARDS
-- ============================================================================
CREATE TABLE IF NOT EXISTS dashboards (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    dataset_id INTEGER NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    dashboard_type VARCHAR(50),  -- 'auto_generated', 'user_created'
    is_default BOOLEAN DEFAULT FALSE,
    layout JSONB,  -- dashboard grid configuration
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_dashboards_project_id ON dashboards(project_id);
CREATE INDEX idx_dashboards_dataset_id ON dashboards(dataset_id);

-- ============================================================================
-- 8. CHARTS (dashboard components)
-- ============================================================================
CREATE TABLE IF NOT EXISTS charts (
    id SERIAL PRIMARY KEY,
    dashboard_id INTEGER NOT NULL REFERENCES dashboards(id) ON DELETE CASCADE,
    chart_type VARCHAR(50) NOT NULL,  -- 'kpi_card', 'trend_chart', 'breakdown_chart', 'table'
    title VARCHAR(255),
    metric_id INTEGER REFERENCES semantic_metrics(id),  -- if chart uses a metric
    dimension_id INTEGER REFERENCES semantic_dimensions(id),  -- grouping dimension
    time_dimension_id INTEGER REFERENCES semantic_time_dimensions(id),  -- if time series
    filters JSONB,  -- applied filters
    chart_config JSONB,  -- visualization-specific config
    position_x INTEGER,
    position_y INTEGER,
    width INTEGER,
    height INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_charts_dashboard_id ON charts(dashboard_id);

-- ============================================================================
-- 9. AUDIT LOG (for trust & transparency)
-- ============================================================================
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(100),  -- 'upload', 'profile', 'create_metric', etc.
    entity_type VARCHAR(50),  -- 'dataset', 'dashboard', etc.
    entity_id INTEGER,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);

-- ============================================================================
-- 10. DATA ISSUES (for transparency)
-- ============================================================================
CREATE TABLE IF NOT EXISTS data_issues (
    id SERIAL PRIMARY KEY,
    dataset_id INTEGER NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    column_name VARCHAR(255),
    issue_type VARCHAR(50),  -- 'missing_values', 'duplicates', 'mixed_types', 'outliers'
    severity VARCHAR(50),  -- 'info', 'warning', 'error'
    count INTEGER,
    percentage DECIMAL(5,2),
    description TEXT,
    is_resolved BOOLEAN DEFAULT FALSE,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_data_issues_dataset_id ON data_issues(dataset_id);

-- ============================================================================
-- SEQUENCES
-- ============================================================================
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users), true);
SELECT setval('projects_id_seq', (SELECT MAX(id) FROM projects), true);
SELECT setval('datasets_id_seq', (SELECT MAX(id) FROM datasets), true);

-- ============================================================================
-- DONE
-- ============================================================================
