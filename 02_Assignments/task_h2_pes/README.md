# Task (Lecture 02, p.101)：H₂ 势能面 RHF vs UHF

> Study the potential energy surface of H₂ at RHF level of theory in the domain
> **0.5–10 Å, at minimum 20 points**. Compare the results with UHF results.
> **Keep the same identical basis sets for both cases. Can you explain why the results differ?**

理论背景见 `../../01_Lecture_Notes/wk02_量子力学基础到HF理论.md` 第十一节。

## ⚠️ 三个坑（前两个讲义里没说）

### 1. `guess=mix` —— 不加的话整个作业做不出来

H₂ 是闭壳层单重态。直接写 `#p UHF/...` 提交，Gaussian 会从对称的初始猜测出发，
**UHF 会原封不动地收敛到 RHF 解**，两条曲线完全重合，你什么也看不到。

必须用 `guess=mix` 把 HOMO 和 LUMO 混合、**人为破坏 α/β 对称性**，
UHF 才能找到 Coulson–Fischer 点之后那个更低的破缺解。

本目录的 `H2_UHF.gjf` 已经加了 `guess=mix`（还加了 `stable=opt` 用于验证解的稳定性，
跑得慢的话可以先去掉）。

### 2. 讲义给的循环只到 1.25 Å，不满足题目要求

原始循环 16 个点、最大 1.25 Å。但**题目要 0.5–10 Å、≥20 点**，
而且 RHF 和 UHF 的差异**恰恰只在大 R 处才显现**。
`run_pes.sh` 里的 R 列表已扩展成 **25 个点、到 10 Å**，近处密远处疏。

### 3. 文件名说 UB3LYP，题目说 RHF/UHF

Canvas 上的模板文件名是 `Gaussian_PES_H2_UB3LYP`，但题目要求的是 **HF**，不是 B3LYP。
本目录的两个模板都用 `6-31G(d,p)`，**两者基组完全一致**（题目明确要求）。

## 用法

```bash
# 1. 传到集群
scp -r task_h2_pes/  你的账号@集群:~/CHM5235/

# 2. 在集群上提交（先改 run_pes.pbs 里的 project code）
qsub run_pes.pbs

# 3. 算完后提取数据
bash extract.sh
```

会生成 `results_RHF.dat`、`results_UHF.dat`（两列：R / E）和 `s2_UHF.dat`（R / ⟨S²⟩）。

## 报告要放什么

1. **两条 PES 曲线叠在一张图**（横轴 R/Å，纵轴 E/Hartree 或相对能量）
2. **标出 Coulson–Fischer 点**——两条曲线开始分离的位置（约 1.2–1.5 × 平衡键长）
3. **⟨S²⟩ 随 R 的变化曲线**——从 0 涨到 ≈1，这就是自旋污染的直接证据
4. **解离极限的定量对比**：
   - UHF 在 R→10 Å 应趋近 2 × E(H)。用 `6-31G(d,p)` 算一个单独的 H 原子做参考
   - RHF 明显更高，因为含 50% 不该有的 H⁻H⁺ 离子项
5. **与实验对比**：$D_e(\mathrm{H_2}) \approx 4.75$ eV。HF 算出来偏小，
   差的那部分就是**电子关联能**——直接呼应讲义第七节的平均场近似丢掉了什么

## 一句话答案

> RHF 强制两个电子占据同一个空间轨道 σ_g，展开后共价项和离子项永远各占 50%，
> 与核间距无关，所以解离时能量过高。UHF 允许 α、β 各自局域到一个核上，
> 超过 Coulson–Fischer 点后破缺自旋对称性，正确解离到 2×E(H)；
> 代价是波函数不再是 Ŝ² 的本征函数，即自旋污染（⟨S²⟩ 从 0 升到约 1）。
