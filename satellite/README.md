# Satellite

ESPHome firmware for the ESP32-S3 satellite.

## What runs on the board, honestly

| Capability | On an ESP32-S3 | Verdict |
|---|---|---|
| Wake word | `micro_wake_word` with the pretrained `hey_jarvis` model | Yes |
| Fixed-command recognition | esp-sr MultiNet7, up to 200 predefined English commands, within 500 ms of end of speech | Yes. This is "STT on the ESP32" |
| Open-vocabulary STT | Nothing Whisper-class fits. The ESP32-P4 does not change this | No. Streamed to the i5 |
| Speech synthesis | Piper voices are tens of MB of ONNX. esp-sr's own TTS is Chinese-only | No. "TTS on the ESP32" is playing pre-rendered Piper clips from flash |
| Echo cancellation, barge-in | Needs a speaker reference channel and DSP | Not on a single-mic DIY board |

## Two stages

**Stage A** is `jarvis-satellite.yaml` — stock ESPHome, no C++. Everything after the wake
word streams to Home Assistant. Useful on its own, blocks on nothing.

**Stage B** adds `components/multinet`, an external component wrapping esp-sr. Nobody ships
one for ESPHome, so this is the part that has to be written. Stage A does not wait for it.

## Bill of materials

| Part | Stocked in India | Approx. price |
|---|---|---|
| ESP32-S3-DevKitC-1 N16R8 | robu.in, Amazon.in, compoindia | ₹900–1,500 |
| INMP441 I2S MEMS mic | robu.in, Amazon.in | ₹150–300 |
| MAX98357A I2S amp | robu.in, Amazon.in | ₹150–300 |
| 4 Ω 3 W speaker | anywhere | ₹100–200 |

Prices approximate. The Home Assistant Voice PE has a better microphone and open ESPHome
firmware but is not stocked by any Indian retailer found; it is an import at about $59 plus
duty.

## Before flashing

Create `secrets.yaml` next to this file — it is gitignored:

```yaml
wifi_ssid: "..."
wifi_password: "..."
api_encryption_key: "..."
ota_password: "..."
```

Then `make clips` to render the phrase bank, and `make firmware` to build and upload.

On the satellite's HA device page, enable **"Allow the device to perform Home Assistant
actions"** — the on-device path calls `homeassistant.action` directly and silently does
nothing without it.
