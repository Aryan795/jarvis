# Home Assistant integration

A thin custom component. Copy `custom_components/jarvis` into your HA config directory and
restart.

One conversation entity whose handler forwards the text, `device_id`, `satellite_id`,
`conversation_id` and language to the brain and returns the speech text. **No model runs on
the Pi.** It relays and orchestrates; that is the whole job.

## Pipeline settings that are not optional

In Settings → Voice assistants, for the satellite's pipeline:

| Setting | Value | Why |
|---|---|---|
| Conversation agent | Jarvis | It must be the *only* agent |
| Prefer handling commands locally | **Off** | On, HA's built-in agent runs first and executes on match. "Lock the front door" would lock the door with no confirmation turn |
| Speech-to-text | The brain's Wyoming endpoint on the i5 | Or wyoming-faster-whisper directly until the fan-out exists |
| Text-to-speech | Piper on the i5 | Same voice the clips were rendered with |

The "prefer local" default is the single remaining path by which a tier C action could fire
with no guard. It is a configuration default, not a bug anyone would write, which is
exactly why it is worth writing down.

## Consequence to accept

Sentence-trigger automations only fire under local preference. If any of the 79 automations
use them, they move into the brain's intent set.
