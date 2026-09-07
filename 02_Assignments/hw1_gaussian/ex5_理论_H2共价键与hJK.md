# Exercise 5（理论题 #2，5 分）

**题目**：以 H₂ 分子为例描述共价键。写出基态的 Slater 行列式，用 Lecture 3 的方法
（用 h、J、K）估算总能量。写出用每个 H 原子上的最小基组能构成的所有激发 Slater 行列式的能量。
解释库仑积分和交换积分。

---

## 1. 最小基组与分子轨道

每个 H 原子放**一个 1s 轨道**：$a=1s_A$，$b=1s_B$。重叠积分 $S=\langle a|b\rangle>0$。
对称性（$D_{\infty h}$）决定分子轨道就是对称/反对称组合：

$$\sigma_g=\frac{a+b}{\sqrt{2(1+S)}}\quad(\text{成键}),\qquad
\sigma_u=\frac{a-b}{\sqrt{2(1-S)}}\quad(\text{反键})$$

- $\sigma_g$：两核之间电子密度增强 → 屏蔽核–核排斥、降低动能 → **成键**，轨道能低。
- $\sigma_u$：两核之间有节面，密度被推向两端 → **反键**，轨道能高。

单电子积分：

$$h_{gg}=\langle\sigma_g|\hat h|\sigma_g\rangle=\frac{h_{aa}+h_{ab}}{1+S},\qquad
h_{uu}=\langle\sigma_u|\hat h|\sigma_u\rangle=\frac{h_{aa}-h_{ab}}{1-S}$$

其中 $h_{aa}=\langle a|\hat h|a\rangle$（原子上的单电子能），
$h_{ab}=\langle a|\hat h|b\rangle$ 是**共振积分（resonance integral）**，$h_{ab}<0$ 且数值可观 ——
**这一项就是共价键的来源**：它把 $h_{gg}$ 压到比孤立原子的 $h_{aa}$ 更低。

---

## 2. 基态 Slater 行列式与总能量

基态：两个电子自旋相反、都占 $\sigma_g$（最小基组下 Pauli 只允许 2 个）。

$$\boxed{\;\Psi_0=|\,\sigma_g\bar\sigma_g\,|
=\frac{1}{\sqrt{2}}
\begin{vmatrix}\sigma_g(1)\alpha(1)&\sigma_g(1)\beta(1)\\[2pt]
\sigma_g(2)\alpha(2)&\sigma_g(2)\beta(2)\end{vmatrix}\;}$$

按 Lecture 3 的能量公式 $E=\sum_i h_{ii}+\sum_{i<j}(J_{ij}-K_{ij})+V_{nn}$，
本行列式只有一对电子（α 与 β，自旋相反 → $K=0$）：

$$\boxed{\;E_0=2\,h_{gg}+J_{gg}+V_{nn}\;}
\qquad V_{nn}=\frac{1}{R}$$

$$J_{gg}=(\sigma_g\sigma_g|\sigma_g\sigma_g)
=\iint |\sigma_g(1)|^2\frac{1}{r_{12}}|\sigma_g(2)|^2\,d\tau_1 d\tau_2$$

**估算含义**：与两个孤立 H 原子的能量 $2h_{aa}$（每个原子一个电子、无电子–电子排斥）相比，

$$E_{\text{bind}}=E_0-2h_{aa}
=\underbrace{\frac{2}{1+S}(h_{aa}+h_{ab})-2h_{aa}}_{<0,\ \text{来自 }h_{ab}}
+\underbrace{J_{gg}+\tfrac1R}_{>0,\ \text{排斥}}$$

净结果为负（约 −4.5 eV，真实值 −4.75 eV）—— 共价键 = 共振积分 $h_{ab}$ 带来的稳定化
胜过电子–电子和核–核排斥。

---

## 3. 所有激发 Slater 行列式的能量

最小基组：2 个空间轨道（$\sigma_g,\sigma_u$）、4 个自旋轨道。基态组态 $\sigma_g^2$。
把电子往 $\sigma_u$ 挪，能写出的行列式及其能量：

