# Lecture 03：标准软件与可视化工具 + 变分原理 + 基组 + SCF 计算细节

> CM5235 · Liviu Ungur · 81 页
> 讲义原件：`slides/CM5235_Lecture_03.pdf`

## 这一讲在干什么

三块内容，主线是**"从理论方程到能在软件里跑的东西"**：

1. **软件巡览**（p.2–24）：四个主力包 + 一堆其他包 + 可视化工具的优缺点、输入语法
2. **变分原理**（p.25–37）：为什么"更大的基组 / 更多变分参数 = 更好的近似"——整个量子化学的地基
3. **SCF 的计算实现**（p.38–76）：Slater 行列式能量表达式 → Fock 算符 → LCAO → Fock 矩阵 →
   双电子积分 → RI/对称性/DIIS 等加速技巧 → 基组的分类
4. 结尾还点出**单行列式不够用的情形**（B 原子的静态相关）→ 引出 Lecture 04

---

## 一、软件巡览（p.2–24）⭐ 可能出"哪个软件适合什么任务"的题

### 四个主力包

| 包 | 强项 | 弱点 / 注意 |
|---|---|---|
| **Gaussian + GaussView** | 内坐标模块强（复杂扫描、约束、势能面分析）；溶剂化/反应场好；输入语法友好、容错 | 很贵、license 限制严；DFT 最多约 32 核、CISD 约 4 核（不 scale）；Linux/OSX 安装很痛苦 |
| **ORCA** | **光谱性质最强**（NMR、EPR，尤其 ZFS、交换相互作用这些"难"的） | 无对称性因子化；闭源（免费但不开源）；无自带图形界面 |
| **OpenMOLCAS** | **多组态方法最强**（CASSCF/RASSCF/CASPT2/SO-RASSI/ANISO）；过渡金属、镧系、自由基开壳层 | 并行化不好；无自带图形界面（免费 + 开源） |
| **VASP** | **固体计算最好之一**；赝势准确；并行好、开发活跃 | 贵、专有（源码只给 licensed 组）；无自带图形界面。能做 DFT/DFPT/TDDFT/RPA/GW：结构优化、带隙、DOS/PDOS、介电、光学响应、声子 |

**Gaussian 的哲学（p.2）**：不是最省 CPU 的包，但**建一个 Gaussian 任务比任何专家级包都省人力**。
> "CPU 时间 $0.01–0.02/小时，脑力时间 $25+/小时。"

### Gaussian 输入解剖（p.4）⭐ 会考

```
%Mem=16GB              -- RAM
%NProcShared=8         -- 核数
#p opt=tight rb3lyp/cc-pVDZ scf=(tight,dsymm) integral=(grid=ultrafine)
Flavin anion geometry optimization    -- 标题行
-1 1                   -- 总电荷 = -1（阴离子），自旋多重度 = 1（S=0，单重态）
C   0.0  0.0  0.0      -- 原子坐标
...
```

- `opt=tight`：紧收敛几何优化
- `rb3lyp`：自旋**限制**（R）DFT，B3LYP 泛函
- `cc-pVDZ`：correlation-consistent 极化价双 zeta 基组
- `scf=(tight,dsymm)`：紧 SCF 收敛 + 每次 SCF 迭代对称化密度矩阵
- `integral=(grid=ultrafine)`：超细积分格点

### Gaussian 输出（p.5）

`SCF Done: E(RB3LYP) = -2692.65913 A.U. after 9 cycles` —— log 文件很啰嗦、不友好，
建议用 GaussView 看结果。`.chk`（二进制）→ `formchk` 转成文本 `.fchk` → GaussView 的 Results 标签。

### 其他包（p.9–12）

GAMESS（CI 模块强、文档好，但 >32 核不 scale、难装）、ADF（Slater 基、重原子/相对论 DFT 强）、
MOPAC（半经验，能处理巨大体系，含 PM6）、Dalton（CI/CC）、**Turbomole**（最快最精简）、
**NWChem**（并行到上千核，强烈推荐）、Quantum Espresso / CASTEP（平面波固体 DFT）、
ONETEP（线性标度 DFT，大体系）。

在 HPC 上：`module load <名字>`。OpenMOLCAS/VASP/ORCA 的安装脚本在 Canvas/LUMINUS，
下载 → `chmod +x` → `dos2unix`（清 Windows 换行）→ `./script`。

