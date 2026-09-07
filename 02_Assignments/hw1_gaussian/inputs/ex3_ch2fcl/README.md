# Ex3 — CH₂FCl 键解离能（5 分）

分子：**氯氟甲烷 CH₂FCl**（C 上接 2 个 H、1 个 F、1 个 Cl）。

## 要交什么

### 1) 三方法总能量对比
`01_ch2fcl_parent.gjf` 一个文件跑了三个优化：
- HF/STO-3G（最低精度）
- B3LYP/cc-pVDZ（合理精度，带 freq）
- CCSD/cc-pVTZ（高精度）

报告各自优化后的基态总能量（搜 `SCF Done` / `Wavefunction amplitudes ... ECCSD`），
比较数值差异，说明为什么（HF 缺相关能 → 偏高；B3LYP 近似相关；CCSD 系统性好）。

### 2) 电子密度 + 静电势图（B3LYP/cc-pVDZ）
`formchk ch2fcl_b3lyp_ccpvdz.chk` → GaussView 打开 `.fchk`：
- Results → Surfaces/Contours → New Surface: **Total Density**（isovalue ≈ 0.0004）
- 然后 Surface Actions → **Map** → Electrostatic Potential
- 截图放报告，说明 F、Cl 端电负性高 → 负电位（红），H 端正电位（蓝）

### 3) C–H 和 C–F 键解离能（B3LYP/cc-pVDZ）
`02_ch2fcl_fragments_bde.gjf` 跑了 4 个片段（全部 opt+freq，UB3LYP）：
CHFCl·（脱一个 H）、CH₂Cl·（脱 F）、H 原子、F 原子。

**策略 = 均裂（homolytic），几何完全弛豫，加零点能校正：**

```
BDE(C–H) = [E(CHFCl·) + ZPE + E(H·)]  −  [E(CH₂FCl) + ZPE]
BDE(C–F) = [E(CH₂Cl·) + ZPE + E(F·)]  −  [E(CH₂FCl) + ZPE]
```

- 电子能量：搜 `SCF Done`
- ZPE：搜 `Zero-point correction=`（Hartree）。也可以直接用 `Sum of electronic and zero-point Energies=`
- 换算：1 Hartree = 2625.50 kJ/mol
- **哪个原子最容易脱** = BDE 更小的那个。CH₂FCl 里通常 C–F 比 C–H 强 → **H 更容易脱**，
  但以你算出来的数为准，并说明理由（自由基稳定性、键强）。

> 报告里要写清“What computational strategy do you use” = 上面这段（均裂 + 弛豫片段 + ZPE 校正）。

## 跑法
```bash
qsub submit_ex3.pbs
```
