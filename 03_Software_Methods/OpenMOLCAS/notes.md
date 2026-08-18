# OpenMOLCAS 笔记

对应 **HW3（15%）**：OpenMOLCAS + Luscus

开源多组态方法软件：https://gitlab.com/Molcas/OpenMolcas

## 为什么需要它（这是理解 HW3 的前提）

Gaussian 和 ORCA 的 DFT / HF 都是**单参考方法**——假设体系的波函数可以用**一个**
Slater 行列式描述。对大多数闭壳层有机分子这没问题。

但下面这些情况，单个行列式根本不够：
- **过渡金属配合物**：d 轨道近简并，多个电子排布方式能量相近
- **镧系化合物**：4f 轨道高度简并，基态本身就是多个组态的叠加
- **键断裂过程、双自由基、激发态**

这时必须用**多组态方法**：波函数写成多个行列式的线性组合，系数一起优化。这就是 CASSCF。

**方法层级**（HW3 要求你理解的核心）：

| 方法 | 处理什么 | 局限 |
|---|---|---|
| HF | 无电子相关 | 精度不够 |
| **CASSCF** | **静态相关**（近简并组态） | 完全没有动态相关，绝对能量差得远 |
| **CASPT2** | 在 CASSCF 基础上用二阶微扰补**动态相关** | 有 intruder state 问题 |
| **RASSI** | 把不同自旋的态放一起做**自旋轨道耦合** | — |

所以标准流程是流水线：**SCF → RASSCF → CASPT2 → RASSI**，
CASSCF 给对的"骨架"，CASPT2 给对的"数值"，RASSI 给对的"能级分裂"。

## 安装 / 环境

- 课程通过 **Canvas 分发预编译可执行文件与运行脚本** —— 优先用老师给的
- 驱动程序是 `pymolcas`
- 关键环境变量：`$MOLCAS`（安装路径）、`$Project`（输出前缀）、
  `$MOLCAS_WORKDIR`（中间文件目录，**必须指向 scratch**）、`$MOLCAS_MEM`

> ⚠️ 待确认 — `$MOLCAS` 路径：`________`

## 输入文件结构

和 Gaussian/ORCA 完全不同：**它是一个"模块流水线"脚本**。

```
&模块名
  关键字 = 值
  关键字
&下一个模块
```

- 模块按**书写顺序依次执行**，前一个的输出自动喂给后一个
- `//` 或 `*` 是注释
- `>>` 开头是 **EMIL 命令**（文件操作、循环、条件），比如 `>> COPY $Project.JobIph JOB001`
- `&` 和模块名之间**不能有空格**

## 各模块干什么

| 模块 | 作用 |
|---|---|
| `&GATEWAY` | 读结构、定基组、设对称性。`AMFI` 开自旋轨道积分、`RICD` 开 Cholesky 加速 |
| `&SEWARD` | 算单电子和双电子积分 |
| `&SCF` | HF 单点，给 RASSCF 提供初始轨道 |
| `&RASSCF` | **核心**：CASSCF/RASSCF 计算 |
| `&CASPT2` | 二阶微扰补动态相关 |
| `&RASSI` | 态间相互作用 + 自旋轨道耦合 |
| `&SINGLE_ANISO` | 单分子磁体的磁性质（g 张量、零场分裂 D/E、磁化率） |

> 💡 `SINGLE_ANISO` 是本课程老师 **Liviu Ungur** 本人（与 Chibotaru）开发的模块。
> 他的研究方向就是镧系单分子磁体的从头算——HW3 若涉及镧系磁性，这就是重点。

## RASSCF 关键字详解

```
Spin   = 6         // 自旋多重度 2S+1
Charge = 0
nActEl = 5 0 0     // 活性电子数 / RAS1 最大空穴数 / RAS3 最大电子数
                   //   后两个是 0 → 纯 CASSCF
                   //   非零 → RASSCF（把空间切成 RAS1/RAS2/RAS3，允许更大空间）
Ras2   = 5         // CAS 空间的轨道数
CIRoot = 5 5 1     // 态平均：算几个态 / 从前几个里取 / 权重(1=等权)
Inactive = 20      // 双占据且不参与相关的轨道数（一般让程序自己定）
```

**CAS(nActEl, Ras2)** 就是文献里常写的 CAS(n,m)。

计算量随 m 组合爆炸：CAS(10,10) 有约 2 万个组态，CAS(14,14) 约 240 万个，
CAS(16,16) 就已经很吃力了。**活性空间的选择 = HW3 的全部难点**，
选法见 `pitfalls.md` 里的专门一节。

## CASPT2 的两个必调参数

- **`IPEA`**：IPEA 位移。MOLCAS 默认 **0.25**，但对过渡金属体系文献普遍推荐 **0.0**。
  两个值算出来的激发能能差几千 cm⁻¹。**报告里必须写明用了哪个。**
- **`IMAG`**：虚位移，典型值 0.1。用来抑制 **intruder state（入侵态）**——
  微扰空间里有个态和参考态能量太接近，导致分母趋零、能量发散。
  看到 intruder 警告就加大 IMAG。

## Luscus 用来做什么

Luscus 是配套的可视化工具，**最重要的用途是检查活性轨道**。

```bash
# 把 MOLCAS 的轨道文件转成 Luscus 能读的格式
$MOLCAS/bin/grid_it   # 或直接用 &GRID_IT 模块生成 .lus / .grid 文件
```

在 `&RASSCF` 之后加一个模块生成格点文件：
```
&GRID_IT
  ALL
```

然后本地用 Luscus 打开，逐个翻活性轨道，确认它们是**你想要的金属 d/f 轨道**，
而不是混进来的配体轨道或空的弥散轨道。**这一步不能省。**

## 结果怎么读

```bash
grep "RASSCF root number" mol.out          # CASSCF 各态能量
grep -A5 "Total energy" mol.out
grep "Total CASPT2 energies" mol.out       # CASPT2 修正后的能量
grep -A30 "Eigenvalues of the SO Hamiltonian" mol.out   # RASSI 自旋轨道耦合后的能级
grep -A10 "g tensor" mol.out               # SINGLE_ANISO 的 g 张量
```

激发能通常换算成 **cm⁻¹** 报告（1 Hartree = 219474.63 cm⁻¹），因为光谱学惯用这个单位。
