# Lecture 02：从量子力学基础到 Hartree-Fock-Roothaan

> CM5235 · Liviu Ungur · 102 页
> 讲义原件：`slides/CM5235_Lecture_02.pptx`

## 这一讲到底在干什么（先抓主线）

102 页看着吓人，但它只讲了**一件事**：

> **把"薛定谔方程"一步步削减成计算机真的能解的东西。**

这条链是：

```
薛定谔方程（严格，但只有氢原子能精确解）
  ↓ 加第二个电子 → 1/r₁₂ 项 → 精确解立刻不存在
  ↓ 近似 1：Born-Oppenheimer     —— 冻住原子核
  ↓ 近似 2：轨道近似             —— 多电子波函数拆成单电子轨道的乘积
  ↓ 近似 3：平均场               —— 每个电子只感受其他电子的"平均"电场
  ↓ 约束：Pauli 原理 → Slater 行列式
  ↓ 变分求最优轨道 → Fock 算符 → Hartree-Fock 方程
  ↓ 近似 4：LCAO（轨道用基组展开）
  ↓
Hartree-Fock-Roothaan 方程 = 矩阵本征值问题 = 计算机能解
  ↓ 自洽迭代
SCF
```

**你在 Gaussian 里敲 `#p HF/6-31G(d)`，程序做的就是这条链的最后两步。**
所以这一讲不是"纯理论课"，它是在解释你的软件里那行 `SCF Done` 到底算完了什么。

---

## 一、什么时候需要量子力学（p.2–9）

### 波粒二象性（p.3–5）

de Broglie 1924 年的推理很简单：光既是波又是粒子，那物质凭什么不是？

从相对论能量 $E = pc$ 和光子能量 $E = h\nu$ 联立，得到

$$\lambda = \frac{h}{p}$$

他断言这对**粒子和光子都成立**。1925 Davisson-Germer、1927 Thompson 的电子衍射实验证实了这一点。
电子显微镜就是这条关系的应用——用电压控制电子波长，比光学显微镜精细得多，
而且电子束还能用电磁场聚焦，这是同波长的电磁辐射做不到的。

### 判据：ΔE 和 k_BT 谁大（p.6–9）⭐ 考点

这是**全课最实用的一个判断**，Ungur 用 Boltzmann 分布给出定量标准：

$$\frac{n_i}{n_j} = \frac{g_i}{g_j}\, e^{-\Delta E / k_B T}$$

| 情况 | 结论 |
|---|---|
| $\Delta E < k_B T$ | 各能级布居差不多，能谱看起来**连续** → **经典力学够用** |
| $\Delta E \approx k_B T$ | 过渡区 |
| $\Delta E > k_B T$ | 只有低能级有布居，能谱**离散** → **必须用量子力学** |

**关键认知**：经典力学和量子力学不是在竞争谁对，而是**适用区间不同**。

这直接解释了课程后面为什么力场（经典）能算蛋白质构象，而电子结构必须用量子方法——
电子激发和分子振动的 ΔE 远大于室温 $k_BT$（≈ 208 cm⁻¹ ≈ 0.026 eV），
而分子整体的平动、转动的 ΔE 远小于它。

> 讲义里还提了简并度 $g$ 的物理含义：能量越高，把能量分配到各自由度的方式越多，
> 简并度越高（也就是熵越高）。

---

## 二、薛定谔方程是怎么来的（p.10–14）

Ungur 走的是**"经典波动方程 + de Broglie"**这条路，不是直接扔公设。值得跟一遍，因为它解释了方程里每一项的出处。

**第 1 步**：经典一维非色散波动方程

$$\frac{\partial^2 \Psi}{\partial x^2} = \frac{1}{v^2}\frac{\partial^2 \Psi}{\partial t^2}$$

（p.11 的练习就是验证 $\Psi = A\sin(kx - \omega t + \phi)$ 是它的解，条件是 $k = \omega/v$。）

**第 2 步**：取驻波解 $\Psi(x,t) = \psi(x)\cos\omega t$。
**驻波 = 定态**，这个对应是整个推导的关键。代入后用 $\omega = 2\pi\nu$、$v = \lambda\nu$ 消掉时间：

$$\frac{\partial^2 \psi}{\partial x^2} + \frac{4\pi^2}{\lambda^2}\psi = 0$$

**第 3 步**：这还是"经典"的。现在插入物理——经典总能量 $E = \frac{p^2}{2m} + V(x)$，
所以 $p^2 = 2m[E - V(x)]$。再用 de Broglie $\lambda = h/p$ 把 $\lambda$ 换掉：

$$\frac{\partial^2 \psi}{\partial x^2} + \frac{8\pi^2 m}{h^2}\left[E - V(x)\right]\psi = 0$$

**第 4 步**：引入约化 Planck 常数 $\hbar = h/2\pi$，整理：

$$\boxed{-\frac{\hbar^2}{2m}\frac{\partial^2 \psi}{\partial x^2} + V(x)\psi = E\psi}$$

**这就是定态（time-independent）薛定谔方程**，用来研究量子体系的定态。
氢原子的 1s、2pz 轨道就是它的解。

### 含时方程与"定态"的含义（p.14）

当势能依赖时间 $V(x,t)$ 时，要用含时方程：

$$-\frac{\hbar^2}{2m}\frac{\partial^2 \Psi}{\partial x^2} + V(x,t)\Psi = i\hbar\frac{\partial \Psi}{\partial t}$$

定态时两个方程同时满足，于是 $i\hbar\frac{\partial\Psi}{\partial t} = E\Psi$，波函数可分离变量：

$$\Psi(x,t) = \psi(x)\, e^{-iEt/\hbar}$$

**为什么叫"定态"**：概率密度

$$\Psi^*\Psi = \psi^* e^{+iEt/\hbar}\, \psi\, e^{-iEt/\hbar} = \psi^*\psi$$

**时间相位完全抵消了**——概率密度不随时间变。
所以电子"绕核运动"却不辐射能量，玻尔模型里硬塞进去的那条假设，在这里自然出现了。

---

## 三、算符、本征值、本征函数（p.15–20）

薛定谔方程可以写成

$$\hat{H}\psi_n = E_n \psi_n$$

$\hat{H}$ 是总能量算符（**Hamiltonian**），$E_n$ 是第 n 个本征值，$\psi_n$ 是第 n 个本征函数。
这是**本征值方程**的一个例子，一般形式是：

