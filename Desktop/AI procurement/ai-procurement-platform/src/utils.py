"""
Utility Functions

This module provides helper functions for formatting, charting, and other
common operations used throughout the application.
"""

import pandas as pd
from typing import Dict, List
import streamlit as st


def format_currency(value: float) -> str:
    """
    Format a value as USD currency.
    
    Args:
        value: Numeric value to format
        
    Returns:
        Formatted currency string
    """
    return f"${value:,.2f}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format a value as percentage.
    
    Args:
        value: Numeric value (0-1) to format as percentage
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    return f"{value * 100:.{decimals}f}%"


def get_demand_color(demand_level: str) -> str:
    """
    Get color code for demand level indicator.
    
    Args:
        demand_level: 'Low', 'Medium', or 'High'
        
    Returns:
        Color code for the demand level
    """
    demand_colors = {
        'Low': '🟢',
        'Medium': '🟡',
        'High': '🔴'
    }
    return demand_colors.get(demand_level, '⚪')


def get_decision_color(decision: str) -> str:
    """
    Get color indicator for procurement decision.
    
    Args:
        decision: Decision string ('Buy Now', 'Consider Buying', 'Wait')
        
    Returns:
        Color emoji for the decision
    """
    decision_colors = {
        'Buy Now': '🟢',
        'Consider Buying': '🟡',
        'Wait': '🔴'
    }
    return decision_colors.get(decision, '⚪')


def get_stock_color(stock_level: int) -> str:
    """
    Get color indicator for stock level.
    
    Args:
        stock_level: Current stock quantity
        
    Returns:
        Color emoji for the stock level
    """
    if stock_level < 50:
        return '🔴'  # Low
    elif stock_level < 150:
        return '🟡'  # Medium
    else:
        return '🟢'  # High


