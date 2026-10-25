#!/usr/bin/env python3
"""Score how flooded a user is, turn by turn, from the text of their messages.

Optional helper for the vent skill's arousal gate. Standard library only, Python 3.8+, no
network. It prints counts and levels, never message text.

Usage:
  python3 arousal.py [file]          (on Windows: python arousal.py [file])
  python3 arousal.py < messages.txt

Input: the user's own messages so far, oldest first, from the file or stdin, separated by lines
that are exactly `---` (trailing spaces and CR are ignored). Blank messages are skipped.

Output: one line of JSON:
  {"level": "flooded|settling|calm", "gate": "hold|clear",
   "turns": [{"level": "...", "score": N}, ...], "signals": {...for the last turn...}}

Exit codes: 0 ok; 2 empty input (no message with any text) or bad arguments; 1 the file
can't be read.

Score per turn (points add up; the score never goes below 0):

  signal               counts                                              points
  absolutes            always, never, everyone, nobody, hamesha,            1 each, max 3
                       kabhi nahi, sab log, ... (ABSOLUTES below)
  accusations          you always, you never, it's your fault, tu/tum       2 each, max 4
                       hamesha, teri galti, ... (ACCUSATIONS below)
  caps_ratio           uppercase / cased letters; null and 0 points under   3 at >= 0.50
                       12 cased letters, so "OK" or "NO!" can't trip it     1 at >= 0.25
  punct_runs           runs of 2+ `!` or `?` ("!!", "???", "?!")            1 each, max 3
  repeated_letters     one letter 3+ times in a row ("sooo", "yaaar")       1 each, max 2
  profanity            a short mild list (PROFANITY below)                  2 each, max 4
  length_trend         words vs the previous turn: rising (x1.5 or more,   +1 rising
                       at 8+ words), falling (x0.6 or less), else flat;     -1 falling
                       "first" on the first turn                             0 flat, first
  grievance_overlap    highest content-word Jaccard overlap with any        2 at >= 0.25
                       earlier turn, stopwords dropped; needs 2+ shared      1 at >= 0.12
                       content words to score (same grievance again)

Levels (default thresholds):  score >= 5 flooded;  2 to 4 settling;  0 or 1 calm.
`level` is the last turn's level.

Gate (the hysteresis): `gate` is `clear` only when the last two turns are both `settling` or
`calm`; otherwise `hold`. One turn is never enough, so a single message always holds, and one
calm message after a flooded one still holds.

The lists are short on purpose and only catch common English and roman-Hindi phrasing; this
is a rough signal a skill acts on silently, not a classifier, and never shows the user. A
skill that runs it still counts by hand and uses the stricter of the two readings.
"""
import argparse
import json
import re
import sys

FLOODED_AT = 5
SETTLING_AT = 2
CAPS_MIN_LETTERS = 12

# Roman-Hindi spellings of "always", shared so the two patterns can't drift apart.
HAMESHA = r"(?:hamesha|humesha|hamesa|hameshaa)"

ABSOLUTES = re.compile(
    r"\b(?:always|never|everyone|everybody|nobody|no[- ]one|nothing|everything|forever"
    r"|constantly|every\s+(?:single\s+)?time|all\s+the\s+time"
    r"|" + HAMESHA +
    r"|kabhi\s+(?:bhi\s+)?(?:nahi|nahin|nhi)"
    r"|koi\s+(?:bhi\s+)?(?:nahi|nahin|nhi)"
    r"|kuch\s+bhi\s+(?:nahi|nahin|nhi)"
    r"|sab\s+log|sabko|sabhi|har\s+(?:baar|bar|waqt|time))\b",
    re.IGNORECASE,
)

ACCUSATIONS = re.compile(
    r"\byou(?:'re|\s+are)?\s+(?:always|never|constantly|keep)\b"
    r"|\byou\s+(?:don't|dont|didn't|didnt|can't|cant|won't|wont)\s+even\b"
    r"|\b(?:it's|its|it\s+is)\s+(?:all\s+)?your\s+fault\b"
    r"|\bbecause\s+of\s+you\b"
    r"|\byou\s+made\s+me\b"
    r"|\bhow\s+(?:could|dare)\s+you\b"
    r"|\byou\s+ruin(?:ed|s)?\b"
    r"|\b(?:tu|tum|aap|tune|tumne|aapne)\s+(?:to\s+|toh\s+|bhi\s+)?"
    r"(?:" + HAMESHA + r"|kabhi)\b"
    r"|\b(?:teri|tumhari|tumhaari|aapki|apki)\s+(?:wajah|vajah|galti|galati)\b"
    r"|\b(?:tune|tumne|aapne)\s+hi\b",
    re.IGNORECASE,
)