$$\text{算符} \times \text{本征函数} = \text{本征值（实标量）} \times \text{同一个本征函数}$$

**每个可观测量对应一个厄米算符**（p.16）：坐标 $\hat{r}$、动量 $\hat{p}$、角动量 $\hat{L}=\hat{r}\times\hat{p}$、
势能 $\hat{V}$、动能 $\hat{K}$、总能量 $\hat{H}$、电偶极矩和磁偶极矩。

p.17 的练习值得自己动手：验证 $\psi(x) = Ae^{ikx} + Be^{-ikx}$
**不是** $\frac{\partial}{\partial x}$ 的本征函数，但**是** $\frac{\partial^2}{\partial x^2}$ 的本征函数，本征值 $-k^2$。

### 三个性质（后面所有推导的地基）

**1. 正交归一性（p.18）**

$$\int \psi_i^* \psi_j \, dx = 0 \quad (i \ne j), \qquad \int \psi_i^* \psi_i \, dx = 1$$

- **正交**：保证各本征态彼此"完全不同"
- **归一**：保证在全空间找到电子的概率是 1（100% 确定它在某处）

**2. 完备性（p.20）**

一个量子力学算符的**全部**本征函数构成**完备集**，任意函数都能用它们展开：

$$\psi(x) = \sum_{n=1}^{\infty} b_n \psi_n(x)$$

Ungur 的类比很到位：就像三维空间里任何向量都能写成 x、y、z 三个正交单位向量的线性组合，
这三个单位向量构成一个完备集。这里的 $\psi_n$ 也叫**基函数 (basis functions)**，
$b_n$ 是**混合系数**。完备集可以是无限的，但不必然无限。

> 💡 **这就是"基组 (basis set)"这个词的来源。** 你在 Gaussian 里写 `6-31G(d)`，
> 就是在选一组**有限**的基函数来近似这个本该无限的完备集。
> 基组越大 = 展开越完整 = 越接近真解，代价是计算量。

**3. 厄米性（p.22）**

$$\int \psi_i^* \hat{O}\psi_j \, dx = \left[\int \psi_j^* \hat{O}\psi_i \, dx\right]^*$$

厄米算符的**本征值全是实数**。所有对应物理可观测量的算符都必须是厄米的——
因为测量结果必须是实数。薛定谔方程的本征值是能量，所以 Hamiltonian 矩阵是厄米矩阵。

---

## 四、对易关系与不确定性（p.21, 23–27）⭐ 考点

### 线性 vs 非线性（p.21）

线性算符满足 $a\hat{O}\psi = \hat{O}a\psi$。反例：$\log(a\psi) \ne a\log\psi$，所以 log 不是线性算符。
量子力学里的算符都是线性的。

### 位置和动量不对易

取 $\hat{A} = x$，$\hat{B} = \hat{p}_x = -i\hbar\frac{\partial}{\partial x}$：

$$\hat{A}\hat{B}\psi = -i\hbar\, x\frac{\partial \psi}{\partial x}$$

$$\hat{B}\hat{A}\psi = -i\hbar\frac{\partial}{\partial x}(x\psi) = -i\hbar\psi - i\hbar\, x\frac{\partial \psi}{\partial x}$$

相减：

$$\boxed{[\hat{x}, \hat{p}] = \hat{x}\hat{p} - \hat{p}\hat{x} = i\hbar = i\frac{h}{2\pi}}$$

**这是量子力学最重要的一条关系**（Heisenberg 提出，Born 和 Jordan 形式化）。
它的含义是：**算符作用的顺序有物理意义**——先测位置再测动量，和反过来，结果不同。

### 它意味着什么（p.24）

1. **牛顿定律对微观粒子是错的**，只能是真实运动方程的一个近似
2. 经典物理成立的条件，正是"**取 $h \to 0$ 对所求性质影响可忽略**"
3. 这个影响不是对可观测量形式的小修小补，而是根本性的

### 矩阵力学（p.25）

数学上有两种等价诠释：把 x、p 看成**算符**，或看成**矩阵**（矩阵乘法本来就 $AB \ne BA$）。
后者就是"**矩阵力学**"这个名字的由来。讲义给出了算符在一组基下的矩阵元形式
$O_{ij} = \int\psi_i^*\hat{O}\psi_j\,dx$——这正是后面 Fock 矩阵的来源。

### 对易子代数（p.26–27）

$$[\hat{A},\hat{B}] = \hat{A}\hat{B} - \hat{B}\hat{A} \quad(\text{对易子}), \qquad \{\hat{A},\hat{B}\} = \hat{A}\hat{B} + \hat{B}\hat{A}\quad(\text{反对易子})$$

**最重要的一条推论**：

> 若 $[\hat{A},\hat{B}] = 0$，则 $\hat{A}$ 的所有本征函数**同时也是** $\hat{B}$ 的本征函数，反之亦然。

这条在氢原子那里立刻要用（$\hat{H}$、$\hat{L}^2$、$\hat{L}_z$ 共享本征态 → 三个量子数 $n, l, m$）。

常用恒等式（p.27，作为练习自己验证）：

$$[\hat{A},\hat{B}] = -[\hat{B},\hat{A}], \qquad [\hat{A},\hat{A}^n] = 0$$
$$[\hat{A},\hat{B}+\hat{C}] = [\hat{A},\hat{B}] + [\hat{A},\hat{C}]$$
$$[\hat{A},\hat{B}\hat{C}] = [\hat{A},\hat{B}]\hat{C} + \hat{B}[\hat{A},\hat{C}]$$

p.31 给出几个有用的结果：$[\hat{x},\hat{H}] = \frac{i\hbar}{m}\hat{p}$、
$[\hat{p},\hat{H}] = -i\hbar\frac{\partial V}{\partial x}$、$[\hat{x},\hat{p}_y] = [\hat{x},\hat{p}_z] = 0$。
（最后一条说明：不同方向的位置和动量之间没有不确定性关系。）

---

## 五、五条公设（p.32–43）⭐ 考点，很可能直接考

### Born 诠释（p.32）

1926 年 Born 提出：$\Psi^*\Psi$ 应被视为**概率密度**。
$\Psi$ 本身可以是复函数，是它和自己共轭的乘积才给出真实的物理概率。
对全空间积分给出**归一化条件** $\int\Psi^*\Psi \, d\tau = 1$。

