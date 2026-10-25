---
name: build-video-handoff
description: Validate an existing source-linked video brief and build narration, storyboard, source ledger and shorts render manifest with exact hashes. Use when a reviewed brief needs a local production handoff.
---

# Build video handoff

Use the bundled Python helper to avoid rewriting the brief-to-render conversion.
Resolve paths from this skill's directory; it works when copied on its own.
Python3.10+ is sufficient; no packages, accounts or model calls are required.

```bash
python scripts/build_packet.py assets/example-brief.json --out output/example
```

For the user's work, replace the example path with their brief and choose a new
output folder. The complete example documents the required fields. The helper
rejects unknown source IDs, missing narration/action/provenance, invalid timing,
duplicate source IDs and an existing output folder.

Inspect the resulting `narration.md`, `storyboard.json`, `sources.json`,
`short.json` and `receipt.json`. Report structural validation separately from
factual review. Its `source_claims_human_reviewed:false` and
`speech_recorded:false` do not become true because the command succeeded.

Hand `short.json` to a compatible renderer if requested. Narration timing is a
plan until matched to a real recording; the manifest deliberately contains no
guessed speech captions. Preserve earlier outputs and diagnose a failed brief
before trying again in a fresh folder. This helper does not render or publish.
