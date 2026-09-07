# Exercise 4（理论题 #1，5 分）

**题目**：描述 Hartree–Fock 自洽场方法中用到的基本近似——Born–Oppenheimer 近似、
轨道近似、平均场近似——并说明它们各自如何简化计算问题。

> 下面是可直接进报告的答案（中英对照要点 + 公式）。写报告时保持 “be concise”，
> 每个近似讲清三件事：**假设什么 / 数学后果 / 计算上省了什么**。

---

## 出发点：为什么需要近似

一个 N 电子、M 核的分子，完整的非相对论定态薛定谔方程是

$$\hat H\,\Psi(\mathbf r_1\dots\mathbf r_N,\mathbf R_1\dots\mathbf R_M)=E\,\Psi$$

$$\hat H=-\sum_A\frac{\nabla_A^2}{2M_A}-\sum_i\frac{\nabla_i^2}{2}
-\sum_{i,A}\frac{Z_A}{r_{iA}}+\sum_{i<j}\frac{1}{r_{ij}}+\sum_{A<B}\frac{Z_AZ_B}{R_{AB}}$$

*读法：动能（核）+ 动能（电子）+ 电子–核吸引 + 电子–电子排斥 + 核–核排斥。*

这是一个 $3(N+M)$ 维的偏微分方程，**电子–电子排斥项 $\sum 1/r_{ij}$ 把所有电子的坐标耦合在一起**，
无法解析求解，维数也让直接数值求解不可能。三个近似逐层把它拆开。

---

## 近似一：Born–Oppenheimer（玻恩–奥本海默）

**假设**：原子核质量比电子大 3–4 个数量级（质子 ≈ 1836 电子质量），核运动比电子慢得多。
于是可以认为**电子瞬时地适应任何一组固定的核位置**，把核坐标 $\{\mathbf R_A\}$ 当作参数而非变量。

**数学后果**：总波函数分离为 $\Psi \approx \psi_{\text{el}}(\mathbf r;\mathbf R)\,\chi_{\text{nuc}}(\mathbf R)$，
核动能项被丢掉，核–核排斥变成常数，得到**电子哈密顿量**和**电子薛定谔方程**：

$$\hat H_{\text{el}}=-\sum_i\frac{\nabla_i^2}{2}-\sum_{i,A}\frac{Z_A}{r_{iA}}+\sum_{i<j}\frac{1}{r_{ij}},
\qquad \hat H_{\text{el}}\,\psi_{\text{el}}=E_{\text{el}}(\mathbf R)\,\psi_{\text{el}}$$

**计算上省了什么**：
- 不用解核的量子运动，问题维数从 $3(N+M)$ 降到 $3N$。
- $E_{\text{el}}(\mathbf R)+V_{nn}(\mathbf R)$ 作为核坐标的函数，就是**势能面 (PES)** —— 几何优化、
  过渡态、振动频率、反应路径这些概念全都建立在这个近似上。
- 核的运动之后可以在 PES 上单独处理（谐振子近似 → 频率）。

**失效场景**：电子态近简并处（锥形交叉、Jahn–Teller、非绝热跃迁），此时 PES 之间强耦合。

---

## 近似二：轨道近似（Orbital / Independent-particle Approximation）

**假设**：N 电子波函数可以用**单电子函数（自旋轨道 $\chi_i$）的乘积**来构造。为满足
电子是费米子、波函数必须对交换任意两个电子反对称（Pauli 原理），用**Slater 行列式**而非简单乘积：

$$\Psi_{\text{HF}}(\mathbf x_1\dots\mathbf x_N)=\frac{1}{\sqrt{N!}}
\begin{vmatrix}
\chi_1(\mathbf x_1) & \chi_2(\mathbf x_1) & \cdots & \chi_N(\mathbf x_1)\\
\chi_1(\mathbf x_2) & \chi_2(\mathbf x_2) & \cdots & \chi_N(\mathbf x_2)\\
\vdots & & \ddots & \vdots\\
\chi_1(\mathbf x_N) & \chi_2(\mathbf x_N) & \cdots & \chi_N(\mathbf x_N)
\end{vmatrix}$$

