# ORCA 笔记

对应 **HW2（15%）**：ORCA + Avogadro / Chemcraft

## 安装 / 环境

- 闭源但**学术免费**：https://orcaforum.kofo.mpg.de/filebase/ （需注册 ORCA Forum 账号）
- **没有 GUI**，纯命令行。可视化交给 Avogadro / Chemcraft / Multiwfn
- HPC@NUS 已有 ORCA 6 模块
- 注册 Forum 账号仍然值得——**官方手册（1000+ 页）在那里下载，是最好的参考资料**

> ⚠️ 待确认 — 集群模块名：`________`　`which orca` 绝对路径：`________`

## 输入文件结构

比 Gaussian 自由得多，没有严格的段落和空行要求：

```
! 关键字行              ← ! 开头，可以写多行，都会被合并
%块设置 ... end         ← % 开头的块，细粒度控制
* xyz 电荷 多重度       ← 坐标块，以 * 开始和结束
  元素 x y z
*
```

`#` 开头是注释。**没有"结尾必须空行"这种坑**，比 Gaussian 友好。

## 关键字含义

| 关键字 | 含义 |
|---|---|
| `Opt` / `Freq` | 优化 / 频率，同 Gaussian |
| `TightSCF` | 收紧 SCF 收敛判据。**算频率和性质时应该开** |
| `D4` | Grimme D4 色散校正（D3 也可写 `D3BJ`）。ORCA 里加色散几乎无代价，建议默认加 |
| `RIJCOSX` | 库仑用 RI 近似、交换用 COSX 数值积分。杂化泛函提速 5–10 倍且几乎不损精度 |
| `def2/J` | RIJCOSX 需要的辅助基组，**和 def2 系列基组配套使用，必须写** |
| `UKS` | 非限制性 Kohn-Sham，开壳层体系用 |
| `xyzfile` | 从外部 `.xyz` 文件读坐标，省得粘贴 |

### 常用块

| 块 | 用途 |
|---|---|
| `%pal nprocs N end` | 并行核数，**必须等于 PBS 的 ncpus** |
| `%maxcore N end` | **每个核**的内存上限（MB），不是总内存！总量 = nprocs × maxcore |
| `%scf ... end` | SCF 控制，破对称 `BrokenSym` 在这里 |
| `%tddft ... end` | TD-DFT 设置 |
| `%geom ... end` | 优化控制（约束、最大步数等） |

**`%maxcore` 是每核内存**——这是 ORCA 最容易搞错的一件事。写 `%maxcore 3000` + `nprocs 8`
意味着要 24GB，PBS 里只申请了 8GB 的话必然被杀。

## 与 Gaussian 的对照（写报告时的对比素材）

| 任务 | Gaussian | ORCA |
|---|---|---|
| 优化+频率 | `#p B3LYP/6-31G(d) opt freq` | `! B3LYP def2-SVP Opt Freq` |
| 并行 | `%nprocshared=8` | `%pal nprocs 8 end` |
| 内存 | `%mem=6GB`（总量） | `%maxcore 3000`（每核） |
| 开壳层 | 多重度 ≠ 1 自动 UDFT | 显式写 `UKS` 更清楚 |
| 色散 | `EmpiricalDispersion=GD3BJ` | `D4` |
| BS-DFT | 手工两步 + `guess=(fragment=n)` | `%scf BrokenSym 5,5 end` 一步搞定 |
| J 值 | 自己套 Yamaguchi 公式算 | **输出里直接给**（多种公式并列） |

课程让你用两个软件做同样的任务，报告里**结果差异的讨论**是得分点：
同样 B3LYP/def2-SVP 下能量差异应该在 μHartree 量级；若差别明显，通常是
积分格点、RI 近似、SCF 收敛判据、或色散校正不一致造成的。

## 结果怎么读

```bash
grep "FINAL SINGLE POINT ENERGY" mol.out | tail -1   # 最终能量 (Hartree)
grep "HURRAY" mol.out                                 # 优化收敛的标志（真的是这个词）
grep -A20 "VIBRATIONAL FREQUENCIES" mol.out           # 频率，虚频显示为负数
grep -A15 "ABSORPTION SPECTRUM" mol.out               # TD-DFT 的激发能与振子强度
```

**BS-DFT 的 J 值**：搜 `Exchange couplings` 或 `J(1,2)`，ORCA 会用几种不同公式各给一个值。
报告里要写清楚你引用的是哪一个（推荐 Yamaguchi），以及用的是 Ĥ = −2J·Ŝ₁·Ŝ₂ 还是 Ĥ = −J·Ŝ₁·Ŝ₂ 约定。

## 可视化

ORCA 输出的轨道在 `.gbw` 文件里（二进制）。转成能看的格式：

```bash
orca_2mkl mol -molden     # 生成 mol.molden.input，可被 Avogadro / Multiwfn / Chemcraft 读
orca_plot mol.gbw -i      # 交互式生成 cube 文件（轨道、密度、自旋密度）
```

- **Avogadro**（免费，https://avogadro.cc）：建分子、看轨道，适合日常
- **Chemcraft**（商业，150 天试用）：出图质量高，适合放进报告
- **Multiwfn**（免费，http://sobereva.com/multiwfn/）：波函数分析的瑞士军刀，
  作者是中国人、文档和论坛都是中文，做原子电荷/轨道局域化分析时强烈推荐
