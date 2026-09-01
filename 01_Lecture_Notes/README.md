# Lecture Notes

按周命名，例如 `wk01_intro_to_qc.md`。用自己的话复述，不抄 slides。
老师发的原始讲义 PDF/PPTX 放 `slides/`。

## 已整理

| 笔记 | 讲义 | 主题 |
|---|---|---|
| `wk01_计算化学概览与HPC入门.md` | `slides/wk01_intro_slides.pdf`（= CM5235_Lecture_01.pdf） | 课程结构、领域概览、计算机/集群解剖、HPC 上手任务 |
| `wk02_量子力学基础到HF理论.md` | `slides/CM5235_Lecture_02.pptx` / `.pdf` | 从薛定谔方程一路近似到 Hartree-Fock-Roothaan + SCF；Linux/ORCA 环境 |
| `wk03_标准软件_变分原理_基组_SCF.md` | `slides/CM5235_Lecture_03.pdf` | 四大软件对照、变分原理、Koopmans、RHF/UHF、双电子积分/RI/DIIS、基组分类 |
| `wk04_电子相关方法.md` | `slides/CM5235_Lecture_04.pdf` | 相关能、静态/动态相关、CI、CASSCF、Coupled Cluster、MPn、BSSE、标度表 |

每份笔记末尾都有**自测清单**和**与作业/后续课程的连接表**。

## 关于公式显示

笔记里的公式用 LaTeX（`$...$` / `$$...$$`）。GitHub 网页版一般能渲染，
但**手机 App、部分浏览器、单行 `$$` 有时会显示成原始代码**。

- wk03 / wk04 的每个块级公式下面都加了一行 `*读法：…*` 中文解释，**不渲染也能看懂**
- 想看渲染效果：用 **VS Code + Markdown Preview Enhanced**、**Typora** 或 **Obsidian** 打开
- 或直接看 `slides/` 里的原始讲义 PDF
