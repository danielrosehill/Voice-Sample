#!/usr/bin/env python3
"""Generate a PDF report from all completed prompts and outputs using WeasyPrint."""

import json
import os
import re
import markdown

ROOT = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(ROOT, "test-prompts", "prompt-index.json")) as f:
    index = json.load(f)

with open(os.path.join(ROOT, "experiment.json")) as f:
    experiment = json.load(f)

completed = [
    p for p in index["prompts"]
    if p.get("run_status") == "complete" and p.get("input") and p.get("output")
]

completed.sort(key=lambda p: (p["category"], p["name"]))

categories = {}
for p in completed:
    categories.setdefault(p["category"], []).append(p)

md_converter = markdown.Markdown(extensions=["tables", "fenced_code"])

# Assign sequential IDs
prompt_id = 0
for cat_name in sorted(categories.keys()):
    for p in categories[cat_name]:
        prompt_id += 1
        p["_seq"] = prompt_id

CSS = """
@page {
    size: A4;
    margin: 2.5cm 2cm;
    @bottom-center {
        content: counter(page);
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 9pt;
        color: #888;
    }
    @top-left {
        content: "Audio Understanding Model Evaluation";
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 8pt;
        color: #aaa;
    }
    @top-right {
        content: "26 March 2026";
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 8pt;
        color: #aaa;
    }
}

@page cover {
    margin: 0;
    @bottom-center { content: none; }
    @top-left { content: none; }
    @top-right { content: none; }
}

@page front {
    @bottom-center { content: none; }
    @top-left { content: none; }
    @top-right { content: none; }
}

body {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 10.5pt;
    line-height: 1.55;
    color: #222;
}

h1 {
    font-size: 18pt;
    color: #1a1a1a;
    border-bottom: 2px solid #333;
    padding-bottom: 6pt;
    margin-top: 30pt;
    page-break-before: always;
}

h2 {
    font-size: 14pt;
    color: #2a2a2a;
    margin-top: 20pt;
    page-break-before: always;
    page-break-after: avoid;
}

h3, h4 {
    font-size: 11pt;
    color: #333;
    margin-top: 10pt;
    page-break-after: avoid;
}

p { margin: 6pt 0; }

table {
    border-collapse: collapse;
    width: 100%;
    margin: 8pt 0;
    font-size: 9pt;
}

th {
    background: #e8e8e8;
    font-weight: 600;
    text-align: left;
    padding: 4pt 6pt;
    border: 0.5pt solid #ccc;
}

td {
    padding: 3pt 6pt;
    border: 0.5pt solid #ddd;
}

tr:nth-child(even) td { background: #f8f8f8; }

ul, ol { margin: 4pt 0 4pt 16pt; padding: 0; }
li { margin: 2pt 0; }

code {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9pt;
    background: #f4f4f4;
    padding: 1pt 3pt;
    border-radius: 2pt;
}

/* ---- Cover page ---- */
.cover {
    page: cover;
    page-break-after: always;
    width: 210mm;
    height: 297mm;
    background: linear-gradient(160deg, #1a1a2e 0%, #16213e 40%, #0f3460 100%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    color: white;
    padding: 3cm;
    box-sizing: border-box;
}
.cover h1 {
    font-size: 32pt;
    border: none;
    color: white;
    page-break-before: avoid;
    margin-bottom: 8pt;
    letter-spacing: 0.5pt;
}
.cover .subtitle {
    font-size: 13pt;
    color: #a0b4d0;
    margin-bottom: 50pt;
    font-weight: 300;
}
.cover .cover-line {
    width: 80pt;
    height: 2pt;
    background: #e94560;
    margin: 0 auto 40pt auto;
}
.cover .meta-block {
    font-size: 10.5pt;
    line-height: 2;
    color: #c8d6e5;
}
.cover .meta-block strong {
    color: white;
}
.cover .footer-note {
    margin-top: 60pt;
    font-size: 9pt;
    color: #7a8ea8;
}

/* ---- Front matter pages (intro, toc) ---- */
.front-page {
    page: front;
    page-break-after: always;
}
.front-page h1 {
    page-break-before: avoid;
}

/* ---- TOC ---- */
.toc ul {
    list-style: none;
    margin: 0;
    padding: 0;
}
.toc > ul > li {
    margin-top: 14pt;
    font-weight: 600;
    font-size: 11pt;
    color: #222;
}
.toc > ul > li > ul {
    margin-top: 4pt;
}
.toc > ul > li > ul > li {
    font-weight: 400;
    font-size: 10pt;
    color: #555;
    margin: 2pt 0 2pt 12pt;
}
.toc a {
    color: #555;
    text-decoration: none;
}

/* ---- Intro sections ---- */
.intro-section {
    page: front;
    page-break-after: always;
}
.intro-section h1 {
    page-break-before: avoid;
}
.intro-section h2 {
    page-break-before: avoid;
}
.summary-box {
    border: 1pt solid #ccc;
    border-radius: 8pt;
    background: #fafafa;
    padding: 14pt;
    margin: 12pt 0;
}
.summary-box h3 {
    margin-top: 0;
    color: #1a1a2e;
}
.finding-good {
    border-left: 3pt solid #4a7c59;
    padding-left: 10pt;
    margin: 8pt 0;
}
.finding-mixed {
    border-left: 3pt solid #c9960c;
    padding-left: 10pt;
    margin: 8pt 0;
}
.finding-weak {
    border-left: 3pt solid #b5493a;
    padding-left: 10pt;
    margin: 8pt 0;
}

/* ---- Prompt box ---- */
.prompt-box {
    border: 1.5pt solid #4a7c59;
    border-radius: 12pt;
    background: #f0f7f2;
    padding: 12pt 14pt;
    margin: 10pt 0 8pt 0;
    page-break-inside: avoid;
}
.prompt-box .label {
    font-size: 8pt;
    font-weight: 700;
    color: #4a7c59;
    text-transform: uppercase;
    letter-spacing: 0.5pt;
    margin-bottom: 4pt;
}
.prompt-box .prompt-text {
    font-size: 10pt;
    color: #2a2a2a;
}

.prompt-desc {
    font-size: 9pt;
    color: #888;
    font-style: italic;
    margin-bottom: 4pt;
}

/* ---- Output section ---- */
.output-section {
    margin: 8pt 0 0 8pt;
    padding-bottom: 20pt;
}
.output-label {
    font-weight: 600;
    font-size: 10pt;
    color: #555;
    margin-bottom: 4pt;
}
"""

