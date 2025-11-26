"""Fetcher for NASDAQ stock data from NASDAQ API."""

import requests
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

NASDAQ_API_URL = "https://api.nasdaq.com/api/screener/stocks"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:85.0) Gecko/20100101 Firefox/85.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

EXCHANGES = ["nasdaq", "nyse", "amex"]


def fetch_nasdaq_tickers(
    exchange: str = "nasdaq",
    limit: int = 25,
    offset: int = 0,
    download: bool = True,
) -> Optional[Dict[str, Any]]:
    """
    Fetch ticker data from NASDAQ API for a specific exchange.

    Args:
        exchange: Exchange name (nasdaq, nyse, amex).
        limit: Number of results per request.
        offset: Offset for pagination.
        download: Whether to request download format (gets all data).

    Returns:
        Dictionary containing API response data, or None if request fails.
    """
    params = {
        "tableonly": "true",
        "limit": str(limit),
        "offset": str(offset),
        "exchange": exchange.lower(),
        "download": "true" if download else "false",
    }

    try:
        logger.info(f"Fetching {exchange.upper()} tickers from NASDAQ API (offset={offset}, limit={limit})")
        response = requests.get(NASDAQ_API_URL, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()

        data = response.json()
        return data

    except requests.RequestException as e:
        logger.error(f"Failed to fetch {exchange.upper()} tickers: {e}")
        return None
    except ValueError as e:
        logger.error(f"Failed to parse JSON for {exchange.upper()}: {e}")
        return None


def fetch_all_nasdaq_tickers(exchange: str = "nasdaq") -> List[Dict[str, Any]]:
    """
    Fetch all tickers for a given exchange using pagination.

    Args:
        exchange: Exchange name (nasdaq, nyse, amex).

    Returns:
        List of ticker dictionaries.
    """
    all_tickers = []
    offset = 0
    limit = 10000  # Large limit to get all data in one request when download=true

    # With download=true, NASDAQ API returns all data regardless of limit/offset
    data = fetch_nasdaq_tickers(exchange=exchange, limit=limit, offset=offset, download=True)

    if data and "data" in data and "rows" in data["data"]:
        tickers = data["data"]["rows"]
        all_tickers.extend(tickers)
        logger.info(f"Fetched {len(tickers)} tickers from {exchange.upper()}")
    else:
        logger.warning(f"No data returned for {exchange.upper()}")

    return all_tickers


def fetch_all_exchanges() -> List[Dict[str, Any]]:
    """
    Fetch ticker lists from NASDAQ API for all exchanges.

    Returns:
        List of ticker dictionaries with exchange information added.
        Each ticker contains: symbol, name, lastsale, netchange, pctchange,
        volume, marketCap, country, ipoyear, industry, sector, url, exchange.

    Raises:
        Exception: If unable to fetch any ticker lists.
    """
    all_tickers = []
    successful_exchanges = []

    for exchange in EXCHANGES:
        try:
            tickers = fetch_all_nasdaq_tickers(exchange)

            # Add exchange information to each ticker (uppercase for consistency)
            for ticker in tickers:
                ticker["exchange"] = exchange.upper()

            all_tickers.extend(tickers)
            successful_exchanges.append(exchange.upper())
            logger.info(f"Successfully fetched {len(tickers)} tickers from {exchange.upper()}")

        except Exception as e:
            logger.error(f"Failed to fetch {exchange.upper()} ticker list: {e}")
            continue

    if not all_tickers:
        raise Exception("Failed to fetch any ticker lists from NASDAQ API")

    logger.info(f"Total tickers fetched: {len(all_tickers)} from exchanges: {', '.join(successful_exchanges)}")

    return all_tickers


def get_unique_symbols(tickers: List[Dict[str, Any]]) -> List[str]:
    """
    Extract unique symbols from ticker list.

    Args:
        tickers: List of ticker dictionaries.

    Returns:
        List of unique ticker symbols.
    """
    symbols = list(dict.fromkeys(ticker["symbol"] for ticker in tickers))
    return symbols