### 公设 1：状态

量子粒子的状态由波函数 $\Psi(x,t)$ **完全确定**。$t_0$ 时刻在 $x_0$ 处宽度 $dx$ 内找到粒子的概率是

$$P(x_0,t_0)\,dx = \Psi^*(x_0,t_0)\Psi(x_0,t_0)\,dx = |\Psi(x_0,t_0)|^2 dx$$

**对 Ψ 的要求**（p.34–35）：

| 要求 | 含义 |
|---|---|
| **单值** | 一个 x 只能对应一个 Ψ 值（否则概率没有唯一定义） |
| **连续** | Ψ 连续，且 $\partial\Psi/\partial x$ 存在、左右极限相等 |
| **有限** | 不能在某个区间内取无穷大 |

这三条不是数学洁癖——**正是它们（加上边界条件）导致能量量子化**。

### 公设 2：可观测量 ↔ 算符

每个可测性质（位置、动量、能量……）都有对应的量子力学算符。

> **实验室里测量某个可观测量，在理论里就对应"用相应算符作用在波函数上"。**

### 公设 3：测量结果

单次测量某个可观测量，**得到的值只可能是对应算符的本征值**，不会是别的任何数。

### 公设 4：期望值

对多个同样制备的体系各测一次，平均值（期望值）是

$$\langle a \rangle = \frac{\int_{-\infty}^{+\infty} \Psi^* \hat{A}\Psi\, dx}{\int_{-\infty}^{+\infty} \Psi^* \Psi\, dx}$$

Ψ 归一时分母为 1。分两种情况：

**情况 1（p.39）**：Ψ 就是 $\hat{A}$ 的归一化本征态，$\hat{A}\varphi_i = a_i\varphi_i$。
则 $\langle a\rangle = a_i$ ——**每次测都得同一个值，没有涨落**。

**情况 2（p.40）**：Ψ 不是 $\hat{A}$ 的本征态。用完备性展开 $\Psi = \sum_n b_n \varphi_n$，
利用正交归一性，交叉项全部消失：

$$\langle a \rangle = \sum_n |b_n|^2 a_n$$

**期望值是加权平均，权重 $|b_n|^2$ 就是测到本征值 $a_n$ 的概率。**

### 叠加原理与波函数坍缩（p.41–42）

测量前，粒子的波函数是所有可能本征态的**叠加**。
$b_n$ 是展开系数，$|b_n|^2$ 是权重。**单次测量只能得到一个本征值**，
要知道全部 $a_n$ 必须测很多次。

> **量子力学里的测量是"主动"的**：测量把波函数**坍缩**到被测算符的某一个本征态上，
> 原来的波函数被摧毁，其中包含的所有其他信息永久丢失。

Einstein 的反问："你真的认为我们不看月亮的时候它就不在那儿吗？"
Schrödinger 的猫：箱子里有猫和一瓶随机释放的毒气，开箱前不知死活。
**"开箱" = 量子力学中的测量过程**。重复足够多次，约 50% 的情况猫是活的。

### 公设 5：时间演化（p.43）

$$\hat{H}\Psi_n(x,t) = i\hbar \frac{\partial \Psi_n(x,t)}{\partial t}$$

---

## 六、氢原子：唯一能精确解的体系（p.44–55）

### 库仑相互作用与球坐标（p.44–45）

$$V = \frac{1}{4\pi\varepsilon_0}\frac{Q_1 Q_2}{|\vec{r}_1 - \vec{r}_2|}$$

球坐标：$x = r\sin\theta\cos\varphi$，$y = r\sin\theta\sin\varphi$，$z = r\cos\theta$。

### 中心力场（p.46–47）

**中心力 = 由球对称势能函数导出的力**。若 $V = V(r)$ 只依赖 $r$，用链式法则

$$\frac{\partial V}{\partial x} = \frac{\partial V}{\partial r}\frac{\partial r}{\partial x} = \frac{x}{r}\frac{\partial V}{\partial r}$$

（y、z 同理）代入 $\vec{F} = -\nabla V$：

$$\vec{F} = -\frac{1}{r}\frac{\partial V}{\partial r}(x\mathbf{i} + y\mathbf{j} + z\mathbf{k}) = -\frac{dV(r)}{dr}\cdot\frac{\vec{r}}{r}$$

**力沿径向。** 这是能解出来的根本原因。

### 关键技巧：把 Laplacian 拆成径向 + 角向（p.48–49）

球坐标下

$$\nabla^2 = \frac{\partial^2}{\partial r^2} + \frac{2}{r}\frac{\partial}{\partial r} + \frac{1}{r^2}\left[\frac{\partial^2}{\partial\theta^2} + \cot\theta\frac{\partial}{\partial\theta} + \frac{1}{\sin^2\theta}\frac{\partial^2}{\partial\varphi^2}\right]$$

而角动量平方算符恰好是

$$\hat{L}^2 = -\hbar^2\left[\frac{\partial^2}{\partial\theta^2} + \cot\theta\frac{\partial}{\partial\theta} + \frac{1}{\sin^2\theta}\frac{\partial^2}{\partial\varphi^2}\right]$$

**方括号里一模一样！** 所以

$$\nabla^2 = \frac{\partial^2}{\partial r^2} + \frac{2}{r}\frac{\partial}{\partial r} - \frac{1}{r^2\hbar^2}\hat{L}^2$$

Hamiltonian 变成

$$\hat{H} = -\frac{\hbar^2}{2m_e}\left(\frac{\partial^2}{\partial r^2} + \frac{2}{r}\frac{\partial}{\partial r}\right) + \frac{1}{2m_e r^2}\hat{L}^2 + V(r)$$

**径向和角向被彻底分开了。**

### 对易性带来量子数（p.50–51）

当 $V = V(r)$ 时（练习：自己证）：

$$[\hat{H}, \hat{L}^2] = 0, \qquad [\hat{H}, \hat{L}_z] = 0, \qquad \hat{L}_z = -i\hbar\frac{\partial}{\partial\varphi}$$

由第四节那条推论，三个算符**共享同一套本征函数**，于是同时有：

