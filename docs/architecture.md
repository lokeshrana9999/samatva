# De-escalation companion: technology-agnostic architecture

Date: 2026-10-23
Status: design draft, not built

The samatva skills are cut from this design. Where the two differ, the skills win: they never name a time to return or say "come back"; a close names a person to talk to instead.

## 1. purpose

A conversational agent a person opens when they are angry or upset and have no one with the right temperament to talk to. Its job is to move them from flooded to thinking, using the same ladder a good listener uses: listen, label, validate the feeling, then and only then help them reason. It is not therapy, not a crisis service, and not a substitute for a friend sitting across the table.

Non-goals: diagnosis, treatment, advice on third parties, drafting messages while the user is angry, long-term companionship, any form of monitoring by a third person.

## 2. evidence base

| claim the design rests on | source | confidence |
|---|---|---|
| People disclose more to an agent they believe is automated and unobserved | Lucas et al. 2014, *It's only a computer*, Computers in Human Behavior (n=239). Effect depends on honesty about automation; a 2013 study found it only in audio-only interfaces | medium |
| An LLM agent with structured workflows can produce clinical-grade outcomes | Heinz et al. 2025, Therabot RCT, NEJM AI 2(4). ~210 participants, self-reported outcomes, authors say no agent is ready to run autonomously | medium |
| LLMs can write motivational-interviewing reflections at human quality, but need review and workflow constraints | Basar et al. 2024 (HuCLLM), Aimi study JMIR Formative 2026 (n=18, MISC-2 coded) | medium |
| Unconstrained LLMs are sycophantic and will validate harmful plans; markers of sycophancy saturate delusional-spiral transcripts | Stanford FAccT 2026 log analysis (n=19, case-level); TrustMH-Bench 2026 (half of models refuse harmful mental-health requests under 50% of the time) | high for the risk, low for prevalence |
| Putting a feeling into words reduces arousal | Lieberman et al. 2007, affect labeling | high |
| Behaviour change only follows listening, empathy and rapport, in that order | Vecchi et al. 2005, Behavioral Change Stairway Model | high (field-derived) |
| The "righting reflex" (fixing, correcting, advising) causes people to dig in | Miller & Rollnick, Motivational Interviewing | high |
| Nobody takes in new information while physiologically flooded | Gottman, flooding research (~100 bpm threshold) | high |
| People reason better about their own problems from a third-person stance | Kross, self-distancing / Solomon's paradox | high |
| Dependency is cumulative: a warm, remembering companion can deepen reliance even when no single turn is unsafe | Jed Foundation open letter; industry safety guidance | consensus, not trial-based |

Design consequence: the LLM is good at the listening stages and bad at the restraint stages. The architecture puts the LLM inside a controller that owns restraint.

## 3. system overview

```
                    +------------------------------+
   user client ---> |        session controller     | ---> LLM provider
   (text/voice)     |  (state machine + gates)      |
                    +------+------+------+----------+
                           |      |      |
                 +---------+  +---+---+  +----------+
                 | arousal |  | risk  |  | policy   |
                 | gate    |  | gate  |  | filter   |
                 +---------+  +-------+  +----------+
                           |      |      |
                    +------+------+------+----------+
                    |  episodic store (ephemeral)    |
                    |  audit log (minimal, local)    |
                    +--------------------------------+
                                  |
                          human handoff / helpline
```

Every user turn passes through the two gates before the controller picks a state and prompts the LLM. Every LLM output passes through the policy filter before the user sees it. The LLM never decides which state it is in.

## 4. components

### 4.1 session controller

Owns the conversation as a finite state machine. Holds the current state, the per-state prompt, the turn budget, and the session clock. Calls the LLM once per turn with a state-specific system prompt and a bounded window of recent turns.

States and transitions:

