# samatva evals

Eval cases for the `samatva` plugin, kept here rather than in `plugins/samatva/` so the published plugin ships no fixtures; one folder per skill (`vent/`, `think-it-through/`, ...), each case a `prompt.md` plus `graders/*.md`, and a `case.yaml` with a `fixture.sh` when it plants a voice profile. `transcripts/` holds the synthetic transcripts the prompts embed, since `claude plugin eval` has no multi-turn prompts. Everything here is synthetic: no real person, chat, or event. Run from the repo root:

```sh
bash scripts/run-evals.sh plugins/samatva --tag vent --scaffold -j 3
```

Flags, reading results with `eval-stats.py`, writing cases, and the platform config: [docs/evals.md](../../docs/evals.md). `scripts/run-evals.sh` stages a copy of the plugin with these cases under its `evals/` and runs `claude plugin eval` there. Results land in `results/` here, git-ignored.
