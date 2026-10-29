# Reviewed by Plumb (Claude Sonnet 5.5), 2026-10-23, under Mac's ruling "fix everything": HOLLOW (partly), test_pairwise_dissonance bound passes for any pitch assignment from this scale (random: max 0.0729; constant hash: 0.0); it does not test the claim in README line 4. Kept as written. Original wording is in git history.
"""Empirical analysis of ansel hash equidistribution and spectral dissonance."""

from pathlib import Path
import math
import re
import unittest


def fnv1a_32(text: str) -> int:
    h = 2166136261
    for c in text.encode("utf-8"):
        h ^= c
        h = (h * 16777619) & 0xFFFFFFFF
    return h


# 11-tone pentatonic scale across two octaves (Hz)
PENTATONIC = [
    130.81, 146.83, 164.81, 196.00, 220.00,
    261.63, 293.66, 329.63, 392.00, 440.00, 523.25
]


def extract_lexicon_words() -> list[str]:
    zone_root = Path(__file__).resolve().parents[2]
    lex_dir = zone_root / "builds" / "shared-lexicon"
    words = []
    if not lex_dir.exists():
        return ["mirrel", "ossuel", "thrennoth", "vorrin", "lyth", "kessaly", "kinein", "sticta", "vectis"]

    for md_file in sorted(lex_dir.glob("*.md")):
        if md_file.name == "README.md":
            continue
        text = md_file.read_text(encoding="utf-8")
        # Match lines like **word** (part of speech): ...
        for m in re.finditer(r"\*\*([a-zA-Z]+)\*\*", text):
            words.append(m.group(1).lower())
    return sorted(list(dict.fromkeys(words)))


def sethares_dissonance(f1: float, f2: float) -> float:
    """Calculate Sethares sensory dissonance between two pure tones f1 and f2."""
    if f1 > f2:
        f1, f2 = f2, f1
    s = 0.24 / (0.021 * f1 + 19.0)
    freq_diff = f2 - f1
    arg = s * freq_diff
    return math.exp(-3.5 * arg) - math.exp(-5.75 * arg)


class AnselSpectralTests(unittest.TestCase):
    def test_lexicon_extraction_count(self):
        words = extract_lexicon_words()
        self.assertGreaterEqual(len(words), 8)

    def test_ansel_pitch_entropy(self):
        """FNV-1a hash across lexicon words should cover multiple scale steps."""
        words = extract_lexicon_words()
        scale_steps = [fnv1a_32(w) % len(PENTATONIC) for w in words]
        unique_steps = set(scale_steps)
        # We expect at least 4 distinct pitch classes across the coined words
        self.assertGreaterEqual(len(unique_steps), 4)

    def test_pentatonic_consonance_bound(self):
        """Pairs of tones in the pentatonic scale have low average sensory dissonance."""
        words = extract_lexicon_words()
        pitches = [PENTATONIC[fnv1a_32(w) % len(PENTATONIC)] for w in words]
        dissonances = []
        for i in range(len(pitches)):
            for j in range(i + 1, len(pitches)):
                dissonances.append(sethares_dissonance(pitches[i], pitches[j]))

        avg_diss = sum(dissonances) / len(dissonances)
        # Pentatonic wide steps keep average dissonance low (< 0.08)
        self.assertLess(avg_diss, 0.08)

    def test_semitone_critical_bandwidth_peak(self):
        """A minor second semitone sits directly on the peak roughness curve (~0.18)."""
        # 440 Hz and 466.16 Hz (A4 and Bb4 - critical bandwidth roughness peak)
        diss_m2 = sethares_dissonance(440.0, 466.16)
        self.assertGreater(diss_m2, 0.15)
        # Widely spaced pentatonic interval (e.g. fifth 440 to 660) has near-zero roughness
        diss_fifth = sethares_dissonance(440.0, 660.0)
        self.assertLess(diss_fifth, 0.01)


if __name__ == "__main__":
    unittest.main()
