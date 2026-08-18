#!/usr/bin/env python3
"""Lightweight Solana meme-coin scanner with strict risk messaging.

This tool intentionally does not provide "guaranteed", "no-risk", or
"sure 10x" recommendations.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass


@dataclass
class Coin:
    symbol: str
    liquidity_usd: float
    volume_24h_usd: float
    age_days: float
    top10_holder_pct: float
    buy_venue: str


def score_coin(coin: Coin) -> tuple[int, str, float]:
    score = 100

    if coin.liquidity_usd < 50_000:
        score -= 35
    elif coin.liquidity_usd < 150_000:
        score -= 15

    if coin.volume_24h_usd < 40_000:
        score -= 25
    elif coin.volume_24h_usd < 120_000:
        score -= 10

    if coin.age_days < 3:
        score -= 20
    elif coin.age_days < 14:
        score -= 8

    if coin.top10_holder_pct > 60:
        score -= 20
    elif coin.top10_holder_pct > 45:
        score -= 10

    score = max(0, min(100, score))

    if score >= 75:
        risk = "Lower (still speculative)"
        max_position_pct = 1.5
    elif score >= 55:
        risk = "Medium"
        max_position_pct = 1.0
    else:
        risk = "High"
        max_position_pct = 0.5

    return score, risk, max_position_pct


def read_coins(path: str) -> list[Coin]:
    with open(path, newline="", encoding="utf-8") as handle:
        rows = csv.DictReader(handle)
        required = {
            "symbol",
            "liquidity_usd",
            "volume_24h_usd",
            "age_days",
            "top10_holder_pct",
            "buy_venue",
        }
        if not rows.fieldnames or not required.issubset(set(rows.fieldnames)):
            missing = sorted(required - set(rows.fieldnames or []))
            raise ValueError(f"Missing required CSV columns: {', '.join(missing)}")

        coins: list[Coin] = []
        for row in rows:
            coins.append(
                Coin(
                    symbol=row["symbol"].strip(),
                    liquidity_usd=float(row["liquidity_usd"]),
                    volume_24h_usd=float(row["volume_24h_usd"]),
                    age_days=float(row["age_days"]),
                    top10_holder_pct=float(row["top10_holder_pct"]),
                    buy_venue=row["buy_venue"].strip(),
                )
            )
        return coins


def main() -> int:
    parser = argparse.ArgumentParser(description="Risk-aware Solana meme-coin scanner")
    parser.add_argument("--input", required=True, help="Path to CSV with candidate coins")
    args = parser.parse_args()

    print("DISCLAIMER: No strategy can guarantee profits or remove risk.")
    print("Use this output as a filtering aid only, then do your own research.\n")

    coins = read_coins(args.input)
    ranked = sorted(((score_coin(c), c) for c in coins), key=lambda item: item[0][0], reverse=True)

    print("symbol,score,risk,max_position_pct_of_portfolio,buy_venue")
    for (score, risk, max_position_pct), coin in ranked:
        print(f"{coin.symbol},{score},{risk},{max_position_pct:.1f},{coin.buy_venue}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