### 可视化（p.16–24）

- **GaussView 6**：极强 GUI，能建 Gaussian 任务 + 解读输出，但只能导出 2D 图，贵
  - **远程用法（p.17）**：`ssh -X` + X11 转发，Mac 需 XQuartz：
    ```
    ssh -X <user>@vanda.nus.edu.sg
    source /app1/ebenv
    module load Gaussian/16.C.02-AVX2
    /app1/common/Gaussian/Rev-C.02/gv/gview.sh
    ```
- **Avogadro**：免费开源，用来看 ORCA 结果（振动频率等），ORCA 打印级别要设成 `large`
- **Chemcraft**：结构编辑强，支持 ORCA，试用 180 天
- **Molden / Jmol / VMD**：VMD 专攻大生物分子

---

## 二、变分原理（p.25–37）⭐⭐ 全课最重要定理之一

### 陈述

对任意算符，用它**真正的基态本征态**算期望值 → 得到最低本征值。
用**近似函数**（非本征态）算 → 结果**总是偏高**：

$$E_{\text{trial}} = \frac{\langle \psi_{\text{trial}}|\hat H|\psi_{\text{trial}}\rangle}{\langle \psi_{\text{trial}}|\psi_{\text{trial}}\rangle} \ge E_{\text{exact}}$$

*读法：拿任何一个近似（试探）波函数算出来的能量期望值，永远 ≥ 真实基态能量。所以"能量越低 = 波函数越好"，可以拿能量当打分标准去优化参数。*

### 证明思路（p.26–27）

把试探函数在哈密顿量的精确本征态里展开 $\psi_{\text{trial}} = \sum_k c_k \varphi_k$，则
$E_{\text{trial}} = \sum_k |c_k|^2 \varepsilon_k$，而 $E_{\text{exact}} = \varepsilon_0$，
于是 $E_{\text{trial}} - E_{\text{exact}} = \sum_k |c_k|^2(\varepsilon_k - \varepsilon_0) \ge 0$。

### 实践中怎么用（p.28）

1. 构造含可调参数的试探波函数 $\psi_{\text{trial}} = \sum_k c_k \varphi_k$
2. 用公式算 $E_{\text{trial}}$
3. **所有 $\partial E / \partial c_i = 0$**，解出最优参数
4. 代回得最低能量

**改进只有两条路**：(a) 增加变分参数（扩大基组）；(b) 换波函数的表示形式。

### 例子：氢原子的非线性变分（p.29–37）

- 试探 $\psi_{\text{trial}} = \sqrt{\alpha^3/\pi}\, e^{-\alpha r}$，算得 $E(\alpha) = \alpha^2/2 - \alpha$，
  $dE/d\alpha = 0 \Rightarrow \alpha = 1$，**恰好还原精确 1s 波函数**（运气好）
- 换个当不成精确解的形式 $\psi_{\text{trial}} = \sqrt{\alpha^5/3\pi}\, r\, e^{-\alpha r}$：
  得 $\alpha = 3/2$，$E = -3/8$ a.u.——在真基态（$-1/2$）之上、第二本征值（$-1/8$）之下
- **投影操作**求各本征态的权重：$c_{1s} = \int \psi_{1s}^* \psi_{\text{trial}}\, d\tau$，
  这里算出 1s 的权重约 **99.55%**（$c_{1s}^2$）

---

## 三、SCF 的计算实现（p.38–76）

### Slater 行列式能量（p.38–45）

用 H₂ 最小基组做完整推导（40 页把单电子积分逐项展开——考试不会让你抄，
但要知道**结论**）：

$$E = \sum_i h_{ii} + \sum_{i}\sum_{j>i}(J_{ij} - K_{ij}) + V_{nn}$$

*读法：总能量 = Σ 单电子项（动能 + 电子-核吸引，记作 $h_{ii}$）+ Σ 电子对之间的（库仑排斥 $J_{ij}$ − 交换 $K_{ij}$）+ 核-核排斥 $V_{nn}$。*

- $J_{ij}$（Coulomb）：**对所有电子对都非零**，不管自旋
- $K_{ij}$（Exchange）：**只对同自旋电子对非零**，无经典对应

练习：给几个 Slater 行列式凭观察写能量表达式。**a)、b) 两个行列式的能差 = 磁交换相互作用 $K_{12}$
→ Broken-Symmetry HF/DFT**（HW1/HW2 会用）。

