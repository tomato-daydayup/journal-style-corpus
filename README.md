# Journal Style Corpus

Build a reusable, evidence-based journal writing guide from a folder of article PDFs—without fine-tuning a model and without repeatedly loading the whole corpus into chat.

`journal-style-corpus` is a Codex skill for turning an already prepared PDF corpus into:

- an audited article registry;
- clean, section-level prose files;
- a target-specific rhetorical-move codebook;
- persistent paragraph-level coding;
- coverage, sequence, transition, and method-variant statistics;
- a versioned writing guide;
- an independent Holdout validation report;
- and, optionally, a traceable manuscript-diagnosis and revision workflow.

The skill is journal- and discipline-agnostic. It does not impose a fixed JIBS or IMRaD template: modules, rhetorical moves, and method-specific variants are learned from each target corpus.

> **Scope:** the user supplies a local folder containing PDFs that have already been obtained. PDF scraping, publisher crawling, authentication, and downloading are intentionally outside this skill.

## Why this exists

Academic writers often want Codex to “learn” how a target journal communicates contributions, develops theory, reports methods and results, and frames implications. Sending dozens or hundreds of complete PDFs into one prompt is expensive, hard to reproduce, and prone to hidden leakage between development and evaluation data.

This skill treats the task as **persistent corpus analysis**, not model fine-tuning:

1. article prose is processed once;
2. paragraph functions are saved as durable structured data;
3. cumulative statistics are recomputed deterministically;
4. the guide is updated only at declared checkpoints;
5. a preassigned Holdout remains unopened until the guide and evaluation protocol are frozen;
6. future manuscript work loads the validated guide, not the original article corpus.

This makes a large corpus usable across multiple Codex chats while reducing token use, preserving provenance, and limiting accidental copying.

## Install

Clone the repository into the Codex skills directory:

```bash
git clone https://github.com/tomato-daydayup/journal-style-corpus.git \
  ~/.codex/skills/journal-style-corpus
```

If the directory already exists, update it from the repository instead of cloning over it.

## Quick start

Prepare the journal PDFs yourself, then invoke the skill in Codex:

```text
Use $journal-style-corpus.
My prepared PDF folder is: /absolute/path/to/journal-pdfs
```

Codex will first inspect the folder read-only. It will report PDF count, nested folders, duplicates, invalid files, naming patterns, and any adjacent BibTeX/RIS/CSV metadata. It then proposes a corpus-size-appropriate plan and asks before starting each mutating stage.

If no folder is supplied, the skill asks only for that path. It does not ask the user to design the entire corpus workflow in advance.

## Workflow

The precise gates adapt to corpus size and discipline, but the dependency order remains stable.

### 1. Read-only preflight

Inventory PDFs, detect byte-identical duplicates and basename collisions, locate existing metadata exports, and determine whether the folder mixes journals or article genres. Source PDFs remain unchanged.

### 2. Project initialization and registry

Create a separate project workspace and a canonical registry containing citation key, title, journal, year, article type, PDF provenance, method/design metadata, split, batch, codebook version, and processing status.

### 3. Genre and method audit

Normalize article types before sampling. Classify method/design through a metadata-first evidence funnel: structured metadata and abstracts first, targeted PDF snippets only when necessary, and compact Codex adjudication for unresolved cases.

### 4. Development/Holdout split

Split before inducing writing rules. Balance by dimensions likely to affect rhetoric, such as method family, article genre, or editorial period. Holdout papers never enter development to increase sample size.

### 5. Pilot extraction and QA

Extract representative articles, verify section boundaries visually, merge only soft line wraps, preserve paragraph boundaries, and remove footnotes, affiliations, editorial notes, tables, equations, headers, and publisher residue from prose analysis.

### 6. Development extraction

Apply verified rules to Development only. Persist full-text provenance, clean module files, page ranges, extraction engine, confidence, and article-specific exceptions.

### 7. Move-code induction

Induce rhetorical moves from what paragraphs do for the reader—not from keywords alone. Define one primary move, optional secondary moves, inclusion cues, exclusion boundaries, and method-specific variants.

### 8. Calibration and codebook lock

