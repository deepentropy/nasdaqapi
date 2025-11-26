"""NASDAQ API functions for fetching comprehensive symbol data."""

import requests
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

NASDAQ_API_BASE = "https://api.nasdaq.com/api"
NASDAQ_WEB_BASE = "https://www.nasdaq.com/api"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:85.0) Gecko/20100101 Firefox/85.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_symbol_info(symbol: str, asset_class: str = "stocks") -> Optional[Dict[str, Any]]:
    """
    Fetch basic quote information for a symbol.

    Args:
        symbol: Stock ticker symbol.
        asset_class: Asset class (default: stocks).

    Returns:
        Dictionary containing quote info, or None if request fails.
    """
    url = f"{NASDAQ_API_BASE}/quote/{symbol}/info"
    params = {"assetclass": asset_class}

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("data")
    except requests.RequestException as e:
        logger.error(f"Failed to fetch info for {symbol}: {e}")
        return None
    except ValueError as e:
        logger.error(f"Failed to parse JSON for {symbol} info: {e}")
        return None


def fetch_symbol_dividends(symbol: str, asset_class: str = "stocks") -> Optional[Dict[str, Any]]:
    """
    Fetch dividend information for a symbol.

    Args:
        symbol: Stock ticker symbol.
        asset_class: Asset class (default: stocks).

    Returns:
        Dictionary containing dividend data, or None if request fails.
    """
    url = f"{NASDAQ_API_BASE}/quote/{symbol}/dividends"
    params = {"assetclass": asset_class}

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("data")
    except requests.RequestException as e:
        logger.error(f"Failed to fetch dividends for {symbol}: {e}")
        return None
    except ValueError as e:
        logger.error(f"Failed to parse JSON for {symbol} dividends: {e}")
        return None


def fetch_symbol_historical(
    symbol: str,
    asset_class: str = "stocks",
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    limit: int = 10,
) -> Optional[Dict[str, Any]]:
    """
    Fetch historical price data for a symbol.

    Args:
        symbol: Stock ticker symbol.
        asset_class: Asset class (default: stocks).
        from_date: Start date in YYYY-MM-DD format (default: 30 days ago).
        to_date: End date in YYYY-MM-DD format (default: today).
        limit: Number of records to return.

    Returns:
        Dictionary containing historical data, or None if request fails.
    """
    url = f"{NASDAQ_API_BASE}/quote/{symbol}/historical"

    # Default date range: last 30 days
    if not to_date:
        to_date = datetime.now().strftime("%Y-%m-%d")
    if not from_date:
        from_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    params = {
        "assetclass": asset_class,
        "fromdate": from_date,
        "todate": to_date,
        "limit": str(limit),
    }

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("data")
    except requests.RequestException as e:
        logger.error(f"Failed to fetch historical data for {symbol}: {e}")
        return None
    except ValueError as e:
        logger.error(f"Failed to parse JSON for {symbol} historical: {e}")
        return None


def fetch_company_historical_nocp(
    symbol: str, timeframe: str = "d5"
) -> Optional[Dict[str, Any]]:
    """
    Fetch company historical data without corporate actions.

    Args:
        symbol: Stock ticker symbol.
        timeframe: Time frame (d5=5 days, m1=1 month, m3=3 months, y1=1 year, etc.).

    Returns:
        Dictionary containing historical data, or None if request fails.
    """
    url = f"{NASDAQ_API_BASE}/company/{symbol}/historical-nocp"
    params = {"timeframe": timeframe}

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("data")
    except requests.RequestException as e:
        logger.error(f"Failed to fetch historical-nocp for {symbol}: {e}")
        return None
    except ValueError as e:
        logger.error(f"Failed to parse JSON for {symbol} historical-nocp: {e}")
        return None


def fetch_company_financials(
    symbol: str, frequency: int = 1
) -> Optional[Dict[str, Any]]:
    """
    Fetch company financial statements.

    Args:
        symbol: Stock ticker symbol.
        frequency: 1 for annual, 2 for quarterly.

    Returns:
        Dictionary containing financial data, or None if request fails.
    """
    url = f"{NASDAQ_API_BASE}/company/{symbol}/financials"
    params = {"frequency": str(frequency)}

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("data")
    except requests.RequestException as e:
        logger.error(f"Failed to fetch financials for {symbol}: {e}")
        return None
    except ValueError as e:
        logger.error(f"Failed to parse JSON for {symbol} financials: {e}")
        return None