$$\hat{L}^2\Psi = l(l+1)\hbar^2\Psi, \qquad l = 0,1,2,3,\dots$$
$$\hat{L}_z\Psi = m\hbar\Psi, \qquad m = -l, -l+1, \dots, l-1, l$$

> **$l$ 和 $m$ 不是硬塞进去的，是对易关系逼出来的。**
> 这是"量子数从哪来"这个问题最干净的回答。

### 分离变量（p.52）

$\hat{L}^2$ 的本征函数是**球谐函数** $Y_l^m(\theta,\varphi)$。
因为 $\hat{L}^2$ 不含 $r$，总解可以写成乘积：

$$\Psi = R(r)\, Y_l^m(\theta,\varphi) = R(r)\sqrt{\frac{2l+1}{4\pi}\frac{(l-m)!}{(l+m)!}}\,P_l^m(\cos\theta)\,e^{im\varphi}$$

代入后角向部分约掉，剩下**径向方程**：

$$-\frac{\hbar^2}{2m_e}\left[\frac{\partial^2}{\partial r^2} + \frac{2}{r}\frac{\partial}{\partial r} - \frac{l(l+1)}{r^2}\right]R(r) + V(r)R(r) = E R(r)$$

> **结论**：对任何球对称势下的单粒子问题，定态波函数都是 $R(r)Y_l^m(\theta,\varphi)$ 的形式。
> p.53 展示了 L=0 到 L=5 各个 m 的球谐函数形状——**这就是 s、p、d、f 轨道的角向部分**。

### 径向函数只对单电子体系可解（p.54）⭐ 关键的一句

> 径向波函数**只有单电子体系能解**。两个电子以上，径向方程**无解析解**，
> 只能用数值方法（精度可以做到任意高）。
> **径向波函数被制表在"基组 (basis sets)"的信息里。**

这一句是理论和软件之间的桥：你选 `6-31G(d)` 时，程序去查的就是这些预先拟合好的径向函数。

---

## 七、氦原子：一切崩塌的地方（p.56–62）⭐ 全课转折点

### 罪魁祸首：$1/r_{12}$

$$\hat{H} = \left(-\tfrac{1}{2}\nabla_1^2 - \tfrac{2}{r_1}\right) + \left(-\tfrac{1}{2}\nabla_2^2 - \tfrac{2}{r_2}\right) + \frac{1}{r_{12}}$$

前两个括号各自是可解的类氢问题，**第三项把两个电子的坐标耦合在一起**，从此无精确解。

> **超过一个电子的体系，都不可能得到精确波函数**，但数值解可以做到任意精度。

### 连锁后果（p.57–59）

- $r_{12}$ 项**破坏球对称性**——向量 $\vec{r}_{12}$ 不从坐标原点出发
- 电子互相排斥、尽量躲开对方，导致**单个电子的角动量涨落、不再量子化**，
  $l_1$、$l_2$ **不再是好量子数**
- 但**总角动量守恒**，是好量子数：

$$\vec{L} = \sum_i^N \vec{l}_i, \qquad \vec{S} = \sum_i^N \vec{s}_i$$

$$L_z = \sum_i m_i = M_L, \qquad S_z = \sum_i m_{s_i} = M_S$$

  注意：**z 分量像普通数一样相加**（标量相加），而矢量本身要按角动量耦合规则相加。
- 电子**不可区分**——不能给它们贴标签 1 和 2
- 单个电子的 $l_i$ 仍有用，因为它给出电子 i 的**平均**轨道角动量

### 三层近似（p.60–62, 78–79, 81）⭐⭐

| 近似 | 内容 | 丢掉了什么 |
|---|---|---|
| **Born-Oppenheimer** (p.78) | 核比电子重约 2000 倍，电子运动快得多 → 视核为**静止**，电子瞬时适应任何核构型 | 核动能项 = 0，核-核排斥 = 常数 |
| **轨道近似** (p.60) | 多电子波函数写成有效单电子波函数的**乘积**：$\psi(1,2) \approx \varphi_1(1)\varphi_2(2)$ | 真实波函数可能含平方项、交叉项等复杂形式 |
| **平均场 MFA** (p.61, 81) | 每个电子只感受核 + 其他所有电子产生的**平均**静电场 | **电子关联**——现实中电子会实时躲避彼此 |

> Ungur 原话：这是个近似，"**但如果我们想解真实分子，我们别无选择……**"

平均场的直白后果（p.81）：
> 每个电子**感受不到其他电子的具体存在，也不知道它们在哪**。
> 但现实是：两个电子靠得很近的概率非常小。

**这三层近似正是后面所有"高级方法"要修补的东西**：
- MP2 / CCSD 补的是平均场丢掉的**动态关联**
- CASSCF / CASPT2 补的是单个乘积（单行列式）不够用的**静态关联**（→ HW3）

轨道近似的回报（p.62）：可以继续用 $l = 0,1,2,3\dots$，加上自旋得到**四个量子数**
$(n_i, l_i, m_i, m_{s_i})$。**这套单电子近似 + Pauli 原理，解释了整张周期表。**

---

## 八、自旋与 Pauli 原理（p.63–73）⭐ 重要考点

### 自旋（p.63–64）

类比轨道角动量，有自旋角动量算符 $\hat{s}^2$ 和 $\hat{s}_z$，
描述"电子绕自身轴的转动"。本征函数记作 $\alpha$ 和 $\beta$：

$$\hat{s}^2\alpha = s(s+1)\alpha, \qquad \hat{s}_z\alpha = +\tfrac{1}{2}\alpha, \qquad \hat{s}_z\beta = -\tfrac{1}{2}\beta$$

正交归一：$\int\alpha^*\alpha\,d\sigma = \int\beta^*\beta\,d\sigma = 1$，$\int\alpha^*\beta\,d\sigma = 0$。

电子 $s = 1/2$，所以 $m_s = \pm 1/2$。
**约定**：单电子用小写 $s, m_s$；多电子体系的总自旋用大写 $S, M_S$。

### Pauli 原理的正确表述（p.65）

> 电子波函数对**任意两个电子的交换**是**反对称**的：
> $$\hat{P}_{12}\,\psi(1,2,\dots) = \psi(2,1,\dots) = -\psi(1,2,\dots)$$

注意概率密度 $\psi^*\psi$ 在交换下**不变**——因为它是可观测量，而电子确实完全不可区分。

（中学里说的"两个电子不能占据同一状态"只是这条的**推论**，不是本质。）

