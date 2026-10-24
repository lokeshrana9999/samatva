# Changelog

Notable changes to samatva, in the [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format. The version is the `samatva` plugin's, in `plugins/samatva/.claude-plugin/plugin.json`.

## [Unreleased]

### Added

- The `samatva` plugin and marketplace manifests, at 0.0.0 with no skills yet.
- Three shared blocks, pasted by `scripts/sync-shared.mjs` (with `--check` for CI): `risk-handoff.md` and `no-memory.md` for every `SKILL.md`, and `arousal-check.md` for the skills that gate on how worked up the user is.
- `scripts/run-evals.sh`, `scripts/eval-stats.py`, and `evals/config/windows.sh`, copied unchanged from the shipyard repo.
- The `check` workflow: shared blocks in sync, scripts compile, plugin and marketplace validate.
- Issue forms (bug, eval case, technique, crisis-line correction, unit) and a pull request template.
- `README.md`, `PRIVACY.md`, `CONTRIBUTING.md`, `LICENSE` (MIT), and `docs/architecture.md`, the design the skills are cut from.
