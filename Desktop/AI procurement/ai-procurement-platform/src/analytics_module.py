"""
Analytics Module for Procurement Intelligence

Provides advanced analytics, market insights, and AI-ready data preparation
for procurement decision systems.

Author: AI Procurement Platform Team
Date: February 2026
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime


class ProcurementAnalytics:
    """
    Advanced analytics engine for AI procurement platform.
    Generates market insights and prepares data for ML models.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize analytics engine.
        
        Args:
            df: Product dataframe
        """
        self.df = df.copy()
        self.analysis_date = datetime.now().strftime("%Y-%m-%d")

    def get_market_overview(self) -> Dict:
        """
        Generate high-level market overview.
        
        Returns:
            Dictionary with market metrics
        """
        return {
            "total_products": self.df["product_id"].nunique(),
            "total_suppliers": self.df["supplier_name"].nunique(),
            "categories": self.df["category"].nunique(),
            "brands": self.df["brand"].nunique(),
            "avg_price": round(self.df["selling_price"].mean(), 2),
            "median_price": round(self.df["selling_price"].median(), 2),
            "price_std_dev": round(self.df["selling_price"].std(), 2),
            "analysis_date": self.analysis_date
        }

    def get_category_performance(self) -> pd.DataFrame:
        """
        Analyze performance metrics by category.
        
        Returns:
            DataFrame with category metrics
        """
        performance = self.df.groupby("category").agg({
            "product_id": "nunique",
            "supplier_name": "nunique",
            "selling_price": ["mean", "min", "max"],
            "mrp": "mean",
            "brand": "nunique"
        }).round(2)
        
        performance.columns = [
            "Products", "Suppliers", "Avg Price", "Min Price", "Max Price", "Avg MRP", "Brands"
        ]
        
        return performance.sort_values("Products", ascending=False)

    def get_supplier_performance(self) -> pd.DataFrame:
        """
        Analyze supplier performance metrics.
        
        Returns:
            DataFrame with supplier metrics
        """
        performance = self.df.groupby("supplier_name").agg({
            "product_id": "nunique",
            "selling_price": ["mean", "min", "max"],
            "brand": "nunique",
            "category": "nunique"
        }).round(2)
        
        performance.columns = [
            "Products", "Avg Price", "Min Price", "Max Price", "Brands", "Categories"
        ]
        
        # Add supplier rankings
        performance["Price Competitiveness"] = (
            100 - (performance["Avg Price"] - performance["Avg Price"].min()) / 
            (performance["Avg Price"].max() - performance["Avg Price"].min()) * 100
        ).round(1)
        
        return performance.sort_values("Price Competitiveness", ascending=False)

    def get_brand_analysis(self, category: str = None) -> pd.DataFrame:
        """
        Analyze brand distribution and pricing.
        
        Args:
            category: Optional category filter
            
        Returns:
            DataFrame with brand metrics
        """
        data = self.df if category is None else self.df[self.df["category"] == category]
        
        brand_analysis = data.groupby("brand").agg({
            "product_id": "nunique",
            "selling_price": ["mean", "min", "max"],
            "supplier_name": "nunique",
            "category": lambda x: ", ".join(x.unique()[:2])
        }).round(2)
        
        brand_analysis.columns = ["Products", "Avg Price", "Min Price", "Max Price", "Suppliers", "Categories"]
        
        return brand_analysis.sort_values("Products", ascending=False)

    def calculate_avg_category_prices(self) -> pd.DataFrame:
        """
        Calculate average prices for each category for procurement planning.
        
        Returns:
            DataFrame with category averages for procurement
        """
        category_prices = self.df.groupby("category").agg({
            "selling_price": ["mean", "median", "std", "min", "max"],
            "product_id": "nunique"
        }).round(2)
        
        category_prices.columns = [
            "Avg Price", "Median Price", "Price Variance", "Min", "Max", "Products"
        ]
        
        return category_prices

    def get_supplier_price_table(self) -> pd.DataFrame:
        """
        Generate supplier price comparison table for procurement decisions.
        
        Returns:
            DataFrame with supplier pricing matrix
        """
        # Create pivot table: Products x Suppliers
        price_matrix = self.df.pivot_table(
            values="selling_price",
            index="product_name",
            columns="supplier_name",
            aggfunc="mean"
        ).round(2)
        
        return price_matrix

    def generate_procurement_dataset(self) -> Dict:
        """
        Generate AI-ready procurement dataset.
        
        Returns:
            Dictionary with structured procurement data
        """
        return {
            "category_averages": self.calculate_avg_category_prices().to_dict(),
            "supplier_comparison": self.get_supplier_price_table().to_dict(),
            "category_performance": self.get_category_performance().to_dict(),
            "supplier_rankings": self.get_supplier_performance().to_dict(),
            "market_overview": self.get_market_overview(),
            "dataset_date": self.analysis_date
        }

    def get_price_competitiveness(self) -> pd.DataFrame:
        """
        Identify products with highest and lowest price variations.
        
        Returns:
            DataFrame with competitiveness scores
        """
        competitiveness = self.df.groupby("product_name").agg({
            "selling_price": ["mean", "std", "min", "max"]
        }).round(2)
        
        competitiveness.columns = ["Avg Price", "Price Variance", "Min Price", "Max Price"]
        
        # Calculate competitiveness: high variance = competitive market
        competitiveness["Competitiveness Score"] = (
            competitiveness["Price Variance"] / competitiveness["Avg Price"] * 100
        ).round(2)
        
        return competitiveness.sort_values("Competitiveness Score", ascending=False)

    def get_market_concentration(self) -> Dict[str, float]:
        """
        Analyze market concentration (HHI - Herfindahl-Hirschman Index).
        
        Returns:
            Dictionary with concentration metrics by category
        """
        concentration = {}
        
        for category in self.df["category"].unique():
            category_data = self.df[self.df["category"] == category]
            
            # Market share by supplier
            supplier_shares = (
                category_data.groupby("supplier_name").size() / len(category_data) * 100
            )
            
            # HHI = sum of squared market shares
            hhi = (supplier_shares ** 2).sum()
            concentration[category] = round(hhi, 2)
        
        return concentration

    def identify_strategic_products(self) -> pd.DataFrame:
        """
        Identify strategic products for procurement focus:
        - High volume (many suppliers)
        - Price sensitive (high variance)
        - Market leverage potential
        
        Returns:
            DataFrame with strategic product ranking
        """
        strategic = self.df.groupby("product_name").agg({
            "supplier_name": "nunique",
            "selling_price": ["mean", "std"],
            "product_id": "count"
        }).round(2)
        
        strategic.columns = ["Supplier Count", "Avg Price", "Price Variance", "Records"]
        
        # Strategic importance = suppliers * variance / avg price
        strategic["Strategic Score"] = (
            strategic["Supplier Count"] * 
            (strategic["Price Variance"] / strategic["Avg Price"]) * 100
        ).round(2)
        
        return strategic.sort_values("Strategic Score", ascending=False)

    def get_savings_potential(self) -> pd.DataFrame:
        """
        Calculate total savings potential across all products.
        
        Returns:
            DataFrame with savings analysis
        """
        savings_data = []
        
        for product_id in self.df["product_id"].unique():
            product_data = self.df[self.df["product_id"] == product_id]
            max_price = product_data["selling_price"].max()
            min_price = product_data["selling_price"].min()
            avg_price = product_data["selling_price"].mean()
            
            if max_price > min_price:
                savings_pct = ((max_price - min_price) / max_price) * 100
                savings_data.append({
                    "product_name": product_data.iloc[0]["product_name"],
                    "category": product_data.iloc[0]["category"],
                    "current_max_price": round(max_price, 2),
                    "best_price": round(min_price, 2),
                    "savings_per_unit": round(max_price - min_price, 2),
                    "savings_percentage": round(savings_pct, 2)
                })
        
        return pd.DataFrame(savings_data).sort_values("savings_percentage", ascending=False)

    def export_for_ml_training(self) -> pd.DataFrame:
        """
        Export data in format suitable for ML model training.
        
        Returns:
            DataFrame optimized for ML
        """
        ml_data = self.df.copy()
        
        # Add engineered features
        ml_data["discount_pct"] = (
            (ml_data["mrp"] - ml_data["selling_price"]) / ml_data["mrp"] * 100
        ).round(2)
        
        ml_data["price_per_gram_equivalent"] = (
            ml_data["selling_price"] / ml_data["pack_size"]
        ).round(4)
        
        ml_data["is_branded"] = ml_data["brand"].notna().astype(int)
        
        # Normalize numeric features
        ml_data["price_normalized"] = (
            (ml_data["selling_price"] - ml_data["selling_price"].min()) /
            (ml_data["selling_price"].max() - ml_data["selling_price"].min())
        ).round(4)
        
        return ml_data[[
            "product_id", "product_name", "category", "subcategory", "brand",
            "supplier_name", "selling_price", "mrp", "pack_size", "unit",
            "discount_pct", "price_per_gram_equivalent", "is_branded", "price_normalized"
        ]]
