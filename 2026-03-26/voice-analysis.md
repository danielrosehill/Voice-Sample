# Voice Sample Analysis — 26 March 2026

**File**: `26_03_2026_16_08.flac`
**Date**: 2026-03-26 16:08
**Analyzed with**: sox, Praat (via parselmouth)

---

## Audio Properties

| Property | Value |
|----------|-------|
| Format | FLAC (mono, 16-bit) |
| Sample Rate | 24,000 Hz |
| Duration | 20m 54s (1,254s) |
| File Size | 30.9 MB |
| Bit Rate | 197 kbps |
| Device | OnePlus Nord 3.5G (HQ mode) |
| Environment | Untreated room, phone-level noise cancellation |

---

## Words Per Minute (WPM)

| Metric | Value |
|--------|-------|
| Total words | 3,524 |
| Overall WPM | **168.6** |
| Category | Moderate (podcasting sweet spot: 140-170) |

### Segment WPM Samples

| Segment | WPM | Words |
|---------|-----|-------|
| 0:00-0:28 | 150.0 | 70 |
| 0:28-0:57 | 173.8 | 84 |
| 0:57-1:25 | 162.9 | 76 |

Average conversational English is 120-150 WPM. This sample sits at the upper end of conversational / moderate pace, right at the podcasting sweet spot.

---

## Pitch (F0) Analysis

| Metric | Value |
|--------|-------|
| Mean F0 | 117.4 Hz |
| Median F0 | 109.6 Hz |
| Std Dev | 33.3 Hz |
| Min | 74.9 Hz |
| Max | 499.9 Hz |
| Range | 425.0 Hz |
| 10th percentile | 93.3 Hz |
| 90th percentile | 146.6 Hz |
| **Voice Type** | **Bass / Low Baritone** |

The median F0 of ~110 Hz places this voice solidly in the bass-baritone range. The wide range (425 Hz) and CV of 28.3% indicate expressive, varied prosody — consistent with the conversational, stream-of-consciousness speaking style.

---

## Formant Analysis (Vocal Tract Resonances)

| Formant | Mean | Median | Indicates |
|---------|------|--------|-----------|
| F1 | 669 Hz | 564 Hz | Jaw openness |
| F2 | 1,896 Hz | 1,904 Hz | Tongue front/back position |
| F3 | 2,873 Hz | 2,803 Hz | Lip rounding / vocal tract length |

The F2 mean of ~1,900 Hz is slightly fronted, consistent with English vowel placement. F1 median of 564 Hz suggests moderate jaw openness typical of relaxed conversational speech.

---

## Signal Levels

| Metric | Value |
|--------|-------|
| Peak Level | -1.02 dB (good headroom, no clipping) |
| RMS Level | -22.21 dB |
| RMS Peak | -8.64 dB |
| RMS Trough | -74.44 dB |
| Crest Factor | 11.47 (high dynamic range) |
| Dynamic Range | ~65.8 dB |
| DC Offset | -0.000016 (negligible) |
| Mean Intensity | 59.9 dB |
| Intensity StdDev | 15.9 dB |

---

## Voice Quality Metrics

| Metric | Value | Assessment |
|--------|-------|------------|
| HNR | 9.6 dB | Breathy / fatigued |
| Jitter (local) | 2.713% | Elevated (norm < 1.04%) |
| Shimmer (local) | 13.089% | Elevated (norm < 3.81%) |

**Note**: Elevated jitter/shimmer and lower HNR are expected given context: the speaker was fatigued (disrupted sleep from rocket sirens), recording on a phone mic in an untreated room while pacing. These metrics would likely improve with rest and a condenser mic in a treated environment.

---

## Speaking Rhythm

| Metric | Value |
|--------|-------|
| Voiced frames | 50.8% |
| Pause/unvoiced | 49.2% |
| Pitch variability (CV) | 28.3% |

The roughly 50/50 voiced/unvoiced split reflects natural conversational pauses, filler moments, and the stream-of-consciousness style. The 28.3% pitch CV confirms expressive, non-monotone delivery.

---

## Voice Profile Summary

- **Speaker**: Male, late 30s
- **Voice type**: Bass / Low Baritone (median F0 ~110 Hz)
- **Accent**: Irish (Cork origin), softened by ~11 years in Israel
- **Style**: Conversational, freeform, expressive prosody
- **WPM**: ~169 (moderate-fast, ideal for podcasting)
- **Quality note**: Recorded while fatigued — voice quality metrics reflect this

---

## EQ Observations

- Recording at 24 kHz caps frequency content at 12 kHz (Nyquist)
- Phone mic likely adds presence boost around 2-4 kHz
- Untreated room may introduce low-mid mud at ~200-400 Hz
- High crest factor (11.47) suggests natural, uncompressed dynamics
- Spectrogram saved as `spectrogram.png` for visual reference
