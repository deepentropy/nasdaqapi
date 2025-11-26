#!/usr/bin/env python3
"""CLI tool to fetch symbol data - uses nasdaqapi client."""

import sys
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.WARNING,  # Only show warnings/errors
    format='%(levelname)s - %(message)s'
)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <symbol> <output_file>")
        sys.exit(1)
    
    symbol = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        # Import after args check for faster feedback
        from nasdaqapi import NasdaqClient
        
        print(f'  Fetching data for {symbol}...')
        client = NasdaqClient()
        data = client.get_symbol_data(symbol)
        
        print(f'  Writing to {output_file}...')
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f'  ✓ Saved {symbol} data')
        sys.exit(0)
        
    except Exception as e:
        print(f'  ✗ Failed {symbol}: {e}', file=sys.stderr)
        sys.exit(1)