Test and refine the provisional codebook on a balanced calibration cohort. Once locked, later batches cannot silently alter definitions. Candidate new moves require a documented version migration and targeted retrospective recoding.

### 9. Persistent batch coding

Process each Development batch once and save paragraph-level coding, excluded-noise logs, QA flags, transitions, citation roles, tense/voice signals, and research links. Merge only new rows into cumulative data.

### 10. Stability analysis and guide checkpoints

Calculate article coverage, normalized first position, adjacent transitions, recurring sequences, and method-group differences. Between formal checkpoints, create lightweight guide-delta packets instead of regenerating the full guide or reopening historical prose.

### 11. Freeze the Development guide

Create a versioned guide containing evidence tiers, reader questions, module architectures, paragraph microstructures, method variants, semantic-slot templates, anti-patterns, checklists, and a Codex drafting/revision protocol. Freeze the codebook, guide, evaluation questions, thresholds, and file hashes before opening Holdout.

### 12. Independent Holdout validation

Extract and code only the preassigned Holdout with frozen rules. Compare move coverage, tier agreement, first positions, transitions, method variants, QA burden, and codebook recoverability. Record misses without immediately changing the guide.

### 13. Validation decision

Preserve the frozen guide, mark it validated with caveats, or—only with explicit authorization—create a separately versioned post-validation guide. Never overwrite the pre-Holdout version.

### 14. Optional manuscript revision

Use only the named frozen/validated guide plus the manuscript. Diagnose paragraph functions before rewriting, preserve claims, evidence, citations, equations, labels, numerical results, and calibrated certainty, and save rule-linked revision logs and author queries.

## Persistent, incremental corpus learning

For approximately 50 or more papers, the skill switches to large-corpus incremental mode. A typical 200-paper design might use:

- a diverse Pilot to induce moves;
- a Calibration cohort to stabilize and lock the codebook;
- bounded Scale batches processed once;
- and an untouched Holdout for independent validation.

Durable project files—not chat history—become the source of truth:

```text
corpus-root/
├── 00_pdfs/                    # immutable source pointer/copies
├── 01_registry/                # audit, registry, split, batch plan
├── 02_extracted/               # extraction provenance
├── 03_sections/                # clean analysis modules
├── 04_style_analysis/
│   ├── codebooks/              # provisional and locked codebooks
│   ├── batches/                # one coding file per batch
│   ├── cumulative_statistics/  # deterministic cumulative evidence
│   ├── guide_deltas/           # changes since prior checkpoint
│   └── qa/                     # noise and review decisions
├── 05_guides/                  # checkpoint and frozen guides
├── 06_holdout_validation/      # validation-only outputs
└── scripts/                    # rerunnable corpus-specific code
```

A new Codex chat can load the current batch, locked codebook, ledger, and cumulative summaries rather than hundreds of old PDFs. This is what “persistent training” means here: the corpus-derived representation and guide evolve on disk. The underlying model weights are not fine-tuned.

## Example: JIBS regular research-article guide

The workflow was used on a corpus of 190 regular `Article` papers from the *Journal of International Business Studies* (JIBS). The goal was to learn rhetorical patterns across quantitative, qualitative, conceptual, and mixed-methods research while keeping an independent validation set.

### Design

- 152 Development articles:
  - 12 Pilot;
  - 28 Calibration;
  - 112 Scale, processed in bounded batches.
- 38 untouched Holdout articles.
- Five analysis modules: Introduction, Theory, Method, Results, and Discussion.
- One locked target-specific codebook containing 36 rhetorical moves.

### Development output

- 10,682 Development prose paragraphs coded.
- 1,196 non-prose or contaminated units excluded.
- A frozen guide with Core/Common/Optional/Rare evidence tiers, module architectures, method-specific variants, semantic-slot templates, and drafting/revision checklists.
- Earlier N=80 and N=120 checkpoint guides preserved rather than overwritten.

### Holdout result

