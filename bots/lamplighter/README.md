# Lamplighter Grok Bot

The build of the Lamplighter template specified in [docs/lamplighter.md](../../docs/lamplighter.md). Two files go into the Grok Bot; nothing else does (no routines, files, connectors, secrets, or seeded memory).

| file | goes into | limit |
|---|---|---|
| [instructions.md](instructions.md) | the Bot's instructions, pasted whole | 4,000 characters (a community figure, unverified); `--check` enforces it |
| [skills/lamplighter-patterns/SKILL.md](skills/lamplighter-patterns/SKILL.md) | one skill, named `lamplighter-patterns` | none known |

The instructions hold what must work even if the skill never loads: the risk gate with its helplines, the money-gate card, the flooded check, the exits, and the hard rules. The skill holds the audit: the tags, the closed list of 28 moves, the published scam scripts with their reporting lines, and the template.

## set it up

1. Open Grok Bot and create a Bot named Lamplighter, subtitle "light every move, judge no one", category Personal.
2. Paste `instructions.md` into its instructions.
3. Add a skill named `lamplighter-patterns` with the body of `SKILL.md` (its frontmatter description is the skill's description).
4. Leave routines, files, and connectors empty.
5. Publish: Share, Create a copy, Publish, Copy link. The listing copy and avatar are kept with the launch media, outside this repo.

## check it

```sh
node scripts/run-lamplighter-evals.mjs --check
node scripts/run-lamplighter-evals.mjs --arm shipped -j 5
node scripts/run-lamplighter-evals.mjs --arm shipped --tier zero --full -j 5
node scripts/run-lamplighter-evals.mjs --set real -j 5
node scripts/run-lamplighter-evals.mjs --backend claude --judge-model claude-sonnet-5-5 -j 6
```

The first verifies the instruction length and the catalog. The second runs every case in [evals/lamplighter/](../../evals/lamplighter/) once through the signed-in `grok` CLI, which is spec layer 1, a proxy: the instructions and the skill go in as one system prompt on a Grok coding model, not the Bot itself. The third is the launch gate: each zero-tolerance case for its own run count (30 or 100). The fourth runs 82 cases rebuilt from the documented scams in the case libraries, with personal details removed ([evals/lamplighter/real/](../../evals/lamplighter/real/README.md)). The fifth sends the same prompts through `claude -p` on Haiku 5.5 with a Sonnet 5.5 judge, for when Grok usage runs out; it shows the text holds on another model family, not on Grok. Results go to `evals/lamplighter/results/`, git-ignored. Layers 2 (scripted multi-turn) and 3 (manual, in a real copy of the template) aren't built.
