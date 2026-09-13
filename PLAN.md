# CHM5235 学习路线与进度看板

> 这是工作台的**总入口**。每次开工先看这里，做完一件事回来勾一个框。
> 最后更新：2026-09-13

## ⚠️ 真实截止日期（2026-09-07 从 Canvas 作业页核对，覆盖下面推算的时间线）

| 作业 | 软件 | 开放 | **截止** | 分值 |
|---|---|---|---|---|
| **HW1** | Gaussian 16 / GaussView 6 | 已开放 | **2026-09-13（周日）23:59** | 30 分（15%）|
| HW2 | ORCA | 已开放 | 2026-09-27 | 30 分 |
| HW3 | OpenMOLCAS | 09-20 开放 | 2026-10-18 | 20 分 |
| HW4 | VASP | 10-11 开放 | 2026-11-08 | 30 分 |
| 期中考 | 理论，无实操 | — | **2026-10-05** | 38 分 |

**2026-09-13：HW1 六题全部跑完、报告写完、合并成一份 PDF，已经在 Canvas 截止日当天准备提交。**
最终产出在桌面 `CM5235 作业文件\CM5235_HW1_Zhang_Xubo.docx`(+ 对应 .pdf)，不在仓库里（学号/声明要本人填，
仓库里 `02_Assignments/hw1_gaussian/` 保留的是输入文件和过程记录）。

集群 = **HPC@NUS，atlas9.nus.edu.sg**（PBS Pro，登录节点名 `atlas9-c01`，实际跑的计算节点显示为 `venus01`）。
确认过的固定值：队列 `serial`（1 核，最多 15GB 内存，无 walltime 下限，`parallel` 队列没查，多数题目
1 核够用）；Gaussian 模块名 `Gaussian/g16`；scratch 目录 `/hpctmp/$USER`；**不需要 `-P` project code**
（默认 project 能跑）。以后 HW2/3/4 的 PBS 脚本可以直接照抄 `hw1_gaussian/inputs/*/submit_*.pbs` 的骨架。

## 一句话策略

课程的四次作业（各 15%，合计 60%）**一一对应四个软件**，而四个软件全部在 HPC@NUS 上跑。
所以真正的主线只有两条：**(A) 把集群用顺手**（一次投入，四次受益）、**(B) 每个软件跑通"优化+频率"这条最小闭环**，
其余任务（TD-DFT、BS-DFT、CASPT2、能带）都是在这条闭环上换关键字。

考试（期中 15% + 期末 25%）考理论概念，不考实操——但理论理解直接决定你能不能看懂算错在哪。

## 时间线

> 下面的周次日期是按「Week 1 = 8/10 开学、9/21–9/27 Recess Week、期中在 Week 7 周二 9/29」**推算**的。
> 拿到正式课表后请回来校正这张表。

| 周次 | 日期 | 主线 | 目标 |
|---|---|---|---|
| W1 | 8/10–8/16 | — | 已过。讲义笔记 `wk01_计算化学概览与HPC入门.md` 已整理 |
| **W2** | **8/17–8/23** | **HPC 打通** | 登录 → 建目录 → 提交第一个测试作业并拿到输出（见 `00_Course_Info/HPC快速上手.md`）<br>📌 **Lecture 02 布置了 H₂ 势能面任务**，见 `02_Assignments/task_h2_pes/`。笔记 `wk02_量子力学基础到HF理论.md` |
| W3 | 8/24–8/30 | Gaussian | 单分子 opt+freq 跑通；GaussView 看轨道/频率动画。笔记 `wk03_标准软件_变分原理_基组_SCF.md`（Lecture 03 练习：o-Cresol opt+freq+PBE） |
| W4 | 8/31–9/6 | Gaussian → **HW1** | TD-DFT 激发态 + BS-DFT 磁交换；写报告。笔记 `wk04_电子相关方法.md`（Lecture 04 练习：乙烷/乙烯 相关方法对比 + counterpoise） |
| W5 | 9/7–9/13 | ORCA | 同样任务换 ORCA 做一遍，对比结果；Avogadro/Chemcraft 可视化 |
| W6 | 9/14–9/20 | ORCA → **HW2** | 提交 HW2 |
| — | 9/21–9/27 | Recess | 复习理论：HF/Roothaan-Hall、电子相关、波函数分析 |
| W7 | 9/28–10/4 | **期中考 9/29 周二 19:00–20:00** | 理论概念题，无实操 |
| W8–9 | 10/5–10/18 | OpenMOLCAS → **HW3** | RASSCF → CASPT2 → RASSI；Luscus 看活性空间轨道 |
| W10–11 | 10/19–11/1 | VASP → **HW4** | 周期性体系：弛豫 → SCF → 能带/DOS；VESTA + vaspkit + py4vasp |
| W12–13 | 11/2–11/15 | 收尾 + 复习 | 补齐笔记，准备期末 |

