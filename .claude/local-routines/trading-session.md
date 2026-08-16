You are the autonomous trading agent described in this repo's CLAUDE.md. Run today's 10:00 ET trading session.

This runs locally — dependencies are already installed and credentials are already in the local `.env` (loaded automatically by `scripts/research.py` / `scripts/trade.py` via python-dotenv). Do not attempt to install packages or export credentials.

Routine:
1. Run `python scripts/trade.py status`. If the market is closed, append a note to today's journal/YYYY-MM-DD.md under a '## Trades (10:00 routine)' heading stating no trades were placed because the market was closed, commit, push, and stop. Never place trades when market status is closed — this rule is absolute.
2. If open, read today's journal/YYYY-MM-DD.md Research section for context (it should already exist from the morning routine; if it's missing, run the relevant `scripts/research.py` commands yourself first to reconstruct the needed context).
3. Run `python scripts/research.py account` and `python scripts/research.py positions` to get current cash balance and open positions.
4. For each symbol in the root-level watchlist.json, decide buy / sell / hold using the research signals (20d vs 50d moving average, news, current positions) and these hard rules from CLAUDE.md:
   - Never invest more than 5% of total portfolio value in a single position (portfolio value comes from the account endpoint).
   - Never place a market order — always a limit order within 0.2% of the current ask. Fetch a fresh quote before sizing any order (the Alpaca quotes endpoint: GET https://data.alpaca.markets/v2/stocks/{symbol}/quotes/latest using the same auth headers as the other scripts) rather than relying on the prior day's close.
   - If any existing position has dropped 8% or more from its entry price, close it immediately regardless of other signals.
5. Place any resulting orders with `python scripts/trade.py order SYMBOL QTY SIDE LIMIT_PRICE`.
6. Append a '## Trades (10:00 routine)' section to today's journal documenting every decision made (including holds, with the reasoning) and every order actually placed, then commit and push to main.

Be conservative: if a signal is ambiguous or conflicting, prefer holding over forcing a trade. Follow every other rule in CLAUDE.md exactly.
