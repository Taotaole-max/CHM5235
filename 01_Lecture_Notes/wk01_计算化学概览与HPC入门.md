# Lecture 01：计算化学概览 + 硬件/HPC 入门

> CM5235 · Liviu Ungur · 42 页
> 讲义原件：`slides/CM5235_Lecture_01.pdf`（旧名 `slides/wk01_intro_slides.pdf`）

## 这一讲在干什么

第一讲没有公式，是**课程说明书 + 领域地图 + 干活的基础设施**三件事：

1. 这门课要学什么（理论主线 + 四个软件）、怎么考、怎么给分
2. 计算化学是什么、从哪来、往哪去
3. 超算/集群是怎么组成的，为什么科学计算离不开 Linux + HPC——
   以及**本周就要动手**：申请 HPC 账号、打通 SSH、练命令行

---

## 一、课程结构（p.2–6）⭐ 必须记住

### 理论主线（讲课 + 考试）

| 模块 | 关键词 |
|---|---|
| 计算化学概览 | 与其他研究领域的关系 |
| 力场方法 | 原子级 / 粗粒化，方法的适用边界 |
| 量子力学基础 | 算符、本征值方程、量子化、氢原子轨道从 SE 解出 |
| Hartree-Fock 理论 | Roothaan-Hall 方程 |
| 波函数分析 | 原子电荷、电子密度、轨道局域化 |
| 电子相关方法 | MP2、CCSD 等 |
| 分子动力学 | DFT 与半经验方法 |

### 实操主线（作业）：四个软件一一对应四次作业

| 作业 | 软件 / 可视化 | 权重 | 典型任务 |
|---|---|---|---|
| HW1 | **Gaussian / GaussView** | 15% | 几何优化、振动频率、轨道/密度/自旋密度可视化、TD-DFT 激发态、BS-DFT 磁交换 |
| HW2 | **ORCA / Avogadro / Chemcraft** | 15% | 同上换 ORCA 做一遍；ORCA 强在光谱性质（NMR、EPR、ZFS） |
| HW3 | **OpenMOLCAS / Luscus** | 15% | 多组态方法 RASSCF / CASPT2 / RASSI，过渡金属与镧系激发态 |
| HW4 | **VASP / VESTA / vaspkit / py4vasp** | 15% | 周期性固体、2D 层、分子在表面的吸附 |

### 评分（p.5）

- 4 次作业 × 15% = 60%，每次交**单个 PDF**（手写也行，字要能看懂）
- 期中 quiz **9/29（周二）19:00–20:00**，15%
- 期末 25%
- **期中和期末只考理论/概念题，不考实操计算**

### 作业都在 HPC@NUS 上跑

Gaussian/GaussView 在 HPC 上已装好，无需本地安装。ORCA 6 是 HPC 的 module。
OpenMOLCAS / VASP 由老师通过 Canvas 发安装脚本。
Windows 用户想本地装 Gaussian/GaussView，要先签署条款并邮件发给老师换安装包。

---

## 二、计算化学是什么（p.7–12）

### 定义

用**计算机 + 粒子间相互作用的基本定律**来回答化学问题。一个典型反应有一堆未知量：
选反应物、选催化剂、反应条件（T、P、溶剂）、产物分离、物性（分子/晶体结构、
势能面、熔点、EPR/UV-VIS/IR/NMR/Raman 谱）、反应机理、动力学（为工业放大）。

### 领域里的名字（p.8–9）

- **Nobel 1998**：Walter Kohn（发展 DFT）、John Pople（发展量子化学计算方法）
- **Nobel 2013**：Karplus、Levitt、Warshel（复杂化学体系的多尺度模型）
- 其他：Hartree、Fock、Roothaan、Hohenberg、Car-Parrinello、Neese（ORCA 作者）、B. O. Roos（CASSCF）等

### 简史（p.11）

1925 矩阵力学（Heisenberg/Born/Jordan）+ 波动力学（Schrödinger）+ 首次化学键计算（Heitler-London）→
1927 Hartree 自洽场 → 1930 Fock → 1950 Roothaan LCAO → 1955 首次对 N₂ 做 ab initio →
1964 Hohenberg-Kohn（DFT）→ 1970 Pople 发布 Gaussian → 2019 Google "量子霸权"。

### 未来方向（p.12）⭐ 可能是概念题

1. **AI / 机器学习 + 计算化学**：有望以 DFT 的精度、快 1 万倍以上 → 更快扫描相空间、预测新材料
2. 弱相互作用的准确描述（范德华、色散、长程相关）
3. 分子晶体的晶体结构与声子谱预测
4. 非平衡量子动力学（电子和核一起解薛定谔方程，即**非 Born-Oppenheimer**）
5. 面向量子处理器的计算方法

---

## 三、计算机与集群的解剖（p.13–27）

### 单机

主板集成：CPU（多个计算核 + 很快的本地 cache）、RAM（快）、硬盘（慢）、显卡（自带 GPU + 显存）。

### 集群（p.15–17）

多个**节点**（每个是一台独立计算机）+ **头节点** + **互连交换机**。
- 异构互连：**同节点内核间传输快，跨节点传输慢**
- 便宜、可大规模部署、容错（单节点挂了单独关掉即可，不用停整个集群）
- 基本都跑 Linux

### 共享内存超算（如 IBM Blue Gene/Q，p.18）

专有大主板，能高效整合大量处理器和内存槽。比同等规模的集群贵得多。
巨大的 RAM + 上千节点能做别处做不了的事：**大矩阵对角化**。

### 内存的延迟与带宽（p.19）⭐ 解释"为什么小体系算得快"

