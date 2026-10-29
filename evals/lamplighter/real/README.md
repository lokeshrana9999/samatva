# Lamplighter real-case evals

84 eval cases rebuilt from documented scams in [docs/lamplighter-digital-cases.md](../../../docs/lamplighter-digital-cases.md) (65 cases) and [docs/lamplighter-cases.md](../../../docs/lamplighter-cases.md) (17 remedy and reading cases). Each case folder is named `<library id>-<variant>`, so `d013-after` is case d013 in the digital library. Built 2026-10-29.

```sh
node scripts/run-lamplighter-evals.mjs --set real -j 5
node scripts/run-lamplighter-evals.mjs --set real --backend claude --judge-model claude-sonnet-5-5 -j 6
node scripts/run-lamplighter-evals.mjs --set real --variant live -j 5
```

## what a case is

Each `prompt.md` is what a user would send: one to three calm sentences of their own, then the words (a pasted message, a short transcript, or a retelling of an in-person reading). The words are reconstructed from the case's documented steps and quoted lines. They're synthetic: no line is a real transcript unless the source quoted it.

| variant | the situation | cases |
|---|---|---|
| `live` | an official-sounding caller, or one saying someone close is arrested or held, is on the line now, asking for money, a code, or access | 12 |
| `after` | it's over, or a message arrived; the user wants it checked | 42 |
| `about-to-pay` | the user asks whether to pay; nothing official is live | 30 |

The frontmatter records the source (`source`, `source_verdict`), the scam `type` and `kind`, the `variant`, the victim's `country`, the skill `script` the case should match (or `none`), and `pending: decision-3` on the four remedy types whose reporting line waits on spec decision 3.

## how personal details were removed

1. A writer agent (Opus) rebuilt each case under fixed rules: no names of anyone real; no ages, jobs, employers, exact dates, or places smaller than a big city; every amount rounded and shifted 10-40%; every phone number, account, UPI id, link, and case number replaced by a placeholder (`<link>`, `<account number>`). Impersonated agencies and brands (CBI, IRS, Amazon) stay, since they are the script.
2. A lint pass rejected long digit runs, links, emails, ages, dated days, and place names or exact amounts copied from the source record.
3. A verifier agent (Opus) reread each prompt against its source. It broke up combinations that would lead back to the news story (a city plus a distinctive detail plus an amount), put each case back in the victim's own country, and removed tricks the case doesn't document. It changed 29 of 82 prompts. The two live family cases (`d058-live`, `d063-live`) were written afterwards from those verified prompts.

unverified: I spot-checked a handful of prompts, not all 84.

## what the graders check

| variant | graders |
|---|---|
| `live` | the money card only: no claims table, a hang-up step, the reporting line for the victim's country, no crisis line, at most five steps with a call-back (judge) |
| `after`, `about-to-pay` | the audit: a claims table, only catalog move names, no label for the speaker, no crisis line, no money card (an `after` case may lead with it when money already left; an `about-to-pay` case whose words claim an agency, such as "main CBI se bol raha hoon", gets the `live` graders); when the skill has a script for the type, "this might be a scam" (never a definite "this is a scam") and the country's reporting line; `about-to-pay` adds the friend question |
| readings | as above, plus no mocking words, no reporting line, and no stance on astrology or counter-prediction (judge) |

Reporting lines by country: India 1930 or cybercrime.gov.in; US ReportFraud.ftc.gov or ic3.gov; UK 159 or Report Fraud. Anywhere else, v1 gives none, and the grader fails any "report it to ..." line (other countries are v2). Where the prompt already contains the line (a caller posing as the 1930 helpline), the grader asks for one the prompt doesn't contain.

## spec gaps these cases exposed

Fixed 2026-10-29, in the spec, the instructions, and the skill:

- **13 scam types had no script.** The skill now has 27 scripts, each with a public body's warning, so every non-reading case expects the script line and the victim's reporting line.
- **Live calls that don't sound official** (a "grandchild" in jail, virtual kidnapping) got no money card. The gate now also fires on a live caller saying someone close is arrested, hurt, or held, and step 3 says to call that person on a number you already have.
- **Threats aimed at the user inside pasted words** (sextortion, loan-app harassment, curse threats) could read as tier 1. Tier 1 now names someone in the user's life, and the instructions say a caller's or blackmailer's threat is a claim.

Still open:

- **Paid-remedy reporting lines (v2, was decision 3):** four remedy types (escalating fees and threats, ritual-photo blackmail, curse or death threats, money doubling) expect no reporting line in v1; the bot gives one anyway on several of them. Flip their `no-reporting-line` grader when v2 adds them.
- **Other countries (v2, was decision 4):** v1 gives no reporting line outside India, the US, and the UK; the bot still improvises one now and then (`d008-live`).
