# Ex1 的三张图是怎么用 Avogadro 做出来的（2026-09-24 完成记录）

题目原文：*"Plot the electronic density together with the electrostatic potential ... **using Avogadro or
Chemcraft**"*，所以这三张图必须在 Avogadro 里出。**已经做完了**，本文件是记录 + 万一要重做时的步骤。

成品：`avogadro_screenshots\` 里的三个 png（外加脚本自动生成的拼图和裁好边的版本）。

---

## 结论：用 **molden** 文件，不要用 cube 文件

中间走过两条弯路，记下来免得重蹈：

| 走法 | 结果 |
|---|---|
| molden 拖进 **Avogadro 1.2** | **闪退**。1.2 是 2016 年的 32 位老程序，扛不住 568 个分子轨道 + `[9G]` 高角动量函数 |
| **cube** 文件（HOMO/LUMO/密度各一个） | 能画等值面，但**「着色依据」是灰的、点不动** → 做不出静电势图。cube 里只有格点数值、没有波函数，Avogadro 没法算静电势 |
| **molden 文件 + Avogadro 2** | ✅ 正解。不闪退，「表面」里直接有 `分子轨道` / `电子密度`，「着色依据」里有 `静电势` |

还踩到一个坑：**打开 cube 文件时 Avogadro 会自动画一次等值面（0.03）**，你再点一次「计算」（0.02）就变成
两层面套在一起，颜色混成紫的。molden 这条路没有这个问题（打开时不自动画面，点几次「计算」都是替换不是叠加）。

---

## 重做步骤（Avogadro 2，中文界面）

用的文件：
`Ex1_2Cl_phenol\B3LYP_gas\ex1_orbitals_density_B3LYP_gas.molden`
（做图时为保险复制到了纯英文路径 `桌面\CM5235_Avogadro\`，其实 Avogadro 2 读中文路径没问题）

### 0. 启动

- 开始菜单搜 **Avogadro2**（蓝色图标）。
- 启动时会弹 **「安装更新的插件？」** → 点 **否**。那些是联网下载的第三方插件，画等值面用不到。
- **文件 → 打开**，选那个 `.molden`。

### 1. 一次性的显示设置

| 菜单 | 设成 | 为什么 |
|---|---|---|
| 视图 → 设置背景颜色 | 白色 `#ffffff` | 报告是白底 |
| 视图 → 投影方法 | **正交** | 分子不会近大远小，比例可信 |
| 视图 → 居中 | — | 把分子摆到画面中间 |

然后**左键拖动**把苯环转到正对屏幕（鼠标：左键拖=转，滚轮=缩放，右键拖=平移）。
**三张图用同一个视角**，报告里才能互相对照 —— 所以先把角度调好，后面只换表面、不动相机。

### 2. HOMO

**分析 → 创建表面...**，对话框里：

- **表面**：`分子轨道`
- 右边那个下拉：选 **`分子轨道 33 (HOMO)`**
  （标签被框宽截断成 `分子...O)`，认不出来就点开下拉按 `Home`，再按 32 次 `↓`。
  Avogadro 从 1 数，ORCA 从 0 数，所以 ORCA 输出里的 "orbital 32" = 这里的 33。
  2-氯苯酚 66 个电子 → 33 个占据轨道，对得上）
- **等值面值**：`0.0200`
- 点 **计算** → **关闭**

工具栏 **`导出图像...`** → 存成 `ex1_avogadro_HOMO.png`。

### 3. LUMO

同上，轨道换成 **`分子轨道 34 (LUMO)`**（下拉里 HOMO 的下一个），等值面值同样 `0.0200`。
存成 `ex1_avogadro_LUMO.png`。

> 怎么确认没选错：HOMO 在苯环上只有**一个节面**（上半红、下半蓝），氧上有明显的瓣；
> LUMO 节面更多（红蓝交替），**氧上几乎没有瓣**。和 `ex1_fig_HOMO_LUMO_B3LYP_gas.png`（ORCA cube 渲染的参考图）一对就知道。

### 4. 电子密度 + 静电势

**分析 → 创建表面...**：

- **表面**：`电子密度`
- **着色依据**：`静电势`（选了 `电子密度` 之后这一栏才会亮）
- 旁边的电荷模型：`EEM`（默认，另有 EEM 2015 / Gasteiger / MMFF94）
- **配色方案**：`Balance`（红=负、蓝=正。另外几个 Blue-DarkRed / Coolwarm / Spectral / Turbo 试过，对比度没更好）
- **等值面值**：`0.0010`
- **计算** → **关闭**

最后调不透明度：左边 **显示类型** 面板里 `表面` 那行的 **`•••`** → **表面 设置** → **不透明度** 滑到约 **80%**。
全不透明时看不见里面的分子（分不清哪边是 O、哪边是 Cl），全透明时颜色太淡，80% 左右最好看。

存成 `ex1_avogadro_density_ESP.png`。

---

## 一个必须在报告里讲清楚的点

**Avogadro 的静电势是点电荷算的，不是波函数算的。**

「着色依据」旁边只能选 EEM / Gasteiger / MMFF94 —— 都是把电荷放在原子核上的经验模型。
后果：氧上的负区、氢上的正区它画得对，但**苯环上下 π 面的负电势它画不出来**，
因为那来自 π 电子的分布，任何原子中心点电荷都描述不了。

所以报告里的数值（−0.035 ~ +0.061 a.u.）取自 **ORCA 的 `orca_vpot`**（从波函数直接算，
数据在 `cube_job\ex1_esp_values_on_grid_B3LYP_gas.txt`，13 万个格点），
图用 Avogadro 的（题目要求），并在图注和正文里写明了这个区别。

---

## 这些图进了报告哪里

`03_report_word\scripts\make_ex1_word.py` 里的 `avogadro_figure()` 会自动：

1. 优先找 `avogadro_screenshots\` 下的三个 png（找不到才退回 PyVista 渲染的版本）
2. 把透明背景压到白底上（Avogadro 导出的 PNG 是透明底，直接用会变黑底）
3. 裁掉视口的白边，HOMO / LUMO 并排拼成一张并标上文字

生成物 `ex1_avogadro_HOMO_LUMO_combined.png` 和 `ex1_avogadro_density_ESP_trimmed.png`
是脚本自动产生的，不用手动维护，删了重跑脚本就有。

改完图之后重新生成报告：

```
D:\venvs\cm5235_hw2\Scripts\python.exe make_ex1_word.py
D:\venvs\cm5235_hw2\Scripts\python.exe make_final_report.py
powershell -ExecutionPolicy Bypass -File docx_to_pdf.ps1 "<docx 完整路径>"
```

（这几个脚本要用 `D:\venvs\cm5235_hw2` 里的 python，系统默认的 anaconda 没装 pyvista。）
