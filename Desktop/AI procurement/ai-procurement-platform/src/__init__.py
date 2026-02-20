"""
AI Procurement & Pricing Intelligence Platform
Package: src

Core modules for the procurement decision system.
"""

__version__ = "1.0.0"
__author__ = "AI Procurement Platform Team"
__email__ = "support@ai-procurement.platform"

from .decision_engine import generate_recommendation, ProcurementDecision
from .data_processor import ProcurementDataLoader, ItemDataProcessor

__all__ = [
    'generate_recommendation',
    'ProcurementDecision',
    'ProcurementDataLoader',
    'ItemDataProcessor',
]
