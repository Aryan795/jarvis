# Deploy

Everything here runs in one unprivileged LXC on the i5. CPU only.

```bash
cp .env.example .env   # add a long-lived HA token
docker compose up -d
```

Then in Home Assistant, add the Wyoming integration once per service:

| Service | Host | Port |
|---|---|---|
| Whisper | i5 | 10300 |
| Speech-to-phrase | i5 | 10301 |
| Piper | i5 | 10200 |
| Brain STT (once the fan-out exists) | i5 | 10302 |

Once the brain's own Wyoming endpoint is running, point the pipeline's STT at **10302**
instead of 10300 — the brain fans the audio to both decoders itself, because HA's pipeline
takes exactly one STT engine.

| Service | Approx. RAM |
|---|---|
| wyoming-faster-whisper, distil-small.en int8 | ~1 GB |
| speech-to-phrase, English | ~0.3 GB |
| wyoming-piper, one medium voice | ~0.2 GB |
| brain | ~1 GB |
