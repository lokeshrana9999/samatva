# Sources: vent

Provenance for the rules in `skills/vent/` (SKILL.md and references/overlay-example.md). Kept outside the skill folder so it never loads into context. Full citations are in `docs/architecture.md`, sections 2 and "sources"; the vent state is specified in its sections 4.1, 4.2, 4.4 and 5.

## SKILL.md

- Reflections only, and the righting reflex forbidden by name (advice, fixing, correcting, reassuring): Miller & Rollnick, *Motivational Interviewing*, 3rd ed. Fixing and correcting make people argue for the position being corrected. Open questions over closed ones, and no "why" questions (they invite self-justification), are standard MI practice from the same book.
- Listening before any influence, in that order: Vecchi, Van Hasselt & Romano 2005, the Behavioral Change Stairway Model (crisis and hostage negotiation). Field-derived, not trial-based.
- Hold until calmer, and no advice while worked up: Gottman, *The Science of Trust* (flooding: nobody takes in new information while physiologically flooded).
- The gate's signals (length trend, absolutes, accusations, caps and punctuation runs, repeated grievance), the flooded/settling/calm levels, and two consecutive settled turns before moving on (hysteresis): docs/architecture.md 4.2. The check itself is the shared block `skills/_shared/arousal-check.md`, which adds swearing and urgency as signs and takes the stricter reading when the script and the count disagree. This is a rules-only design heuristic, not a validated instrument; the by-hand thresholds (0 calm, 1-2 settling, 3+ flooded) are a design choice.
- No new feeling words in vent; naming a feeling waits for think-it-through: Lieberman et al. 2007, *Putting feelings into words*, Psychological Science (affect labelling reduces arousal). The evidence supports labelling; placing it after the gate, as one tentative label the user can correct, follows the state order in docs/architecture.md 4.1 and 5, so a wrong label isn't pressed on someone mid-flood.
- No agreement with a plan or with the user's side, no verdicts on the feeling: Stanford delusional-spiral transcript analysis, ACM FAccT 2026 (sycophancy markers saturate harmful-spiral transcripts); TrustMH-Bench 2026, arXiv 2603.03047 (models often comply with harmful mental-health requests).
- No label, diagnosis, motive, or evaluation for any third party, even when asked: docs/architecture.md 4.4 (third-party protection) and 4.6 (the manipulation pattern this project grew out of: a listener harvesting details to feed back later); README principle 2.
- Short, constrained reflections rather than free-form empathy: Basar et al. 2024, LLM-generated MI reflections, HuCLLM; the Aimi study, JMIR Formative Research 2026 (LLMs reflect at human quality but need review and workflow constraints).
- Two-sentence ceiling and the forbidden-move list: docs/architecture.md 4.4 (policy filter, vent: two sentences). The 40-word cap and the tighten-only overlay are design choices that carry the filter into prompt text, since a skill has no controller.
- Never showing the gate; pace as the only visible sign: docs/architecture.md 4.8 (the client shows state implicitly, through pace and brevity, never as a label).
- No emoji, humour, or swearing in a vent reply whatever the profile allows, and no answering word (haan, ok) after a yes/no question: README principle 7 (restraint beats voice); voice-setup/references/mirroring-rules.md 6 (if the voice and the content can't both fit, keep the content).
- Offering cool-down-close after 15 user turns (default) since they first brought it up, counted across every samatva skill (the key and count think-it-through and cool-down-close share; samatva build decision, 2026-10-24), and handing over without asking at twice that: Jed Foundation, open letter to the AI and technology industry (dependency is cumulative); docs/architecture.md 6 (session limits; a session that never settles still closes). The re-offer every 5 turns is a design choice.
- Exits and their order (risk first, think-it-through only after the gate, drafting handed to before-you-send): docs/architecture.md 4.1 and 4.3; the README skills table (router row) tie-break.
- Honest identity and no retention hooks (shared boundaries block): Lucas, Gratch et al. 2014, *It's only a computer*, Computers in Human Behavior (disclosure depends on honesty about automation); Jed Foundation open letter.

## references/overlay-example.md

- Tighten-only settings: docs/voice.md and CONTRIBUTING.md (voice and behaviour live in separate files, so editing style can never loosen restraint); docs/architecture.md 4.5 (a sycophantic conversational model must not be able to talk its way past the gates).
- Both files read, the stricter value of each key winning, in place of first match: samatva build decision, 2026-10-24. Under first match, a project file the person didn't write (one committed to a cloned repo) hid their home file and loosened what they chose.

## Specifics removed from the skill (as of 2026-10-23)

- The ~100 bpm flooding threshold (Gottman): a skill sees only text, so the gate uses text signals.
- Turn latency and voice prosody as arousal signals (docs/architecture.md 4.2): no host reports them to a skill.
- Regenerating a reply that fails the filter, up to two retries, then a stock reflection (docs/architecture.md 4.4): there is no controller; the skill's before-sending checklist stands in for it.
- Low temperature in vent (docs/architecture.md 4.5): a skill can't set it.
- Session clock in minutes (docs/architecture.md 6): replaced by a count of user turns, which a model can track.
