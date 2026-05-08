# Changelog

Versioned revisions to the Kitty framework. Dates use ISO `YYYY-MM-DD`.

## v1.1 — 2026-05-08

### Layer 2 (Technical Setup) expanded

Three new signals computed in a new `technicals.py` module from the same yfinance daily DataFrame the main script already pulls. No second network call.

- **OBV slope over 20 days** earns +5 when positive. Linear regression slope of On-Balance Volume across the trailing 20 trading days. The headline addition; Gill referenced OBV directly in his streams as the accumulation tell.
- **MACD bullish crossover** earns +2 when a crossover occurred in the last 10 trading days. Standard 12 / 26 / 9 parameters.
- **Weekly RSI(14)** earns +3 when the value sits in the 40-65 recovery zone. Daily closes resampled to Friday weekly bars.

Existing Layer 2 signals reweighted to make room: Price > 50DMA 5 → 3, Price > 200DMA 5 → 3, RSI(14) zone 5 → 3, Volume ratio 5 → 3. The −5 RSI overbought penalty is unchanged. Layer 2 maximum 20 → 22.

### Layer 5 (Catalyst Watch) adds Gill StockCharts signal

- **`gill_stockcharts_last_seen`** date in `manual_flags.json` drives a new +3 signal under the existing 7-day decay pattern. Source page: `stockcharts.com/public/1778236`. Edited chartlists historically preceded Gill's X return.
- Gill social media activity weight reduced 10 → 8 to make room. Still the highest single Layer 5 signal.
- Layer 5 maximum ~23 → 24.

Auto-scrape of the StockCharts chartlist for last-modified detection deferred. The page renders server-side but bot detection has been increasing; manual entry via the date field is more reliable for now.

### Regime caveat

- New `event_driven_volatility` boolean and `event_description` string in `manual_flags.json`.
- When set, the script prepends a `REGIME WARNING` block to the daily debrief, prefixes the ntfy title with `[EVENT-DRIVEN]`, and bumps push priority to high.
- The dashboard renders a bold red banner with an alert-triangle icon at the top of the page until the flag is reset.
- **The score itself is not adjusted.** The flag is informational. Captures the case where elevated readings come from news-driven chop rather than the quiet capitulation pattern that preceded May 2024.

### Schema and display changes

- `data.json` now carries `version`, `layer_max`, `total_max`, `event_driven_volatility`, and `event_description`. The dashboard reads these so future revisions can change layer maxes without a frontend redeploy.
- Total max 103 → 106. Score thresholds at 51 / 71 / 86 retained as absolute heuristics; the score is not normalized.
- Header version stamp reflects `data.version` automatically.
- Methodology section in the dashboard rewritten with per-signal weights.

## v1.0 — 2026-05-06

Initial Phase 2 build. Five-layer scoring (Floor 20, Technical 20, Options Tape 25, Structural 15, Catalyst 23). Daily GitHub Actions workflow with ntfy.sh push, GitHub Pages dashboard, options snapshot via yfinance, NYSE Reg SHO threshold check, SEC EDGAR Form 4 monitoring. Manual flags for Gill / Cohen activity and quarterly fundamentals. See the original handoff in `reference/kitty-framework-methodology.md`.
