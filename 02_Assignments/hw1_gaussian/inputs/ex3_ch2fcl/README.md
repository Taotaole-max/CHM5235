# Ex3 — CH₂FCl 键解离能（5 分）

分子：**氯氟甲烷 CH₂FCl**（C 上接 2 个 H、1 个 F、1 个 Cl）。

## 要交什么

### 1) 三方法总能量对比
拆成 3 个独立任务并发跑（CH2FCl 比前两题的双原子大，CCSD/cc-pVTZ 优化可能要跑很久，
拆开才能让它和其他任务同时进行，不占用总时间）：
- `01a_ch2fcl_hf_sto3g.gjf`（HF/STO-3G，最低精度，几秒到几分钟）
- `01b_ch2fcl_b3lyp_ccpvdz.gjf`（B3LYP/cc-pVDZ，合理精度，带 freq，几十分钟）
- `01c_ch2fcl_ccsd_ccpvtz.gjf`（CCSD/cc-pVTZ，高精度，**这个最慢，可能要几小时到十几小时**）

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

## 跑法（4 个独立任务，同时提交）
```bash
qsub submit_ex3_hf.pbs
qsub submit_ex3_b3lyp.pbs
qsub submit_ex3_ccsd.pbs
qsub submit_ex3_frags.pbs
qstat -u $USER      # 应该看到 4 个任务号
```
`submit_ex3_ccsd.pbs` 申请了 96 小时 walltime 保底；如果跑了几小时后 `qstat` 里一直是 R
但迟迟不结束，且临近截止日期，可以考虑改成在 `01b` 优化好的 B3LYP 几何上做 CCSD **单点**
（去掉 opt 关键字）而不是重新优化几何，能省下大量时间，报告里注明这个简化即可。
