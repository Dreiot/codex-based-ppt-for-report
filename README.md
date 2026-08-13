<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="Codex-Based PPT for Report：从 Codex 项目对话到有事实依据的研究汇报 PPT">
</p>

<p align="center">
  <strong>把选定的 Codex 项目对话，转化为有事实边界、可编辑、可讲述的中文研究汇报。</strong>
</p>

<p align="center">
  双周研究进展 · 方法与实验方案 · 审稿返修计划 · 阶段成果总结 · 多项目组会
</p>

## 它解决什么

科研项目的进展通常散落在多个 Codex 任务中：方法为什么修改、实验怎样组织、哪些结果已经验证、哪些仍是计划。`codex-based-ppt-for-report` 先限定对话与时间范围，再确认事实依据和逐页结构，最后才进入演示文稿制作。

它不是把聊天记录压缩成幻灯片，而是把研究过程整理为一条可讲述的主线：

> 研究方向 → 修改内容与依据 → 实验组织 → 当前认识与边界 → 下一阶段工作

<p align="center">
  <img src="./assets/readme/workflow.svg" width="100%" alt="从选择 Codex 项目任务、确认事实依据和逐页大纲，到生成并验收 PPTX 的工作流">
</p>

## 核心原则

| 原则 | 具体行为 |
| --- | --- |
| 事实先于制作 | 先确认项目、日期、任务、事实摘要与冲突项，再生成演示文稿。 |
| 优先项目权威 | 若仓库提供 `AGENTS.md`、`PROJECT_CORE.md` 和 `CURRENT_STAGE.md`，先用它们确定边界、长期战略与当前状态；缺失时正常回退。 |
| 并行精简证据 | 多项目或长对话默认由 Luna 等轻量子代理按项目提取临时证据包，主代理只复核权威状态和关键 claim。 |
| 内容先于视觉 | 逐页大纲需要先获确认；不会让版式反过来决定研究结论。 |
| 研究语言面向听众 | 默认不把提交号、审查代码、开发门控和流水线细节堆进正文。 |
| 改动必须解释清楚 | 流程、目标函数、公式或实验方案发生变化时，说明修改前、修改后、依据、核心区别与影响。 |
| 公式必须可靠 | 非平凡展示公式使用 Office Math 或 LaTeX/MathJax 矢量对象，不用普通文本框模拟；导出后逐符号核对。 |
| 备注就是汇报稿 | 实质页备注写成可直接照讲的中文讲稿；来源留在临时证据包，默认不写 `[Sources]`。 |
| 多项目保持分章 | 每个项目是独立大章节，并在切换前加入明确而简洁的过渡页。 |
| 默认只留下成品 | 内部仍会完成证据核对、逐页渲染与 QA；除非明确要求，最终目录只保存 PPTX。 |

## 快速开始

将 Skill 复制到 Codex Skills 目录：

```powershell
Copy-Item -Recurse -Force `
  '.\skills\codex-based-ppt-for-report' `
  "$env:USERPROFILE\.codex\skills\codex-based-ppt-for-report"
```

