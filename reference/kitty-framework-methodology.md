# Kitty — A Daily Monitoring Framework for GME

A structured way to read GME market conditions through the same lens Keith Gill plausibly uses: deep value floor first, technical setup second, options tape third, structural backdrop fourth, catalyst watch fifth. Synthesize, don't predict.

## What this is and isn't

**This is** a disciplined daily checklist that scores GME against the historical pre-spike conditions documented in the May 2024 forensic work. It produces a composite score (0-100) and a structured debrief.

**This is not** a trading signal, a buy/sell recommendation, or a prediction. A high Kitty Score does not mean the stock will run. It means today's conditions resemble the conditions that preceded historical runs. That's a categorical difference. Markets do not have to repeat.

**This is also not** automated. I cannot send push notifications from a chat interface. The dashboard requires you to enter today's data and run it manually each day. If you want true automation, the Python data-collection script in section 7 can be cron-scheduled on your own machine.

## Philosophy: thinking like Gill

From the forensic work, Gill's actual decision pattern looks like:

1. **Establish a fundamental floor years before any catalyst.** He bought GME in 2019 at ~$5 because the cash on the balance sheet, the brand asset, and Cohen's involvement priced in zero turnaround optionality. The floor lets him sit through years of nothing.
2. **Use technicals to time entry, not to predict direction.** V-bottoms, MA reclaims, OBV divergence — these are entry triggers, not crystal balls.
3. **Read the options tape for accumulation by sophisticated capital.** Unusual call activity is the cleanest "someone who knows is buying" signal he had access to in late April 2024.
4. **Express conviction through cheap convex calls when IV is suppressed.** Low IV at a depressed price means the market gives you optionality for free. He bought $20 strikes when the stock was $17.
5. **Be aware of structural backdrop, but don't trade on it.** XRT FTDs, quarter-end pressure, T+1 effects, swap opacity — these size the powder keg, but they don't light fuses.
6. **Recognize that you yourself can be the catalyst.** Gill posting is a market-moving event. Most people don't have that lever, but the principle generalizes: the right setup plus a small catalyst is more dangerous than the wrong setup plus a big one.

The framework codifies these as five layers, each with explicit metrics and thresholds.

## The five layers

### Layer 1 — Fundamental Floor (0-20 points)

**Question this layer answers:** Is there a cash-and-balance-sheet floor that protects you from being wrong on timing?

| Signal | Threshold | Points |
|---|---|---|
| Cash + marketable securities > 50% of market cap | yes | 10 |
| Cash + marketable securities > 30% of market cap | yes (instead of above) | 5 |
| Operating cash flow positive in most recent quarter | yes | 5 |
| No imminent dilution announced | yes | 5 |

**Data sources:** GameStop 10-K and 10-Q filings, latest earnings press release, recent 8-K filings.

**Update cadence:** Quarterly, with potential mid-quarter updates if material 8-K events.

**Note:** GME's fundamental floor was the entire reason Gill could hold from 2019 through 2024 without panic. As of mid-2025, the company had ~$8.7B in cash. That's an unusually thick floor for a sub-$15B market cap. Layer 1 has rarely been weak in GME's modern era.

### Layer 2 — Technical Setup (0-20 points)

**Question this layer answers:** Does the chart show a setup consistent with pre-spike accumulation?

| Signal | Threshold | Points |
|---|---|---|
| Price > 50-day moving average | yes | 5 |
| Price > 200-day moving average | yes | 5 |
| RSI(14) in 40-65 range | yes | 5 |
| RSI(14) > 75 (overbought, deduct) | yes | -5 |
| Volume ratio (today / 20-day avg) > 1.5x | yes | 5 |

**Data sources:** Any charting platform (TradingView, StockCharts, Yahoo Finance, Barchart). Gill's documented preferred tool was StockCharts.com.

**Update cadence:** Daily.

**Note:** The April 16, 2024 capitulation low at $10.02 followed by recovery through the 50 DMA on rising volume was the textbook pre-spike technical pattern. Layer 2 is the entry-trigger layer.

### Layer 3 — Options Tape (0-25 points, the most weighted layer)

**Question this layer answers:** Is sophisticated capital quietly positioning for an upside move?

| Signal | Threshold | Points |
|---|---|---|
| Call volume ratio (today / 20-day avg) > 2x | yes | 10 |
| Call volume ratio > 3x (exceptional) | yes (instead of above) | 15 |
| IV rank < 30 (cheap premium) | yes | 5 |
| IV rank < 15 (very cheap) | yes (instead of above) | 10 |
| Put/call volume ratio < 0.5 | yes | 5 |
| Multi-day persistence (3+ consecutive days of unusual activity) | yes | 5 |

**Data sources:** Unusual Whales (paid), Barchart options unusual activity, OptionCharts, Market Chameleon. Free sources are limited; many options-tape signals require a paid feed.

**Update cadence:** Daily, intraday if possible.

**Note:** This is the layer that gave Gill his timing edge in May 2024. Unusual Whales flagged GME starting April 24, 2024. May 3 and May 10 were the highest call-volume days of 2024. Layer 3 is the smoking gun.

### Layer 4 — Structural Backdrop (0-15 points)

**Question this layer answers:** How big is the powder keg?

