# Parallel evidence packets

Use this workflow to protect the main presentation context when the user
selects multiple projects or long Codex task histories.

## Extraction topology

- Assign one extractor to one project; do not split one project across agents
  unless its confirmed task set is exceptionally large.
- Run at most three extractors concurrently by default.
- Prefer `gpt-5.6-luna` with `medium` reasoning for narrow extraction work when
  model selection is available.
- Give each extractor only the approved project, inclusive date range,
  confirmed task IDs, repository/ref, authority paths, and a unique output
  directory.
- Extractors may read evidence and write their packet. They must not modify a
  repository, select the final story, resolve scientific conflicts, or create
  presentation slides.

## Temporary layout

```text
<temp>/ppt-report/<run-id>/
├── run-manifest.json
└── <project>/
    ├── project-brief.md
    ├── evidence-ledger.jsonl
    └── artifact-index.md
```

`project-brief.md` records:

- repository, branch/ref, authority paths, and authority blob hashes;
- research question, current direction, innovation/component status, explored
  route decisions, claim ceiling, current stage, and next action;
- reporting-period timeline and the smallest useful presentation delta;
- unresolved conflicts, missing evidence, and recommended source spot-checks.

`evidence-ledger.jsonl` uses one JSON object per claim or visual:

```json
{"claim_id":"P1-C01","claim":"...","status":"已验证","source_role":"detailed_evidence","source_locator":"task/thread + date or file + section","artifact":"path or null","period_relevance":"new|context|superseded","uncertainty":null}
```

`artifact-index.md` lists only artifacts needed for the deck, including formula
sources, figures, tables, experiment outputs, and earlier slides worth reusing.
Record why each artifact matters and whether it was opened or only referenced.

## Main-agent validation

The main agent reads the compact packets instead of full task bodies, then:

1. verifies repository/ref and authority blob identity;
2. spot-checks the current strategy and state directly;
3. traces every central, surprising, or conflicting claim to its locator;
4. asks the user to resolve conflicts that change the narrative;
5. approves the evidence summary and outline before production.

Do not treat agreement between extractors as independent scientific evidence.
Packet extraction is context management, not peer review.

## Retention

Keep packets outside repositories and outside the final output directory. Keep
them through draft correction and user acceptance. Delete the run directory
after the user accepts the final presentation unless the user asks to retain a
packet or evidence map. Record `created_at`, `retain_requested`, `accepted_at`,
and `expires_at` in `run-manifest.json`. Set `retain_requested=true` whenever
the user asks to keep any packet or evidence map. At the start of a later run,
remove abandoned directories older than 14 days only when they are under this
skill's dedicated temporary root, `retain_requested=false`, and contain no
user-requested deliverable.
