# Settings example

A person keeps this at `~/.claude/samatva/vent.md`, or a project at `.claude/samatva/vent.md`; when both exist, vent reads both and the stricter value of each key wins, so a file the person didn't write (one committed to a cloned repo, say) can't loosen what they chose. Every setting is optional; anything left out keeps the default in SKILL.md.

Settings can only make vent more restrained. A value that would loosen a rule is ignored and the default stays, so a typo or a bad copy can't switch the restraint off.

```markdown
# vent settings

- max-sentences: 1
- max-words: 25
- hold-turns: 5
- close-after: 10
- questions: none
```

- `max-sentences`: `1` or `2` (default `2`). One-sentence reflections suit someone for whom two sentences already feel like too much talk. Any other value is ignored.
- `max-words`: a whole number from `1` to `40` (default `40`). The voice cap (`median-words` x 1.5) still applies; the smaller of the two wins. Above 40 is ignored.
- `hold-turns`: a whole number, `3` or more (default `3`): how many user turns vent stays before it may offer think-it-through, even once the gate is clear. Below 3 is ignored.
- `close-after`: a whole number from `1` to `15` (default `15`): after this many user turns since they first brought up what upset them, counted across every samatva skill, vent offers cool-down-close, and at twice this many it hands over without asking. Above 15 is ignored. think-it-through and cool-down-close read the same key, with the same count, from their own settings files. Set it below `hold-turns` and vent offers to close before it would offer think-it-through.
- `questions`: `none` or `few` (default `few`). `none`: every reply ends in silence. `few`: at most one open question in a reply, and never in two replies in a row. A voice profile's `wants-questions: none` also means none; the stricter of the two wins.

What settings can't do: change the voice (that lives in `voice.md`, from voice-setup), turn off the risk block or the boundaries, allow advice, options, verdicts, or labels, or show the gate to the user.

In a chat app with no file access, paste the same `# vent settings` block into the conversation or the project instructions.
