# CHM5235 — Applied Computational Chemistry Workbench

个人课程工作台：讲义、作业、软件/方法笔记、项目与文献的统一管理仓库。
课程：CM5235 Applied Computational Chemistry（NUS，授课教师 Liviu Ungur）。

## 目录结构

| 目录 | 用途 |
|---|---|
| `00_Course_Info/` | 教学大纲、评分标准、HPC@NUS 接入说明、推荐书目 |
| `01_Lecture_Notes/` | 按周/主题整理的课堂笔记，建议命名 `wk01_topic.md`；`slides/` 存放老师发的原始讲义 PDF |
| `02_Assignments/` | 作业，建议每次作业一个子目录 `hwN_topic/`（课程共 4 次 HW，各 15%） |
| `03_Software_Methods/` | 按软件分类的学习笔记、输入模板、常见坑：`Gaussian` / `ORCA` / `OpenMOLCAS` / `VASP` / `_others` |
| `04_Projects/` | 课程项目或课题相关计算 |
| `05_Papers_References/` | 相关文献、综述、方法论文的笔记与 PDF（大文件建议不入库，见下） |
| `06_Cheatsheets/` | 命令速查、可视化工具清单、单位换算等 |
| `scratch/` | 临时计算文件（已在 .gitignore 中忽略，不会提交） |

`03_Software_Methods/` 下四个软件目录对应课程四次作业，每个目录建议包含：
- `notes.md` — 理论要点、关键字/参数含义
- `templates/` — 输入文件模板
- `pitfalls.md` — 踩过的坑与排查方法

## 每周工作流建议

1. 课前/课后：在 `01_Lecture_Notes/` 新建当周笔记
2. 新方法/软件第一次接触：在 `03_Software_Methods/<软件>/notes.md` 记录安装、基本用法
3. 作业：`02_Assignments/hwN_topic/`，输入输出文件与报告放一起
4. 计算过程中的大文件（波函数、checkpoint、轨迹等）留在本地或 `scratch/`，不提交到 git（见 `.gitignore`）
5. 每完成一次有意义的进展就 commit，commit message 写清楚"做了什么/为什么"

## Git 使用提示

```bash
git add -A
git commit -m "wk01: DFT 基础笔记 + Gaussian 输入模板"
git push
```

大文件（>50MB，如轨迹文件、波函数文件）不要提交；如需版本管理科研数据，后续可评估 Git LFS。