推荐同时安装仓库提供的两个 Agent。若目标路径已有自行定制的同名配置，
先备份或合并差异，再使用 `-Force`：

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\agents" | Out-Null
Copy-Item -Force '.\agents\ppt-agent.toml' "$env:USERPROFILE\.codex\agents\ppt-agent.toml"
Copy-Item -Force '.\agents\ppt-evidence-extractor.toml' "$env:USERPROFILE\.codex\agents\ppt-evidence-extractor.toml"
```

- `ppt-agent`：使用较强推理，负责已批准内容的视觉制作、公式路径、渲染与验收。
- `ppt-evidence-extractor`：默认使用 `gpt-5.6-luna / medium`，按项目生成精简证据包。该配置要求当前账户能够使用 Luna；若不可用，不安装此配置，Skill 会改用其他合适的快速子代理或串行提取。

Agent 不固定 sandbox，会继承父任务的权限；用户选择的临时目录和最终输出目录必须位于父任务可写范围。安装或更新 Agent 后重启 Codex。没有安装这些 Agent 时，Skill 仍可串行提取证据；若需要从 PPT Agent 切换为直接使用内置 Presentations，必须先说明路径变化并获得用户同意。

重新打开相关 Codex 任务后，显式调用：

```text
$codex-based-ppt-for-report
```

一个完整请求可以这样写：

```text
使用 $codex-based-ppt-for-report，根据 TFS TSK-Ising 与 UC-FCM+ACSLL
两个 Codex 项目最近 14 天的对话，制作一份 20 分钟双周研究进展汇报。
重点说明目标函数和关键公式修改前后、修改依据与影响，采用视觉讲解型。
```

## 推荐搭配：Codex Research Workflow

本 Skill 可以独立使用，不要求仓库采用特定治理框架。对于长期科研项目，推荐搭配
[Dreiot/codex-research-workflow](https://github.com/Dreiot/codex-research-workflow)：

- `AGENTS.md` 保存稳定的操作、数据、验证与 claim 边界；
- `docs/PROJECT_CORE.md` 保存研究问题、主方向、创新、组件、探索历史和证据位置；
- `docs/CURRENT_STAGE.md` 保存当前里程碑、阻塞项和下一动作。

当仓库已能识别且这些文件存在时，本 Skill 会优先读取它们；若仓库路径只能从已确认
的任务正文获得，则在路径出现后、综合叙事前读取。随后用 `PROJECT_CORE.md` 建立项目
叙事，再用选定对话说明汇报周期内发生的变化。文件缺失、
部分缺失或仓库未采用该框架时，会自动回退到原有的对话与 artifact 证据流程，不会
创建文件，也不会阻止 PPT 制作。

## 默认工作方式

1. 确认一个或多个 Codex 项目、时间范围、汇报类型和预计时长。
2. 优先读取已选项目中现有的三份权威文件；若不存在则直接继续。
3. 列出候选 Codex 任务，仅在用户确认后读取任务正文。
4. 多项目或长对话时，每个项目由一个轻量子代理生成独立临时证据包；主代理复核权威文件和关键 claim。
5. 建立证据台账，区分权威角色以及已验证、未验证、计划、受阻、否决和待确认内容。
6. 提交事实摘要、冲突项与逐页大纲，等待确认。
7. 新建科研 PPTX 默认由 PPT Agent 隔离生产上下文并统筹制作，底层仍使用内置 Presentations；局部修改或简单短稿可以直接使用内置工具。公式较多时先试制一条代表性公式。
8. 生成演示文稿，为实质页写入可直接使用的中文汇报稿备注，完成逐页渲染和 PPTX 包审计。
9. 默认只交付 `<YYYY-MM-DD>.pptx`；临时证据包在用户验收后删除。

## 支持的汇报类型

- **双周研究进展**：研究方向、方法调整、实验组织、阶段性认识与下一周期计划。
- **论文方法与实验方案**：研究问题、方法机制、目标函数、实验设计与预期证据。
- **审稿意见与返修计划**：审稿问题、响应策略、证据、风险与后续动作。
- **阶段成果总结与下一步安排**：里程碑、已形成的认识、剩余缺口与决策点。
- **自定义汇报**：依据用途重新组织结构，同时保留事实边界与改动说明。

## 公式与视觉质量

公式优先使用 Office Math；能力受限时使用 LaTeX 或 MathJax 生成的 SVG/EMF。非平凡展示公式不得使用普通文本框和数学字体近似，矢量公式需要以 `Equation:` alt text 标记。SVG 必须使用 `preserveAspectRatio="xMidYMid meet"`，按 `viewBox` 计算单一缩放系数并居中。导出后检查自然宽高比与显示宽高比，允许的相对误差不超过 1%，并与权威公式逐符号核对。最终审计显式声明展示公式页、简单行内数学页和允许简短备注的封面/章节页，避免无关 SVG 或页码造成误判。

每张实质页的 speaker notes 默认写成自然、连贯、可直接照讲的中文汇报稿，包含本页结论、视觉讲解顺序、证据边界和过渡。来源信息保存在临时证据包，不在备注中附加 `[Sources]`，除非用户明确要求。

所有页面都需要渲染后检查。标题采用简洁、自然的主题型表达；讲述句和汇报组织说明进入正文或演讲者备注。设计以白底、深灰和克制深蓝为基线，但可根据严谨学术型、视觉讲解型、决策讨论型或自定义倾向调整。

`ppt-agent` 与内置 Presentations 不是互斥引擎：前者负责隔离上下文、叙事编排、公式路径和逐页验收，后者负责实际创建和修改 PPTX。新建、多项目或公式密集型科研汇报默认采用两者组合；直接调用内置工具更适合局部修改和结构简单的短稿。

## 默认交付

```text
<YYYY-MM-DD>.pptx
```

用户明确选择离线 HTML 时，只交付对应的 `.html`。证据映射、QA 报告、渲染图、检查数据和源工程只在明确要求时保存。

## 项目结构

```text
agents/
├── ppt-agent.toml
└── ppt-evidence-extractor.toml

skills/codex-based-ppt-for-report/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   └── audit_pptx.py
└── references/
    ├── conversation-evidence.md
    ├── content-architecture.md
    ├── evidence-packets.md
    └── design-and-qa.md
```

README 视觉资源位于 `assets/readme/`。Skill 本体保持精简，只包含执行工作流所需的说明与参考文件。

`tests/test_audit_pptx.py` 覆盖页面重排后的备注关系、无关矢量图、简单公式识别以及公式页中残留文本公式等边界。

## 使用边界

- 只处理用户确认的项目和 Codex 任务；可优先读取已选项目中现有的三份权威文件及其必要索引，不扫描无关仓库。
- 不在未获允许时引入外部资料或扩大项目、任务与日期范围。
- 不把计划、假设或代理自述误写成已经完成并验证的研究结论。
- 不在未获明确许可时覆盖已有演示文稿。
- 任何未执行的检查都必须如实说明，不能写成已通过。
