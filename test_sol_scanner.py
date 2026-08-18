import tempfile
import unittest
from pathlib import Path

from sol_scanner import read_coins, score_coin


class SolScannerTests(unittest.TestCase):
    def test_score_coin_penalizes_risk(self):
        csv_content = (
            "symbol,liquidity_usd,volume_24h_usd,age_days,top10_holder_pct,buy_venue\n"
            "GOOD,200000,200000,30,30,Jupiter\n"
            "RISKY,10000,5000,1,85,Unknown\n"
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "candidates.csv"
            path.write_text(csv_content, encoding="utf-8")
            coins = read_coins(str(path))

        good_score, _, _ = score_coin(coins[0])
        risky_score, _, _ = score_coin(coins[1])

        self.assertGreater(good_score, risky_score)

    def test_read_coins_shows_row_on_invalid_numeric_value(self):
        csv_content = (
            "symbol,liquidity_usd,volume_24h_usd,age_days,top10_holder_pct,buy_venue\n"
            "BAD,abc,1000,1,70,Jupiter\n"
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "candidates.csv"
            path.write_text(csv_content, encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "row 2"):
                read_coins(str(path))


if __name__ == "__main__":
    unittest.main()