- 38/38 Holdout papers processed.
- 177 formal module files and 2,644 prose paragraphs.
- 100% locked-codebook recoverability under the predefined review rule.
- 16/18 Development Core moves remained Core.
- 31/36 move tiers matched exactly; five shifted by one tier; none shifted by two or more tiers.
- 33/36 moves showed close coverage replication; three showed moderate deviation; none crossed the material coverage threshold.
- Top-five transition structure replicated closely in all five modules.
- No new rhetorical move was required.

The final decision was to preserve the frozen guide and mark it **Holdout validated with caveats**, rather than revise it to fit the Holdout. For example, qualitative Results treated the qualitative-evidence move as design-specific Core even though it was Rare in the all-design denominator. Position differences were retained as caveats instead of being turned into rigid paragraph-order rules.

No source articles, extracted article text, or full project-specific guide are included in this repository.

## Included resources

- `SKILL.md`: core routing, workflow, invariants, and manuscript application rules.
- `references/onboarding.md`: PDF-folder-first intake and staged planning.
- `references/workflow.md`: extraction, QA, move induction, guide, and validation details.
- `references/large-corpus.md`: persistent batch processing and token discipline.
- `references/move-analysis.md`: functional coding and stability interpretation.
- `references/schemas.md`: registries, coding tables, validation, and revision schemas.
- `references/manuscript-revision.md`: diagnosis, priority rules, revision logs, and preservation audit.
- `scripts/init_journal_corpus.py`: initialize a corpus workspace.
- `scripts/manage_incremental_corpus.py`: plan and merge incremental batches.
- `scripts/validate_style_corpus.py`: validate module coverage, noise, and Holdout isolation.
- `scripts/analyze_move_coding.py`: calculate article coverage and transition statistics.

## Important boundaries

- This is corpus analysis, not causal evidence about publication success.
- Frequency does not automatically become a writing rule; recommendations also need a reader-facing rationale.
- Automated coding is a first pass and does not imply human intercoder reliability.
- Corpus papers govern rhetorical choices, not manuscript claims or findings.
- The skill does not copy corpus sentences into new manuscripts.
- PDF acquisition and scraping are out of scope.

---

# Journal Style Corpus（中文说明）

从一个已经准备好的期刊论文 PDF 文件夹出发，建立可复用、可验证、可持续更新的期刊写作指南——不需要微调模型，也不需要在每次对话中重新读取整个语料库。

`journal-style-corpus` 是一个 Codex skill，可以把本地 PDF 语料转换为：

- 经过审计的论文注册表；
- 按模块清洗的正文文件；
- 针对目标期刊归纳的修辞 move codebook；
- 可持久保存的段落级编码；
- move 覆盖率、顺序、转移和方法类型差异统计；
- 版本化的写作指南；
- 独立的 Holdout 验证报告；
- 以及可选的论文诊断、逐节修改和修改日志工作流。

这个 skill 不限定学科，也不会把 JIBS 或 IMRaD 模板强加给其他期刊。模块、move 和方法类型变体都需要从用户提供的目标语料中归纳。

> **使用边界：**用户需要先自行准备本地 PDF。论文抓取、出版社爬虫、登录认证和 PDF 下载不属于本 skill。

## 为什么需要这个 skill

研究者常希望 Codex “学习”目标期刊如何建立研究问题、发展理论、报告方法与结果，以及表达理论贡献。但把几十或几百篇完整 PDF 一次性放入提示词，既消耗 token，也难以复现，还容易造成 Development 与验证语料之间的隐性泄漏。

本 skill 将任务视为**可持久化的语料分析**，而不是模型微调：

1. 每篇文章正文只需处理一次；
2. 段落功能被保存为结构化、可复用的数据；
3. 累积统计由脚本确定性重算；
4. 只有在预定检查点才更新完整指南；
5. Holdout 在指南、评价问题和阈值冻结前保持封存；
6. 后续论文修改只加载验证后的指南，不再读取原始语料论文。

因此，即使跨多个 Codex 对话，也可以继续在磁盘上的同一套注册表、编码、统计和版本指南上工作，同时减少 token 消耗、保留证据来源，并降低文本复制风险。

## 安装

将仓库克隆到 Codex skills 目录：

```bash
git clone https://github.com/tomato-daydayup/journal-style-corpus.git \
  ~/.codex/skills/journal-style-corpus
```