def create_price_comparison_chart(supplier_prices: Dict[str, float]):
    """
    Create a bar chart comparing supplier prices.
    
    Args:
        supplier_prices: Dictionary mapping supplier names to prices
    """
    if not supplier_prices:
        st.warning("No supplier data available for chart.")
        return
    
    # Create chart data
    suppliers = list(supplier_prices.keys())
    prices = list(supplier_prices.values())
    
    # Sort by price for better visualization
    sorted_data = sorted(zip(suppliers, prices), key=lambda x: x[1])
    suppliers_sorted = [x[0] for x in sorted_data]
    prices_sorted = [x[1] for x in sorted_data]
    
    import plotly.graph_objects as go
    
    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=suppliers_sorted,
            y=prices_sorted,
            marker_color=['#1f77b4' if i == 0 else '#ff7f0e' for i in range(len(prices_sorted))],
            text=[f"${p:.2f}" for p in prices_sorted],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Price: $%{y:.2f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Supplier Price Comparison",
        xaxis_title="Supplier",
        yaxis_title="Unit Price ($)",
        height=400,
        showlegend=False,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def create_price_distribution_chart(supplier_data: pd.DataFrame):
    """
    Create a distribution chart showing min, average, and max prices.
    
    Args:
        supplier_data: DataFrame with supplier price data
    """
    if supplier_data.empty:
        st.warning("No data available for distribution chart.")
        return
    
    import plotly.graph_objects as go
    
    prices = supplier_data['unit_price'].values
    min_price = prices.min()
    max_price = prices.max()
    avg_price = prices.mean()
    
    # Create box plot
    fig = go.Figure(data=[
        go.Box(
            y=prices,
            name='Prices',
            marker_color='#1f77b4',
            boxmean='sd',
            hovertemplate='Price: $%{y:.2f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Price Distribution Across Suppliers",
        yaxis_title="Unit Price ($)",
        height=300,
        showlegend=False,
        hovermode='closest'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Minimum", format_currency(min_price))
    with col2:
        st.metric("Average", format_currency(avg_price))
    with col3:
        st.metric("Maximum", format_currency(max_price))
    with col4:
        st.metric("Range", format_currency(max_price - min_price))


def create_demand_vs_stock_matrix(
    stock_level: int,
    demand_level: str,
    avg_stock: float
):
    """
    Display a visual matrix showing the relationship between stock and demand.
    
    Args:
        stock_level: Current stock quantity
        demand_level: Current demand level ('Low', 'Medium', 'High')
        avg_stock: Average stock across suppliers
    """
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Current Stock Level",
            f"{stock_level} units",
            f"Avg: {avg_stock:.0f} units"
        )
    
    with col2:
        st.metric(
            "Demand Level",
            f"{demand_level} {get_demand_color(demand_level)}",
            "Market demand"
        )


def display_key_insight_cards(recommendation):
    """
    Display recommendation insights as cards.
    
    Args:
        recommendation: SupplierRecommendation object from decision engine
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Best Supplier",
            recommendation.best_supplier,
            f"${recommendation.best_price:.2f}"
        )
    
    with col2:
        savings = recommendation.average_price - recommendation.best_price
        savings_pct = (savings / recommendation.average_price * 100) if recommendation.average_price > 0 else 0
        st.metric(
            "Savings Potential",
            format_currency(savings),
            f"{savings_pct:.1f}% below average"
        )
    
    with col3:
        st.metric(
            "Suggested Price",
            format_currency(recommendation.suggested_purchase_price),
            "With negotiation"
        )


def display_decision_highlight(decision: str):
    """
    Display the procurement decision with visual highlight.
    
    Args:
        decision: The procurement decision string
    """
    decision_config = {
        'Buy Now': {
            'color': '#d4edda',
            'border': '2px solid #28a745',
            'emoji': '✅',
            'urgency': 'HIGH PRIORITY'
        },
        'Consider Buying': {
            'color': '#fff3cd',
            'border': '2px solid #ffc107',
            'emoji': '⚠️',
            'urgency': 'MEDIUM PRIORITY'
        },
        'Wait': {
            'color': '#f8d7da',
            'border': '2px solid #dc3545',
            'emoji': '⏸️',
            'urgency': 'MONITOR'
        }
    }
    
    config = decision_config.get(decision, decision_config['Wait'])
    
    st.markdown(
        f"""
        <div style="padding: 20px; background-color: {config['color']}; 
                    border: {config['border']}; border-radius: 8px; text-align: center;">
            <h2>{config['emoji']} {decision}</h2>
            <p style="margin: 5px 0; font-size: 14px; color: #666;">{config['urgency']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def display_metadata(last_updated: str, data_source: str = "CSV Database"):
    """
    Display metadata about the data.
    
    Args:
        last_updated: Last update timestamp
        data_source: Source of the data
    """
    col1, col2 = st.columns(2)
    with col1:
        st.caption(f"📅 Last Updated: {last_updated}")
    with col2:
        st.caption(f"📦 Data Source: {data_source}")


def create_insights_text(recommendation) -> str:
    """
    Create detailed insight text explaining the recommendation.
    
    Args:
        recommendation: SupplierRecommendation object
        
    Returns:
        Formatted insight text
    """
    insights = []
    
    # Price insight
    savings = recommendation.average_price - recommendation.best_price
    if savings > 0:
        savings_pct = (savings / recommendation.average_price * 100)
        insights.append(
            f"💰 **Price Opportunity**: {recommendation.best_supplier} offers "
            f"{savings_pct:.1f}% savings vs market average."
        )
    
    # Negotiation insight
    negotiation_savings = recommendation.average_price - recommendation.suggested_purchase_price
    insights.append(
        f"🤝 **Negotiation Potential**: Aim for {format_currency(recommendation.suggested_purchase_price)} "
        f"(5% negotiation margin) from current average of {format_currency(recommendation.average_price)}."
    )
    
    # Decision insight
    insights.append(f"📊 **Recommendation**: {recommendation.decision}")
    
    return "\n\n".join(insights)
