"""NASDAQ API endpoints configuration."""


class Endpoints:
    """NASDAQ API endpoint URLs."""
    
    API_BASE = "https://api.nasdaq.com/api"
    WEB_BASE = "https://www.nasdaq.com/api"
    
    def screener(self) -> str:
        """Stock screener endpoint."""
        return f"{self.API_BASE}/screener/stocks"
    
    def quote_info(self, symbol: str) -> str:
        """Quote information endpoint."""
        return f"{self.API_BASE}/quote/{symbol}/info"
    
    def dividends(self, symbol: str) -> str:
        """Dividend data endpoint."""
        return f"{self.API_BASE}/quote/{symbol}/dividends"
    
    def historical(self, symbol: str) -> str:
        """Historical prices endpoint."""
        return f"{self.API_BASE}/quote/{symbol}/historical"
    
    def financials(self, symbol: str) -> str:
        """Financial statements endpoint."""
        return f"{self.API_BASE}/company/{symbol}/financials"
    
    def institutional_holdings(self, symbol: str) -> str:
        """Institutional holdings endpoint."""
        return f"{self.API_BASE}/company/{symbol}/institutional-holdings"
    
    def insider_trades(self, symbol: str) -> str:
        """Insider trades endpoint."""
        return f"{self.API_BASE}/company/{symbol}/insider-trades"
    
    def peg_ratio(self, symbol: str) -> str:
        """PEG ratio and analyst data endpoint."""
        return f"{self.API_BASE}/analyst/{symbol}/peg-ratio"
    
    def short_interest(self, symbol: str) -> str:
        """Short interest endpoint."""
        return f"{self.API_BASE}/quote/{symbol}/short-interest"
    
    def sec_filings(self, symbol: str) -> str:
        """SEC filings endpoint."""
        return f"{self.API_BASE}/company/{symbol}/sec-filings"
    
    def press_releases(self, symbol: str) -> str:
        """Press releases endpoint."""
        return f"{self.WEB_BASE}/news/topic/press_release"
    
    def news(self, symbol: str) -> str:
        """News articles endpoint."""
        return f"{self.WEB_BASE}/news/topic/articlebysymbol"
