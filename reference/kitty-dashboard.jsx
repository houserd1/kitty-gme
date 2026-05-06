import React, { useState, useEffect, useMemo } from 'react';
import { ChevronDown, ChevronRight, Save, Trash2, Eye, AlertCircle, TrendingUp } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, ResponsiveContainer, Tooltip, ReferenceLine } from 'recharts';

const FONTS = `
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,800;1,9..144,400;1,9..144,600&family=JetBrains+Mono:wght@400;500;700&display=swap');
.font-display { font-family: 'Fraunces', serif; font-variation-settings: 'opsz' 144; }
.font-mono { font-family: 'JetBrains Mono', monospace; }
.tabular { font-variant-numeric: tabular-nums; }
`;

const initialInputs = {
  // Layer 1 - Fundamental Floor
  cashOverMcap: 'over50',  // 'over50' | 'over30' | 'under30'
  ocfPositive: true,
  noDilutionRisk: true,
  // Layer 2 - Technical
  priceOver50dma: true,
  priceOver200dma: true,
  rsi: 55,
  volRatio: 1.0,
  // Layer 3 - Options Tape
  callRatio: 1.0,
  ivRank: 50,
  putCallRatio: 1.0,
  optionsPersistence: false,
  // Layer 4 - Structural
  xrtThreshold: false,
  daysToQuarterEnd: 60,
  shortVolPct: 45,
  borrowFeeRising: false,
  drsLocked: true,
  // Layer 5 - Catalyst
  cohenBuy7d: false,
  cohenPost7d: false,
  gillActive7d: false,
  earningsWithin30d: false,
  macroEvent: false,
  // Meta
  price: 0,
  notes: '',
};

function scoreInputs(i) {
  // Layer 1 - Fundamental Floor (0-20)
  let l1 = 0;
  if (i.cashOverMcap === 'over50') l1 += 10;
  else if (i.cashOverMcap === 'over30') l1 += 5;
  if (i.ocfPositive) l1 += 5;
  if (i.noDilutionRisk) l1 += 5;

  // Layer 2 - Technical (0-20)
  let l2 = 0;
  if (i.priceOver50dma) l2 += 5;
  if (i.priceOver200dma) l2 += 5;
  const rsi = Number(i.rsi);
  if (rsi >= 40 && rsi <= 65) l2 += 5;
  if (rsi > 75) l2 -= 5;
  if (Number(i.volRatio) > 1.5) l2 += 5;

  // Layer 3 - Options Tape (0-25)
  let l3 = 0;
  const cr = Number(i.callRatio);
  if (cr > 3) l3 += 15;
  else if (cr > 2) l3 += 10;
  const iv = Number(i.ivRank);
  if (iv < 15) l3 += 10;
  else if (iv < 30) l3 += 5;
  if (Number(i.putCallRatio) < 0.5) l3 += 5;
  if (i.optionsPersistence) l3 += 5;

  // Layer 4 - Structural (0-15)
  let l4 = 0;
  if (i.xrtThreshold) l4 += 5;
  if (Number(i.daysToQuarterEnd) < 15) l4 += 3;
  if (Number(i.shortVolPct) > 50) l4 += 3;
  if (i.borrowFeeRising) l4 += 2;
  if (i.drsLocked) l4 += 2;

  // Layer 5 - Catalyst (0-20)
  let l5 = 0;
  if (i.cohenBuy7d) l5 += 5;
  if (i.cohenPost7d) l5 += 3;
  if (i.gillActive7d) l5 += 10;
  if (i.earningsWithin30d) l5 += 3;
  if (i.macroEvent) l5 += 2;

  const total = l1 + l2 + l3 + l4 + l5;
  return { l1, l2, l3, l4, l5, total };
}

function getState(score) {
  if (score >= 86) return { label: 'Significant Convergence', tone: 'text-amber-400', bar: 'bg-amber-400' };
  if (score >= 71) return { label: 'Heightened', tone: 'text-amber-300', bar: 'bg-amber-300' };
  if (score >= 51) return { label: 'Elevated', tone: 'text-amber-200', bar: 'bg-amber-200' };
  if (score >= 31) return { label: 'Watching', tone: 'text-stone-300', bar: 'bg-stone-400' };
  return { label: 'Quiet', tone: 'text-stone-500', bar: 'bg-stone-600' };
}

