"""
Category Categorization Engine for Indian Grocery & FMCG Products

This module provides automatic product categorization using rule-based logic
designed for Indian e-commerce grocery and FMCG products.

Author: AI Procurement Platform Team
Date: February 2026
"""

import pandas as pd
from typing import Dict, List, Tuple, Optional


class CategoryMappingEngine:
    """
    Intelligent category mapping engine for Indian grocery and FMCG products.
    Uses keyword-based rules to automatically categorize products.
    """

    def __init__(self):
        """Initialize category mappings and rules"""
        self.categories = {
            "Rice & Grains": {
                "keywords": ["basmati", "rice", "jasmine", "white rice", "brown rice", 
                            "arborio", "parboiled", "long grain", "short grain"],
                "popular_brands": ["Aeroplane", "India Gate", "Basmati", "Taj", "Daawat"],
                "subcategories": ["Basmati", "Regular Rice", "Brown Rice", "Specialty Grains"]
            },
            "Atta & Flour": {
                "keywords": ["atta", "flour", "maida", "wheat", "besan", "corn flour", 
                            "ragi", "jowar", "whole wheat"],
                "popular_brands": ["Aashirvaad", "Pillsbury", "Maida", "Patanjali", "Catch"],
                "subcategories": ["Wheat Atta", "Maida", "Gram Flour", "Specialty Flours"]
            },
            "Dal & Legumes": {
                "keywords": ["dal", "lentil", "pulses", "moong", "chana", "masoor", 
                            "arhar", "urad", "gram", "beans", "chickpea"],
                "popular_brands": ["Tata Sampann", "Aashirvaad", "Nature's Gift", "Catch"],
                "subcategories": ["Red Lentils", "Chickpeas", "Moong Dal", "Mixed Pulses"]
            },
            "Edible Oil": {
                "keywords": ["oil", "ghee", "coconut oil", "mustard oil", "groundnut oil",
                            "sunflower oil", "sesame oil", "refined oil", "olive oil"],
                "popular_brands": ["Fortune", "Sundrop", "Saffola", "Nandini", "Patanjali"],
                "subcategories": ["Groundnut Oil", "Sunflower Oil", "Coconut Oil", "Ghee"]
            },
            "Milk & Dairy": {
                "keywords": ["milk", "curd", "yogurt", "cheese", "paneer", "lassi", 
                            "butter", "cream", "dairy", "dhai"],
                "popular_brands": ["Amul", "Mother Dairy", "Nandini", "Arun Icecream", "Britannia"],
                "subcategories": ["Milk", "Curd", "Paneer", "Cheese", "Butter"]
            },
            "Snacks & Namkeen": {
                "keywords": ["snack", "chips", "wafer", "namkeen", "bhujia", "mixture",
                            "peanut", "samosa", "chakli", "murukku"],
                "popular_brands": ["Lay's", "Bingo", "Kurkure", "Haldiram's", "Balaji"],
                "subcategories": ["Potato Chips", "Corn Snacks", "Baked Snacks", "Mixed Namkeen"]
            },
            "Beverages": {
                "keywords": ["tea", "coffee", "juice", "drink", "cola", "water", 
                            "soft drink", "energy drink", "powder"],
                "popular_brands": ["Tata Tea", "Nescafé", "Bru", "Sprite", "Frooti", "Tropicana"],
                "subcategories": ["Tea", "Coffee", "Juices", "Energy Drinks"]
            },
            "Personal Care": {
                "keywords": ["shampoo", "soap", "toothpaste", "face", "skin", "hair",
                            "lotion", "cream", "deodorant", "sanitizer"],
                "popular_brands": ["Dove", "Clinic Plus", "Crest", "Colgate", "Dettol", "Himalaya"],
                "subcategories": ["Hair Care", "Skincare", "Oral Care", "Bath Products"]
            },
            "Cleaning Products": {
                "keywords": ["detergent", "soap", "cleaner", "disinfectant", "bleach",
                            "floor", "glass", "dish", "laundry", "cleaning"],
                "popular_brands": ["Surf", "Ariel", "Rin", "Dettol", "Harpic", "Lizol"],
                "subcategories": ["Laundry Detergent", "Dish Wash", "Floor Cleaner", "Disinfectants"]
            },
            "Packaged Foods": {
                "keywords": ["instant", "noodle", "pasta", "sauce", "pickle", "jam",
                            "spread", "ketchup", "mayo", "cornflakes", "cereal"],
                "popular_brands": ["Maggi", "Sunfeast", "Britannia", "Nestlé", "Kissan"],
                "subcategories": ["Instant Noodles", "Breakfast Cereals", "Condiments", "Pickles"]
            },
            "Spices & Condiments": {
                "keywords": ["spice", "powder", "masala", "turmeric", "chili", "pepper",
                            "salt", "garam masala", "cumin", "coriander"],
                "popular_brands": ["MDH", "Everest", "Catch", "Tata Sampann", "Shan"],
                "subcategories": ["Spice Powders", "Spice Mixes", "Salt", "Condiments"]
            },
            "Household Essentials": {
                "keywords": ["paper", "tissue", "towel", "napkin", "garbage", "bag",
                            "container", "storage", "candle", "matches"],
                "popular_brands": ["Surbharoti", "Mondelez", "ITC", "Procter & Gamble"],
                "subcategories": ["Paper Products", "Storage", "Kitchen Essentials"]
            }
        }

    def categorize_product(self, product_name: str) -> Tuple[str, str]:
        """
        Automatically categorize a product based on its name.
        
        Args:
            product_name: Name of the product to categorize
            
        Returns:
            Tuple of (category, subcategory)
        """
        product_lower = product_name.lower()
        
        # Find matching category
        for category, details in self.categories.items():
            for keyword in details["keywords"]:
                if keyword in product_lower:
                    # Select subcategory based on specific keywords
                    subcategory = self._select_subcategory(product_lower, details["subcategories"])
                    return category, subcategory
        
        # Default category if no match found
        return "Other Products", "Uncategorized"

    def _select_subcategory(self, product_name: str, subcategories: List[str]) -> str:
        """
        Select the most appropriate subcategory based on product keywords.
        
        Args:
            product_name: Product name in lowercase
            subcategories: List of available subcategories
            
        Returns:
            Selected subcategory
        """
        # Simple keyword matching for subcategories
        keyword_subcategory_map = {
            "basmati": "Basmati",
            "red": "Red Lentils",
            "moong": "Moong Dal",
            "paneer": "Paneer",
            "curd": "Curd",
            "chips": "Potato Chips",
            "tea": "Tea",
            "coffee": "Coffee",
            "shampoo": "Hair Care",
            "toothpaste": "Oral Care",
            "detergent": "Laundry Detergent",
            "noodle": "Instant Noodles",
            "cereal": "Breakfast Cereals",
        }
        
        for keyword, subcat in keyword_subcategory_map.items():
            if keyword in product_name and subcat in subcategories:
                return subcat
        
        return subcategories[0] if subcategories else "General"

    def get_brand_list(self, category: str) -> List[str]:
        """Get popular brands for a category"""
        return self.categories.get(category, {}).get("popular_brands", [])

    def get_all_categories(self) -> List[str]:
        """Get list of all categories"""
        return list(self.categories.keys())

    def get_category_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate category statistics from a dataframe.
        
        Args:
            df: DataFrame with 'category' and 'subcategory' columns
            
        Returns:
            DataFrame with category distribution statistics
        """
        stats = df.groupby("category").agg({
            "product_id": "count",
            "mrp": ["mean", "min", "max"],
            "selling_price": "mean",
            "brand": "nunique"
        }).round(2)
        
        stats.columns = ["Product Count", "Avg MRP", "Min MRP", "Max MRP", "Avg Selling Price", "Unique Brands"]
        return stats

    def get_subcategory_distribution(self, df: pd.DataFrame, category: str = None) -> pd.DataFrame:
        """Get subcategory distribution statistics"""
        if category:
            filtered_df = df[df["category"] == category]
        else:
            filtered_df = df
        
        distribution = filtered_df.groupby("subcategory").agg({
            "product_id": "count",
            "selling_price": "mean"
        }).round(2)
        
        distribution.columns = ["Count", "Avg Price"]
        return distribution.sort_values("Count", ascending=False)
