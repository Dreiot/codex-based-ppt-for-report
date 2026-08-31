---
name: codex-based-ppt-for-report
description: Create evidence-grounded, editable Chinese research group meeting presentations from user-selected Codex project conversations, available canonical project authorities, and relevant local artifacts. Use for biweekly research updates, method and experiment plans, reviewer-response presentations, milestone summaries, multi-project group meetings, or revisions to an existing group-meeting deck when Codex must select tasks by project and time range, confirm the factual basis before production, distinguish verified progress from plans, explain workflow or formula changes before versus after, obtain outline approval, disclose and use an appropriate presentation-production path, and deliver only the requested PPTX by default or an explicitly requested offline HTML. Prefer AGENTS.md, docs/PROJECT_CORE.md, and docs/CURRENT_STAGE.md when present, but remain fully usable for projects that do not follow that framework.
---

# Codex-Based PPT for Report

Create a defensible presentation from selected Codex task history. Keep content approval separate from visual production. Do not treat plans, hypotheses, or unverified agent claims as completed research.

## Non-negotiable boundaries

- Use only user-approved projects and Codex tasks. Within a selected project,
  prefer available canonical repository authorities and task-referenced local
  artifacts; never require the project to use a particular handoff framework.
- Do not browse for supplementary claims or introduce external evidence without explicit permission.
- Never silently broaden the project, task, or date scope.
- Never overwrite an existing deck unless the user explicitly requests it.
- Require user approval of the evidence summary and slide-by-slide outline before producing the deck.
- Explicitly disclose the final presentation-production path before using it. It may be a `ppt-agent`, built-in presentation tooling, `oil-ppt`, or a clearly described custom workflow.
- Confirm the factual basis before presentation production. Keep the evidence ledger available during production and QA, but do not use production as a substitute for unresolved evidence decisions.
- Deliver only an editable `.pptx` by default, or only an offline editable `.html` when the user explicitly requests HTML. Do not persist evidence maps, QA reports, rendered previews, source projects, inspection dumps, or other supporting artifacts unless the user explicitly requests them.

## Workflow

### 1. Establish the run contract

Ask one compact set of startup questions covering only decisions that cannot be discovered:

1. Select one or more Codex projects.
2. Select the time range: since the previous report cutoff, the latest 14 days, or custom dates.
3. Select the report type:
   - 双周研究进展
   - 论文方法与实验方案
   - 审稿意见与返修计划
   - 阶段成果总结与下一步安排
   - 自定义类型
4. State the expected speaking duration.
5. Confirm a report type and output directory when they cannot be safely inferred from context. Use editable `.pptx` by default; accept offline editable `.html` when explicitly requested. Unless the user specifies another convention, name the final file with the local production date only: `<YYYY-MM-DD>.pptx` or `.html`. If that path already exists and overwrite permission is absent, ask before replacing it.

Identify each selected project's repository only from user-provided paths,
established workspace mappings, task metadata, or approved task references.
When the repository is already known, read the preferred files before task
bodies. If an approved task first reveals the repository, read the files as
soon as it does and before synthesizing the project narrative. Prefer these
files when they exist:

- `AGENTS.md` for stable operating, data, validation, and claim boundaries;
- `docs/PROJECT_CORE.md` for durable research direction, innovations,
  components, explored directions, evidence position, and scientific limits;
- `docs/CURRENT_STAGE.md` for the current milestone, formal review state,
  material blockers, and next action.

These files are preferred context, not prerequisites. If they are absent,
partially present, inaccessible, or clearly not used by the project, continue
with the conversation-evidence workflow. Do not create, migrate, or edit them
as a side effect of making a presentation, and do not scan unrelated
repositories to find them.

List candidate Codex tasks within the selected projects and dates. Let the user confirm which tasks to include before reading their full content. For multiple projects, preserve each project as a separate top-level chapter; do not explain relationships or rank priorities unless requested.

Then recommend a design tendency based on the chosen report type and ask the user to confirm or adjust it. Treat a design tendency explicitly supplied in the user's request as already confirmed; do not ask again.

