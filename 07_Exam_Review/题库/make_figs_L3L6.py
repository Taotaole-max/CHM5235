# 生成 L3-L6 题库用的图：讲义截图 + matplotlib 示意图，输出到 img/
import pymupdf, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
OUT = Path(__file__).parent / "img"; OUT.mkdir(exist_ok=True)
LEC = Path(r"C:/Users/letaotao/Desktop/CM5235")
L3 = pymupdf.open(LEC / "CM5235_Lecture_03 (1).pdf")
L4 = pymupdf.open(LEC / "CM5235_Lecture_04 (1).pdf")

def crop(doc, page, rect, name, z=2.2):
    doc[page - 1].get_pixmap(matrix=pymupdf.Matrix(z, z), clip=pymupdf.Rect(*rect)).save(OUT / name)

# 讲义截图（页面 720x540 pt）
crop(L3, 72, (0, 0, 720, 540), "L3_p72_sto_gto.png", z=1.4)
crop(L4, 21, (0, 0, 720, 540), "L4_p21_h2_fci.png", z=1.4)

# 1. H 原子变分：两种试探函数的 E(α)
a = np.linspace(0.2, 2.6, 300)
fig, ax = plt.subplots(figsize=(6.4, 3.4))
ax.plot(a, a**2 / 2 - a, lw=2, label=r"$\psi\propto e^{-\alpha r}$：$E=\alpha^2/2-\alpha$")
ax.plot(a, a**2 / 6 - a / 2, lw=2, label=r"$\psi\propto r\,e^{-\alpha r}$：$E=\alpha^2/6-\alpha/2$")
ax.axhline(-0.5, color="k", ls="--", lw=1); ax.text(2.0, -0.53, "精确 1s：−0.5 Ha", fontsize=9, va="top")
ax.axhline(-0.125, color="gray", ls=":", lw=1); ax.text(2.0, -0.11, "精确 n=2：−0.125 Ha", fontsize=9, color="gray")
ax.plot([1], [-0.5], "o", color="tab:blue"); ax.plot([1.5], [-0.375], "o", color="tab:orange")
ax.annotate("α=1，E=−0.5（正好是精确解）", xy=(1, -0.5), xytext=(0.25, -0.2), fontsize=9, arrowprops=dict(arrowstyle="->"))
ax.annotate("α=1.5，E=−0.375", xy=(1.5, -0.375), xytext=(1.6, -0.28), fontsize=9, arrowprops=dict(arrowstyle="->"))
ax.set_xlabel("α（轨道收缩程度）"); ax.set_ylabel("E / Ha"); ax.set_ylim(-0.6, 0.3)
ax.legend(fontsize=9, loc="upper left"); ax.set_title("变分：调参数找能量最低点，最低点仍在精确值之上")
fig.tight_layout(); fig.savefig(OUT / "fig_var_h_atom.png", dpi=170); plt.close(fig)

# 2. Ne 各激发级别的权重（L4 p16）
lv = np.arange(0, 9)
w = [0.96, 9.8e-4, 3.4e-2, 3.7e-4, 4.5e-4, 1.9e-5, 1.7e-6, 1.4e-7, 1.1e-9]
fig, ax = plt.subplots(figsize=(6.4, 3.0))
bars = ax.bar(lv, w, color=["gray", "tab:blue", "tab:red", "tab:blue", "tab:red", "tab:blue", "tab:red", "tab:blue", "tab:red"])
ax.set_yscale("log"); ax.set_xticks(lv); ax.set_xlabel("激发级别（0 = HF 行列式，1 = 单激发，2 = 双激发 …）")
ax.set_ylabel("权重"); ax.set_title("Ne 的 FCI 波函数：双激发远大于单激发，四激发 > 三激发")
fig.tight_layout(); fig.savefig(OUT / "fig_ne_weights.png", dpi=170); plt.close(fig)

