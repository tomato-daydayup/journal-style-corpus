# Journal Style Corpus

Turn a folder of journal article PDFs into a practical writing guide for that journal.

You provide the PDFs. Codex organizes the corpus, learns recurring writing patterns, checks whether those patterns hold in unseen papers, and produces a guide you can later use to draft or revise a manuscript.

> This is persistent corpus learning, not model fine-tuning. PDF downloading and scraping are not included.

## What do I get?

A completed project can give you:

- a clean, organized article corpus;
- a map of what paragraphs do in each section;
- common section structures and transitions;
- method-specific writing patterns;
- an evidence-based writing guide with templates and checklists;
- an independent validation report;
- and an optional workflow for diagnosing and revising your manuscript.

The skill learns rhetorical functions and organization. It does not copy sentences or findings from the source papers.

## Install

```bash
git clone https://github.com/tomato-daydayup/journal-style-corpus.git \
  ~/.codex/skills/journal-style-corpus
```

## Start

Prepare the PDFs yourself, then tell Codex:

```text
Use $journal-style-corpus.
My prepared PDF folder is: /absolute/path/to/journal-pdfs
```

Codex first checks the folder without changing the original files. It then proposes a plan and asks before each major step.

## The workflow in five simple steps

### 1. Check and organize the PDFs

Codex counts the papers, finds duplicates or broken files, reads available metadata, and helps decide which article types belong in the guide.

### 2. Create a fair learning and test split

Most papers become the **Development set**, used to learn writing patterns. A separate **Holdout set** is kept unopened until the guide is finished, so the guide can be tested honestly.

### 3. Learn how the journal writes

Codex cleans and separates relevant sections—for example Introduction, Theory, Method, Results, and Discussion. It then identifies the communicative job of each paragraph, such as establishing a problem, developing a mechanism, explaining a measure, reporting evidence, or claiming a contribution.

### 4. Build and validate the guide

Recurring patterns are converted into a readable guide: common section structures, paragraph functions, transitions, method-specific variants, semantic-slot templates, anti-patterns, and checklists. The frozen guide is then tested on the unseen Holdout papers.

### 5. Use the guide on your manuscript

Codex can diagnose your manuscript section by section and revise it against the validated guide. Your facts, citations, equations, numerical results, labels, and level of certainty remain protected.

```text
Prepared PDFs
      ↓
Audit and split
      ↓
Learn paragraph functions
      ↓
Build and validate guide
      ↓
Diagnose or revise manuscript
```

## How does it handle hundreds of papers?

Large corpora are processed in batches. Each paper is read and coded once, and the results are saved to project files. Later batches update the cumulative statistics and guide without reopening every old PDF.

This means you can stop, start a new Codex chat, and continue from the saved project state. The persistent files—not chat memory—become the source of truth.

In plain language:

- **Pilot papers** help discover the writing patterns.
- **Calibration papers** help clarify and lock the coding rules.
- **Scale batches** expand the evidence without repeatedly rereading old papers.
- **Holdout papers** test whether the final guide generalizes.

The model itself is not retrained. The reusable “learning” is stored in the corpus registry, paragraph coding, cumulative statistics, versioned guides, and validation reports.

<details>
<summary><strong>Technical workflow for advanced users</strong></summary>

1. Read-only PDF preflight and metadata audit.
2. Registry construction and article-type normalization.
3. Method/design classification using metadata first and targeted PDF reading only when needed.
4. Balanced Development/Holdout assignment before style induction.
5. Pilot extraction, visual boundary QA, and noise cleaning.
6. Development-only section extraction.
7. Pilot rhetorical-move induction.
8. Calibration and codebook lock.
9. Bounded batch coding with persistent paragraph-level outputs.
10. Coverage, first-position, transition, sequence, and method-group analysis.
11. Versioned guide checkpoints and guide-delta packets.
12. Pre-Holdout freeze of guide, codebook, evaluation questions, thresholds, and hashes.
13. Independent Holdout evaluation without changing the frozen rules.
14. Optional manuscript diagnosis, section revision, change log, and preservation audit.