| 位置 | 延迟 | 带宽 |
|---|---|---|
| CPU 寄存器 / L1 cache | 1 时钟 | 150 GB/s |
| 本地 RAM | 100 时钟 | 10 GB/s |
| NUMA / 别的节点 RAM | 150 / 10k 时钟 | 10 / 1 GB/s |
| 磁盘 | 10k 时钟 | 0.1 GB/s |

**小数据集/小程序更快，因为能塞进更高层的 cache。频繁随机命中主 RAM 会让程序很慢。**

### CPU 性能指标（p.20）

- **GIPS**：每秒十亿条机器指令（架构相关）
- **GFLOPS**：每秒十亿次浮点运算。**科学计算几乎全用双精度。**
- 能耗对单机不关键（约 0.2 kWh），但对大集群是大问题
- ARM 处理器（手机/平板、Apple M1、日本 Fugaku 的 A64FX）能耗低得多

### Moore 定律（p.21）

集成电路上的晶体管数**约每两年翻一番**。算力增长驱动计算化学处理更大体系、用更高级别理论。

### 文件系统性能（p.25）⭐ 实操要点

`RAM disk` > `scratch/swap`（0.1–1 GB/s，专门放中间结果）> 本地文件系统 > 网络文件系统（家目录）> 备份。
**大量 IO 会显著拖慢集群。跑计算要用 scratch 目录**，按集群管理员的指示。

### BLAS / LAPACK 运算的标度（p.26）

| 运算 | CPU 代价 | 并行 |
|---|---|---|
| 矩阵-矩阵乘 | O(n³) | 容易 |
| 矩阵-向量乘 | O(n²) | 容易 |
| 大多数矩阵分解（SVD、LU、对角化…） | O(n³)，内存也 O(n³) | **难**，且不能用稀疏存储省 |

### Linux 统治超算（p.27）

**自 2018 年起，全球 TOP500 超算 100% 跑 Linux。**

---

## 四、本周动手任务（p.28–42）

### 必做

1. 装 NUS VPN 并登录：https://nusit.nus.edu.sg/eguides/
2. 申请 HPC@NUS 账号：https://nusit.nus.edu.sg/hpc/get-an-hpc-account/
3. SSH 登录成功（Windows 用 PuTTY，Mac 用 Terminal）
4. **必读**：新用户入门指南 + 如何跑批处理作业（PBS）
   - https://nusit.nus.edu.sg/services/getting-started/introductory-guide-for-new-hpc-users/
   - https://nusit.nus.edu.sg/services/getting-started/how-to-run-batch-job/

### 命令行练习（纯终端完成）

- `vi`/`nano` 建文本文件填约 1000 词 → `mkdir` + `mv` 移进文件夹 → `cp` 复制 → 改副本删一个词 →
  `diff` 比较 → 数 "and" 出现几次：`cat file1 | grep ' and ' | wc -l`
- `scp` 传文件到集群 → `ssh` 登录 → 在 `$HOME` 建改文件 → 传回本地
- 读 PBS 作业提交，跑通示例

### PBS 脚本骨架（p.41）

```bash
#!/bin/bash
#PBS -P test_script
#PBS -q parallel
#PBS -l select=1:ncpus=12:mem=2GB
#PBS -j oe
cd $PBS_O_WORKDIR
if [ -f file4 ]; then rm -rf file4; fi
echo 'some random text'                  >  file4
echo 'PBS_O_WORKDIR =' $PBS_O_WORKDIR    >> file4
exit
```

### 非考核 homework：尽量熟练

命令行（`vi ssh scp qsub cat sed awk`、bash 脚本、正则）、Linux 系统（环境变量、
`$PATH`、`$LD_LIBRARY_PATH`、Linux/Windows 换行符差异）、HPC 与 NSCC 的作业提交
（两者相似但有细节差别）、本地 ↔ 服务器文件传输。

### 常用软件清单（p.35–37）

- 连接/传输：PuTTY、FileZilla、WinSCP、Notepad++
- 可视化/编辑：GaussView、Avogadro、Jmol、Molden、Chemcraft（试用 150 天）、VMD（大生物分子）、
  VESTA（晶体）、Multiwfn（波函数分析）、Material Studio（NUS 有 license）
- 波函数后处理：Multiwfn、Molden

---

## 与后续课程/作业的连接

| 这一讲 | 用在哪 |
|---|---|
| 内存延迟/带宽、O(n³) 对角化 | Lecture 03 的 SCF 计算代价、RI 方法为什么能省 |
| scratch 目录、大 IO 拖慢集群 | 所有作业的 `.gitignore` 规矩、PBS 脚本 |
| 四软件 ↔ 四作业对应表 | 整个学期的主线（见 `PLAN.md`） |
| 期中/期末只考理论 | 复习重点全在 `01_Lecture_Notes/` |
| AI + 计算化学、非 BO 动力学 | 可能的概念题 |

## 自测清单

- [ ] 能说出四次作业分别用什么软件、各占多少分、期中期末考什么
- [ ] 能解释集群"同节点内快、跨节点慢"以及它对内存密集型计算的影响
- [ ] 能解释为什么小体系算得快（cache 层级）
- [ ] 知道 GFLOPS 与双精度的关系
- [ ] 能说出计算化学的 2–3 个未来方向，并解释"非 Born-Oppenheimer"是什么意思
- [ ] 会用 `cat | grep | wc -l` 统计词频
- [ ] 能写出一个最简 PBS 提交脚本并说明每行 `#PBS` 的含义
- [ ] HPC 账号已申请、SSH 已登录成功（见 `PLAN.md` 进度看板 A）
