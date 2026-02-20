"""
DATA PROFILING ENGINE

Analyzes each column:
- Detects type (numeric, categorical, date, text)
- Calculates statistics (nulls, unique count, min/max/mean/median/std)
- Detects issues (duplicates, outliers, mixed types)
- Provides confidence scores

This runs automatically after file upload.
User reviews the results before proceeding.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')


class DataProfiler:
    """Auto-profile uploaded datasets"""
    
    @staticmethod
    def detect_column_type(series: pd.Series, name: str) -> Tuple[str, float]:
        """
        Detect column type with confidence score
        
        Returns:
        - 'numeric', 'categorical', 'date', or 'text'
        - confidence score 0-1
        """
        # Try to infer type, skipping nulls
        non_null = series.dropna()
        
        if len(non_null) == 0:
            return 'unknown', 0.0
        
        # Check if numeric
        try:
            pd.to_numeric(series, errors='coerce')
            numeric_count = pd.to_numeric(series, errors='coerce').notna().sum()
            numeric_ratio = numeric_count / len(non_null)
            
            if numeric_ratio > 0.95:  # 95%+ can be converted to numeric
                return 'numeric', 0.95
        except:
            pass
        
        # Check if date
        try:
            pd.to_datetime(series, errors='coerce')
            date_count = pd.to_datetime(series, errors='coerce').notna().sum()
            date_ratio = date_count / len(non_null)
            
            if date_ratio > 0.90:  # 90%+ can be converted to date
                return 'date', 0.90
        except:
            pass
        
        # Check if categorical (low cardinality)
        unique_ratio = series.nunique() / len(non_null)
        
        if unique_ratio < 0.05:  # <5% unique = likely categorical
            return 'categorical', 0.9
        
        # Default to text
        return 'text', 0.6
    
    @staticmethod
    def detect_issues(series: pd.Series, col_type: str) -> List[Dict[str, Any]]:
        """Detect data quality issues in a column"""
        issues = []
        
        # 1. Missing values
        null_count = series.isna().sum()
        null_pct = (null_count / len(series)) * 100
        
        if null_count > 0:
            issues.append({
                'type': 'missing_values',
                'severity': 'warn' if null_pct < 50 else 'error',
                'count': int(null_count),
                'percentage': round(null_pct, 2),
                'message': f'{null_pct:.1f}% of values are missing'
            })
        
        # 2. Duplicates
        dup_count = series.duplicated().sum()
        dup_pct = (dup_count / len(series)) * 100
        
        if dup_count > 0:
            issues.append({
                'type': 'duplicates',
                'severity': 'warn' if dup_pct < 10 else 'error',
                'count': int(dup_count),
                'percentage': round(dup_pct, 2),
                'message': f'{dup_pct:.1f}% of values are duplicated'
            })
        
        # 3. For numeric columns: outliers
        if col_type == 'numeric':
            non_null = pd.to_numeric(series, errors='coerce').dropna()
            
            if len(non_null) > 0:
                Q1 = non_null.quantile(0.25)
                Q3 = non_null.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outlier_count = ((non_null < lower_bound) | (non_null > upper_bound)).sum()
                outlier_pct = (outlier_count / len(non_null)) * 100
                
                if outlier_count > 0:
                    issues.append({
                        'type': 'outliers',
                        'severity': 'info',
                        'count': int(outlier_count),
                        'percentage': round(outlier_pct, 2),
                        'message': f'{outlier_pct:.1f}% of values are statistical outliers'
                    })
        
        # 4. For mixed types: conflicting types
        if col_type == 'numeric':
            try:
                numeric = pd.to_numeric(series, errors='coerce')
                numeric_valid = numeric.notna().sum()
                non_null_valid = series.notna().sum()
                
                if numeric_valid < non_null_valid * 0.99:
                    issues.append({
                        'type': 'mixed_types',
                        'severity': 'warn',
                        'count': int(non_null_valid - numeric_valid),
                        'message': 'Column contains non-numeric values'
                    })
            except:
                pass
        
        return issues
    
    @staticmethod
    def calculate_statistics(series: pd.Series, col_type: str) -> Dict[str, Any]:
        """Calculate descriptive statistics"""
        stats = {
            'count': int(series.notna().sum()),
            'null_count': int(series.isna().sum()),
            'unique_count': int(series.nunique()),
            'data_type': col_type
        }
        
        if col_type == 'numeric':
            numeric_series = pd.to_numeric(series, errors='coerce')
            
            stats.update({
                'min': float(numeric_series.min()) if not numeric_series.empty else None,
                'max': float(numeric_series.max()) if not numeric_series.empty else None,
                'mean': float(numeric_series.mean()) if not numeric_series.empty else None,
                'median': float(numeric_series.median()) if not numeric_series.empty else None,
                'std': float(numeric_series.std()) if not numeric_series.empty else None
            })
        
        elif col_type == 'categorical':
            # Top 5 categories
            top_categories = series.value_counts().head(5)
            stats['top_values'] = [
                {'value': str(k), 'count': int(v)}
                for k, v in top_categories.items()
            ]
        
        elif col_type == 'date':
            date_series = pd.to_datetime(series, errors='coerce')
            stats['earliest'] = str(date_series.min())
            stats['latest'] = str(date_series.max())
        
        return stats
    
    @classmethod
    def profile_dataset(cls, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Complete dataset profiling
        
        Returns comprehensive profile with column-level analysis
        """
        profiles = []
        all_issues = []
        
        for col_name in df.columns:
            series = df[col_name]
            
            # 1. Detect type
            col_type, confidence = cls.detect_column_type(series, col_name)
            
            # 2. Detect issues
            issues = cls.detect_issues(series, col_type)
            all_issues.extend([
                {**issue, 'column': col_name}
                for issue in issues
            ])
            
            # 3. Calculate statistics
            stats = cls.calculate_statistics(series, col_type)
            
            profile = {
                'column_name': col_name,
                'detected_type': col_type,
                'type_confidence': round(confidence, 2),
                'statistics': stats,
                'issues': issues
            }
            
            profiles.append(profile)
        
        # Summary
        issue_count = len(all_issues)
        error_count = len([i for i in all_issues if i['severity'] == 'error'])
        
        return {
            'profile_timestamp': datetime.utcnow().isoformat(),
            'row_count': len(df),
            'column_count': len(df.columns),
            'columns': profiles,
            'issues': all_issues,
            'summary': {
                'total_issues': issue_count,
                'errors': error_count,
                'warnings': len([i for i in all_issues if i['severity'] == 'warn']),
                'data_quality_score': cls._calculate_quality_score(profiles, all_issues)
            }
        }
    
    @staticmethod
    def _calculate_quality_score(profiles: List[Dict], issues: List[Dict]) -> float:
        """
        Calculate overall data quality score (0-100)
        
        Factors:
        - Type detection confidence
        - Number of issues
        - Severity of issues
        """
        # Start at 100
        score = 100.0
        
        # Penalize low type confidence
        avg_confidence = np.mean([p['type_confidence'] for p in profiles]) if profiles else 0
        confidence_penalty = (1 - avg_confidence) * 10
        score -= confidence_penalty
        
        # Penalize issues
        for issue in issues:
            if issue['severity'] == 'error':
                score -= 5
            elif issue['severity'] == 'warn':
                score -= 2
            elif issue['severity'] == 'info':
                score -= 0.5
        
        return max(0, min(100, score))  # Clamp to 0-100
