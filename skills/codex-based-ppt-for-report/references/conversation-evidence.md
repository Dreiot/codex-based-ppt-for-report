# Conversation evidence workflow

## Scope selection

Use Codex task/thread tools to discover tasks within the user-selected project and time range. Search for task/thread management capabilities such as `list_threads` and `read_thread` before asking the user for identifiers. A time range explicitly selected by the user always overrides defaults. When the user selects the latest 14 days, interpret it as 14 inclusive calendar dates in the user's timezone, ending on the current date, and state the resolved start and end dates. Otherwise prefer the previous report cutoff through the current date. If no cutoff can be established, default to the latest 14 inclusive calendar dates. Always support custom inclusive start and end dates.

Show candidate task titles, dates, and stable task/thread identifiers before reading full task contents. Read only the tasks the user confirms. If task discovery tools are unavailable, ask the user for task links or identifiers; do not substitute filesystem guessing for conversation history. If the available tool cannot expose metadata without also returning full content, disclose that limitation and request permission to read the candidate tasks before calling it. Do not treat unapproved full content returned incidentally by a discovery tool as authorized evidence.

## Preferred repository authorities

For each selected project, identify its repository only from a user-provided
path, an established workspace mapping, task metadata, or an approved task
reference. Do not scan unrelated repositories or require a repository at all.
When the repository is already known, read its preferred files before task
bodies. If the repository becomes identifiable only after reading a confirmed
task, read the files immediately afterward and before synthesizing claims.

Before reading confirmed task bodies, probe these paths in the selected
project and read the ones that exist:

| Preferred file | Authority role | Presentation use |
|---|---|---|
| `AGENTS.md` | Stable operating, data, validation, and claim boundaries | Prevent unsupported access or wording; normally keep it off slides |
| `docs/PROJECT_CORE.md` | Durable strategy, innovations, components, explored directions, evidence position, and scientific boundaries | Frame the project narrative and interpret period changes |
| `docs/CURRENT_STAGE.md` | Current milestone, formal review state, material blockers, and next action | State the present position and immediate next step |

These are preferred inputs, not required files. If none exists, continue with
the normal conversation-first workflow without warning that the project is
noncompliant. If only some exist, use the available files and mark the missing
context internally only when it affects a claim. Never create, migrate, or edit
handoff files during presentation work.

Treat authority by responsibility rather than using one global ordering:

- checked-in `PROJECT_CORE.md` governs the current durable strategy;
- checked-in `CURRENT_STAGE.md` governs the current volatile stage;
- `AGENTS.md` governs stable project boundaries;
- detailed reports, outputs, tests, and figures support specific evidence;
- selected conversations reconstruct chronology, rationale, and artifact
  pointers within the requested reporting period.

If a conversation describes an older direction that is now rejected,
deferred, or superseded in `PROJECT_CORE.md`, it may appear as decision history
but not as the active route. Do not project today's strategic status backward
onto an earlier date. If an authority is stale, internally inconsistent, or in
material conflict with direct checked-in evidence, surface the conflict and
ask the user before making it central.

## Evidence states

Classify every substantive item:

| State | Meaning | Allowed presentation wording |
|---|---|---|
| 已验证 | Implementation or result has direct successful validation evidence | May state as completed and verified |
| 已实现但未验证 | Change exists but final validation is missing or failed to run | State implementation separately from validation gap |
| 计划中 | Proposed future work without completion evidence | Present only as a plan |
| 受阻 | Work stopped on a named dependency or failed gate | Present blocker and next gate |
| 已否决 | Superseded, rejected, or explicitly abandoned | Use only when explaining decision history |
| 待确认 | Evidence is ambiguous, contradictory, or incomplete | Ask the user before making it central |

Do not promote self-reported completion to `已验证` without the validation result. Distinguish a code change, a test run, a successful test, a commit, and a published result.

## Conflict resolution

Build a chronological mini-timeline when two tasks disagree. Prefer the newest state that has direct evidence, but show:

- the conflicting statements;
- their dates and task identifiers;
- the evidence strength;
- the proposed resolution.

Ask the user to resolve conflicts affecting the report's main conclusion. Minor unresolved details may remain visibly labeled `待确认`.

## Local artifact access

Follow canonical-source indexes in an available `PROJECT_CORE.md` and paths
explicitly mentioned in confirmed tasks when necessary to reproduce a figure,
formula, experimental table, or precise change. Read the smallest relevant
scope. Do not scan unrelated projects.

Hide operational noise from slides by default: absolute paths, temporary commands, proxy settings, internal task numbers, and routine tool chatter. Retain versions, commits, seeds, datasets, configurations, failure gates, and validation results when they affect research credibility.

## Transient evidence map format

Create one row per slide:

| Slide | Claim or visual | Source role | Codex source | Canonical/local artifact | Evidence state | Notes |
|---|---|---|---|---|---|---|

Use project name, task title or ID, and message date as the Codex locator. Record exact local artifact paths when used. If a slide contains only navigation or section framing, label it accordingly rather than inventing evidence.

Keep this map as an internal temporary record by default. Persist or deliver it only when the user explicitly requests an evidence map.

For multi-project or long-history runs, follow
[evidence-packets.md](evidence-packets.md). Let project extractors read the
confirmed task bodies and write exact locators so the main agent can work from
compact packets. Packet extraction does not replace direct verification of the
current authorities or central claims.
