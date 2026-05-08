# Kitty

**Version 1.1.** A scheduled monitoring framework that scores GameStop (GME) daily against historical pre-spike conditions and pushes a notification each weekday after market close. Personal analytical tool. Not financial advice.

The scoring framework is documented in [reference/kitty-framework-methodology.md](reference/kitty-framework-methodology.md) (the original v1.0 spec) and updated in [CHANGELOG.md](CHANGELOG.md) for subsequent revisions. Five layers, 106 points total in v1.1: Fundamental Floor (20), Technical Setup (22), Options Tape (25), Structural Backdrop (15), Catalyst Watch (24).

## How it runs

GitHub Actions runs `kitty.py` every weekday at 21:30 UTC (5:30 PM ET in EDT, 4:30 PM ET in EST). The script pulls free public data, reads `manual_flags.json` for the inputs that no public API exposes (Gill activity, Cohen X posts, fundamentals that change quarterly), computes the score, writes `data.json` and `history.json`, commits them back, and pushes a debrief via [ntfy.sh](https://ntfy.sh).

The dashboard at the GitHub Pages URL reads `data.json` and `history.json` from the same repo and renders the score, layer breakdown, today's read, and a 30-day trend.

## First-time setup

Steps in order. Each one is a single web action you can do on a phone.

**1. Pick an ntfy.sh topic.** Install the ntfy app on your phone (App Store / Play Store). Open it, tap **Subscribe to topic**, and enter a topic name. The topic is shared with anyone who subscribes to the same name, so a guessable one leaks your scores. The recommended format is `kitty-gme-` plus six random characters you pick.

**2. Add the topic as a GitHub secret.** In the repo, go to **Settings → Secrets and variables → Actions → New repository secret**. Name it `NTFY_TOPIC`. Value is the topic string from step 1 (no URL, just the topic name).

**3. Enable Actions write permissions.** **Settings → Actions → General → Workflow permissions → Read and write permissions**. Save. Without this, the workflow cannot commit `data.json` and `history.json` back.

**4. Enable GitHub Pages.** **Settings → Pages → Source: Deploy from a branch → Branch: main, folder: / (root)**. Save. Pages takes 2-3 minutes to publish on the first deploy.

**5. Run the workflow once manually.** **Actions → Kitty Daily Score → Run workflow → Run**. Watch it finish (about a minute). It writes `data.json` and `history.json` and pushes a notification.

**6. Bookmark the dashboard.** Once Pages has published, the URL appears in **Settings → Pages**. Open it, confirm the score is rendering, add it to your phone home screen.

## Daily use

Read the dashboard each morning. The score, layer bars, and "Today's Read" tell the story. The 30-day sparkline shows trend. Two horizontal lines mark the 51 (Elevated) and 71 (Heightened) thresholds.

When you see Gill or Cohen post something, edit `manual_flags.json` from GitHub's mobile web UI: navigate to the file in the repo, tap the pencil icon, change the relevant boolean, commit. The next scheduled run picks it up automatically. The dashboard's "Edit on GitHub" link opens the file directly.

After each GameStop earnings report, update the fundamental fields in `manual_flags.json` (`cash_tier`, `ocf_positive`, `no_dilution_risk`, `drs_locked`) and bump `fundamentals_last_updated` to the date you reviewed.

## Score interpretation

Thresholds are absolute heuristics, not percentile bands.

| Score | State | Meaning |
|---|---|---|
| 0-30 | Quiet | Conditions don't resemble historical pre-spike setups. |
| 31-50 | Watching | Some layers showing signal. Not actionable. |
| 51-70 | Elevated | Multiple layers aligning. Mid-stage pre-spike setup. Notification fires here by default. |
| 71-85 | Heightened | Most layers aligned. Late-stage pre-spike resemblance (April / early May 2024). |
| 86+ | Significant Convergence | Layer alignment matches or exceeds historical pre-spike maximums. Rare. |

The v1.1 max is 106 points (was 103 in v1.0). The thresholds above are unchanged because the score is a heuristic, not a normalized metric. A modest calibration drift comes with the framework expansion; that's accepted.

**Regime caveat.** The score reads conditions; it does not distinguish structural accumulation setups from event-driven volatility. The May 2024 spike was preceded by quiet capitulation, not by a major news catalyst. When a tariff announcement, geopolitical event, or regulator action is driving the tape, set `event_driven_volatility` in `manual_flags.json` along with `event_description`. The script will:

- Prepend a `REGIME WARNING` block to the daily debrief
- Prefix the ntfy push title with `[EVENT-DRIVEN]` and bump priority to high
- Render a red banner at the top of the dashboard with the event description

The score itself is not adjusted. The flag is informational and should be reset to false once the event resolves.

## Configuration

| Setting | Where | Default |
|---|---|---|
| ntfy topic | repo secret `NTFY_TOPIC` | required |
| Schedule | `.github/workflows/kitty.yml` cron | `30 21 * * 1-5` (UTC) |
| Alert threshold | `kitty.py --alert-threshold` | 51 |
| Always push | `kitty.py --always-push` | yes (set in workflow) |
| Manual flags | `manual_flags.json` | edit in repo |

To change the schedule, edit the `cron` line. To change the alert threshold for a single manual run, override it via the workflow_dispatch input. To change it permanently, edit the workflow.

## Manual flags reference

The Gill and Cohen activity signals decay automatically. Edit only the
`*_last_seen` date when you see a post. The script derives the 7-day
active flag from that date, so the catalyst layer drops the credit on
its own once the window expires. No manual reset.

| Field | Update when |
|---|---|
| `gill_last_seen` | Set to today's date (ISO `YYYY-MM-DD`) when Gill posts on X, Reddit, or YouTube. Catalyst layer scores +8 for 7 days, then decays. |
| `gill_stockcharts_last_seen` | Set to today's date when Gill edits his public chartlist at `stockcharts.com/public/1778236`. Catalyst layer scores +3 for 7 days, then decays. Historically a leading tell before his X return. |
| `cohen_last_seen` | Set to today's date when Cohen posts publicly on X. Catalyst layer scores +3 for 7 days, then decays. (Cohen Form 4 buys are auto-pulled from EDGAR; +5 for those is automatic.) |
| `event_driven_volatility` | Set true when an exogenous event (tariff announcement, war, regulator action) is driving GME's tape. Triggers REGIME WARNING in the debrief, `[EVENT-DRIVEN]` prefix on the push, and a red banner on the dashboard. Reset to false when the event resolves. Does not change the score. |
| `event_description` | Short free-text description of the event (e.g. `"April tariff retaliation"`). Surfaced in the warning banner. |
| `macro_event` | Material macro / regulatory event affecting market structure (Layer 5 +2). Different from `event_driven_volatility`; this one does score. Set true and remember to set false when it ages out. |
| `cash_tier` | After each earnings: `over50`, `over30`, or `under30` (cash + securities vs market cap). |
| `ocf_positive` | After each earnings: was operating cash flow positive last quarter. |
| `no_dilution_risk` | After each earnings: any new ATM filings or convertibles. |
| `drs_locked` | After each 10-Q: is DRS share count still ~25% of float. |
| `borrow_fee_rising` | When you check IBKR / Fintel and the trend is up week-over-week. |
| `short_vol_pct` | Most recent FINRA short volume % (from shortvolume.com or Fintel). |
| `fundamentals_last_updated` | Bump to today's date after refreshing the four `cash_tier` / `ocf_positive` / `no_dilution_risk` / `drs_locked` fields. The dashboard warns if this is more than 100 days old. |
| `notes` | Free text. |

## Troubleshooting

**The workflow ran but no notification arrived.** Confirm `NTFY_TOPIC` matches the topic string you subscribed to in the app, character-for-character. Confirm the ntfy app is allowed background notifications.

**The workflow ran but the dashboard still says "Awaiting first run".** GitHub Pages caches aggressively. Force-refresh the page (long-press reload on iOS Safari, or add `?nocache=1` to the URL).

**The workflow says "Permission denied" when committing.** Step 3 of first-time setup was skipped. Enable read/write workflow permissions and re-run.

**Layer 3 (Options Tape) is stuck at 0 for the first few weeks.** Expected. The 20-day call volume average and 252-day IV range have to be built up from prior runs of the script. Layer 3 starts contributing once 5+ days of options history accumulate, and stabilizes around day 20.

**A data source returns nothing.** The script logs the failure and continues. The affected signal scores zero, the debrief notes the gap, and the next run retries.

## What's in this repo

```
.github/workflows/kitty.yml                  GitHub Actions schedule
.github/workflows/kitty-failure-alert.yml    ntfy push when main workflow fails
kitty.py                                     Main script
technicals.py                                OBV, MACD, weekly RSI (v1.1)
options_scraper.py                           yfinance options snapshot + relative metrics
manual_flags.json                            Inputs that change less than daily
data.json                                    Latest run output (read by dashboard)
history.json                                 Rolling 365 entries
index.html                                   Static dashboard
requirements.txt                             Python deps
CHANGELOG.md                                 Versioned framework revisions
reference/                                   Background research and prototypes
```

## Disclaimer

This tool is for personal analytical use. The Kitty Score reports condition similarity to historical pre-spike setups, not predictions. The framework is calibrated against a small sample (n=2 major spikes). False positives are possible and have occurred. A high score does not mean the stock will run. A low score does not mean it will not. Nothing here is investment advice.
