# Ex6 水团簇的分子动力学：(a) 从头算 DFT 和 (b) 半经验 XTB

题目要求：用 ORCA 的 `%md` 模块，在 400 K、Nosé–Hoover 链恒温器、50 Å 的球里，对冰晶切出来的水团簇跑一条轨迹：
(a) PBE/def2-SVP，小团簇，200 步；(b) XTB，大团簇，5000 步。用 Avogadro 打开其中一条轨迹做成动画；
回答从模拟里能学到什么、轨迹里还能提取什么信息。

## 现在有的文件

```
Ex6_water_MD/
├── Ex6_说明.md                              本文件
├── ex6a_water_cluster_20H2O_for_DFT.xyz     (a) 用的小团簇：20 个水（Canvas 原文件副本）
├── ex6b_water_cluster_128H2O_for_XTB.xyz    (b) 用的大团簇：128 个水（Canvas 原文件副本）
├── ex6_submit_2_simulations.sh              提交脚本：一条命令交两个作业
├── ex6_run_one_simulation.pbs               作业脚本：跑一条轨迹，跑完自动检查、归档
├── 6a_DFT_PBE/  ex6a_md_DFT_PBE.inp         ORCA 输入：(a) PBE/def2-SVP，200 步
├── 6b_XTB/      ex6b_md_XTB.inp             ORCA 输入：(b) GFN2-xTB，5000 步
└── ex6_analysis/                            结果分析（只在本机用）
    ├── ex6_analyze_trajectories.py          温度、氢键数、四面体序参数随时间的变化，O–O 距离分布
    ├── ex6_render_trajectory.py             首/末帧快照 + (b) 的轨迹动画 GIF
    ├── ex6_fig_temperature_structure.png    （生成）温度 / 氢键数 / 四面体序参数随时间
    ├── ex6_fig_OO_distance_distribution.png （生成）开头和结尾的 O–O 距离分布
    ├── ex6_fig_snapshots.png                （生成）(a)(b) 的第一帧和最后一帧
    ├── ex6b_trajectory_animation_XTB.gif    （生成）题目要的轨迹动画
    └── ex6_summary.md                       （生成）报告要引用的数字
```

分析用的两个指标：
- **氢键数**：O···O < 3.5 Å 且 H–O···O 夹角 < 30° 算一个氢键，统计每个水分子平均有几个。
- **四面体序参数 q**：冰里每个水被 4 个邻居按正四面体包围，q ≈ 1；液态水约 0.6。
  团簇是从冰里切的，表面分子凑不齐 4 个邻居，所以 q 只对一开始就有 4 个邻居的"内部"分子平均
  （20 水团簇里 2 个，128 水团簇里 48 个）。初始 q = 0.998，q 往下掉就说明冰在熔化。

- 两个团簇文件的第二行都写着 "H24 O12"，那是 Canvas 原文件里留下的旧注释，实际分别是 20 个和 128 个水分子。
  ORCA 读坐标时不看这一行，不影响计算。
- `ex6_submit_2_simulations.sh`：在集群上运行它。两个作业互不依赖，同时排队；
  (a) 申请 10 GB 内存，(b) xtb 很省内存，只申请 4 GB，排队更快。
- `ex6_run_one_simulation.pbs`：不用手动运行。它做三件事：跑 ORCA → 数一下轨迹有多少帧写进日志 →
  把 ORCA 的中间文件收进 `orca_raw_files/`。

## 算完之后，每个子文件夹里会有什么

以 `6a_DFT_PBE/` 为例：

| 文件 | 干什么用 |
|---|---|
| `ex6a_md_DFT_PBE.inp` | 输入（不变） |
| `ex6a_md_DFT_PBE.out` | ORCA 主输出。每一步的温度、势能、动能、守恒能量都在这里，可以画温度和能量随时间的变化 |
| `ex6a_trajectory_DFT_PBE.xyz` | **轨迹**：每一步一帧的多帧 xyz，用 Avogadro 打开就能播放、做动画 |
| `ex6_pbs_log_6a_DFT_PBE.txt` | 作业日志，写着轨迹有多少帧、有没有正常结束 |
| `orca_raw_files/` | ORCA 的中间文件（波函数、续跑用的 .mdrestart 等），一般不用打开 |

(b) 的轨迹有 5001 帧 × 384 个原子，大约 100 MB，Avogadro 直接开会很卡；做动画前我会先每隔几帧抽一帧。

## 怎么跑

`bash Ex6_water_MD/ex6_submit_2_simulations.sh`（在集群上 `~/CHM5235/as2` 里运行）。
两个作业都是单核、限时 12 小时，预计各 1–4 小时。想中途停掉：在对应子文件夹里 `touch EXIT`。

## 设置和理由

- (a) `! MD PBE def2-SVP def2/J`；(b) `! MD XTB2`（GFN2-xTB，ORCA 调用它目录里自带的 `otool_xtb`）。
- `%md` 块，两个一样：
  - `Timestep 0.5_fs`：ORCA 手册建议含 H 的体系时间步不超过 0.5 fs（O–H 伸缩振动周期约 9 fs，步长太大积分会失真）。
    所以 (a) 200 步 = 100 fs，(b) 5000 步 = 2.5 ps。
  - `Initvel 400_K`：按 400 K 的麦克斯韦-玻尔兹曼分布随机给初速度。
  - `Thermostat NHC 400_K Timecon 10.0_fs`：题目指定的 Nosé–Hoover 链恒温器，把体系维持在 400 K。
  - `Cell Sphere cx, cy, cz, 25.0`：题目说的"50 Å 的球"。按直径 50 Å 理解，半径取 25 Å。
    它是一堵软墙，只防止从热团簇上蒸发出去的分子飞远。球心放在团簇的几何中心，因为 xyz 坐标不是以原点为中心的。
    团簇本身半径只有 6.4 Å（a）和 13.7 Å（b），正常情况下碰不到这堵墙。
  - `Dump Position Stride 1`：每一步都存一帧。
- 两个模拟用不同大小的团簇，是因为代价差很多：DFT 每一步都要解一次 SCF，只跑得起小体系、短轨迹；
  XTB 便宜两三个数量级，能跑大体系、长轨迹。
