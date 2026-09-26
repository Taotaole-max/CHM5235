# 生成 L1-L2 题库用的图：讲义截图 + matplotlib 示意图，输出到 img/
import pymupdf, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
OUT = Path(__file__).parent / "img"; OUT.mkdir(exist_ok=True)
L2 = pymupdf.open(r"C:/Users/letaotao/Desktop/CM5235/CM5235_Lecture_02 (1).pdf")

def crop(doc, page, rect, name, z=2.2):
    doc[page - 1].get_pixmap(matrix=pymupdf.Matrix(z, z), clip=pymupdf.Rect(*rect)).save(OUT / name)

# 讲义截图（坐标单位 pt，页面 720x540）
crop(L2, 9, (80, 220, 620, 500), "L2_p9_boltzmann.png")
crop(L2, 55, (140, 30, 560, 490), "L2_p55_radial.png")
crop(L2, 75, (60, 270, 660, 500), "L2_p75_penetration.png")

# 1. Boltzmann 布居比 vs ΔE/kT，标出 298 K 下的转动/振动/电子跃迁
fig, ax = plt.subplots(figsize=(6.4, 3.4))
x = np.logspace(-2, 2.3, 300)
ax.semilogx(x, np.exp(-x), lw=2)
kT = 207.0  # cm-1 at 298 K
for dE, lab, c in [(10, "转动 ~10 cm$^{-1}$", "tab:green"), (2000, "振动 ~2000 cm$^{-1}$", "tab:orange"),
                   (30000, "电子跃迁 ~30000 cm$^{-1}$", "tab:red")]:
    r = dE / kT
    ax.axvline(r, color=c, ls="--"); ax.text(r * (0.93 if r > 100 else 1.08), 0.55 if r < 1 else (0.6 if r > 100 else 0.3), lab, ha="right" if r > 100 else "left", color=c, fontsize=9)
ax.axvline(1, color="gray", lw=0.8); ax.text(1.05, 0.9, "ΔE = kT", color="gray", fontsize=9)
ax.set_xlabel("ΔE / k_BT  (298 K 时 k_BT ≈ 207 cm$^{-1}$)"); ax.set_ylabel("$n_2/n_1$ = e^(−ΔE/kT)")
ax.set_title("能级间隔和热能相比：什么时候必须用量子力学")
fig.tight_layout(); fig.savefig(OUT / "fig_boltzmann.png", dpi=170); plt.close(fig)

# 2. He 1s2s 单重态/三重态能级：E1s+E2s → +J → ±K
fig, ax = plt.subplots(figsize=(6.2, 3.6))
lv = dict(a=0.0, b=1.0, S=1.35, T=0.65)
def bar(x, y, t, c="k", side="right"):
    ax.plot([x, x + 1], [y, y], color=c, lw=2.5)
    if side == "right": ax.text(x + 1.08, y, t, va="center", fontsize=9, color=c)
    else: ax.text(x + 0.5, y + 0.07, t, ha="center", va="bottom", fontsize=9, color=c)
bar(0, lv["a"], "$E_{1s}+E_{2s}$\n(无电子排斥)", side="top")
bar(2.6, lv["b"], "+ J\n(平均库仑排斥)", side="top")
bar(5.4, lv["S"], "$2^1S$：+ J + K\n空间对称 × 自旋单重态", "tab:red")
bar(5.4, lv["T"], "$2^3S$：+ J − K\n空间反对称 × 自旋三重态", "tab:blue")
for y in (lv["S"], lv["T"]): ax.plot([3.6, 5.4], [lv["b"], y], "k:", lw=1)
ax.plot([1, 2.6], [lv["a"], lv["b"]], "k:", lw=1)
ax.annotate("", xy=(9.5, lv["T"]), xytext=(9.5, lv["S"]), arrowprops=dict(arrowstyle="<->"))
ax.text(9.6, 1.0, "ΔE = 2K", fontsize=10)
ax.set_xlim(-0.2, 11); ax.set_ylim(-0.1, 1.75); ax.axis("off")
ax.set_title("He 1s2s 激发态：交换积分 K 让三重态更低（Hund 规则的来源）")
fig.tight_layout(); fig.savefig(OUT / "fig_he_1s2s.png", dpi=170); plt.close(fig)

