# Content architecture and change explanation

## Report-type emphasis

### 双周研究进展

Emphasize the research direction, why the method or workflow changed, how experiments were organized, what can currently be concluded, what remains scientifically uncertain, and the next two-week plan. Keep routine development bookkeeping out of the main narrative unless it changes the scientific interpretation.

### 论文方法与实验方案

Emphasize research question, method mechanism, objective function, optimization or implementation flow, experiment design, expected evidence, and unresolved assumptions.

### 审稿意见与返修计划

Map each reviewer concern to the underlying issue, planned or completed response, evidence, manuscript location, risk, and next action. Never state that a concern is resolved without evidence.

### 阶段成果总结与下一步安排

Emphasize milestone goals, accumulated verified outcomes, remaining gaps, decision points, and the next-stage plan.

### 自定义类型

Derive a structure from the user's stated purpose while preserving evidence states and change explanations.

## Canonical project context when available

When a selected project contains the optional three-file authority model, use
it to establish the research narrative before interpreting the selected
conversation period:

- `PROJECT_CORE.md` `Research Objective` and `Core Direction` frame the chapter
  opening and research question;
- `Innovation Hypotheses` and `Component Map` ground method, mechanism,
  architecture, and formula slides;
- `Explored Directions` explains why routes were accepted, rejected, deferred,
  or superseded when that history is useful to the audience;
- `Evidence and Claim Position` and `Scientific Boundaries` constrain result
  wording, uncertainty, limitations, and the current claim ceiling;
- `Open Strategic Questions` and `Strategic Roadmap` inform longer-term plans,
  while `CURRENT_STAGE.md` supplies the immediate milestone and next action;
- `Canonical Sources` provides targeted artifact and report pointers.

Use `AGENTS.md` internally for stable data, validation, and claim boundaries;
do not turn operating rules into slide content unless the presentation is
about governance or the boundary materially changes the scientific meaning.

The three files are optional. When unavailable, derive the same audience
questions from approved conversation evidence and task-referenced artifacts.
Do not invent a missing strategy, component status, evidence level, or claim
boundary. Do not expose authority filenames or schema fields on ordinary
research slides.

## Audience-facing research narrative

Maintain a detailed evidence ledger during preparation, but do not reproduce it mechanically on slides. For ordinary research updates, translate provenance and implementation state into a concise narrative:

`研究方向 → 修改内容与依据 → 实验组织 → 当前观察与认识 → 适用边界 → 下一阶段工作`

By default, omit developer-facing details from the main deck:

- commit hashes, branch names, and exact diff ranges;
- review-verdict codes and implementation-candidate labels;
- development Gates, internal stage identifiers, and workflow bookkeeping;
- CI logs and exhaustive test-count inventories.

Retain these details in the transient evidence ledger or internal QA record. Persist those records only when the user requests them. Show the details on slides only when the user requests them, the presentation is specifically about review or engineering governance, or the detail is essential to explain why a result can or cannot be trusted.

Do not confuse simplification with overclaiming. Replace internal status labels with research-facing boundary statements supported by evidence, for example:

- `当前为单数据集、单种子的阶段性观察`;
- `正式外部实验尚未开展`;
- `现有结果用于验证流程一致性，不用于证明性能优越性`;
- `该结论仍需更多数据集、随机种子或对照实验验证`.

For multi-project progress reports, keep each project as a separate top-level chapter and give each chapter the same four audience questions:

1. 当前研究方向是什么？
2. 实验或方法为什么这样调整，具体如何组织？
3. 目前观察到了什么，能够和不能够得出什么结论？
4. 下一阶段准备做什么？

## Slide titles and project transitions

Default to concise topic-led titles for research group meetings. A title should name the slide's scientific subject, not narrate the author's presentation strategy.

Prefer:

- `SampleBalanced研究动机`;
- `Caltech101-7实验设置`;
- `平均损失目标函数`;
- `阶段性认识与下一步`.

Avoid generated-sounding titles such as `用三条研究主线回答为什么改、怎样验证、目前知道什么` or `三条主线采用同一套研究叙事`. Put this kind of framing in speaker notes or, when genuinely useful to the audience, in a short body takeaway.

In a multi-project deck, insert a brief chapter transition before each project. Use the project name and, optionally, one neutral research-focus subtitle. Do not jump directly from the last technical slide of one project into the first technical slide of another.

## Mandatory change analysis

Check every report for material changes to:

- research or engineering workflow;
- objective function or its core representation;
- key formula, constraint, or optimization step;
- method architecture or mechanism;
- experiment protocol, dataset processing, metric, or validation gate.

If a material change exists, show:

1. 修改前：the previous workflow, representation, or formula;
2. 修改后：the current version;
3. 修改依据：the observed problem, theoretical reason, experimental evidence, review feedback, or implementation constraint;
4. 核心区别：what was added, removed, replaced, relaxed, constrained, or reordered;
5. 影响：what the change enables, fixes, risks, or still leaves unverified.

If no material change exists, explicitly state `本期无流程或核心表示变更` in the evidence summary. Do not force a comparison slide when it adds no value.

## Formula presentation

- Reconstruct core equations clearly; do not use blurry screenshots.
- Preserve notation from the source. Never invent missing terms or silently normalize inconsistent symbols.
- Typeset formulas as mathematics. Do not expose source-code notation such as `eta_SB`, `lambda_L0_mean`, or raw underscore-based subscripts in visible equations when proper mathematical notation can be rendered.
- Prefer native editable equation objects. When the production tool cannot create them reliably, generate high-resolution SVG from LaTeX or MathJax and preserve the LaTeX source in the editable production source or speaker notes.
- Verify fractions, subscripts, superscripts, matrix transposes, norms, traces, Greek letters, and operator spacing in the final rendered slide.
- Compare before and after side by side or through a progressive reveal.
- Highlight only the changed terms using restrained color and annotations.
- Explain every changed term and symbol in Chinese.
- Split long derivations into `总体目标 → 关键子项 → 优化影响`.
- Prefer editable equations. Use high-resolution vector output only when editable rendering is unreliable.
- Pair a formula with a mechanism diagram or plain-Chinese interpretation when the audience needs intuition.

## Chinese terminology

Use Chinese in the body. On first occurrence, write `中文名称（English Full Name，ABBR）`; afterwards use Chinese or the established abbreviation. Keep official method names, algorithm names, dataset names, journal names, and product names unchanged when translation would reduce precision.

Give every formula symbol a Chinese meaning. Avoid untranslated process labels such as `pipeline`, `baseline`, or `ablation` when established Chinese terms exist; use `流程`, `基线方法`, and `消融实验`.

## Speaker notes

Add concise notes to every substantive slide when the approved presentation format supports speaker notes:

- one-sentence takeaway;
- recommended speaking order;
- change rationale or evidence that must be emphasized;
- likely advisor question or caveat;
- suggested time allocation when useful.

Do not hide essential evidence only in notes.

If the approved format cannot store speaker notes, disclose the limitation before production, obtain the user's approval, and record the agreed substitute in the internal QA record. Persist that record only when requested. Do not silently omit notes.
