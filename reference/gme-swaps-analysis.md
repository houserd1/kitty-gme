# Swaps and GME — What the Theory Actually Says, What's Documented, What's Inferred

## The mechanism, briefly

A total return swap (TRS) is a contract where one party pays a financing fee to a counterparty (usually a bank prime broker) in exchange for the total economic return on a reference asset, including price moves and dividends. The bank holds the actual shares; the hedge fund has the synthetic exposure. Reverse the direction and you have a synthetic short.

This matters for GME because:

- **Swap positions are not in 13F filings.** Funds don't disclose them. The bank shows the share holding, but the bank is hedged.
- **Reg T margin rules don't apply directly.** A fund that needs 50% margin to short 100M shares the regular way can use a TRS with 5-10% margin. Massive synthetic leverage, massive concealed exposure.
- **Pre-2023, security-based swap position reporting was effectively absent.** SEC Rule 10B-1 was adopted in June 2023 with phased compliance dates extending through 2024 and beyond. During the May 2024 GME spike, the position-disclosure regime for swaps was still largely opaque.
- **Swaps can be booked offshore.** US banks have moved swap activity to London, Tokyo, and other jurisdictions where Dodd-Frank reporting is weaker. This is documented in academic work and in the Greenberger SEC public comment record.

The community's structural claim is that some unknown amount of short GME exposure that existed in early 2021 was never actually covered — it was rolled into TRS contracts and is still sitting on bank balance sheets in synthetic form. That claim has elements that are documented and elements that are inferred.

## Documented foundation

**Archegos.** Bill Hwang used TRS to build $50B+ of leveraged exposure with $20B of equity, hidden across multiple banks. When margin calls hit in March 2021, Credit Suisse lost $5.5B, Nomura lost $2.85B, UBS $861M, Morgan Stanley $911M, Mitsubishi UFJ $300M. Hwang was convicted of fraud in 2024. This proves the TRS-as-hiding-mechanism concept is real and can produce nine-figure losses when it goes wrong.

**Archegos timing relative to GME.** Archegos collapsed in late March 2021, weeks after the January GME squeeze. SEC public-comment filings (notably one cited in S7-32-10) included community DD arguing that Archegos's exposure included GME and other meme names. The official Credit Suisse special committee report on Archegos, however, names ViacomCBS, Discovery, and other media stocks as the primary positions. Whether GME was specifically inside Archegos's swap book in size is **not officially documented** in the public Archegos post-mortems I've seen. The community has overstated this connection.

**SEC swap rulemaking.** Post-Archegos, the SEC adopted Rule 10B-1 (June 2023) requiring position reporting for large security-based swap positions, plus Rule 9j-1 prohibiting fraud in security-based swaps. Compliance phase-in extended into 2024 and 2025. This is direct regulatory acknowledgment that swap markets had a transparency hole big enough to drive a freight train through.

**Bank disclosures.** Annual reports and 10-K filings from major prime brokers (UBS, Goldman, Morgan Stanley, JPMorgan) discuss aggregate counterparty exposures and ISDA-collateralized swap books. They do not name individual reference assets. The information needed to verify or falsify a "GME swap book at Bank X" claim is not public.

## What Ryan Cohen has actually said

This is the part where I have to be careful with what's recorded versus what's inferred.

**What's documented:** Cohen has used X (formerly Twitter) cryptically for years. He has tweeted about executive accountability, the decay of corporate America, "Owner's Mentality" governance, and the importance of CEOs putting personal capital at risk. He has criticized hedge funds and short-sellers in general terms.

**What's not documented:** I could not find a single public statement, letter, interview, SEC filing, or earnings-call comment in which Ryan Cohen explicitly endorses the total return swap theory or names specific banks as carrying hidden GME short exposure. If such a statement exists, it's not in the indexed public record I searched.

**What the community infers:** The Superstonk/r/GME communities read Cohen's emoji posts, his timing of ATM offerings, his repeated dilution into strength, and his refusal to engage with media as evidence that he understands the swap dynamic and is acting on it. The clearest example: GameStop's June 2024 ATM raised $2.14B by selling 75M shares directly into the squeeze. Community interpretation: he was forcing covers and feeding shares to the synthetic short side. Alternative interpretation: he saw an open window to fund a holding-company strategy and took it. Both interpretations fit the same facts.

**Honest read:** Cohen's behavior is consistent with someone who *understands* how the market structure can be exploited by short interests and who is willing to act ruthlessly to extract value from volatility. That's different from him publicly *endorsing* the swap theory. The community has bridged that gap with interpretation, not evidence.

## Patterns and trends that are applicable

These are observable in the data, even if the mechanism behind them is partially uncertain.

### 1. Quarterly boundary effects

TRS contracts typically have quarterly reset dates. If a swap is causing buying pressure when its counterparty needs to roll or rebalance, you'd expect concentration of activity near quarter-ends.

GME has shown elevated activity around several quarter boundaries:
- **March 2021** (Q1 close, Archegos margin calls): a ~50% rally and pullback
- **June 2021** (Q2 close): a sharp spike to ~$300 in early June
- **March 2022** (Q1 close): rally to mid-$50s
- **March 2024** (Q1 close): the Q4 2023 earnings selloff, but a base forming
- **June 2024** (Q2 close): the second leg of the 2024 squeeze
- **September 2024**: Cohen 13D amendment activity

