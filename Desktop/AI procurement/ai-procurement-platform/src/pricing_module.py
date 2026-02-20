"""
Pricing Intelligence Module for Indian E-commerce Products

Provides pricing analysis, comparison, and procurement recommendations
for AI-driven pricing decisions.

Author: AI Procurement Platform Team
Date: February 2026
"""

import pandas as pd
from typing import Dict, List, Optional, Tuple
import numpy as np


class PricingAnalyzer:
    """
    Advanced pricing analysis engine for procurement decision support.
    Analyzes price variations, calculates fair pricing, and generates insights.
    """

    def __init__(self):
        """Initialize pricing analyzer"""
        self.discount_margin = 0.05  # 5% negotiation margin
        self.price_variance_threshold = 0.20  # 20% variance is significant

    def analyze_product_pricing(self, df: pd.DataFrame, product_id: int) -> Dict:
        """
        Comprehensive pricing analysis for a specific product.
        
        Args:
            df: DataFrame with product data
            product_id: Product ID to analyze
            
        Returns:
            Dictionary with detailed pricing insights
        """
        product_data = df[df["product_id"] == product_id].copy()
        
        if product_data.empty:
            return {"error": "Product not found"}
        
        prices = product_data["selling_price"].values
        mrp_prices = product_data["mrp"].values
        discount_pct = ((mrp_prices - prices) / mrp_prices * 100).mean()
        
        analysis = {
            "product_name": product_data.iloc[0]["product_name"],
            "product_id": product_id,
            "avg_mrp": float(mrp_prices.mean()),
            "avg_selling_price": float(prices.mean()),
            "min_price": float(prices.min()),
            "max_price": float(prices.max()),
            "price_range": float(prices.max() - prices.min()),
            "price_std_dev": float(prices.std()),
            "avg_discount_pct": float(discount_pct),
            "supplier_count": len(product_data),
            "median_price": float(np.median(prices)),
            "fair_price": self._calculate_fair_price(prices),
        }
        
        # Price comparison by supplier
        supplier_prices = product_data[["supplier_name", "brand", "selling_price", "mrp", "pack_size"]].copy()
        analysis["supplier_comparison"] = supplier_prices.to_dict("records")
        
        return analysis

    def _calculate_fair_price(self, prices: np.ndarray) -> float:
        """Calculate fair market price using median with outlier removal"""
        # Remove outliers using IQR method
        Q1 = np.percentile(prices, 25)
        Q3 = np.percentile(prices, 75)
        IQR = Q3 - Q1
        
        filtered_prices = prices[(prices >= Q1 - 1.5*IQR) & (prices <= Q3 + 1.5*IQR)]
        
        if len(filtered_prices) == 0:
            return float(np.median(prices))
        
        return float(np.median(filtered_prices))

    def calculate_procurement_price(self, fair_price: float, negotiation_margin: float = None) -> float:
        """
        Calculate procurement target price based on fair price and negotiation margin.
        
        Args:
            fair_price: Fair market price
            negotiation_margin: Discount margin (default 5%)
            
        Returns:
            Target procurement price
        """
        margin = negotiation_margin or self.discount_margin
        return float(fair_price * (1 - margin))

    def get_price_statistics_by_category(self, df: pd.DataFrame, category: str = None) -> pd.DataFrame:
        """
        Get price statistics grouped by category or overall.
        
        Args:
            df: Product dataframe
            category: Optional category to filter
            
        Returns:
            DataFrame with price statistics
        """
        if category:
            data = df[df["category"] == category]
        else:
            data = df
        
        stats = data.groupby("product_name").agg({
            "selling_price": ["mean", "min", "max", "std"],
            "mrp": "mean",
            "supplier_name": "count",
            "brand": lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0]
        }).round(2)
        
        stats.columns = ["Avg Price", "Min Price", "Max Price", "Std Dev", "Avg MRP", "Suppliers", "Brand"]
        return stats.sort_values("Avg Price", ascending=False)

    def identify_price_anomalies(self, df: pd.DataFrame, product_id: int = None) -> pd.DataFrame:
        """
        Identify products with unusual price variations across suppliers.
        
        Args:
            df: Product dataframe
            product_id: Optional product ID to check
            
        Returns:
            DataFrame with anomalies
        """
        if product_id:
            data = df[df["product_id"] == product_id]
        else:
            data = df
        
        anomalies = []
        
        for product in data["product_id"].unique():
            product_prices = data[data["product_id"] == product]["selling_price"]
            
            if len(product_prices) > 1:
                cv = product_prices.std() / product_prices.mean()  # Coefficient of variation
                
                if cv > self.price_variance_threshold:
                    anomalies.append({
                        "product_id": product,
                        "product_name": data[data["product_id"] == product].iloc[0]["product_name"],
                        "max_price": product_prices.max(),
                        "min_price": product_prices.min(),
                        "variance_pct": (cv * 100),
                        "status": "High Variance"
                    })
        
        return pd.DataFrame(anomalies)

    def compare_suppliers(self, df: pd.DataFrame, product_id: int = None, category: str = None) -> pd.DataFrame:
        """
        Compare supplier pricing for better procurement decisions.
        
        Args:
            df: Product dataframe
            product_id: Optional specific product
            category: Optional category filter
            
        Returns:
            DataFrame with supplier comparison
        """
        if product_id:
            data = df[df["product_id"] == product_id]
        elif category:
            data = df[df["category"] == category]
        else:
            data = df
        
        supplier_comparison = data.groupby("supplier_name").agg({
            "selling_price": ["mean", "min", "max"],
            "product_id": "count",
            "brand": "nunique"
        }).round(2)
        
        supplier_comparison.columns = ["Avg Price", "Min Price", "Max Price", "Products Offered", "Brands"]
        supplier_comparison = supplier_comparison.sort_values("Avg Price")
        
        return supplier_comparison

    def get_discount_distribution(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze discount distribution across products.
        
        Args:
            df: Product dataframe
            
        Returns:
            DataFrame with discount statistics
        """
        df_copy = df.copy()
        df_copy["discount_pct"] = ((df_copy["mrp"] - df_copy["selling_price"]) / df_copy["mrp"] * 100).round(2)
        
        discount_stats = df_copy.groupby("category")["discount_pct"].agg([
            "mean", "min", "max", "std"
        ]).round(2)
        
        discount_stats.columns = ["Avg Discount %", "Min Discount %", "Max Discount %", "Std Dev"]
        
        return discount_stats

    def calculate_savings_opportunity(self, df: pd.DataFrame, product_id: int) -> Dict:
        """
        Calculate potential savings for a product by buying from best supplier.
        
        Args:
            df: Product dataframe
            product_id: Product ID
            
        Returns:
            Dictionary with savings analysis
        """
        product_data = df[df["product_id"] == product_id]
        
        if product_data.empty:
            return {"error": "Product not found"}
        
        prices = product_data["selling_price"]
        max_price = prices.max()
        min_price = prices.min()
        savings_per_unit = max_price - min_price
        savings_pct = (savings_per_unit / max_price) * 100
        
        worst_supplier = product_data[product_data["selling_price"] == max_price]["supplier_name"].values[0]
        best_supplier = product_data[product_data["selling_price"] == min_price]["supplier_name"].values[0]
        
        return {
            "product_name": product_data.iloc[0]["product_name"],
            "savings_per_unit": round(savings_per_unit, 2),
            "savings_percentage": round(savings_pct, 2),
            "current_supplier": worst_supplier,
            "best_supplier": best_supplier,
            "current_price": round(max_price, 2),
            "best_price": round(min_price, 2)
        }

    def get_price_trends_by_supplier(self, df: pd.DataFrame) -> Dict:
        """
        Analyze pricing trends by supplier for market intelligence.
        
        Args:
            df: Product dataframe
            
        Returns:
            Dictionary with supplier insights
        """
        supplier_stats = df.groupby("supplier_name")["selling_price"].agg([
            "mean", "min", "max", "std"
        ]).round(2)
        
        supplier_stats.columns = ["Avg Price", "Min Price", "Max Price", "Price Variance"]
        supplier_stats = supplier_stats.sort_values("Avg Price")
        
        return {
            "cheapest_supplier": supplier_stats.index[0],
            "most_expensive_supplier": supplier_stats.index[-1],
            "supplier_stats": supplier_stats.to_dict("index")
        }