### 氦基态（p.66）

两个电子不可区分，两种写法等价，取线性组合：

$$\Psi_\pm = 1s(r_1)\alpha(1)\,1s(r_2)\beta(2) \pm 1s(r_2)\alpha(2)\,1s(r_1)\beta(1)$$

交换算符作用：$\hat{P}_{12}\Psi_+ = +\Psi_+$（对称），$\hat{P}_{12}\Psi_- = -\Psi_-$（反对称）。

**只有 $\Psi_-$ 满足 Pauli 原理**。所以氦基态（$L=0, S=0, J=0$，记作 $^1S_0$）是

$$\Psi(^1S_0) = \frac{1}{\sqrt{2}}\, 1s(r_1)\,1s(r_2)\left[\alpha(1)\beta(2) - \alpha(2)\beta(1)\right]$$

### 氦激发态与交换积分（p.67–71）⭐⭐ 本讲最精彩的一段

考虑第一激发组态 $1s^1 2s^1$。因为两个电子在**不同轨道**且不可区分，
空间波函数必须写成线性组合，得到一对对称/反对称函数：

$$\Psi^{sym}_{space} = \tfrac{1}{\sqrt2}\left[1s(r_1)2s(r_2) + 1s(r_2)2s(r_1)\right]$$
$$\Psi^{anti}_{space} = \tfrac{1}{\sqrt2}\left[1s(r_1)2s(r_2) - 1s(r_2)2s(r_1)\right]$$

自旋部分有四个函数（p.68）：

| 自旋函数 | 交换对称性 | $S, M_S$ |
|---|---|---|
| $\alpha(1)\alpha(2)$ | 对称 | $S=1, M_S=+1$ |
| $\beta(1)\beta(2)$ | 对称 | $S=1, M_S=-1$ |
| $\tfrac{1}{\sqrt2}[\alpha(1)\beta(2)+\alpha(2)\beta(1)]$ | 对称 | $S=1, M_S=0$ |
| $\tfrac{1}{\sqrt2}[\alpha(1)\beta(2)-\alpha(2)\beta(1)]$ | **反对称** | $S=0, M_S=0$ |

**总波函数必须反对称** → 只能"对称 × 反对称"配对（p.69）：

- **三重态 $^3S_1$**（3 个简并态）= **反对称空间** × **对称自旋**
- **单重态 $2\,^1S_0$** = **对称空间** × **反对称自旋**

用氢的 1s、2s 原子轨道作近似空间函数，算期望值 $E = \frac{\langle\Psi|\hat{H}|\Psi\rangle}{\langle\Psi|\Psi\rangle}$，
经过大量代数后得到（p.70）：

$$E(^3S_1) = E_{1s} + E_{2s} + J - K$$
$$E(2\,^1S_0) = E_{1s} + E_{2s} + J + K$$

$$\boxed{\Delta E = E(^3S_1) - E(2\,^1S_0) = -2K}$$

其中（p.71）：

$$J = \iint 1s^*(r_1)\,2s^*(r_2)\,\frac{1}{r_{12}}\,1s(r_1)\,2s(r_2)\,d\tau \qquad \textbf{库仑积分}$$

$$K = \iint 1s^*(r_1)\,2s^*(r_2)\,\frac{1}{r_{12}}\,\underline{1s(r_2)\,2s(r_1)}\,d\tau \qquad \textbf{交换积分}$$

**物理意义（这是要理解的核心）**：

- **$J$（库仑积分）有经典对应**——就是两团电荷云之间的静电排斥
- **$K$（交换积分）没有任何经典对应**。看它的下标：右半边两个轨道的**电子标号交换了**。
  它纯粹来自波函数的反对称性要求，是彻底的量子效应

**$K > 0$，所以三重态比单重态低 $2K$。**

> 💡 **这就是 Hund 第一定则的量子力学根源**：
> 自旋平行（三重态）强制空间波函数**反对称**，而反对称波函数在 $r_1 \to r_2$ 时趋于零——
> 两个电子天然地互相远离，静电排斥小，能量低。
> **不是"自旋平行本身有什么魔力"，而是自旋平行通过 Pauli 原理强制了空间反对称。**

> 💡 **直接连到 HW1/HW2 的 BS-DFT 磁交换**：双核配合物里两个金属中心的
> 铁磁/反铁磁耦合常数 $J$，本质就是这里的交换相互作用推广到分子尺度。
> 参见 `03_Software_Methods/Gaussian/notes.md` 的 BS-DFT 一节。

（p.70 顺带给了个数字：近似的氦基态波函数给出能量 **−2.75 Ha**。）

### Slater 行列式（p.72–73）

1930 年代初 Slater 提出：用**行列式**自动构造反对称波函数。
若有 N 个占据的自旋轨道 $\phi_a, \phi_b, \dots$：

$$\Psi(1,2,\dots,N) = \frac{1}{\sqrt{N!}}
\begin{vmatrix}
\phi_a(1) & \phi_b(1) & \cdots & \phi_N(1) \\
\phi_a(2) & \phi_b(2) & \cdots & \phi_N(2) \\
\vdots & \vdots & \ddots & \vdots \\
\phi_a(N) & \phi_b(N) & \cdots & \phi_N(N)
\end{vmatrix}$$

**行列式的两条性质恰好对应 Pauli 原理**：

1. **交换任意两行（或两列），行列式变号** → 反对称性 ✅
2. **两行（或两列）相同时，行列式恒为 0** → 两个电子不能占据同一自旋轨道 ✅

数学工具和物理原理在这里完美吻合——这是量子化学里最漂亮的一步。

氦基态就是一个 2×2 行列式；激发单重态则需要**两个行列式的线性组合**（p.73）
——注意这个细节：**开壳层单重态天生不能用单个行列式描述**，这是后面 CASSCF 存在的理由之一。

### 轨道能量依赖（p.74–75）

碱金属只有一个价电子，本该像氢原子那样能量只依赖主量子数 $n$。
但实际上电子-电子排斥**破坏了球对称性**，导致能量强烈依赖角量子数：

$$E_{ns} < E_{np} < E_{nd} < E_{nf}$$

原因是**外层电子对核的穿透能力**按 $s > p > d > f$ 递减。
（单电子原子里没有这个效应，能量对同一 $n$ 的所有 $l$ 都简并。）

