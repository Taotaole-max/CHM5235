# HW1 — Homework Gaussian（30 分 / 占总成绩 15%）

**截止：2026-09-13（周日）23:59** · 交**单个 PDF** · 最多传 5 次（取最后一次）·
软件：Gaussian 16 + GaussView 6 · 允许用 AI 但**必须在报告里声明**（见下）

题目原件：`../../01_Lecture_Notes/slides/` 无此件；作业 PDF 见
`C:\Users\letaotao\Downloads\CM5235_2026_Homework_Gaussian-1.pdf`（也可从 Canvas 作业页重下）。

## 六道题

| # | 类型 | 分子 | 目录 / 文件 | 依赖集群 |
|---|---|---|---|---|
| Ex1 | 计算 | HCl | `inputs/ex1_hcl/` | ✅ |
| Ex2 | 计算 | H–F | `inputs/ex2_hf_pes/` | ✅ |
| Ex3 | 计算 | CH₂FCl | `inputs/ex3_ch2fcl/` | ✅ |
| Ex4 | 理论 | — | `ex4_理论_HF三个近似.md` | ❌ 已成稿 |
| Ex5 | 理论 | H₂ | `ex5_理论_H2共价键与hJK.md` | ❌ 已成稿 |
| Ex6 | 计算 | CH₂F–OH | `inputs/ex6_ch2foh/` | ✅ |

## 执行顺序

1. **先做 RECON**：`RECON.md` 里 5 条命令在 atlas9 上跑一次，输出贴回给 Claude
   → 填死所有 `submit_*.pbs` 里的 `<<<PROJECT>>>` / `<<<QUEUE>>>` / `<<<GAUSSIAN_MODULE>>>` / `<<<SCRATCH>>>`。
2. **跑 hello.pbs** 确认链路通（`00_Course_Info/HPC快速上手.md` 第 4 节）。
3. 传输入文件到 `~/CHM5235/hw1_gaussian/exN/`，`dos2unix *.pbs *.gjf` 清 Windows 换行。
4. 按 **Ex1 → Ex3 → Ex6 → Ex2** 的顺序 `qsub`（Ex2 的 CCSD(T) 扫描最久，先交它排队也行）。
5. 取回 `.log` / `.fchk`，贴回给 Claude → 提取数据、做表、画图、写讨论。
6. Ex4/Ex5 直接用现成稿，按报告格式排版。

## 提交前检查

- [ ] 封面填 Full Name / Student Number / E-mail / Date / Signature
- [ ] 六道题每题都有：做法说明 + 结果（表/图）+ 讨论
- [ ] 所有图用 Origin/Excel/Python 画，**无手绘**
- [ ] Ex1 的 6 基组表、Ex2 的四曲线图、Ex3 的 BDE、Ex6 的对比表和 UV/Vis 谱齐全
- [ ] **AI 使用声明**（见下），否则算抄袭
- [ ] 合并成一个 PDF，文件名 `CM5235_HW1_张旭博.pdf` 之类
- [ ] Canvas 作业页 `Start Assignment` → 上传

## AI 使用声明（放报告末尾，按实际情况改）

> I used Claude (Anthropic) to help plan the calculations, generate and check the
> Gaussian input files and PBS scripts, extract data from the output logs, produce
> the plots, and draft the two theoretical answers. I ran all calculations myself on
> the NUS HPC, verified the results, and am responsible for the content and quality
> of the submitted work.