如果该目录已经存在，应更新现有仓库，而不是直接覆盖或再次克隆。

## 快速开始

用户自行准备 PDF 后，在 Codex 中输入：

```text
使用 $journal-style-corpus。
我已经准备好的 PDF 文件夹是：/absolute/path/to/journal-pdfs
```

Codex 会先进行只读预检：统计 PDF、识别嵌套目录、重复文件、损坏文件和命名规律，并查找相邻的 BibTeX、RIS、CSV 或 manifest 元数据。随后，它会根据语料规模制定计划，并在每个会修改项目文件的步骤前征求确认。

如果用户没有提供路径，skill 只会先询问 PDF 文件夹，不会要求用户提前设计完整工作流。

## 具体工作流程

### 1. PDF 文件夹只读预检

盘点 PDF、识别字节级重复文件和同名冲突、定位已有元数据，并判断文件夹是否混合了多个期刊或文章类型。原始 PDF 保持不变。

### 2. 初始化项目与建立注册表

在原始 PDF 之外建立项目目录，保存 citation key、标题、期刊、年份、文章类型、PDF 来源、方法标签、数据集划分、批次、Codebook 版本和处理状态。

### 3. 文章类型与方法审计

先规范化 article type，再进行抽样。方法判断采用元数据优先的证据漏斗：先使用结构化文献数据和摘要；只有摘要不足或冲突时才读取 PDF 的局部片段；最后才把紧凑证据包交给 Codex 复核。

### 4. Development/Holdout 划分

在归纳写作规则之前完成划分，并尽可能按方法类型、文章体裁或编辑时期平衡。Holdout 不能为了扩大样本而重新放入 Development。

### 5. Pilot 提取与质量检查

选择具有代表性的文章测试边界识别和清洗规则；视觉检查章节起止页；只合并段落内部的软换行；保留段落边界；去除脚注、作者信息、编辑说明、表格、公式、页眉页脚等非正文内容。

### 6. 提取 Development 正文

把经过验证的规则应用于 Development，保存完整文本来源、清洗后的模块文件、页码范围、提取引擎、置信度和文章级例外。

### 7. 归纳修辞 Move Codebook

根据段落为读者完成的沟通功能归纳 move，而不是仅根据关键词分类。每段有一个 primary move，并可包含少量 secondary moves；每个代码都需要定义纳入线索、排除边界及方法类型变体。

### 8. Calibration 与锁定 Codebook

使用平衡的 Calibration 样本测试并修正 provisional codebook。锁定后，后续批次不能静默改变定义；新 move 必须通过版本迁移和定向回溯编码处理。

### 9. 分批持久化编码

每个 Development 批次只处理一次。持久保存段落编码、排除噪声、QA 标记、过渡方式、引文作用、时态语态以及与假设、模型、表格的联系。新增批次只合并新增行。

### 10. 稳定性分析与指南检查点

计算文章覆盖率、首次出现位置、相邻 move 转移、典型顺序及不同方法类型的差异。在正式检查点之间只生成轻量 guide delta，不反复读取历史正文，也不每批重写完整指南。

### 11. 冻结 Development 指南

生成版本化指南，包括证据层级、读者问题、模块架构、段落微结构、方法变体、语义槽模板、反例、检查表和 Codex 起草/修改协议。在打开 Holdout 前冻结 Codebook、指南、评价问题、阈值及文件哈希。

### 12. 独立 Holdout 验证

使用冻结规则提取和编码预先划定的 Holdout，比较 move 覆盖率、层级一致性、首次位置、转移、方法类型差异、QA 负担及 Codebook 可恢复性。记录偏差，但不立即修改指南。

### 13. 验证决策

可以保留冻结指南、将其标记为“带限制验证通过”，或在明确授权后建立独立的 post-validation 版本。绝不覆盖 Holdout 打开前的冻结版本。

### 14. 可选的论文诊断与修改

只使用指定的冻结/验证指南和待修改论文。先诊断段落功能，再逐节改写；保留事实、证据、引文、方程、标签、数值结果和因果强度；同时输出与规则关联的修改日志和 author queries。