*读法：每个电子“占据”一个自旋轨道；行列式形式自动保证反对称（交换两行变号）和
Pauli 不相容（两个轨道相同 → 行列式为零）。*

**数学后果**：把“求一个 $3N$ 维的多电子波函数”换成“求 $N$ 个三维的单电子轨道”。

**计算上省了什么**：
- 未知量从一个 $3N$ 维函数变成 $N$ 个 3 维函数 —— 可以用有限的原子轨道基组展开
  （$\varphi_i=\sum_\mu c_{\mu i}\chi_\mu$，Roothaan–Hall），把微分方程问题变成**矩阵代数**。
- 能量、密度等物理量都能写成轨道的简单求和/积分。

**代价**：真实波函数**不是**单个行列式（Full CI 才是所有行列式的线性组合）。
单行列式丢掉的部分就是**电子相关能**（Lecture 04 的主题）。

---

## 近似三：平均场近似（Mean-Field / Hartree–Fock）

**假设**：每个电子不感受其他电子的**瞬时位置**，只感受它们的**平均电荷分布**产生的静电场。

**数学后果**：耦合的双电子算符 $\sum_{i<j}1/r_{ij}$ 被替换成作用在单个电子上的**有效单电子算符**
—— Fock 算符：

$$\hat f(1)=\hat h(1)+\sum_{j}^{\text{occ}}\big[\hat J_j(1)-\hat K_j(1)\big],
\qquad \hat f\,\varphi_i=\varepsilon_i\,\varphi_i$$

其中 $\hat h$ 是单电子项（动能 + 电子–核吸引），$\hat J_j$ 是电子 $j$ 的平均库仑势，
$\hat K_j$ 是非经典的交换项（来自 Slater 行列式的反对称性，只作用于同自旋电子）。
HF 总能量：

$$E_{\text{HF}}=\sum_i h_{ii}+\tfrac12\sum_{i,j}\big(J_{ij}-K_{ij}\big)+V_{nn}$$

**自洽性**：Fock 算符依赖于所有占据轨道（通过 $\hat J,\hat K$），而占据轨道又是 Fock 算符的
本征函数 —— 所以必须**迭代到自洽（SCF）**：猜密度 → 建 Fock 矩阵 → 对角化 → 新密度 → 重复，
直到能量和密度不再变化。收敛判据背后是**变分原理**（$E_{\text{trial}}\ge E_{\text{exact}}$）。

**计算上省了什么**：
- $N$ 个电子的相互耦合问题 → $N$ 个**互相独立**的单电子本征值问题（每个电子在平均场中运动）。
- 标度：形式上 $O(N^4)$（双电子积分数目），配 RI/密度拟合可降到 $O(N^3)$ —— 相比 Full CI 的
  $O(N!)$ 是天壤之别。

**代价**：平均场 = 忽略电子的瞬时“躲避”（动态相关）。HF 通常回收约 99% 的总能量，
但缺的那 ~1%（相关能，量级 ~eV/电子对）对键能、反应势垒、弱相互作用往往是决定性的。

---

## 一句话总结（可作结尾）

三个近似依次把问题降维：
**Born–Oppenheimer** 把核和电子分开（$3(N{+}M)\to 3N$，给出 PES）；
**轨道近似** 把多电子波函数写成单电子轨道的反对称乘积（$3N$ 维函数 → $N$ 个 3 维轨道，可用基组展开）；
**平均场近似** 把电子间的瞬时排斥换成平均场（耦合问题 → $N$ 个独立的单电子 SCF 本征值问题，
标度从 $O(N!)$ 降到 $O(N^{3\text{–}4})$）。代价是丢失动态电子相关，由 post-HF 方法补回。