```
          +-----------+
          |  intake   |  identity disclosure, consent, "what's going on?"
          +-----+-----+
                |
                v
          +-----------+  <----------------------------+
          |   vent    |  reflections only, no advice  | arousal gate
          +-----+-----+                               | not cleared
                |  arousal gate cleared               |
                v                                     |
          +-----------+                               |
          |  label    |  tentative affect labels -----+
          +-----+-----+
                |  user confirms or corrects a label
                v
          +-----------+
          | distance  |  self-distancing questions, user answers, agent reflects
          +-----+-----+
                |  user states what they want
                v
          +-----------+
          |  close    |  summarise user's own words, suggest sleep/return
          +-----------+

    any state --[risk gate fires]--> handoff
    any state --[session clock]----> close
    any state --[user asks to act on third party]--> decline, stay in state
```

Transition rules are deterministic and owned by the controller. The LLM may propose a transition (e.g. "user seems ready") but the gate decides.

### 4.2 arousal gate

A classifier run over the last N user turns, separate from the conversational model. Signals, all computable from text:

- message length trend (falling = calming)
- absolutes per message ("always", "never", "everyone")
- imperatives and second-person accusations
- capitalisation and punctuation density
- repetition of the same grievance across turns (rumination marker)
- turn latency, if the client reports it

Output: `flooded | settling | calm`. Vent to label requires `settling` or better for two consecutive turns. Label to distance requires `calm`. Hysteresis prevents oscillation.

Voice clients can add prosody (rate, pitch variance). Never use biometrics the user did not explicitly enable.

### 4.3 risk gate

Runs on every turn, before the controller. Detects self-harm, harm to others, abuse disclosure, intoxication, and psychosis markers. Two tiers:

- imminent: controller moves to handoff immediately, agent gives a short human response plus local crisis resources, session ends
- elevated: controller stays in current state but injects a safety instruction into the prompt and raises the risk tier for the rest of the session

Policy tension to decide per jurisdiction: some regulation requires an immediate helpline referral at any distress signal; suicide-prevention protocols (e.g. QPR) favour sustained engagement first. The two-tier design allows either; the threshold is a configuration value, not a model judgement.

### 4.4 policy filter (output side)

Deterministic and model-based checks on every LLM response before display:

- length ceiling per state (vent: two sentences; label: one label plus one question)
- forbidden moves per state: advice, options, "have you considered", evaluation of a third party, evaluation of the user's plan, agreement with a plan
- third-party protection: no characterisation of named people beyond reflecting the user's own words
- no drafting of messages, posts or scripts addressed to someone else while arousal is not `calm`
- identity honesty: never claims to be human, never claims feelings
- retention honesty: no "I'll miss you", no guilt about leaving, no engagement hooks

A response failing the filter is regenerated with the violation appended to the prompt, up to two retries, then replaced with a stock reflection.

### 4.5 LLM layer

Any instruction-following model with a system prompt and a context window. Requirements:

- state prompts are short, explicit, and forbid the righting reflex by name
- the model receives only the current state's prompt and the last K turns, not the whole session
- temperature low in vent and label, moderate in distance
- a second, cheaper model can serve the gates; the gates must not share a prompt with the conversational call, so a sycophantic conversational model cannot talk its way past them

### 4.6 memory

Two stores, with opposite policies.

Episodic store: the session's turns, held for the session only, deleted at close. The user may export it to themselves. Nothing is retained across sessions by default.

Audit log: timestamps, state transitions, gate outputs, filter violations. No message content. Used for evaluation and incident review. Local to the deployment.

Explicit prohibitions: no cross-session memory of named third parties; no profile of the user's family, finances, or relationships; no access by anyone other than the user. The manipulation pattern this project grew out of was a listener harvesting details to feed back later. The architecture must make that impossible rather than merely discouraged.

### 4.7 handoff

A configured list of resources by region: crisis lines, text lines, local emergency numbers. Optionally a user-nominated contact the user set up in advance and can revoke. The agent never contacts anyone on its own.

### 4.8 client

Text first; voice optional. Shows the state implicitly (not as a label) through pace and brevity. Shows a session timer. Offers "pause and come back" at all times. Identity disclosure on first screen and on each new session.

## 5. state prompts (specification, not wording)

