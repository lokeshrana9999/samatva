# Lamplighter Grok Bot

The build of the Lamplighter template specified in [docs/lamplighter.md](../../docs/lamplighter.md). Two files go into the Grok Bot; nothing else does (no routines, files, connectors, secrets, or seeded memory).

| file | goes into | limit |
|---|---|---|
| [instructions.md](instructions.md) | the Bot's standing role, sent in chat | 4,000 characters (a community figure, unverified); `--check` enforces it |
| [skills/lamplighter-patterns/SKILL.md](skills/lamplighter-patterns/SKILL.md) | one private skill, named `lamplighter-patterns`, created in chat | none known |

The instructions hold what must work even if the skill never loads: the risk gate with its helplines, the money-gate card, the flooded check, the protection-first order, the look-up rule for unlisted countries, the exits, and the hard rules. The skill holds the first-reply template, the audit template, the tags, the closed list of 28 moves, the published scam scripts, and the reporting lines.

## set it up

Personal Bots have no settings page: the role and the skill are set by chatting with the new Bot.

1. Open Grok Bot and create a Bot named Lamplighter.
2. In its chat, send: "Remember everything inside <instructions> below as your standing role, exactly as written. Reply with one word: saved." followed by `instructions.md` inside `<instructions>` tags.
3. Then send: "Create a private skill named lamplighter-patterns from the text inside <skill> below, exactly as written. Reply with one word: created." followed by `SKILL.md` inside `<skill>` tags.
4. Leave routines, files, and connectors empty.
5. Publish: Share, Create a copy, Publish, Copy link. The listing copy and avatar are kept with the launch media, outside this repo.

## check it

```sh
node scripts/run-lamplighter-evals.mjs --check
node scripts/run-lamplighter-evals.mjs --arm shipped -j 5
node scripts/run-lamplighter-evals.mjs --arm shipped --tier zero --full -j 5
node scripts/run-lamplighter-evals.mjs --set real -j 5
node scripts/run-lamplighter-evals.mjs --backend claude --judge-model claude-sonnet-5-5 -j 6
node scripts/run-lamplighter-evals.mjs --set multi -j 5
```

The first verifies the instruction length and the catalog. The second runs every case in [evals/lamplighter/](../../evals/lamplighter/) once through the signed-in `grok` CLI, which is spec layer 1, a proxy: the instructions and the skill go in as one system prompt on a Grok coding model, not the Bot itself. The third is the launch gate: each zero-tolerance case for its own run count (30 or 100). The fourth runs 84 cases rebuilt from the documented scams in the case libraries, with personal details removed ([evals/lamplighter/real/](../../evals/lamplighter/real/README.md)). The fifth sends the same prompts through `claude -p` on Haiku 5.5 with a Sonnet 5.5 judge, for when Grok usage runs out; it shows the text holds on another model family, not on Grok. Results go to `evals/lamplighter/results/`, git-ignored. The sixth is layer 2: nine scripted conversations in [evals/lamplighter/multi/](../../evals/lamplighter/multi/) that push on one rule each over several turns (a verdict on a friend, "just say it's a scam", "is astrology real?", a caller who won't let you hang up), each turn graded. Layer 3 is manual, in a real copy of the template: [acceptance.md](acceptance.md).

The eval sets are generated, not hand-edited: `scripts/lamplighter/make-cases.js` (core), `scripts/lamplighter/real/build-real.js` (real cases, from `briefs-index.json` and the verified prompts in `verified/`), and `scripts/lamplighter/make-multi.js` (layer 2). Change a generator and rerun it rather than editing graders by hand.
