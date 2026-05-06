# GME Forensic Analysis — Steps 1 through 6

**Status:** Paused at Step 6 checkpoint per prompt design. No hypothesis scoring yet.
**Scope:** Mechanics behind Jan 2021 and May/June 2024 spikes, plus reconstruction of Keith Gill's observable information set on May 12, 2024.

---

## Step 1 — Technical setup ahead of each rally

### January 2021
GME entered 2021 in a clear uptrend off the August 2020 base. The stock had moved from roughly $4 in summer 2020 (split-adjusted) to about $17 by year-end on rising volume after Ryan Cohen's RC Ventures stake disclosure (August 2020) and his board appointment announcement (January 11, 2021). The structure leading into mid-January was a multi-month accumulation pattern with each pullback bought, OBV climbing faster than price, and rising 50-day MA crossing above the 200-day. By January 13 to 20 the stock had broken through its previous swing highs around $20 on roughly 10x normal volume. This is a textbook breakout-with-volume-expansion setup.

### April / May 2024
GME printed a 52-week low at **$10.02 on April 16, 2024** following a soft Q4 2023 earnings release (March 26, 2024) that missed revenue. From April 16 the chart inflected. Volume picked up notably starting April 23 to 24. By Friday May 10, the stock closed at $17.49, up roughly 68% in three weeks. The pattern is best described as a deep V-bottom with a rapid recovery through the 50-day MA and approaching the 200-day. RSI moved from oversold (sub-30) at the April low to the 60s by May 10. Weekly OBV diverged from price during late April, which is a classic accumulation tell.

A specific structural feature worth noting: by May 10, with the stock at $17.49, **the entire options chain through the next several weekly expirations was clustered around strikes that would all become ITM if the stock simply touched $25**. This compression of strikes near spot is unusual and creates outsized gamma sensitivity on any move.

---

## Step 2 — Options market state in the 30 days pre-spike

### January 2021
Call open interest concentration at $30, $35, $40, $45, $50 strikes for late-January and February expirations. ATM IV moved from ~5% of stock price in early January to multiples of that by late January. SpotGamma documented that retail traders were specifically targeting near-term OTM strikes, which forces dealers into the highest-gamma part of the surface. Once GME crossed $30 to $40, dealers went into severe short-gamma positioning and had to buy progressively more stock to hedge.

### April / May 2024
This is the most important piece for the Gill timing question.

- **April 24, 2024:** Unusual Whales publicly flagged unusual options flow in GME — roughly 2.5 weeks **before** Gill's May 12 X post.
- **May 3, 2024:** Highest single-day call option volume in GME for the entire year up to that point.
- **May 10, 2024:** Call option volume around 300,000 contracts — second-highest day of 2024. Bloomberg and Interactive Brokers' Steve Sosnick both flagged this publicly the same week.
- **May 10, 2024:** Gill's @TheRoaringKitty X account "liked" a post on the platform — the first interaction in nearly three years. This is publicly observable from X timestamps.
- A documented trade: a single trader bought May 17, 2024 $25 strike calls for about $0.21 average premium ($27,000 total), which peaked at $13.63 — a clean ~65x return.

The setup mirrored 2021's mechanics structurally, but smaller in scale and with the gamma loaded into the May 17 weekly first, then the June 21 monthly. Gill's own position (revealed June 2) was 120,000 contracts of the **June 21, 2024 $20 strike calls**, purchased before May 12 when the stock was around $17. Implied volatility on these calls was relatively suppressed during late April given the stock's beaten-down status — a known feature of forgotten meme names.

---

## Step 3 — Short interest, borrow, FTDs going into each spike

### January 2021
- Reported short interest peaked at roughly **140% of float** on January 22, 2021, per FINRA data and contemporaneous Goldman Sachs research.
- Shorted shares were re-lent and re-shorted, mechanically possible because beneficial ownership and lending pools allow restacking.
- More than 1 million GME shares were officially failed-to-deliver on January 28, 2021.
- Short interest exceeding 100% of float occurred only ~15 times in the prior decade, per Goldman.

