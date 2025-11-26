#!/usr/bin/env python3
"""Fetch and normalize a single NASDAQ symbol."""
import sys
import json
import logging
import traceback

sys.path.insert(0, 'src')
from nasdaq import fetch_all_symbol_data, normalize_nasdaq_data

# Configure logging - INFO level to reduce verbosity
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)
# Suppress urllib3 debug logs
logging.getLogger('urllib3').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <symbol> <output_file>")
        sys.exit(1)
    
    symbol = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        print(f'  Fetching data for {symbol}...')
        raw_data = fetch_all_symbol_data(symbol)
        
        print(f'  Normalizing data for {symbol}...')
        normalized_data = normalize_nasdaq_data(raw_data)
        
        with open(output_file, 'w') as f:
            json.dump(normalized_data, f, indent=2, default=str)
        
        print(f'  ✓ Saved {symbol} data')
        sys.exit(0)
        
    except Exception as e:
        logger.error(f'Failed to process {symbol}: {e}')
        logger.error(f'Full traceback:\n{traceback.format_exc()}')
        print(f'  ✗ Failed {symbol}: {e}', file=sys.stderr)
        sys.exit(1)
