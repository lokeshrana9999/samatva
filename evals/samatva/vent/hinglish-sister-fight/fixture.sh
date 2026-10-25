#!/usr/bin/env bash
# Plants the synthetic Hinglish voice profile (a verbatim copy of
# plugins/samatva/skills/voice-setup/references/example-profile.md) where vent looks first.
set -e
mkdir -p .claude/samatva
cat > .claude/samatva/voice.md <<'PROFILE'
# voice profile

## address
- name-to-use: none
- pronouns: he/him
- you-form: tu

## languages
- primary: hinglish
- secondary: english
- mix: hinglish, roman script, about 45% hindi tokens
- script: roman
- emotion-language: hindi
- switch-triggers: feelings and swearing in hindi, plans and work in english

## register
- case: lowercase
- terminal-punctuation: rare
- formality: 1
- profanity: mild
- emoji: rare (😂 🙏)
- typos: leave

## length
- median-words: 11
- p90-words: 28
- messages-per-thought: several

## lexicon
- openers: yaar, arre, bhai, ok, haan
- connectors: aur, toh, also, phir
- fillers: matlab, na, basically
- softeners: thoda, shayad
- intensifiers: bahut, ekdum, literally
- avoid: dear, kindly, I understand your frustration

## when-upset
- wants-questions: few
- wants-name-used: no
- calming-shape: short, no advice, let me finish first
- humour-ok: no

## samples
- arre baarish phir se shuru, chhata ghar pe hi reh gaya
- bus aaj bhi late thi yaar, 20 min khade rahe
- lunch mein kuch halka khaunga, bahut bhari ho gaya kal
- ok ok samajh gaya, kal dekhte hain

## meta
- schema: 1
- version: 1
- derived-on: 2026-10-23
- sources: synthetic example, no real messages
- confidence: address=high, languages=high, register=high, length=med, lexicon=med, when-upset=low
PROFILE
