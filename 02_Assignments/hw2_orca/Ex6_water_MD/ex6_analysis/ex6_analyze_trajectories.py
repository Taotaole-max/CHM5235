"""Ex6 轨迹分析：温度、氢键数、四面体序参数随时间的变化，以及 O–O 距离分布。

用法：D:\\venvs\\cm5235_hw2\\Scripts\\python ex6_analyze_trajectories.py [--root <Ex6_water_MD 目录>]
读取（每个模拟子文件夹）：
    <sim>/ex6?_trajectory_*.xyz                 轨迹，每步一帧（Å）
    <sim>/ex6?_md_*-md-ener.csv                 每步的温度、能量（作业结束后在 <sim>/orca_raw_files/ 里）
写出（本文件夹）：
    ex6_fig_temperature_structure.png           3 行 × 2 列：温度 / 每个水的氢键数 / 四面体序参数 q，左 (a) DFT，右 (b) XTB
    ex6_fig_OO_distance_distribution.png        开头 10 % 和最后 10 % 帧的 O–O 距离分布，左 (a) 右 (b)
    ex6_summary.md                              报告里要引用的数字

判据：
    氢键 O_d–H···O_a：d(O_d···O_a) < 3.5 Å 且 ∠(H–O_d···O_a) < 30°（常用几何判据）
    四面体序参数（Errington–Debenedetti）：q = 1 − 3/8 Σ_{j<k} (cos ψ_jk + 1/3)^2，
        取每个 O 最近的 4 个 O；理想四面体 q = 1，完全无序 q = 0，冰约 0.9，室温液态水约 0.6。
        团簇从冰里切出来，表面分子凑不齐 4 个邻居，q 天然就低，所以 ⟨q⟩ 只对"内部"分子平均：
        第 0 帧时 3.2 Å 内正好有 4 个 O 邻居的分子（20 水团簇 2 个，128 水团簇 48 个），之后一直跟踪这些分子。
"""
import argparse
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SIMS = {
    "6a_DFT_PBE": dict(traj="ex6a_trajectory_DFT_PBE.xyz", ener="ex6a_md_DFT_PBE-md-ener.csv",
                       title="(a) PBE/def2-SVP, 20 H$_2$O"),
    "6b_XTB": dict(traj="ex6b_trajectory_XTB.xyz", ener="ex6b_md_XTB-md-ener.csv",
                   title="(b) GFN2-xTB, 128 H$_2$O"),
}
DT = 0.5  # fs


def find(root, sim, name):
    for p in [root / sim / name, root / sim / "orca_raw_files" / name]:
        if p.exists():
            return p
    raise FileNotFoundError(f"{sim}/{name}")


def read_traj(path):
    lines = Path(path).read_text().splitlines()
    n = int(lines[0])
    nfr = len(lines) // (n + 2)
    sym = [lines[2 + i].split()[0] for i in range(n)]
    X = np.empty((nfr, n, 3))
    for f in range(nfr):
        blk = lines[f * (n + 2) + 2:f * (n + 2) + 2 + n]
        X[f] = [[float(v) for v in l.split()[1:4]] for l in blk]
    return np.array(sym), X


def read_ener(path):
    rows = []
    for l in Path(path).read_text().splitlines():
        if l.startswith("#") or not l.strip():
            continue
        p = [c.strip() for c in l.split(";")]
        rows.append([float(p[1]), float(p[4]), float(p[6]), float(p[8]) if p[8] else np.nan])
    return np.array(rows)   # t (fs), T (K), E_pot (Eh), conserved (Eh)


def frame_analysis(sym, x, interior):
    O = x[sym == "O"]; H = x[sym == "H"]
    dOO = np.linalg.norm(O[:, None] - O[None], axis=-1)
    np.fill_diagonal(dOO, np.inf)
    # 每个 H 归到最近的 O（供体）
    dHO = np.linalg.norm(H[:, None] - O[None], axis=-1)
    donor = dHO.argmin(1)
    # 氢键：供体 O_d、受体 O_a，O_d···O_a < 3.5 Å，∠(H–O_d···O_a) < 30°
    v_OH = H - O[donor]                                   # (nH,3)
    v_OO = O[None] - O[donor][:, None]                    # (nH,nO,3)
    dist = np.linalg.norm(v_OO, axis=-1)
    cos = np.einsum("hk,hak->ha", v_OH, v_OO) / (np.linalg.norm(v_OH, axis=1)[:, None] * np.where(dist > 0, dist, 1))
    ok = (dist < 3.5) & (dist > 0) & (cos > np.cos(np.radians(30)))
    nhb = ok.sum() / len(O)                               # 氢键总数 / N；每个氢键连着两个水分子，所以下面乘 2
    # 四面体序参数
    nn = np.argsort(dOO, axis=1)[:, :4]
    q = np.empty(len(O))
    for i in range(len(O)):
        u = O[nn[i]] - O[i]
        u /= np.linalg.norm(u, axis=1)[:, None]
        c = u @ u.T
        s = sum((c[j, k] + 1 / 3) ** 2 for j in range(3) for k in range(j + 1, 4))
        q[i] = 1 - 3 / 8 * s
    com = O.mean(0)
    rmax = np.linalg.norm(O - com, axis=1).max()
    return 2 * nhb, q[interior].mean(), dOO[np.triu_indices(len(O), 1)], rmax


