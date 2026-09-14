#!/usr/bin/env python3
"""Generate the Jarvis v3 architecture SVG in the visual style of the April 2026 v1 diagram."""
from xml.sax.saxutils import escape

W, H = 870, 1490
FONT = "-apple-system, 'Helvetica Neue', Helvetica, Arial, sans-serif"

PAL = {
    "green":  ("rgb(8,80,65)",    "rgb(93,202,165)",  "rgb(159,225,203)"),
    "purple": ("rgb(60,52,137)",  "rgb(175,169,236)", "rgb(210,206,246)"),
    "blue":   ("rgb(12,68,124)",  "rgb(110,175,235)", "rgb(175,215,250)"),
    "olive":  ("rgb(39,80,10)",   "rgb(150,210,95)",  "rgb(195,235,150)"),
    "amber":  ("rgb(99,56,6)",    "rgb(239,159,39)",  "rgb(250,199,117)"),
    "gray":   ("rgb(68,68,65)",   "rgb(170,168,160)", "rgb(215,213,205)"),
    "rust":   ("rgb(113,43,19)",  "rgb(240,150,110)", "rgb(250,195,170)"),
    "maroon": ("rgb(114,36,62)",  "rgb(235,140,175)", "rgb(250,195,215)"),
}
GROUP_STROKE = "rgba(0,0,0,0.28)"
LABEL = "rgb(110,108,100)"
ARROW = "rgba(0,0,0,0.5)"
ARROW_SOFT = "rgba(0,0,0,0.32)"

out = []
warn = []

def est(text, size):
    return len(text) * size * 0.52

def box(x, y, w, h, pal, lines, title_size=13, sub_size=10.5, stroke_w=0.5):
    fill, stroke, title = PAL[pal]
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
               f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}"/>')
    n = len(lines)
    gap = 13
    block = title_size + gap * (n - 1)
    cy = y + h / 2
    ty = cy - block / 2 + title_size / 2
    cx = x + w / 2
    for i, line in enumerate(lines):
        if i == 0:
            out.append(f'<text x="{cx}" y="{ty:.1f}" text-anchor="middle" dominant-baseline="central" '
                       f'font-size="{title_size}" font-weight="500" fill="{title}">{escape(line)}</text>')
            if est(line, title_size) > w - 12:
                warn.append(f"title overflow: {line!r} in {w}px")
        else:
            yy = ty + gap * i
            out.append(f'<text x="{cx}" y="{yy:.1f}" text-anchor="middle" dominant-baseline="central" '
                       f'font-size="{sub_size}" fill="{stroke}">{escape(line)}</text>')
            if est(line, sub_size) > w - 12:
                warn.append(f"line overflow: {line!r} in {w}px")

def group(x, y, w, h, label):
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="none" '
               f'stroke="{GROUP_STROKE}" stroke-width="1" stroke-dasharray="6 4"/>')
    out.append(f'<text x="{x+10}" y="{y-7}" font-size="12" font-weight="500" fill="{LABEL}">{escape(label)}</text>')

