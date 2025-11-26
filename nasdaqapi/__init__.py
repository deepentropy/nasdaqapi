"""NASDAQ API Data Retrieval System.

A system to retrieve ticker data from NASDAQ API for all US exchanges.
"""

from .api import (
    fetch_nasdaq_tickers,
    fetch_all_nasdaq_tickers,
    fetch_all_exchanges,
    get_unique_symbols,
)

from .symbol import (
    fetch_symbol_info,
    fetch_symbol_dividends,
    fetch_symbol_historical,
    fetch_company_historical_nocp,
    fetch_company_financials,
    fetch_analyst_peg_ratio,
    fetch_short_interest,
    fetch_institutional_holdings,
    fetch_insider_trades,
    fetch_sec_filings,
    fetch_press_releases,
    fetch_news_articles,
    fetch_all_symbol_data,
)

from .normalizer import (
    normalize_nasdaq_data,
)

__version__ = "0.1.0"

__all__ = [
    # Ticker list functions
    "fetch_nasdaq_tickers",
    "fetch_all_nasdaq_tickers",
    "fetch_all_exchanges",
    "get_unique_symbols",
    # Symbol data functions
    "fetch_symbol_info",
    "fetch_symbol_dividends",
    "fetch_symbol_historical",
    "fetch_company_historical_nocp",
    "fetch_company_financials",
    "fetch_analyst_peg_ratio",
    "fetch_short_interest",
    "fetch_institutional_holdings",
    "fetch_insider_trades",
    "fetch_sec_filings",
    "fetch_press_releases",
    "fetch_news_articles",
    "fetch_all_symbol_data",
    # Normalizer
    "normalize_nasdaq_data",
]


