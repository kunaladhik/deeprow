"""
SEMANTIC LAYER ENGINE

This is the core intelligence that makes the platform domain-agnostic.
It automatically detects:
1. Metrics (numeric measures)
2. Dimensions (categorical grouping fields)
3. Time dimensions (date hierarchies)

Without this, the platform is just another BI tool.
With this, it's an intelligence layer.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime

class SemanticLayerEngine:
    """Detects metrics, dimensions, time fields automatically"""
    
    # Keywords for business naming
    METRIC_KEYWORDS = {
        'amount', 'revenue', 'sales', 'total', 'sum', 'count',
        'qty', 'quantity', 'cost', 'price', 'value', 'rate',
        'profit', 'margin', 'income', 'expense', 'balance',
        'minutes', 'hours', 'duration', 'length', 'weight',
        'temperature', 'score', 'rating', 'percentage'
    }
    
    TIME_KEYWORDS = {
        'date', 'time', 'datetime', 'created', 'updated',
        'posted', 'published', 'day', 'month', 'year',
        'timestamp', 'dt', '_date', '_time', '_at'
    }
    
    CATEGORICAL_KEYWORDS = {
        'region', 'country', 'state', 'city', 'area',
        'category', 'type', 'status', 'class', 'group',
        'name', 'id', 'code', 'label', 'tag', 'bucket'
    }
    
    @staticmethod
    def humanize_name(column_name: str) -> str:
        """
        Convert snake_case/camelCase to Title Case
        
        Examples:
        - sales_amount → Sales Amount
        - order_dt → Order Date
        - customer_id → Customer
        - total_revenue → Total Revenue
        """
        # Handle special suffixes
        cleaned = column_name
        cleaned = cleaned.replace('_dt', ' Date')
        cleaned = cleaned.replace('_id', '')
        cleaned = cleaned.replace('_ts', ' Timestamp')
        cleaned = cleaned.replace('_at', ' Date')
        
        # Convert snake_case to Title Case
        words = cleaned.split('_')
        return ' '.join(word.capitalize() for word in words if word)
    
    @staticmethod
    def detect_metric_aggregation(column_name: str, data_type: str) -> str:
        """Suggest aggregation for a metric"""
        if 'count' in column_name.lower() or 'qty' in column_name.lower():
            return 'sum'
        if 'avg' in column_name.lower() or 'average' in column_name.lower():
            return 'avg'
        if data_type == 'numeric':
            return 'sum'
        return 'sum'
    
    @staticmethod
    def detect_format_type(column_name: str, data_type: str) -> str:
        """Suggest format (currency, percentage, etc.)"""
        col_lower = column_name.lower()
        
        if any(kw in col_lower for kw in ['revenue', 'sales', 'amount', 'cost', 'price', 'profit']):
            return 'currency'
        if any(kw in col_lower for kw in ['percentage', 'percent', 'ratio', 'rate']):
            return 'percentage'
        if 'count' in col_lower or 'qty' in col_lower or 'quantity' in col_lower:
            return 'integer'
        
        return 'decimal'
    
    @staticmethod
    def is_likely_metric(column_name: str, data_type: str, unique_count: int, row_count: int) -> bool:
        """
        Determine if a column is a metric (numeric measure)
        
        Rules:
        - Must be numeric
        - Should not be ID (cardinality close to row_count)
        - Match metric keywords
        """
        if data_type != 'numeric':
            return False
        
        col_lower = column_name.lower()
        
        # Strong metric signal
        if any(kw in col_lower for kw in SemanticLayerEngine.METRIC_KEYWORDS):
            return True
        
        # Avoid IDs and high-cardinality columns
        cardinality_ratio = unique_count / max(row_count, 1)
        if cardinality_ratio > 0.8:  # Almost all unique
            return False
        
        return True
    
    @staticmethod
    def is_likely_dimension(column_name: str, data_type: str, unique_count: int, row_count: int) -> bool:
        """
        Determine if a column is a dimension (categorical/grouping field)
        
        Rules:
        - Should be low cardinality (<50 unique values)
        - Match dimension keywords
        - NOT numeric (unless it's a code)
        """
        col_lower = column_name.lower()
        
        # ID columns are problematic
        if '_id' in col_lower:
            return False
        
        # Low cardinality = dimension candidate
        cardinality_ratio = unique_count / max(row_count, 1)
        
        # Strong dimension signal
        if any(kw in col_lower for kw in SemanticLayerEngine.CATEGORICAL_KEYWORDS):
            if unique_count <= 1000:  # Reasonable dimension size
                return True
        
        # Generic low-cardinality categorical
        if data_type == 'categorical' and unique_count <= 100:
            return True
        
        return False
    
    @staticmethod
    def is_likely_time_dimension(column_name: str, data_type: str) -> bool:
        """
        Determine if a column is a time dimension
        
        Rules:
        - Must be date type
        - Match time keywords
        """
        if data_type != 'date':
            return False
        
        col_lower = column_name.lower()
        
        # Check time keywords
        if any(kw in col_lower for kw in SemanticLayerEngine.TIME_KEYWORDS):
            return True
        
        return True  # All dates are time dimensions
    
    @classmethod
    def generate_semantics(
        cls,
        df: pd.DataFrame,
        profiles: List[Dict[str, Any]],
        dataset_row_count: int
    ) -> Dict[str, Any]:
        """
        Main method: Generate complete semantic model
        
        returns:
        {
            'metrics': [
                {
                    'column': 'sales',
                    'business_name': 'Sales Amount',
                    'aggregation': 'sum',
                    'format': 'currency',
                    'is_kpi': True
                },
                ...
            ],
            'dimensions': [
                {
                    'column': 'region',
                    'business_name': 'Region',
                    'type': 'categorical'
                },
                ...
            ],
            'time_dimensions': [
                {
                    'column': 'order_date',
                    'business_name': 'Order Date',
                    'hierarchy': ['year', 'month', 'day']
                }
            ]
        }
        """
        metrics = []
        dimensions = []
        time_dimensions = []
        
        for profile in profiles:
            col_name = profile['column_name']
            data_type = profile['detected_type']
            unique_count = profile['unique_count']
            
            # Try time dimension first (highest priority)
            if cls.is_likely_time_dimension(col_name, data_type):
                time_dimensions.append({
                    'column': col_name,
                    'business_name': cls.humanize_name(col_name),
                    'hierarchy': ['year', 'month', 'day']
                })
            
            # Then try metric
            elif cls.is_likely_metric(col_name, data_type, unique_count, dataset_row_count):
                is_kpi = any(kw in col_name.lower() for kw in [
                    'revenue', 'sales', 'profit', 'quantity'
                ])
                
                metrics.append({
                    'column': col_name,
                    'business_name': cls.humanize_name(col_name),
                    'aggregation': cls.detect_metric_aggregation(col_name, data_type),
                    'format': cls.detect_format_type(col_name, data_type),
                    'is_kpi': is_kpi,
                    'data_type': data_type
                })
            
            # Finally try dimension
            elif cls.is_likely_dimension(col_name, data_type, unique_count, dataset_row_count):
                dimensions.append({
                    'column': col_name,
                    'business_name': cls.humanize_name(col_name),
                    'type': 'categorical',
                    'unique_count': unique_count
                })
        
        return {
            'metrics': metrics,
            'dimensions': dimensions,
            'time_dimensions': time_dimensions,
            'metadata': {
                'user_input_needed': len(metrics) == 0 and len(dimensions) == 0,
                'confidence': cls._calculate_confidence(metrics, dimensions, time_dimensions)
            }
        }
    
    @staticmethod
    def _calculate_confidence(metrics: List, dimensions: List, time_dims: List) -> float:
        """
        Calculate confidence in semantic detection
        
        Returns 0-1 score
        """
        total_fields = len(metrics) + len(dimensions) + len(time_dims)
        
        if total_fields == 0:
            return 0.0
        
        # More dimensions/time = higher confidence
        dimension_score = (len(dimensions) + len(time_dims)) / max(total_fields, 1)
        
        # At least one metric and dimension = good
        has_metrics = len(metrics) > 0
        has_dimensions = len(dimensions) + len(time_dims) > 0
        
        structure_score = 0.5 if (has_metrics and has_dimensions) else 0.3
        
        return (dimension_score * 0.7) + structure_score * 0.3