def analyse(root, sim):
    sym, X = read_traj(find(root, sim, SIMS[sim]["traj"]))
    E = read_ener(find(root, sim, SIMS[sim]["ener"]))
    O0 = X[0][sym == "O"]
    d0 = np.linalg.norm(O0[:, None] - O0[None], axis=-1); np.fill_diagonal(d0, np.inf)
    interior = (d0 < 3.2).sum(1) == 4
    res = [frame_analysis(sym, x, interior) for x in X]
    t = np.arange(len(X)) * DT
    hb = np.array([r[0] for r in res]); q = np.array([r[1] for r in res]); rmax = np.array([r[3] for r in res])
    k = max(50, len(X) // 10)   # 统计窗口：至少 50 帧（25 fs），小团簇的分布才不至于太毛躁
    d_first = np.concatenate([r[2] for r in res[:k]]); d_last = np.concatenate([r[2] for r in res[-k:]])
    return dict(t=t, E=E, hb=hb, q=q, rmax=rmax, d_first=d_first, d_last=d_last, nfr=len(X),
                nwat=int((sym == "O").sum()), k=k, ninterior=int(interior.sum()))


def smooth(y, w):
    if w <= 1 or len(y) < w:
        return y
    return np.convolve(y, np.ones(w) / w, mode="valid")


def plot_time(R):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    blue, grey = "#2a78d6", "#8a8984"
    fig, ax = plt.subplots(3, 2, figsize=(7.2, 6.4), dpi=300, sharex="col")
    for c, sim in enumerate(SIMS):
        if sim not in R:
            continue
        r = R[sim]
        E = r["E"]
        ax[0, c].plot(E[:, 0], E[:, 1], color=blue, lw=1.0)
        ax[0, c].axhline(400, color=grey, lw=0.8, ls="--")
        ax[0, c].set_title(SIMS[sim]["title"], fontsize=9.5)
        w = max(1, r["nfr"] // 100)     # 长轨迹画滑动平均（细线是原始值）
        for row, y in [(1, r["hb"]), (2, r["q"])]:
            ax[row, c].plot(r["t"], y, color=blue, lw=0.6, alpha=0.35 if w > 1 else 1)
            if w > 1:
                ax[row, c].plot(r["t"][w // 2:w // 2 + len(smooth(y, w))], smooth(y, w), color=blue, lw=1.6)
        ax[2, c].set_xlabel("time (fs)")
    ax[0, 0].set_ylabel("T (K)")
    ax[1, 0].set_ylabel("H-bonds per\nH$_2$O")
    ax[2, 0].set_ylabel("tetrahedral\norder ⟨q⟩")
    for a in ax.flat:
        a.spines[["top", "right"]].set_visible(False)
        a.spines[["left", "bottom"]].set_color("#8a8984")
        a.tick_params(colors="#52514e", labelsize=8)
        a.grid(axis="y", color="#e6e5e0", lw=0.6); a.set_axisbelow(True)
    fig.align_ylabels(ax[:, 0])
    fig.tight_layout()
    p = HERE / "ex6_fig_temperature_structure.png"
    fig.savefig(p, bbox_inches="tight", facecolor="white"); plt.close(fig)
    print("写出", p.name)


def plot_dist(R):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(7.2, 2.8), dpi=300, sharey=True)
    bins = np.linspace(2.2, 7.0, 97)
    rc = 0.5 * (bins[1:] + bins[:-1])
    for c, sim in enumerate(SIMS):
        if sim not in R:
            continue
        r = R[sim]
        for d, col, lab in [(r["d_first"], "#2a78d6", f"first {r['k'] * DT:g} fs"),
                            (r["d_last"], "#eb6834", f"last {r['k'] * DT:g} fs")]:
            h, _ = np.histogram(d, bins=bins)
            g = h / (4 * np.pi * rc ** 2 * np.diff(bins))
            g /= g.max()
            ax[c].plot(rc, g, color=col, lw=1.6, label=lab)
        ax[c].set_title(SIMS[sim]["title"], fontsize=9.5)
        ax[c].set_xlabel("O–O distance (Å)")
        ax[c].legend(frameon=False, fontsize=8)
    ax[0].set_ylabel("O–O pair density\n(n(r)/4πr², scaled)")
    for a in ax:
        a.spines[["top", "right"]].set_visible(False)
        a.spines[["left", "bottom"]].set_color("#8a8984")
        a.tick_params(colors="#52514e", labelsize=8)
        a.grid(axis="y", color="#e6e5e0", lw=0.6); a.set_axisbelow(True)
    fig.tight_layout()
    p = HERE / "ex6_fig_OO_distance_distribution.png"
    fig.savefig(p, bbox_inches="tight", facecolor="white"); plt.close(fig)
    print("写出", p.name)


def summary(R):
    L = ["# Ex6 summary\n"]
    for sim, r in R.items():
        E = r["E"]; half = len(E) // 2
        cons = E[1:, 3]
        L += [f"## {sim}  ({r['nwat']} H2O, {r['nfr']} frames = {(r['nfr'] - 1) * DT:g} fs)",
              f"- T mean (2nd half) = {E[half:, 1].mean():.1f} K, std = {E[half:, 1].std():.1f} K",
              f"- conserved quantity drift = {(cons[-1] - cons[0]) * 627.5095:.3f} kcal/mol over the run",
              f"- H-bonds per H2O: start {r['hb'][:r['k']].mean():.2f} -> end {r['hb'][-r['k']:].mean():.2f}",
              f"- tetrahedral order <q> over {r['ninterior']} interior molecules: start {r['q'][:r['k']].mean():.3f} -> end {r['q'][-r['k']:].mean():.3f}",
              f"- largest O distance from cluster centre: start {r['rmax'][0]:.1f} A, max over run {r['rmax'].max():.1f} A",
              ""]
    (HERE / "ex6_summary.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(HERE.parent))
    a = ap.parse_args()
    root = Path(a.root)
    R = {}
    for sim in SIMS:
        try:
            R[sim] = analyse(root, sim)
        except FileNotFoundError as e:
            print("跳过", sim, "：没有", e)
    plot_time(R); plot_dist(R); summary(R)
