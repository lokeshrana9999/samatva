<!-- Source of truth for the arousal check in the samatva skills that gate on it (vent, think-it-through, before-you-send, cool-down-close, samatva). Optional block: pasted only where its markers are. Edit here, then run `node scripts/sync-shared.mjs`. This comment is not copied. -->
## arousal check

Run this silently every turn, before replying. Never show the result, a score, or a word like "flooded", and never tell the user how worked up they seem.

- **With a shell that runs it without asking**, if `../../scripts/arousal.py` exists (from this skill's folder): pipe it the user's messages so far through a bash heredoc, oldest first, separated by lines that are exactly `---`, with `python3` (`python` on Windows). Never write the messages to a file. Use the `level` of each turn and the `gate`. If running it would show the user a permission prompt (that would put their messages on screen and make the check visible), if a run was denied or failed, or if the only shell is PowerShell (it can mangle non-English text), count by hand for the rest of the conversation.
- **By hand**, count the signs each user message shows; when unsure, count it:
  1. longer than their message before it
  2. an absolute: always, never, everyone, nobody, hamesha, kabhi nahi, sab log
  3. an accusation at someone: "you always", "she never", "tu hamesha"
  4. a whole word in capitals (not an acronym), or a run like `!!`, `??`, `?!`
  5. the same grievance as an earlier message, again
  6. swearing at or about someone
  7. urgency or wanting it to hurt: "right now", "tonight", "i want him to feel it"

  0 signs: calm. 1-2: settling. 3 or more: flooded.
- **The gate** is `clear` only when the user's last two messages are both settling or calm; otherwise it is `hold`. One message on its own never clears it, unless this skill says otherwise.
- When the script and your count disagree, use the stricter reading.
