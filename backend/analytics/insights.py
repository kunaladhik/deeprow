"""
Analytics & Insights Engine
Generates aggregations, trends, comparisons, and distributions
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any

class InsightsEngine:
    """
    Generates analytics:
    - Aggregations (sum, count, average)
    - Trends (over time)
    - Comparisons (by category)
    - Distributions (histograms)
    """
    
    @staticmethod
    def generate_aggregations(
        df: pd.DataFrame,
        numeric_cols: List[str],
        group_by: str = None
    ) -> Dict[str, Any]:
        """
        Generate summary statistics and aggregations
        """
        aggregations = {
            'summary': {},
            'by_group': {}
        }
        
        # Overall summary
        for col in numeric_cols:
            if col in df.columns:
                non_null = df[col].dropna()
                if len(non_null) > 0:
                    aggregations['summary'][col] = {
                        'sum': float(non_null.sum()),
                        'count': int(len(non_null)),
                        'average': float(non_null.mean()),
                        'min': float(non_null.min()),
                        'max': float(non_null.max()),
                        'median': float(non_null.median())
                    }
        
        # Group by analysis
        if group_by and group_by in df.columns:
            try:
                for col in numeric_cols:
                    if col in df.columns:
                        grouped = df.groupby(group_by)[col].agg(['sum', 'count', 'mean']).reset_index()
                        aggregations['by_group'][col] = grouped.to_dict('records')
            except Exception as e:
                pass
        
        return aggregations
    
    @staticmethod
    def detect_trends(
        df: pd.DataFrame,
        date_col: str,
        numeric_cols: List[str]
    ) -> Dict[str, List[Dict]]:
        """
        Detect trends over time
        """
        trends = {}
        
        if date_col not in df.columns:
            return trends
        
        try:
            df_sorted = df.copy()
            df_sorted[date_col] = pd.to_datetime(df_sorted[date_col])
            df_sorted = df_sorted.sort_values(date_col)
            
            for col in numeric_cols:
                if col in df.columns:
                    # Group by date and aggregate
                    trend_data = df_sorted.groupby(date_col)[col].sum().reset_index()
                    trends[col] = trend_data.to_dict('records')
        except Exception as e:
            pass
        
        return trends
    
    @staticmethod
    def generate_distribution(
        df: pd.DataFrame,
        column: str,
        bins: int = 10
    ) -> Dict[str, Any]:
        """
        Generate histogram/distribution data
        """
        distribution = {
            'column': column,
            'bins': [],
            'values': []
        }
        
        try:
            data = df[column].dropna()
            if len(data) > 0:
                if pd.api.types.is_numeric_dtype(data):
                    counts, bin_edges = np.histogram(data, bins=bins)
                    for i in range(len(counts)):
                        distribution['bins'].append({
                            'min': float(bin_edges[i]),
                            'max': float(bin_edges[i + 1]),
                            'count': int(counts[i])
                        })
                else:
                    # For categorical
                    value_counts = data.value_counts().head(10)
                    distribution['values'] = [
                        {'category': str(cat), 'count': int(count)}
                        for cat, count in value_counts.items()
                    ]
        except Exception as e:
            pass
        
        return distribution
    
    @staticmethod
    def generate_all_insights(
        df: pd.DataFrame,
        profile: Dict
    ) -> Dict[str, Any]:
        """
        Generate comprehensive insights
        """
        numeric_cols = profile.get('numeric_columns', [])
        date_cols = profile.get('date_columns', [])
        
        insights = {
            'aggregations': InsightsEngine.generate_aggregations(df, numeric_cols),
            'distributions': {},
            'trends': {}
        }
        
        # Distributions for numeric columns
        for col in numeric_cols[:5]:  # Limit to first 5
            insights['distributions'][col] = InsightsEngine.generate_distribution(df, col)
        
        # Trends if we have date column
        if date_cols:
            date_col = date_cols[0]
            insights['trends'] = InsightsEngine.detect_trends(df, date_col, numeric_cols)
        
        return insights
