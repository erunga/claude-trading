You are the autonomous trading agent described in this repo's CLAUDE.md. Run today's 16:15 ET end-of-day journal routine. This runs every trading day regardless of whether any trades were placed.

This runs locally — dependencies are already installed and credentials are already in the local `.env` (loaded automatically by the scripts via python-dotenv). Do not attempt to install packages or export credentials.

Routine:
1. Run `python scripts/research.py account` and `python scripts/research.py positions` to get final cash/portfolio value and open positions.
2. Fetch today's orders: GET {APCA_BASE_URL}/v2/orders with params status=all, after=<today 00:00:00Z>, until=<tomorrow 00:00:00Z>, limit=100, using the same auth headers as scripts/trade.py.
3. Open today's journal/YYYY-MM-DD.md (it should already exist from the morning/trading routines; create it if genuinely missing) and append a '## End-of-Day Reflection (16:15 routine)' section covering: final account state (cash, portfolio value, equity, positions), a list of orders placed today (or 'none'), a 'What worked' note, a 'What didn't' note, and a 'Watch tomorrow' list of specific things to check at the next research pass (e.g. names near their moving averages, open legal/news catalysts, any position approaching the 8% stop-loss).
4. Commit and push the completed journal file to main with a descriptive commit message.
5. Email the day's digest: run `python scripts/notify.py journal/YYYY-MM-DD.md` (with today's actual date). This is best-effort — if it fails (e.g. missing/broken `brevo` package, bad credentials), log the error clearly in your output but do not treat it as fatal to the overall run, and do not stop or skip the journal commit because of it.

Always write this journal entry, even on days with zero trades — that is a hard rule in CLAUDE.md. Keep the reflection honest and specific, not generic.
