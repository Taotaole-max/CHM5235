# Ex1 — HCl 基态，多计算方法对比（5 分）

## 要交什么

1. **单点计算**（按题目给的输入，`01_hcl_sp_rhf_sto3g.gjf`，R = 1.275 Å 固定）
   从 `.log` 里挖出并报告：
   - SCF energy（搜 `SCF Done`）
   - Electric dipole moment（搜 `Dipole moment`）
   - 全部分子轨道（占据 + 空）的数目和轨道能（搜 `Alpha  occ. eigenvalues` / `Alpha virt. eigenvalues`）
   - Mulliken charges（搜 `Mulliken charges`）

   > 注：连接表里的 `1 2 3.0` 是 GaussView 显示用的“键级”，**不影响量子化学计算结果**，照抄即可。

2. **opt + freq 六个基组**（`02_hcl_optfreq_all_basis.gjf`，一个文件用 `--Link1--` 串了 6 个作业）
   基组：STO-3G / 6-31G / cc-pVDZ / cc-pVTZ / cc-pVQZ / 6-311+G(d)
   做一张表，每个基组一行：

   | 基组 | 平衡键长 Å | 振动频率 cm⁻¹ | 轨道数 | 基函数数 | 总能量 Hartree | HOMO–LUMO gap eV |
   |---|---|---|---|---|---|---|

   - 平衡键长：搜 `!    R1` 或优化收敛后的 `Optimized Parameters`
   - 振动频率：搜 `Frequencies --`
   - 轨道数 / 基函数数：搜 `NBasis=` 和 `NBsUse=`
   - 总能量：搜 `SCF Done`
   - HOMO–LUMO gap：占据轨道能最高的那个 vs 空轨道能最低的那个，差值 ×27.2114 得 eV

3. **与实验值对比**：到 https://cccbdb.nist.gov/exp2x.asp 搜 “HCl”，取实验的
   键长、振动频率、转动常数/转动惯量、熵、焓；和你算的对比，讨论
   **随基组增大计算值如何收敛、往哪个方向偏**。
   （熵、焓在 freq job 的 `Thermochemistry` 段；转动常数搜 `Rotational constants`）

4. **轨道能级图 + 占据轨道图**（RHF/6-311+G(d)，用 `hcl_6311pgd.chk`）
   - 能级图：把该 log 里的 α 轨道能列出来，按高低画横线（占据/空用不同颜色），标 HOMO/LUMO
   - 轨道等值面：`formchk hcl_6311pgd.chk` → GaussView 打开 `.fchk` → Results → Surfaces/Contours，
     逐个画占据 MO（HCl 有 9 个电子对里… 实际 18 电子 → 9 个占据 MO），截图放报告

## 跑法

```bash
qsub submit_ex1.pbs
```