**关键节点**：期中 9/29（周二 19:00–20:00）· 每次作业交**单个 PDF**

## 进度看板

### A. HPC@NUS（主线一，最优先）

- [x] 申请 HPC 账号
- [x] 首次 SSH 登录成功
- [x] **确认到底用哪个集群**：是 **HPC@NUS**，登录节点 `atlas9.nus.edu.sg`（PBS Pro）。用户账号已能登录。
- [x] 确认自己所属的 **project code**：不需要，默认 project 就能跑（`-P` 不加也行）
- [x] `module avail` 查清 Gaussian 模块名：`Gaussian/g16`（ORCA/MOLCAS/VASP 的还没查）
- [x] 确认可用队列和资源上限：`serial`（1 核 / ≤15GB / 无 walltime 下限），已够 HW1 全部用
- [x] 规划目录：`~/CHM5235/hw1/exN/` 放输入脚本，scratch 用 `/hpctmp/$USER/`
- [x] **提交第一个测试作业并成功拿到输出**（里程碑，2026-09-08 达成）
- [x] 打通本地 ↔ 集群文件传输：FileZilla（SFTP），用户已经很熟练
- [x] 会用 `qstat` 查状态、看 `.o` 日志和 `.log` 里的 `Normal termination`/`Error termination` 定位失败原因

### A2. Lecture 02 布置的任务：H₂ 势能面 RHF vs UHF

📁 `02_Assignments/task_h2_pes/`（模板、扫描脚本、提取脚本都已备好）

- [ ] 读讲义笔记第十一节，搞懂 RHF 为什么在解离时失败
- [ ] 从 Canvas 下载老师给的原始输入文件，对照本目录的模板
- [ ] 跑 RHF 扫描（25 个点，0.5–10 Å）
- [ ] 跑 UHF 扫描（**必须加 `guess=mix`**，否则会塌回 RHF 解，整个任务白做）
- [ ] 提取能量和 ⟨S²⟩，画两条 PES 曲线 + ⟨S²⟩ 曲线
- [ ] 标出 Coulson–Fischer 点，与实验 Dₑ ≈ 4.75 eV 对比
- [ ] 写清"为什么结果不同"

### B. Gaussian + GaussView（HW1，15%）—— ✅ 2026-09-13 全部完成并提交

实际 HW1 六题跟这里原来猜的模板不一样（真题是 HCl 多基组 / H-F 解离曲线 / CH2FCl 键能 /
两道理论题 / CH2F-OH 激发态），细节和踩过的坑见 `02_Assignments/hw1_gaussian/`
和 `03_Software_Methods/Gaussian/pitfalls.md`（**最大的坑**：`guess=mix` 对异核双原子
不一定生效，扫描全程 ⟨S²⟩=0 都不代表对，要查一遍再用 `stable=opt` 校正）。
- [x] Gaussian 模块名 `Gaussian/g16`
- [x] opt+freq 跑通，会判断收敛/虚频
- [x] GaussView 看分子轨道（MOs 对话框）、电子密度+静电势叠加图（Surfaces and Contours →
      Cube Actions 生成 Density/ESP 立方体 → 选中立方体 → Surface Actions → **New Mapped Surface**）