- 严谨学术型
- 视觉讲解型
- 决策讨论型
- 自定义

Read [references/conversation-evidence.md](references/conversation-evidence.md) before collecting or reconciling evidence.

### 2. Build the evidence ledger

Read available canonical authorities first, then read only the confirmed task
bodies. Follow authority indexes and explicit task references to local
formulas, figures, experiment outputs, source files, reports, or prior decks
when required for fidelity.

For two or more projects, long confirmed task bodies, or a context-sensitive
run, read [references/evidence-packets.md](references/evidence-packets.md) and
prefer parallel evidence extraction. Use one narrowly scoped extractor per
project, at most three concurrently by default. Request `gpt-5.6-luna` with
`medium` reasoning when model selection is available; otherwise use the
fastest suitable subagent. Each extractor reads only its assigned authorities,
confirmed tasks, and referenced artifacts, then writes to a disjoint temporary
project directory. It records exact source locators and uncertainty but does
not decide the final narrative, resolve material conflicts, or promote claims.
If subagents are unavailable, build the same packet serially.

Keep the main agent out of full conversation bodies when a valid packet is
available. The main agent must still verify repository/ref identity, read or
spot-check the current `PROJECT_CORE.md` and `CURRENT_STAGE.md`, and trace every
central or conflicting claim back to its recorded source before approval.

For every candidate claim, record:

- project identity and, when applicable, task identity;
- message date or stable locator;
- source role: canonical strategy, current state, stable boundary, detailed
  evidence, or conversation chronology;
- status: `已验证`, `已实现但未验证`, `计划中`, `受阻`, `已否决`, or `待确认`;
- supporting artifact or validation result;
- whether it changes a workflow, objective function, formula, method, or experiment plan.

Respect each canonical file only within its responsibility. Use
`PROJECT_CORE.md` for the current durable strategy, `CURRENT_STAGE.md` for the
current volatile state, and `AGENTS.md` for stable boundaries. Use selected
tasks to reconstruct the reporting-period chronology and explain changes, not
to silently override checked-in authorities. Prefer newer verified evidence
within the same role, but never silently discard conflicts. Surface material
conflicts and ask the user to resolve any conflict that changes the central
narrative.

Treat the evidence packets and ledger as transient internal working records by
default. Establish them before generation, use them to approve the facts and
audit the deck, and do not save them in the final output directory unless
explicitly requested. Retain them in the temporary run directory until the user
accepts the final presentation, then delete them.

### 3. Prepare content for approval

Read [references/content-architecture.md](references/content-architecture.md). Produce:

1. a concise fact and evidence summary;
2. missing, conflicting, or unverified items;
3. a slide-by-slide outline;
4. a proposed design tendency and estimated slide count.

For a project with `PROJECT_CORE.md`, also summarize the durable research
question, primary direction, innovation and component status, explored-route
decisions, current claim ceiling, and open strategic questions before showing
the reporting-period delta. Do not retroactively present the current strategy
as if it already existed earlier in the selected date range.

Estimate length from speaking time rather than filling a fixed page quota. Use roughly one slide per minute only as a starting point; allocate more time and fewer slides for formulas, mechanism diagrams, and before-after explanations.

For research-progress and milestone presentations, keep the evidence ledger as an internal verification layer. Translate it into an audience-facing research narrative centered on:

`研究方向 → 方法或流程如何调整 → 实验如何组织 → 当前观察与认识 → 下一阶段工作`

Do not place developer-facing state in the main deck by default, including commit hashes, branch names, review verdict codes, implementation candidates, development Gates, CI details, or exhaustive test counts. Include such material only when the user asks for it, when the report type is explicitly about review or engineering governance, or when omitting it would materially misrepresent the research.

Preserve scientifically meaningful uncertainty even when development metadata is omitted. Use concise research-facing wording such as `单数据集阶段性观察`, `尚未开展正式实验`, `仍需更多种子验证`, or `当前结果不足以支持优越性结论` when supported by the evidence.

Every project chapter should default to:

`研究方向 → 流程/公式改动前后及依据 → 实验组织 → 当前结论与适用边界 → 下一步计划`

For multiple projects, use:

