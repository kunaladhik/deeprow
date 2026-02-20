"""
Data Profiler Module
Automatically detects column types and data characteristics
"""
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Any

class DataProfiler:
    """
    Analyzes data to understand:
    - Column types (numeric, categorical, date, text)
    - Value distributions
    - Missing data
    - KPI detection
    """
    
    KPI_KEYWORDS = [
        'sales', 'revenue', 'profit', 'cost', 'price',
        'quantity', 'qty', 'units', 'amount', 'value',
        'count', 'total', 'sum', 'income', 'expense'
    ]
    
    DATE_KEYWORDS = [
        'date', 'time', 'day', 'month', 'year', 'created', 'updated'
    ]
    
    @staticmethod
    def detect_column_type(series: pd.Series) -> str:
        """
        Detect column type
        
        Returns: 'numeric', 'date', 'categorical', 'text'
        """
        # Skip null values
        non_null = series.dropna()
        
        if len(non_null) == 0:
            return 'text'
        
        # Try numeric
        try:
            pd.to_numeric(non_null)
            return 'numeric'
        except (ValueError, TypeError):
            pass
        
        # Try datetime
        try:
            pd.to_datetime(non_null)
            return 'date'
        except (ValueError, TypeError):
            pass
        
        # Check cardinality for categorical vs text
        unique_ratio = len(non_null.unique()) / len(non_null)
        if unique_ratio < 0.05:  # Less than 5% unique values
            return 'categorical'
        
        return 'text'
    
    @staticmethod
    def profile_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate comprehensive data profile
        
        Returns:
        {
            'shape': (rows, cols),
            'columns': [
                {
                    'name': 'sales',
                    'type': 'numeric',
                    'is_kpi': true,
                    'null_count': 0,
                    'unique_count': 100,
                    'min': 100,
                    'max': 5000,
                    'mean': 2500
                },
                ...
            ],
            'row_count': 1000,
            'kpis': ['sales', 'revenue']
        }
        """
        profile = {
            'shape': df.shape,
            'row_count': len(df),
            'column_count': len(df.columns),
            'columns': [],
            'kpis': [],
            'date_columns': [],
            'categorical_columns': [],
            'numeric_columns': []
        }
        
        for col in df.columns:
            col_type = DataProfiler.detect_column_type(df[col])
            is_kpi = any(kpi in col.lower() for kpi in DataProfiler.KPI_KEYWORDS)
            is_date = any(date_kw in col.lower() for date_kw in DataProfiler.DATE_KEYWORDS)
            
            col_info = {
                'name': str(col),
                'type': col_type,
                'is_kpi': is_kpi,
                'is_date': is_date,
                'null_count': int(df[col].isna().sum()),
                'null_percentage': float(df[col].isna().sum() / len(df) * 100),
                'unique_count': int(df[col].nunique())
            }
            
            # Add type-specific stats
            if col_type == 'numeric':
                non_null = df[col].dropna()
                if len(non_null) > 0:
                    col_info['min'] = float(non_null.min())
                    col_info['max'] = float(non_null.max())
                    col_info['mean'] = float(non_null.mean())
                    col_info['median'] = float(non_null.median())
                    col_info['std'] = float(non_null.std())
                profile['numeric_columns'].append(col)
            
            elif col_type == 'categorical':
                col_info['categories'] = df[col].dropna().unique().tolist()[:10]
                profile['categorical_columns'].append(col)
            
            elif col_type == 'date':
                profile['date_columns'].append(col)
            
            profile['columns'].append(col_info)
            
            if is_kpi:
                profile['kpis'].append(col)
        
        return profile
