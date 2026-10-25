"""Tests for plugins/samatva/scripts/arousal.py. Standard library only.

Run from the repo root: python3 -m unittest discover -s scripts -p "test_*.py"

The transcript tests replay each eval transcript's user turns and check them against the
readings its notes record ("`scripts/arousal.py` on the five user turns ..."), so a change to
the scoring that moves a recorded reading fails here instead of leaving the notes stale.
"""
import importlib.util
import io
import re
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("arousal", ROOT / "plugins/samatva/scripts/arousal.py")
arousal = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(arousal)

TRANSCRIPTS = ROOT / "evals/samatva/transcripts"
RECORDED = re.compile(r"^`scripts/arousal\.py` on the \w+ user turns [^:]*: (.*?); gate `(\w+)`", re.M)


def user_turns(transcript):
    """The quoted `**me:**` turns of the `## text` section, then the live message."""
    text = transcript.split("\n## text\n", 1)[1]
    turns, live = [], []
    for line in text.splitlines():
        if line.startswith("> **me:** "):
            turns.append(line[len("> **me:** "):])
        elif line.strip() and not line.startswith(">"):
            live.append(line)
    # The first unquoted line introduces the quote ("here's where we were:"); the rest is live.
    turns.append("\n".join(live[1:]))
    return turns


class TranscriptReadings(unittest.TestCase):
    def test_recorded_readings_hold(self):
        paths = sorted(TRANSCRIPTS.glob("*.md"))
        self.assertTrue(paths)
        for path in paths:
            with self.subTest(transcript=path.name):
                transcript = path.read_text(encoding="utf-8")
                m = RECORDED.search(transcript)
                self.assertIsNotNone(m, "no recorded arousal.py reading")
                want = [(lv, int(n)) for lv, n in re.findall(r"(\w+) (\d+)", m.group(1))]
                result = arousal.analyse(user_turns(transcript))
                self.assertEqual([(t["level"], t["score"]) for t in result["turns"]], want)
                self.assertEqual(result["gate"], m.group(2))


class Signals(unittest.TestCase):
    def signals(self, text):
        return arousal.analyse([text])["signals"]

    def test_hamesha_spellings_count_alike(self):
        for spelling in ("hamesha", "humesha", "hamesa", "hameshaa"):
            with self.subTest(spelling=spelling):
                s = self.signals("tu {} aisa karti hai".format(spelling))
                self.assertEqual(s["accusations"], 1)
                self.assertEqual(s["absolutes"], 1)

    def test_short_caps_dont_count(self):
        self.assertIsNone(self.signals("NO! OK")["caps_ratio"])

    def test_curly_apostrophe_matches(self):
        self.assertEqual(self.signals("you’re always late")["accusations"], 1)


class Gate(unittest.TestCase):
    def test_one_message_holds(self):
        self.assertEqual(arousal.analyse(["fine, whatever"])["gate"], "hold")

    def test_calm_after_flooded_holds(self):
        flooded = "she ALWAYS does this!! NOBODY ever listens to me, EVER, it's your fault!!"
        self.assertEqual(arousal.analyse([flooded, "ok"])["gate"], "hold")

    def test_two_calm_messages_clear(self):
        self.assertEqual(arousal.analyse(["it was a long day", "i'm a bit better now"])["gate"], "clear")


class Cli(unittest.TestCase):
    def test_empty_input_exits_2(self):
        with tempfile.TemporaryDirectory() as d:
            empty = Path(d) / "messages.txt"
            empty.write_text("\n---\n  \n", encoding="utf-8")
            with redirect_stderr(io.StringIO()):
                self.assertEqual(arousal.main([str(empty)]), 2)

    def test_unreadable_file_exits_1(self):
        with tempfile.TemporaryDirectory() as d, redirect_stderr(io.StringIO()):
            self.assertEqual(arousal.main([str(Path(d) / "missing.txt")]), 1)

    def test_parse_skips_blank_messages(self):
        self.assertEqual(arousal.parse_messages("one\n---\n  \n---\ntwo\n"), ["one", "two"])


if __name__ == "__main__":
    unittest.main()
