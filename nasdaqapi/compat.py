"""Backward compatibility layer for existing code."""

from .client import NasdaqClient
from typing import Dict, Any, List

# Create a default client instance
_client = NasdaqClient()


def fetch_all_symbol_data(symbol: str) -> Dict[str, Any]:
    """
    Fetch all data for a symbol (legacy compatibility).
    
    Args:
        symbol: Stock ticker symbol
        
    Returns:
        Dictionary with all symbol data
    """
    return _client.get_symbol_data(symbol)


def normalize_nasdaq_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize NASDAQ data (legacy compatibility).
    
    Since the new client returns normalized data by default,
    this just returns the data as-is.
    
    Args:
        raw_data: Data from fetch_all_symbol_data
        
    Returns:
        The same data (already normalized)
    """
    return raw_data


def fetch_all_exchanges() -> List[Dict[str, Any]]:
    """
    Fetch all ticker symbols from all exchanges (legacy compatibility).
    
    Returns:
        List of ticker dictionaries
    """
    return _client.search_symbols()


def get_unique_symbols(tickers: List[Dict[str, Any]]) -> List[str]:
    """
    Extract unique symbols from ticker list.
    
    Args:
        tickers: List of ticker dictionaries
        
    Returns:
        List of unique symbols
    """
    return list(set(t["symbol"] for t in tickers if "symbol" in t))


# Export legacy function names
__all__ = [
    "fetch_all_symbol_data",
    "normalize_nasdaq_data",
    "fetch_all_exchanges",
    "get_unique_symbols",
]
