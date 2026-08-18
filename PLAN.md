# CHM5235 学习路线与进度看板

> 这是工作台的**总入口**。每次开工先看这里，做完一件事回来勾一个框。
> 最后更新：2026-08-18

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
| W1 | 8/10–8/16 | — | 已过。讲义 `wk01_intro_slides.pdf` 已入库 |
| **W2** | **8/17–8/23** | **HPC 打通** | 登录 → 建目录 → 提交第一个测试作业并拿到输出（见 `00_Course_Info/HPC快速上手.md`） |
| W3 | 8/24–8/30 | Gaussian | 单分子 opt+freq 跑通；GaussView 看轨道/频率动画 |
| W4 | 8/31–9/6 | Gaussian → **HW1** | TD-DFT 激发态 + BS-DFT 磁交换；写报告 |
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
- [ ] 确认自己所属的 **project code**（`-P` 参数要用），记进 `00_Course_Info/HPC快速上手.md`
- [ ] `module avail` 查清四个软件的模块名，回填到各自 `notes.md`
- [ ] 确认可用队列和资源上限（`qstat -Q`）
- [ ] 规划目录：家目录放输入/脚本，scratch 放计算中间文件
- [ ] **提交第一个测试作业并成功拿到输出**（里程碑）
- [ ] 打通本地 ↔ 集群文件传输（WinSCP / `scp`）
- [ ] 会用 `qstat` 查状态、`qdel` 撤作业、看 `.o`/`.e` 日志定位失败原因

### B. Gaussian + GaussView（HW1，15%）

- [ ] 拿到 Gaussian 模块名与 `g16`/`g09` 版本
- [ ] 跑通 opt+freq（用 `templates/01_opt_freq.gjf`）
- [ ] 会判断优化是否收敛、频率有无虚频
- [ ] GaussView 看分子轨道、电子密度、自旋密度、振动模式
- [ ] TD-DFT 激发态（`templates/02_td_dft.gjf`）
- [ ] BS-DFT 磁交换常数 J（`templates/03_bs_dft.gjf`）
- [ ] 报告成稿 → `02_Assignments/hw1_gaussian/`

### C. ORCA + Avogadro/Chemcraft（HW2，15%）

- [ ] 注册 ORCA Forum 账号（即使集群已装，本地看文档要用）
- [ ] 确认集群上 ORCA 6 模块名与**可执行文件绝对路径**（并行必须用全路径，见 `pitfalls.md`）
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

- [ ] 力场方法（原子级 / 粗粒化）
- [ ] 量子力学基础与 Hartree-Fock、Roothaan-Hall 方程
- [ ] 波函数分析：原子电荷、电子密度、轨道局域化
- [ ] 电子相关：MP2 / CCSD，与 DFT 的关系
- [ ] 分子动力学（DFT / 半经验）
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