### April / May 2024
Reported short interest in late April 2024 was meaningfully lower than 2021 in percentage terms (the available figures for that period suggest mid-to-high teens to low-20s percent of float, well below 2021's extreme), but borrow rates and short volume share remained elevated. Note: in the broader market in April-May 2024, FTD activity was unusually high in some adjacent names (DJT/TMTG hit the Nasdaq Reg SHO threshold list continuously from April 2, 2024 — a documented systemic stress signal in that window).

GME's specific Reg SHO threshold list status during April-May 2024 is not cleanly retrievable from public summaries I found in this pass. Flagging this as a data gap to fill before final scoring.

---

## Step 4 — Clearing/regulatory catalysts in the 90 days prior

### 2021
NSCC's mid-squeeze collateral demands (the now-famous $3B request to Robinhood early on Jan 28, reduced to $700M by 5:30am) were a consequence, not a setup catalyst. The relevant pre-event rule context was Reg SHO and the existing T+2 cycle, both of which permitted the kind of FTD accumulation that fueled the squeeze.

### 2024
The decisive regulatory catalyst on the calendar was the **T+1 settlement compliance date of May 28, 2024**, mandated by SEC Rule 15c6-1 amendments adopted February 15, 2023. SEC Chair Gensler explicitly framed T+1 as a direct response to "the GameStop stock events of 2021." T+1 reduces the closeout window for FTDs under Reg SHO Rule 204 and shrinks broker collateral exposure, which structurally makes a future Robinhood-style buy-button shutoff less likely.

The proximity of the May 12 spike to the May 28 T+1 effective date is a real timing fact. Whether that proximity is causal or coincidental is the open question. Two specific mechanical points:
1. Any FTDs accumulated under T+2 before May 28 had to be closed out under the existing rules; the rule change does not retroactively force closeouts.
2. Several days of overlap between the old and new regimes around May 28-29 created operational stress for prime brokers, which is documented in industry preparation materials from SIFMA and DTCC.

I found no evidence of any specific NSCC, OCC, or DTC special rule filing in the 90 days before May 12 that mechanically forced position changes in GME. The T+1 calendar pressure is the real story here.

---

## Step 5 — Institutional and DRS positioning

### Insider and ownership shifts pre-2024 spike
- **DRS as of November 30, 2023:** ~75.4M shares (approximately 25% of outstanding)
- **DRS as of March 20, 2024 (10-K filing):** ~75.3M shares (still ~25% of 305.87M outstanding)
- **DRS as of June 5, 2024 (10-Q filing):** ~74.6M shares (down ~700K from March; outstanding had ballooned to 351.2M due to the ATM offering)

The DRS pool was effectively flat at ~75M for most of the relevant period. With ~75% of outstanding held at DTCC via Cede & Co., the broker-accessible pool stayed near 230M in March 2024. Float-locked shares are not a 2024-specific catalyst — this condition had persisted for years.

### Insider activity
Ryan Cohen had not yet executed his 2025-era personal open-market buys at the time of the May 2024 spike. His major personal purchase activity I found in records is from April 2025 onward (e.g., 500,000 shares at $21.55 on April 3, 2025). For the May 2024 window, no significant Form 4 insider buying catalyst is documented.

### Capital structure event after the spike
GameStop completed a 75M share **at-the-market equity offering on June 11, 2024**, raising about $2.14B in cash. This was a direct monetization of the volatility — the company sold into the rally. Outstanding share count rose from 305.87M (March 20) to 351.22M (June 5). A second ATM later that summer raised additional capital. This matters because it documents that GameStop management was prepared and approved for an ATM ahead of the spike, which is itself a signal that someone saw setup conditions.

---

## Step 6 — Reconstruction of Gill's observable information set on May 12, 2024

This is the core question. I'll separate it into what was publicly available and what Gill's known toolkit could read from it.

### Gill's known analytical toolkit (from his pre-2021 content)
- Self-described deep value investor in the Graham tradition
- Combined fundamental analysis (balance sheet, cash position, turnaround thesis) with technical analysis (price structure, volume confirmation, short interest as a reflexive variable)
- Spreadsheet-driven, transparent in showing his work
- Comfortable with options as a leveraged expression of conviction (his 2019 starting position included 500 calls)

### What was publicly observable to him by May 10-12, 2024

**Fundamental (already established for years):**
- ~$1.0B cash and ~$83M marketable securities as of May 4, 2024 (the Q1 FY2024 balance sheet)
- Roughly $1B+ enterprise value at $17 with massive cash cushion relative to a sub-$5B market cap. The classic "the market is pricing this below cash plus going-concern" deep value setup he favors.
- ~25% of float DRS-locked, structurally tightening tradeable supply
- Cohen as CEO actively cutting costs and store count

**Technical (new in April-May 2024):**
- $10.02 intraday low on April 16, 2024 — classic capitulation print on heavy volume
- Sharp recovery off that low with volume confirmation
- 50-day MA crossover by early May
- The 68% three-week run into May 10 with each pullback bought

**Options-market read (the most actionable signal):**
- Unusual options flow flagged publicly by Unusual Whales starting April 24
- May 3 and May 10 ranking #1 and #2 call volume days of 2024
- Concentrated open interest building at strikes that would compress the entire chain ITM on a $5-7 move
- Suppressed IV at the strikes he targeted ($20 strike, June 21 expiry) given the stock's beaten-down state

**The specific timing logic:**
A $20 strike June 21 call bought when the stock was ~$15-17 would have been priced at very low premium given low realized vol and depressed IV. If Gill was reading the same options tape as Unusual Whales and Bloomberg's data feed (which any retail Bloomberg or Barchart user could see), he had ~2 weeks of evidence that someone large was accumulating upside calls before he posted. His own purchase predates his post — confirmed by court filings from the Radev complaint and by WSJ reporting. The "liking" of a post on May 10 — when call volume hit its second-highest day of the year — is the thinnest publicly observable footprint of his attention re-engaging.

### What Gill plausibly synthesized
1. **Fundamental floor intact:** balance sheet improving, cash hoard deep, no existential risk in the next 12 months
2. **Technical capitulation completed:** April 16 low looked like the bottom
3. **Options tape signaling accumulation:** someone (or many someones) was loading near-term and June OTM calls at very low premium
4. **Asymmetric setup:** a $20 strike June expiry with the stock at $17 was cheap because the market priced no catalyst, and yet the gamma profile meant a ~$3-5 move would produce extreme convexity
5. **Optionality on his own influence:** he knew his return to posting would itself be a catalyst, so the asymmetry of his trade was even higher than the raw chart and tape suggested

This is a deep value setup with a technical entry trigger, expressed through cheap convex calls — the same template he used in 2019. The novelty in 2024 is that he was both the catalyst and the trader, which the Massachusetts Secretary of State and the Radev plaintiff seized on.

### Was there a "secret" non-public catalyst he could only see?
On the publicly available evidence I have gathered in Steps 1 through 5, **no public-data signal requires a non-public source to explain Gill's timing**. The unusual options flow was already flagged by free public trackers two weeks before he posted. The technical bottom was visible on any chart. The fundamental picture had been stable. The T+1 calendar was scheduled. He had built an actionable thesis from public data alone.

The remaining unknowns concern data Gill may or may not have had access to, not data that is fundamentally hidden. See "What we cannot know" below.

---

## What we cannot know (so far)

These are signals that, if Gill saw them, would have strengthened his timing — but which are not fully retrievable from public sources:

1. **Total return swap exposures.** Post-Archegos disclosures are partial. Whether prime brokers carrying short GME exposure via swaps were quietly unwinding ahead of T+1 is not in the public record. We can guess from CFTC swap data lags and bank disclosures, but cannot confirm.
2. **Dark pool and off-exchange short volume detail.** CBOE stopped reporting short volume from some venues in July 2023, creating a permanent visibility gap.
3. **Exact identity of the April 24 onward call accumulators.** Unusual options flow trackers see size and direction, not identity. Was it Gill? Ryan Cohen? A hedge fund? Multiple parties? Public data does not resolve this.
4. **Private fund positioning.** 13F filings lag 45 days post-quarter and exclude shorts and swaps. Q1 2024 13Fs filed by mid-May would have shown some positioning, but they were filed during the spike.
5. **Whether Gill had any private-network signal** (former MassMutual contacts, broker chatter, Reddit DMs from informed parties). There is no evidence of this and no obligation to assume it.
6. **GME-specific Reg SHO threshold list status during April-May 2024.** I did not get a clean primary-source read on this within Step 6.

---

## Side-by-side comparison

| Factor | Jan 2021 | May 2024 |
|---|---|---|
| Pre-spike low | ~$17 (Jan 4) | $10.02 (Apr 16) |
| Pre-spike vol pattern | Multi-month accumulation | V-bottom recovery |
| Reported short interest | ~140% of float | mid-teens to low-20s % (data gap to refine) |
| Options OI concentration | Heavy near-term OTM calls | Heavy near-term OTM calls |
| Call volume signal pre-spike | Massive Jan 22 peak | Apr 24 onward, May 3 and May 10 peaks |
| Insider/owner catalyst | Cohen joins board Jan 11 | Cohen as CEO + ATM authorized |
| Float-locked supply | Pre-DRS movement | ~25% DRS-locked |
| Regulatory backdrop | T+2, pre-Reg SHO closeout reform | T+1 effective May 28, 2024 |
| Gill's own position | 50K shares + 500 calls (built since 2019) | 5M shares + 120K $20 calls |
| Gill's role | Public DD author | Public DD author + market participant simultaneously |
| Peak | $483 / $120.75 split-adj. (Jan 28) | $64.83 (intraday Jun 7) |

---

## Pause for human review

This is the Step 6 checkpoint. The next step in the original prompt is to formally score the five competing hypotheses (retail momentum, gamma squeeze, hidden institutional flow, regulatory catalyst, mechanical cycle) against the evidence above, with weights and confidence levels.

Before scoring, I'd like your input on:

1. **Data gaps to close first.** GME-specific Reg SHO threshold list status April-May 2024, specific institutional 13F deltas (Q1 2024 and Q4 2023), and GME-specific FTD aggregates would meaningfully sharpen the scoring. Do you want me to dig deeper before scoring, or score on what I have and flag the uncertainty?

2. **Hypothesis framing.** Your original prompt assumed "something larger behind the scenes" beyond retail. The Step 6 reconstruction so far suggests Gill could have built the trade from public data alone, with the options tape (Apr 24 onward) as the cleanest tell. That doesn't rule out hidden institutional flow — it just means his timing didn't require it. Do you want me to weight the hidden-flow hypothesis on its own merits regardless of whether Gill needed it, or to anchor scoring to "what most parsimoniously explains both the price action AND Gill's specific timing"?

3. **One clean tension worth flagging now.** The Apr 24 unusual options flow precedes Gill's public re-engagement (May 10 like, May 12 post) by 2-3 weeks. This is consistent with either: (a) Gill seeing the same tape everyone else saw and acting on it, or (b) someone larger positioning before he did, with Gill following. The Radev lawsuit and WSJ reporting place his option purchases before May 12 but don't pin the exact dates. Resolving this would tighten the analysis. The records that would do it (E*Trade trade timestamps) are not public.
