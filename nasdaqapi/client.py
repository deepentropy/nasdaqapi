"""NASDAQ API Client - Main interface."""

import requests
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from .endpoints import Endpoints
from .parser import ResponseParser

logger = logging.getLogger(__name__)


class NasdaqClient:
    """
    Clean interface to NASDAQ's public API.
    
    Example:
        >>> client = NasdaqClient()
        >>> quote = client.get_quote('AAPL')
        >>> print(f"Price: ${quote['price']}")
    """
    
    def __init__(self, timeout: int = 30):
        """
        Initialize NASDAQ API client.
        
        Args:
            timeout: Request timeout in seconds (default: 30)
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
        })
        self.endpoints = Endpoints()
        self.parser = ResponseParser()
    
    def _request(self, url: str, params: Dict[str, Any] = None) -> Optional[Dict]:
        """Make HTTP request with error handling."""
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return data.get("data")
        except requests.RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            return None
        except ValueError as e:
            logger.error(f"JSON parse error for {url}: {e}")
            return None
    
    # ========== Core Data Methods ==========
    
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Get current quote for a symbol.
        
        Args:
            symbol: Stock ticker (e.g., 'AAPL')
            
        Returns:
            Normalized quote data with keys: symbol, price, change, volume, etc.
        """
        url = self.endpoints.quote_info(symbol)
        raw_data = self._request(url, {"assetclass": "stocks"})
        return self.parser.parse_quote(raw_data, symbol) if raw_data else {}
    
    def get_financials(self, symbol: str, period: str = 'annual') -> Dict[str, Any]:
        """
        Get financial statements.
        
        Args:
            symbol: Stock ticker
            period: 'annual' or 'quarterly'
            
        Returns:
            Financial data with income_statement, balance_sheet, cash_flow
        """
        frequency = 1 if period == 'annual' else 2
        url = self.endpoints.financials(symbol)
        raw_data = self._request(url, {"frequency": frequency})
        return self.parser.parse_financials(raw_data) if raw_data else {}
    
    def get_dividends(self, symbol: str) -> Dict[str, Any]:
        """
        Get dividend information.
        
        Args:
            symbol: Stock ticker
            
        Returns:
            Dividend data with yield, payment_date, history, etc.
        """
        url = self.endpoints.dividends(symbol)
        raw_data = self._request(url, {"assetclass": "stocks"})
        return self.parser.parse_dividends(raw_data) if raw_data else {}
    
    def get_ownership(self, symbol: str) -> Dict[str, Any]:
        """
        Get institutional ownership and insider trades.
        
        Args:
            symbol: Stock ticker
            
        Returns:
            Ownership data with institutional_holders, insider_trades
        """
        # Institutional holdings
        inst_url = self.endpoints.institutional_holdings(symbol)
        inst_data = self._request(inst_url, {
            "limit": 50,
            "type": "TOTAL",
            "sortColumn": "marketValue"
        })
        
        # Insider trades
        insider_url = self.endpoints.insider_trades(symbol)
        insider_data = self._request(insider_url, {
            "limit": 50,
            "type": "all",
            "sortColumn": "lastDate",
            "sortOrder": "DESC"
        })
        
        return self.parser.parse_ownership(inst_data, insider_data)
    
    def get_historical(
        self, 
        symbol: str, 
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        period: str = '1month'
    ) -> List[Dict[str, Any]]:
        """
        Get historical price data.
        
        Args:
            symbol: Stock ticker
            from_date: Start date YYYY-MM-DD (optional)
            to_date: End date YYYY-MM-DD (optional)
            period: '1day', '5day', '1month', '3month', '1year' (default: '1month')
            
        Returns:
            List of daily price records
        """
        if not to_date:
            to_date = datetime.now().strftime("%Y-%m-%d")
        if not from_date:
            days_map = {'1day': 1, '5day': 5, '1month': 30, '3month': 90, '1year': 365}
            days = days_map.get(period, 30)
            from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        url = self.endpoints.historical(symbol)
        raw_data = self._request(url, {
            "assetclass": "stocks",
            "fromdate": from_date,
            "todate": to_date,
            "limit": 100
        })
        return self.parser.parse_historical(raw_data) if raw_data else []
    
    def get_news(self, symbol: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get news articles for a symbol.
        
        Args:
            symbol: Stock ticker
            limit: Number of articles (max 50)
            
        Returns:
            List of news articles
        """
        url = self.endpoints.news(symbol)
        raw_data = self._request(url, {
            "q": f"{symbol}|STOCKS",
            "offset": 0,
            "limit": min(limit, 50),
            "fallback": "true"
        })
        return self.parser.parse_news(raw_data) if raw_data else []
    
    def get_analyst_ratings(self, symbol: str) -> Dict[str, Any]:
        """Get analyst ratings and price targets."""
        url = self.endpoints.peg_ratio(symbol)
        raw_data = self._request(url)
        return self.parser.parse_analyst(raw_data) if raw_data else {}
    
    def get_short_interest(self, symbol: str) -> Dict[str, Any]:
        """Get short interest data."""
        url = self.endpoints.short_interest(symbol)
        raw_data = self._request(url, {"assetClass": "stocks"})
        return self.parser.parse_short_interest(raw_data) if raw_data else {}
    
    # ========== Convenience Methods ==========
    
    def get_symbol_data(
        self, 
        symbol: str, 
        include: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get comprehensive data for a symbol.
        
        Args:
            symbol: Stock ticker
            include: List of categories to include. If None, includes all.
                    Options: ['quote', 'financials', 'dividends', 'ownership',
                             'historical', 'news', 'analyst', 'short_interest']
        
        Returns:
            Dictionary with all requested data
        """
        if include is None:
            include = ['quote', 'financials', 'dividends', 'ownership', 
                      'historical', 'news', 'analyst', 'short_interest']
        
        result = {"symbol": symbol, "fetched_at": datetime.now().isoformat()}
        
        method_map = {
            'quote': self.get_quote,
            'financials': self.get_financials,
            'dividends': self.get_dividends,
            'ownership': self.get_ownership,
            'historical': self.get_historical,
            'news': self.get_news,
            'analyst': self.get_analyst_ratings,
            'short_interest': self.get_short_interest,
        }
        
        for category in include:
            if category in method_map:
                try:
                    result[category] = method_map[category](symbol)
                except Exception as e:
                    logger.error(f"Failed to fetch {category} for {symbol}: {e}")
                    result[category] = {}
        
        return result
    
    def search_symbols(
        self, 
        exchange: Optional[str] = None,
        sector: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for symbols.
        
        Args:
            exchange: Filter by exchange ('NASDAQ', 'NYSE', 'AMEX')
            sector: Filter by sector
            
        Returns:
            List of symbols with basic info
        """
        url = self.endpoints.screener()
        params = {
            "tableonly": "true",
            "limit": "10000",
            "download": "true"
        }
        
        if exchange:
            params["exchange"] = exchange.lower()
        
        raw_data = self._request(url, params)
        
        if not raw_data or "rows" not in raw_data:
            return []
        
        symbols = raw_data["rows"]
        
        # Filter by sector if provided
        if sector:
            symbols = [s for s in symbols if s.get("sector", "").lower() == sector.lower()]
        
        return self.parser.parse_screener(symbols)
    
    def __enter__(self):
        """Context manager support."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close session on exit."""
        self.session.close()