---

## 九、Hartree-Fock（p.76–85）⭐⭐ 核心

### 出发点（p.76–77）

多电子体系基态波函数 = **一个 Slater 行列式**。
它自动满足 Pauli 不相容原理，**但完全不含电子关联**。行列式是归一化的。

多电子体系的完整 Hamiltonian（原子单位）包含五项：
核动能、核-核排斥、电子动能、核-电子吸引、电子-电子排斥。

### Born-Oppenheimer 化简（p.78–79）

BO 近似后：核动能项 $\sum_\alpha \nabla_\alpha^2 = 0$，核-核排斥 $V_{NN}$ = 常数。
剩下的电子 Hamiltonian 可以整理成：

$$\hat{H} = \sum_i^{N_{elec}} \hat{h}_i + \frac{1}{2}\sum_i^{N_{elec}}\sum_{j\ne i}^{N_{elec}} \hat{g}_{ij} + V_{NN}$$

其中（p.80）

$$\hat{h}_i = -\nabla_i^2 - \sum_\alpha^{N_{nuc}} \frac{Z_\alpha}{|\vec{r}_i - \vec{r}_\alpha|} \qquad \text{（单电子：动能 + 核吸引）}$$

$$\hat{g}_{ij} = \frac{1}{|\vec{r}_i - \vec{r}_j|} \qquad \text{（双电子：电子排斥）}$$

### 能量表达式（p.82–83）⭐ 闭壳层

对 $E = \langle\Psi|\hat{H}|\Psi\rangle$ 展开、化简后（闭壳层）：

$$\boxed{E = 2\sum_i^{N/2} H_i + \sum_i^{N/2}\sum_j^{N/2}\left(2J_{ij} - K_{ij}\right) + V_{NN}}$$

| 符号 | 名称 | 表达式 |
|---|---|---|
| $H_i$ | **core Hamiltonian**，单电子积分 | $\langle\phi_i(1)|\hat{h}|\phi_i(1)\rangle$ |
| $J_{ij}$ | **库仑积分** | $\langle\phi_i(1)\phi_j(2)|\hat{g}|\phi_i(1)\phi_j(2)\rangle$ |
| $K_{ij}$ | **交换积分** | $\langle\phi_i(1)\phi_j(2)|\hat{g}|\phi_j(1)\phi_i(2)\rangle$ ← **右侧下标交换** |

$J$ 和 $K$ 统称 **ERI（Electron Repulsion Integrals，双电子积分）**。

> 💡 **这是量化计算贵的根本原因**：ERI 的数量随基函数数 $N$ 按 $N^4$ 增长。
> 200 个基函数就有约 $8\times10^8$ 个积分。
> ORCA 的 `RIJCOSX`、MOLCAS 的 `RICD`（Cholesky 分解）解决的就是这个问题——
> 你在模板里写的那些加速关键字，都是在对付这个 $N^4$。

### 变分 → Fock 算符（p.84）

$\phi_i$ 的具体形式还没定。按**变分原理**对分子轨道系数求能量极小，得到

$$\hat{F}\phi_i(1) = \varepsilon_i \phi_i(1)$$

$$\hat{F} = -\nabla_1^2 - \sum_\alpha \frac{Z_\alpha}{|\vec{r}_1 - \vec{r}_\alpha|} + \sum_j^{N/2}\left[2\hat{J}_j(1) - \hat{K}_j(1)\right]$$

$\varepsilon_i$ 是轨道能量，$\hat{F}$ 叫 **Fock 算符**。

> ⚠️ **这里藏着 HF 的自指困境（考点）**：
> Fock 算符里含有 $\hat{J}_j$ 和 $\hat{K}_j$，而它们**依赖于你正在求解的那些轨道 $\phi_j$**。
> 所以这不是普通的本征值问题——**必须迭代**。这就是 SCF 的由来，不是工程上的偷懒，
> 是方程结构本身要求的。

总能量（p.85）：$E = \sum_i^{N_{occ}} \gamma_i \varepsilon_i$，$\gamma_i$ 是轨道 i 的占据数。

---

## 十、Hartree-Fock-Roothaan（p.86–90）⭐⭐ 最终落地

HF 方程是**积分微分方程**，直接解很难。
Roothaan（1955）的贡献：**用 LCAO 把它变成矩阵方程**。

$$\phi_i = \sum_s^N c_{si}\,\chi_s \qquad \text{（分子轨道 = 原子轨道的线性组合）}$$

代入 $\hat{F}\phi_i = \varepsilon_i\phi_i$，左乘 $\chi_t^*$ 并积分：

$$\boxed{\sum_s^N c_{si}\left(F_{ts} - \varepsilon_i S_{ts}\right) = 0, \qquad t = 1,2,\dots,N}$$

其中

$$F_{ts} = \langle\chi_t|\hat{F}|\chi_s\rangle \quad \textbf{(Fock 矩阵)}, \qquad S_{ts} = \langle\chi_t|\chi_s\rangle \quad \textbf{(重叠矩阵)}$$

要有非平凡解，**久期行列式 (secular determinant) 必须为零**：

$$\left|F_{ts} - \varepsilon_i S_{ts}\right| = 0$$

> Ungur 的原话：**这些方程用自洽场 (SCF) 迭代求解，使总能量收敛到容许的阈值。
> 这些方程构成了现代量子化学与计算化学的基础。**

### SCF 循环长什么样

```
猜一组初始系数 c（初始猜测）
   ↓
用 c 构造密度矩阵 → 算 J 和 K 积分 → 组装 Fock 矩阵 F
   ↓
解广义本征值问题 FC = SCε  → 得到新的 c 和轨道能 ε
   ↓
新 c 与旧 c 的差别够小？ ── 否 ──┐
   ↓ 是                          │
收敛，输出能量  ←─────────────────┘
```

> 💡 **这就是 Gaussian 日志里 `SCF Done` 那一行的含义**，
> 也是 ORCA 的 `TightSCF`、VASP 的 `EDIFF` 在控制的东西。
>
> **"SCF 不收敛"** = 这个迭代在打转。两类原因：
> ① 初始猜测太差（→ 换更好的初猜、先用小基组）；
> ② **体系本身有近简并态，单个 Slater 行列式根本描述不了**
>   （→ 这正是 HW3 要用 CASSCF 的原因，见 `03_Software_Methods/OpenMOLCAS/notes.md`）

