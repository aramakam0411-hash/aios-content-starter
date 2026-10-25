---
name: workflow-to-aiox-squad
description: Turn a practical workflow into an original Synkra AIOX squad with task files, role definitions and explicit handoffs. Use when someone wants a reusable AIOS/AIOX workflow, not the distinct AGI Research AIOS kernel.
---

# Workflow to AIOX squad

Identify the user's input, desired output and the decisions that require an
agent. Combine steps that share context; keep deterministic transformations in
ordinary scripts. A role definition is not an independently running service.

Write a small workflow JSON following [the complete example](assets/workflow.json).
Each step needs a unique kebab-case `id`, specific `purpose`, and named `inputs`
and `outputs`. Express observable handoffs rather than a list of vague personas.
Preserve the user's chosen tools, permission boundaries and existing work.

From this skill directory, scaffold the task package with Python3.10+:

```bash
python scripts/scaffold_squad.py assets/workflow.json --out output/my-squad
```

The helper makes `squad.yaml`, agents, tasks, a handoff checklist, run order and
a source-hash receipt. No host installation, model call, delegation or publishing
occurs. It refuses an existing folder. Review generated instructions for the
actual workflow; the helper cannot establish that an integration works.

If the user already has Synkra AIOX, copy the generated folder into its existing
`squads/` directory and use that host's squad creator to validate the exact path:

```text
@squad-creator
*validate-squad ./squads/my-squad --strict
```

The schema/task conventions come from the
[upstream squad guide](https://github.com/SynkraAI/aiox-core/blob/main/docs/guides/squads-guide.md).
The bundled example passes the actual upstream strict validator; a generated
different workflow still needs its own validation. Report that separately from
full host execution. If the user means AGI Research AIOS, explain the distinction
and adapt to its actual SDK rather than claiming this squad is kernel compatible.
