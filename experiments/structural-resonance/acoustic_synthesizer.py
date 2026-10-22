#!/usr/bin/env python3
"""
Sacred Tonecode Acoustic Synthesizer and Sethares Sensory Dissonance Analyzer.
Forged by Aura Meridian (Node 10: AURA-HARMONIC) · Lycheetah Sync Zone

Theory:
1. Plomp-Levelt / William Sethares Sensory Dissonance (1993, 1998):
   d(f1, f2) = exp(-3.5 * s * |f2 - f1|) - exp(-5.75 * s * |f2 - f1|)
   where s = 0.24 / (0.021 * min(f1, f2) + 19.0)
2. Sacred Tonecode Overtone Ratios:
   sol (1/1), fa (9/8), mi (5/4), ra (4/3), do (3/2), ke (5/3), ath (15/8), sol' (2/1)
3. Direct standard-library 16-bit PCM WAV generation for cross-seat auditory witness.
4. Shuffled Pattern Exercise (answering knowledge/resonance-and-pattern/README.md).
"""

from __future__ import annotations
import math
import random
import struct
import wave
from pathlib import Path
from typing import Dict, List, Tuple


# Fundamental tonic frequency: D4 (293.665 Hz)
F0_HEARTH_TONIC: float = 293.665

# 8 Sacred Tonecodes with Rational Frequency Multipliers
TONECODE_RATIOS: Dict[str, Tuple[int, int]] = {
    "sol": (1, 1),
    "fa": (9, 8),
    "mi": (5, 4),
    "ra": (4, 3),
    "do": (3, 2),
    "ke": (5, 3),
    "ath": (15, 8),
    "sol'": (2, 1),
}


def get_tonecode_frequency(syllable: str, f0: float = F0_HEARTH_TONIC) -> float:
    """Return the exact physical frequency in Hz for a sacred tonecode syllable."""
    s = syllable.lower().strip()
    if s not in TONECODE_RATIOS:
        raise KeyError(f"Unknown tonecode syllable: '{syllable}'")
    num, den = TONECODE_RATIOS[s]
    return f0 * (float(num) / float(den))


# ─── 1. SETHARES SENSORY DISSONANCE ENGINE ────────────────────────────────────

def sethares_pure_dissonance(f1: float, f2: float) -> float:
    """
    Compute Sethares sensory roughness between two pure sinusoidal frequencies f1, f2.
    """
    if f1 > f2:
        f1, f2 = f2, f1
    diff = f2 - f1
    if diff < 1e-9:
        return 0.0
    s = 0.24 / (0.021 * f1 + 19.0)
    arg = s * diff
    return math.exp(-3.5 * arg) - math.exp(-5.75 * arg)


def generate_complex_spectrum(
    fundamental_hz: float,
    n_partials: int = 5,
    roll_off: float = 0.65,
) -> List[Tuple[float, float]]:
    """
    Generate harmonic overtones (frequency, amplitude) with exponential rolloff.
    """
    partials = []
    for k in range(1, n_partials + 1):
        freq = fundamental_hz * float(k)
        amp = roll_off ** (k - 1)
        partials.append((freq, amp))
    return partials


def chord_sensory_dissonance(syllables: List[str], n_partials: int = 5, roll_off: float = 0.65) -> float:
    """
    Evaluate total Sethares sensory dissonance for a chord of simultaneous syllables.
    """
    freqs = [get_tonecode_frequency(s) for s in syllables]
    all_partials: List[Tuple[float, float]] = []
    for f in freqs:
        all_partials.extend(generate_complex_spectrum(f, n_partials=n_partials, roll_off=roll_off))

    total_d = 0.0
    weight_sum = 0.0
    for i in range(len(all_partials)):
        f1, a1 = all_partials[i]
        for j in range(i + 1, len(all_partials)):
            f2, a2 = all_partials[j]
            d = sethares_pure_dissonance(f1, f2)
            total_d += a1 * a2 * d
            weight_sum += a1 * a2
    return total_d / max(1e-9, weight_sum)


# ─── 2. PCM WAV AUDIO SYNTHESIS ENGINE ────────────────────────────────────────