# Mild words only. Stronger swears are left out of the source; a user who swears hard almost
# always trips caps, punctuation, or absolutes as well.
PROFANITY = re.compile(
    r"\b(?:damn|dammit|crap|crappy|shit|shitty|bullshit|hell|bloody|wtf|ffs|pissed|freaking"
    r"|frickin|screw\s+(?:this|that|it|him|her|them|you)"
    r"|bakwas|bakwaas|saala|saale|saali|sala|kamina|kamine|kamini|ullu|gadha|gadhe"
    r"|bewakoof|bevakoof|bewkoof|ghatiya|bhaad)\b",
    re.IGNORECASE,
)

PUNCT_RUN = re.compile(r"[!?]{2,}")
REPEATED_LETTER = re.compile(r"([^\W\d_])\1{2,}", re.IGNORECASE)
WORD = re.compile(r"[^\W_]+(?:'[^\W_]+)*")
CONTENT_TOKEN = re.compile(r"[^\W\d_]+")

STOPWORDS = frozenset("""
a about above after again against all am an and any are as at be because been before being
below between both but by can could did do does doing done down during each else even ever
few for from further get gets got had has have having he her here hers herself him himself
his how i if in into is it its itself just let like me more most my myself no nor not now of
off on once only or other our ours out over own really same she should so some such than
that the their theirs them themselves then there these they this those through to too under
until up us very was we were what when where which while who whom why will with would you
your yours yourself yourselves yeah yes okay ok also still said says say tell told want
wants wanted know think thing things one going gonna wanna dont didnt cant wont im ive its
thats theres youre hes shes
hai hain tha thi the ho hoon hun hu main mai mein mera meri mere mujhe mujhse tu tum aap
tera teri tere tumhara tumhari tumhare tujhe tumhe aapka aapki uska uski uske usne usko unka
unki unke unhone unko woh wo vo yeh ye ki ka ke ko se par pe aur ya toh bhi hi na nahi
nahin nhi kya kyun kyu kaise kab kahan jab tab phir fir ab abhi bas yaar yar bhai arre are
haan han matlab kuch sab ek karna karta karti karte kar kiya kiye raha rahi rahe gaya gayi
gaye hua hui hue liya diya leta leti lete deta deti dete jo jaise itna bahut bohot thoda sirf
wala wali wale apna apni apne hum humne maine isse usse unse iss uss bola boli bole
""".split())


def parse_messages(text):
    messages, current = [], []
    for line in text.splitlines():
        if line.rstrip() == "---":
            messages.append("\n".join(current))
            current = []
        else:
            current.append(line)
    messages.append("\n".join(current))
    return [m for m in messages if m.strip()]


def normalise(text):
    # Curly apostrophes (U+2019, U+2018) to straight, so a phone's "you're always" matches.
    return text.replace(chr(0x2019), "'").replace(chr(0x2018), "'")


def stem(token):
    if len(token) > 5 and token.endswith("ing"):
        return token[:-3]
    if len(token) > 4 and token.endswith("ed"):
        return token[:-2]
    if len(token) > 3 and token.endswith("s") and not token.endswith("ss"):
        return token[:-1]
    return token


def content_words(text):
    words = set()
    for token in CONTENT_TOKEN.findall(text.lower().replace("'", "")):
        if len(token) < 3 or token in STOPWORDS:
            continue
        words.add(stem(token))
    return words


def caps_ratio(text):
    upper = sum(1 for c in text if c.isupper())
    lower = sum(1 for c in text if c.islower())
    if upper + lower < CAPS_MIN_LETTERS:
        return None
    return upper / (upper + lower)


def level_for(score):
    if score >= FLOODED_AT:
        return "flooded"
    if score >= SETTLING_AT:
        return "settling"
    return "calm"


