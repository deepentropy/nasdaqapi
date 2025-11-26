# NASDAQ API

A comprehensive Python library for fetching stock data from the NASDAQ API.

## Features

- 📈 **Complete Stock Data**: Fetch quotes, financials, dividends, historical prices, and more
- 🏢 **Ownership Information**: Institutional holdings and insider trades
- 📊 **Financial Statements**: Income statements, balance sheets, cash flow (annual & quarterly)
- 📰 **News & Filings**: SEC filings, press releases, and news articles
- 🔄 **Normalized Data**: Clean, structured data ready for analysis
- ⚡ **Easy to Use**: Simple, intuitive API

## Installation

```bash
pip install nasdaqapi
```

## Quick Start

```python
from nasdaqapi import fetch_all_symbol_data, normalize_nasdaq_data

# Fetch all data for a symbol
raw_data = fetch_all_symbol_data("AAPL")

# Normalize the data for easier access
data = normalize_nasdaq_data(raw_data)

# Access normalized data
print(f"Company: {data['metadata']['company_name']}")
print(f"Price: ${data['quote']['price']}")
print(f"Shares Outstanding: {data['key_metrics']['shares_outstanding']:,}")
print(f"Dividend Yield: {data['key_metrics']['dividend_yield']:.2%}")
```

## Available Data

### Metadata
- Company name, symbol, exchange
- Stock type and asset class
- Market status (pre-market, regular, after-hours)

### Quote Data
- Current price, change, volume
- Bid/ask prices and sizes
- Previous close, timestamp

### Key Metrics
- P/E ratio, dividend yield
- 52-week high/low
- Shares outstanding
- Market cap (when available)

### Financial Statements
- Income Statement (annual & quarterly)
- Balance Sheet (annual & quarterly)
- Cash Flow Statement (annual & quarterly)
- Financial Ratios

### Dividends
- Yield, annual amount, payout ratio
- Ex-dividend date, payment date
- Complete dividend history (80+ years for some stocks)

### Historical Prices
- Daily historical prices
- 5-day and 1-month periods
- Open, high, low, close, volume

### Ownership
- Institutional holdings and changes
- Top holders (Vanguard, BlackRock, etc.)
- Insider trades
- Ownership percentages

### Analyst Data
- PEG ratio
- P/E ratio trends
- Growth rate estimates

### Short Interest
- Shares short
- Average daily volume
- Days to cover

### News & Filings
- SEC filings (10-K, 10-Q, 8-K, etc.)
- Press releases
- News articles

## Advanced Usage

### Fetch Specific Data Categories

```python
from nasdaqapi import (
    fetch_symbol_info,
    fetch_symbol_dividends,
    fetch_company_financials,
    fetch_institutional_holdings
)

# Fetch only what you need
info = fetch_symbol_info("MSFT")
dividends = fetch_symbol_dividends("MSFT")
financials = fetch_company_financials("MSFT", frequency=1)  # 1=annual, 2=quarterly
holdings = fetch_institutional_holdings("MSFT", limit=50)
```

### Fetch Multiple Exchanges

```python
from nasdaqapi import fetch_all_exchanges, get_unique_symbols

# Get all tickers from NASDAQ, NYSE, and AMEX
tickers = fetch_all_exchanges()
symbols = get_unique_symbols(tickers)

print(f"Total symbols: {len(symbols)}")
```

## Data Structure

The normalized data follows this structure:

```python
{
    "metadata": {
        "symbol": "AAPL",
        "company_name": "Apple Inc. Common Stock",
        "exchange": "NASDAQ-GS",
        "stock_type": "Common Stock",
        ...
    },
    "quote": {
        "price": 277.90,
        "change": 0.93,
        "change_percent": 0.0034,
        "volume": 55881,
        ...
    },
    "key_metrics": {
        "pe_ratio": 45.26,
        "week_52_high": 280.38,
        "week_52_low": 169.21,
        "dividend_yield": 0.0038,
        "shares_outstanding": 14776000000,
        ...
    },
    "dividends": {
        "summary": {...},
        "history": [...]
    },
    "financials": {
        "annual": {
            "income_statement": [...],
            "balance_sheet": [...],
            "cash_flow": [...],
            "financial_ratios": [...]
        },
        "quarterly": {...}
    },
    "ownership": {
        "institutional": {
            "summary": {...},
            "top_holders": [...]
        },
        "insider_trades": [...]
    },
    "analyst_data": {...},
    "short_interest": {...},
    "sec_filings": [...],
    "news": {
        "press_releases": [...],
        "articles": [...]
    },
    "historical_prices": {
        "daily": [...],
        "period_5d": [...],
        "period_1m": [...]
    }
}
```

## Requirements

- Python 3.8+
- requests >= 2.31.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This library fetches data from NASDAQ's public API. Please review NASDAQ's terms of service and ensure your usage complies with their policies. This library is not affiliated with or endorsed by NASDAQ.

## Author

Created with ❤️ for the financial data community