### Fock 算符与轨道（p.46）

$$\hat F_i = \hat h_i + \sum_{j\ne i}(\hat J_j - \hat K_j), \qquad \hat F_i \varphi_i = \varepsilon_i \varphi_i$$

*读法：Fock 算符 = 单电子项 + 其他所有电子产生的平均（库仑 − 交换）场。它作用在轨道 $\varphi_i$ 上得到 $\varepsilon_i \varphi_i$ —— 即轨道是 Fock 算符的本征函数，轨道能 $\varepsilon_i$ 是本征值。*

- HF 轨道能 = Fock 算符的本征值
- 收敛后的轨道叫**正则分子轨道（canonical MO）**，此时 Fock 矩阵对角
- 同一 HF 波函数有多套轨道（任意酉变换都给相同总能量）
- **自然轨道**：对角化单电子密度矩阵得到

### Koopmans 定理（p.47–48）⭐ 会考

用 N 电子体系的轨道去算 (N±1) 电子体系的能量（假设轨道不变）：

$$E_N - E_{N-1} = \varepsilon_i \quad(\text{从轨道 } i \text{ 电离所需能量} = -\varepsilon_i)$$
$$E_{N+1} - E_N = \varepsilon_a \quad(\text{往空轨道 } a \text{ 加电子})$$

*读法：假设加/减一个电子时其他轨道纹丝不动，那么"从占据轨道 i 拔走一个电子"要付出的能量正好等于 $-\varepsilon_i$；"往空轨道 a 塞一个电子"释放/吸收的能量等于 $\varepsilon_a$。*

即 **HOMO 轨道能 ≈ −电离能，LUMO 轨道能 ≈ −电子亲和能**（冻结轨道近似下）。

### B 原子：单行列式的失败（p.49–50）⭐ 重要概念

B 基态组态 $1s^2 2s^2 2p^1$，2p 三重简并 → **三个 Slater 行列式等价**，
真波函数是三者的线性组合。**HF 只优化一个行列式的轨道 → 对 B 原子不适用**，
必须用 CASSCF。这是典型的**静态电子相关**问题。

### RHF / ROHF / UHF（p.51–53）⭐ 会考

| 方法 | 特点 |
|---|---|
| **限制（R）** | 强制 α、β 空间部分相同（每个占据 MO 两个电子），α 密度 = β 密度 |
| **非限制（U）** | α、β 两套独立 MO。开壳层体系首选；**解离极限描述对**（但"对的理由是错的"） |
| **ROHF** | 限制的开壳层版本 |

- RHF 更快（积分少），但**断键过程失败**（H₂ 解离给出离子对而非两个自由基）
- UHF 断键对，但有**自旋污染**：波函数不是总自旋算符的本征态
  $$\langle \hat S^2\rangle_{\text{UHF}} \ge S(S+1) = \frac{n_{\text{unpair}}}{2}\left(\frac{n_{\text{unpair}}}{2}+1\right)$$

  *读法：理想情况下 $\langle \hat S^2\rangle$ 应等于 $S(S+1)$（S = 未成对电子数的一半）。UHF 算出来的值总是**偏大**，多出来的部分就是自旋污染的量。软件在 SCF 结束时会打印这个值，用来判断污染严重不严重。*

- 处理自旋污染：annihilation（SCF 后投掉）/ projection（SCF 内投掉）/ spin constraint（拉格朗日约束）
- **HF 里大的自旋污染 = 单行列式是坏近似的信号 → 该上 MCSCF**

### 基组近似 → Roothaan-Hall（p.54–61）

MO 写成原子轨道的线性组合 $\varphi_i = \sum_\alpha c_{i\alpha}\chi_\alpha$，HF 方程变矩阵形式：

$$\mathbf{FC} = \mathbf{SC}\varepsilon$$

*读法：把"解微分方程求轨道"变成"解矩阵方程求系数"。F 是 Fock 矩阵，S 是基函数的重叠矩阵，C 是要求的展开系数（每一列一个 MO），ε 是对角的轨道能矩阵。这是个广义本征值问题，计算机拿手。*