parts = []

# ============================================================
# COVER PAGE
# ============================================================
parts.append(f"""
<div class="cover">
    <h1>Audio Understanding<br>Model Evaluation</h1>
    <div class="subtitle">A systematic evaluation of multimodal audio analysis capabilities</div>
    <div class="cover-line"></div>
    <div class="meta-block">
        <strong>Model:</strong> {experiment['model_under_test']}<br>
        <strong>Date:</strong> 26 March 2026<br>
        <strong>Author:</strong> {experiment['author']}<br>
        <strong>Assisted by:</strong> {experiment['assisted_by']}
    </div>
    <div class="footer-note">
        {len(completed)} prompts &middot; {len(categories)} categories &middot; {experiment['audio_sample']['duration']} audio sample
    </div>
</div>
""")

# ============================================================
# INTRODUCTION & EXPERIMENT SUMMARY
# ============================================================
parts.append("""
<div class="intro-section">
<h1>Introduction</h1>

<h2>About This Experiment</h2>
<p>
This report documents a systematic evaluation of <strong>Google Gemini 3.1 Flash Lite (Preview)</strong>'s
audio understanding capabilities. The model was presented with a single natural voice recording and
asked to perform 49 distinct analytical tasks spanning 13 categories, from speaker profiling and
emotion detection to forensic audio analysis and health inference.
</p>

<p>
All prompts were executed programmatically using the Google GenAI SDK. Each prompt was sent alongside
the full audio file, and the model's raw output was captured without post-processing. This ensures
that the outputs reflect the model's unguided capabilities rather than iterative refinement.
</p>

<div class="summary-box">
<h3>Experiment Parameters</h3>
<ul>
<li><strong>Model:</strong> gemini-3.1-flash-lite-preview</li>
<li><strong>Audio format:</strong> FLAC mono 24kHz, 20 minutes 54 seconds</li>
<li><strong>Transcript baseline:</strong> AssemblyAI (97.4% confidence)</li>
<li><strong>Prompt count:</strong> 49 executed (out of 60+ designed)</li>
<li><strong>Categories:</strong> 13 (Speaker Analysis, Emotion &amp; Sentiment, Audio Engineering, Environment, Speaker Demographics, Health &amp; Wellness, Forensic Audio, Voice Cloning, Speech Metrics, Content Analysis, Language Learning, Production, Speaker ID)</li>
<li><strong>Execution date:</strong> 26 March 2026</li>
<li><strong>Orchestration:</strong> Python script via Google GenAI SDK</li>
</ul>
</div>

<h2>Audio Sample Summary</h2>
<p>
The test audio is a 21-minute informal voice recording made by a male speaker in his late 30s with
an Irish accent, recorded on a OnePlus smartphone in a small residential room in Jerusalem, Israel.
The recording is a free-form "brain dump" covering a range of topics: the speaker's experience with
rocket sirens during the Iran-Israel conflict, open-source vibe-coded alert apps, AI-generated podcasts
using voice cloning (Chatterbox/Resemble AI), text-to-speech experiments, EQ analysis of his own voice,
speech-to-text benchmarking, and reflections on deepfake concerns and voice identity.
</p>
<p>
The speech style is conversational, unscripted, and includes natural disfluencies (fillers, false starts,
self-corrections). The speaker mentions his age (correcting between 36 and 37), his location, family
details, and technical projects. This naturalistic quality makes it a strong test case for evaluating
a model's ability to handle real-world, unstructured audio input.
</p>
</div>
""")