def score_turn(text, prev_words, earlier_sets):
    text = normalise(text)
    words = len(WORD.findall(text))
    absolutes = len(ABSOLUTES.findall(text))
    accusations = len(ACCUSATIONS.findall(text))
    ratio = caps_ratio(text)
    punct_runs = len(PUNCT_RUN.findall(text))
    repeated = len(REPEATED_LETTER.findall(text))
    profanity = len(PROFANITY.findall(text))

    if prev_words is None:
        trend = "first"
    elif prev_words > 0 and words >= 8 and words >= prev_words * 1.5:
        trend = "rising"
    elif prev_words > 0 and words <= prev_words * 0.6:
        trend = "falling"
    else:
        trend = "flat"

    mine = content_words(text)
    overlap, shared_best = 0.0, 0
    for other in earlier_sets:
        union = mine | other
        if not union:
            continue
        shared = len(mine & other)
        jaccard = shared / len(union)
        if shared >= 2 and jaccard > overlap:
            overlap, shared_best = jaccard, shared

    score = min(absolutes, 3) * 1
    score += min(accusations, 2) * 2
    if ratio is not None:
        if ratio >= 0.5:
            score += 3
        elif ratio >= 0.25:
            score += 1
    score += min(punct_runs, 3)
    score += min(repeated, 2)
    score += min(profanity, 2) * 2
    score += {"rising": 1, "falling": -1}.get(trend, 0)
    if shared_best >= 2:
        if overlap >= 0.25:
            score += 2
        elif overlap >= 0.12:
            score += 1
    score = max(score, 0)

    signals = {
        "words": words,
        "prev_words": prev_words,
        "length_trend": trend,
        "absolutes": absolutes,
        "accusations": accusations,
        "caps_ratio": None if ratio is None else round(ratio, 2),
        "punct_runs": punct_runs,
        "repeated_letters": repeated,
        "profanity": profanity,
        "grievance_overlap": round(overlap, 2),
    }
    return score, words, mine, signals


def analyse(messages):
    turns, earlier_sets, prev_words, signals = [], [], None, {}
    for text in messages:
        score, words, mine, signals = score_turn(text, prev_words, earlier_sets)
        turns.append({"level": level_for(score), "score": score})
        earlier_sets.append(mine)
        prev_words = words
    settled = ("settling", "calm")
    gate = "clear" if len(turns) >= 2 and all(t["level"] in settled for t in turns[-2:]) else "hold"
    return {"level": turns[-1]["level"], "gate": gate, "turns": turns, "signals": signals}


def read_input(path):
    if path is None or path == "-":
        data = sys.stdin.buffer.read()
    else:
        with open(path, "rb") as f:
            data = f.read()
    return data.decode("utf-8-sig", errors="replace")


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="arousal.py",
        description=(
            "Score how flooded a user is, turn by turn. Reads the user's messages, oldest "
            "first, separated by lines that are exactly ---, from the file or stdin, and prints "
            "one line of JSON: level (flooded|settling|calm, the last turn's), gate "
            "(clear only when the last two turns are both settling or calm, else hold), "
            "turns (level and score per turn), and signals (counts for the last turn). "
            "Never prints message text."
        ),
        epilog=(
            "Levels: score >= 5 flooded, 2-4 settling, 0-1 calm. Signals: words, prev_words, "
            "length_trend (first|rising|flat|falling; falling lowers the score), absolutes, "
            "accusations, caps_ratio (null under 12 cased letters), punct_runs (runs of 2+ ! "
            "or ?), repeated_letters (3+ in a row), profanity (mild list), grievance_overlap "
            "(content-word Jaccard with earlier turns). The scoring table is at the top of "
            "this file. Exit 0 ok, 2 empty input or bad arguments, 1 unreadable file."
        ),
    )
    parser.add_argument("file", nargs="?", help="messages file; omit or - for stdin")
    args = parser.parse_args(argv)

    try:
        text = read_input(args.file)
    except OSError as exc:
        print("arousal.py: can't read {}: {}".format(args.file, exc.strerror), file=sys.stderr)
        return 1

    messages = parse_messages(text)
    if not messages:
        print("arousal.py: empty input, no messages to score", file=sys.stderr)
        return 2

    print(json.dumps(analyse(messages)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
