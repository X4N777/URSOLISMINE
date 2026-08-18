# URSOLISMINE

A minimal, risk-aware Solana meme-coin scanner helper.

This project **does not** promise guaranteed returns, "no-risk" trades, or "sure 10x" outcomes.

## Usage

Create a CSV file with these columns:

- `symbol`
- `liquidity_usd`
- `volume_24h_usd`
- `age_days`
- `top10_holder_pct`
- `buy_venue`

Then run:

```bash
python sol_scanner.py --input /absolute/path/to/candidates.csv
```

It prints ranked candidates with:

- a risk-adjusted score
- a risk band
- a conservative max position size suggestion (% of total portfolio)
- a buy venue hint from your data source