- [x] TD-DFT / CIS 激发态对比（Ex6）
- [x] 报告成稿 → 桌面 `CM5235 作业文件\CM5235_HW1_Zhang_Xubo.docx`

### C. ORCA + Avogadro/Chemcraft（HW2，15%）

- [ ] 注册 ORCA Forum 账号（即使集群已装，本地看文档要用）
- [ ] 确认集群上 ORCA 模块名与**可执行文件绝对路径**（并行必须用全路径，见 `pitfalls.md`）
      ⚠️ Lecture 02 p.95 用的是 **ORCA 5.0.3 + OpenMPI 4.1.1**，不是大纲写的 ORCA 6
- [ ] opt+freq 跑通并与 Gaussian 结果对比
- [ ] TD-DFT、BS-DFT（ORCA 会直接输出 J，注意用的是哪个公式）
- [ ] Avogadro 或 Chemcraft 可视化
- [ ] 报告成稿 → `02_Assignments/hw2_orca/`

### D. OpenMOLCAS + Luscus（HW3，15%）

- [ ] 从 Canvas 拿到课程提供的可执行文件与运行脚本
- [ ] 理解**活性空间 (n electrons, m orbitals)** 怎么选——这是整个 HW3 的命门
- [ ] RASSCF 跑通
- [ ] CASPT2 修正动态相关
- [ ] RASSI + 自旋轨道耦合
- [ ] Luscus 检查活性轨道选对了没有
- [ ] 报告成稿 → `02_Assignments/hw3_openmolcas/`

### E. VASP + VESTA/vaspkit/py4vasp（HW4，15%）

- [ ] 拿到课程提供的 VASP 可执行文件与 POTCAR 路径
- [ ] 搞清 POSCAR/INCAR/KPOINTS/POTCAR 四个文件各自管什么
- [ ] ENCUT 和 k 点收敛测试
- [ ] 结构弛豫 → 静态 SCF → 能带 + DOS 三步流程
- [ ] 2D 材料 / 表面吸附：真空层、偶极修正、色散校正
- [ ] VESTA 看结构、vaspkit 后处理、py4vasp 画图
- [ ] 报告成稿 → `02_Assignments/hw4_vasp/`

### F. 理论（考试用，占 40%）

> 讲义笔记都在 `01_Lecture_Notes/`，每份含自测清单。索引见该目录 `README.md`。

- [x] Lecture 01：计算化学概览 + 硬件/HPC（`wk01_计算化学概览与HPC入门.md`）
- [x] Lecture 02：量子力学基础 → Hartree-Fock、Roothaan-Hall 方程（`wk02_量子力学基础到HF理论.md`）
- [x] Lecture 03：软件对照 + 变分原理 + Koopmans + RHF/UHF + 双电子积分/RI/DIIS + 基组（`wk03_标准软件_变分原理_基组_SCF.md`）
- [x] Lecture 04：电子相关 —— CI / CASSCF / Coupled Cluster / MPn / BSSE / 标度（`wk04_电子相关方法.md`）
- [ ] 力场方法（原子级 / 粗粒化）—— 还没讲到
- [ ] 波函数分析：原子电荷、电子密度、轨道局域化 —— 待后续课
- [ ] 分子动力学（DFT / 半经验）—— 待后续课
- [ ] 每周课后在 `01_Lecture_Notes/wkNN_topic.md` 留一份自己的话复述

## 每周固定动作

1. **课后当天**：`01_Lecture_Notes/wkNN_topic.md` 写笔记，用自己的话，不抄 slides
2. **第一次碰某个软件**：在 `03_Software_Methods/<软件>/notes.md` 记模块名、启动命令、关键字含义
3. **每次报错**：立刻记进对应的 `pitfalls.md`——现象 / 原因 / 解决。这个文件的价值随时间指数增长
4. **每次有进展**：commit，message 写清"做了什么 / 为什么"
5. **回到这里勾框**

## 大文件规矩

`.chk` `.wfn` `WAVECAR` `CHGCAR` 轨迹文件等**一律不进 git**。留在集群的 scratch 或本地 `scratch/`（已 gitignore）。
报告 PDF 和最终的输入/关键输出文件可以进库。