def arrow(d, label=None, lx=None, ly=None, soft=False, dashed=False, head=True):
    stroke = ARROW_SOFT if soft else ARROW
    extra = ' stroke-dasharray="4 3"' if dashed else ""
    m = ' marker-end="url(#arrow)"' if head else ""
    out.append(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="1.5"{extra}{m}/>')
    if label:
        out.append(f'<text x="{lx}" y="{ly}" text-anchor="middle" font-size="10" fill="{LABEL}">{escape(label)}</text>')

def note(x, y, text, anchor="start", size=11):
    out.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{LABEL}">{escape(text)}</text>')

# ---------- header ----------
note(30, 14, "Jarvis · system architecture after the 13 Sep 2026 review", size=12)
note(W - 30, 14, "supersedes jarvis_system_architecture.svg · Apr 2026", anchor="end", size=11)

# ---------- band 1: three locations ----------
group(30, 44, 300, 596, "ESP32-S3 satellite · ESPHome on ESP-IDF")
group(350, 44, 220, 596, "Home Assistant · HAOS Pi 4 · relay")
group(590, 44, 250, 596, "Jarvis brain · i5 LXC · CPU only")

# column A (x 56..306)
AX, AW = 56, 250
box(AX, 64, AW, 48, "green", ["I2S mic + amp", "INMP441 · MAX98357A · 16 kHz 16-bit mono"])
box(AX, 128, AW, 48, "green", ["Wake word · micro_wake_word", "hey_jarvis + VAD · always on · plays chime"])
box(AX, 214, AW, 76, "green", ["MultiNet fast path", "esp-sr mn7_en · ~50 tier-A commands",
                               "absolute states only · shadow phase first", "< 500 ms · needs HA, not the i5"], stroke_w=1.5)
box(AX, 306, AW, 62, "green", ["Stream to HA", "voice_assistant · PCM 16 kHz · native API",
                               "starts with MultiNet · cancelled on a hit"])
box(AX, 384, AW, 48, "green", ["Clip bank in flash", "Piper renders · FLAC · acks, errors, chime"])
box(AX, 448, AW, 48, "green", ["satellite_hit event", "cmd · p1 · p2 → HA → audit log"])
box(AX, 512, AW, 48, "green", ["Speaker · announcement pipeline", "no barge-in · mic gated while playing"])
box(AX, 576, AW, 48, "gray",  ["Physical fallback", "mic-mute GPIO · wall rockers if HA is down"])

# column B (x 360..560)
BX, BW = 360, 200
box(BX, 64, BW, 48, "purple", ["Exposed entities + areas", "the only vocabulary, hassil too"])
box(BX, 128, BW, 48, "purple", ["Wyoming integration", "STT + TTS by host:port on the i5"])
box(BX, 228, BW, 48, "purple", ["Native API action", "satellite → HA service · tier A only"])
box(BX, 306, BW, 62, "purple", ["Assist pipeline", "VAD · one STT · one agent · one TTS",
                                "prefer-local OFF · else tier C bypass"])
box(BX, 384, BW, 48, "purple", ["Jarvis conversation entity", "text · device_id · satellite_id"])
box(BX, 448, BW, 48, "purple", ["WebSocket API", "call_service · verify · state events"])
box(BX, 512, BW, 48, "purple", ["TTS cache", "by text · URL streamed to satellite"])
box(BX, 576, BW, 48, "gray",   ["Nothing heavy runs here", "2 GB · 79 automations · 32 KB/s relay"])

# column C (x 600..830)
CX, CW = 600, 230
box(CX, 64, CW, 62, "gray", ["Placement", "Whisper · S2P · Piper · embeddings · NLU",
                             "all on the i5 LXC, never on the Pi"])
box(CX, 142, CW, 48, "blue", ["Audit subscriber", "state_changed + satellite_hit → log"])
box(CX, 206, CW, 48, "blue", ["Registry sync", "exposed names → hassil slots + S2P grammar"])
# STT service container
fill, stroke, title = PAL["blue"]
out.append(f'<rect x="{CX}" y="306" width="{CW}" height="110" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="0.5"/>')
out.append(f'<text x="{CX+CW/2}" y="322" text-anchor="middle" dominant-baseline="central" font-size="13" font-weight="500" fill="{title}">STT service · Wyoming endpoint</text>')
def inner(x, y, w, h, lines):
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="rgb(20,90,160)" stroke="{stroke}" stroke-width="0.5"/>')
    cx = x + w / 2
    ty = y + h / 2 - (12 + 11 * (len(lines) - 1)) / 2 + 6
    for i, line in enumerate(lines):
        size = 12 if i == 0 else 9.5
        col = title if i == 0 else stroke
        out.append(f'<text x="{cx}" y="{ty + 11*i:.1f}" text-anchor="middle" dominant-baseline="central" font-size="{size}" font-weight="{500 if i==0 else 400}" fill="{col}">{escape(line)}</text>')
inner(CX, 334, 110, 44, ["Speech-to-Phrase", "grammar-constrained", "tens of ms · measure"])
inner(CX + 120, 334, 110, 44, ["distil-whisper", "small.en · no prompt", "0.9–1.4 s"])
out.append(f'<text x="{CX+CW/2}" y="398" text-anchor="middle" dominant-baseline="central" font-size="10" fill="{stroke}">B/C need both to agree · audio hash kept</text>')
box(CX, 448, CW, 62, "blue", ["Cascade + context injector", "FastAPI + asyncio · area from satellite_id",
                              "text in → guard chain below → speech out"])
box(CX, 512, 110, 48, "blue", ["Piper TTS", "Wyoming · one voice", "shared with the clips"], title_size=12, sub_size=9.5)

# ---------- band 1 arrows ----------
arrow("M181 112 L181 128")
arrow("M181 176 L181 192", head=False)
out.append('<circle cx="181" cy="192" r="3" fill="rgba(0,0,0,0.5)"/>')
arrow("M181 192 L181 214")                           # dot -> MultiNet
arrow("M181 192 L44 192 L44 337 L56 337")            # dot -> stream, via left corridor
out.append(f'<text x="36" y="268" transform="rotate(-90 36 268)" text-anchor="middle" font-size="9" fill="{LABEL}">both start on wake</text>')
arrow("M306 252 L360 252", "tier A", 333, 245)  # MultiNet -> native API action
arrow("M306 337 L360 337", "audio", 333, 330)          # stream -> assist pipeline
arrow("M560 337 L600 337", "audio", 580, 330)          # pipeline -> STT service
arrow("M600 408 L560 408", "text", 580, 402)     # STT -> conversation entity
arrow("M560 426 L600 470")                             # entity -> cascade
arrow("M600 536 L560 536", "speech", 580, 529)         # piper -> tts cache
arrow("M360 536 L306 536", "URL", 333, 529)            # tts cache -> speaker
# cascade -> decision band bus
arrow("M770 510 L770 648 L165 648", head=False)
arrow("M165 648 L165 702")
arrow("M435 648 L435 702")
note(762, 596, "turn enters the race", anchor="end", size=9)

# ---------- band 2: decision ----------
group(30, 674, 810, 330, "Decision — hassil ‖ retriever race, then the guard chain · nothing fires without passing all three gates")
box(40, 702, 250, 56, "olive", ["Tier 0 · hassil, in-process", "match or nothing · per-bucket prior"])
box(310, 702, 250, 56, "olive", ["Tier 1 · semantic retriever", "sqlite-vec + bge-small · candidates only"])
box(580, 702, 250, 56, "gray",  ["Tier 2 · local NLU", "DistilBERT intent + slots · on a miss"])
box(40, 786, 250, 62, "amber", ["1 · Calibration", "score → P(correct) · fit from audit log", "no guessed constants"])
box(310, 786, 250, 62, "amber", ["2 · Polarity + quantity guard", "verbs · negation · numbers · RAW text", "mismatch kills the candidate"])
box(580, 786, 250, 62, "amber", ["3 · Risk gate", "A ≥ 0.80 fire · B ≥ 0.92 announce first", "C · confirmation turn, always"])
box(40, 882, 380, 56, "blue", ["Execution engine", "HA WebSocket · call_service · verify state · log the turn"])
box(440, 882, 390, 56, "rust", ["Tier 3 · Clarify", "ask, never guess · continue_conversation reopens the mic"])
arrow("M165 758 L165 786")
arrow("M435 758 L165 786", soft=True)
arrow("M705 758 L435 786", "re-enters at gate 2", 640, 776, soft=True)
arrow("M290 817 L310 817")
arrow("M560 817 L580 817")
arrow("M705 848 L230 882", "pass", 440, 868)
arrow("M705 848 L635 882", "unsure", 690, 872)
note(830, 976, "Rejection at any gate drops to tier 2, whose output re-enters at gate 2.", anchor="end", size=10.5)
note(830, 991, "HA's built-in agent and sentence triggers stay off: the brain is the only agent.", anchor="end", size=10.5)

# ---------- band 3: memory ----------
group(30, 1024, 810, 190, "Memory — SQLite + sqlite-vec · one file, single truth")
box(40, 1052, 250, 56, "olive", ["Commands + vectors", "confidence · episodes · index rebuildable"])
box(310, 1052, 250, 56, "olive", ["Audit log", "every turn, satellite hits included"])
box(580, 1052, 250, 56, "olive", ["Replay harness", "zero regressions before any deploy"])
box(40, 1132, 250, 56, "maroon", ["Shadow gate", "predict-only until N confirms · MultiNet too"])
box(310, 1132, 250, 56, "olive", ["Calibration fits", "per matcher, from shadow data"])
box(580, 1132, 250, 56, "gray",  ["Dedup rule", "identical intent · polarity · entity · slot"])
arrow("M300 938 L400 1052", "log every turn", 270, 975, soft=True, dashed=True)

# ---------- band 4: learning ----------
group(30, 1234, 810, 106, "Learning — built last · everything starts predict-only")
box(40, 1262, 250, 56, "maroon", ["Habit detector", "time + sequence patterns → shadow first"])
box(310, 1262, 250, 56, "maroon", ["Correction classifier", "“no, actually…” → confidence update"])
box(580, 1262, 250, 56, "maroon", ["Proactive engine", "suggests automations · never creates silently"])

# ---------- band 5: failure ----------
group(30, 1360, 810, 106, "Failure behaviour — silence is never an outcome")
box(40, 1382, 250, 62, "gray", ["i5 down", "fast path still works, via HA", "otherwise ‘brain unreachable’ clip"])
box(310, 1382, 250, 62, "gray", ["Pi 4 or Wi-Fi down", "wake works · the action call fails", "‘hub unreachable’ clip · use the rockers"])
box(580, 1382, 250, 62, "gray", ["MultiNet false accept", "the acknowledgement names the action", "‘hey jarvis, undo’ · pair logged for review"])

note(30, 1480, "13 Sep 2026 · voice/ARCHITECTURE_REVIEW.md · v1 defect removed: dispatch on FAISS > 0.85 · embeddings retrieve, deterministic code decides", size=10.5)

svg = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" xmlns="http://www.w3.org/2000/svg" font-family="{FONT}">',
       '<title>Jarvis v3 system architecture</title>',
       '<desc>ESP32-S3 satellite with on-device wake word and MultiNet fast path, Home Assistant on a Pi 4 as relay and orchestrator, and a CPU-only brain on the i5 with a two-decoder STT service, a hassil/retriever race, a three-gate guard chain, SQLite memory, and predict-only learning.</desc>',
       '<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
       '<path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>',
       f'<rect x="0" y="0" width="{W}" height="{H}" fill="rgb(250,250,247)"/>']
svg += out
svg.append('</svg>')
open('/Users/aryanpandey/Documents/claude/voice/jarvis_system_architecture_v3.svg', 'w').write("\n".join(svg))
print("ok")
