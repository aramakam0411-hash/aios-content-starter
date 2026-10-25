# Brief format

Use `assets/example-brief.json` from the skill root as the complete JSON example.

| Field | Meaning |
| --- | --- |
| title | Viewer-facing subject/question |
| sources | Records with unique `id`, original HTTPS `url`, supporting `note` |
| scenes | Ordered scene records |
| scenes[].title | Short visible heading |
| scenes[].seconds | Initial duration, 1 to 60 seconds |
| scenes[].narration | Exact proposed spoken words |
| scenes[].action | Meaningful visible change, focus and settled result |
| scenes[].steps | 1 to 4 visible labels, at most 24 characters each |
| scenes[].sources | Known source IDs supporting this scene |
| scenes[].visual_basis | `original`, `own-recording`, `licensed`, or `documentation-illustration` |

The existing handoff builder supports up to30scenes and180seconds. Keep full
source URLs in the ledger; the rendered credit uses short source IDs. This
schema describes a plan, not a claim that speech or external footage is ready.
