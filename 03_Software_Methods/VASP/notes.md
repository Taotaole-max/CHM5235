# VASP 笔记

对应 **HW4（15%）**：VASP + VESTA / vaspkit / py4vasp

商业闭源软件 https://www.vasp.at ，课程提供预编译可执行文件与运行脚本。

## 和前三个软件的根本区别

Gaussian / ORCA / OpenMOLCAS 算的是**孤立分子**，用的是**原子轨道基组**（高斯函数）。

VASP 算的是**周期性固体**——晶体在三个方向上无限重复。它用：
- **平面波基组**（天然适合周期性）+ **赝势 (PAW)**（把内层电子冻结，只算价电子）
- **k 点取样**：周期性体系的电子态是波矢 k 的函数，必须在倒空间取样求和

所以概念全部要换一套：没有"分子轨道"只有"能带"，没有"HOMO-LUMO gap"只有"带隙"，
基组大小不由"用什么基组"决定而由 **ENCUT（截断能）** 决定。

课程要求的三类体系：**固体周期性材料、2D 层状材料、表面分子吸附**。

> ⚠️ 待确认 — 集群模块名：`________`　POTCAR 库路径：`________`　可执行文件：`________`

## 四个输入文件

见 `templates/README.md`。核心记忆点：**POTCAR 的元素顺序必须匹配 POSCAR，错了不报错但结果全废**。

## INCAR 关键参数

### 决定精度的
| 参数 | 含义 | 建议 |
|---|---|---|
| `ENCUT` | 平面波截断能 (eV)，相当于"基组大小" | ≥ POTCAR 最大 ENMAX × 1.3；变胞优化时更要给足 |
| `PREC` | 精度档位 | `Accurate` |
| `EDIFF` | 电子步收敛判据 | 弛豫 1E-6，静态 1E-8 |
| `EDIFFG` | 离子步收敛判据 | 负值 = 力判据 (eV/Å)，用 -0.01 或 -0.02 |

### 决定"算什么"的
| 参数 | 含义 |
|---|---|
| `ISTART` | 0=从头；1=读 WAVECAR |
| `ICHARG` | 2=原子电荷叠加作初猜；**11=固定读 CHGCAR 做非自洽**（能带/DOS 的标志） |
| `IBRION` | -1=不动原子；2=共轭梯度优化；5=有限差分算频率；0=分子动力学 |
| `ISIF` | 2=只动原子；3=原子+晶胞全动；**4=动原子和形状但保持体积（2D 材料用）** |
| `NSW` | 最大离子步数，静态计算设 0 |

### 电子占据（ISMEAR，最容易选错）
| 值 | 用于 | 说明 |
|---|---|---|
| `0` | 半导体、分子、**不确定时** | 高斯展宽，SIGMA=0.05，最安全 |
| `1` / `2` | 金属 | Methfessel-Paxton，SIGMA=0.1~0.2 |
| `-5` | **最终的精确 DOS 和总能** | 四面体法+Blöchl 校正，最准，但**不能用于结构弛豫**（力不准）且要求 k 点足够多 |

判断标准：算完检查 OUTCAR 里的 `entropy T*S`，**每个原子应 < 1 meV**，否则 SIGMA 太大。

### 并行
- `NCORE`：每条能带用几个核。经验值 ≈ √(总核数)，或取每节点核数的因子。设错会显著变慢
- `KPAR`：k 点并行组数，k 点多时开

### 特殊体系
| 场景 | 必加的参数 |
|---|---|
| 2D 材料 / 层状 | `IVDW = 12`（DFT-D3 BJ 色散）；`ISIF = 4`；真空层 ≥ 15 Å |
| 表面吸附 | `IDIPOL = 3` + `LDIPOL = .TRUE.`（偶极修正，消除周期镜像间的静电作用） |
| 磁性体系 | `ISPIN = 2` + `MAGMOM`（给每个原子初始磁矩） |
| 过渡金属氧化物 | `LDAU = .TRUE.` 等一套 DFT+U 参数（纯 GGA 会严重低估带隙） |

## 标准工作流（HW4 的骨架）

```
收敛测试 (ENCUT, k点)
   ↓
1. 结构弛豫    ISIF=3, IBRION=2      → 产物 CONTCAR
   ↓  ★ cp CONTCAR POSCAR
2. 静态 SCF    NSW=0, LCHARG=.TRUE.  → 产物 CHGCAR
   ↓
3. 能带  ICHARG=11 + KPOINTS 线模式   → EIGENVAL / PROCAR
4. DOS   ICHARG=11 + 更密的网格        → DOSCAR
```

**`cp CONTCAR POSCAR` 这一步忘了，后面全是在算未优化的结构。**

## 收敛测试（做 HW4 前必须做，也是报告里的得分点）

VASP 的结果**没有"默认就对"这回事**，ENCUT 和 k 点密度都必须自己测：

```bash
# ENCUT 测试：固定 k 点，扫 ENCUT
for E in 300 350 400 450 500 550 600; do
  mkdir -p enc_$E && cd enc_$E
  cp ../{POSCAR,POTCAR,KPOINTS} .
  sed "s/^ENCUT.*/ENCUT = $E/" ../INCAR > INCAR
  # 提交作业
  cd ..
done
# 收敛标准：总能变化 < 1 meV/atom
```

k 点测试同理，扫 Gamma 网格密度。**报告里放这两张收敛曲线图，是标准做法。**

## 后处理工具

### VESTA（结构可视化，免费）
读 `POSCAR` / `CONTCAR` / `CHGCAR`。用来：建结构、看晶胞、切表面、加真空层、
画电荷密度等值面和差分电荷密度。**建 POSCAR 最方便的方式就是 VESTA 里画完导出。**

### vaspkit（命令行后处理，免费）
把 VASP 那堆难读的输出变成能直接画图的数据文件。

```bash
vaspkit              # 交互式菜单，第一次用它熟悉功能编号
vaspkit -task 102    # 也可以非交互直接调用
```

常用功能分类（**具体编号以你装的版本菜单为准，第一次跑的时候确认并回填这里**）：

| 功能 | 编号（待确认） |
|---|---|
| 生成 INCAR | `101` |
| 生成 KPOINTS | `102` |
| 生成 POTCAR | `103` |
| 总态密度 DOS | `211` |
| 投影态密度 PDOS | `213` |
| 能带结构 | `251` |
| 投影能带 | `252` |

> ⚠️ 待确认 — 我这版 vaspkit 的实际编号：`________`

vaspkit 还会**自动帮你把费米能级移到 0**，省掉手工对齐的麻烦。

### py4vasp（Python 后处理，免费）
读 `vasprun.xml`，在 Python 里直接画图，适合做批量分析和自定义图。

```bash
pip install py4vasp
```
```python
from py4vasp import Calculation
calc = Calculation.from_path("./2_scf")
calc.dos.plot()
calc.band.plot()
```

本机已有 Python 3.13，`pip install py4vasp` 应该可以直接装（建议开虚拟环境）。

## 结果怎么读

```bash
grep "free  energy   TOTEN" OUTCAR | tail -1     # 最终总能 (eV)
grep "E-fermi" OUTCAR                             # 费米能级
grep "reached required accuracy" OUTCAR           # 出现这句 = 离子步收敛
tail -20 OSZICAR                                  # 看收敛过程
grep -A5 "TOTAL-FORCE" OUTCAR | tail -20          # 各原子受力
```

**没有 `reached required accuracy` 就是没优化完**，`CONTCAR` 不能用。