def fetch_analyst_peg_ratio(symbol: str) -> Optional[Dict[str, Any]]:
    """
    Fetch analyst PEG ratio data for a symbol.

    Args:
        symbol: Stock ticker symbol.

    Returns:
        Dictionary containing PEG ratio data, or None if request fails.
    """
    url = f"{NASDAQ_API_BASE}/analyst/{symbol}/peg-ratio"

    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("data")
    except requests.RequestException as e:
        logger.error(f"Failed to fetch PEG ratio for {symbol}: {e}")
        return None
    except ValueError as e:
        logger.error(f"Failed to parse JSON for {symbol} PEG ratio: {e}")
        return None


def fetch_short_interest(symbol: str, asset_class: str = "stocks") -> Optional[Dict[str, Any]]:
    """
    Fetch short interest data for a symbol.

    Args:
        symbol: Stock ticker symbol.
        asset_class: Asset class (default: stocks).

    Returns:
        Dictionary containing short interest data, or None if request fails.
    """
    url = f"{NASDAQ_API_BASE}/quote/{symbol}/short-interest"
    params = {"assetClass": asset_class}

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("data")
    except requests.RequestException as e:
        logger.error(f"Failed to fetch short interest for {symbol}: {e}")
        return None
    except ValueError as e:
        logger.error(f"Failed to parse JSON for {symbol} short interest: {e}")
        return None


def fetch_institutional_holdings(
    symbol: str,
    limit: int = 10,
    holding_type: str = "TOTAL",
    sort_column: str = "marketValue",
) -> Optional[Dict[str, Any]]:
    """
    Fetch institutional holdings for a symbol.

    Args:
        symbol: Stock ticker symbol.
        limit: Number of records to return.
        holding_type: Type of holdings (TOTAL, NEW, INCREASED, etc.).
        sort_column: Column to sort by (marketValue, shares, etc.).

    Returns:
        Dictionary containing institutional holdings, or None if request fails.
    """
    url = f"{NASDAQ_API_BASE}/company/{symbol}/institutional-holdings"
    params = {
        "limit": str(limit),
        "type": holding_type,
        "sortColumn": sort_column,
    }

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("data")
    except requests.RequestException as e:
        logger.error(f"Failed to fetch institutional holdings for {symbol}: {e}")
        return None
    except ValueError as e:
        logger.error(f"Failed to parse JSON for {symbol} institutional holdings: {e}")
        return None


def fetch_insider_trades(
    symbol: str,
    limit: int = 10,
    trade_type: str = "all",
    sort_column: str = "lastDate",
    sort_order: str = "DESC",
) -> Optional[Dict[str, Any]]:
    """
    Fetch insider trading data for a symbol.

    Args:
        symbol: Stock ticker symbol.
        limit: Number of records to return.
        trade_type: Type of trades (all, buy, sell).
        sort_column: Column to sort by (lastDate, shares, etc.).
        sort_order: Sort order (ASC or DESC).

    Returns:
        Dictionary containing insider trades, or None if request fails.
    """
    url = f"{NASDAQ_API_BASE}/company/{symbol}/insider-trades"
    params = {
        "limit": str(limit),
        "type": trade_type,
        "sortColumn": sort_column,
        "sortOrder": sort_order,
    }

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("data")
    except requests.RequestException as e:
        logger.error(f"Failed to fetch insider trades for {symbol}: {e}")
        return None
    except ValueError as e:
        logger.error(f"Failed to parse JSON for {symbol} insider trades: {e}")
        return None


def fetch_sec_filings(
    symbol: str,
    limit: int = 14,
    sort_column: str = "filed",
    sort_order: str = "desc",
) -> Optional[Dict[str, Any]]:
    """
    Fetch SEC filings for a symbol.

    Args:
        symbol: Stock ticker symbol.
        limit: Number of records to return.
        sort_column: Column to sort by (filed, etc.).
        sort_order: Sort order (asc or desc).

    Returns:
        Dictionary containing SEC filings, or None if request fails.
    """
    url = f"{NASDAQ_API_BASE}/company/{symbol}/sec-filings"
    params = {
        "limit": str(limit),
        "sortColumn": sort_column,
        "sortOrder": sort_order,
        "IsQuoteMedia": "true",
    }

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("data")
    except requests.RequestException as e:
        logger.error(f"Failed to fetch SEC filings for {symbol}: {e}")
        return None
    except ValueError as e:
        logger.error(f"Failed to parse JSON for {symbol} SEC filings: {e}")
        return None