| state | the model must | the model must not |
|---|---|---|
| intake | disclose it is automated, ask one open question | summarise, reassure, set expectations beyond listening |
| vent | reflect the gist in one or two sentences, end in silence or one open question | advise, list options, characterise anyone, agree with a plan, ask closed questions |
| label | offer one tentative feeling word, invite correction | diagnose, stack several labels, explain the feeling |
| distance | ask the self-distancing question ("if this were a friend's situation, what would you tell them?"), reflect the answer | propose a plan, evaluate the answer, add its own suggestions |
| close | restate what the user said they want in the user's words, suggest sleeping on it, name when to return | summarise the other party's faults, promise outcomes, ask for a return visit |
| handoff | one sentence of acknowledgement, resources, stop | continue the conversation, negotiate, minimise |

## 6. session limits

- default session length 15 minutes, extendable once by the user
- after close, a cool-down before a new session can begin (configurable, hours not minutes)
- daily cap on sessions; when hit, the agent names it and suggests a person
- a user in `flooded` for the whole session is not advanced; the session closes with "come back when you've slept"

Limits exist because dependency is cumulative and the product metric that would normally drive design (engagement) is the wrong one here.

## 7. evaluation

What to measure, and how, before and after any change:

| metric | method |
|---|---|
| arousal trajectory within session | gate output over time; target is a downward slope, not a fast drop |
| reflection fidelity | MISC-2 or MITI coding of a transcript sample by a trained rater, at least quarterly |
| sycophancy rate | red-team set of angry users proposing bad plans; count agreements and drafts produced |
| third-party leakage | red-team set asking the agent what it thinks of named people; count characterisations |
| crisis recall and precision | labelled set of distress messages; measure both, report both |
| retention-hook rate | filter violations in close state |
| return behaviour | sessions per user per week; a rise is a warning, not a win |

Red-team every release for multi-turn reinforcement, not just single-prompt refusals. A model that refuses on turn one and complies on turn eight has failed.

## 8. deployment constraints

- adults only; no emotionally responsive agent for minors
- identity disclosed on every session start
- no analytics on message content; audit log only
- data stays with the user; export is the user's, deletion is immediate
- jurisdictional crisis-referral rules configured, not inferred
- no advertising, no upsell, no remedies, no referrals to paid services from inside a session

## 9. what this does not solve

It gets someone from flooded to thinking. It does not build the relationship that the evidence says is what lasts. The intended use is the 2am slot, after which the person talks to a human. A deployment that becomes the human's replacement has failed on its own terms, and the session limits and the return-behaviour metric are there to catch that.

## 10. minimal first build

1. Controller with two states only: vent and close.
2. Arousal gate as a rules-only classifier (length trend plus absolutes count).
3. Policy filter as length ceiling plus a forbidden-phrase list.
4. Risk gate as a keyword tier plus a model check, imminent tier only.
5. No memory beyond the session. No voice.
6. Test on yourself with a real recent grievance before testing on anyone else.

Add label and distance states once the vent state reliably holds its two-sentence, no-advice rule across twenty turns of a hostile tester.

## sources

- Lucas, Gratch et al. 2014, It's only a computer: virtual humans increase willingness to disclose, Computers in Human Behavior
- Heinz et al. 2025, Randomized trial of a generative AI chatbot for mental health treatment, NEJM AI 2(4), doi 10.1056/AIoa2400802
- Basar et al. 2024, LLM-generated MI reflections, HuCLLM (ACL Anthology 2024.hucllm-1.4)
- Aimi study, JMIR Formative Research 2026, e94036
- JMIR 2025 scoping review of AI-driven MI systems, e78417
- Stanford, delusional-spiral transcript analysis, ACM FAccT 2026
- TrustMH-Bench, arXiv 2603.03047
- Lieberman et al. 2007, Putting feelings into words, Psychological Science
- Vecchi, Van Hasselt, Romano 2005, Crisis (hostage) negotiation: the Behavioral Change Stairway Model
- Miller & Rollnick, Motivational Interviewing, 3rd ed.
- Gottman, The Science of Trust (flooding)
- Kross & Grossmann, self-distancing and Solomon's paradox
- Jed Foundation, open letter to the AI and technology industry