function generateRead(scores, inputs) {
  const points = [];
  
  // Drivers
  if (scores.l3 >= 20) points.push("The options tape is loud. Call activity, low IV, and tape persistence are the strongest signals here.");
  else if (scores.l3 >= 15) points.push("Options activity is meaningful but not extreme. Watch for multi-day persistence to confirm.");
  else if (scores.l3 < 5 && Number(inputs.callRatio) < 1.2) points.push("Options tape is quiet. The May 2024 setup required clear unusual activity that built for weeks.");

  if (scores.l2 >= 15) points.push("Technical structure supports an entry: price above key MAs, RSI in the recovery zone, volume confirming.");
  else if (Number(inputs.rsi) > 75) points.push("RSI is overbought. Historically this is late-cycle, not pre-spike.");
  else if (!inputs.priceOver50dma) points.push("Price is below the 50-day MA. The technical setup is incomplete.");

  if (inputs.gillActive7d) points.push("Gill is publicly active. This has historically been the single most reliable catalyst for short-term moves.");
  if (inputs.cohenBuy7d) points.push("Cohen has bought in the open market within the last week. This is a high-conviction insider signal.");

  if (scores.l4 >= 10) points.push("Structural backdrop is loaded: XRT threshold, short volume share, or quarter-end pressure are amplifying any catalyst.");
  if (inputs.xrtThreshold && Number(inputs.daysToQuarterEnd) < 20) points.push("XRT is on the threshold list and quarter-end is close. This is the historically reactive combination.");

  if (scores.l1 < 10) points.push("Fundamental floor has weakened. The thesis that protects you from being wrong on timing depends on Layer 1.");

  if (Number(inputs.callRatio) > 2 && Number(inputs.ivRank) < 30) {
    points.push("Cheap convex calls are available right now. This is the asymmetric setup Gill targets.");
  }

  if (scores.total >= 71) {
    points.push("Composite score matches the late-stage pre-spike conditions documented in late April 2024. Increase monitoring frequency.");
  } else if (scores.total >= 51) {
    points.push("Composite score is in the elevated range. Multiple layers are aligning but the setup is not yet at May 2024 levels.");
  } else if (scores.total < 31) {
    points.push("Composite score is quiet. No layer convergence today.");
  }

  return points.length ? points : ["No notable signal in any layer today."];
}

function whatChangesIt(scores, inputs) {
  const items = [];
  if (scores.l3 < 15) items.push(`Call volume ratio rising above 2x with IV rank under 30 (currently ${inputs.callRatio}x, IV rank ${inputs.ivRank})`);
  if (!inputs.gillActive7d) items.push("Gill posting on X, Reddit, or YouTube");
  if (!inputs.cohenBuy7d) items.push("A new Form 4 disclosing Cohen open-market buying");
  if (!inputs.xrtThreshold) items.push("XRT appearing on the Reg SHO threshold list");
  if (Number(inputs.daysToQuarterEnd) > 20) items.push(`Approach of quarter-end (currently ${inputs.daysToQuarterEnd} days out)`);
  if (!inputs.optionsPersistence) items.push("3+ consecutive days of unusual options activity");
  return items.slice(0, 5);
}

function Section({ title, children, defaultOpen = false, accent = false }) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className={`border-t ${accent ? 'border-amber-400/30' : 'border-stone-800'}`}>
      <button onClick={() => setOpen(!open)} className="w-full flex items-center justify-between py-3 px-1 text-left hover:bg-stone-900/50 transition-colors">
        <span className={`font-mono text-xs uppercase tracking-widest ${accent ? 'text-amber-300' : 'text-stone-400'}`}>{title}</span>
        {open ? <ChevronDown className="w-4 h-4 text-stone-500" /> : <ChevronRight className="w-4 h-4 text-stone-500" />}
      </button>
      {open && <div className="pb-4 px-1">{children}</div>}
    </div>
  );
}

