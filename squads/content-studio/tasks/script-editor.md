# Script Editor

task: script_editor()
responsável: script-editor
responsavel_type: Agente
atomic_layer: Content

**Entrada:**
- campo: topic-and-prior-handoff
  tipo: object
  origem: user brief or preceding task
  obrigatório: true

**Saída:**
- campo: reviewed-brief-section
  tipo: object
  destino: next task and packet.py
  persistido: true

**Checklist:**
  pre-conditions:
    - [ ] Viewer question and available source ledger are explicit.
      tipo: pre-condition
      blocker: true
      validação: Read the supplied brief and source URLs.
  post-conditions:
    - [ ] Output records evidence, limits and actual tool use.
      tipo: post-condition
      blocker: true
      validação: Compare claims to the source ledger.
  acceptance-criteria:
    - [ ] No unsupported claims, hidden dependencies or invented demonstrations.
      tipo: acceptance
      blocker: true
      validação: Independent final review before packet handoff.

## Work

Write a short clear explanation answering the viewer question. Every factual scene must cite an existing source ID. Keep uncertainty and limits. Provide natural narration without inventing results.

Use examples/file-hash.json from the repository root. Fill the corresponding fields in a copy of that
brief. Do not invoke new services, delegate, publish or spend without the user's
authorization. If a required capability is missing, state what remains untested.
