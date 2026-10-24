# contributing

A skill is a folder under `plugins/samatva/skills/` holding a `SKILL.md` (frontmatter `name` and `description`, then the instructions) and optional `references/`. Changes land through a branch and a pull request against `main`. Contributions are licensed under the repo's [MIT license](LICENSE).

## repo layout

```
.claude-plugin/marketplace.json       Claude Code marketplace "samatva"
plugins/samatva/
  .claude-plugin/plugin.json          Claude Code plugin manifest
  README.md, LICENSE                  plugin README and license
  skills/<skill>/                     SKILL.md plus references/
  skills/_shared/                     risk-handoff.md, no-memory.md, arousal-check.md: the one source for each shared block
  scripts/                            voice-stats.py, profile-lint.py, arousal.py (optional, stdlib only)
  docs/sources/<skill>.md             where each skill's rules came from
docs/                                 voice.md, evals.md, architecture.md
examples/                             voice.md (synthetic profile), samatva-settings/ (example overlays)
evals/samatva/<skill>/<case>/         eval cases per skill (kept out of the shipped plugin)
evals/samatva/transcripts/            the synthetic transcripts the cases embed
evals/config/                         per-OS eval config (windows.sh)
scripts/                              run-evals.sh, eval-stats.py (copied unchanged from shipyard),
                                      sync-shared.mjs
```

## rules for skills

- Restraint lives in the text. Name every forbidden move explicitly (advice, options, "have you considered", agreeing with a plan, labelling a third party), give each reply a cap in sentences and words, and say what the model does instead. A rule a sycophantic model can read around is not a rule.
- Every `SKILL.md` carries the `risk-handoff` and `no-memory` blocks between their markers; `samatva`, `vent`, `think-it-through`, `before-you-send`, and `cool-down-close` also carry `arousal-check`, so every skill that gates on arousal counts the same signs. Edit `skills/_shared/<block>.md`, never the pasted copy, then run `node scripts/sync-shared.mjs`; `--check` fails if a required block is missing.
- Restraint beats voice. A voice profile changes the surface of a reply (language, script, case, length within the cap), never its content. Voice settings never go in an overlay, and an overlay can only tighten a rule; a skill ignores any overlay value that would loosen one.
- Don't depend on one agent. Every skill must work in a chat app with no file access and no shell: say what to do without the script, the voice file, or the Skill tool.
- Write patterns, not specifics, and mark defaults as defaults (`default: 15 turns`). The one exception is the crisis resource list, which lives only in `skills/_shared/risk-handoff.md`; recheck every number on it before each release.
- Record where a rule came from in `plugins/samatva/docs/sources/<skill>.md`. That folder sits outside `skills/`, so it never loads into an agent's context.

## privacy rules for the repo

- Every transcript, fixture, and example is synthetic: invented first names, no real person, workplace, or event. If a case is modelled on a real conversation, rename every person and place, change every amount and date, and rephrase every line.
- Never commit a real chat export or a real voice profile. `.gitignore` excludes `.claude/samatva/`; keep exports outside the repo.

## before merging

1. Run `skill-auditor` (from the shipyard plugin) on the changed skill and fix what its report finds. Don't commit the report.
2. Run that skill's evals, `bash scripts/run-evals.sh plugins/samatva --tag <skill> --scaffold`, and check with `eval-stats.py` that the with-minus-without delta is positive and no new `NON-DISCRIMINATING` or `UNDERPOWERED` flag appears. Details are in [docs/evals.md](docs/evals.md).
3. Check nothing is stale: `node scripts/sync-shared.mjs --check` and `claude plugin validate plugins/samatva`.
4. If you touched the voice schema or the example profile, run `python plugins/samatva/scripts/profile-lint.py examples/voice.md`; it must print `clean`.
5. Add a line under `Unreleased` in [CHANGELOG.md](CHANGELOG.md).

Never commit eval results (`evals/samatva/results/`); they're git-ignored.

## trying a change

In Claude Code, start it with `claude --plugin-dir plugins/samatva` from the repo root. In other agents, link the skill folder from your checkout into their skills folder, or run `npx skills add <path to your checkout> --skill <skill> --agent <agent>`. To try a skill in a chat app such as claude.ai, upload the skill folder as a custom skill; the scripts don't run there, and each skill says what it does instead.
