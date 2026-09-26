# Assignments

每次作业一个子目录。

| 目录 | 作业 | 内容 |
|---|---|---|
| `hw1_gaussian/` | HW1 Gaussian（2026-09-13 已交） | `inputs/` 是提交集群用的输入和 PBS；`final_runs_and_report/` 是跑完的 .log、提取的数据、图和最终报告（每题单独 docx/pdf + 合并版） |
| `hw2_orca/` | HW2 ORCA（截止 2026-09-27） | `00_题目和原始文件/` 题目和 Canvas 结构；`Ex1/4/5/6_*` 每个方法一个子文件夹（.inp、.out、优化结构）；`*_analysis/` 提取脚本和结果表；`03_report_word/` 报告和生成脚本 |
| `hw3_openmolcas/` | HW3 OpenMOLCAS | 还没开始 |
| `hw4_vasp/` | HW4 VASP | 还没开始 |
| `task_h2_pes/` | 集群上手练习 | H₂ 势能面 RHF/UHF |

## hw2_orca 没有入库的文件

在桌面 `CM5235 作业文件\as2` 里还有，没推上来：

- `orca_raw_files/`：ORCA 的中间文件（.gbw、.densities、SCF 日志等），报告用不到
- `*.cube`、`ex1_esp_grid_points_bohr.xyz`：画图用的格点，能用 `ex1_figures/cube_job/` 里的输入重新生成
- `Ex6_water_MD/6b_XTB/ex6b_trajectory_XTB.xyz`（105 MB，超过 GitHub 单文件上限）；
  每 100 步抽一帧的版本在 `ex6_avogadro_animation/`
