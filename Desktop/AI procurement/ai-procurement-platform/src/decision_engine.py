"""
Procurement Decision Engine

This module implements the core business logic for making procurement recommendations
based on supplier prices, stock levels, and demand levels.

Future phases can extend this module with:
- Supplier scoring models
- Price trend analytics
- ML-based predictions
- Risk assessment algorithms
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class ProcurementDecision(Enum):
    """Enumeration of procurement recommendations"""
    BUY_NOW = "Buy Now"
    CONSIDER_BUYING = "Consider Buying"
    WAIT = "Wait"


@dataclass
class SupplierRecommendation:
    """Data class for supplier recommendation"""
    best_supplier: str
    best_price: float
    average_price: float
    suggested_purchase_price: float
    decision: ProcurementDecision
    reasoning: str


def get_stock_level_category(stock: int) -> str:
    """
    Categorize stock level based on quantity.
    
    Args:
        stock: Current stock level in units
        
    Returns:
        Category as string: 'Low', 'Medium', or 'High'
    """
    if stock < 50:
        return "Low"
    elif stock < 150:
        return "Medium"
    else:
        return "High"


def calculate_average_price(prices: List[float]) -> float:
    """
    Calculate the average price from multiple suppliers.
    
    Args:
        prices: List of supplier prices
        
    Returns:
        Average price rounded to 2 decimal places
    """
    if not prices:
        return 0.0
    return round(sum(prices) / len(prices), 2)


def calculate_negotiation_price(average_price: float, negotiation_margin: float = 0.05) -> float:
    """
    Calculate suggested procurement price with negotiation margin.
    
    Args:
        average_price: Average price from all suppliers
        negotiation_margin: Negotiation discount as decimal (default 5%)
        
    Returns:
        Suggested purchase price rounded to 2 decimal places
    """
    return round(average_price * (1 - negotiation_margin), 2)


def identify_best_supplier(supplier_prices: Dict[str, float]) -> Tuple[str, float]:
    """
    Identify the cheapest supplier.
    
    Args:
        supplier_prices: Dictionary mapping supplier name to price
        
    Returns:
        Tuple of (supplier_name, price)
    """
    if not supplier_prices:
        return ("Unknown", 0.0)
    
    best_supplier = min(supplier_prices.items(), key=lambda x: x[1])
    return best_supplier


def is_supplier_preferred(supplier_price: float, average_price: float, threshold: float = 0.1) -> bool:
    """
    Determine if a supplier offers a preferred (below average) price.
    
    Args:
        supplier_price: Price from specific supplier
        average_price: Average market price
        threshold: Price difference threshold as decimal (default 10%)
        
    Returns:
        True if supplier price is significantly below average
    """
    return supplier_price < average_price * (1 - threshold)


def make_procurement_decision(
    stock_level: int,
    demand_level: str,
    supplier_price: float,
    average_price: float
) -> str:
    """
    Make a procurement recommendation using rule-based logic.
    
    Decision Rules:
    - Low stock + High demand → Buy Now
    - Medium stock + High demand → Consider Buying
    - High stock → Wait (unless price is exceptionally low)
    - Low demand + High stock → Wait
    
    Args:
        stock_level: Current stock quantity
        demand_level: Demand level ('Low', 'Medium', 'High')
        supplier_price: Price from selected supplier
        average_price: Average market price
        
    Returns:
        Procurement decision as string
    """
    stock_category = get_stock_level_category(stock_level)
    
    # Rule 1: Low stock + High demand = Buy Now
    if stock_category == "Low" and demand_level == "High":
        return ProcurementDecision.BUY_NOW.value
    
    # Rule 2: Medium stock + High demand = Consider Buying
    if stock_category == "Medium" and demand_level == "High":
        return ProcurementDecision.CONSIDER_BUYING.value
    
    # Rule 3: High stock = Wait (unless price is exceptional)
    if stock_category == "High":
        # Exception: Buy if price is significantly below average and demand is high
        if demand_level == "High" and is_supplier_preferred(supplier_price, average_price, 0.15):
            return ProcurementDecision.CONSIDER_BUYING.value
        return ProcurementDecision.WAIT.value
    
    # Rule 4: Medium stock + Low/Medium demand = Wait  
    if stock_category == "Medium" and demand_level in ["Low", "Medium"]:
        return ProcurementDecision.WAIT.value
    
    # Default: Conservative approach
    return ProcurementDecision.WAIT.value


def generate_decision_reasoning(
    decision: str,
    stock_level: int,
    demand_level: str,
    stock_category: str,
    supplier_price: float,
    average_price: float,
    best_supplier: str
) -> str:
    """
    Generate human-readable reasoning for the procurement decision.
    
    Args:
        decision: The procurement decision
        stock_level: Current stock quantity
        demand_level: Demand level
        stock_category: Stock category (Low/Medium/High)
        supplier_price: Selected supplier price
        average_price: Average market price
        best_supplier: Name of best (cheapest) supplier
        
    Returns:
        Reasoning explanation as string
    """
    price_savings = average_price - supplier_price
    price_savings_pct = (price_savings / average_price * 100) if average_price > 0 else 0
    
    reasoning_parts = []
    reasoning_parts.append(f"Stock Level: {stock_category} ({stock_level} units) | Demand: {demand_level}")
    reasoning_parts.append(f"Supplier selected at ${supplier_price:.2f} vs market average of ${average_price:.2f}")
    
    if price_savings > 0:
        reasoning_parts.append(f"(Savings: {price_savings_pct:.1f}% below average)")
    
    reasoning_parts.append(f"Best supplier available: {best_supplier}")
    
    if decision == ProcurementDecision.BUY_NOW.value:
        reasoning_parts.append(f"✓ Low inventory with high demand requires immediate procurement.")
    elif decision == ProcurementDecision.CONSIDER_BUYING.value:
        reasoning_parts.append(f"⚠ Moderate inventory with high demand. Consider purchase if pricing is favorable.")
    else:  # WAIT
        reasoning_parts.append(f"⏸ Current stock levels are sufficient. Monitor for price improvements.")
    
    return " | ".join(reasoning_parts)


def generate_recommendation(
    selected_supplier: str,
    selected_price: float,
    supplier_prices: Dict[str, float],
    stock_level: int,
    demand_level: str
) -> SupplierRecommendation:
    """
    Generate a complete procurement recommendation.
    
    This is the main entry point for the decision engine.
    
    Args:
        selected_supplier: Name of selected supplier
        selected_price: Price from selected supplier
        supplier_prices: Dictionary of all supplier prices
        stock_level: Current stock quantity
        demand_level: Current demand level
        
    Returns:
        SupplierRecommendation object with complete analysis
    """
    # Calculate metrics
    average_price = calculate_average_price(list(supplier_prices.values()))
    negotiation_price = calculate_negotiation_price(average_price)
    best_supplier, best_price = identify_best_supplier(supplier_prices)
    stock_category = get_stock_level_category(stock_level)
    
    # Make decision
    decision = make_procurement_decision(
        stock_level,
        demand_level,
        selected_price,
        average_price
    )
    
    # Generate reasoning
    reasoning = generate_decision_reasoning(
        decision,
        stock_level,
        demand_level,
        stock_category,
        selected_price,
        average_price,
        best_supplier
    )
    
    return SupplierRecommendation(
        best_supplier=best_supplier,
        best_price=best_price,
        average_price=average_price,
        suggested_purchase_price=negotiation_price,
        decision=decision,
        reasoning=reasoning
    )
