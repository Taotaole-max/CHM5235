# Ex5 Cu₂ 配合物的磁交换常数 J：BS-DFT，非相对论 / DKH / ZORA

题目要求：用 BS-DFT 算给定 Cu₂ 配合物中两个 Cu(II)（d⁹，各 S = 1/2）之间的磁交换 J，总电荷 −2；
再分别用 DKH（DKH-def2-SVP）和 ZORA（ZORA-def2-SVP）加上相对论效应重算。
列表比较三次的总能量和 J，说明相对论效应对 J 的影响有多大。

## 现在有的文件

```
Ex5_Cu2_BSDFT/
├── Ex5_说明.md                          本文件
├── ex5_Cu2_geometry_from_canvas.xyz     Cu₂ 配合物结构（Canvas 原文件的副本，没改过）
├── ex5_submit_3_methods.sh              提交脚本：一条命令交三个作业
├── ex5_run_one_method.pbs               作业脚本：跑一种处理，跑完自动检查、归档
├── nonrelativistic/  ex5_bsdft_nonrelativistic.inp   ORCA 输入：非相对论（def2-SVP）
├── DKH/              ex5_bsdft_DKH.inp               ORCA 输入：DKH（DKH-def2-SVP）
└── ZORA/             ex5_bsdft_ZORA.inp              ORCA 输入：ZORA（ZORA-def2-SVP）
```

- `ex5_Cu2_geometry_from_canvas.xyz`：题目给的结构，直接用，不做优化（题目只要求在这个结构上算 J）。
- `ex5_submit_3_methods.sh`：在集群上运行它。三个作业互不依赖，同时排队。
- `ex5_run_one_method.pbs`：不用手动运行。它做三件事：跑 ORCA → 把 BS 分析（能量、⟨S²⟩、J）打到日志里 →
  把 ORCA 的中间文件收进 `orca_raw_files/`。
- 三个 `.inp`：泛函和基组大小相同，只差相对论处理和对应的基组。

## 算完之后，每个子文件夹里会有什么

以 `DKH/` 为例：

| 文件 | 干什么用 |
|---|---|
| `ex5_bsdft_DKH.inp` | 输入（不变） |
| `ex5_bsdft_DKH.out` | ORCA 主输出。高自旋和破缺对称两个态的总能量、⟨S²⟩、Cu 上的自旋布居、J 都在这里 |
| `ex5_pbs_log_DKH.txt` | 作业日志，里面直接有 BS 分析那一段（E_HS、E_BS、⟨S²⟩、J），一眼能看到结果 |
| `orca_raw_files/` | ORCA 的中间文件（波函数 .gbw 等），一般不用打开 |

## 怎么跑

`bash Ex5_Cu2_BSDFT/ex5_submit_3_methods.sh`（在集群上 `~/CHM5235/as2` 里运行）。
每个作业单核、10 GB、限时 12 小时；66 个原子、两个 SCF，预计 1–4 小时。

## 设置和理由

- 关键字：`! UKS B3LYP <基组> <辅助基组> RIJCOSX TightSCF SlowConv`，`%scf BrokenSym 1,1 end`，
  坐标行 `* xyzfile -2 3`。
  - 非相对论：`def2-SVP` + `def2/J`
  - DKH：`DKH DKH-def2-SVP` + `SARC/J`
  - ZORA：`ZORA ZORA-def2-SVP` + `SARC/J`（相对论计算用全电子的 SARC/J 作辅助基组）
- **三组用同一个泛函和同样大小的基组**：题目没说非相对论那组用什么，这里取 B3LYP/def2-SVP，
  这样三组之间只差相对论处理这一项，表格才能直接比较。报告里要写一句说明这个选择。
- **BrokenSym 1,1 在做什么**：两个 Cu 各有 1 个未成对电子。ORCA 先收敛"两个自旋都朝上"的高自旋态（三重态），
  再把其中一个 Cu 上的自旋翻过来，收敛"一上一下"的破缺对称态，由两者的能量差求 J。
  坐标行要写**高自旋**的多重度：2×(1/2+1/2)+1 = 3。
- **J 的符号约定**：ORCA 用 H = −2J S₁·S₂，J < 0 是反铁磁（两个自旋倾向反平行）。
  输出里 J(1)、J(2)、J(3) 是三个公式的结果，J(3) 就是 Yamaguchi 公式
  J = (E_BS − E_HS)/(⟨S²⟩_HS − ⟨S²⟩_BS)，讲义 L05 用的就是它（讲义 p42/43 的符号有笔误，以这个为准）。
- **SlowConv**：过渡金属开壳层体系的 SCF 容易振荡，加阻尼让它稳一点，代价是多迭代几轮。
- **为什么总电荷是 −2**：结构是"桨轮"型，4 个三氟乙酸根 CF₃COO⁻ 桥连两个 Cu（Cu–Cu 2.73 Å），
  每个 Cu 轴向上还配位一个 C₅H₁₁O₂ 配体。2 个 Cu²⁺ + 4 个 CF₃COO⁻ 本身是中性的；
  轴向配体和 Cu 配位的那个 O 只连着一个 CH₂、上面没有 H（晶体结构里常定位不到羟基氢），
  题目把它当成带一个负电的烷氧基，所以总电荷 −2。电子数 394 是偶数，能组成三重态，自洽。
- **预期**：Cu 是第一过渡系（Z = 29），相对论效应不大，三组的 J 应该差得不多；
  总能量会差得比较多（主要来自内层电子），但 J 取的是两个态的能量差，这部分会大体抵消。

## 题目之外补做的验证（2026-09-20/21）

| 文件夹 | 干什么用 |
|---|---|
| `verify_nonrelativistic/`、`verify_DKH/`、`verify_ZORA/` | 三个必做计算加密格点重算（DefGrid3 + VeryTightSCF），J 只变 0.1 cm⁻¹ 左右 → 格点误差可以排除 |
| `PBE0/`、`TPSSh/` | 换泛函（25% / 10% HF 交换），非相对论 SVP：J 随 HF 比例单调变化，跨度约 200 cm⁻¹ |
| `TZVP_nonrel/`、`TZVP_DKH/`、`TZVP_ZORA/` | 基组加大到 TZVP 级：三个都是反铁磁，DKH 与 ZORA 一致到 0.003 cm⁻¹，相对论让 J 加强约 49 cm⁻¹ |
| `ex5_analysis/ex5_extract_J.py` | 从以上全部输出里提取能量、⟨S²⟩、J，生成 `ex5_results_table.md` |

结论：SVP 下"加相对论后 J 变号"是基组太小造成的假象；基组够大时相对论效应是约 −49 cm⁻¹（|J| 的 60% 左右），
DKH 和 ZORA 给出相同结果；决定 J 数值的最大因素是泛函。
