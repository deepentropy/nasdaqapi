"""Data models for type hints and documentation."""

from typing import TypedDict, List, Optional


class QuoteData(TypedDict, total=False):
    """Stock quote data."""
    symbol: str
    company_name: str
    price: Optional[float]
    change: Optional[float]
    change_percent: Optional[float]
    volume: Optional[float]
    bid: Optional[float]
    ask: Optional[float]
    previous_close: Optional[float]
    week_52_high: Optional[float]
    week_52_low: Optional[float]
    market_status: str
    timestamp: str


class FinancialData(TypedDict, total=False):
    """Financial statements data."""
    income_statement: List[dict]
    balance_sheet: List[dict]
    cash_flow: List[dict]
    ratios: List[dict]


class OwnershipData(TypedDict, total=False):
    """Ownership data."""
    institutional: dict
    insider_trades: List[dict]


class NewsData(TypedDict, total=False):
    """News article."""
    title: str
    summary: str
    url: str
    published_date: str
    source: str
