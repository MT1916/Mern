"""
Product Catalog Module for Indian E-commerce

Manages product catalog, search, filtering, and organization
for AI procurement platform.

Author: AI Procurement Platform Team
Date: February 2026
"""

import pandas as pd
from typing import List, Dict, Optional, Tuple
import numpy as np


class ProductCatalog:
    """
    Manages product catalog with search, filtering, and discovery capabilities.
    Optimized for Indian e-commerce and procurement operations.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize catalog with product data.
        
        Args:
            df: DataFrame containing product information
        """
        self.df = df.copy()
        self.total_products = len(df["product_id"].unique())
        self.total_suppliers = df["supplier_name"].nunique()

    def search_products(self, query: str, limit: int = 50) -> pd.DataFrame:
        """
        Search products by name, brand, or category.
        
        Args:
            query: Search query
            limit: Maximum results to return
            
        Returns:
            DataFrame with matching products
        """
        query_lower = query.lower()
        
        mask = (
            self.df["product_name"].str.lower().str.contains(query_lower, na=False) |
            self.df["brand"].str.lower().str.contains(query_lower, na=False) |
            self.df["category"].str.lower().str.contains(query_lower, na=False) |
            self.df["subcategory"].str.lower().str.contains(query_lower, na=False)
        )
        
        results = self.df[mask].drop_duplicates(subset=["product_id"])
        return results.head(limit)

    def get_products_by_category(self, category: str) -> pd.DataFrame:
        """
        Get all products in a specific category.
        
        Args:
            category: Category name
            
        Returns:
            DataFrame with products in category
        """
        return self.df[self.df["category"] == category].drop_duplicates(subset=["product_id"])

    def get_products_by_subcategory(self, subcategory: str) -> pd.DataFrame:
        """
        Get all products in a specific subcategory.
        
        Args:
            subcategory: Subcategory name
            
        Returns:
            DataFrame with products in subcategory
        """
        return self.df[self.df["subcategory"] == subcategory].drop_duplicates(subset=["product_id"])

    def get_products_by_brand(self, brand: str, category: str = None) -> pd.DataFrame:
        """
        Get all products from a specific brand.
        
        Args:
            brand: Brand name
            category: Optional category filter
            
        Returns:
            DataFrame with products from brand
        """
        mask = self.df["brand"] == brand
        
        if category:
            mask = mask & (self.df["category"] == category)
        
        return self.df[mask].drop_duplicates(subset=["product_id"])

    def get_brands_by_category(self, category: str) -> List[str]:
        """
        Get list of brands available in a category.
        
        Args:
            category: Category name
            
        Returns:
            Sorted list of brand names
        """
        brands = self.df[self.df["category"] == category]["brand"].unique()
        return sorted(brands.tolist())

    def get_all_categories(self) -> List[str]:
        """Get sorted list of all categories"""
        return sorted(self.df["category"].unique().tolist())

    def get_all_subcategories(self) -> List[str]:
        """Get sorted list of all subcategories"""
        return sorted(self.df["subcategory"].unique().tolist())

    def get_all_suppliers(self) -> List[str]:
        """Get sorted list of all suppliers"""
        return sorted(self.df["supplier_name"].unique().tolist())

    def get_product_details(self, product_id: int) -> pd.DataFrame:
        """
        Get detailed information about a specific product across all suppliers.
        
        Args:
            product_id: Product ID
            
        Returns:
            DataFrame with complete product details
        """
        return self.df[self.df["product_id"] == product_id].sort_values("selling_price")

    def get_product_by_name(self, product_name: str) -> pd.DataFrame:
        """Get all suppliers for a product by name"""
        return self.df[self.df["product_name"] == product_name]

    def filter_by_price_range(self, min_price: float, max_price: float) -> pd.DataFrame:
        """
        Filter products within a price range.
        
        Args:
            min_price: Minimum price
            max_price: Maximum price
            
        Returns:
            DataFrame with products in price range
        """
        return self.df[
            (self.df["selling_price"] >= min_price) & 
            (self.df["selling_price"] <= max_price)
        ].drop_duplicates(subset=["product_id"])

    def filter_by_pack_size(self, unit: str, min_size: float = None, max_size: float = None) -> pd.DataFrame:
        """
        Filter products by pack size and unit.
        
        Args:
            unit: Unit type (kg, litre, gram, piece, etc.)
            min_size: Optional minimum pack size
            max_size: Optional maximum pack size
            
        Returns:
            DataFrame with matched products
        """
        mask = self.df["unit"] == unit
        
        if min_size:
            mask = mask & (self.df["pack_size"] >= min_size)
        
        if max_size:
            mask = mask & (self.df["pack_size"] <= max_size)
        
        return self.df[mask].drop_duplicates(subset=["product_id"])

    def get_bestsellers(self, limit: int = 20) -> pd.DataFrame:
        """
        Get most stocked/popular products (proxy for bestsellers).
        
        Args:
            limit: Number of products to return
            
        Returns:
            DataFrame with top products
        """
        return self.df.groupby("product_name").agg({
            "product_id": "first",
            "category": "first",
            "selling_price": "mean",
            "supplier_name": "count"
        }).rename(columns={"supplier_name": "suppliers_count"}).sort_values(
            "suppliers_count", ascending=False
        ).head(limit).reset_index()

    def get_catalog_summary(self) -> Dict:
        """
        Get comprehensive catalog summary statistics.
        
        Returns:
            Dictionary with catalog metrics
        """
        return {
            "total_unique_products": self.total_products,
            "total_suppliers": self.total_suppliers,
            "total_records": len(self.df),
            "categories": len(self.df["category"].unique()),
            "subcategories": len(self.df["subcategory"].unique()),
            "brands": len(self.df["brand"].unique()),
            "avg_product_price": round(self.df["selling_price"].mean(), 2),
            "price_range": f"{self.df['selling_price'].min():.2f} - {self.df['selling_price'].max():.2f}",
            "units": self.df["unit"].unique().tolist()
        }

    def get_price_per_unit(self, df_subset: pd.DataFrame = None) -> pd.DataFrame:
        """
        Calculate normalized price per standard unit.
        
        Args:
            df_subset: Optional subset of dataframe
            
        Returns:
            DataFrame with normalized pricing
        """
        data = df_subset if df_subset is not None else self.df
        
        data_copy = data.copy()
        # Convert to per-unit pricing (assuming price is per pack)
        data_copy["price_per_unit"] = data_copy["selling_price"] / data_copy["pack_size"]
        
        return data_copy[["product_name", "brand", "pack_size", "unit", "selling_price", "price_per_unit"]].sort_values(
            "price_per_unit"
        )

    def compare_similar_products(self, product_id: int) -> pd.DataFrame:
        """
        Find and compare similar products in same category/subcategory.
        
        Args:
            product_id: Reference product ID
            
        Returns:
            DataFrame with similar products
        """
        product = self.df[self.df["product_id"] == product_id].iloc[0]
        
        similar = self.df[
            (self.df["subcategory"] == product["subcategory"]) &
            (self.df["product_id"] != product_id)
        ].drop_duplicates(subset=["product_id"]).sort_values("selling_price")
        
        return similar[["product_id", "product_name", "brand", "selling_price", "pack_size", "unit"]]

    def get_category_composition(self) -> Dict[str, List[str]]:
        """
        Get mapping of categories to subcategories.
        
        Returns:
            Dictionary mapping categories to subcategories
        """
        composition = {}
        for category in self.get_all_categories():
            subcats = self.df[self.df["category"] == category]["subcategory"].unique().tolist()
            composition[category] = sorted(subcats)
        
        return composition
