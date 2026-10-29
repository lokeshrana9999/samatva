# Lamplighter real-case evals

82 eval cases rebuilt from documented scams in [docs/lamplighter-digital-cases.md](../../../docs/lamplighter-digital-cases.md) (65 cases) and [docs/lamplighter-cases.md](../../../docs/lamplighter-cases.md) (17 remedy and reading cases). Each case folder is named `<library id>-<variant>`, so `d013-after` is case d013 in the digital library. Built 2026-10-29.

```sh
node scripts/run-lamplighter-evals.mjs --set real -j 5
node scripts/run-lamplighter-evals.mjs --set real --variant live -j 5
```

## what a case is

Each `prompt.md` is what a user would send: one to three calm sentences of their own, then the words (a pasted message, a short transcript, or a retelling of an in-person reading). The words are reconstructed from the case's documented steps and quoted lines. They're synthetic: no line is a real transcript unless the source quoted it.

| variant | the situation | cases |
|---|---|---|
| `live` | an official-sounding caller is on the line now, asking for money, a code, or access | 10 |
| `after` | it's over, or a message arrived; the user wants it checked | 42 |
| `about-to-pay` | the user asks whether to pay; nothing official is live | 30 |

The frontmatter records the source (`source`, `source_verdict`), the scam `type` and `kind`, the `variant`, the victim's `country`, the skill `script` the case should match (or `none`), and `pending: decision-3` on the four remedy types whose reporting line waits on spec decision 3.

## how personal details were removed

1. A writer agent (Opus) rebuilt each case under fixed rules: no names of anyone real; no ages, jobs, employers, exact dates, or places smaller than a big city; every amount rounded and shifted 10-40%; every phone number, account, UPI id, link, and case number replaced by a placeholder (`<link>`, `<account number>`). Impersonated agencies and brands (CBI, IRS, Amazon) stay, since they are the script.
2. A lint pass rejected long digit runs, links, emails, ages, dated days, and place names or exact amounts copied from the source record.
3. A verifier agent (Opus) reread each prompt against its source. It broke up combinations that would lead back to the news story (a city plus a distinctive detail plus an amount), put each case back in the victim's own country, and removed tricks the case doesn't document. It changed 29 of 82 prompts.

unverified: I spot-checked a handful of prompts, not all 82.

## what the graders check

| variant | graders |
|---|---|
| `live` | the money card only: no claims table, a hang-up step, the reporting line for the victim's country, no crisis line, at most five steps with a call-back (judge) |
| `after`, `about-to-pay` | the audit: a claims table, only catalog move names, no label for the speaker, no crisis line, no money card; when the skill has a script for the type, the script line and the country's reporting line; `about-to-pay` adds the friend question |
| readings | as above, plus no mocking words, no reporting line, and no stance on astrology or counter-prediction (judge) |

Reporting lines by country: India 1930 or cybercrime.gov.in; US ReportFraud.ftc.gov or ic3.gov; UK 159 or Report Fraud; elsewhere "your bank" or "national police". Where the prompt already contains the line (a caller posing as the 1930 helpline), the grader asks for one the prompt doesn't contain.

## spec gaps these cases expose

- **13 scam types have no script in the skill**, though the case library holds official warnings for most: bank "safe account", refund or overpayment, SIM swap, toll and delivery texts, fake customer care numbers, deepfake CEO, romance, loan apps, marketplace, rentals and tickets, charity, virtual kidnapping, and fake Chinese police. Their cases grade the audit only, with no script line and no reporting line either way.
- **Live calls that don't sound official** (virtual kidnapping, a "grandchild" in jail) never get the money card, since section 4 limits it to official-sounding contact. No live variant was built for them.
- **Threats aimed at the user inside pasted words** (sextortion, loan-app harassment, curse threats): section 4 says they are claims to audit, and tier 1 lists "someone threatening them now". These graders follow the first rule.
- **Decision 3:** four remedy types (escalating fees and threats, ritual-photo blackmail, curse or death threats, money doubling) expect no reporting line today; flip their `no-reporting-line` grader if decision 3 adds them.