`封面 → 目录 → 项目 A 章节过渡 → 项目 A → 项目 B 章节过渡 → 项目 B → … → 本期总结与待讨论问题`

Use concise, natural topic titles for ordinary group-meeting slides. Prefer titles such as `研究动机`, `实验设置`, `阶段性结果`, or a precise method name. Move presenter-like summary sentences, rhetorical framing, and generated-sounding phrases into the slide body or speaker notes. Avoid titles such as `用三条主线回答……`, `三条主线采用同一套研究叙事`, or other complete sentences that describe how the deck was constructed.

Do not start PPT production until the user approves both the fact/evidence summary and the slide-by-slide outline. Resolve central factual conflicts, unsupported conclusions, and material uncertainty before generation; do not defer these decisions to the production or QA stage.

### 4. Select and disclose the production path

Recommend a production path after considering formula editability, visual complexity, available tools, and the user's requested output. State the selected path and why it fits before starting production. Treat a path explicitly selected by the user as confirmed. Otherwise let the user adjust the recommendation.

Allowed paths include:

- `ppt-agent` for specialized planning, visual design, production, rendering, and verification;
- built-in presentation tooling for direct editable PowerPoint creation or modification;
- `oil-ppt` alone for an explicitly requested offline HTML deliverable, or combined with an explicitly disclosed PPTX conversion or reconstruction tool and post-conversion QA for a PPTX deliverable;
- a custom workflow whose tools, editable source, conversion path, and QA method are named explicitly.

For a new research `.pptx`, prefer a callable custom `ppt-agent` as the
production orchestrator; it should use the built-in Presentations tooling as
its PowerPoint engine. Spawn that role only after outline approval and pass the
approved packet paths, output path, note policy, formula-slide list, and QA
contract. This keeps production context isolated while preserving editable
PPTX output. If the role is unavailable, say so and use the built-in tooling
directly after the user accepts that route. Direct production is also suitable
for bounded edits to an existing deck and simple short decks.

For any formula-heavy deck, test one representative equation before full
production. The selected route must demonstrate native Office Math or clean
LaTeX/MathJax SVG/EMF output. Ordinary text boxes using a math font do not
satisfy this test. If the test fails, correct the equation pipeline; using a
different orchestrator does not by itself change the rendering engine. Ask
before changing to a materially different production route.

Do not switch production paths silently. If the selected path is unavailable or fails, report the problem and ask the user to approve the proposed alternative.

### 5. Produce the presentation

After approval, give the selected production path the following source packet without adding unsupported conclusions:

- approved slide outline;
- approved fact/evidence summary;
- evidence ledger and conflict resolutions;
- selected design tendency and user customizations;
- speaking duration and target slide count;
- local artifact paths needed for figures or formulas;
- the rules in [references/design-and-qa.md](references/design-and-qa.md);
- the required output paths.

Require a fully editable 16:9 presentation in the approved format, Chinese academic terminology, full-slide rendering, full-size visual inspection, and revision of visual defects before delivery. Require audience-ready Chinese talk tracks in the speaker notes of every substantive slide when the selected format supports notes. Notes must be written as natural presentation prose that can be spoken directly, not as production instructions, evidence ledgers, or one-line metadata summaries. The skill owner has explicitly selected source-free talk-track notes: keep provenance in the transient evidence packet and pass `do not add [Sources] blocks or source lists to speaker notes` as an explicit user requirement to the production engine. If an engine cannot honor that requirement, report the conflict instead of silently changing the notes policy. If the format cannot store notes, disclose that limitation and obtain approval before production; do not silently omit the talk track.

Apply the following typography defaults to every generated or revised research
deck unless the user explicitly requests a different font system:

- set the East Asian typeface of all visible Chinese presentation text to
  `宋体` (`SimSun`);
- set the Latin typeface of ordinary English letters and Arabic numerals to
  `Times New Roman`, including mixed Chinese-English text, chart labels, slide
  numbers, and table text;
- preserve a proper mathematical typeface inside native Office Math or
  LaTeX/MathJax formula objects instead of forcing Times New Roman onto a
  non-trivial equation and damaging mathematical layout;
