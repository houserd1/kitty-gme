# GME Forensic Analysis — Final Steps 7 through 9

**Anchor for scoring:** What most parsimoniously explains both the May 2024 price action AND Keith Gill's specific timing on May 12, 2024.

---

## Updated data from second-pass research

Three meaningful additions to the Step 1-6 picture:

### 1. GME-specific Reg SHO threshold list status during the spike
GME (NYSE-listed) was not on the NYSE Reg SHO threshold list during the April-May 2024 spike window. This is verifiable from publicly tracked NYSE data and from contemporaneous community DD that explicitly noted GME's absence from the list as of mid-June 2024. **However**, XRT (SPDR S&P Retail ETF), which holds GME, has accumulated 1,691 total threshold days historically per a 2025 SEC rulemaking petition, with FTDs in XRT reaching as high as $418M. XRT was on the threshold list as recently as December 27, 2024. The squeeze fuel from settlement failures was channeled through the ETF wrapper, not the underlying stock. This is a documented and persistent feature of GME's market structure.

### 2. GME FTD data has acknowledged public-record gaps starting May 24, 2024
A FOIA request submitted to the SEC in October 2024 sought the missing GME FTD records for specific dates in 2024 (starting May 24, the day of GameStop's first ATM offering, and continuing through June 11-12, July 25, July 31-August 1, August 15, August 20-28, and September 4-13). The SEC denied the request citing FOIA Exemption 4 (confidential commercial or financial information). This is a primary-source data gap I cannot fill. The published SEC FTD record for GME in this window is incomplete by the SEC's own admission.

### 3. Q1 2024 institutional flows and market-maker accumulation
The 13F deltas for the relevant quarters tell a consistent story:
- **Q2 2024** (filed mid-August, covers the spike): Citadel Advisors +2,334% (1,830,940 shares added on a small base), Jane Street +1,519% (1,752,231 shares), Dimensional +439%. These are signature market-maker inventory builds during high-vol periods, not directional bets.
- **Q3 2024** (post-spike): BlackRock +42.7% (9.6M shares), Vanguard +24.9% (7.4M shares), Geode +41.8%. Passive index buying as GME's market cap re-inflated.
- **Q1 2024 specifically** (filed mid-May 2024, during the spike): I did not pin down a clean aggregate delta from public sources within this pass. The 13F filing window straddled the actual price spike, so the Q1 numbers themselves are only useful as a baseline, not a leading indicator.

### 4. Gill's documented technical-analysis toolkit
Gill maintained a public StockCharts.com chart list (still indexed under user 1778236). His pre-2021 YouTube content explicitly worked through chart structure, moving averages, support and resistance, and volume-confirmation patterns alongside fundamental DD. This is corroborated by Wikipedia's source-cited claim that his GME thesis used "both fundamental and technical analysis" and by independent Medium write-ups documenting his methodology.

---

## Step 7 — Reframed hypothesis set

The original prompt listed five hypotheses. After the data work, two refinements are warranted:

- The **"hidden institutional flow"** hypothesis is best split into two distinct sub-hypotheses: (c1) someone with material non-public information was trading ahead of Gill, and (c2) prime broker swap exposures were quietly being unwound into the spike.
- The **"clearing/regulatory catalyst"** hypothesis is best understood as a backdrop condition (T+1 calendar pressure), not a primary trigger.

### Refined hypothesis list
- **(a)** Retail-driven momentum and reflexive media coverage
- **(b)** Gamma squeeze from accumulated low-IV call positioning visible in public options flow
- **(c1)** Someone with material non-public information traded ahead of Gill
- **(c2)** Prime broker swap unwinds or hidden institutional risk transfer
- **(d)** T+1 calendar pressure as structural backdrop
- **(e)** Mechanical FTD cycle, ETF rebalancing, or tax-flow buying

---

## Step 8 — Hypothesis scoring

I'm scoring each on two dimensions: **explanatory weight** (does it fit the May 2024 price action?) and **timing fit** (does it explain Gill's specific May 12 entry?). Plausibility scores are 1-10 on each dimension. The final score is the parsimony weight, which rewards hypotheses that explain both with the fewest assumptions.

