"""NASDAQ API Client - Clean and efficient interface to NASDAQ's public API."""

__version__ = "0.2.0"

from .client import NasdaqClient
from .models import (
    QuoteData,
    FinancialData,
    OwnershipData,
    NewsData,
)

# Backward compatibility imports
from .compat import (
    fetch_all_symbol_data,
    normalize_nasdaq_data,
    fetch_all_exchanges,
    get_unique_symbols,
)

# Convenience functions for quick access
def get_quote(symbol: str) -> dict:
    """
    Quick access to get stock quote.
    
    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL')
        
    Returns:
        Dictionary with normalized quote data
        
    Example:
        >>> quote = get_quote('AAPL')
        >>> print(f"Price: ${quote['price']}")
    """
    client = NasdaqClient()
    return client.get_quote(symbol)


def get_symbol_data(symbol: str, include: list = None) -> dict:
    """
    Get comprehensive data for a symbol.
    
    Args:
        symbol: Stock ticker symbol
        include: List of data categories to include. If None, includes all.
                 Options: ['quote', 'financials', 'dividends', 'ownership', 
                          'historical', 'news', 'analyst', 'short_interest']
    
    Returns:
        Dictionary with all requested data
        
    Example:
        >>> data = get_symbol_data('MSFT', include=['quote', 'financials'])
        >>> print(data.keys())
    """
    client = NasdaqClient()
    return client.get_symbol_data(symbol, include=include)


def search_symbols(exchange: str = None, sector: str = None) -> list:
    """
    Search for symbols by exchange or sector.
    
    Args:
        exchange: Filter by exchange ('NASDAQ', 'NYSE', 'AMEX')
        sector: Filter by sector
        
    Returns:
        List of matching symbols with basic info
    """
    client = NasdaqClient()
    return client.search_symbols(exchange=exchange, sector=sector)


__all__ = [
    # Main client
    "NasdaqClient",
    # Data models
    "QuoteData",
    "FinancialData",
    "OwnershipData",
    "NewsData",
    # Convenience functions
    "get_quote",
    "get_symbol_data",
    "search_symbols",
    # Backward compatibility
    "fetch_all_symbol_data",
    "normalize_nasdaq_data",
    "fetch_all_exchanges",
    "get_unique_symbols",
]

