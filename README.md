# AIOS Content Starter

Three portable agent skills for turning a real workflow or sourced idea into
useful production material. The skills are the main entry point; the AIOX squad,
examples and local Python helpers support them. **Synkra AIOX (formerly AIOS)**
is distinct from AGI Research's AIOS kernel. This is not an official Synkra package.

## Choose a skill

| Skill | Use it for | Output |
| --- | --- | --- |
| [source-to-video-brief](skills/source-to-video-brief/SKILL.md) | Turn checked sources into a useful factual explanation | Source-linked narration and visible scene actions |
| [workflow-to-aiox-squad](skills/workflow-to-aiox-squad/SKILL.md) | Turn your own repeatable process into specific tasks and roles | AIOX squad files, ordered handoffs and a receipt |
| [build-video-handoff](skills/build-video-handoff/SKILL.md) | Validate a brief and prepare material for rendering | Narration, storyboard, source ledger and shorts manifest |

Copy a selected **whole folder** from `skills/` into your assistant's chosen
skills directory if it supports SKILL.md discovery. Keep its scripts, references
and assets together. You can also ask an assistant to read the chosen SKILL.md
directly in this checkout. No global configuration change is needed to try it.

Example requests:

> Use source-to-video-brief to explain this release for someone building with AI.
> Check the original sources and show what the viewer could actually do with it.

> Use workflow-to-aiox-squad to turn my research, script and claim-review process
> into a reusable squad with explicit input and output for each task.

The script-bearing skills work when copied individually, outside this repo.
Their Python helpers need no dependencies. The source-writing skill can use your
assistant's existing research tools; no paid service or model is bundled.

## Try the skills' executable examples

```bash
python skills/workflow-to-aiox-squad/scripts/scaffold_squad.py \
  skills/workflow-to-aiox-squad/assets/workflow.json --out output/my-squad
python skills/build-video-handoff/scripts/build_packet.py \
  skills/build-video-handoff/assets/example-brief.json --out output/skill-demo
```

All three skills pass the skill frontmatter/scaffold validator. Both the existing
and freshly generated example squads pass the actual upstream strict validator.
Seven tests cover the handoff, invalid inputs, no-overwrite and helpers copied
away from the repository. Full host/LLM execution remains untested.

## Try the working example

Python 3.10+, no dependencies, credentials or network needed:

```bash
python packet.py examples/file-hash.json --out output/hash-demo
python -m unittest discover -s tests -v
```

`packet.py` remains a compatibility command; its implementation now lives with
the portable `build-video-handoff` skill.

The new folder contains `narration.md`, `storyboard.json`, `sources.json`,
`short.json` and a hash receipt. Copy that folder into
[Shorts Studio Starter](https://github.com/aramakam0411-hash/shorts-studio-starter),
then run its renderer on `output/hash-demo/short.json`. Add your own narration
recording before final publication. The example is an authored explanation,
not an AI-generated script or an actual recorded hash application.

## Use with AIOX

Copy `squads/content-studio/` into your existing AIOX project's `squads/` folder.
Use your installed host's squad creator to validate it:

```text
@squad-creator
*validate-squad content-studio --strict
```

Read `squads/content-studio/README.md` for the four tasks. Give your agent the
brief example and ask it to perform research, script, motion plan and review
in order. Fill every source reference and distinguish actual demos from authored
illustrations. Run the deterministic builder after review. You can also use the
same task files with your existing coding assistant without installing AIOX.

The squad passes the actual upstream strict SquadValidator with its schema,
including tasks, agents and file references; local packet
validation and example rendering are tested. Full AIOX host/LLM execution is
not tested in this release. No host install, model service, autonomous delegation
or account connection is performed by this repository.

## Make it yours

Replace the example with your topic, checked sources, narration and visible
actions. Scene source IDs must exist; duration, visual provenance and short
visual steps are required. The builder refuses to overwrite an old output.
It validates structure, not truth, licences, speech timing or retention.

The workflow hands over material; it never posts, emails, spends or invokes a
model. No keys are needed for the offline example. Any host you choose may
require its own account. Generated files are ignored by Git.

## References

Names and layout checked October 25, 2026 against the primary
[AIOX squad guide](https://github.com/SynkraAI/aiox-core/blob/main/docs/guides/squads-guide.md),
[squad schema](https://github.com/SynkraAI/aiox-core/blob/main/.aiox-core/schemas/squad-schema.json)
and [task format](https://github.com/SynkraAI/aiox-core/blob/main/.aiox-core/docs/standards/TASK-FORMAT-SPECIFICATION-V1.md).
The other project named [AIOS](https://github.com/AGIResearch/AIOS) is a distinct
runtime; these files do not claim kernel integration.

Original code/templates: MIT. Linked frameworks keep their own licences.