function NumInput({ label, value, onChange, hint, min, max, step = 0.1 }) {
  return (
    <div className="mb-3">
      <label className="block text-stone-400 font-mono text-xs mb-1">{label}</label>
      <input
        type="number"
        value={value}
        min={min}
        max={max}
        step={step}
        onChange={(e) => onChange(e.target.value)}
        className="w-full bg-stone-950 border border-stone-700 text-stone-100 font-mono text-sm px-3 py-2 focus:border-amber-400 focus:outline-none tabular"
      />
      {hint && <div className="text-stone-600 font-mono text-[10px] mt-1">{hint}</div>}
    </div>
  );
}

function Toggle({ label, value, onChange, hint }) {
  return (
    <div className="mb-3 flex items-start gap-3">
      <button
        onClick={() => onChange(!value)}
        className={`mt-0.5 w-10 h-5 flex-shrink-0 border transition-colors ${value ? 'bg-amber-400 border-amber-400' : 'bg-stone-950 border-stone-700'}`}
        aria-pressed={value}
      >
        <div className={`w-4 h-4 bg-stone-100 transition-transform ${value ? 'translate-x-5' : 'translate-x-0.5'}`}></div>
      </button>
      <div className="flex-1">
        <label className="block text-stone-300 font-mono text-xs">{label}</label>
        {hint && <div className="text-stone-600 font-mono text-[10px]">{hint}</div>}
      </div>
    </div>
  );
}

function LayerBar({ label, score, max, weight }) {
  const pct = (score / max) * 100;
  return (
    <div className="mb-2">
      <div className="flex justify-between font-mono text-[10px] uppercase tracking-wider mb-1">
        <span className="text-stone-400">{label}</span>
        <span className="text-stone-300 tabular">{score}<span className="text-stone-600">/{max}</span></span>
      </div>
      <div className="h-1 bg-stone-900 relative overflow-hidden">
        <div className="h-full bg-amber-400 transition-all" style={{ width: `${pct}%` }}></div>
      </div>
    </div>
  );
}