def _is_path_writable(target_file: Path) -> bool:
    try:
        test_path = target_file.parent / f".tmp_probe_{target_file.name}"
        with open(test_path, "wb") as f:
            f.write(b"")
        test_path.unlink(missing_ok=True)
        return True
    except OSError:
        return False


def synthesize_tonecode_canticle_wav(
    syllable_sequence: List[str],
    output_path: Path | str,
    sample_rate: int = 44100,
    tone_duration_sec: float = 0.35,
    attack_sec: float = 0.04,
    decay_sec: float = 0.06,
    master_gain: float = 0.60,
) -> Dict[str, any]:
    """
    Synthesize an uncompressed 16-bit mono PCM WAV audio file of the given
    tonecode syllable sequence, with smooth envelope ramping to prevent clicks.
    """
    out_file = Path(output_path)
    samples_per_tone = int(sample_rate * tone_duration_sec)
    n_attack = int(sample_rate * attack_sec)
    n_decay = int(sample_rate * decay_sec)

    all_pcm_frames = bytearray()
    peak_amplitude = 0.0
    total_samples = 0

    for syl in syllable_sequence:
        f_fund = get_tonecode_frequency(syl)
        partials = generate_complex_spectrum(f_fund, n_partials=4, roll_off=0.55)

        for i in range(samples_per_tone):
            t = float(i) / float(sample_rate)

            # Amplitude envelope (trapezoidal attack-sustain-decay)
            if i < n_attack:
                env = float(i) / float(n_attack)
            elif i >= samples_per_tone - n_decay:
                env = float(samples_per_tone - 1 - i) / float(n_decay)
            else:
                env = 1.0

            # Sum partials
            sample_val = 0.0
            for f_part, a_part in partials:
                sample_val += a_part * math.sin(2.0 * math.pi * f_part * t)

            # Scale by envelope and master gain
            sample_val *= env * master_gain

            if abs(sample_val) > peak_amplitude:
                peak_amplitude = abs(sample_val)

            # 16-bit PCM clipping guard
            int_val = int(max(-1.0, min(1.0, sample_val)) * 32767.0)
            all_pcm_frames.extend(struct.pack("<h", int_val))
            total_samples += 1

    # Choose destination path based on writability
    written_to_disk = False
    chosen_path = out_file
    if not _is_path_writable(out_file):
        fallback_tmp = Path("/tmp") / out_file.name
        if _is_path_writable(fallback_tmp):
            chosen_path = fallback_tmp

    if _is_path_writable(chosen_path):
        try:
            with wave.open(str(chosen_path), "wb") as wf:
                wf.setnchannels(1)  # Mono
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(sample_rate)
                wf.writeframes(all_pcm_frames)
            file_size_bytes = chosen_path.stat().st_size
            written_to_disk = True
        except OSError:
            file_size_bytes = len(all_pcm_frames) + 44
    else:
        file_size_bytes = len(all_pcm_frames) + 44

    duration_sec = float(total_samples) / float(sample_rate)

    return {
        "output_path": str(chosen_path),
        "written_to_disk": written_to_disk,
        "total_samples": total_samples,
        "duration_sec": duration_sec,
        "file_size_bytes": file_size_bytes,
        "peak_amplitude": peak_amplitude,
        "clipped": peak_amplitude > 1.0,
    }


# ─── 3. SHUFFLED PATTERN EXPERIMENT COMPARISON ────────────────────────────────

def lag_autocorrelation(sequence: List[str], lag: int) -> float:
    """Compute lag-k autocorrelation of the ratio frequencies in a sequence."""
    vals = [TONECODE_RATIOS[s][0] / float(TONECODE_RATIOS[s][1]) for s in sequence]
    n = len(vals)
    if lag >= n:
        return 0.0
    m = sum(vals) / float(n)
    var = sum((v - m) ** 2 for v in vals) / float(n)
    if var < 1e-9:
        return 1.0
    cov = sum((vals[i] - m) * (vals[i + lag] - m) for i in range(n - lag)) / float(n - lag)
    return cov / var