### Hypothesis (b) — Gamma squeeze from accumulated low-IV calls

**Confirming evidence:**
- Unusual Whales publicly flagged unusual GME call options flow starting April 24, 2024
- May 3 and May 10 ranked as the #1 and #2 highest call-volume days of 2024 — both before Gill's May 12 post
- The May 17 weekly $25 strikes saw documented sweeps (one trader turned $27K into peak ~$1.78M on those calls)
- Gill's own position (120K June 21 $20 calls) was purchased before May 12 per the Radev complaint and WSJ reporting, when the stock was $15-17
- IV on those strikes was suppressed because the stock was beaten-down; cheap premium meant high convexity
- The mechanical signature of the May 13 move (50%+ gap up at the open, multiple volatility halts, dealer buying behavior) matches the gamma-squeeze playbook documented by SpotGamma

**Disconfirming evidence:**
- Reported short interest in early 2024 was much lower than 2021 (mid-teens to low-20s percent of float, not 140%), which means short covering provided less mechanical fuel than in 2021
- A pure gamma squeeze typically dies once the front-month expiration prints; the June 7 second leg required a fresh catalyst (Gill's stream announcement plus surprise early earnings)

**Explanatory weight:** 9/10. The options tape is the cleanest single explanation for the build-up.
**Timing fit for Gill:** 9/10. The April 24 onward options accumulation is exactly the signal Gill's own toolkit (chart structure plus options flow) would catch. He likely participated in it directly.
**Parsimony score:** **High.**

### Hypothesis (a) — Retail-driven momentum

**Confirming evidence:**
- Massive retail engagement on May 13 onward, NYSE volatility halts five times that day
- WSB and Superstonk traffic spiked
- Other meme names (AMC, Virgin Galactic, BlackBerry) ran simultaneously, classic retail rotation behavior

**Disconfirming evidence:**
- Retail-only doesn't explain the late-April options flow that built before any retail buzz
- Retail alone does not produce the specific gamma mechanics of the May 13 gap
- The Bloomberg and Interactive Brokers reporting placed the unusual options activity in the institutional-and-sophisticated-trader bucket, not the retail bucket

**Explanatory weight:** 6/10. Retail amplified the move but did not initiate it.
**Timing fit for Gill:** 4/10. Gill returning IS the retail catalyst, so this hypothesis is partly circular when used to explain his timing.
**Parsimony score:** **Medium.** Best as a co-driver, not a primary explanation.

### Hypothesis (d) — T+1 calendar pressure as backdrop

**Confirming evidence:**
- T+1 compliance date was May 28, 2024, a real and proximate calendar event
- SEC Chair Gensler explicitly tied T+1 to the 2021 GameStop events
- Reg SHO Rule 204 closeout windows shrank under T+1
- DTCC/SIFMA preparation materials acknowledged operational stress in the transition window
- Some pre-transition closeout pressure on legacy fails is mechanically plausible

**Disconfirming evidence:**
- GME itself was not on the Reg SHO threshold list during the spike
- The spike was visible across multiple meme names simultaneously, not just GME, suggesting a broader retail trigger rather than a GME-specific clearing event
- T+1 is a structural change, not a directional one; it would not by itself cause buying

**Explanatory weight:** 4/10. Backdrop only.
**Timing fit for Gill:** 5/10. He could have observed the T+1 calendar and used it to time entry, but it would be a thin reed alone.
**Parsimony score:** **Medium-low.** Useful as supporting context.

### Hypothesis (c1) — Someone with material non-public information traded ahead of Gill

**Confirming evidence:**
- The April 24 onward options flow predates Gill's public re-engagement (May 10 like, May 12 post) by 2-3 weeks
- Whoever was buying knew or strongly suspected something
- The Radev complaint specifically alleged a coordinated pump-and-dump structure

**Disconfirming evidence:**
- "Material non-public information" implies an inside catalyst. The actual GME corporate news during the spike was the ATM offering and surprise early earnings — both reactive to the spike, not its cause
- The early call buyers may simply have been reading the same publicly observable setup (V-bottom plus depressed IV) that Gill read
- The Radev complaint was voluntarily dismissed within three days of filing, weakening it as an evidence base
- No SEC enforcement action has produced documented findings of insider activity in this window

**Explanatory weight:** 5/10. Possible but unproven.
**Timing fit for Gill:** 3/10. If anyone had MNPI, it was Gill himself (about his own intent to post). That is not the same as a hidden inside catalyst.
**Parsimony score:** **Low.** Requires assumptions that public data does not support.

### Hypothesis (c2) — Prime broker swap unwinds or hidden institutional risk transfer

**Confirming evidence:**
- Post-Archegos disclosure regime is partial; bank swap exposures to specific names are not fully visible
- The missing GME FTD data starting May 24, 2024 (per the FOIA denial) is consistent with operational stress in the clearing chain, though does not prove swap activity
- Q2 2024 market-maker positioning (Citadel, Jane Street large percentage adds) is consistent with hedging large derivative books

**Disconfirming evidence:**
- No documented swap-related news or earnings disclosure tied this to GME in the window
- Bank Q2 2024 trading revenue was not anomalous in a way that would suggest a major GME-related unwind
- The Q2 13F market-maker patterns are equally explained by routine high-vol inventory management

**Explanatory weight:** 4/10. Possible, unproven, and not necessary to explain the price action.
**Timing fit for Gill:** 2/10. Even if swaps were unwinding, Gill would have no clean public window into them.
**Parsimony score:** **Low.**

### Hypothesis (e) — Mechanical cycle (FTD T+35, ETF rebalance, tax flows)

**Confirming evidence:**
- XRT's persistent threshold-list status creates known FTD cycle pressure
- T+35 windows do produce observable buying patterns in some meme names
- Tax-loss harvesting season effects on beaten-down names are documented

**Disconfirming evidence:**
- FTD cycles produce smaller, more periodic moves; they do not produce 110% single-day gaps with five trading halts
- Multiple prior FTD cycle dates passed without similar spikes
- Cycle-driven buying alone has no mechanism for triggering retail engagement at scale

**Explanatory weight:** 3/10. Marginal contributor.
**Timing fit for Gill:** 3/10. Cycle dates are public; he could time them, but the chosen entry is more cleanly explained by the options tape.
**Parsimony score:** **Low.**

---

## Step 9 — Final ranked conclusion

### What most parsimoniously explains both the price action and Gill's timing

**Primary driver: gamma squeeze from accumulated low-IV call positioning, ignited by Gill's public re-engagement.**

The cleanest explanation that fits all the evidence and requires the fewest assumptions:

1. By April 16, 2024, GME hit a capitulation low at $10.02 with a deep cash floor (~$1.0B), DRS-locked supply (~25% of float), and a forgotten-stock IV profile that priced June OTM calls cheaply.
2. Starting April 24, sophisticated traders (likely including Gill) began accumulating upside calls. The flow was visible publicly through Unusual Whales, Bloomberg, and Interactive Brokers commentary.
3. Gill bought 120,000 of the June 21 $20 strike calls before May 12, then re-engaged publicly with the May 12 X post knowing his return would itself catalyze retail flow.
4. The May 13 gap-up triggered dealer hedging into a short-gamma posture. Retail piled in. Multiple volatility halts followed. The feedback loop ran from May 13 through May 14 ($48.75 close on May 14).
5. The June 6-7 second leg required a fresh catalyst: Gill's YouTube stream announcement plus GameStop's surprise early earnings release. Without that, the May spike would have decayed faster.
6. T+1 (effective May 28) operated as backdrop pressure but was not the primary mechanism.

This explanation:
- Uses only publicly observable data
- Does not require hidden institutional flows or non-public information
- Fits the mechanical signature of the price action (gap, halts, dealer hedging behavior)
- Fits Gill's documented toolkit (deep value floor + technical entry + cheap convex options)
- Fits his timing without circular reasoning

### What this means for your original hypothesis

You proposed: "this is not a normal stock and it can't just be retail fuel; something larger was happening behind the scenes and Keith knew it."

That framing is **half right**.

**Right:** Retail alone does not explain the move. The "something larger" was real — but it was the gamma-squeeze mechanics combined with the structural setup (DRS supply lock, depressed IV, fundamental floor, T+1 calendar). These mechanics are public and observable. They do not require a hidden conspiracy.

**Wrong:** "Behind the scenes" implies non-public information. The available evidence shows Gill was reading the same public options tape, the same chart, the same fundamentals that any careful analyst could read. He had no documented advantage in non-public data. His advantage was that he had built a deep-value thesis years earlier, had the conviction to size into June calls when premium was cheap, and knew his own public re-engagement would amplify the move he was already positioned for.

The parsimonious answer to "how did Keith know" is: he didn't have a secret. He had a reading of the options tape, a chart pattern, a balance-sheet thesis, and an asymmetric setup. The market gave him the trade; he recognized it and sized it.

### Confidence levels

- **High confidence** in the gamma-squeeze-as-primary-driver conclusion. Multiple independent public sources corroborate the options flow timeline.
- **Medium confidence** in the specific mechanism by which Gill's May 12 post propagated. Court filings narrow the timing window for his option purchases but do not produce exact trade timestamps.
- **Low confidence** on swap-related contributions. Public data simply does not let us rule this in or out cleanly. The missing FTD data starting May 24 is a flag, not proof.
- **Negligible confidence** in any non-public-information theory regarding Gill specifically. The Radev lawsuit was dropped within three days; no enforcement action has produced findings.

### Final ranked hypotheses (most to least parsimonious)

1. **Gamma squeeze from accumulated low-IV calls (b)** — primary driver
2. **Retail amplification (a)** — necessary co-driver from May 13 onward
3. **T+1 calendar backdrop (d)** — supporting structural condition
4. **Mechanical cycles (e)** — marginal contributor
5. **Hidden institutional flow / swap unwind (c2)** — possible but unsupported by public data
6. **MNPI ahead of Gill (c1)** — least supported; circular when applied to Gill's timing

---

## What we still cannot know (closing inventory)

Same gaps remain after the second pass:

1. **Specific E*Trade trade timestamps for Gill's call purchases.** Court filings narrow the window but do not produce exact dates.
2. **GME FTD data for May 24, 2024 onward.** SEC denied FOIA. This is a confirmed data gap, not a guess.
3. **Total return swap exposures** held by prime brokers against GME. Public disclosure regime is incomplete post-Archegos.
4. **Identity of the April 24 onward unusual call buyers.** Flow trackers see size and direction, not names.
5. **Whether GameStop management's pre-spike ATM authorization** had any communication path to early call buyers. No evidence either way; flagging because the timing is suggestive but proves nothing.

These gaps mean the **floor** of confidence is "gamma squeeze plus retail explains the public price action and Gill's timing without invoking anything else." The **ceiling** of confidence — whether something else was also happening behind the scenes — is bounded by what the SEC, prime brokers, and Gill himself have not made public. That ceiling is permanently uncertain.

---

## One closing observation worth flagging for your own thinking

The 2021 spike was a short squeeze on a stock with 140%-of-float short interest — an unprecedented setup that probably will not repeat in the same form because regulators and prime brokers have learned. The 2024 spike was a gamma squeeze on a stock with depressed IV, DRS-locked float, and a fundamental floor — a more replicable setup, but still rare because it requires both the technical compression and a credible catalyst. The two events share the meme-stock label but are mechanically different. Conflating them risks pattern-matching on the wrong variables for any future trade you might be evaluating.