### 剩下的困难（p.88）

从 HFR 方程出发，需要算大量 $J$、$K$ 积分并求系数 $c_{si}$。
**积分数量太大，所以还要更多近似**——后续课程的 DFT、RI 近似、赝势都从这里长出来。

---

## 十一、RHF vs UHF（p.91）⭐⭐ 与作业直接相关

| | **自旋限制 RHF** | **自旋非限制 UHF** |
|---|---|---|
| 轨道 | 每个占据分子轨道放 **2 个**电子 | α 和 β **各优化一套独立轨道** |
| 自旋密度 | α 密度 ≡ β 密度 | 两者不同 |
| 平衡几何、基态附近 | 与 UHF 基本等价 | 与 RHF 基本等价 |
| **解离极限** | **表现很差** | **明显更好** |
| 代价 | — | **自旋污染 (spin contamination)** |

> ⚠️ 讲义 p.91 最后写 "The shape of spin-beta orbitals **is identical to** spin-alpha orbitals"，
> 与同段前面的说法矛盾，应是**笔误**（自旋非限制的两套轨道形状**不相同**才对）。
> 答题时按物理理解写。

### 为什么解离时 RHF 会崩（这就是作业问的"为什么不同"）

以 H₂ 为例。RHF 强制两个电子共用同一个空间轨道
$\sigma_g = \frac{1}{\sqrt2}(1s_A + 1s_B)$，双占据。展开 $\sigma_g(1)\sigma_g(2)$：

$$\sigma_g(1)\sigma_g(2) \propto \underbrace{A(1)B(2) + B(1)A(2)}_{\text{共价：H}\cdot + \cdot\text{H}} + \underbrace{A(1)A(2) + B(1)B(2)}_{\text{离子：H}^-\text{H}^+}$$

**共价项和离子项永远各占 50%，与核间距 R 无关。**

但物理上 $R \to \infty$ 时应该是两个中性氢原子，离子项该趋于零。
所以 **RHF 的解离能量太高**——它趋向 $\frac{1}{2}[E(\text{H}+\text{H}) + E(\text{H}^-+\text{H}^+)]$，
解离曲线在大 R 处**平不下来、明显抬高**。

UHF 允许 α 电子局域到 A 核、β 电子局域到 B 核。
超过 **Coulson–Fischer 点**（约 1.2–1.5 倍平衡键长）后，UHF 会自发**破坏自旋对称性**，
找到一个能量低于 RHF 的解，**正确解离到 2 × E(H)**。

**代价**：UHF 波函数**不再是 $\hat{S}^2$ 的本征函数**。
H₂ 解离过程中 $\langle S^2\rangle$ 从 0 逐渐涨到约 1——三重态混了进来。
**这就是自旋污染。**

> 💡 这条逻辑和 HW1/HW2 的 **BS-DFT** 完全同构：破对称解用"不物理的自旋污染"
> 换取"正确的能量描述"。也解释了 `Gaussian/pitfalls.md` 里那条
> "开壳层结果不对，⟨S²⟩ 远大于理论值 → 加 `stable=opt`"。

---

## 十二、实践部分（p.92–100）

课程实践部分的安排：Linux 基础 → 在集群上装 ORCA/MOLCAS → 准备输入 →
写作业提交脚本 → 提交测试计算（PBS 调度）→ 看输出。

### Linux 要点（p.93–98）

| 概念 | 内容 |
|---|---|
| `$HOME` (`~/`) | 你的家目录，完全自主。`/` 是根目录，只有 root 能改，很危险 |
| `/boot/` `/usr/` `/bin/` `/etc/` `/opt/` | 启动信息 / 包管理器装的软件 / 系统基本工具 / 配置和本地数据库 / 自己编译的软件 |
| **`$PATH`** | 冒号分隔的目录列表。**只有在 PATH 里的可执行文件，系统才找得到、才能直接调用** |
| **`$LD_LIBRARY_PATH`** | 告诉系统去哪些额外目录找动态库。**ORCA 启动崩溃常常就是这个没设对** |
| `.bash_profile` / `.bashrc` / `.vimrc` | 用户自定义（别名、PATH、程序变量）。**千万别删**，删了会各种"找不到程序" |

讲义给的 ORCA 环境设置范例（p.95–96）：

```bash
export ORCA=$HOME/software/orca_5_0_3_linux_x86-64_openmpi411
export PATH=$ORCA/:$PATH
echo $PATH                 # 确认加进去了
which orca                 # 确认系统能找到
ldd $ORCA/orca             # 检查动态库是否都能解析
export LD_LIBRARY_PATH=<目录>:$LD_LIBRARY_PATH   # 缺库时补上
ldd $ORCA/orca             # 再检查一次
```

> Ungur 特别说明：`ldd` 报告有库找不到时，**这不代表 ORCA 装坏了**，
> 只是操作系统不知道去哪儿找而已，设好 `LD_LIBRARY_PATH` 就行。

> ⚠️ **两条要回填到工作台的重要信息**：
> 1. 版本是 **ORCA 5.0.3 + OpenMPI 4.1.1**（文件名里的 `openmpi411`），
>    不是课程大纲写的 ORCA 6。这也**印证了** `ORCA/pitfalls.md` 里"MPI 版本必须精确匹配"那条。
> 2. p.92 写的是在 **NSCC**（新加坡国家超算中心）上装 ORCA/MOLCAS，
>    而不是 `00_Course_Info/README.md` 里写的 HPC@NUS。**必须确认到底用哪个集群。**

### vi 编辑器（p.99）

> 超算上的 Linux 通常装得很"苦行"，emacs 之类常常没有，但**所有 Unix 系统都有 vi**。

| 命令 | 作用 |
|---|---|
| `vi <文件名>` | 打开文件 |
| `:q` | 不保存退出 |
| `:ZZ`（或 `:wq`） | 保存并退出 |
| `i` / `Shift-I` | 进入插入模式 |
| `Shift-V` | 选中一行 |
| `Shift-Y` | 复制选中内容 |

老师说会用邮件发 vi 速查表。

### 常用命令（p.100）

