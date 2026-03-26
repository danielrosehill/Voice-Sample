# Eq Recommendation

This voice recording has a notable proximity effect (boosted low-end), some mud in the low-mids, and can sound a bit harsh or sibilant depending on the volume and monitoring system. To make this sound like a broadcast-ready voice-over, I recommend the following EQ strategy and processing chain.

### Recommended EQ Preset: "Broadcast Narrator"

| Band Type | Frequency | Gain | Q/Width | Reason |
| :--- | :--- | :--- | :--- | :--- |
| **High Pass (HPF)** | ~85 Hz | -12 dB/Oct | N/A | Essential. Cuts low-end rumble and mechanical noise while smoothing out the proximity effect. |
| **Low-Mid Cut** | ~350 Hz | -3 dB | 1.0 | Cleans up the "mud" or boxiness created by the microphone's inherent sound. |
| **Mid Cut** | ~800 Hz | -2 dB | 1.5 | Often, these microphones can sound a bit "nasal" in this range. A slight dip makes the voice more professional. |
| **High-Mid Boost** | 3.5 kHz | +3 dB | 1.2 | Increases presence and speech intelligibility. This helps the voice "cut through" the mix. |
| **High Shelf** | 10 kHz | +2.5 dB | N/A | Adds "air" and brightness, providing a polished, studio-quality sheen. |

---

### Recommended Processing Chain

Because this is a raw phone recording, I highly recommend the following steps in this exact order:

1.  **De-Esser:** This is crucial. Your recording has some sharp "S" and "T" sounds that the HPF and high boost might accentuate. Use a de-esser to target the 5kHz–8kHz range to tame those harsh sibilants without making the voice sound lisp-y.
2.  **Compressor:** This is essential for podcast narration.
    *   **Ratio:** 3:1 or 4:1.
    *   **Threshold:** Aim for 3-5 dB of gain reduction on the loudest peaks. 
    *   **Make-up Gain:** Add back the volume lost during compression. 
    *   *Goal:* To even out the dynamic range so the volume is consistent throughout the entire piece.
3.  **Subtle Noise Reduction:** If there is any background hiss (common in 24kHz phone recordings), a light noise-reduction plugin (like iZotope RX or a simple gate) can help tidy up the silences between your sentences.
4.  **Limiter:** Add a brick-wall limiter as the final step in the chain. Set the output ceiling to -1.0 dB. This prevents the signal from clipping (distorting) and ensures it hits a professional volume level without sounding over-compressed.

### Summary of Tips for the Speaker
*   **Mic Technique:** You have a lot of "plosives" (popping sounds on 'P' and 'B' words). In future recordings, try to speak slightly across the microphone (at a 45-degree angle) rather than directly into it.
*   **Consistency:** Phone microphones have dynamic gain staging. Try to maintain a constant distance from the mic to keep the tonal quality uniform. 

These steps should transform the raw file into a clean, warm, and professional-sounding podcast narrative.