# 3. 两个 S=1/2 自旋的 Heisenberg 能级
fig, axs = plt.subplots(1, 2, figsize=(6.6, 3.0))
for ax, J, title in [(axs[0], +1, "J > 0：铁磁（三重态更低）"), (axs[1], -1, "J < 0：反铁磁（单重态更低）")]:
    Et, Es = -J / 2, 1.5 * J
    for E, lab, c in [(Et, "三重态 S=1（3 个）", "tab:blue"), (Es, "单重态 S=0（1 个）", "tab:red")]:
        ax.plot([0, 1], [E, E], color=c, lw=3); ax.text(1.05, E, lab, va="center", fontsize=9, color=c)
    ax.annotate("", xy=(0.5, Et), xytext=(0.5, Es), arrowprops=dict(arrowstyle="<->"))
    ax.text(0.55, (Et + Es) / 2, "|2J|", fontsize=10)
    ax.set_xlim(-0.1, 2.6); ax.set_ylim(-2, 2); ax.axis("off"); ax.set_title(title, fontsize=10)
fig.suptitle(r"$\hat H=-2J\,\hat S_A\cdot\hat S_B$：$E_T=-J/2$，$E_S=+3J/2$，$E_T-E_S=-2J$", fontsize=10)
fig.tight_layout(); fig.savefig(OUT / "fig_heisenberg.png", dpi=170); plt.close(fig)

# 4. Lennard-Jones 势
r = np.linspace(0.92, 2.5, 300)
V = 4 * ((1 / r) ** 12 - (1 / r) ** 6)
fig, ax = plt.subplots(figsize=(6.0, 3.2))
ax.plot(r, V, "k", lw=2, label="LJ 总和")
ax.plot(r, 4 * (1 / r) ** 12, "tab:red", ls="--", label=r"$+4\varepsilon(\sigma/r)^{12}$ 排斥")
ax.plot(r, -4 * (1 / r) ** 6, "tab:blue", ls="--", label=r"$-4\varepsilon(\sigma/r)^{6}$ 色散吸引")
ax.axhline(0, color="gray", lw=0.8)
ax.plot([2 ** (1 / 6)], [-1], "o", color="k"); ax.annotate(r"极小：$r=2^{1/6}\sigma$，$V=-\varepsilon$", xy=(2 ** (1 / 6), -1), xytext=(1.35, -1.6), fontsize=9, arrowprops=dict(arrowstyle="->"))
ax.annotate(r"$V=0$ 处 $r=\sigma$", xy=(1, 0), xytext=(1.2, 1.2), fontsize=9, arrowprops=dict(arrowstyle="->"))
ax.set_ylim(-2.2, 2.5); ax.set_xlabel(r"$r/\sigma$"); ax.set_ylabel(r"$V/\varepsilon$"); ax.legend(fontsize=9)
ax.set_title("显式水模型中的 Lennard-Jones 项")
fig.tight_layout(); fig.savefig(OUT / "fig_lj.png", dpi=170); plt.close(fig)

# 5. 垂直激发 vs 绝热激发
x = np.linspace(-2, 3, 300)
g = 0.5 * x**2; e = 0.5 * (x - 1.0) ** 2 + 3.0
fig, ax = plt.subplots(figsize=(5.6, 3.4))
ax.plot(x, g, "k", lw=2); ax.plot(x, e, "tab:red", lw=2)
ax.annotate("", xy=(0, 3.5), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="tab:blue", lw=2))
ax.text(-1.25, 1.8, "垂直吸收\n（核不动）", color="tab:blue", fontsize=9)
ax.annotate("", xy=(1, 0.5), xytext=(1, 3.0), arrowprops=dict(arrowstyle="->", color="tab:green", lw=2))
ax.text(1.1, 1.3, "垂直发射", color="tab:green", fontsize=9)
ax.plot([0, 1], [0, 0], "k:"); ax.plot([1, 1.9], [3, 3], "k:")
ax.annotate("", xy=(1.9, 3.0), xytext=(1.9, 0), arrowprops=dict(arrowstyle="<->", color="gray"))
ax.text(1.95, 1.4, "绝热激发能\n（两个极小之差）", fontsize=9, color="gray")
ax.set_ylim(-0.3, 6); ax.set_xlabel("核坐标"); ax.set_ylabel("能量"); ax.set_xticks([]); ax.set_yticks([])
ax.set_title("吸收 > 绝热 > 发射（Stokes 位移）")
fig.tight_layout(); fig.savefig(OUT / "fig_vertical_adiabatic.png", dpi=170); plt.close(fig)
print("ok")