See [SKILL.md](SKILL.md) and the files under [`references/`](references/) for implementation details.

</details>

## Example: a JIBS writing guide

This workflow was tested on 190 regular research articles from the *Journal of International Business Studies* (JIBS).

### Corpus design

- 152 Development papers used to build the guide;
- 38 unseen Holdout papers used only for validation;
- quantitative, qualitative, conceptual, and mixed-methods papers included;
- Introduction, Theory, Method, Results, and Discussion analyzed;
- 36 target-specific paragraph functions identified.

### What the project produced

- 10,682 Development paragraphs coded;
- a versioned guide with section structures, method variants, templates, and checklists;
- earlier guide checkpoints preserved rather than overwritten;
- 2,644 Holdout paragraphs used for independent testing.

### Validation result

- 31 of 36 writing-pattern tiers matched exactly in Holdout;
- the other five moved by only one tier;
- no pattern moved by two or more tiers;
- no material coverage failure was found;
- the main transition structure replicated across all five sections;
- no new paragraph function was needed.

The guide was therefore kept unchanged and marked **Holdout validated with caveats**. Differences caused by research design were recorded as variants instead of being turned into rigid universal rules.

The repository does not include the source articles, extracted article text, or the complete JIBS guide.

## Boundaries

- The skill starts from PDFs the user has already prepared.
- It does not scrape publishers or download papers.
- It cannot prove that a writing pattern causes acceptance.
- Frequency alone does not automatically become a writing rule.
- Automated coding is a first pass, not a claim of human intercoder reliability.
- Corpus papers guide rhetorical choices, not the manuscript's substantive claims.

---

# Journal Style Corpus（中文）

把一个期刊论文 PDF 文件夹，转化为一份可实际使用的目标期刊写作指南。

用户提供已经准备好的 PDF。Codex 负责整理语料、学习反复出现的写作模式、用未参与学习的论文检验这些模式，并生成可用于起草或修改论文的指南。

> 这是可持久化的语料学习，不是模型微调。本 skill 不负责抓取或下载 PDF。

## 最后可以得到什么？

- 一套经过审计和清洗的论文语料；
- 每个章节中“段落在做什么”的功能地图；
- 常见的章节结构、论证顺序和过渡方式；
- 不同研究方法对应的写作变体；
- 包含模板和检查表的循证写作指南；
- 独立的验证报告；
- 可选的论文诊断和逐节修改流程。

Skill 学习的是修辞功能和组织方式，不会复制语料论文的句子或研究发现。

## 安装

```bash
git clone https://github.com/tomato-daydayup/journal-style-corpus.git \
  ~/.codex/skills/journal-style-corpus
```

## 开始使用

用户自行准备 PDF，然后告诉 Codex：

```text
使用 $journal-style-corpus。
我已经准备好的 PDF 文件夹是：/absolute/path/to/journal-pdfs
```

Codex 会先只读检查文件夹，不修改原始 PDF。随后给出计划，并在每个主要步骤开始前询问是否继续。

## 五步工作流程

### 1. 检查和整理 PDF

统计论文、识别重复或损坏文件、利用已有元数据，并确认哪些文章类型应该进入写作指南。

### 2. 划分“学习集”和“测试集”

大部分论文进入 **Development**，用于学习写作模式；另一部分进入独立的 **Holdout**，在指南完成前保持封存，用于检验指南是否真的能够推广到未见论文。

### 3. 学习期刊如何写作

Codex 清洗并拆分相关章节，例如 Introduction、Theory、Method、Results 和 Discussion。然后判断每个段落的沟通功能，例如提出问题、发展机制、解释测量、报告证据或声明理论贡献。

### 4. 生成并验证指南

