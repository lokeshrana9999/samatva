# Privacy

samatva collects nothing. The plugin has no server, no telemetry, and no analytics: it's a set of instruction files and three optional local scripts that your agent reads and runs on your machine.

What the skills do with your words happens inside your own agent session:

- The conversational skills (`vent`, `think-it-through`, `cool-down-close`, `before-you-send`, the `samatva` router) are told to write nothing that outlives the conversation about your relationships, family, finances, health, or anyone you name: no memory tool, no notes file, no project instructions file.
- `cold-read-check` reads the transcript you give it and writes an audit file only when you ask for one, where you say.
- `voice-setup` reads chat exports you point it at, in place, and never copies them into a scratch file, the repo, or the profile. Reading them does bring their text, other people's lines included, into your agent's context: like anything your agent reads, it goes to your model provider and into your agent's local session history, so use an export you're comfortable handling that way. It writes one file, your voice profile (by default `~/.claude/samatva/voice.md`), after a scrub pass that looks for names, places, employers, amounts, dates, relationship and health facts, and any run of more than four words from your messages (with a shell, `profile-lint.py` checks too). It shows you the whole profile before it writes, and the profile is a plain markdown file you can read, edit, or delete.
- The scripts (`voice-stats.py`, `profile-lint.py`, `arousal.py`) use only the Python standard library, make no network calls, and print counts and findings, never message text.

These are instructions to a model, not enforced controls; see the honest limit in the [README](README.md#the-honest-limit). Your agent's own provider (for example Anthropic for Claude Code or claude.ai) processes what you type under that provider's terms. Nothing is sent to the author of this plugin.

Questions: open an issue at https://github.com/lokeshrana9999/samatva/issues.