# 3. H2 解离：RHF / UHF / 精确 示意
R = np.linspace(0.6, 5, 300)
def morse(R, D, a, Re): return D * (1 - np.exp(-a * (R - Re))) ** 2 - D
Re, Rcf = 1.40, 2.3
exact = morse(R, 0.174, 1.0, Re)
rhf = exact + 0.04 + np.where(R > Re, 0.22 * (1 - np.exp(-0.8 * (R - Re))) ** 2, 0)
w = np.where(R > Rcf, 1 - np.exp(-2.0 * (R - Rcf)), 0)
uhf = rhf - w * (rhf - (exact + 0.006))
fig, ax = plt.subplots(figsize=(6.4, 3.6))
ax.plot(R, exact, "k", lw=2, label="精确 (FCI)")
ax.plot(R, rhf, "tab:red", lw=2, label="RHF")
ax.plot(R, uhf, "tab:blue", lw=2, ls="--", label="UHF")
ax.axhline(0, color="gray", lw=0.8); ax.text(4.2, 0.012, "2 个 H 原子", fontsize=9, color="gray")
ax.annotate("RHF 解离极限偏高：\n强行保留 50% 离子项 H$^+$H$^-$", xy=(4.6, rhf[-20]), xytext=(2.6, 0.2),
            arrowprops=dict(arrowstyle="->"), fontsize=9)
ax.annotate("Coulson–Fischer 点：\nUHF 从 RHF 分叉", xy=(2.3, uhf[np.argmin(abs(R-2.3))]), xytext=(2.9, -0.08),
            arrowprops=dict(arrowstyle="->"), fontsize=9)
ax.set_xlabel("H–H 距离 R（示意）"); ax.set_ylabel("相对能量（示意）"); ax.set_yticks([])
ax.legend(loc="lower right", fontsize=9); ax.set_title("H$_2$ 解离曲线示意：RHF 失败、UHF 能量对但有自旋污染")
fig.tight_layout(); fig.savefig(OUT / "fig_h2_dissoc.png", dpi=170); plt.close(fig)

# 4. SCF 循环流程图
fig, ax = plt.subplots(figsize=(6.6, 3.4)); ax.axis("off")
boxes = [(0.5, 0.85, "初猜 $C^{(0)}$（或密度 $P^{(0)}$）"), (0.5, 0.64, "用当前 P 构造 Fock 矩阵\nF = H_core + G(P)  ← J、K 积分"),
         (0.5, 0.42, "解 FC = SCε\n得到新的轨道 C 和 ε"), (0.5, 0.2, "按占据轨道算新密度 P\n比较 E、P 是否不再变化")]
for x, y, t in boxes:
    ax.text(x, y, t, ha="center", va="center", fontsize=10, bbox=dict(boxstyle="round", fc="#eef4fb", ec="#4a78b0"))
for (x1, y1, _), (x2, y2, _) in zip(boxes, boxes[1:]):
    ax.annotate("", xy=(x2, y2 + 0.07), xytext=(x1, y1 - 0.07), arrowprops=dict(arrowstyle="->"))
