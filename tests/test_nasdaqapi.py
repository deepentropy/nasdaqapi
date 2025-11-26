"""Tests for nasdaqapi package."""
import pytest
from nasdaqapi import (
    fetch_symbol_info,
    fetch_all_symbol_data,
    normalize_nasdaq_data,
    parse_price,
    parse_percentage,
    parse_volume,
)


def test_parse_price():
    """Test price parsing."""
    assert parse_price("$100.50") == 100.50
    assert parse_price("1,234.56") == 1234.56
    assert parse_price("N/A") is None
    assert parse_price("") is None


def test_parse_percentage():
    """Test percentage parsing."""
    assert parse_percentage("50%") == 0.50
    assert parse_percentage("10.5%") == 0.105
    assert parse_percentage("N/A") is None


def test_parse_volume():
    """Test volume parsing."""
    assert parse_volume("1,000") == 1000
    assert parse_volume("1,234,567") == 1234567
    assert parse_volume("") is None


def test_fetch_symbol_info():
    """Test fetching symbol info."""
    info = fetch_symbol_info("AAPL")
    assert info is not None
    assert "symbol" in info
    assert info["symbol"] == "AAPL"


def test_fetch_all_symbol_data():
    """Test fetching all data for a symbol."""
    data = fetch_all_symbol_data("MSFT")
    assert data is not None
    assert "symbol" in data
    assert data["symbol"] == "MSFT"
    assert "info" in data
    assert "dividends" in data


def test_normalize_nasdaq_data():
    """Test data normalization."""
    raw_data = fetch_all_symbol_data("GOOGL")
    normalized = normalize_nasdaq_data(raw_data)
    
    assert "metadata" in normalized
    assert "quote" in normalized
    assert "key_metrics" in normalized
    assert "dividends" in normalized
    assert "financials" in normalized
    assert "ownership" in normalized
    
    # Check metadata
    assert normalized["metadata"]["symbol"] == "GOOGL"
    assert normalized["metadata"]["company_name"] is not None
    
    # Check quote
    assert "price" in normalized["quote"]
    assert "volume" in normalized["quote"]