export default function KittyDashboard() {
  const [inputs, setInputs] = useState(initialInputs);
  const [history, setHistory] = useState([]);
  const [activeTab, setActiveTab] = useState('today');
  const [saveStatus, setSaveStatus] = useState('');

  const update = (key, value) => setInputs(prev => ({ ...prev, [key]: value }));

  const scores = useMemo(() => scoreInputs(inputs), [inputs]);
  const state = useMemo(() => getState(scores.total), [scores.total]);
  const read = useMemo(() => generateRead(scores, inputs), [scores, inputs]);
  const changes = useMemo(() => whatChangesIt(scores, inputs), [scores, inputs]);

  // Load history from storage
  useEffect(() => {
    (async () => {
      try {
        const r = await window.storage.list('kitty:');
        if (r && r.keys) {
          const entries = [];
          for (const k of r.keys) {
            try {
              const e = await window.storage.get(k);
              if (e && e.value) {
                entries.push(JSON.parse(e.value));
              }
            } catch (err) { /* skip */ }
          }
          entries.sort((a, b) => new Date(a.date) - new Date(b.date));
          setHistory(entries);
        }
      } catch (err) {
        console.log('No history yet');
      }
    })();
  }, []);

  const saveToday = async () => {
    const today = new Date().toISOString().slice(0, 10);
    const entry = {
      date: today,
      total: scores.total,
      l1: scores.l1, l2: scores.l2, l3: scores.l3, l4: scores.l4, l5: scores.l5,
      price: Number(inputs.price) || null,
      notes: inputs.notes || '',
    };
    try {
      await window.storage.set(`kitty:${today}`, JSON.stringify(entry));
      const newHistory = history.filter(e => e.date !== today);
      newHistory.push(entry);
      newHistory.sort((a, b) => new Date(a.date) - new Date(b.date));
      setHistory(newHistory);
      setSaveStatus('Saved');
      setTimeout(() => setSaveStatus(''), 2000);
    } catch (err) {
      setSaveStatus('Error');
      setTimeout(() => setSaveStatus(''), 2000);
    }
  };

  const clearHistory = async () => {
    if (!confirm('Delete all saved Kitty entries?')) return;
    try {
      const r = await window.storage.list('kitty:');
      if (r && r.keys) {
        for (const k of r.keys) await window.storage.delete(k);
      }
      setHistory([]);
    } catch (err) { /* */ }
  };

  const recentHistory = history.slice(-30);
  const today = new Date().toISOString().slice(0, 10);

  return (
    <div className="min-h-screen bg-stone-950 text-stone-100">
      <style>{FONTS}</style>

      {/* Header */}
      <header className="border-b border-stone-800 px-4 py-5">
        <div className="flex items-baseline justify-between">
          <div className="flex items-baseline gap-2">
            <span className="font-display text-3xl text-amber-400 italic">Kitty</span>
            <span className="font-mono text-[10px] uppercase tracking-widest text-stone-500">v1.0</span>
          </div>
          <div className="font-mono text-[10px] text-stone-500 tabular">{today}</div>
        </div>
        <div className="font-mono text-[10px] text-stone-500 mt-1 uppercase tracking-wider">GME Daily Conditions Monitor</div>
      </header>

      {/* Tabs */}
      <div className="flex border-b border-stone-800 px-4">
        {[['today','Today'],['history','History'],['method','Method']].map(([k,l]) => (
          <button key={k}
            onClick={() => setActiveTab(k)}
            className={`px-4 py-3 font-mono text-[11px] uppercase tracking-widest transition-colors ${activeTab === k ? 'text-amber-400 border-b-2 border-amber-400' : 'text-stone-500 hover:text-stone-300'}`}
          >{l}</button>
        ))}
      </div>

      {activeTab === 'today' && (
        <div className="p-4 space-y-4">
          {/* Score Display */}
          <div className="border border-stone-800 p-5 bg-stone-900/30">
            <div className="flex items-baseline justify-between mb-1">
              <span className="font-mono text-[10px] uppercase tracking-widest text-stone-500">Composite Score</span>
              <span className={`font-mono text-[10px] uppercase tracking-widest ${state.tone}`}>{state.label}</span>
            </div>
            <div className="flex items-baseline gap-3">
              <span className="font-display text-7xl text-stone-100 tabular leading-none">{scores.total}</span>
              <span className="font-mono text-stone-600 text-sm">/100</span>
            </div>
            <div className="mt-4 h-1.5 bg-stone-900 relative overflow-hidden">
              <div className={`h-full ${state.bar} transition-all`} style={{ width: `${scores.total}%` }}></div>
            </div>

            <div className="mt-5 space-y-2">
              <LayerBar label="Floor" score={scores.l1} max={20} />
              <LayerBar label="Technical" score={scores.l2} max={20} />
              <LayerBar label="Options Tape" score={scores.l3} max={25} />
              <LayerBar label="Structural" score={scores.l4} max={15} />
              <LayerBar label="Catalyst" score={scores.l5} max={20} />
            </div>
          </div>

          {/* Today's Read */}
          <div className="border border-amber-400/30 bg-amber-400/[0.02] p-4">
            <div className="flex items-center gap-2 mb-3">
              <Eye className="w-3 h-3 text-amber-400" />
              <span className="font-mono text-[10px] uppercase tracking-widest text-amber-300">Today's Read</span>
            </div>
            <ul className="space-y-2">
              {read.map((p, i) => (
                <li key={i} className="font-mono text-xs text-stone-300 leading-relaxed">
                  <span className="text-amber-400 mr-2">·</span>{p}
                </li>
              ))}
            </ul>
          </div>

          {/* What Changes the Picture */}
          {changes.length > 0 && (
            <div className="border border-stone-800 p-4">
              <div className="flex items-center gap-2 mb-3">
                <TrendingUp className="w-3 h-3 text-stone-400" />
                <span className="font-mono text-[10px] uppercase tracking-widest text-stone-400">What Would Move The Score Up</span>
              </div>
              <ul className="space-y-1.5">
                {changes.map((c, i) => (
                  <li key={i} className="font-mono text-xs text-stone-400">
                    <span className="text-stone-600 mr-2">→</span>{c}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Save */}
          <div className="flex gap-2 items-center">
            <button onClick={saveToday}
              className="flex-1 bg-amber-400 hover:bg-amber-300 text-stone-950 font-mono text-xs uppercase tracking-widest py-3 transition-colors flex items-center justify-center gap-2"
            >
              <Save className="w-3 h-3" /> Save Today's Entry
            </button>
            {saveStatus && <span className="font-mono text-[10px] text-amber-300 uppercase tracking-widest">{saveStatus}</span>}
          </div>

          {/* Inputs */}
          <div className="border border-stone-800 mt-6">
            <div className="px-3 py-2 bg-stone-900/50">
              <span className="font-mono text-[10px] uppercase tracking-widest text-stone-400">Daily Inputs</span>
            </div>

            <Section title="Quick Reference Price & Notes" defaultOpen={false}>
              <NumInput label="Today's Price ($)" value={inputs.price} onChange={(v) => update('price', v)} step="0.01" />
              <div className="mb-3">
                <label className="block text-stone-400 font-mono text-xs mb-1">Notes</label>
                <textarea value={inputs.notes} onChange={(e) => update('notes', e.target.value)}
                  className="w-full bg-stone-950 border border-stone-700 text-stone-100 font-mono text-xs px-3 py-2 focus:border-amber-400 focus:outline-none"
                  rows="2" placeholder="Anything worth flagging today..."
                />
              </div>
            </Section>

            <Section title="Layer 1 — Fundamental Floor" defaultOpen={false}>
              <div className="mb-3">
                <label className="block text-stone-400 font-mono text-xs mb-2">Cash + Marketable Securities vs Market Cap</label>
                <div className="space-y-1">
                  {[['over50','> 50% (10 pts)'],['over30','30-50% (5 pts)'],['under30','< 30% (0 pts)']].map(([v,l]) => (
                    <button key={v} onClick={() => update('cashOverMcap', v)}
                      className={`w-full text-left px-3 py-2 font-mono text-xs border transition-colors ${inputs.cashOverMcap === v ? 'bg-amber-400/10 border-amber-400 text-amber-200' : 'bg-stone-950 border-stone-800 text-stone-400 hover:border-stone-600'}`}
                    >{l}</button>
                  ))}
                </div>
              </div>
              <Toggle label="Operating cash flow positive last quarter" value={inputs.ocfPositive} onChange={(v) => update('ocfPositive', v)} />
              <Toggle label="No imminent dilution announced" value={inputs.noDilutionRisk} onChange={(v) => update('noDilutionRisk', v)} hint="Watch convertible note announcements, ATM filings" />
            </Section>

            <Section title="Layer 2 — Technical Setup">
              <Toggle label="Price > 50-day moving average" value={inputs.priceOver50dma} onChange={(v) => update('priceOver50dma', v)} />
              <Toggle label="Price > 200-day moving average" value={inputs.priceOver200dma} onChange={(v) => update('priceOver200dma', v)} />
              <NumInput label="RSI (14)" value={inputs.rsi} onChange={(v) => update('rsi', v)} min="0" max="100" step="1" hint="Recovery zone 40-65 favored. Above 75 deducts." />
              <NumInput label="Volume Ratio (today / 20-day avg)" value={inputs.volRatio} onChange={(v) => update('volRatio', v)} hint="> 1.5x scores. From any chart platform." />
            </Section>

            <Section title="Layer 3 — Options Tape" accent>
              <NumInput label="Call Volume Ratio (today / 20-day avg)" value={inputs.callRatio} onChange={(v) => update('callRatio', v)} hint="> 2x = 10 pts. > 3x = 15 pts. The smoking gun layer." />
              <NumInput label="IV Rank (0-100)" value={inputs.ivRank} onChange={(v) => update('ivRank', v)} min="0" max="100" step="1" hint="< 30 = cheap premium. < 15 = exceptional." />
              <NumInput label="Put / Call Volume Ratio" value={inputs.putCallRatio} onChange={(v) => update('putCallRatio', v)} hint="< 0.5 indicates upside positioning" />
              <Toggle label="Multi-day persistence (3+ unusual days)" value={inputs.optionsPersistence} onChange={(v) => update('optionsPersistence', v)} />
            </Section>

            <Section title="Layer 4 — Structural Backdrop">
              <Toggle label="XRT on Reg SHO Threshold List" value={inputs.xrtThreshold} onChange={(v) => update('xrtThreshold', v)} hint="Check nyse.com/regulation/threshold-securities" />
              <NumInput label="Days to Next Quarter End" value={inputs.daysToQuarterEnd} onChange={(v) => update('daysToQuarterEnd', v)} step="1" min="0" max="92" hint="< 15 days scores" />
              <NumInput label="Short Volume % (FINRA)" value={inputs.shortVolPct} onChange={(v) => update('shortVolPct', v)} step="1" min="0" max="100" hint="> 50% scores. From shortvolume.com or Fintel" />
              <Toggle label="Borrow Fee Trending Up Week-over-Week" value={inputs.borrowFeeRising} onChange={(v) => update('borrowFeeRising', v)} />
              <Toggle label="DRS share count maintained ~25% of float" value={inputs.drsLocked} onChange={(v) => update('drsLocked', v)} />
            </Section>

            <Section title="Layer 5 — Catalyst Watch" accent>
              <Toggle label="Cohen Form 4 buy in last 7 days" value={inputs.cohenBuy7d} onChange={(v) => update('cohenBuy7d', v)} hint="Check SEC EDGAR or OpenInsider" />
              <Toggle label="Cohen X post / public statement in last 7 days" value={inputs.cohenPost7d} onChange={(v) => update('cohenPost7d', v)} />
              <Toggle label="Gill social media activity in last 7 days" value={inputs.gillActive7d} onChange={(v) => update('gillActive7d', v)} hint="@TheRoaringKitty, u/DeepFuckingValue, YouTube" />
              <Toggle label="Earnings within 30 days" value={inputs.earningsWithin30d} onChange={(v) => update('earningsWithin30d', v)} />
              <Toggle label="Material macro/regulatory event" value={inputs.macroEvent} onChange={(v) => update('macroEvent', v)} hint="T+0 transition, swap rule changes, market structure shifts" />
            </Section>
          </div>

          <div className="text-stone-600 font-mono text-[10px] leading-relaxed pt-4 border-t border-stone-800">
            Not financial advice. The Kitty Score reports condition similarity to historical pre-spike setups. Past patterns do not have to recur. Gill's edge was conviction over years; this tool tracks conditions, not certainty.
          </div>
        </div>
      )}

      {activeTab === 'history' && (
        <div className="p-4 space-y-4">
          {recentHistory.length === 0 ? (
            <div className="border border-stone-800 p-8 text-center">
              <AlertCircle className="w-6 h-6 mx-auto text-stone-600 mb-2" />
              <div className="font-mono text-xs text-stone-500">No saved entries yet. Save today's entry from the Today tab.</div>
            </div>
          ) : (
            <>
              <div className="border border-stone-800 p-4">
                <div className="font-mono text-[10px] uppercase tracking-widest text-stone-400 mb-3">Score Trend ({recentHistory.length} entries)</div>
                <div className="h-48">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={recentHistory.map(e => ({ date: e.date.slice(5), score: e.total }))}>
                      <XAxis dataKey="date" tick={{ fill: '#78716c', fontSize: 10, fontFamily: 'JetBrains Mono' }} stroke="#44403c" />
                      <YAxis domain={[0, 100]} tick={{ fill: '#78716c', fontSize: 10, fontFamily: 'JetBrains Mono' }} stroke="#44403c" />
                      <Tooltip
                        contentStyle={{ background: '#1c1917', border: '1px solid #44403c', fontFamily: 'JetBrains Mono', fontSize: '11px' }}
                        labelStyle={{ color: '#fbbf24' }}
                      />
                      <ReferenceLine y={71} stroke="#fbbf24" strokeDasharray="3 3" label={{ value: 'Heightened', fill: '#fbbf24', fontSize: 9 }} />
                      <ReferenceLine y={51} stroke="#78716c" strokeDasharray="3 3" />
                      <Line type="monotone" dataKey="score" stroke="#fbbf24" strokeWidth={2} dot={{ fill: '#fbbf24', r: 3 }} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>

              <div className="border border-stone-800">
                <div className="px-3 py-2 bg-stone-900/50 flex justify-between items-center">
                  <span className="font-mono text-[10px] uppercase tracking-widest text-stone-400">Saved Entries</span>
                  <button onClick={clearHistory} className="text-stone-500 hover:text-rose-400 transition-colors">
                    <Trash2 className="w-3 h-3" />
                  </button>
                </div>
                <div className="divide-y divide-stone-800 max-h-96 overflow-y-auto">
                  {[...recentHistory].reverse().map((e, i) => (
                    <div key={i} className="px-3 py-2 flex items-center justify-between">
                      <div>
                        <div className="font-mono text-xs text-stone-300 tabular">{e.date}</div>
                        {e.price && <div className="font-mono text-[10px] text-stone-600 tabular">${Number(e.price).toFixed(2)}</div>}
                      </div>
                      <div className="text-right">
                        <div className={`font-mono text-sm tabular ${getState(e.total).tone}`}>{e.total}<span className="text-stone-700">/100</span></div>
                        <div className="font-mono text-[10px] text-stone-600 uppercase tracking-wider">{getState(e.total).label}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
        </div>
      )}

      {activeTab === 'method' && (
        <div className="p-4 space-y-4 font-mono text-xs text-stone-300 leading-relaxed">
          <div>
            <div className="font-display text-2xl text-amber-400 italic mb-2">Philosophy</div>
            <p>Five layers, scored daily. Built from forensic work on the January 2021 and May 2024 GME spikes. Designed to think like Keith Gill: deep value floor first, technical entry second, options tape third, structural backdrop fourth, catalyst watch fifth.</p>
          </div>

          <div className="border border-stone-800 p-3">
            <div className="text-amber-300 uppercase tracking-widest text-[10px] mb-2">Score States</div>
            <div className="space-y-1">
              <div className="flex justify-between"><span>0-30</span><span className="text-stone-500">Quiet</span></div>
              <div className="flex justify-between"><span>31-50</span><span className="text-stone-300">Watching</span></div>
              <div className="flex justify-between"><span>51-70</span><span className="text-amber-200">Elevated</span></div>
              <div className="flex justify-between"><span>71-85</span><span className="text-amber-300">Heightened</span></div>
              <div className="flex justify-between"><span>86-100</span><span className="text-amber-400">Significant Convergence</span></div>
            </div>
          </div>

          <div>
            <div className="text-amber-300 uppercase tracking-widest text-[10px] mb-2">Layer Weights</div>
            <p className="text-stone-400">Floor 20 · Technical 20 · Options Tape 25 · Structural 15 · Catalyst 20. The options tape is the heaviest single layer because it was the cleanest pre-May-2024 signal in the historical record.</p>
          </div>

          <div>
            <div className="text-amber-300 uppercase tracking-widest text-[10px] mb-2">Free Data Sources</div>
            <ul className="space-y-1 text-stone-400">
              <li>· Price, volume, RSI, MAs: Yahoo Finance, TradingView, Barchart</li>
              <li>· Options activity: Barchart unusual options, OptionCharts.io</li>
              <li>· IV rank: Market Chameleon (free tier), Barchart</li>
              <li>· Short volume: Fintel, ChartExchange, shortvolume.com</li>
              <li>· FTDs: SEC.gov, ChartExchange, companiesmarketcap.com</li>
              <li>· XRT threshold: nyse.com/regulation/threshold-securities</li>
              <li>· DRS, cash position: SEC EDGAR (10-Q, 10-K)</li>
              <li>· Form 4 filings: SEC EDGAR, OpenInsider</li>
            </ul>
          </div>

          <div>
            <div className="text-amber-300 uppercase tracking-widest text-[10px] mb-2">Notifications & True Automation</div>
            <p className="text-stone-400">This tool runs in your browser. It cannot push notifications or run on a schedule. For true automation, run a Python script on a personal server that pulls the same data, computes the score, and pushes via Pushover, Telegram bot, or ntfy.sh. Ask Claude for the script if you want it.</p>
          </div>

          <div>
            <div className="text-amber-300 uppercase tracking-widest text-[10px] mb-2">Limitations</div>
            <ul className="space-y-1 text-stone-400">
              <li>· Calibrated against a small sample (n=2 major spikes). Statistical robustness is low.</li>
              <li>· Several inputs require subjective interpretation.</li>
              <li>· Does not account for macro market regime.</li>
              <li>· Past pre-spike conditions do not have to recur.</li>
              <li>· Not investment advice. Tracks conditions, not certainty.</li>
            </ul>
          </div>

          <div className="pt-4 border-t border-stone-800">
            <div className="font-display text-amber-400 italic text-lg">Remember.</div>
            <p className="text-stone-400 mt-1">Gill's edge was a fundamental floor that let him hold for years, plus a technical eye that recognized when the setup was finally cooked. The score points to the latter. The former is the part you bring yourself.</p>
          </div>
        </div>
      )}
    </div>
  );
}
