# AIOS Content Starter

Turn a sourced idea into a script, shot plan and renderable shorts manifest.
Includes a small original squad for **Synkra AIOX (formerly AIOS)** and an
offline Python handoff builder. This is not AGI Research's AIOS kernel and is
not an official Synkra package.

## Try the working example

Python 3.10+, no dependencies, credentials or network needed:

```bash
python packet.py examples/file-hash.json --out output/hash-demo
python -m unittest discover -s tests -v
```

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
