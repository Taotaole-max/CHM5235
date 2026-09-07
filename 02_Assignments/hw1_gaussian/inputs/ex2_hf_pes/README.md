# Ex2 — H–F 分子势能面，4 方法（5 分）

## 方法（都用 cc-pVTZ，spin-unrestricted）

| 文件 | 方法 |
|---|---|
| `hf_scan_uhf.gjf`    | UHF |
| `hf_scan_ub3lyp.gjf` | UB3LYP |
| `hf_scan_uccsd.gjf`  | UCCSD |
| `hf_scan_uccsdt.gjf` | UCCSD(T) |

扫描：R(H–F) 从 0.50 到 10.00 Å，步长 0.01 Å（951 点，rigid scan）。

## ⚠️ 关键坑：`guess=mix`

H–F 均裂解离成 **两个开壳层原子（H· + F·）**。限制波函数（或没打破 α/β 对称的非限制）
在长键极限会给出**离子对 H⁺F⁻**，能量偏高几百 kJ/mol，曲线尾巴翘上去——整道题的 (c)(d) 就废了。
四个输入都加了 `guess=mix`（打破 α/β 空间对称）。跑完检查：**R > 8 Å 时能量应基本变平**。
若某个方法尾巴仍不平，把那一段（如 R 5–10 Å）单独重跑并加 `stable=opt`。

## 要交什么

- **a)** 一张图，四条 PES 曲线叠加，E = f(R)。用 `extract_pes.sh` 提数 → `plot_pes.py` 出图。
- **b)** 每个方法的平衡键长 R_e（能量最低点）。
- **c)** 每个方法的解离能 D_e = E(R→∞) − E(R_e)，换算成 kJ/mol。
- **d)** 与实验 BDE(H–F) = 568.6 kJ/mol 对比，讨论哪个方法最准。
  预期：**CCSD(T) ≈ CCSD > B3LYP > UHF**；UHF 严重低估（缺动态相关），
  且 UHF 在中等键长有非物理的“肩膀”（自旋污染 + Coulson–Fischer 点）。

## 跑法

```bash
qsub submit_ex2.pbs
# 回本地后：
bash extract_pes.sh && python plot_pes.py
```
