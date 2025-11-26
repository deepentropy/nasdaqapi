"""Data normalizer for NASDAQ API responses."""

import re
import logging
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

logger = logging.getLogger(__name__)


def parse_price(value: str) -> Optional[float]:
    """Convert price string to float."""
    if not value or value in ["", "N/A", "NA", "-", "null"]:
        return None
    try:
        # Remove $, commas, and spaces
        cleaned = value.replace("$", "").replace(",", "").strip()
        return float(cleaned)
    except (ValueError, AttributeError):
        return None


def parse_percentage(value: str) -> Optional[float]:
    """Convert percentage string to decimal."""
    if not value or value in ["", "N/A", "NA", "-", "null"]:
        return None
    try:
        # Remove % and convert to decimal
        cleaned = value.replace("%", "").strip()
        return float(cleaned) / 100.0
    except (ValueError, AttributeError):
        return None


def parse_volume(value: str) -> Optional[int]:
    """Convert volume string to integer."""
    if not value or value in ["", "N/A", "NA", "-", "null"]:
        return None
    try:
        # Remove commas and convert
        cleaned = value.replace(",", "").strip()
        return int(float(cleaned))
    except (ValueError, AttributeError):
        return None


def parse_range(value: str) -> Optional[Dict[str, float]]:
    """Parse range string into low/high dict."""
    if not value or value in ["", "N/A", "NA", "-"]:
        return None
    try:
        # Split on dash or hyphen
        parts = re.split(r'\s*-\s*', value)
        if len(parts) == 2:
            return {
                "low": parse_price(parts[0]),
                "high": parse_price(parts[1])
            }
    except:
        pass
    return None


