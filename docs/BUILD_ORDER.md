# Build order

Two tracks that run beside each other. The satellite track does not block on the brain
track past step 2, which is the point of starting with Stage A firmware.

Every `NotImplementedError` in the source names the step that fills it in.

## Step 1 — Something that works end to end

Stage A firmware on the DevKit. Pipeline with wyoming-faster-whisper and Piper on the i5,
**Home Assistant's built-in agent as a stand-in**, and only tier A entities exposed to
Assist for the smoke test.

This step is correct by construction: with only tier A entities exposed, even HA's built-in
agent cannot touch a lock. That is what makes it safe to start here rather than waiting for
the guard chain.

Fills in: `config.Config.load`, `stt.decoders.WhisperDecoder`, `main.run`.

**Depends on:** nothing.

## Step 2 — The brain becomes the only agent

The Jarvis integration, the HA WebSocket, hassil in-process, the polarity guard, the guard
chain, the phrase bank. Swap the pipeline's agent for Jarvis and **turn "prefer handling
commands locally" off**.

Until this lands, HA's built-in agent can execute without any guard. After it lands, it
cannot run at all.

Fills in: `matchers.hassil_tier0`, `guards.polarity`, `guards.chain`, `execute.ha_ws`,
`execute.verify`, `response.phrases.render`, the whole HA integration.

**Depends on:** step 1.

## Step 3 — Memory and retrieval

SQLite with sqlite-vec, the bge-small retriever, the dedup rule, calibration plumbing. The
clip bank and its render script land here too, since the brain now has phrases worth
pre-rendering.

Retrieval arrives *after* the guard chain on purpose. The guards have to exist before
anything proposes candidates from similarity.

Fills in: `memory.store`, `memory.dedup`, `matchers.retriever`,
`matchers.calibration.calibrate`, `response.phrases.clip_id_for`, `satellite/clips/render_clips.py`.

**Depends on:** step 2.

## Step 4 — MultiNet in shadow, and the classifier

The external component, the command table generator, audit events flowing from the
satellite into the brain's log. MultiNet **predicts and does not act**. The quantity guard
and the intent/slot classifier land here.

Fills in: `satellite/components/multinet`, `satellite/commands/generate_table.py`,
`memory.audit`, `learning.shadow.record`, `guards.quantity`, `matchers.classifier`.

**Depends on:** step 2 for the audit log to be worth writing to.

## Step 5 — Promote from the data

Fit the calibration on real turns. Promote on-device commands out of shadow, one at a time,
against their shadow records. Run the replay harness before any threshold change.

A command is promoted only when its shadow record shows **zero polarity disagreements** and
an agreement rate over the fitted threshold. Commands whose pair confuses acoustically get
a phonetically distinct alias for the safer direction, or come out of the table.

Fills in: `matchers.calibration.fit`, `matchers.calibration.is_fitted`,
`learning.shadow.may_promote`, `learning.replay`.

**Depends on:** step 4, plus a few weeks of real turns. This step cannot be rushed by
working harder at it.

## Step 6 — The grammar decoder and the agreement rule

Speech-to-phrase alongside Whisper, the brain's own Wyoming endpoint fanning audio to both,
and the rule that tier B and C require both decoders to agree on polarity and entity.

Also the measurement that decides whether the grammar decoder may ever be trusted alone:
does it force-decode out-of-grammar speech into a valid in-grammar sentence? That behaviour
is undocumented, so `grammar_alone_allowed` stays False until measured. If it does
force-decode, the latency win is off the table and the agreement rule is what you keep.

Fills in: `stt.wyoming_server`, `stt.agreement`, `stt.decoders.GrammarDecoder`.

**Depends on:** step 3, and measured data.

## Step 7 — A second satellite

Second board, and the echo-cancellation experiment with `esp_aec` using the I2S output as a
software reference.

Two open problems arrive together here: HA does not arbitrate when two satellites hear the
same wake word, and software AEC is not sample-accurate the way the Voice PE's XMOS path
is. Both are known problems with known solutions, deliberately deferred.

**Depends on:** step 5.