| 行列式 | 类型 | $M_S$ | 能量（$-V_{nn}$ 略去写在括号外，统一 $+V_{nn}$）|
|---|---|---|---|
| $|\sigma_g\bar\sigma_g|$ | 基态 | 0 | $2h_{gg}+J_{gg}+V_{nn}$ |
| $|\sigma_g\sigma_u|$ | 单激发 | +1 | $h_{gg}+h_{uu}+J_{gu}-K_{gu}+V_{nn}$ |
| $|\bar\sigma_g\bar\sigma_u|$ | 单激发 | −1 | $h_{gg}+h_{uu}+J_{gu}-K_{gu}+V_{nn}$ |
| $|\sigma_g\bar\sigma_u|$ | 单激发 | 0 | $h_{gg}+h_{uu}+J_{gu}+V_{nn}$ |
| $|\bar\sigma_g\sigma_u|$ | 单激发 | 0 | $h_{gg}+h_{uu}+J_{gu}+V_{nn}$ |
| $|\sigma_u\bar\sigma_u|$ | 双激发 | 0 | $2h_{uu}+J_{uu}+V_{nn}$ |

其中
$J_{gu}=(\sigma_g\sigma_g|\sigma_u\sigma_u)$，
$K_{gu}=(\sigma_g\sigma_u|\sigma_u\sigma_g)$。
注意**单个** $M_S=0$ 的行列式里没有 $K$（两个电子自旋相反）；$K$ 只在同自旋的
$M_S=\pm1$ 行列式里出现。

### 自旋组合后的谱项（更物理）

两个 $M_S=0$ 的单激发行列式不是自旋本征态，线性组合给出：

$$^3\Sigma_u^+:\quad E=h_{gg}+h_{uu}+J_{gu}-K_{gu}+V_{nn}\quad(\text{三重简并})$$
$$^1\Sigma_u^+:\quad E=h_{gg}+h_{uu}+J_{gu}+K_{gu}+V_{nn}$$
$$^1\Sigma_g^+\,(\text{双激发}):\quad E=2h_{uu}+J_{uu}+V_{nn}$$

三重态比单重态低 $2K_{gu}$ —— 这就是 **Hund 规则**的微观来源：同自旋电子因交换效应
彼此“回避”，库仑排斥减小。

---

## 4. 库仑积分 J 与交换积分 K

$$J_{ij}=(ii|jj)=\iint\varphi_i^*(1)\varphi_i(1)\,\frac{1}{r_{12}}\,
\varphi_j^*(2)\varphi_j(2)\,d\tau_1 d\tau_2$$

- **物理意义**：电荷云 $|\varphi_i|^2$ 与电荷云 $|\varphi_j|^2$ 之间的**经典静电排斥**。
- 有经典对应物；对实轨道 $J_{ij}>0$；与自旋无关（对所有电子对都出现）。

$$K_{ij}=(ij|ji)=\iint\varphi_i^*(1)\varphi_j(1)\,\frac{1}{r_{12}}\,
\varphi_j^*(2)\varphi_i(2)\,d\tau_1 d\tau_2$$

- **物理意义**：纯量子效应，来自 Slater 行列式的**反对称性**（Pauli）。积分里两个电子
  “交换”了轨道标签，没有经典图像。
- **只对自旋相同的电子对非零**；对实轨道 $K_{ij}>0$，在能量表达式里带负号 →
  **降低同自旋组态的能量**（交换稳定化 / 费米空穴：同自旋电子天然分离）。
- HF 中 $J_{ii}=K_{ii}$，所以电子不会和自己排斥（自相互作用被交换项精确抵消）——
  这是 HF 相对纯 Hartree 方法的关键改进，也是 DFT 里“自相互作用误差”的对照。

---

## 5. 附：RHF 为什么在解离时失败（与 Ex2 呼应，可选加分）

把 $\Psi_0=|\sigma_g\bar\sigma_g|$ 用原子轨道展开：

$$\Psi_0\propto
\underbrace{a(1)b(2)+b(1)a(2)}_{\text{共价 H·\,·H}}
+\underbrace{a(1)a(2)+b(1)b(2)}_{\text{离子 H}^-\text{H}^+}$$

单行列式**强制共价项和离子项等权重**，且这个比例不随 $R$ 变化。$R\to\infty$ 时正确答案
应是纯共价（两个中性 H 原子），但 RHF 仍保留 50% 离子成分 → 解离能被高估、曲线形状错。
修正：UHF（允许 $\sigma_g$ 局域化到单个原子，但有自旋污染）或加入双激发
$|\sigma_u\bar\sigma_u|$ 做 CI（2×2 组态相互作用，即最小的 CASSCF(2,2)）。
