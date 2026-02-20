"""
Visualization Template Generator
Automatically creates chart templates based on data
"""
from typing import Dict, List, Any

class TemplateGenerator:
    """
    Generates visualization templates for:
    - Bar charts
    - Line charts
    - Pie charts
    - Tables
    - KPI cards
    """
    
    @staticmethod
    def generate_kpi_card(
        label: str,
        value: float,
        unit: str = '',
        trend: str = 'neutral'
    ) -> Dict[str, Any]:
        """Generate KPI card template"""
        return {
            'type': 'kpi_card',
            'label': label,
            'value': value,
            'unit': unit,
            'trend': trend  # 'up', 'down', 'neutral'
        }
    
    @staticmethod
    def generate_bar_chart(
        data: List[Dict],
        x_field: str,
        y_field: str,
        title: str = ''
    ) -> Dict[str, Any]:
        """Generate bar chart template"""
        return {
            'type': 'bar_chart',
            'title': title,
            'x_axis': x_field,
            'y_axis': y_field,
            'data': data
        }
    
    @staticmethod
    def generate_line_chart(
        data: List[Dict],
        x_field: str,
        y_field: str,
        title: str = ''
    ) -> Dict[str, Any]:
        """Generate line chart template"""
        return {
            'type': 'line_chart',
            'title': title,
            'x_axis': x_field,
            'y_axis': y_field,
            'data': data
        }
    
    @staticmethod
    def generate_pie_chart(
        data: List[Dict],
        label_field: str,
        value_field: str,
        title: str = ''
    ) -> Dict[str, Any]:
        """Generate pie chart template"""
        return {
            'type': 'pie_chart',
            'title': title,
            'labels': label_field,
            'values': value_field,
            'data': data
        }
    
    @staticmethod
    def generate_distribution_chart(
        distribution: Dict
    ) -> Dict[str, Any]:
        """Generate histogram from distribution data"""
        return {
            'type': 'histogram',
            'title': f'Distribution of {distribution["column"]}',
            'data': distribution.get('bins', distribution.get('values', []))
        }
    
    @staticmethod
    def auto_generate_templates(
        profile: Dict,
        insights: Dict
    ) -> List[Dict[str, Any]]:
        """
        Automatically generate recommended visualizations
        based on data profile and insights
        """
        templates = []
        
        # KPI Cards for each KPI
        kpis = profile.get('kpis', [])
        if len(kpis) > 0:
            for kpi in kpis[:3]:  # Top 3 KPIs
                if kpi in insights.get('aggregations', {}).get('summary', {}):
                    agg = insights['aggregations']['summary'][kpi]
                    templates.append(
                        TemplateGenerator.generate_kpi_card(
                            label=kpi.title(),
                            value=agg.get('sum', 0)
                        )
                    )
        
        # Bar chart for categorical vs numeric
        numeric_cols = profile.get('numeric_columns', [])
        categorical_cols = profile.get('categorical_columns', [])
        
        if numeric_cols and categorical_cols:
            # Create a sample bar chart structure
            templates.append({
                'type': 'bar_chart',
                'title': f'{numeric_cols[0].title()} by {categorical_cols[0].title()}',
                'x_axis': categorical_cols[0],
                'y_axis': numeric_cols[0],
                'data': insights.get('aggregations', {}).get('by_group', {}).get(numeric_cols[0], [])
            })
        
        # Distribution charts
        for col, dist in insights.get('distributions', {}).items():
            templates.append(
                TemplateGenerator.generate_distribution_chart(dist)
            )
        
        # Trend chart if we have date data
        if profile.get('date_columns') and numeric_cols:
            templates.append({
                'type': 'line_chart',
                'title': f'{numeric_cols[0].title()} Over Time',
                'x_axis': profile['date_columns'][0],
                'y_axis': numeric_cols[0],
                'data': insights.get('trends', {}).get(numeric_cols[0], [])
            })
        
        return templates