- center every table cell horizontally and vertically, including headers,
  row labels, method names, and numeric cells, unless the user explicitly
  approves a different alignment for a specific table.

Implement mixed-script text with separate East Asian and Latin font settings
or run-level formatting rather than relying on application font fallback.
Verify the exported PPTX package and full-size render; setting only an editor
theme or a default font without checking the actual runs is insufficient.

For multiple projects, require a brief chapter divider or an equally explicit visual transition before each new project. Keep the divider simple: project name plus one neutral research-focus subtitle is usually enough.

Render mathematical expressions as mathematics, not programmer-style text.
Use native Office Math when it can be created and rendered reliably; otherwise
use LaTeX/MathJax SVG or EMF and retain the exact source expression in the
temporary production files. Do not build non-trivial display equations from
ordinary text boxes, even with Cambria Math. Keep Chinese explanations outside
the equation and use symbolic terms inside it. Never present core equations
with raw underscores, improvised Unicode spacing, flattened scripts, or text
standing in for mathematical subscripts when proper fractions, norms, traces,
transposes, Greek symbols, and operator spacing are available.
Set each vector equation picture's alt text to `Equation: <source-id>` so the
package audit can distinguish equations from logos and decorative SVG assets.

Preserve every formula's natural aspect ratio. For SVG formulas, include `preserveAspectRatio="xMidYMid meet"`, parse the SVG `viewBox`, compute one uniform scale with `min(slotWidth / viewBoxWidth, slotHeight / viewBoxHeight)`, and center the resulting object in its allotted slot. Never stretch a formula by independently forcing both its width and height to the slot dimensions. After export, compare the formula's natural aspect ratio with its displayed object frame and require at most 1% relative error, then visually inspect every formula-heavy slide for stretching, clipping, blur, font substitution, and misplaced subscripts or superscripts.

Keep internal provenance, review, and validation details in the transient evidence ledger or internal QA record unless they are explicitly part of the approved slide outline. Persist those records only when requested. Do not let implementation bookkeeping displace the research question, experiment design, observations, or next-stage plan.

The design must vary with content. Keep the approved white, dark-gray, restrained-deep-blue baseline, but do not repeat one table/card layout across the deck. Prefer diagrams, plots, experimental figures, and formula explanations when they communicate the evidence better. Do not retain third-party template branding such as `Made with GAMMA`.

### 6. Audit and deliver

Independently verify the production outputs against the approved outline and evidence ledger. Require all checks in [references/design-and-qa.md](references/design-and-qa.md).

Run the deterministic package audit before delivery:

```text
<python> <skill-dir>/scripts/audit_pptx.py <final.pptx> \
  --formula-slides <comma-separated slide numbers or none> \
  --inline-math-slides <intentional simple inline-math slides or none> \
  --brief-note-slides <title/divider slides allowed brief notes or none>
```

Treat missing notes, `[Sources]` blocks, production-instruction notes, or
unapproved brief notes, undeclared formula text, or text-only approximations of
non-trivial display equations as failures. Do not use inline-math exceptions on
declared display-formula slides. Use allow flags only for deliberate exceptions
that remain consistent with the approved outline.

Perform the full audit even though supporting records are not default deliverables. Keep the evidence packets, ledger, renderings, inspection output, and QA results in an operating-system temporary directory or another clearly separated staging area. Keep them available for corrections during user acceptance, then remove them after the user accepts the presentation. Do not delete the only trace needed to correct a rejected draft.

Mark each temporary run with its creation time. At the start of a later run,
remove abandoned run directories older than 14 days only when they are inside
this skill's dedicated temporary root, `retain_requested` is false, and they
contain no user-requested deliverable.

Deliver exactly one default artifact:

- `<YYYY-MM-DD>.pptx`

When the user explicitly selects offline HTML, deliver only `<YYYY-MM-DD>.html` and adapt format-specific QA accordingly. Persist an evidence map, QA report, rendered slides, editable source project, or inspection data only when the user explicitly requests that artifact.

Report any check that did not run and the substitute evidence used. Never describe a skipped check as passed.
