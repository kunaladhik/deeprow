"""
Dataset and file upload routes

POST /api/projects/{id}/upload - Upload CSV/Excel file
GET /api/projects/{id}/dataset - Get dataset with profiling results

This is where raw data becomes semantic understanding.
"""

import os
import io
from fastapi import APIRouter, Depends, HTTPException, status, Header, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime
import pandas as pd

from app.core.database import get_db
from app.core.security import decode_token
from app.models.models import User, Project, Dataset, DatasetProfile
from app.engines.profiler import DataProfiler
from app.engines.semantic_engine import SemanticLayerEngine
from app.schemas.projects import ProjectResponse, DatasetResponse, DatasetProfileResponse
from app.schemas.projects import SemanticLayerResponse, ColumnProfile

router = APIRouter(prefix="/api/datasets", tags=["datasets"])


def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)) -> User:
    """Extract user from Authorization header"""
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token required")
    
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth header")
    
    try:
        user_id = decode_token(parts[1])
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user


def parse_upload_file(file: UploadFile, max_size_mb: int = 50) -> pd.DataFrame:
    """
    Parse uploaded CSV/Excel file
    
    Constraints:
    - Max 50MB
    - CSV or Excel format only
    - UTF-8 encoding
    
    Raises HTTPException on invalid format
    """
    
    # Check file size
    file_size = len(file.file.read())
    file.file.seek(0)
    
    if file_size > max_size_mb * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds {max_size_mb}MB limit"
        )
    
    # Check file format
    filename = file.filename.lower()
    
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(file.file, encoding='utf-8', on_bad_lines='warn')
        elif filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file.file)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file format. Please use CSV or Excel."
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to parse file: {str(e)}"
        )
    
    # Validate data
    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty"
        )
    
    if len(df.columns) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File has no columns"
        )
    
    return df


@router.post("/upload/{project_id}")
async def upload_dataset(
    project_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload CSV or Excel file to a project
    
    Steps:
    1. Validate file (format, size, encoding)
    2. Parse into DataFrame
    3. Store in database
    4. Profile columns (auto-detection)
    5. Generate semantic layer (auto-generate metrics/dimensions)
    6. Return results to user
    
    Non-technical user just uploads file. System handles everything.
    """
    
    # 1. Verify project ownership
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied"
        )
    
    # 2. Parse file
    try:
        df = parse_upload_file(file)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File processing error: {str(e)}"
        )
    
    # 3. Create dataset record
    dataset = Dataset(
        project_id=project_id,
        filename=file.filename,
        file_size=len(file.file.read() or b''),
        row_count=len(df),
        column_count=len(df.columns),
        status="uploaded",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(dataset)
    db.flush()  # Get dataset.id without committing yet
    
    # 4. Profile dataset
    try:
        profiler = DataProfiler()
        profile = profiler.profile_dataset(df)
        
        # Store column profiles
        for col_profile in profile['columns']:
            profile_record = DatasetProfile(
                dataset_id=dataset.id,
                column_name=col_profile['column_name'],
                detected_type=col_profile['detected_type'],
                type_confidence=col_profile['type_confidence'],
                statistics=col_profile['statistics'],
                issues=col_profile['issues']
            )
            db.add(profile_record)
        
        dataset.status = "profiled"
    except Exception as e:
        dataset.status = "error"
        dataset.error_message = f"Profiling failed: {str(e)}"
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Data profiling failed"
        )
    
    # 5. Generate semantic layer
    try:
        profiles = profile['columns']
        semantic = SemanticLayerEngine.generate_semantics(
            df, profiles, len(df)
        )
    except Exception as e:
        semantic = {
            'metrics': [],
            'dimensions': [],
            'time_dimensions': [],
            'metadata': {'error': str(e)}
        }
    
    db.commit()
    db.refresh(dataset)
    
    # 6. Return comprehensive response
    return {
        "dataset_id": dataset.id,
        "filename": dataset.filename,
        "row_count": dataset.row_count,
        "column_count": dataset.column_count,
        "status": dataset.status,
        "profile": profile,
        "semantic_layer": semantic
    }


@router.get("/{dataset_id}")
async def get_dataset(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get dataset with full profiling results and semantic layer
    
    User sees:
    - File metadata (name, row count, column count)
    - Column analysis (type, nulls, unique values, issues)
    - Auto-detected metrics/dimensions
    - Data quality score
    """
    
    # Verify access
    dataset = db.query(Dataset).join(Project).filter(
        Dataset.id == dataset_id,
        Project.user_id == current_user.id
    ).first()
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found or access denied"
        )
    
    # Get profiles
    profiles = db.query(DatasetProfile).filter(
        DatasetProfile.dataset_id == dataset_id
    ).all()
    
    profile_data = {
        'profile_timestamp': datetime.utcnow().isoformat(),
        'row_count': dataset.row_count,
        'column_count': dataset.column_count,
        'columns': [
            {
                'column_name': p.column_name,
                'detected_type': p.detected_type,
                'type_confidence': p.type_confidence,
                'statistics': p.statistics,
                'issues': p.issues
            }
            for p in profiles
        ],
        'issues': [issue for p in profiles for issue in p.issues],
        'summary': {
            'total_issues': sum(len(p.issues) for p in profiles),
            'data_quality_score': 85.0  # TODO: calculate from profiles
        }
    }
    
    return {
        'id': dataset.id,
        'project_id': dataset.project_id,
        'filename': dataset.filename,
        'file_size': dataset.file_size,
        'row_count': dataset.row_count,
        'column_count': dataset.column_count,
        'status': dataset.status,
        'created_at': dataset.created_at.isoformat(),
        'updated_at': dataset.updated_at.isoformat(),
        'profile': profile_data
    }