- $F_{\alpha\beta} = \langle\chi_\alpha|\hat F|\chi_\beta\rangle$ Fock 矩阵，$S_{\alpha\beta} = \langle\chi_\alpha|\chi_\beta\rangle$ 重叠矩阵
- 密度矩阵 $D_{\gamma\delta} = \sum_j^{\text{occ}} c_{\gamma j} c_{\delta j}$
- $\mathbf F = \mathbf h + \mathbf G(\mathbf D)$ —— **Fock 矩阵依赖于密度，而密度又来自解 Fock 矩阵 → 必须自洽迭代**

### SCF 循环（p.60）

初猜密度矩阵 → 建 Fock 矩阵 → 对角化 → 新密度矩阵 → 迭代到 (a) 能量不变 (b) 密度矩阵不变。
**收敛判据背后是变分原理。**

- $D_{\gamma\delta}$ 对角 → 自然轨道，对角值 = 占据数（RHF 是 2,2,2,…）
- $F_{\alpha\beta}$ 对角 → 正则轨道，对角值 = 轨道能

### 双电子积分（2-ERI）是瓶颈（p.62–64）

$\langle\chi_\alpha\chi_\gamma|\mathbf g|\chi_\beta\chi_\delta\rangle$ —— 四中心积分数目组合爆炸，
**比苯大的分子就存不进内存**。

- **Conventional**：预算好存盘（只算一次，但受磁盘随机访问带宽限制）
- **Direct**：边算边用（每个用 4–16 次，但只需存基组描述）
- **Semi-direct**：折中，post-HF 方法用，SSD 上快
- **半经验方法 = 部分忽略双电子积分**

### RI / 密度拟合 / Cholesky（p.64）⭐

用单位算符分解 $\hat 1 = \sum_P |P\rangle\langle P|$（拟合基组 $P,Q$ 有限且远小于原始基函数乘积数）
把 4 指标积分拆成 3 指标：**HF 标度从 N⁴ 降到 N³ 甚至更低**。Cholesky 分解是 RI 的一种特例。

### SCF 收敛加速（p.65–68）⭐ 实操必备

1. **外推**：用前 3–5 次迭代的 Fock 矩阵外推
2. **阻尼**：$D^{\text{new}} = \omega D_n + (1-\omega)D_{n-1}$
3. **能级移动（level shifting）**：人为拉大 HOMO-LUMO 间隙 → 减少占据/空轨道混合 →
   保证收敛，但可能收到局域极小
4. **DIIS**（Direct Inversion of Iterative Subspace）：$F_{n+1} = \sum_i c_i F_i$，
   系数由最小化误差 $\text{Trace}[(FDS - SDF)^2]$ 求出（约束 $\sum c_i = 1$）——**最常用**
5. Newton-Raphson / 共轭梯度：用轨道梯度和 Hessian，近极小时收敛好，Hessian 贵，DIIS 失败时备用

### 对称性（p.69）

分子有对称性 → 用点群操作生成 SALC 作初猜；Fock/核哈密顿/双电子积分/密度矩阵变**块对角** →
省空间、乘法更快、收敛更好。

### 基组分类（p.70–76）⭐⭐ 会考

**Slater 型（STO）vs Gaussian 型（GTO）**：STO 物理上更对（尖点、渐近行为），
但 GTO 有一个杀手锏——**两个 Gaussian 的乘积还是 Gaussian（在重心处）→ 所有双电子积分解析可算**，
比数值积分快得多。用几个 GTO **拟合**一个 STO（contraction）。

GTO 缺点：远处衰减太快（大距离渐近行为错）、原点处导数为零（小距离行为错）、
基函数固定在核上 → **基组重叠误差（BSSE）**。

| 术语 | 含义 |
|---|---|
| Core / Valence 函数 | 描述内层 / 价层电子（价层参与成键） |
| **Zeta 数** | 价层独立径向基函数的套数（通常 2–4），越多越灵活 |
| **极化函数** | 更高角动量的函数，让 AO 能相对核"极化"偏移 |
| **弥散函数** | 很宽的函数，改善远核区描述，**阴离子必用** |
| Tight 函数 | 紧贴核，为 NMR/ESR 计算改善核区描述 |
| **有效核势（ECP）** | 替代重原子内层轨道（非相对论方法描述不好） |
| Rydberg 函数 | 极度弥散，描述 Rydberg 态 |

命名读法：
- Pople：`6-311G++(3df,3pd)` = 6 个 core Gaussian，价层三 zeta（3/1/1），++ 弥散，(3df,3pd) 极化
- Dunning：`aug-cc-pVTZ` = "augmented correlation-consistent polarized valence triple-zeta"，aug = 加弥散