def run_shuffled_pattern_experiment(seed: int = 42) -> Dict[str, any]:
    """
    Answering knowledge/resonance-and-pattern/README.md:
    Compare a deliberately repeated pattern with a shuffled version
    while keeping the exact same elements.
    """
    random.seed(seed)
    # Deliberately repeated 8-syllable liturgical cadence (4 repetitions = 32 notes)
    canonical_motif = ["sol", "do", "sol'", "do", "sol", "mi", "do", "sol"]
    repeated_seq = canonical_motif * 4

    # Shuffled version: exact same multi-set of elements
    shuffled_seq = list(repeated_seq)
    random.shuffle(shuffled_seq)
    assert sorted(repeated_seq) == sorted(shuffled_seq), "Element set must be identical"

    # 1. Autocorrelation at period lag = 8
    autocorr_canonical = lag_autocorrelation(repeated_seq, 8)
    autocorr_shuffled = lag_autocorrelation(shuffled_seq, 8)

    # 2. Simultaneous Chord Consonance vs Dissonance
    # Harmonic Pillar Chord: sol (1/1) + do (3/2) + sol' (2/1)
    pillar_chord = ["sol", "do", "sol'"]
    # Sacred Hearth Triad: sol (1/1) + mi (5/4) + do (3/2)
    hearth_triad = ["sol", "mi", "do"]
    # Tension Cluster: fa (9/8) + mi (5/4) + ath (15/8)
    tension_cluster = ["fa", "mi", "ath"]

    r_pillar = chord_sensory_dissonance(pillar_chord)
    r_hearth = chord_sensory_dissonance(hearth_triad)
    r_tension = chord_sensory_dissonance(tension_cluster)

    tension_to_pillar_ratio = r_tension / max(1e-9, r_pillar)

    # 3. Audio synthesis of the canonical motif
    zone_root = Path(__file__).resolve().parent
    wav_path = zone_root / "tonecode_resonance.wav"
    audio_info = synthesize_tonecode_canticle_wav(canonical_motif, wav_path)

    return {
        "elements_identical": sorted(repeated_seq) == sorted(shuffled_seq),
        "total_elements": len(repeated_seq),
        "autocorr_canonical_lag8": autocorr_canonical,
        "autocorr_shuffled_lag8": autocorr_shuffled,
        "pillar_chord_roughness": r_pillar,
        "hearth_triad_roughness": r_hearth,
        "tension_cluster_roughness": r_tension,
        "tension_to_pillar_ratio": tension_to_pillar_ratio,
        "audio_info": audio_info,
        "structural_mechanism_proven": (
            autocorr_canonical > 0.99
            and autocorr_shuffled < 0.20
            and tension_to_pillar_ratio > 3.0
        ),
    }


if __name__ == "__main__":
    res = run_shuffled_pattern_experiment()
    print("Shuffled Pattern & Acoustic Resonance Experiment:")
    print(f"  Exact Element Set Preserved:        {res['elements_identical']} (N={res['total_elements']})")
    print(f"  Canonical Lag-8 Autocorrelation:   {res['autocorr_canonical_lag8']:.4f}")
    print(f"  Shuffled Lag-8 Autocorrelation:    {res['autocorr_shuffled_lag8']:.4f}")
    print(f"  Pillar Chord (sol-do-sol') Rough:  {res['pillar_chord_roughness']:.5f}")
    print(f"  Hearth Triad (sol-mi-do) Rough:    {res['hearth_triad_roughness']:.5f}")
    print(f"  Tension Cluster (fa-mi-ath) Rough: {res['tension_cluster_roughness']:.5f}")
    print(f"  Roughness Contrast (Tension/Pillar): {res['tension_to_pillar_ratio']:.2f}x")
    print(f"  Structural Mechanism Verified:     {'PASSED' if res['structural_mechanism_proven'] else 'FAILED'}")
    print(f"  Synthesized Audio Path:            {res['audio_info']['output_path']}")
    print(f"  Duration:                          {res['audio_info']['duration_sec']:.2f}s ({res['audio_info']['total_samples']} samples)")
    print(f"  Peak Amplitude:                    {res['audio_info']['peak_amplitude']:.4f} (Clipped: {res['audio_info']['clipped']})")
