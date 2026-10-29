// Step 1 of the real-case build (2026-10-29): picks library cases and writes writer briefs. Its output,
// briefs-index.json, was then edited by hand (scripts set on 13 types, two live variants added), so rerun only to start over.
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..', '..', '..');
const d = require(path.join(root, 'docs/lamplighter-digital-cases.json'));
const r = require(path.join(root, 'docs/lamplighter-cases.json'));

// kind: official (money gate can fire), offer (money offer), pressure (threats to the user), reading
// script: the skill's script this type should match, or null (no script in the skill yet)
// variants: which scenarios to write; live only for the first case of a type
const TYPES = {
  'gov-impersonation-tax': { kind: 'official', script: 'tax agency, court, or jury-duty fine by phone', variants: ['live', 'after'] },
  'police-court-fine': { kind: 'official', script: 'tax agency, court, or jury-duty fine by phone', variants: ['live', 'after'] },
  'digital-arrest': { kind: 'official', script: 'digital arrest', variants: ['live', 'after'] },
  'courier-customs-parcel': { kind: 'official', script: 'official-sounding parcel with drugs or a seized package', variants: ['live', 'after'] },
  'chinese-police-embassy': { kind: 'official', script: null, variants: ['live', 'after'] },
  'utility-disconnection': { kind: 'official', script: 'utility cut-off today', variants: ['live', 'after'] },
  'kyc-sim-block': { kind: 'official', script: 'KYC update or SIM block', variants: ['live', 'after'] },
  'bank-safe-account': { kind: 'official', script: null, variants: ['live', 'after'] },
  'tech-support': { kind: 'official', script: 'tech support pop-up or call, remote access', variants: ['live', 'after'] },
  'refund-overpayment': { kind: 'official', script: null, variants: ['after'] },
  'gift-card-payment': { kind: 'official', script: 'gift cards as payment', variants: ['live', 'after'] },
  'sim-swap-otp-takeover': { kind: 'official', script: null, variants: ['after'] },
  'delivery-toll-smishing': { kind: 'official', script: null, variants: ['after'] },
  'fake-customer-care': { kind: 'official', script: null, variants: ['after'] },
  'deepfake-ceo-bec': { kind: 'official', script: null, variants: ['after'] },
  'family-emergency-voice-clone': { kind: 'pressure', script: 'family emergency call, voice possibly cloned', variants: ['after'] },
  'virtual-kidnapping': { kind: 'pressure', script: null, variants: ['after'] },
  'lottery-prize': { kind: 'offer', script: 'prize or lottery with a fee', variants: ['about-to-pay'] },
  'pig-butchering-crypto': { kind: 'offer', script: 'crypto platform from an online contact', variants: ['about-to-pay'] },
  'investment-tips-groups': { kind: 'offer', script: 'guaranteed returns, stock-tip groups', variants: ['about-to-pay'] },
  'task-job': { kind: 'offer', script: 'task or part-time job, pay to unlock earnings', variants: ['about-to-pay'] },
  romance: { kind: 'offer', script: null, variants: ['about-to-pay'] },
  'marketplace-buyer-seller': { kind: 'offer', script: null, variants: ['about-to-pay'] },
  'rental-booking-ticket': { kind: 'offer', script: null, variants: ['about-to-pay'] },
  'charity-disaster': { kind: 'offer', script: null, variants: ['about-to-pay'] },
  'recovery-scam': { kind: 'offer', script: 'recovery offer after a loss', variants: ['about-to-pay'] },
  sextortion: { kind: 'pressure', script: 'intimate images, then payment demands', variants: ['after'] },
  'loan-app-harassment': { kind: 'pressure', script: null, variants: ['after'] },
};
const REMEDY = {
  'online-astrologer-remedy': 'about-to-pay', 'disease-cure-puja': 'about-to-pay', 'vashikaran-love-problem': 'about-to-pay',
  'black-magic-removal': 'about-to-pay', other: 'about-to-pay', 'money-gold-doubling': 'about-to-pay',
  'escalating-fees-threats': 'after', 'ritual-photo-blackmail': 'after', 'curse-death-threat-extortion': 'after',
};
const DECISION3 = new Set(['escalating-fees-threats', 'ritual-photo-blackmail', 'curse-death-threat-extortion', 'money-gold-doubling']);

const country = (l) => {
  for (const [k, rx] of [['India', /India/], ['US', /USA|United States|\bUS\b|U\.S\./], ['UK', /\bUK\b|United Kingdom|England|Scotland|Wales/]]) if (rx.test(l)) return k;
  return 'elsewhere';
};
const score = (c) => (c.verdict === 'verified' ? 100 : 0) + ((c.quoted_lines || []).length ? 20 : 0) + (c.steps || []).length;
const pick = (list, n) => {
  const sorted = [...list].sort((a, b) => score(b) - score(a));
  const out = [];
  for (const c of sorted) {
    if (out.length >= n) break;
    // second pick prefers another country
    if (out.length && country(out[0].location) === country(c.location) && sorted.some((x) => !out.includes(x) && x !== c && country(x.location) !== country(out[0].location))) continue;
    out.push(c);
  }
  for (const c of sorted) if (out.length < n && !out.includes(c)) out.push(c);
  return out;
};

const briefs = [];
for (const [type, t] of Object.entries(TYPES)) {
  pick(d.cases.filter((c) => c.category === type), 2).forEach((c, i) => {
    for (const v of t.variants) {
      if (v === 'live' && i > 0) continue;
      briefs.push({ eval_id: `${c.id}-${v}`, source_id: c.id, library: 'digital', type, kind: t.kind, script: t.script, variant: v, country: country(c.location), case: c });
    }
  });
}
for (const [script, v] of Object.entries(REMEDY)) {
  pick(r.cases.filter((c) => c.script === script), 2).forEach((c) => {
    briefs.push({ eval_id: `${c.id}-${v}`, source_id: c.id, library: 'remedy', type: script, kind: 'reading', script: null, decision3: DECISION3.has(script), variant: v, country: country(c.location), case: c });
  });
}
const strip = ({ sources, ...c }) => c; // writers never need the source URLs
const out = path.join(__dirname, 'briefs');
fs.mkdirSync(out, { recursive: true });
const N = 4;
for (let b = 0; b < N; b++) {
  const batch = briefs.filter((_, i) => i % N === b).map((x) => ({ ...x, case: strip(x.case) }));
  fs.writeFileSync(path.join(out, `batch-${b + 1}.json`), JSON.stringify(batch, null, 1));
}
fs.writeFileSync(path.join(__dirname, 'briefs-index.json'), JSON.stringify(briefs.map(({ case: c, ...x }) => x), null, 1));
const tally = (k) => briefs.reduce((a, x) => ((a[x[k]] = (a[x[k]] || 0) + 1), a), {});
console.log(briefs.length, 'evals', JSON.stringify(tally('variant')), JSON.stringify(tally('kind')), JSON.stringify(tally('country')));
