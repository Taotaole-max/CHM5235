# Gaussian 笔记

对应 **HW1（15%）**：Gaussian + GaussView

## 安装 / 环境

- HPC@NUS 已预装 → `module avail 2>&1 | grep -i gaussian`
- Windows 笔记本可申请安装包（需签使用协议后向老师索取）
- Mac 需 Windows 虚拟机（Parallels / VMware Fusion / VirtualBox）

> ⚠️ 待确认 — 集群模块名：`________`　可执行文件：`g16` / `g09`？`________`

## 输入文件的五段结构

Gaussian 输入文件是**严格分段**的，段与段之间用**空行**隔开，顺序不能变：

```
%chk=mol.chk              ← 1. Link 0：资源与文件设置（% 开头）
%mem=6GB
%nprocshared=8
#p B3LYP/6-31G(d) opt freq  ← 2. Route section：算什么（# 开头）
                          ← 空行
Title                     ← 3. 标题，随便写但不能省
                          ← 空行
0 1                       ← 4. 电荷 自旋多重度
O  0.0  0.0  0.117        ←    坐标
H  0.0  0.757 -0.469
H  0.0 -0.757 -0.469
                          ← 5. 结尾必须有空行！
```

**最后一行空行漏掉是最高频的报错来源**，现象是作业秒退、日志几乎为空。

## 关键字含义

### Route section 常用

| 关键字 | 含义 |
|---|---|
| `#p` | 输出详细信息（`#` 是普通，`#t` 是简略）。调试期用 `#p` |
| `opt` | 几何优化。`opt=tight` 更严格；`opt=(calcfc)` 先算力常数，难收敛时用 |
| `freq` | 振动频率分析。**必须在与 opt 相同的方法/基组下做**，否则无意义 |
| `freq=noraman` | 不算拉曼强度，省时间 |
| `TD(NStates=10)` | TD-DFT，算 10 个激发态 |
| `geom=check` | 从 `.chk` 读几何结构（配合 `%oldchk`） |
| `guess=read` | 从 `.chk` 读初始波函数，省一次 SCF |
| `guess=(fragment=n)` | 按片段构造初始猜测——**BS-DFT 的关键** |
| `pop=full` | 打印完整布居分析（原子电荷、轨道组成） |
| `scrf=(pcm,solvent=water)` | 隐式溶剂 |
| `stable=opt` | 检查波函数稳定性并重优化，开壳层体系值得一做 |

### 泛函与基组的选择逻辑

- **B3LYP**：默认起手式，有机分子几何和频率都够用
- **B3LYP-D3 / ωB97XD**：体系有色散作用（π 堆积、弱相互作用）时必须加
- **6-31G(d)**：优化用的经济基组
- **6-311+G(d,p)**：单点能/激发态用，`+` 是弥散函数——**阴离子和激发态必须加**
- **def2-TZVP**：含过渡金属时用，因为它自带赝势 (ECP)

规矩：**小基组优化几何 → 大基组算单点性质**，这是标准做法也是省机时的关键。

## 电荷与自旋多重度

`0 1` = 电荷 0、多重度 1（闭壳层单重态）。
多重度 = 2S + 1 = 未成对电子数 + 1。
- 单重态（全配对）= 1
- 双重态（1 个未成对，自由基）= 2
- 高自旋 Mn(II) d⁵（5 个未成对）= 6

**写错多重度是"算完但结果离谱"的头号原因**，且程序不会报错。

## 结果怎么读

### 优化收敛了吗
在 `.log` 里搜：
```bash
grep -A4 "Converged?" mol.log | tail -8      # 四个判据要全是 YES
grep "Stationary point found" mol.log        # 找到这句 = 优化成功
```

### 有虚频吗
```bash
grep -A3 "Frequencies --" mol.log | head
```
- **0 个虚频（全正）** = 真正的极小点 ✅
- **1 个虚频** = 过渡态。如果你想要极小点，说明优化到鞍点了，需要沿虚频模式扰动结构重优化
- **多个虚频** = 结构有问题，重来

虚频在输出里显示为**负数**频率。

### 能量在哪
```bash
grep "SCF Done" mol.log | tail -1            # 电子能量 (Hartree)
grep "Sum of electronic and thermal Free Energies" mol.log   # 吉布斯自由能
```
单位换算：1 Hartree = 627.5095 kcal/mol = 27.2114 eV = 2625.5 kJ/mol

## BS-DFT 算磁交换常数 J

用于双核过渡金属配合物，判断两个金属中心是**铁磁 (F)** 还是**反铁磁 (AF)** 耦合。

**做法**：算两个态的能量
1. **HS（高自旋）**：两个局域自旋平行，多重度 = 2(S₁+S₂)+1
2. **BS（破对称）**：一个中心的自旋翻转，用 `guess=(fragment=2)` 且第二个片段多重度写**负数**

见 `templates/03_bs_dft.gjf`（一个文件用 `--Link1--` 连做两步）。

**Yamaguchi 公式**（最稳健，自旋污染大时也适用）：

```
J = (E_BS − E_HS) / (⟨S²⟩_HS − ⟨S²⟩_BS)
```

Hamiltonian 约定 Ĥ = −2J·Ŝ₁·Ŝ₂ 时，**J > 0 铁磁，J < 0 反铁磁**。
⚠️ 不同文献的 Hamiltonian 约定差一个因子 2，**写报告时一定要写明你用的是哪个约定**。

在 `.log` 里取 ⟨S²⟩：
```bash
grep "S\*\*2" mol.log
```

## TD-DFT 激发态

见 `templates/02_td_dft.gjf`。要点：
- **必须在优化好的基态几何上做**（垂直激发）
- 基组要带弥散函数（`6-311+G(d,p)`），否则激发能系统性偏高
- 电荷转移态用 B3LYP 会严重低估，需换长程校正泛函（`CAM-B3LYP` / `ωB97XD`）——这是 TD-DFT 的经典陷阱

读结果：
```bash
grep "Excited State" mol.log
```
输出形如 `Excited State 1: Singlet-A 3.4521 eV 359.15 nm f=0.0234`，
其中 **f 是振子强度**，f≈0 的态在紫外可见光谱上看不到。

## GaussView 用来做什么

- 建分子、改结构、生成 `.gjf`
- 看优化轨迹动画（确认优化过程合理）
- 看**振动模式动画**（确认虚频对应什么运动）
- 画**分子轨道**（HOMO/LUMO）、电子密度、自旋密度等值面
- 画模拟的 IR / UV-Vis 谱

需要 `.chk` 文件。若集群上的 `.chk` 是二进制不通用，用 `formchk mol.chk mol.fchk`
转成文本格式的 `.fchk` 再下载到本地——**这一步经常被忘记**。
