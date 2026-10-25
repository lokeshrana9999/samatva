# samatva review concerns

Project concerns for the shipyard `pr-review` skill, in the format of its `references/catalog.md`. They add to the starter catalog; an id that matches a starter concern replaces it.

## Process

- **Content outside the PR's unit** (`process/out-of-unit-scope`, default issue): A PR lands one unit, the issue it closes, and everything in it must belong to that unit. A file, hunk, or reference that belongs to another unit ships ahead of it: users read about a skill they can't run yet, links and hand-overs dangle, and the later unit's PR no longer shows its own change.
  - look-for: files or hunks the closed issue doesn't list; a relative link, a path in prose or a comment, a hand-over (`samatva:<skill>`, `../<skill>/SKILL.md`), or a skill name that points at a skill, file, or doc found neither on the base branch nor in this PR; tooling or config edits riding along with a skill.
  - gate: the target is already on the base branch or is added by this same PR.