ax.annotate("", xy=(0.78, 0.64), xytext=(0.78, 0.2), arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.5", color="tab:red"))
ax.text(0.9, 0.42, "没收敛：\n回去重建 F", color="tab:red", fontsize=9, ha="center")
ax.text(0.5, 0.02, r"收敛 → 输出 $E_{HF}$、轨道能 $\varepsilon_i$、MO 系数", ha="center", fontsize=10, color="tab:green")
ax.set_title("SCF：Fock 算符依赖于它自己的解，所以只能迭代")
fig.tight_layout(); fig.savefig(OUT / "fig_scf_loop.png", dpi=170); plt.close(fig)
# 5. O2 的 π* 两电子：6 个行列式（微观状态）
fig, ax = plt.subplots(figsize=(7.2, 2.6)); ax.axis("off")
states = [("↑", "↑", "M=+1"), ("↓", "↓", "M=−1"), ("↑", "↓", "M=0 混合"), ("↓", "↑", "M=0 混合"),
          ("↑↓", "", "闭壳层"), ("", "↑↓", "闭壳层")]
for k, (a, b, lab) in enumerate(states):
    x0 = k * 1.2
    for j, e in enumerate((a, b)):
        ax.plot([x0 + j * 0.5, x0 + j * 0.5 + 0.4], [0.5, 0.5], "k", lw=2)
        ax.text(x0 + j * 0.5 + 0.2, 0.56, e, ha="center", va="bottom", fontsize=15)
    ax.text(x0 + 0.45, 0.22, lab, ha="center", fontsize=8.5)
ax.text(3.3, 1.12, r"$\pi^*_x$ 与 $\pi^*_y$ 简并，放 2 个电子：C(4,2) = 6 个 Slater 行列式", ha="center", fontsize=10)
ax.text(3.3, -0.12, r"→ 组合成 $^3\Sigma_g^-$（3 个，最低）+ $^1\Delta_g$（2 个，+0.98 eV）+ $^1\Sigma_g^+$（1 个，+1.63 eV）", ha="center", fontsize=9.5)
ax.set_xlim(-0.2, 7.2); ax.set_ylim(-0.25, 1.3)
fig.tight_layout(); fig.savefig(OUT / "fig_o2_microstates.png", dpi=170); plt.close(fig)

# 6. 占据轨道 vs 虚轨道：各自"看到"几个电子
fig, ax = plt.subplots(figsize=(6.6, 2.0)); ax.axis("off")
for x0, title, n_other, col in [(0.05, "占据轨道 i 上的电子", "看到其余 N−1 个电子\n（J_ii − K_ii = 0，自己不排斥自己）", "tab:blue"),
                                (0.55, "虚轨道 a 上（假想）的电子", "看到全部 N 个占据电子\n（它像是 N+1 电子体系里的那个额外电子）", "tab:red")]:
    ax.add_patch(plt.Rectangle((x0, 0.15), 0.4, 0.7, fill=False, ec=col, lw=1.5))
    ax.text(x0 + 0.2, 0.78, title, ha="center", fontsize=10, color=col)
    ax.text(x0 + 0.2, 0.45, n_other, ha="center", va="center", fontsize=9)
ax.text(0.5, 0.02, r"$\varepsilon_{\rm LUMO}-\varepsilon_{\rm HOMO}$ ≈ 电离能 − 电子亲和能（基本能隙），不是光学激发能", ha="center", fontsize=9.5)
fig.tight_layout(); fig.savefig(OUT / "fig_occ_virt.png", dpi=170); plt.close(fig)

# 7. H2 / D2：同一条势能曲线，不同的零点能
R = np.linspace(0.45, 3.0, 300)
V = 4.75 * (1 - np.exp(-1.94 * (R - 0.741))) ** 2 - 4.75
fig, ax = plt.subplots(figsize=(6.4, 3.6))
ax.plot(R, V, "k", lw=2, label="BO 势能曲线（H₂ 与 D₂ 完全相同）".replace("₂", "$_2$"))
for zpe, lab, c in [(0.27, "H$_2$ 零点能 ≈ 0.27 eV", "tab:red"), (0.19, "D$_2$ 零点能 ≈ 0.19 eV", "tab:blue")]:
    y = -4.75 + zpe
    xs = R[V <= y]
    ax.plot([xs.min(), xs.max()], [y, y], color=c, lw=2)
    ax.annotate(lab, xy=(xs.max(), y), xytext=(1.2, -4.45 if "H$" in lab else -4.85), color=c, fontsize=9,
                arrowprops=dict(arrowstyle="->", color=c))
ax.axhline(0, color="gray", lw=0.8)
ax.annotate("", xy=(2.4, -4.75), xytext=(2.4, 0), arrowprops=dict(arrowstyle="<->"))
ax.text(2.45, -2.4, "$D_e$ 相同", fontsize=9)
ax.set_xlabel("R / Å"); ax.set_ylabel("E / eV"); ax.set_ylim(-5.1, 0.6)
ax.set_title("同位素替换：势能面不变，零点能变 → $D_0$ 不同")
ax.legend(loc="upper left", fontsize=9)
fig.tight_layout(); fig.savefig(OUT / "fig_h2_d2_zpe.png", dpi=170); plt.close(fig)
print("ok")