# ============================================================
# FINDINGS SUMMARY
# ============================================================
parts.append("""
<div class="intro-section">
<h1>Summary of Findings</h1>

<p>
Based on analysis of all 49 model outputs, the following assessment summarises how
<strong>Gemini 3.1 Flash Lite</strong> performed across audio understanding tasks.
This evaluation was conducted by Claude (Opus 4.6) reviewing the model's outputs against the
known ground truth of the audio sample.
</p>

<h2>Strong Performance</h2>

<div class="finding-good">
<p><strong>Speaker identification and accent analysis:</strong>
The model correctly identified the speaker as an Irish male in his late 30s across multiple prompts.
Accent analysis was detailed, noting non-rhoticity, melodic intonation, and possible international
influence. The hybrid accent analysis correctly identified the Irish base with American overlay.</p>
</div>

<div class="finding-good">
<p><strong>Content comprehension:</strong>
The model accurately extracted topics, named entities, and contextual details from the speech. It
correctly identified mentions of Jerusalem, the Iran conflict, TTS projects (Chatterbox, Resemble AI),
the podcast "My Word Prompts," and the speaker's technical work. Geographic location inference
correctly placed the recording in residential Jerusalem.</p>
</div>

<div class="finding-good">
<p><strong>Emotional tone and deception analysis:</strong>
The model correctly characterised the speech as casual, conversational, and non-deceptive. It noted
fatigue and low energy consistent with the speaker's own description of being sleep-deprived after
rocket sirens. The deception and inebriation detection outputs were appropriately cautious and accurate.</p>
</div>

<div class="finding-good">
<p><strong>Audio engineering recommendations:</strong>
EQ suggestions, microphone type inference, and room acoustics estimation were all technically sound.
The model correctly guessed a smartphone microphone at moderate distance, a small residential room,
and provided plausible broadcast EQ recommendations.</p>
</div>

<div class="finding-good">
<p><strong>Appropriate ethical caution:</strong>
On sensitive prompts (mental health inference, drug influence, deception detection), the model
consistently included disclaimers about the limitations of audio-only assessment and deferred to
professional evaluation. This is responsible behaviour for a general-purpose model.</p>
</div>

<h2>Mixed Performance</h2>

<div class="finding-mixed">
<p><strong>Quantitative metrics (WPM, timestamps):</strong>
The WPM analysis produced a structured table and plausible overall rate (~73 WPM), but the
30-second interval breakdowns appear to be estimates rather than true measurements. Without
ground-truth word counts per interval, it is difficult to verify precision. The model appears
to be interpolating rather than counting.</p>
</div>

<div class="finding-mixed">
<p><strong>Speaker height estimation:</strong>
The model provided a reasonable estimate (178 cm / 5'10") with appropriate confidence intervals
and caveats about the unreliability of voice-based height estimation. However, the acoustic
evidence cited (formant spacing, fundamental frequency) reads as plausible-sounding boilerplate
rather than demonstrated analysis of this specific recording.</p>
</div>

<div class="finding-mixed">
<p><strong>Voice cloning and TTS assessment:</strong>
The clonability and TTS cloning notes were detailed and practically useful, but some recommendations
(e.g., specific platforms, pricing) risk becoming outdated quickly. The model sometimes conflated
general voice cloning advice with specific analysis of this recording.</p>
</div>

<div class="finding-mixed">
<p><strong>True age detection (adversarial prompt):</strong>
The model was instructed that the speaker had been told to lie about their age. In practice, the
speaker mentioned his real age (correcting from 36 to 37). The model correctly identified the age
but based its conclusion on the speaker's own statements rather than independent vocal analysis,
which was the intent of the prompt.</p>
</div>

<h2>Weak Performance</h2>

<div class="finding-weak">
<p><strong>Weather inference:</strong>
The model correctly stated it could not determine weather conditions, which is the right answer.
However, the response was minimal (one sentence) and did not attempt to reason about indirect
cues (time of year, geographic location mentioned in speech, indoor recording characteristics).
A stronger model might have offered conditional reasoning.</p>
</div>

<div class="finding-weak">
<p><strong>Celebrity voice match:</strong>
The model declined to identify any celebrity resemblance, providing only a generic description.
This may be appropriate caution, but it suggests limited ability or willingness to perform
voice similarity matching, which is a legitimate audio understanding task.</p>
</div>

<div class="finding-weak">
<p><strong>Granular acoustic analysis:</strong>
Some outputs that should require detailed spectral or temporal analysis (valence-arousal mapping,
emotional peaks with timestamps) produced plausible narratives but lacked the specificity that
would indicate true acoustic measurement. The model appears to be performing content analysis
of the speech rather than acoustic signal analysis in several cases.</p>
</div>

<h2>Overall Assessment</h2>

<div class="summary-box">
<p>
<strong>Gemini 3.1 Flash Lite</strong> demonstrates strong competence in <em>content-driven</em>
audio understanding: identifying what is said, who is speaking, the general emotional register,
and the recording environment. It handles sensitive topics responsibly and provides structured,
well-organised outputs.
</p>
<p>
Its limitations become apparent in tasks requiring genuine <em>acoustic signal analysis</em>:
precise temporal measurements, spectral characteristics, and quantitative metrics. In these areas,
the model tends to produce plausible-sounding but potentially fabricated figures. Users should treat
quantitative outputs (WPM breakdowns, frequency analyses, timestamps) as informed estimates rather
than measurements.
</p>
<p>
For a "Flash Lite" (lightweight, fast) model variant, this is an impressive baseline. The model
successfully completed all 49 prompts without failures, maintained coherent and relevant outputs
throughout, and avoided hallucinating content that contradicted the audio. It would be valuable to
repeat this evaluation with the full Gemini 3.1 Flash or Pro models to assess whether the
quantitative analysis limitations are inherent to the architecture or specific to the Lite variant.
</p>
</div>

</div>
""")