def fetch_press_releases(
    symbol: str,
    asset_class: str = "stocks",
    limit: int = 10,
    offset: int = 0,
) -> Optional[Dict[str, Any]]:
    """
    Fetch press releases for a symbol.

    Args:
        symbol: Stock ticker symbol.
        asset_class: Asset class (default: stocks).
        limit: Number of records to return.
        offset: Offset for pagination.

    Returns:
        Dictionary containing press releases, or None if request fails.
    """
    url = f"{NASDAQ_WEB_BASE}/news/topic/press_release"
    params = {
        "q": f"symbol:{symbol.lower()}|assetclass:{asset_class}",
        "limit": str(limit),
        "offset": str(offset),
    }

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("data")
    except requests.RequestException as e:
        logger.error(f"Failed to fetch press releases for {symbol}: {e}")
        return None
    except ValueError as e:
        logger.error(f"Failed to parse JSON for {symbol} press releases: {e}")
        return None


def fetch_news_articles(
    symbol: str,
    asset_class: str = "STOCKS",
    limit: int = 10,
    offset: int = 0,
    fallback: bool = True,
) -> Optional[Dict[str, Any]]:
    """
    Fetch news articles for a symbol.

    Args:
        symbol: Stock ticker symbol.
        asset_class: Asset class (default: STOCKS, uppercase).
        limit: Number of records to return.
        offset: Offset for pagination.
        fallback: Enable fallback to general market news.

    Returns:
        Dictionary containing news articles, or None if request fails.
    """
    url = f"{NASDAQ_WEB_BASE}/news/topic/articlebysymbol"
    params = {
        "q": f"{symbol.upper()}|{asset_class.upper()}",
        "offset": str(offset),
        "limit": str(limit),
        "fallback": "true" if fallback else "false",
    }

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("data")
    except requests.RequestException as e:
        logger.error(f"Failed to fetch news articles for {symbol}: {e}")
        return None
    except ValueError as e:
        logger.error(f"Failed to parse JSON for {symbol} news articles: {e}")
        return None


def fetch_all_symbol_data(symbol: str) -> Dict[str, Any]:
    """
    Fetch all available data for a symbol from NASDAQ API.

    Args:
        symbol: Stock ticker symbol.

    Returns:
        Dictionary containing all data categories:
        {
            "info": {...},
            "dividends": {...},
            "historical": {...},
            "historical_5d": {...},
            "historical_1m": {...},
            "financials_annual": {...},
            "financials_quarterly": {...},
            "peg_ratio": {...},
            "short_interest": {...},
            "institutional_holdings": {...},
            "insider_trades": {...},
            "sec_filings": {...},
            "press_releases": {...},
            "news_articles": {...}
        }
    """

    data = {
        "symbol": symbol,
        "fetched_at": datetime.now().isoformat(),
        "info": fetch_symbol_info(symbol),
        "dividends": fetch_symbol_dividends(symbol),
        "historical": fetch_symbol_historical(symbol, limit=100),
        "historical_5d": fetch_company_historical_nocp(symbol, timeframe="d5"),
        "historical_1m": fetch_company_historical_nocp(symbol, timeframe="m1"),
        "financials_annual": fetch_company_financials(symbol, frequency=1),
        "financials_quarterly": fetch_company_financials(symbol, frequency=2),
        "peg_ratio": fetch_analyst_peg_ratio(symbol),
        "short_interest": fetch_short_interest(symbol),
        "institutional_holdings": fetch_institutional_holdings(symbol, limit=50),
        "insider_trades": fetch_insider_trades(symbol, limit=50),
        "sec_filings": fetch_sec_filings(symbol, limit=50),
        "press_releases": fetch_press_releases(symbol, limit=50),
        "news_articles": fetch_news_articles(symbol, limit=50),
    }

    # Count successful fetches
    successful = sum(1 for v in data.values() if v is not None and v not in [symbol, data["fetched_at"]])
    logger.info(f"Successfully fetched {successful}/14 data categories for {symbol}")

    return data
