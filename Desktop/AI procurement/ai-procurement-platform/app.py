"""
AI-Ready Indian E-commerce Product Categorization & Procurement Dataset System

Phase 1: Product Catalog & Pricing Intelligence Platform

A comprehensive procurement decision support system for Indian grocery and FMCG products:
- Browse and search Indian grocery catalog
- Automatic product categorization 
- Multi-supplier price comparison and analysis
- AI-ready data preparation for ML models
- Market intelligence and procurement insights

Author: AI Procurement Platform Team
Version: 1.0.0
Date: February 2026
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
from pathlib import Path

# Import custom modules
from src.data_loader_ecommerce import IndianEcommerceCatalogLoader
from src.category_engine import CategoryMappingEngine
from src.catalog_module import ProductCatalog
from src.pricing_module import PricingAnalyzer
from src.analytics_module import ProcurementAnalytics


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Indian E-commerce Product Catalog",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main { padding: 2rem; }
    .metric-card { 
        background-color: #f0f2f6; 
        padding: 1rem; 
        border-radius: 0.5rem; 
        margin: 0.5rem 0;
    }
    .category-button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 15px;
        border-radius: 5px;
        cursor: pointer;
        margin: 5px;
    }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# CACHE & INITIALIZATION
# ============================================================================

@st.cache_resource
def load_data():
    """Load and cache product data"""
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'sample_data.csv')
    
    if not os.path.exists(csv_path):
        st.error(f"❌ Data file not found: {csv_path}")
        st.stop()
    
    try:
        loader = IndianEcommerceCatalogLoader(csv_path)
        return loader.get_dataframe()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()


@st.cache_resource
def initialize_modules(df):
    """Initialize analytics modules"""
    category_engine = CategoryMappingEngine()
    catalog = ProductCatalog(df)
    pricing = PricingAnalyzer()
    analytics = ProcurementAnalytics(df)
    
    return category_engine, catalog, pricing, analytics


# ============================================================================
# LOAD DATA & MODULES
# ============================================================================

df = load_data()
category_engine, catalog, pricing_analyzer, analytics = initialize_modules(df)

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
    ---
    # � AI Procurement and Pricing
    ## Intelligent Supplier Analysis & Price Optimization
    *Smart procurement decisions powered by data-driven insights*
    ---
""")


# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

st.sidebar.markdown("### 📋 Navigation")

page = st.sidebar.radio(
    "Select Page:",
    ["🏠 Dashboard", 
     "📦 Product Catalog", 
     "💰 Pricing Analysis", 
     "📊 Market Intelligence", 
     "🎯 Procurement Data",
     "ℹ️ About & Guide"]
)

# Sidebar - Data Summary
st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Data Summary")
summary = catalog.get_catalog_summary()

col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("Products", summary["total_unique_products"])
    st.metric("Suppliers", summary["total_suppliers"])
with col2:
    st.metric("Categories", summary["categories"])
    st.metric("Brands", summary["brands"])

st.sidebar.markdown(f"**Avg Price:** ₹{summary['avg_product_price']}")


# ============================================================================
# PAGE 1: DASHBOARD
# ============================================================================