**Caveat:** Quarter-ends also see ETF rebalancing, options expiration, and tax-related flows. Disentangling swap-driven activity from these other flows requires data we don't have. Pattern is real; sole cause is unconfirmed.

### 2. ETF wrapper FTDs as a leakage mechanism

XRT (SPDR S&P Retail ETF) holds GME. XRT has been on the Reg SHO threshold list for **1,691 cumulative days** per a 2025 SEC rulemaking petition. FTDs in XRT have run as high as $418M.

The mechanism: a short seller can short XRT to gain economic exposure to a basket including GME without directly shorting GME. The ETF's authorized participants can create or redeem shares using the basket constituents, but if the AP is short on delivery, the short exposure persists. This is sometimes called "ETF arbitrage failure" or "creation-redemption stress."

**Why this matters for the swap theory:** Even if direct GME shorts have been "covered" on the tape, equivalent exposure may persist via XRT short positions, which themselves are sometimes inside swap books. The reported GME short interest at low levels (mid-teens %) does not tell the full story of total economic short exposure.

**Caveat:** XRT-as-GME-short-proxy is real but not unique to GME. Many ETFs have persistent FTDs. The size of GME-specific exposure inside XRT FTDs is not directly observable.

### 3. T+35 close-out cycles

Reg SHO Rule 204 requires broker-dealers to close out FTD positions within specific windows. Combined with options market-maker exemptions and certain extension rules, some FTDs can persist for ~35 calendar days before mandatory close-out. The community has argued that recurring T+35 cycles produce predictable buying pressure on specific dates.

**Documented:** The T+35 framework exists and has been studied academically.
**Not documented:** That GME's specific spikes systematically map to T+35 windows in a way that distinguishes them from coincidence. Backtests run by Superstonk DD authors have produced both convincing-looking matches and obvious misses.

### 4. Convertible bond hedging circularity

GameStop issued $1.3B of 0% convertible notes due 2030 in March 2025, then another $1.75B of 0% notes due 2032 in June 2025. Convertible bond buyers typically short the underlying stock as a hedge to isolate the convertible's optionality. This means **every dollar of convertible issuance creates new short interest** that is structurally not bearish.

Short interest data does not distinguish between directional shorts and convertible-arbitrage hedging shorts. The 15-20% of float currently shown as short likely includes a meaningful portion of convert-arb shorts. This is a real structural feature post-March 2025; it was less of a factor in May 2024 when no converts were outstanding.

### 5. Persistent low borrow rates despite high reported short volume share

GME's borrow fee has often been below 1% even when short volume share runs 50-60% of daily volume. This has been a long-standing puzzle for the retail DD community. One explanation: prime brokers running internal book matches against their own swap inventory don't need to source external borrows, which keeps fees down even when demand for synthetic exposure is high.

This is a real, observable inconsistency. The TRS explanation fits but isn't the only possible explanation; ETF-create-redeem dynamics and intra-broker netting also depress borrow demand.

## What this means for May 2024 specifically

If you ask "did swaps cause the May 2024 spike?" the honest answer is: probably no, not as the trigger. The trigger was the gamma squeeze. But the *backdrop* against which the gamma squeeze ran was almost certainly shaped by pre-existing swap exposures somewhere in the system, because the broader regulatory record makes clear those exposures exist.

In other words: swaps did not light the fuse on May 13. The lit fuse ran into a structurally compressed environment partly created by years of accumulated swap activity, ETF FTDs, and post-Archegos opacity. That's why the move was as violent as it was.

## What this means for whether Cohen "knew"

Cohen probably understands the structural dynamics — he has a finance background, he runs an unusual capital allocation strategy, and his behavior (DRS encouragement, dilution into strength, refusal to communicate on Wall Street's terms) suggests someone who reads the market structure cynically and acts on it. Whether he subscribes to the specific community version of the swap theory is unknown and unrecorded. He has commercial reasons not to comment publicly on it either way: endorsing it would draw regulatory attention; denying it would alienate the retail base.

The most defensible reading: Cohen acts as if he believes some version of the swap-and-structural-opacity story, but has never said so publicly, and his actions are also fully consistent with someone simply running a contrarian dilution-into-strength playbook. Both readings fit. The community has chosen the more romantic one.

## Where this leaves the original analysis

In my Step 9 conclusion I ranked "hidden institutional flow / swap unwind" as low parsimony for explaining the May 2024 spike specifically, and I stand by that. But I want to refine the language: swaps are not best understood as a *trigger* hypothesis competing with the gamma squeeze. They're best understood as a *structural condition* of GME's market — a permanent feature, not an event — that makes any catalyst (gamma squeeze, Cohen action, Gill return, regulatory shift) produce sharper moves than would otherwise occur.

If you want a single sentence: **the gamma squeeze lit the fuse; the swap-and-structural-opacity environment is why the powder keg was the size it was.**

The patterns and trends most worth watching:
- Quarter-end activity, especially March, June, September boundaries
- XRT threshold-list status as a leading indicator for GME
- Convertible bond issuance and its effect on reported short interest
- Cohen's capital allocation moves, treated as one signal among many
- Bank trading-revenue anomalies in quarters where GME makes large moves

What we still cannot know:
- Specific swap exposures by counterparty and reference asset
- Whether the unhedged tail of these positions is large enough to matter for any specific future move
- What Cohen actually believes versus what his actions imply

The honest framing for your forensic work: treat the swap structural environment as a real and persistent feature of GME's market, treat specific swap-driven event claims as testable but unproven, and treat Cohen's belief as inferred not stated.