**更大更灵活的基组 → 对原微分方程更准的矩阵表示 → 更准的结果**（但见 Lecture 04：对能量以外的性质不一定）。

### 精确波函数 = Full CI（p.77–80）→ 引出 Lecture 04

$$\Psi = a_0\psi_{HF} + \sum_{ia} a_i^a \psi_i^a + \sum_{ijab} a_{ij}^{ab}\psi_{ij}^{ab} + \cdots$$

*读法：精确波函数 = HF 行列式 + 所有单激发行列式（各配系数）+ 所有双激发行列式 + …（详见 wk04 同一公式的展开说明）。*

加进激发 Slater 行列式 → 电子开始"感受并躲避"彼此 → **动态相关**。
两大类：单参考（MP2/MP3/MP4、CCSD/CCSDT、CISD/CISDT）、多参考（CASPT2、NEVPT2、MRCI、CASSCF、RASSCF）。

CI 标度：CID O(n⁵)、CISD O(n⁶)、CISDT O(n⁸)、full CI O(n!)。
**CASSCF = 对一个轨道子集（活性空间）做 full CI**，选轨道不是易事（HW3 的命门）。

---

## 四、结尾练习（p.81）

GaussView 画个中等分子（如邻甲酚 o-Cresol）→ 设置：tight 优化 + 自旋非限制 DFT（PBE 泛函）+
ultrafine 格点 + 算频率 → 传到 HPC 跑 → 回来看：所有频率是否为实（正）？为什么重要？优化成功没？
看 HOMO/LUMO、Mulliken 电荷（哪个原子最正/最负）→ 换 RevTPSS 泛函 + 自旋限制再做一遍，对比频率差异。

---

## 与后续课程/作业的连接

| 这一讲 | 用在哪 |
|---|---|
| 变分原理 | 整个量子化学的地基；解释"更大基组更准" |
| $J$ 与 $K$、BS-HF/DFT | **HW1/HW2 磁交换常数** |
| RHF/UHF/自旋污染 | H₂ PES 任务、HW1/HW2 开壳层 |
| B 原子静态相关 → CASSCF | **HW3 活性空间的选择** |
| 双电子积分瓶颈、RI/Cholesky | ORCA/MOLCAS 里的 `RIJCOSX`、`Cholesky` 关键字 |
| DIIS / level shift / damping | 所有软件的 SCF 不收敛问题（→ 各 `pitfalls.md`） |
| 基组分类（zeta / 极化 / 弥散 / ECP） | 四次作业全部要选基组 |
| 各软件优缺点对照表 | 期中概念题 "哪个包适合哪个任务" |

## 自测清单

- [ ] 能说出 Gaussian / ORCA / OpenMOLCAS / VASP 各自最适合什么任务
- [ ] 能逐行解释一个 Gaussian 输入（`opt=tight`、`rb3lyp`、`cc-pVDZ`、`scf`、`grid`、电荷/多重度）
- [ ] 能陈述并证明变分原理（$E_{\text{trial}} \ge E_{\text{exact}}$）
- [ ] 能解释"改进近似只有两条路：加变分参数 / 换表示形式"
- [ ] 能区分 $J$ 和 $K$，说明 $K$ 只对同自旋非零、无经典对应
- [ ] 能陈述 Koopmans 定理，并说明 $-\varepsilon_{\text{HOMO}} \approx$ 电离能
- [ ] 能解释 B 原子为什么需要 CASSCF（静态相关、三个等价行列式）
- [ ] 能区分 RHF / ROHF / UHF，解释 UHF 的自旋污染及其来源
- [ ] 能解释为什么 HF 必须自洽迭代（$\mathbf F$ 依赖 $\mathbf D$）
- [ ] 能说清双电子积分为什么是瓶颈，conventional / direct / semi-direct 的区别
- [ ] 能解释 RI / 密度拟合如何把 N⁴ 降到 N³
- [ ] 能说出至少 3 种 SCF 收敛加速技巧，重点讲清 DIIS
- [ ] 能解释 GTO 为什么比 STO 受欢迎（Gaussian 乘积定理 → 解析积分）
- [ ] 能读懂 `aug-cc-pVTZ` 和 `6-311G++(3df,3pd)` 每一部分的意思
- [ ] 知道弥散函数用于阴离子、ECP 用于重原子、tight 函数用于 NMR/ESR
