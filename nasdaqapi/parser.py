"""Response parser for NASDAQ API data."""

from typing import Dict, Any, List, Optional
import re


class ResponseParser:
    """Parse and normalize NASDAQ API responses."""
    
    @staticmethod
    def _parse_number(value: Any) -> Optional[float]:
        """Parse number from string, handling $, %, commas."""
        if value is None or value == "":
            return None
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            # Remove $, %, commas
            cleaned = value.replace("$", "").replace("%", "").replace(",", "").strip()
            if cleaned in ("N/A", "NA", "--", ""):
                return None
            try:
                return float(cleaned)
            except ValueError:
                return None
        return None
    
    @staticmethod
    def _parse_percentage(value: Any) -> Optional[float]:
        """Parse percentage to decimal (e.g., '10%' -> 0.10)."""
        num = ResponseParser._parse_number(value)
        return num / 100 if num is not None else None
    
    def parse_quote(self, data: Dict, symbol: str) -> Dict[str, Any]:
        """Parse quote data."""
        if not data:
            return {}
        
        primary = data.get("primaryData", {})
        secondary = data.get("secondaryData", {})
        key_stats = data.get("keyStats", {})
        
        # Parse 52-week range
        range_str = key_stats.get("fiftyTwoWeekHighLow", {}).get("value", "")
        week_52_high, week_52_low = None, None
        if range_str:
            match = re.search(r'([\d.]+)\s*-\s*([\d.]+)', range_str)
            if match:
                week_52_low = self._parse_number(match.group(1))
                week_52_high = self._parse_number(match.group(2))
        
        return {
            "symbol": symbol,
            "company_name": data.get("companyName"),
            "price": self._parse_number(primary.get("lastSalePrice")),
            "change": self._parse_number(primary.get("netChange")),
            "change_percent": self._parse_percentage(primary.get("percentageChange")),
            "volume": self._parse_number(primary.get("volume")),
            "bid": self._parse_number(primary.get("bidPrice")),
            "ask": self._parse_number(primary.get("askPrice")),
            "previous_close": self._parse_number(secondary.get("lastSalePrice")),
            "week_52_high": week_52_high,
            "week_52_low": week_52_low,
            "market_status": data.get("marketStatus"),
            "timestamp": primary.get("lastTradeTimestamp"),
        }
    
    def parse_financials(self, data: Dict) -> Dict[str, Any]:
        """Parse financial statements."""
        if not data:
            return {}
        
        def parse_statement(table_data):
            """Parse a financial statement table."""
            if not table_data or "rows" not in table_data:
                return []
            
            statements = []
            for row in table_data["rows"]:
                statement = {"line_item": row.get("label")}
                # Parse all year columns
                for key, value in row.items():
                    if key != "label":
                        statement[key] = self._parse_number(value)
                statements.append(statement)
            return statements
        
        return {
            "income_statement": parse_statement(data.get("incomeStatementTable")),
            "balance_sheet": parse_statement(data.get("balanceSheetTable")),
            "cash_flow": parse_statement(data.get("cashFlowTable")),
            "ratios": parse_statement(data.get("financialRatiosTable")),
        }
    
    def parse_dividends(self, data: Dict) -> Dict[str, Any]:
        """Parse dividend data."""
        if not data:
            return {}
        
        history = []
        div_data = data.get("dividends") or {}
        rows = div_data.get("rows") or []
        
        for row in rows:
            history.append({
                "ex_date": row.get("exOrEffDate"),
                "amount": self._parse_number(row.get("amount")),
                "type": row.get("type", "").lower(),
                "payment_date": row.get("paymentDate"),
            })
        
        return {
            "yield": self._parse_percentage(data.get("yield")),
            "annual_amount": self._parse_number(data.get("annualizedDividend")),
            "payout_ratio": self._parse_percentage(data.get("payoutRatio")),
            "ex_dividend_date": data.get("exDividendDate"),
            "payment_date": data.get("dividendPaymentDate"),
            "history": history,
        }
    
    def parse_ownership(
        self, 
        institutional_data: Optional[Dict],
        insider_data: Optional[Dict]
    ) -> Dict[str, Any]:
        """Parse ownership data."""
        result = {
            "institutional": {
                "summary": {},
                "top_holders": []
            },
            "insider_trades": []
        }
        
        # Institutional
        if institutional_data:
            summary = institutional_data.get("ownershipSummary", {})
            
            shares_out = summary.get("ShareoutstandingTotal", {}).get("value", "")
            inst_pct = summary.get("SharesOutstandingPCT", {}).get("value", "")
            
            result["institutional"]["summary"] = {
                "shares_outstanding_millions": self._parse_number(shares_out),
                "institutional_ownership_percent": self._parse_percentage(inst_pct),
            }
            
            # Top holders
            table = institutional_data.get("holdingsTransactions", {}).get("table", {})
            for row in table.get("rows", [])[:10]:  # Top 10
                result["institutional"]["top_holders"].append({
                    "institution": row.get("ownerName"),
                    "shares": self._parse_number(row.get("sharesHeld")),
                    "value_thousands": self._parse_number(row.get("marketValue")),
                    "change_percent": self._parse_percentage(row.get("sharesChangePCT")),
                    "date": row.get("date"),
                })
        
        # Insider trades
        if insider_data:
            table = insider_data.get("transactionTable", {})
            for row in table.get("rows", [])[:20]:  # Last 20 trades
                result["insider_trades"].append({
                    "insider": row.get("insiderName"),
                    "relationship": row.get("relationship"),
                    "transaction_type": row.get("transactionType"),
                    "shares": self._parse_number(row.get("sharesTraded")),
                    "price": self._parse_number(row.get("lastPrice")),
                    "date": row.get("lastDate"),
                })
        
        return result
    
    def parse_historical(self, data: Dict) -> List[Dict[str, Any]]:
        """Parse historical price data."""
        if not data or "tradesTable" not in data:
            return []
        
        prices = []
        for row in data["tradesTable"].get("rows", []):
            prices.append({
                "date": row.get("date"),
                "open": self._parse_number(row.get("open")),
                "high": self._parse_number(row.get("high")),
                "low": self._parse_number(row.get("low")),
                "close": self._parse_number(row.get("close")),
                "volume": self._parse_number(row.get("volume")),
            })
        return prices
    
    def parse_news(self, data: Dict) -> List[Dict[str, Any]]:
        """Parse news articles."""
        if not data or "data" not in data:
            return []
        
        articles = []
        rows = data["data"].get("rows") if isinstance(data["data"], dict) else data["data"]
        
        if isinstance(rows, list):
            for article in rows[:20]:  # Limit to 20 articles
                articles.append({
                    "title": article.get("title"),
                    "summary": article.get("summary"),
                    "url": article.get("url"),
                    "published_date": article.get("publishedDate") or article.get("published"),
                    "source": article.get("providerName") or article.get("source"),
                })
        
        return articles
    
    def parse_analyst(self, data: Dict) -> Dict[str, Any]:
        """Parse analyst ratings."""
        if not data:
            return {}
        
        peg_data = data.get("pegRatio", {})
        
        return {
            "peg_ratio": self._parse_number(peg_data.get("value")),
            "pe_ratio": self._parse_number(peg_data.get("peRatio")),
            "growth_rate": self._parse_percentage(peg_data.get("growthRate")),
        }
    
    def parse_short_interest(self, data: Dict) -> Dict[str, Any]:
        """Parse short interest data."""
        if not data or "shortInterestTable" not in data:
            return {}
        
        table = data["shortInterestTable"]
        rows = table.get("rows", [])
        
        if not rows:
            return {}
        
        latest = rows[0] if rows else {}
        
        return {
            "shares_short": self._parse_number(latest.get("shortInterest")),
            "short_percent_float": self._parse_percentage(latest.get("percentOfFloat")),
            "short_percent_outstanding": self._parse_percentage(latest.get("percentOfSharesOut")),
            "average_daily_volume": self._parse_number(latest.get("averageDailyShareVolume")),
            "settlement_date": latest.get("settlementDate"),
        }
    
    def parse_screener(self, symbols: List[Dict]) -> List[Dict[str, Any]]:
        """Parse screener results."""
        parsed = []
        for symbol in symbols:
            parsed.append({
                "symbol": symbol.get("symbol"),
                "name": symbol.get("name"),
                "sector": symbol.get("sector"),
                "industry": symbol.get("industry"),
                "market_cap": self._parse_number(symbol.get("marketCap")),
                "last_sale": self._parse_number(symbol.get("lastsale")),
                "volume": self._parse_number(symbol.get("volume")),
                "exchange": symbol.get("exchange"),
            })
        return parsed