if page == "🏠 Dashboard":
    st.markdown("### Dashboard Overview")
    
    # Market Overview - Key Metrics
    market = analytics.get_market_overview()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Products", market["total_products"])
    with col2:
        st.metric("Suppliers", market["total_suppliers"])
    with col3:
        st.metric("Avg Price", f"₹{market['avg_price']}")
    with col4:
        st.metric("Median Price", f"₹{market['median_price']}")
    
    st.markdown("---")
    
    # Category Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Category Distribution")
        category_dist = df.groupby("category").size().sort_values(ascending=False)
        fig = px.bar(
            x=category_dist.values,
            y=category_dist.index,
            orientation='h',
            labels={'x': 'Number of Products', 'y': 'Category'},
            title="Products by Category"
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Brand Distribution (Top 10)")
        brand_dist = df.groupby("brand").size().sort_values(ascending=False).head(10)
        fig = px.pie(
            values=brand_dist.values,
            names=brand_dist.index,
            title="Top 10 Brands"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Price Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Price Distribution")
        fig = px.histogram(
            df,
            x="selling_price",
            nbins=30,
            title="Price Distribution (Selling Price)",
            labels={'selling_price': 'Price (₹)', 'count': 'Frequency'}
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Average Price by Supplier")
        supplier_avg = df.groupby("supplier_name")["selling_price"].mean().sort_values()
        fig = px.bar(
            x=supplier_avg.values,
            y=supplier_avg.index,
            orientation='h',
            title="Average Price by Supplier",
            labels={'x': 'Average Price (₹)', 'y': 'Supplier'}
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# PAGE 2: PRODUCT CATALOG
# ============================================================================

elif page == "📦 Product Catalog":
    st.markdown("### Product Catalog Browser")
    
    # Search and Filter Section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_query = st.text_input("🔍 Search Products", placeholder="e.g., Rice, Milk, Oil...")
    
    with col2:
        selected_category = st.selectbox("📂 Filter by Category", ["All"] + catalog.get_all_categories())
    
    with col3:
        selected_brand = st.selectbox("🏷️ Filter by Brand", ["All"] + catalog.get_all_suppliers()[:20])
    
    # Apply filters
    filtered_df = df.copy()
    
    if search_query:
        search_results = catalog.search_products(search_query)
        filtered_df = filtered_df[filtered_df["product_id"].isin(search_results["product_id"])]
    
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df["category"] == selected_category]
    
    if selected_brand != "All":
        filtered_df = filtered_df[filtered_df["supplier_name"] == selected_brand]
    
    # Display results
    st.markdown(f"**Total Products Found:** {filtered_df['product_id'].nunique()}")
    
    if not filtered_df.empty:
        # Product Count by Category in filtered results
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Products by Category")
            cat_counts = filtered_df["category"].value_counts()
            fig = px.bar(x=cat_counts.index, y=cat_counts.values, title="Count by Category")
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Price Range")
            fig = px.box(filtered_df, y="selling_price", title="Price Distribution")
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Detailed Product Table
        st.markdown("#### Product Details")
        
        display_df = filtered_df[["product_id", "product_name", "category", "brand", 
                                   "supplier_name", "selling_price", "mrp", "pack_size", "unit"]].copy()
        display_df = display_df.drop_duplicates(subset=["product_id", "supplier_name"])
        display_df = display_df.sort_values("selling_price")
        
        st.dataframe(display_df, use_container_width=True)
    else:
        st.warning("⚠️ No products found matching your filters.")
    
    # Product Details - Expandable
    st.markdown("---")
    st.markdown("#### Detailed Product Analysis")
    
    all_products = df["product_name"].unique()
    selected_product = st.selectbox("Select a product for detailed analysis:", all_products)
    
    if selected_product:
        product_id = df[df["product_name"] == selected_product]["product_id"].values[0]
        product_details = catalog.get_product_details(product_id)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Product:** {selected_product}")
            st.markdown(f"**Category:** {product_details.iloc[0]['category']}")
            st.markdown(f"**Subcategory:** {product_details.iloc[0]['subcategory']}")
            st.markdown(f"**Pack Size:** {product_details.iloc[0]['pack_size']} {product_details.iloc[0]['unit']}")
        
        with col2:
            prices = product_details["selling_price"].values
            st.markdown(f"**Price Range:** ₹{prices.min():.2f} - ₹{prices.max():.2f}")
            st.markdown(f"**Average Price:** ₹{prices.mean():.2f}")
            st.markdown(f"**Available from {len(product_details)} suppliers**")
        
        # Supplier Comparison
        st.markdown("#### Supplier Comparison")
        comparison_df = product_details[["supplier_name", "brand", "selling_price", "mrp"]].copy()
        comparison_df = comparison_df.sort_values("selling_price")
        st.dataframe(comparison_df, use_container_width=True)


# ============================================================================
# PAGE 3: PRICING ANALYSIS
# ============================================================================

elif page == "💰 Pricing Analysis":
    st.markdown("### Pricing Intelligence & Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        analysis_product = st.selectbox(
            "Select a product for pricing analysis:",
            df["product_name"].unique()
        )
    
    with col2:
        analysis_category = st.selectbox(
            "Or analyze a category:",
            ["Single Product"] + catalog.get_all_categories()
        )
    
    st.markdown("---")
    
    if analysis_category != "Single Product":
        st.markdown(f"### 📊 Pricing Analysis: {analysis_category}")
        
        category_data = df[df["category"] == analysis_category]
        
        # Price Statistics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Avg Price", f"₹{category_data['selling_price'].mean():.2f}")
        with col2:
            st.metric("Min Price", f"₹{category_data['selling_price'].min():.2f}")
        with col3:
            st.metric("Max Price", f"₹{category_data['selling_price'].max():.2f}")
        with col4:
            st.metric("Median", f"₹{category_data['selling_price'].median():.2f}")
        with col5:
            st.metric("Products", category_data["product_id"].nunique())
        
        st.markdown("---")
        
        # Price Comparison by Supplier
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Average Price by Supplier")
            supplier_prices = category_data.groupby("supplier_name")["selling_price"].mean().sort_values()
            fig = px.bar(
                x=supplier_prices.values,
                y=supplier_prices.index,
                orientation='h',
                title="Supplier Price Comparison"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Product Subcategories")
            subcats = category_data.groupby("subcategory").size()
            fig = px.pie(values=subcats.values, names=subcats.index, title="Subcategory Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        # Discount Analysis
        st.markdown("---")
        st.markdown("#### Discount Analysis")
        
        category_data_copy = category_data.copy()
        category_data_copy["discount_pct"] = ((category_data_copy["mrp"] - category_data_copy["selling_price"]) / category_data_copy["mrp"] * 100)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Avg Discount %", f"{category_data_copy['discount_pct'].mean():.1f}%")
        with col2:
            st.metric("Max Discount %", f"{category_data_copy['discount_pct'].max():.1f}%")
        
        # Products table
        st.markdown("#### Products in Category")
        prod_table = category_data[["product_name", "brand", "selling_price", "supplier_name"]].drop_duplicates()
        prod_table = prod_table.sort_values("selling_price")
        st.dataframe(prod_table, use_container_width=True)
    
    else:
        st.markdown(f"### 📊 Pricing Analysis: {analysis_product}")
        
        product_id = df[df["product_name"] == analysis_product]["product_id"].values[0]
        analysis = pricing_analyzer.analyze_product_pricing(df, product_id)
        
        if "error" not in analysis:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Avg Price", f"₹{analysis['avg_selling_price']:.2f}")
            with col2:
                st.metric("Fair Price", f"₹{analysis['fair_price']:.2f}")
            with col3:
                st.metric("Price Range", f"₹{analysis['price_range']:.2f}")
            with col4:
                st.metric("Suppliers", analysis['supplier_count'])
            
            st.markdown("---")
            
            # Supplier Pricing
            st.markdown("#### Supplier Price Comparison")
            supplier_comp = pd.DataFrame(analysis["supplier_comparison"])
            supplier_comp = supplier_comp.sort_values("selling_price")
            
            fig = px.bar(
                supplier_comp,
                x="supplier_name",
                y="selling_price",
                title="Price by Supplier"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Savings Opportunity
            st.markdown("---")
            savings = pricing_analyzer.calculate_savings_opportunity(df, product_id)
            
            if "error" not in savings:
                st.markdown("#### 💰 Savings Opportunity")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Savings per Unit", f"₹{savings['savings_per_unit']}")
                    st.markdown(f"**Best Supplier:** {savings['best_supplier']}")
                    st.markdown(f"**Best Price:** ₹{savings['best_price']}")
                
                with col2:
                    st.metric("Savings %", f"{savings['savings_percentage']:.1f}%")
                    st.markdown(f"**Current Supplier:** {savings['current_supplier']}")
                    st.markdown(f"**Current Price:** ₹{savings['current_price']}")


# ============================================================================
# PAGE 4: MARKET INTELLIGENCE
# ============================================================================

elif page == "📊 Market Intelligence":
    st.markdown("### Market Intelligence & Insights")
    
    # Category Performance
    st.markdown("#### Category Performance Analysis")
    
    perf_df = analytics.get_category_performance()
    st.dataframe(perf_df, use_container_width=True)
    
    st.markdown("---")
    
    # Supplier Performance
    st.markdown("#### Supplier Performance Ranking")
    
    supplier_perf = analytics.get_supplier_performance()
    st.dataframe(supplier_perf, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Price Competitiveness")
        competitiveness = analytics.get_price_competitiveness().head(10)
        
        fig = px.bar(
            competitiveness.reset_index(),
            x="Competitiveness Score",
            y="product_name",
            orientation='h',
            title="Top 10 Most Competitive Products"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Savings Potential")
        savings = analytics.get_savings_potential().head(10)
        
        fig = px.bar(
            savings,
            x="savings_percentage",
            y="product_name",
            orientation='h',
            title="Top 10 Savings Opportunities"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Strategic Products
    st.markdown("#### Strategic Products (High Priority)")
    strategic = analytics.identify_strategic_products().head(10)
    st.dataframe(strategic, use_container_width=True)


# ============================================================================
# PAGE 5: PROCUREMENT DATA
# ============================================================================

elif page == "🎯 Procurement Data":
    st.markdown("### AI-Ready Procurement Dataset Preparation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Dataset Export Options")
        
        export_format = st.radio(
            "Select export format:",
            ["Category Averages", "Supplier Matrix", "ML Training Data", "Full Dataset"]
        )
    
    with col2:
        st.markdown("#### Dataset Summary")
        summary = catalog.get_catalog_summary()
        
        st.json({
            "Total Records": len(df),
            "Unique Products": summary["total_unique_products"],
            "Categories": summary["categories"],
            "Suppliers": summary["total_suppliers"],
            "Brands": summary["brands"]
        })
    
    st.markdown("---")
    
    if export_format == "Category Averages":
        st.markdown("#### Average Category Prices (for Procurement)")
        cat_avg = analytics.calculate_avg_category_prices()
        st.dataframe(cat_avg, use_container_width=True)
        
        # Download button
        csv = cat_avg.to_csv()
        st.download_button(
            label="📥 Download Category Averages (CSV)",
            data=csv,
            file_name="category_averages.csv",
            mime="text/csv"
        )
    
    elif export_format == "Supplier Matrix":
        st.markdown("#### Supplier Price Matrix")
        supplier_matrix = analytics.get_supplier_price_table()
        st.dataframe(supplier_matrix, use_container_width=True)
        
        csv = supplier_matrix.to_csv()
        st.download_button(
            label="📥 Download Supplier Matrix (CSV)",
            data=csv,
            file_name="supplier_price_matrix.csv",
            mime="text/csv"
        )
    
    elif export_format == "ML Training Data":
        st.markdown("#### ML Training Dataset")
        ml_data = analytics.export_for_ml_training()
        st.dataframe(ml_data.head(50), use_container_width=True)
        
        csv = ml_data.to_csv(index=False)
        st.download_button(
            label="📥 Download ML Dataset (CSV)",
            data=csv,
            file_name="ml_training_data.csv",
            mime="text/csv"
        )
        
        st.markdown("**Dataset Features:**")
        st.markdown("""
        - `product_id`: Unique product identifier
        - `category`: Product category
        - `subcategory`: Product subcategory
        - `brand`: Product brand
        - `selling_price`: Current selling price
        - `mrp`: Maximum retail price
        - `pack_size`: Package size
        - `discount_pct`: Discount percentage
        - `price_per_gram_equivalent`: Normalized price
        - `is_branded`: Binary indicator for branded products
        - `price_normalized`: Normalized price (0-1)
        """)
    
    else:  # Full Dataset
        st.markdown("#### Full Dataset")
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Full Dataset (CSV)",
            data=csv,
            file_name="indian_procurement_dataset.csv",
            mime="text/csv"
        )


# ============================================================================
# PAGE 6: ABOUT & GUIDE
# ============================================================================

elif page == "ℹ️ About & Guide":
    st.markdown("""
    # About This Platform
    
    ## Overview
    This is an **AI-Ready Indian E-commerce Product Categorization & Procurement Dataset System** 
    designed for supply chain and procurement intelligence.
    
    ## System Features
    
    ### 1. Product Catalog
    - Browse 45+ Indian grocery and FMCG products
    - Automatic categorization using intelligent rules
    - Multi-supplier price tracking
    - Real-time availability across platforms
    
    ### 2. Category Intelligence
    - 11 main product categories
    - Intelligent subcategory mapping
    - Category-based price analytics
    - Distribution analysis
    
    ### 3. Pricing Module
    - Supplier price comparisons
    - Fair market price calculations
    - Discount analysis and tracking
    - Savings opportunity identification
    
    ### 4. Market Intelligence
    - Supplier performance rankings
    - Price competitiveness scoring
    - Strategic product identification
    - Market concentration analysis
    
    ### 5. Procurement Data Preparation
    - AI-ready dataset export
    - ML training data generation
    - Supplier price matrices
    - Category average pricing for negotiations
    
    ## Product Categories
    
    The system covers these Indian grocery & FMCG categories:
    
    - **Rice & Grains**: Basmati, Regular Rice, Specialty Grains
    - **Atta & Flour**: Wheat Atta, Maida, Gram Flour
    - **Dal & Legumes**: Masoor, Moong, Chana, Mixed Pulses
    - **Edible Oil**: Groundnut, Sunflower, Coconut, Ghee
    - **Milk & Dairy**: Fresh Milk, Curd, Paneer, Cheese, Butter
    - **Snacks & Namkeen**: Chips, Corn Snacks, Mixed Namkeen
    - **Beverages**: Tea, Coffee, Juices, Energy Drinks
    - **Personal Care**: Hair Care, Bath, Oral Care, Skincare
    - **Cleaning Products**: Detergent, Disinfectants, Floor Cleaner
    - **Packaged Foods**: Noodles, Cereals, Condiments, Pickles
    - **Spices & Condiments**: Spice Powders, Masala Mixes, Salt
    
    ## Popular Brands
    
    System includes trusted Indian brands:
    - **Rice/Atta**: Aeroplane, India Gate, Aashirvaad, Pillsbury
    - **Dal**: Tata Sampann, Catch, Nature's Gift
    - **Oil**: Fortune, Saffola, Sundrop
    - **Dairy**: Amul, Mother Dairy, Nandini
    - **Snacks**: Lay's, Kurkure, Bingo, Haldiram's
    - **Beverages**: Tata Tea, Nescafé, Sprite, Tropicana
    - **Personal Care**: Dove, Clinic Plus, Colgate, Himalaya
    - **Cleaning**: Surf, Ariel, Harpic, Dettol
    
    ## Suppliers Tracked
    
    - BigBasket
    - Blinkit
    - Grofers
    - Amazon Fresh
    
    ## How to Use
    
    ### For Procurement Analysis
    1. Go to **Pricing Analysis** page
    2. Select a product to analyze supplier prices
    3. View savings opportunities
    4. Compare fair market prices
    
    ### For Product Search
    1. Go to **Product Catalog** page
    2. Use search, category filters, and brand filters
    3. View detailed product information
    4. Compare pricing across suppliers
    
    ### For Market Intelligence
    1. Go to **Market Intelligence** page
    2. Review supplier performance rankings
    3. Identify strategic products
    4. Analyze market competitiveness
    
    ### For Data Export
    1. Go to **Procurement Data** page
    2. Select desired format (Category Averages, Supplier Matrix, ML Data)
    3. Download as CSV for further analysis
    
    ## AI/ML Ready Features
    
    The platform prepares data for future AI models:
    
    ### Prepared Data Features
    - Normalized pricing data
    - Category and subcategory encoding
    - Discount percentage calculation
    - Per-unit price normalization
    - Brand indicator variables
    - Price correlation matrices
    
    ### Future ML Capabilities
    - **Price Prediction Models**: Forecast future prices
    - **Demand Forecasting**: Predict product demand
    - **Supplier Recommendation Engine**: Optimal supplier selection
    - **Dynamic Pricing Optimization**: Real-time price optimization
    - **Procurement Timing Model**: Best time to purchase
    
    ## Data Schema
    
    ```
    product_id          : Unique product identifier
    product_name        : Product name
    category            : Main category (11 types)
    subcategory         : Product subcategory
    brand               : Brand name
    supplier_name       : Marketplace/Supplier
    mrp                 : Maximum Retail Price (₹)
    selling_price       : Current selling price (₹)
    pack_size           : Size of package
    unit                : Unit of measurement (kg, litre, gram, ml, piece)
    ```
    
    ## Kaggle Dataset Integration
    
    ### Recommended Datasets
    1. **Indian Grocery Store Dataset**: Comprehensive grocery catalog
    2. **E-commerce Product Catalog**: Multi-category product data
    3. **Indian FMCG Pricing Data**: Pricing intelligence
    
    ### Integration Steps
    1. Download CSV from Kaggle
    2. Place in `/data/` folder
    3. System auto-loads on startup
    4. Check data quality report
    5. Use in procurement analysis
    
    ## Architecture
    
    The system uses modular architecture:
    
    - **category_engine.py**: Automatic categorization logic
    - **catalog_module.py**: Product search and discovery
    - **pricing_module.py**: Pricing analysis algorithms
    - **analytics_module.py**: Market intelligence generation
    - **data_loader_ecommerce.py**: Data loading and validation
    
    ## Use Cases
    
    ### For Procurement Teams
    - Find cheapest suppliers for products
    - Negotiate better pricing with data-backed insights
    - Track price trends over time
    - Plan bulk purchases strategically
    
    ### For Supply Chain Managers
    - Monitor supplier performance
    - Identify high-risk supplier concentration
    - Forecast demand and pricing
    - Optimize category spend
    
    ### For AI/ML Engineers
    - High-quality training data
    - Pre-engineered features
    - Procurement domain knowledge
    - Ready-to-use datasets
    
    ## Contact & Support
    
    **Platform Version**: 1.0.0  
    **Last Updated**: February 2026  
    **Domain Focus**: Indian E-commerce, Grocery & FMCG Procurement  
    """)