def normalize_metadata(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and normalize metadata."""
    info = raw_data.get("info", {})
    
    return {
        "symbol": raw_data.get("symbol"),
        "fetched_at": raw_data.get("fetched_at"),
        "company_name": info.get("companyName"),
        "stock_type": info.get("stockType"),
        "exchange": info.get("exchange"),
        "asset_class": info.get("assetClass"),
        "market_status": info.get("marketStatus"),
        "is_nasdaq_listed": info.get("isNasdaqListed"),
        "is_nasdaq_100": info.get("isNasdaq100"),
    }


def normalize_quote(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and normalize quote data."""
    info = raw_data.get("info", {})
    primary = info.get("primaryData", {})
    secondary = info.get("secondaryData", {})
    
    return {
        "price": parse_price(primary.get("lastSalePrice")),
        "change": parse_price(primary.get("netChange")),
        "change_percent": parse_percentage(primary.get("percentageChange")),
        "volume": parse_volume(primary.get("volume")),
        "bid": parse_price(primary.get("bidPrice")),
        "ask": parse_price(primary.get("askPrice")),
        "bid_size": parse_volume(primary.get("bidSize")),
        "ask_size": parse_volume(primary.get("askSize")),
        "previous_close": parse_price(secondary.get("lastSalePrice")),
        "timestamp": primary.get("lastTradeTimestamp"),
        "is_realtime": primary.get("isRealTime"),
    }


def normalize_key_metrics(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and normalize key metrics."""
    info = raw_data.get("info", {})
    key_stats = info.get("keyStats", {})
    dividends = raw_data.get("dividends", {})
    
    # Parse 52-week range
    range_str = key_stats.get("fiftyTwoWeekHighLow", {}).get("value", "")
    week_range = parse_range(range_str)
    
    # Get shares outstanding from institutional holdings data (in millions)
    inst_data = raw_data.get("institutional_holdings", {})
    ownership_summary = inst_data.get("ownershipSummary", {})
    shares_out_data = ownership_summary.get("ShareoutstandingTotal", {})
    shares_out_str = shares_out_data.get("value", "") if isinstance(shares_out_data, dict) else ""
    shares_outstanding_millions = parse_volume(shares_out_str)
    
    # Convert to actual shares (multiply by 1 million if we have data)
    shares_outstanding = None
    if shares_outstanding_millions:
        shares_outstanding = int(shares_outstanding_millions * 1_000_000)
    
    return {
        "pe_ratio": parse_price(dividends.get("payoutRatio")),
        "week_52_high": week_range.get("high") if week_range else None,
        "week_52_low": week_range.get("low") if week_range else None,
        "dividend_yield": parse_percentage(dividends.get("yield")),
        "market_cap": None,  # Not in current data
        "avg_volume": None,  # Not in current data
        "shares_outstanding": shares_outstanding,
        "shares_outstanding_millions": shares_outstanding_millions,
    }


def normalize_dividends(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and normalize dividend data."""
    div_data = raw_data.get("dividends", {})
    
    summary = {
        "yield": parse_percentage(div_data.get("yield")),
        "annual_amount": parse_price(div_data.get("annualizedDividend")),
        "payout_ratio": parse_percentage(div_data.get("payoutRatio")),
        "ex_dividend_date": div_data.get("exDividendDate"),
        "payment_date": div_data.get("dividendPaymentDate"),
    }
    
    # Normalize dividend history
    history = []
    dividends_dict = div_data.get("dividends") or {}
    div_rows = dividends_dict.get("rows") or []
    for row in div_rows:
        history.append({
            "ex_date": row.get("exOrEffDate"),
            "amount": parse_price(row.get("amount")),
            "type": row.get("type", "").lower(),
            "declaration_date": row.get("declarationDate"),
            "record_date": row.get("recordDate"),
            "payment_date": row.get("paymentDate"),
        })
    
    return {
        "summary": summary,
        "history": history
    }


def normalize_historical_prices(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and normalize historical price data."""
    result = {}
    
    # Daily historical from 'historical'
    historical = raw_data.get("historical", {})
    trades = historical.get("tradesTable", {}).get("rows", [])
    daily = []
    for row in trades:
        daily.append({
            "date": row.get("date"),
            "close": parse_price(row.get("close")),
            "volume": parse_volume(row.get("volume")),
            "open": parse_price(row.get("open")),
            "high": parse_price(row.get("high")),
            "low": parse_price(row.get("low")),
        })
    result["daily"] = daily
    
    # 5-day period
    hist_5d = raw_data.get("historical_5d", {})
    period_5d = []
    for row in hist_5d.get("nocp", {}).get("rows", []):
        period_5d.append({
            "date": row.get("date"),
            "close": parse_price(row.get("close")),
            "volume": parse_volume(row.get("volume")),
            "open": parse_price(row.get("open")),
            "high": parse_price(row.get("high")),
            "low": parse_price(row.get("low")),
        })
    result["period_5d"] = period_5d
    
    # 1-month period
    hist_1m = raw_data.get("historical_1m", {})
    period_1m = []
    for row in hist_1m.get("nocp", {}).get("rows", []):
        period_1m.append({
            "date": row.get("date"),
            "close": parse_price(row.get("close")),
            "volume": parse_volume(row.get("volume")),
            "open": parse_price(row.get("open")),
            "high": parse_price(row.get("high")),
            "low": parse_price(row.get("low")),
        })
    result["period_1m"] = period_1m
    
    return result


def normalize_financials(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and normalize financial statements."""
    annual = raw_data.get("financials_annual", {})
    quarterly = raw_data.get("financials_quarterly", {})
    
    def normalize_statement(data: Dict) -> Dict[str, List]:
        result = {
            "income_statement": [],
            "balance_sheet": [],
            "cash_flow": [],
            "financial_ratios": []
        }
        
        # Income statement
        income_rows = data.get("incomeStatementTable", {}).get("rows", [])
        for row in income_rows:
            period = {}
            for key, value in row.items():
                if key == "label":
                    period["line_item"] = value
                else:
                    period[key] = parse_price(value) if value else None
            result["income_statement"].append(period)
        
        # Balance sheet
        balance_rows = data.get("balanceSheetTable", {}).get("rows", [])
        for row in balance_rows:
            period = {}
            for key, value in row.items():
                if key == "label":
                    period["line_item"] = value
                else:
                    period[key] = parse_price(value) if value else None
            result["balance_sheet"].append(period)
        
        # Cash flow
        cash_rows = data.get("cashFlowTable", {}).get("rows", [])
        for row in cash_rows:
            period = {}
            for key, value in row.items():
                if key == "label":
                    period["line_item"] = value
                else:
                    period[key] = parse_price(value) if value else None
            result["cash_flow"].append(period)
        
        # Financial ratios (NEW!)
        ratio_rows = data.get("financialRatiosTable", {}).get("rows", [])
        for row in ratio_rows:
            ratio = {}
            for key, value in row.items():
                if key == "value1":
                    ratio["ratio_name"] = value
                else:
                    # Parse percentage values
                    ratio[key] = parse_percentage(value) if value and value else None
            result["financial_ratios"].append(ratio)
        
        return result
    
    return {
        "annual": normalize_statement(annual),
        "quarterly": normalize_statement(quarterly) if quarterly else {
            "income_statement": [], 
            "balance_sheet": [], 
            "cash_flow": [],
            "financial_ratios": []
        }
    }


def normalize_ownership(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and normalize ownership data."""
    inst_data = raw_data.get("institutional_holdings", {})
    insider_data = raw_data.get("insider_trades", {})
    
    # Institutional holdings
    institutional = {
        "summary": {},
        "top_holders": []
    }
    
    ownership_summary = inst_data.get("ownershipSummary", {})
    if ownership_summary:
        # Extract shares outstanding (in millions)
        shares_out_data = ownership_summary.get("ShareoutstandingTotal", {})
        shares_out_str = shares_out_data.get("value", "") if isinstance(shares_out_data, dict) else ""
        
        # Extract institutional ownership percentage
        inst_own_data = ownership_summary.get("SharesOutstandingPCT", {})
        inst_own_str = inst_own_data.get("value", "") if isinstance(inst_own_data, dict) else ""
        
        # Extract total value
        total_value_data = ownership_summary.get("TotalHoldingsValue", {})
        total_value_str = total_value_data.get("value", "") if isinstance(total_value_data, dict) else ""
        
        institutional["summary"] = {
            "shares_outstanding_millions": parse_volume(shares_out_str),
            "institutional_ownership_percent": parse_percentage(inst_own_str),
            "total_value_millions": parse_price(total_value_str),
        }
    
    # Get total institutional shares from holdingsTransactions
    holdings_trans = inst_data.get("holdingsTransactions", {})
    if holdings_trans:
        institutional["summary"]["total_institutional_holders"] = parse_volume(holdings_trans.get("totalRecords"))
        institutional["summary"]["total_shares_held"] = parse_volume(holdings_trans.get("sharesHeld"))
    
    # Top holders
    holder_rows = inst_data.get("holdingsTransactions", {}).get("table", {}).get("rows", [])
    for row in holder_rows:
        institutional["top_holders"].append({
            "institution": row.get("ownerName"),
            "shares": parse_volume(row.get("sharesHeld")),
            "change": parse_volume(row.get("sharesChange")),
            "change_percent": parse_percentage(row.get("sharesChangePCT")),
            "value_thousands": parse_price(row.get("marketValue")),
            "date": row.get("date"),
        })
    
    # Insider trades
    insider_trades = []
    trade_rows = insider_data.get("transactionTable", {}).get("rows", [])
    for row in trade_rows:
        insider_trades.append({
            "date": row.get("lastDate"),
            "insider": row.get("insider"),
            "title": row.get("position"),
            "transaction": row.get("transactionType"),
            "shares": parse_volume(row.get("sharesTraded")),
            "price": parse_price(row.get("lastPrice")),
            "shares_held": parse_volume(row.get("sharesHeld")),
        })
    
    return {
        "institutional": institutional,
        "insider_trades": insider_trades
    }


def normalize_analyst_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and normalize analyst data."""
    peg_data = raw_data.get("peg_ratio", {})
    
    # Extract PEG ratio value
    peg_ratio = None
    if peg_data and "pegr" in peg_data:
        peg_ratio = peg_data["pegr"].get("pegValue")
    
    # Extract P/E ratio from chart data
    pe_ratio = None
    if peg_data and "per" in peg_data:
        pe_chart = peg_data["per"].get("peRatioChart", [])
        # Get the most recent actual P/E
        for entry in pe_chart:
            if "Actual" in entry.get("x", ""):
                pe_ratio = entry.get("y")
                break
    
    # Extract growth rate from chart data
    growth_rate = None
    if peg_data and "gr" in peg_data:
        gr_chart = peg_data["gr"].get("peGrowthChart", [])
        # Get latest year growth estimate
        if gr_chart:
            # Usually last entry has the forecast
            growth_rate = gr_chart[-1].get("y")
    
    return {
        "peg_ratio": peg_ratio,
        "pe_ratio": pe_ratio,
        "growth_rate": growth_rate,
    }


def normalize_short_interest(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and normalize short interest data."""
    short_data = raw_data.get("short_interest", {})
    table_rows = short_data.get("shortInterestTable", {}).get("rows", [])
    
    if table_rows:
        latest = table_rows[0]
        return {
            "settlement_date": latest.get("settlementDate"),
            "shares_short": parse_volume(latest.get("shortInterest")),
            "avg_daily_volume": parse_volume(latest.get("avgDailyShareVolume")),
            "days_to_cover": parse_price(latest.get("daysToCover")),
        }
    
    return {}


def normalize_sec_filings(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract and normalize SEC filings."""
    filings_data = raw_data.get("sec_filings", {})
    rows = filings_data.get("data", {}).get("rows", [])
    
    result = []
    for row in rows:
        result.append({
            "date_filed": row.get("filed"),
            "form_type": row.get("formType"),
            "description": row.get("description"),
            "url": row.get("url"),
        })
    
    return result


def normalize_news(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and normalize news data."""
    press_data = raw_data.get("press_releases", {})
    news_data = raw_data.get("news_articles", {})
    
    # Press releases
    press_releases = []
    for row in press_data.get("rows", []):
        press_releases.append({
            "date": row.get("created"),
            "title": row.get("title"),
            "url": row.get("url"),
            "publisher": row.get("publisher"),
        })
    
    # News articles
    articles = []
    for row in news_data.get("rows", []):
        articles.append({
            "date": row.get("created"),
            "title": row.get("title"),
            "url": row.get("url"),
            "publisher": row.get("publisher"),
            "related_symbols": [s.split("|")[0].upper() for s in row.get("related_symbols", [])],
        })
    
    return {
        "press_releases": press_releases,
        "articles": articles
    }


def normalize_nasdaq_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function to normalize all NASDAQ API data.
    
    Args:
        raw_data: Raw data from fetch_all_symbol_data()
    
    Returns:
        Normalized and reorganized data structure
    """
    symbol = raw_data.get("symbol", "UNKNOWN")
    result = {}
    
    try:
        result["metadata"] = normalize_metadata(raw_data)
    except Exception as e:
        logger.error(f"Error normalizing metadata for {symbol}: {e}")
        result["metadata"] = {}
    
    try:
        result["quote"] = normalize_quote(raw_data)
    except Exception as e:
        logger.error(f"Error normalizing quote for {symbol}: {e}")
        result["quote"] = {}
    
    try:
        result["key_metrics"] = normalize_key_metrics(raw_data)
    except Exception as e:
        logger.error(f"Error normalizing key_metrics for {symbol}: {e}")
        result["key_metrics"] = {}
    
    try:
        result["dividends"] = normalize_dividends(raw_data)
    except Exception as e:
        logger.error(f"Error normalizing dividends for {symbol}: {e}")
        result["dividends"] = {}
    
    try:
        result["historical_prices"] = normalize_historical_prices(raw_data)
    except Exception as e:
        logger.error(f"Error normalizing historical_prices for {symbol}: {e}")
        result["historical_prices"] = {}
    
    try:
        result["financials"] = normalize_financials(raw_data)
    except Exception as e:
        logger.error(f"Error normalizing financials for {symbol}: {e}")
        result["financials"] = {}
    
    try:
        result["ownership"] = normalize_ownership(raw_data)
    except Exception as e:
        logger.error(f"Error normalizing ownership for {symbol}: {e}")
        result["ownership"] = {}
    
    try:
        result["analyst_data"] = normalize_analyst_data(raw_data)
    except Exception as e:
        logger.error(f"Error normalizing analyst_data for {symbol}: {e}")
        result["analyst_data"] = {}
    
    try:
        result["short_interest"] = normalize_short_interest(raw_data)
    except Exception as e:
        logger.error(f"Error normalizing short_interest for {symbol}: {e}")
        result["short_interest"] = {}
    
    try:
        result["sec_filings"] = normalize_sec_filings(raw_data)
    except Exception as e:
        logger.error(f"Error normalizing sec_filings for {symbol}: {e}")
        result["sec_filings"] = []
    
    try:
        result["news"] = normalize_news(raw_data)
    except Exception as e:
        logger.error(f"Error normalizing news for {symbol}: {e}")
        result["news"] = {}
    
    return result
