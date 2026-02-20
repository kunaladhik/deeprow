"""
Data Loader Module
Handles CSV and Excel file loading
"""
import pandas as pd
import io
from typing import Tuple

class DataLoader:
    """Load and parse CSV and Excel files"""
    
    @staticmethod
    def load_csv(file_content: bytes) -> pd.DataFrame:
        """Load CSV file"""
        try:
            df = pd.read_csv(io.BytesIO(file_content))
            return df
        except Exception as e:
            raise ValueError(f"Error loading CSV: {str(e)}")
    
    @staticmethod
    def load_excel(file_content: bytes) -> pd.DataFrame:
        """Load Excel file"""
        try:
            df = pd.read_excel(io.BytesIO(file_content))
            return df
        except Exception as e:
            raise ValueError(f"Error loading Excel: {str(e)}")
    
    @staticmethod
    def load_file(file_content: bytes, filename: str) -> pd.DataFrame:
        """
        Auto-detect file type and load
        
        Args:
            file_content: Raw file bytes
            filename: Original filename with extension
            
        Returns:
            Loaded DataFrame
        """
        filename_lower = filename.lower()
        
        if filename_lower.endswith('.csv'):
            return DataLoader.load_csv(file_content)
        elif filename_lower.endswith(('.xlsx', '.xls')):
            return DataLoader.load_excel(file_content)
        else:
            raise ValueError(f"Unsupported file type: {filename}")