```bash
cp <f1> <f2>       # 复制          mv <f1> <f2>     # 移动/改名
rm <f1>            # 删除          cd <dir>         # 进目录
cd ../             # 上一级        chmod +x <f1>    # 加可执行权限
touch <f1>         # 更新时间戳    zip a.zip <f1>   # 压缩
sh script.sh       # 执行脚本（= ./script.sh）
qsub script.sh     # 提交作业到队列系统
qdel JOBID         # 删除作业
```

（更完整的 PBS 命令见 `06_Cheatsheets/pbs.md`。）

---

## 十三、📌 作业任务（p.101）

> **Study the potential energy surface of H₂ at RHF level of theory in the domain
> 0.5–10 Å, at minimum 20 points.** Automate the calculation by the following bash loop.
> Input files for Gaussian PES/H₂ are uploaded in Canvas.
> **Compare the results with UHF results. Keep the same identical basis sets for both cases.
> Can you explain why the results differ?**
> As alternative, you may use the `scan` function in Gaussian / GaussView.

讲义给的自动化循环：

```bash
input=Gaussian_PES_H2_UB3LYP
for R in 0.50 0.55 0.60 0.65 0.70 0.75 0.80 0.85 0.90 0.95 1.00 1.05 1.10 1.15 1.20 1.25 ; do
   sed -e "s/DISTANCE/$R/g"  $input.gjf  > "$input"_R_"$R".gjf
   g16  <  "$input"_R_"$R".gjf           > "$input"_R_"$R".log
   echo "The calculation is done!"
done
grep 'SCF Done' "$input"_*.log > results.txt
```

### ⚠️ 三个必须注意的坑

1. **讲义给的循环不满足题目要求。**
   它只到 **1.25 Å、共 16 个点**，而题目要求 **0.5–10 Å、至少 20 个点**。
   **必须自己把 R 列表扩展到 10 Å。** 建议近处密、远处疏：
   键长附近（0.5–1.5 Å）用 0.05–0.1 Å 步长，1.5–3 Å 用 0.25 Å，3–10 Å 用 0.5–1 Å。
   —— 解离行为的差异正是在大 R 处才显现，只算到 1.25 Å 什么都看不出来。

2. **原理是 `sed` 模板替换。**
   `.gjf` 模板里把键长写成字面量 `DISTANCE`，循环逐个替换成数值。所以模板坐标段应该是：
   ```
   H  0.0  0.0  0.0
   H  0.0  0.0  DISTANCE
   ```

3. **文件名叫 `..._UB3LYP`，但题目要的是 RHF 和 UHF。**
   检查 Canvas 上下载的输入文件里的方法关键字，需要改成 `RHF` 和 `UHF`，
   且**两次必须用完全相同的基组**（题目明确要求）。

### 答案要点（"为什么结果不同"）

详见第十一节。核心三句：

1. **短距离（平衡键长附近）**：RHF ≈ UHF——UHF 会自动塌回 RHF 解，因为此时它就是最低解
2. **超过 Coulson–Fischer 点后**：UHF 自发破缺自旋对称性，能量**低于** RHF
3. **解离极限**：RHF 因强制双占据而永远含 50% 不该有的离子项 H⁻H⁺，能量**过高**；
   UHF 允许两电子各自局域，正确趋向 2 × E(H)。**代价是 $\langle S^2\rangle$ 从 0 涨到 ≈1，即自旋污染**

**报告里应该放**：
- 两条 PES 曲线叠在同一张图（横轴 R，纵轴 E）
- 标出两条曲线开始分离的位置 = **Coulson–Fischer 点**
- $\langle S^2\rangle$ 随 R 变化的曲线（`grep "S\*\*2" *.log` 提取）
- 与实验解离能 $D_e(\text{H}_2) \approx 4.75$ eV 对比，说明 HF 差的那一块正是**电子关联能**
  （呼应第七节的平均场近似）

数据提取（配合 `Gaussian/notes.md`）：

```bash
grep 'SCF Done' *.log | awk '{print $5}'      # 取能量
grep 'S\*\*2' *.log                            # 取 <S^2>
```

---

## 与后续课程/作业的连接

| 这一讲的概念 | 后面用在哪 |
|---|---|
| 完备集 / 基函数 | 基组选择（全部四次作业） |
| 径向函数被制表在基组里 | 为什么换基组会改变结果 |
| **交换积分 $K$** | HW1/HW2 的 **BS-DFT 磁交换常数** |
| 平均场丢掉电子关联 | MP2 / CCSD / DFT 泛函 |
| 单行列式不够用 | **HW3 的 CASSCF / CASPT2** |
| SCF 自洽循环 | 所有软件的 SCF 收敛问题 |
| RHF/UHF 与自旋污染 | HW1/HW2 开壳层计算、BS-DFT |
| $\hat{L}^2$、$\hat{L}_z$、自旋算符 | **HW3 的 RASSI 自旋轨道耦合** |
| Linux / PATH / LD_LIBRARY_PATH | 集群上跑任何软件 |

---

## 自测清单

- [ ] 能说出判断"要不要用量子力学"的定量标准（ΔE 与 $k_BT$）
- [ ] 能从经典波动方程 + de Broglie 关系推到定态薛定谔方程
- [ ] 能解释为什么定态的概率密度不随时间变化
- [ ] 能推导 $[\hat{x},\hat{p}] = i\hbar$ 并说明它的物理含义
- [ ] 能背出五条公设，并解释公设 4 的两种情况
- [ ] 能解释"$[\hat{A},\hat{B}]=0$ ⟹ 共享本征函数"，以及它如何给出 $l$ 和 $m$
- [ ] 能解释氢原子为什么可解、氦原子为什么不可解（$1/r_{12}$）
- [ ] 能说清 BO / 轨道近似 / 平均场三层近似**各自丢了什么**
- [ ] 能写出 Pauli 原理的反对称形式，并解释 Slater 行列式为何自动满足它
- [ ] **能区分 $J$ 和 $K$，解释 $K$ 为何没有经典对应、为何导致三重态更低（Hund 规则）**
- [ ] 能写出闭壳层 HF 能量表达式并说明每一项的物理意义
- [ ] **能解释为什么 HF 必须迭代求解（Fock 算符依赖于待求轨道）**
- [ ] 能说清 LCAO 如何把 HF 方程变成矩阵方程（Fock 矩阵、重叠矩阵、久期行列式）
- [ ] **能解释 H₂ 解离时 RHF 为何失败、UHF 为何更好、代价是什么**
