"""
Data Loader Module for Indian E-commerce Product Catalog

Handles loading, validating, and preparing product data.
Supports CSV imports and data cleaning for AI procurement platform.

Author: AI Procurement Platform Team
Date: February 2026
"""

import pandas as pd
import os
from typing import Optional, List, Dict
from pathlib import Path


class IndianEcommerceCatalogLoader:
    """
    Loads and processes Indian e-commerce product catalogs.
    Supports CSV data and provides data validation and cleaning.
    """

    def __init__(self, csv_path: str):
        """
        Initialize loader.
        
        Args:
            csv_path: Path to CSV file
        """
        self.csv_path = csv_path
        self.df = None
        self.original_df = None
        self._load_and_validate()

    def _load_and_validate(self) -> None:
        """Load and validate data"""
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
        
        try:
            self.df = pd.read_csv(self.csv_path)
            self.original_df = self.df.copy()
            
            # Validate required columns
            required_cols = [
                "product_id", "product_name", "category", "subcategory",
                "brand", "supplier_name", "mrp", "selling_price",
                "pack_size", "unit"
            ]
            
            missing_cols = [col for col in required_cols if col not in self.df.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
            
            # Clean and prepare data
            self._clean_data()
            
        except Exception as e:
            raise Exception(f"Error loading CSV: {str(e)}")

    def _clean_data(self) -> None:
        """Clean and prepare data"""
        # Convert numeric columns
        self.df["product_id"] = pd.to_numeric(self.df["product_id"], errors="coerce").astype(int)
        self.df["mrp"] = pd.to_numeric(self.df["mrp"], errors="coerce")
        self.df["selling_price"] = pd.to_numeric(self.df["selling_price"], errors="coerce")
        self.df["pack_size"] = pd.to_numeric(self.df["pack_size"], errors="coerce")
        
        # Remove rows with missing required values
        self.df = self.df.dropna(subset=["product_id", "selling_price", "mrp"])
        
        # Strip whitespace from string columns
        string_cols = self.df.select_dtypes(include=['object']).columns
        for col in string_cols:
            self.df[col] = self.df[col].str.strip()

    def get_dataframe(self) -> pd.DataFrame:
        """Get processed dataframe"""
        return self.df.copy()

    def get_summary(self) -> Dict:
        """Get data summary"""
        return {
            "total_records": len(self.df),
            "unique_products": self.df["product_id"].nunique(),
            "suppliers": self.df["supplier_name"].nunique(),
            "categories": self.df["category"].nunique(),
            "brands": self.df["brand"].nunique(),
            "date_loaded": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def filter_by_category(self, category: str) -> pd.DataFrame:
        """Filter data by category"""
        return self.df[self.df["category"] == category]

    def export_processed(self, output_path: str) -> None:
        """Export processed data"""
        self.df.to_csv(output_path, index=False)

    def get_data_quality_report(self) -> Dict:
        """Generate data quality report"""
        return {
            "total_rows": len(self.df),
            "complete_rows": self.df.dropna().shape[0],
            "missing_values": self.df.isnull().sum().to_dict(),
            "duplicate_records": self.df.duplicated().sum(),
            "numeric_columns_stats": self.df[["mrp", "selling_price", "pack_size"]].describe().to_dict()
        }


class KaggleDatasetGuide:
    """
    Guide for integrating Kaggle datasets into the procurement platform.
    Provides standardization and transformation utilities.
    """

    @staticmethod
    def recommended_kaggle_datasets() -> List[Dict]:
        """
        List of recommended Kaggle datasets for Indian grocery/FMCG.
        
        Returns:
            List of dataset recommendations
        """
        return [
            {
                "name": "Indian Grocery Store Dataset",
                "url": "https://www.kaggle.com/datasets/",
                "columns_map": {
                    "product_name": "Name",
                    "category": "Category",
                    "mrp": "MRP",
                    "selling_price": "Price"
                },
                "description": "Comprehensive Indian grocery product dataset"
            },
            {
                "name": "E-commerce Product Catalog",
                "url": "https://www.kaggle.com/datasets/",
                "columns_map": {
                    "product_name": "product_title",
                    "selling_price": "product_price"
                },
                "description": "Multi-category e-commerce product data"
            }
        ]

    @staticmethod
    def standardize_kaggle_data(df: pd.DataFrame, column_mapping: Dict[str, str]) -> pd.DataFrame:
        """
        Standardize Kaggle dataset to platform format.
        
        Args:
            df: Raw Kaggle dataframe
            column_mapping: Mapping of platform columns to Kaggle columns
            
        Returns:
            Standardized dataframe
        """
        standardized = pd.DataFrame()
        
        for platform_col, kaggle_col in column_mapping.items():
            if kaggle_col in df.columns:
                standardized[platform_col] = df[kaggle_col]
        
        # Add default columns if missing
        if "product_id" not in standardized.columns:
            standardized["product_id"] = range(1, len(standardized) + 1)
        
        if "category" not in standardized.columns:
            standardized["category"] = "Uncategorized"
        
        return standardized

    @staticmethod
    def get_import_instructions() -> str:
        """Get step-by-step instructions for importing Kaggle data"""
        return """
        KAGGLE DATASET INTEGRATION GUIDE
        =================================
        
        Steps to integrate Kaggle datasets:
        
        1. DOWNLOAD DATASET
           - Visit https://www.kaggle.com
           - Search for Indian grocery or FMCG dataset
           - Download CSV file
        
        2. PLACE IN PROJECT
           - Copy CSV to: data/kaggle_import.csv
        
        3. PREPARE COLUMNS
           - Ensure CSV has: product_name, category, price, brand
           - Add missing columns with default values
        
        4. CLEAN DATA
           - Remove duplicates
           - Handle missing values
           - Standardize formatting
        
        5. MAP TO PLATFORM
           - Use KaggleDatasetGuide.standardize_kaggle_data()
           - Provide column mapping dictionary
        
        6. LOAD & VALIDATE
           - CSV will auto-load on application startup
           - Check data quality report in UI
        
        RECOMMENDED DATASETS:
        - Indian Grocery Store Dataset
        - E-commerce Grocery Products
        - Indian FMCG Product Pricing
        
        REQUIRED COLUMNS (MINIMUM):
        - product_name: Product name
        - category: Product category
        - selling_price: Current selling price
        - supplier_name: Where product is sold
        
        OPTIONAL COLUMNS:
        - mrp: Maximum retail price
        - brand: Product brand
        - pack_size: Size of package
        - unit: Unit of measurement
        """