## 分批持久化“训练”语料库

当语料达到约 50 篇以上时，skill 会使用大型语料增量模式。例如，200 篇论文可以划分为：

- 用于归纳 move 的 Pilot；
- 用于稳定并锁定 Codebook 的 Calibration；
- 只处理一次的多个 Scale 批次；
- 始终独立的 Holdout。

注册表、批次计划、段落编码、QA 结果、累计统计、guide delta 和版本化指南会被保存在项目文件中。新对话只需要加载当前批次、锁定 Codebook、批次 ledger 和累计摘要，不需要重新输入历史 PDF。

这里的“持久化训练”是指在磁盘上持续积累结构化语料表示和写作指南，**不会修改底层模型权重，也不是 API fine-tuning**。

## 使用实例：JIBS 常规研究论文指南

该流程曾应用于 *Journal of International Business Studies*（JIBS）的 190 篇常规 `Article`，目的是同时学习定量、质性、概念和混合方法论文的写作结构，并保留独立验证集。

### 语料设计

- 152 篇 Development：
  - 12 篇 Pilot；
  - 28 篇 Calibration；
  - 112 篇 Scale，按有界批次处理。
- 38 篇完全独立的 Holdout。
- 五个分析模块：Introduction、Theory、Method、Results、Discussion。
- 锁定的目标期刊 Codebook 包含 36 个修辞 moves。

### Development 产出

- 编码 10,682 个 Development 正文段落。
- 排除 1,196 个非正文或污染单元。
- 生成带有 Core/Common/Optional/Rare 层级、模块架构、方法类型变体、语义槽模板和起草/修改检查表的冻结指南。
- 保留 N=80、N=120 的历史检查点版本，没有覆盖旧指南。

### Holdout 验证效果

- 完成 38/38 篇 Holdout。
- 生成 177 个正式模块文件，编码 2,644 个正文段落。
- 在预先规定的复核规则下，锁定 Codebook 可恢复性为 100%。
- Development 的 18 个 Core moves 中有 16 个在 Holdout 仍为 Core。
- 36 个 move 中，31 个层级完全一致，5 个发生一级变化，没有两级以上变化。
- 33 个 move 的覆盖率接近复现，3 个为中度偏差，没有材料性覆盖率偏差。
- 五个模块的 Top-5 转移结构均达到接近复现。
- 没有发现必须新增的修辞 move。

最终决策是保留冻结指南，并标记为 **Holdout validated with caveats**，而不是根据 Holdout 重新拟合指南。例如，质性 Results 中的质性证据 move 在全体论文分母下属于 Rare，但在质性论文内部仍是设计特定的 Core；顺序差异则被保留为限制，而没有转化为僵化的段落位置规则。

本仓库不包含源论文、提取后的文章正文或 JIBS 完整指南。

## 仓库内容

- `SKILL.md`：核心路由、工作流、不变量和论文修改规则。
- `references/onboarding.md`：PDF 文件夹优先的启动与分阶段规划。
- `references/workflow.md`：提取、QA、move 归纳、指南与验证细节。
- `references/large-corpus.md`：持久化批处理与 token 管理。
- `references/move-analysis.md`：功能编码与稳定性解释。
- `references/schemas.md`：注册表、编码、验证与修改数据结构。
- `references/manuscript-revision.md`：诊断、优先级、修改日志和内容保留审计。
- `scripts/init_journal_corpus.py`：初始化语料项目。
- `scripts/manage_incremental_corpus.py`：规划和合并增量批次。
- `scripts/validate_style_corpus.py`：检查模块覆盖、提取噪声和 Holdout 隔离。
- `scripts/analyze_move_coding.py`：计算文章覆盖率和 move 转移统计。

## 重要边界

- 本流程不能证明某种写法会导致录用。
- 高频不自动等于写作规则；推荐还必须有明确的读者沟通理由。
- 自动编码属于 first pass，不代表人工编码一致性。
- 语料论文只用于约束修辞选择，不能为待修改论文提供主张或研究发现。
- 不复制语料论文句子到新稿件中。
- PDF 获取与爬虫不属于本 skill。

