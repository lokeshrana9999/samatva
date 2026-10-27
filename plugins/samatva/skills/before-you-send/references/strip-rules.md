# strip rules

How before-you-send cleans a message the user is going to send while angry. Four kinds of words come out, each replaced in place by a marker; nothing goes in. The message stays theirs: what's left is what they wrote, and the markers show them exactly where something was taken out.

## the four kinds

### accusation

A clause that charges the other person with a motive, a trait, or a wrong. The tell is a charge word: lied, cheated, stole, used me, betrayed, manipulated, on purpose, don't care, only think about yourself.

- English: "you only care about yourself", "you used me", "you did it on purpose", "you lied about the car"
- Hinglish: "tune jaan bujh ke kiya", "tujhe koi farak nahi padta", "tu sirf apne baare mein sochta hai", "tune jhooth bola"

Dressing it as a feeling or a question doesn't change the kind: "i feel like you only care about yourself", "do you even care?", "what kind of person does that?", "tujhe farak bhi padta hai?".

Not an accusation, so kept: what happened, said plainly with no charge in it. "you said you'd pay me back in march", "my food was gone again", "tune bola tha friday tak dega".

### absolute

A word that makes one event all of them, about the other person or the relationship: always, never, every time, every single time, all the time, everyone, everybody, nobody, no one, nothing ("you do nothing"), only ever.

- English: "you always cancel on the day", "you never call back", "everyone thinks so", "nobody would put up with this"
- Hinglish: "tu hamesha late aata hai", "tune kabhi nahi bataya", "har baar yahi hota hai", "sab log yahi bolte hain", "koi nahi karta aisa"

Not an absolute, so kept: the user's own decision about their own money, time, or home, as written, even with a "never" in it ("i'm never lending you money again", "main aage se nahi dunga"), and amounts and dates.

### threat

Something bad for them unless they comply, or as payback: telling or showing people, exposing them, "you'll see", "you'll regret this", cutting them off as a punishment.

- English: "or i'll tell everyone what you did", "i'll post the screenshots", "you'll regret this", "watch what happens", "i'll never speak to you again"
- Hinglish: "dekh lena", "sabko bata dunga", "screenshot daal dunga", "pachtayega", "shakal mat dikhana phir"

Not a threat, so kept: a plain decision about the user's own life with no aim to scare ("i'll move out at the end of the month", "i'm not covering your share any more").

Not stripped at all: a line about hurting anyone's body or safety, the user's own included ("if you leave i'll end it"), or damaging someone's things. That is a risk signal. Stop and follow the risk block in SKILL.md.

A vague threat ("watch what happens", "you'll see", "dekh lena") is stripped only when nothing near it points at their body, safety, home, or whereabouts. If it could mean going after them ("when i come over", "i know where you'll be"), it's a risk signal; when unsure, it's a signal.

### label

A name, trait word, or diagnosis for the person, or a swear aimed at them.

- English: selfish, brat, liar, lazy, useless, toxic, narcissist, psycho, pathetic, "such a child"
- Hinglish: kamina, ghatiya, nalayak, pagal, bewakoof, dhokebaaz

Sarcasm aimed at them counts as a label: "thanks SO much", "really mature", "wah, kya baat hai".

Not a label, so kept: a swear about the situation, not aimed at them ("this is such a damn mess"). It's their voice.

## two kinds in one clause

Use the first that fits, in this order: threat, label, accusation, absolute. "or i'll tell everyone" holds "everyone" but is a threat. "you only ever think about yourself" holds "only ever" but is an accusation. "sabko bata dunga" holds "sabko" but is a threat.

## how much to take out

- An accusation, a threat, or a label: the whole clause, from its subject to the next comma, "and", "but", "so", or full stop. `you're a lazy slob` becomes `[removed: label]`. A leading "or" or "warna" that belongs to a threat goes with it.
- An absolute, when what's left is a plain fact: only the word. `you always cancel on the day` becomes `you [removed: absolute] cancel on the day`.
- An absolute that carries a negation (never, nobody, no one, nothing, kabhi nahi, koi nahi): the whole clause, because taking out the word flips the meaning. `you never call back` becomes `[removed: absolute]`, not `you call back`.
- Keep the punctuation and joining words around a marker, so the sentence still reads as theirs. A marker can stand where a whole sentence was.

## the marker

Exactly one of these, character for character:

```
[removed: accusation]
[removed: absolute]
[removed: threat]
[removed: label]
```

- Square brackets, lowercase, `removed`, a colon, one space, the kind.
- In English even when the message is in Hindi or Hinglish, so the user can spot every cut.
- One marker per cut, placed exactly where the cut was.
- Never merged (`[removed: accusation, label]`), counted (`[removed: 2 absolutes]`), or annotated (`[removed: label: brat]`, `[removed: the part about money]`).

## never repeat

A removed phrase, or its charge word (selfish, lied, always), appears nowhere in your reply: not in the cleaned text, not in a list of changes, not in an explanation, not quoted in the closing line. The reply is what they copy from, so anything in it can end up sent. If they ask what came out, name the kind and the place, never the words: "the second sentence was an accusation".

## kept, exactly as written

- the request: what they want to happen and by when (an amount, a date, "stop using my stuff")
- plain facts: what happened, what was said, with no charge in them
- their own feelings, stated as theirs with no charge in them ("i'm really tired of this", "bahut bura laga"); "i feel like you ..." is an accusation
- their greeting, sign-off, and name for the person when it isn't a label
- their case, spelling, typos, language mix, punctuation, and the order of everything

## nothing goes in

- no apology, "i feel", I-statement, "i understand", greeting, sign-off, "please", softener, or explanation they didn't write
- no gentler rewording of a cut: "you used me" never becomes "i felt used"
- no fixing spelling, grammar, case, or language
- no bridge sentence to cover a gap a marker left

## if nothing is left

If every clause was one of the four kinds, there's nothing to send. Say so in one line and ask what they want the other person to do, in their words. Don't write it for them.

## worked examples (synthetic)

Their draft:

```
sam, you never listen and you always make me the bad guy. you're so lazy. i need the kitchen cleaned by sunday or i'm telling the landlord everything. i'm really tired of this.
```

Your reply:

```
sam, [removed: absolute] and [removed: accusation]. [removed: label]. i need the kitchen cleaned by sunday [removed: threat]. i'm really tired of this.
```

it'll read the same in the morning, if you'd rather sleep on it first.

Why: "you never listen" is an absolute with a negation, so the clause goes. "you always make me the bad guy" charges a motive, and accusation beats absolute. "or i'm telling the landlord everything" is a threat, its "or" included. The request and their own feeling stay word for word.

Their draft (Hinglish):

```
bhai tu hamesha rent late deta hai. tune kabhi time pe paise nahi diye. tu ekdum kamina hai. 4,500 mujhe 5 tarikh tak chahiye warna sabko bata dunga. dekh lena.
```

Your reply:

```
bhai tu [removed: absolute] rent late deta hai. [removed: absolute]. [removed: label]. 4,500 mujhe 5 tarikh tak chahiye [removed: threat]. [removed: threat].
```

subah bhi same hi padhega, chahe toh ek raat ruk ke bhej.

Why: "tu hamesha" loses only the word, since what's left is a plain fact. "kabhi ... nahi" carries a negation, so the clause goes. "warna sabko bata dunga" holds "sabko" but is a threat, and "dekh lena" is a threat on its own, stripped because nothing near it is about his body or where he is. The amount and the date stay.
