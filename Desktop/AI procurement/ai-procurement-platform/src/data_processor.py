"""
Data Processing Module

This module handles loading, filtering, and transforming procurement data.
It provides utilities for working with CSV data and preparing it for analysis.

Future phases can replace CSV with database operations.
"""

import pandas as pd
from typing import Dict, List, Tuple
import os


class ProcurementDataLoader:
    """
    Handles loading and caching procurement data from CSV files.
    """
    
    def __init__(self, csv_path: str):
        """
        Initialize the data loader.
        
        Args:
            csv_path: Path to the CSV file containing procurement data
        """
        self.csv_path = csv_path
        self.df = None
        self.load_data()
    
    def load_data(self) -> pd.DataFrame:
        """
        Load data from CSV file.
        
        Returns:
            DataFrame with procurement data
            
        Raises:
            FileNotFoundError: If CSV file doesn't exist
            ValueError: If CSV format is invalid
        """
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"Data file not found: {self.csv_path}")
        
        try:
            self.df = pd.read_csv(self.csv_path)
            
            # Validate required columns
            required_columns = [
                'item_id', 'item_name', 'supplier_id', 'supplier_name',
                'unit_price', 'stock_level', 'demand_level', 'last_updated'
            ]
            
            missing_columns = set(required_columns) - set(self.df.columns)
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Convert data types
            self.df['unit_price'] = pd.to_numeric(self.df['unit_price'], errors='coerce')
            self.df['stock_level'] = pd.to_numeric(self.df['stock_level'], errors='coerce')
            
            return self.df
        except Exception as e:
            raise ValueError(f"Error loading CSV file: {str(e)}")
    
    def get_all_items(self) -> List[Tuple[int, str]]:
        """
        Get list of all unique items in the dataset.
        
        Returns:
            List of tuples: (item_id, item_name)
        """
        if self.df is None:
            return []
        
        items = self.df[['item_id', 'item_name']].drop_duplicates().sort_values('item_name')
        return list(zip(items['item_id'], items['item_name']))
    
    def get_item_name_by_id(self, item_id: int) -> str:
        """
        Get item name by item ID.
        
        Args:
            item_id: The item ID
            
        Returns:
            Item name or empty string if not found
        """
        if self.df is None:
            return ""
        
        item = self.df[self.df['item_id'] == item_id]['item_name'].iloc[0] if len(self.df[self.df['item_id'] == item_id]) > 0 else ""
        return str(item)


class ItemDataProcessor:
    """
    Processes data for a specific item and returns supplier comparison information.
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the processor with data.
        
        Args:
            df: DataFrame containing procurement data
        """
        self.df = df
    
    def get_item_data(self, item_id: int) -> pd.DataFrame:
        """
        Get all supplier data for a specific item.
        
        Args:
            item_id: The item ID to filter by
            
        Returns:
            DataFrame filtered for the item
        """
        return self.df[self.df['item_id'] == item_id].copy()
    
    def get_supplier_prices(self, item_id: int) -> Dict[str, float]:
        """
        Get supplier name to price mapping for an item.
        
        Args:
            item_id: The item ID
            
        Returns:
            Dictionary mapping supplier names to prices
        """
        item_data = self.get_item_data(item_id)
        if item_data.empty:
            return {}
        
        return dict(zip(item_data['supplier_name'], item_data['unit_price']))
    
    def get_item_summary(self, item_id: int) -> Dict:
        """
        Get summary information for an item.
        
        Args:
            item_id: The item ID
            
        Returns:
            Dictionary with item summary data
        """
        item_data = self.get_item_data(item_id)
        
        if item_data.empty:
            return {
                'item_id': item_id,
                'item_name': 'Unknown',
                'supplier_count': 0,
                'avg_price': 0.0,
                'min_price': 0.0,
                'max_price': 0.0,
                'average_stock': 0.0,
                'average_demand': 'Unknown'
            }
        
        return {
            'item_id': item_id,
            'item_name': item_data['item_name'].iloc[0],
            'supplier_count': len(item_data),
            'avg_price': round(item_data['unit_price'].mean(), 2),
            'min_price': round(item_data['unit_price'].min(), 2),
            'max_price': round(item_data['unit_price'].max(), 2),
            'average_stock': round(item_data['stock_level'].mean(), 1),
            'average_demand': item_data['demand_level'].mode()[0] if not item_data['demand_level'].empty else 'Unknown'
        }
    
    def get_supplier_comparison_table(self, item_id: int) -> pd.DataFrame:
        """
        Get formatted supplier comparison table for an item.
        
        Args:
            item_id: The item ID
            
        Returns:
            DataFrame formatted for display with supplier comparison
        """
        item_data = self.get_item_data(item_id)
        
        if item_data.empty:
            return pd.DataFrame()
        
        # Select and rename columns for display
        display_df = item_data[['supplier_id', 'supplier_name', 'unit_price', 'stock_level', 'demand_level']].copy()
        display_df.columns = ['Supplier ID', 'Supplier Name', 'Unit Price ($)', 'Stock Level', 'Demand']
        
        # Sort by price
        display_df = display_df.sort_values('Unit Price ($)').reset_index(drop=True)
        
        # Format price column
        display_df['Unit Price ($)'] = display_df['Unit Price ($)'].apply(lambda x: f"${x:.2f}")
        
        return display_df
    
    def get_price_statistics(self, item_id: int) -> Dict:
        """
        Get price statistics for an item across all suppliers.
        
        Args:
            item_id: The item ID
            
        Returns:
            Dictionary with price statistics
        """
        item_data = self.get_item_data(item_id)
        
        if item_data.empty:
            return {}
        
        prices = item_data['unit_price'].values
        
        return {
            'min': round(prices.min(), 2),
            'max': round(prices.max(), 2),
            'avg': round(prices.mean(), 2),
            'median': round(prices.median(), 2),
            'std': round(prices.std(), 2),
            'price_range': round(prices.max() - prices.min(), 2)
        }


class SupplierFilter:
    """
    Utilities for filtering and analyzing supplier data.
    """
    
    @staticmethod
    def get_suppliers_by_price_range(
        df: pd.DataFrame,
        item_id: int,
        max_price: float
    ) -> pd.DataFrame:
        """
        Get suppliers offering prices below a threshold.
        
        Args:
            df: DataFrame with procurement data
            item_id: The item ID
            max_price: Maximum acceptable price
            
        Returns:
            Filtered DataFrame
        """
        item_data = df[df['item_id'] == item_id]
        return item_data[item_data['unit_price'] <= max_price]
    
    @staticmethod
    def get_reliable_suppliers(
        df: pd.DataFrame,
        item_id: int,
        min_stock: int = 20
    ) -> pd.DataFrame:
        """
        Get suppliers with adequate stock levels.
        
        Args:
            df: DataFrame with procurement data
            item_id: The item ID
            min_stock: Minimum stock threshold
            
        Returns:
            Filtered DataFrame of reliable suppliers
        """
        item_data = df[df['item_id'] == item_id]
        return item_data[item_data['stock_level'] >= min_stock]
    
    @staticmethod
    def get_best_value_suppliers(
        df: pd.DataFrame,
        item_id: int,
        top_n: int = 3
    ) -> pd.DataFrame:
        """
        Get top N suppliers with best pricing.
        
        Args:
            df: DataFrame with procurement data
            item_id: The item ID
            top_n: Number of top suppliers to return
            
        Returns:
            Top N suppliers sorted by price
        """
        item_data = df[df['item_id'] == item_id]
        return item_data.nsmallest(top_n, 'unit_price')