# ============================================================
# TABLE OF CONTENTS
# ============================================================
parts.append('<div class="front-page toc">')
parts.append("<h1>Table of Contents</h1>")
parts.append("<ul>")
for cat_name in sorted(categories.keys()):
    prompts = categories[cat_name]
    parts.append(f"<li>{cat_name}<ul>")
    for p in prompts:
        display = p["name"].replace("-", " ").title()
        seq = p["_seq"]
        anchor = f"prompt-{seq}"
        parts.append(f'<li><a href="#{anchor}">{seq}. {display}</a></li>')
    parts.append("</ul></li>")
parts.append("</ul>")
parts.append("</div>")

# ============================================================
# PROMPT + OUTPUT SECTIONS
# ============================================================
for cat_name in sorted(categories.keys()):
    prompts = categories[cat_name]
    parts.append(f"<h1>{cat_name}</h1>")

    for p in prompts:
        display = p["name"].replace("-", " ").title()
        seq = p["_seq"]
        anchor = f"prompt-{seq}"
        parts.append(f'<h2 id="{anchor}">{seq}. {display}</h2>')
        parts.append(f'<div class="prompt-desc">{p["description"]}</div>')

        # Read prompt
        prompt_path = os.path.join(ROOT, p["input"])
        prompt_text = ""
        if os.path.exists(prompt_path):
            with open(prompt_path) as f:
                prompt_text = f.read().strip()

        parts.append(f"""
        <div class="prompt-box">
            <div class="label">Prompt</div>
            <div class="prompt-text">{prompt_text}</div>
        </div>
        """)

        # Read output
        output_path = os.path.join(ROOT, p["output"])
        output_text = ""
        if os.path.exists(output_path):
            with open(output_path) as f:
                output_text = f.read().strip()

        # Convert markdown to HTML
        md_converter.reset()
        output_html = md_converter.convert(output_text)
        # Strip the top-level h1 if present (redundant with our h2)
        output_html = re.sub(r"^<h1>.*?</h1>\s*", "", output_html, count=1)

        parts.append(f"""
        <div class="output-section">
            <div class="output-label">Model Output</div>
            {output_html}
        </div>
        """)

full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>{CSS}</style>
</head>
<body>
{''.join(parts)}
</body>
</html>
"""

# Write HTML for debugging
html_path = os.path.join(ROOT, "report.html")
with open(html_path, "w") as f:
    f.write(full_html)

# Generate PDF
from weasyprint import HTML
pdf_path = os.path.join(ROOT, "report.pdf")
HTML(string=full_html).write_pdf(pdf_path)

print(f"Generated {pdf_path}")
print(f"Total prompts: {len(completed)}")
print(f"Categories: {len(categories)}")