把稳定出现的模式转化为容易使用的指南，包括章节结构、段落功能、过渡方式、方法类型变体、语义槽模板、反面模式和检查表。指南冻结后，再用 Holdout 进行独立验证。

### 5. 用指南诊断或修改论文

Codex 可以根据验证后的指南逐节诊断和修改用户论文，同时保护原有事实、引文、方程、数值结果、标签和论断强度。

```text
准备好的 PDF
      ↓
审计并划分语料
      ↓
学习段落功能
      ↓
生成并验证指南
      ↓
诊断或修改论文
```

## 文章很多时怎么办？

大型语料会分批处理。每篇论文只读取和编码一次，结果保存到项目文件中。后续批次只更新累计统计和指南，不需要反复读取之前的所有 PDF。

因此，用户可以暂停工作、打开新的 Codex 对话，再从保存的项目状态继续。真正的“记忆”来自项目文件，而不是某一次聊天记录。

简单来说：

- **Pilot** 用来发现写作模式；
- **Calibration** 用来澄清并锁定编码规则；
- **Scale batches** 用来逐批增加证据；
- **Holdout** 用来独立检验最终指南。

这里不会修改模型权重。所谓“持久化训练”，是把学习结果保存在注册表、段落编码、累计统计、版本化指南和验证报告中。

<details>
<summary><strong>高级用户：技术流程</strong></summary>

1. PDF 文件夹只读预检与元数据审计。
2. 建立注册表并规范文章类型。
3. 优先利用元数据判断研究方法，仅在必要时读取 PDF 局部内容。
4. 在学习写作模式前完成 Development/Holdout 平衡划分。
5. Pilot 提取、边界视觉检查和噪声清洗。
6. 只提取 Development 正文。
7. 从 Pilot 归纳修辞 move。
8. 使用 Calibration 稳定并锁定 Codebook。
9. 按有界批次编码，并持久保存段落级结果。
10. 分析覆盖率、首次位置、转移、顺序和方法类型差异。
11. 在正式检查点生成版本化指南，其余批次只生成 guide delta。
12. 打开 Holdout 前冻结指南、Codebook、评价问题、阈值和哈希。
13. 使用冻结规则进行独立 Holdout 验证。
14. 可选：论文诊断、逐节修改、修改日志和内容保留审计。

实现细节见 [SKILL.md](SKILL.md) 和 [`references/`](references/) 目录。

</details>

## 实例：JIBS 写作指南

该流程曾用于分析 *Journal of International Business Studies*（JIBS）的 190 篇常规研究论文。

### 语料设计

- 152 篇 Development 用于生成指南；
- 38 篇未见过的 Holdout 只用于验证；
- 同时包含定量、质性、概念和混合方法论文；
- 分析 Introduction、Theory、Method、Results 和 Discussion；
- 归纳出 36 个针对该期刊的段落功能。

### 项目产出

- 编码 10,682 个 Development 段落；
- 生成包含章节结构、方法变体、模板和检查表的版本化指南；
- 保留早期指南版本，没有覆盖历史结果；
- 使用 2,644 个 Holdout 段落进行独立检验。

### 验证效果

- 36 个写作模式层级中，31 个在 Holdout 完全一致；
- 其余 5 个只变化了一级；
- 没有任何模式变化两级以上；
- 没有发现材料性覆盖率失效；
- 五个章节的主要转移结构均得到复现；
- 不需要增加新的段落功能。

因此，最终保留冻结指南不变，并标记为 **Holdout validated with caveats**。由研究设计造成的差异被保留为方法变体，没有被写成僵化的通用规则。

本仓库不包含源论文、提取后的论文正文或完整 JIBS 指南。

## 使用边界

- 用户需要先自行准备 PDF。
- Skill 不负责出版社爬虫或论文下载。
- 不能证明某种写法会导致论文录用。
- 高频不自动等于写作规则。
- 自动编码是 first pass，不代表人工编码一致性。
- 语料只用于约束修辞选择，不能为用户论文提供新的实质主张。

