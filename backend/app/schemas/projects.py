"""
Project and dataset request/response schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class ProjectCreateRequest(BaseModel):
    """Create a new project"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    
    class Config:
        example = {
            "name": "Q4 Sales Analysis",
            "description": "Quarterly sales performance review"
        }


class ProjectResponse(BaseModel):
    """Project response"""
    id: int
    user_id: int
    name: str
    description: Optional[str] = None
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True
        example = {
            "id": 1,
            "user_id": 1,
            "name": "Q4 Sales Analysis",
            "description": "Quarterly sales performance review",
            "created_at": "2024-01-15T10:30:00",
            "updated_at": "2024-01-15T10:30:00"
        }


class DatasetStatus(str, Enum):
    """Dataset processing status"""
    UPLOADING = "uploading"
    UPLOADED = "uploaded"
    PROFILING = "profiling"
    PROFILED = "profiled"
    ERROR = "error"


class ColumnProfile(BaseModel):
    """Column-level profile (part of dataset profile response)"""
    column_name: str
    detected_type: str
    type_confidence: float
    statistics: Dict[str, Any]
    issues: List[Dict[str, Any]]


class DatasetProfileResponse(BaseModel):
    """Dataset profiling result"""
    profile_timestamp: str
    row_count: int
    column_count: int
    columns: List[ColumnProfile]
    issues: List[Dict[str, Any]]
    summary: Dict[str, Any]
    
    class Config:
        example = {
            "profile_timestamp": "2024-01-15T10:30:00",
            "row_count": 1000,
            "column_count": 5,
            "columns": [
                {
                    "column_name": "sales",
                    "detected_type": "numeric",
                    "type_confidence": 0.95,
                    "statistics": {
                        "count": 1000,
                        "null_count": 0,
                        "unique_count": 987,
                        "min": 10.0,
                        "max": 5000.0,
                        "mean": 1234.5,
                        "median": 1000.0,
                        "std": 500.0
                    },
                    "issues": []
                }
            ],
            "issues": [],
            "summary": {
                "total_issues": 0,
                "errors": 0,
                "warnings": 0,
                "data_quality_score": 95.0
            }
        }


class SemanticMetricResponse(BaseModel):
    """Auto-detected business metric"""
    column: str
    business_name: str
    aggregation: str  # sum, avg, count, min, max
    format: str  # currency, percentage, integer, decimal
    is_kpi: bool
    data_type: str


class SemanticDimensionResponse(BaseModel):
    """Auto-detected grouping field"""
    column: str
    business_name: str
    type: str  # categorical, geographic, temporal
    unique_count: int


class SemanticTimeDimensionResponse(BaseModel):
    """Auto-detected date field"""
    column: str
    business_name: str
    hierarchy: List[str]  # [year, month, day]


class SemanticLayerResponse(BaseModel):
    """Auto-generated semantic model"""
    metrics: List[SemanticMetricResponse]
    dimensions: List[SemanticDimensionResponse]
    time_dimensions: List[SemanticTimeDimensionResponse]
    metadata: Dict[str, Any]


class DatasetResponse(BaseModel):
    """Dataset response"""
    id: int
    project_id: int
    filename: str
    file_size: int
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    status: str
    error_message: Optional[str] = None
    created_at: str
    updated_at: str
    profile: Optional[DatasetProfileResponse] = None
    semantic_layer: Optional[SemanticLayerResponse] = None
    
    class Config:
        from_attributes = True
