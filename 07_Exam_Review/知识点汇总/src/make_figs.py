# 自绘示意图 → img/fig_*.png。黑白打印优先：用线型、标记和灰度区分，不靠颜色
import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

here = Path(__file__).parent
img = here / "img"
img.mkdir(exist_ok=True)
font_manager.fontManager.addfont("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc")
plt.rcParams.update({
    "font.family": ["DejaVu Sans", "WenQuanYi Zen Hei"],
    "font.size": 10, "axes.linewidth": 0.8, "lines.linewidth": 1.6,
    "axes.spines.top": False, "axes.spines.right": False,
    "savefig.dpi": 220, "savefig.bbox": "tight", "mathtext.fontset": "dejavusans",
})
K, G1, G2 = "#000000", "#555555", "#999999"
FIGS = {}


def fig(fn):
    FIGS[fn.__name__] = fn
    return fn


def save(f, name):
    f.savefig(img / f"{name}.png")
    plt.close(f)
    print("ok", name)


@fig
def fig_he_1s2s():
    f, ax = plt.subplots(figsize=(3.4, 2.6))
    ax.axis("off")
    lv = lambda x0, x1, y, **k: ax.plot([x0, x1], [y, y], color=K, lw=2, **k)
    lv(0, 1, 0); ax.text(0.5, -0.12, r"$E_{1s}+E_{2s}$", ha="center", va="top")
    lv(1.6, 2.6, 1.0); ax.text(2.1, 0.88, r"$+J$", ha="center", va="top")
    lv(3.2, 4.2, 1.6); ax.text(4.3, 1.6, "2¹S₀ 单重态", va="center")
    lv(3.2, 4.2, 0.4); ax.text(4.3, 0.4, "³S₁ 三重态", va="center")
    for (a, b, c, d) in [(1, 0, 1.6, 1.0), (2.6, 1.0, 3.2, 1.6), (2.6, 1.0, 3.2, 0.4)]:
        ax.plot([a, c], [b, d], ls=":", color=G1, lw=1)
    ax.annotate("", xy=(3.7, 1.6), xytext=(3.7, 0.4), arrowprops=dict(arrowstyle="<->", color=K))
    ax.text(3.6, 1.0, "2K", ha="right", va="center", fontsize=11, fontweight="bold")
    ax.text(4.3, 1.33, "+K", color=G1, fontsize=9); ax.text(4.3, 0.67, "−K", color=G1, fontsize=9)
    ax.set_xlim(-0.2, 6.2); ax.set_ylim(-0.4, 1.9)
    save(f, "fig_he_1s2s")


@fig
def fig_h2_rhf_uhf():
    R = np.linspace(0.45, 4.0, 400)
    De, a, Re = 0.174, 1.03, 0.74
    exact = -1.0 + De * ((1 - np.exp(-a * (R - Re))) ** 2 - 1)  # 以 2E(H) = −1 Ha 为解离极限
    rhf = exact + 0.02 + 0.25 * (1 - np.exp(-0.9 * (R - Re))) ** 2 * (R > Re)
    rcf = 1.2
    i0 = np.searchsorted(R, rcf)
    off = rhf[i0] - exact[i0]
    uhf = np.where(R < rcf, rhf, exact + off * np.exp(-2.2 * (R - rcf)))
    f, ax = plt.subplots(figsize=(3.4, 2.7))
    ax.plot(R, exact, color=K, lw=1.2, ls="-", label="精确（FCI）")
    ax.plot(R, rhf, color=K, lw=2, ls="--", label="RHF")
    ax.plot(R, uhf, color=G2, lw=2.4, ls="-", label="UHF")
    ax.axhline(-1.0, color=G1, lw=0.6, ls=":")
    ax.text(3.95, -0.99, "2E(H)", ha="right", va="bottom", fontsize=8, color=G1)
    ax.annotate("Coulson–Fischer 点", xy=(rcf, rhf[np.searchsorted(R, rcf)]), xytext=(1.5, -1.12),
                fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.7))
    ax.text(3.2, -0.83, "RHF 极限过高\n(50% 离子项)", fontsize=8, ha="center")
    ax.text(3.0, -1.07, r"UHF: $\langle S^2\rangle\to1$", fontsize=8, ha="center", color=G1)
    ax.set_xlabel("R (Å)"); ax.set_ylabel("E (Ha)")
    ax.set_ylim(-1.2, -0.72); ax.set_xlim(0.4, 4.0)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    save(f, "fig_h2_rhf_uhf")


@fig
def fig_ladder():
    f, ax = plt.subplots(figsize=(2.6, 3.4))
    ax.axis("off")
    rungs = [("1  LDA", "ρ"), ("2  GGA", "+ ∇ρ"), ("3  meta-GGA", "+ τ 或 ∇²ρ"),
             ("4  杂化", "+ HF 交换"), ("5  双杂化", "+ 虚轨道 (MP2)")]
    for i, (a, b) in enumerate(rungs):
        y = i * 1.0
        ax.plot([0, 3], [y, y], color=K, lw=2)
        ax.text(0.05, y + 0.12, a, fontsize=9, fontweight="bold", va="bottom")
        ax.text(2.95, y + 0.12, b, fontsize=8, va="bottom", ha="right", color=G1)
    ax.plot([0, 0], [-0.3, 4.6], color=K, lw=2.5); ax.plot([3, 3], [-0.3, 4.6], color=K, lw=2.5)
    ax.text(1.5, 5.0, "化学精度（天堂）", ha="center", fontsize=9)
    ax.text(1.5, -0.75, "Hartree 世界（无 xc）", ha="center", fontsize=8, color=G1)
    ax.annotate("", xy=(3.35, 4.5), xytext=(3.35, 0), arrowprops=dict(arrowstyle="->", lw=1.2))
    ax.text(3.45, 2.2, "更准\n更贵", fontsize=8, va="center")
    ax.set_xlim(-0.2, 4.1); ax.set_ylim(-1.0, 5.3)
    save(f, "fig_ladder")


@fig
def fig_scaling():
    import numpy as np
    K_ = np.linspace(10, 1000, 200)
    f, ax = plt.subplots(figsize=(3.2, 2.6))
    for p, ls, lab in [(3, ":", "K³ 对角化/RI"), (4, "-", "K⁴ HF"), (5, "--", "K⁵ MP2"), (6, "-.", "K⁶ CCSD/CISD"), (7, (0, (5, 1, 1, 1, 1, 1)), "K⁷ CCSD(T)")]:
        ax.plot(K_, (K_ / 10) ** p, color=K if p != 3 else G1, ls=ls, lw=1.4, label=lab)
    ax.set_yscale("log"); ax.set_xscale("log")
    ax.set_xlabel("基函数数 K"); ax.set_ylabel("相对耗时")
    ax.legend(frameon=False, fontsize=7, loc="upper left")
    save(f, "fig_scaling")


if __name__ == "__main__":
    names = sys.argv[1:] or list(FIGS)
    for n in names:
        FIGS[n]()
