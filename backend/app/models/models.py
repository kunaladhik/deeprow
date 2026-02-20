"""
SQLAlchemy ORM Models
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, BigInteger, Numeric, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    persona = Column(String(50))  # teacher, researcher, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")

class Project(Base):
    """Project model (groups datasets)"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="projects")
    datasets = relationship("Dataset", back_populates="project", cascade="all, delete-orphan")
    dashboards = relationship("Dashboard", back_populates="project", cascade="all, delete-orphan")

class Dataset(Base):
    """Uploaded dataset model"""
    __tablename__ = "datasets"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(755))
    file_size_bytes = Column(BigInteger)
    row_count = Column(Integer)
    column_count = Column(Integer)
    upload_status = Column(String(50), default="pending")  # pending, processing, success, error
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    uploaded_at = Column(DateTime)
    processed_at = Column(DateTime)
    
    # Relationships
    project = relationship("Project", back_populates="datasets")
    profiles = relationship("DatasetProfile", back_populates="dataset", cascade="all, delete-orphan")
    metrics = relationship("SemanticMetric", back_populates="dataset", cascade="all, delete-orphan")
    dimensions = relationship("SemanticDimension", back_populates="dataset", cascade="all, delete-orphan")
    time_dimensions = relationship("SemanticTimeDimension", back_populates="dataset", cascade="all, delete-orphan")
    cleaning_rules = relationship("CleaningRule", back_populates="dataset", cascade="all, delete-orphan")
    data_issues = relationship("DataIssue", back_populates="dataset", cascade="all, delete-orphan")
    dashboards = relationship("Dashboard", back_populates="dataset", cascade="all, delete-orphan")

class DatasetProfile(Base):
    """Data profiling metadata"""
    __tablename__ = "dataset_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    column_name = Column(String(255), nullable=False)
    column_position = Column(Integer)
    data_type = Column(String(50))  # numeric, categorical, date, text
    detected_type = Column(String(50))
    null_count = Column(Integer)
    null_percentage = Column(Numeric(5, 2))
    unique_count = Column(Integer)
    min_value = Column(String(255))
    max_value = Column(String(255))
    mean_value = Column(Numeric(10, 4))
    median_value = Column(Numeric(10, 4))
    std_dev = Column(Numeric(10, 4))
    sample_values = Column(Text)  # JSON array
    has_duplicates = Column(Boolean, default=False)
    has_outliers = Column(Boolean, default=False)
    date_format = Column(String(50))
    confidence_score = Column(Numeric(5, 2))
    profiling_metadata = Column(JSON)
    
    # Relationships
    dataset = relationship("Dataset", back_populates="profiles")

class SemanticMetric(Base):
    """Metric definition (numeric measure)"""
    __tablename__ = "semantic_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    column_name = Column(String(255), nullable=False)
    business_name = Column(String(255), nullable=False)  # e.g., "Total Sales"
    aggregation = Column(String(50), default="sum")  # sum, avg, count, min, max
    data_type = Column(String(50))
    format_type = Column(String(50))  # currency, percentage, decimal, integer
    is_kpi = Column(Boolean, default=False)
    description = Column(Text)
    user_defined = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    dataset = relationship("Dataset", back_populates="metrics")
    charts = relationship("Chart", back_populates="metric")

class SemanticDimension(Base):
    """Dimension definition (categorical/grouping field)"""
    __tablename__ = "semantic_dimensions"
    
    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    column_name = Column(String(255), nullable=False)
    business_name = Column(String(255), nullable=False)  # e.g., "Region"
    dimension_type = Column(String(50))  # categorical, geographic, hierarchical
    unique_values_count = Column(Integer)
    sample_values = Column(Text)  # JSON array
    user_defined = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    dataset = relationship("Dataset", back_populates="dimensions")
    charts = relationship("Chart", back_populates="dimension")

class SemanticTimeDimension(Base):
    """Time dimension definition (date hierarchies)"""
    __tablename__ = "semantic_time_dimensions"
    
    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    column_name = Column(String(255), nullable=False)
    business_name = Column(String(255), nullable=False)  # e.g., "Order Date"
    date_format = Column(String(50))
    has_year = Column(Boolean, default=True)
    has_quarter = Column(Boolean, default=True)
    has_month = Column(Boolean, default=True)
    has_week = Column(Boolean, default=False)
    has_day = Column(Boolean, default=False)
    time_granularity = Column(String(50), default="month")
    user_defined = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    dataset = relationship("Dataset", back_populates="time_dimensions")
    charts = relationship("Chart", back_populates="time_dimension")

class CleaningRule(Base):
    """Data cleaning rules"""
    __tablename__ = "cleaning_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    column_name = Column(String(255), nullable=False)
    rule_type = Column(String(50))  # remove_duplicates, fill_missing, etc.
    rule_config = Column(JSON)  # flexible config
    is_applied = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    dataset = relationship("Dataset", back_populates="cleaning_rules")

class Dashboard(Base):
    """Dashboard model"""
    __tablename__ = "dashboards"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    dashboard_type = Column(String(50), default="auto_generated")
    is_default = Column(Boolean, default=False)
    layout = Column(JSON)  # grid configuration
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="dashboards")
    dataset = relationship("Dataset", back_populates="dashboards")
    charts = relationship("Chart", back_populates="dashboard", cascade="all, delete-orphan")

class Chart(Base):
    """Chart/widget in dashboard"""
    __tablename__ = "charts"
    
    id = Column(Integer, primary_key=True, index=True)
    dashboard_id = Column(Integer, ForeignKey("dashboards.id"), nullable=False)
    chart_type = Column(String(50), nullable=False)  # kpi_card, trend_chart, breakdown_chart, table
    title = Column(String(255))
    metric_id = Column(Integer, ForeignKey("semantic_metrics.id"))
    dimension_id = Column(Integer, ForeignKey("semantic_dimensions.id"))
    time_dimension_id = Column(Integer, ForeignKey("semantic_time_dimensions.id"))
    filters = Column(JSON)
    chart_config = Column(JSON)  # visualization-specific config
    position_x = Column(Integer)
    position_y = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    dashboard = relationship("Dashboard", back_populates="charts")
    metric = relationship("SemanticMetric", back_populates="charts")
    dimension = relationship("SemanticDimension", back_populates="charts")
    time_dimension = relationship("SemanticTimeDimension", back_populates="charts")

class DataIssue(Base):
    """Data quality issues detected"""
    __tablename__ = "data_issues"
    
    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    column_name = Column(String(255))
    issue_type = Column(String(50))  # missing_values, duplicates, mixed_types, outliers
    severity = Column(String(50))  # info, warning, error
    count = Column(Integer)
    percentage = Column(Numeric(5, 2))
    description = Column(Text)
    is_resolved = Column(Boolean, default=False)
    detected_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    dataset = relationship("Dataset", back_populates="data_issues")