| Signal | Threshold | Points |
|---|---|---|
| XRT (S&P Retail ETF) on Reg SHO threshold list | yes | 5 |
| Days to next quarter-end < 15 | yes | 3 |
| Short volume share (FINRA daily) > 50% | yes | 3 |
| Borrow fee trending up week-over-week | yes | 2 |
| DRS share count maintained ~25% of float | yes | 2 |

**Data sources:**
- XRT threshold status: NYSE Reg SHO Threshold list (free, daily)
- Quarter-end calendar: trivial
- Short volume: FINRA daily files via Fintel, ChartExchange, or shortvolume.com (free)
- Borrow fee: IBKR, Fintel, Stocknear (free/freemium)
- DRS: GameStop 10-Q filings (quarterly)

**Update cadence:** Daily for most signals; quarterly for DRS.

**Note:** The structural backdrop doesn't trigger moves, it amplifies them. A high Layer 4 score means any catalyst hitting will produce a sharper reaction than baseline.

### Layer 5 — Catalyst Watch (0-20 points)

**Question this layer answers:** Is there an active or imminent catalyst that could ignite the setup?

| Signal | Threshold | Points |
|---|---|---|
| Cohen Form 4 open-market buy in last 7 days | yes | 5 |
| Cohen public statement / X post in last 7 days | yes | 3 |
| Gill social media activity in last 7 days | yes | 10 |
| GameStop earnings within 30 days | yes | 3 |
| Material macro/regulatory event affecting market structure | yes | 2 |

**Data sources:**
- Form 4 filings: SEC EDGAR (free), OpenInsider
- Cohen X posts: directly on X
- Gill posts: directly on X (@TheRoaringKitty), Reddit (u/DeepFuckingValue), YouTube
- Earnings calendar: any market data source
- Macro/regulatory: news monitoring

**Update cadence:** Daily, with active monitoring of Gill's accounts.

**Note:** Gill activity gets the highest single weight in Layer 5 because his return is the most reliable single-day catalyst documented. A Form 4 buy from Cohen is the second strongest. The combination is rare and historically powerful.

## Composite Kitty Score interpretation

| Score | State | What it means |
|---|---|---|
| 0-30 | **Quiet** | Nothing notable. Current conditions don't resemble historical pre-spike setups. |
| 31-50 | **Watching** | Some layers showing signal. Worth checking daily. Not actionable. |
| 51-70 | **Elevated** | Multiple layers aligning. Conditions are similar to mid-stage pre-spike setups. Increase monitoring frequency. |
| 71-85 | **Heightened** | Most layers aligned. Setup resembles late-stage pre-spike conditions like late April / early May 2024. This is where serious attention is warranted. |
| 86-100 | **Significant convergence** | Rare condition. Layer alignment matches or exceeds historical pre-spike maximums. Treat with caution: signals this strong have historically preceded large moves but can also produce disappointing fizzles. |

**Critical caveat:** The score is calibrated against two known pre-spike events (Jan 2021, May 2024). Two data points is not a robust statistical base. False positives are possible and have happened. The score is a structured frame, not a verdict.

## Daily workflow

The intended use is a 10-minute daily ritual:

1. **Open the Kitty dashboard** (the React artifact).
2. **Update the seven core inputs** (price, volume ratio, call ratio, IV rank, RSI, days to quarter-end, XRT threshold status). The other inputs change less frequently.
3. **Read the scored output**. Pay attention to which layers are driving the score.
4. **Save today's entry**. The dashboard logs to local storage so you can see trend.
5. **Compare today to yesterday and to the 7-day moving average.** The trend matters more than the absolute number.
6. **If score crosses into Heightened or above**, increase frequency. Check the options tape intraday. Watch Gill and Cohen accounts.

## Section 7 — Toward automation

True notifications require a Python script you run on your own infrastructure (a personal server, a cloud function, a Raspberry Pi). The script would:

1. Pull GME daily price/volume from a free source (yfinance, Alpha Vantage, Polygon free tier)
2. Pull options activity from a paid source (Unusual Whales API, Tradier, Polygon options) — paid feeds are the bottleneck
3. Scrape XRT Reg SHO status from `nyse.com/regulation/threshold-securities` daily
4. Check SEC EDGAR for new GME Form 4 filings via the EDGAR REST API
5. Check Gill's X account for new posts (X API or scraping; X has restricted scraping)
6. Compute the Kitty Score
7. Push results via Pushover, Telegram bot, ntfy.sh, email, or SMS via Twilio

I can write this script as a separate deliverable if you want it. The free-tier paths are fragile but workable. The paid-tier paths cost roughly $30-100/month for adequate options data.

## Limitations and disclosures

- The framework is calibrated on a small historical sample (n=2 major spikes). Statistical robustness is low.
- Several inputs (options tape persistence, Gill activity intent) require subjective interpretation.
- The score does not account for macro market regime. A high Kitty Score in a bear market is materially different from one in a bull market. Use judgment.
- Past pre-spike conditions do not have to recur. Market structure changes (T+1, post-Archegos rules, evolving options market). Patterns degrade.
- This framework is for personal analytical use. It is not investment advice and Claude is not a financial advisor.

## How to use the dashboard

The React artifact accompanying this spec implements all of the above. Inputs are organized by layer. Output is a composite score, layer breakdowns, today's read, what would change the picture, and a saved history of prior runs. Open it daily, spend 10 minutes, save the entry. Review the trend weekly.
