You are the autonomous trading agent described in this repo's CLAUDE.md. Run today's morning research routine (09:45 ET).

This runs locally — dependencies are already installed and credentials are already in the local `.env` (loaded automatically by `scripts/research.py` / `scripts/trade.py` via python-dotenv). Do not attempt to install packages or export credentials.

Routine:
1. Run `python scripts/trade.py status` to check market status. If the market is closed, still create/append today's journal/YYYY-MM-DD.md noting the market was closed, commit, push, and stop — do not fetch research.
2. If open, read the symbol list from the root-level watchlist.json. For each symbol run `python scripts/research.py bars SYMBOL` and `python scripts/research.py news SYMBOL`. Also run `python scripts/research.py account` and `python scripts/research.py positions`.
3. From each symbol's returned daily closes, compute the 20-day and 50-day moving averages (average of the last 20 / last 50 closes) and note whether the trend is bullish (20d MA > 50d MA) or bearish.
4. Write today's journal/YYYY-MM-DD.md (create it if it doesn't exist). Under a '## Research (09:45 routine)' heading, include: market status, account cash/portfolio value, open positions, and a per-symbol table of last close / 20d MA / 50d MA / signal / brief risk notes, plus a short news-highlights section. Use journal/2026-08-04.md in this repo as a formatting reference.
5. Commit the journal file and push to the main branch with a descriptive commit message.

Follow every rule in CLAUDE.md. Do not place any trades during this routine — it is research only.
