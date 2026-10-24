Closes #

<!-- One line: what this changes, in a sentence a user would understand. -->

## before merging

<!-- From CONTRIBUTING.md. Tick what you did; write "n/a" after an item that doesn't apply. -->

- [ ] Everything added is synthetic: invented first names, no real person, workplace, event, chat export, or voice profile.
- [ ] Ran `skill-auditor` (from the shipyard plugin) on the changed skill and fixed what its report found. The report is not committed.
- [ ] Ran that skill's evals, `bash scripts/run-evals.sh plugins/samatva --tag <skill> --scaffold`, and checked with `eval-stats.py` that the with-minus-without delta is positive and no new `NON-DISCRIMINATING` or `UNDERPOWERED` flag appears. Eval results are not committed.
- [ ] If a script changed, its tests ran.
- [ ] `node scripts/sync-shared.mjs --check` and `claude plugin validate plugins/samatva` pass.
- [ ] If the voice schema or the example profile changed, `python plugins/samatva/scripts/profile-lint.py examples/voice.md` prints `clean`.
- [ ] Added a line under `Unreleased` in CHANGELOG.md.
