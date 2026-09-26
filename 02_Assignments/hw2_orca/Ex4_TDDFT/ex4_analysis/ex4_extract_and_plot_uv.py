"""Ex4 结果提取 + UV 光谱图。

用法：D:\\venvs\\cm5235_hw2\\Scripts\\python ex4_extract_and_plot_uv.py
读取：../<方法>/ex4_tddft_<方法>.out
写出（本文件夹）：
    ex4_excited_states_table.md   5 个激发态的能量、波长、振子强度、主要跃迁（给人看的核对表）
    ex4_fig_UV_spectra.png        UV 光谱：上栏高斯展宽后的摩尔吸光系数，下栏振子强度竖线
报告脚本 03_report_word/scripts/make_ex4_word.py 直接 import 这里的 parse()。

展宽：每个跃迁在波数上取高斯线形，半高宽 FWHM = 3000 cm^-1（约 0.37 eV），
ε(ν̃) = Σ 2.174e8 · f_i / FWHM · exp(-2.773 · ((ν̃ - ν̃_i)/FWHM)^2)   [L mol^-1 cm^-1]
（和 GaussSum 等常用程序同一个公式）。
"""
import re
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
EX4 = HERE.parent
METHODS = ["PBE_gas", "B3LYP_gas", "PBE_water", "B3LYP_water"]
LABELS = {"PBE_gas": "PBE (gas)", "B3LYP_gas": "B3LYP (gas)",
          "PBE_water": "PBE (water)", "B3LYP_water": "B3LYP (water)"}
HOMO = 32          # 2-氯苯酚 66 个电子，HOMO = 32 号，LUMO = 33 号（ORCA 从 0 编号）
FWHM = 3000.0      # cm^-1


def orb_name(i):
    d = i - HOMO
    if d <= 0:
        return "HOMO" if d == 0 else f"HOMO−{-d}"
    d -= 1
    return "LUMO" if d == 0 else f"LUMO+{d}"


def parse(method):
    out = (EX4 / method / f"ex4_tddft_{method}.out").read_text(errors="replace")
    blk = out[out.rfind("EXCITED STATES (SINGLETS)"):]
    blk = blk[:blk.find("EXCITATION SPECTRA") if "EXCITATION SPECTRA" in blk else None]
    states = []
    for m in re.finditer(r"STATE\s+(\d+):\s+E=\s+([\d.]+) au\s+([\d.]+) eV\s+([\d.]+) cm\*\*-1(.*?)(?=STATE\s+\d+:|\Z)",
                         blk, re.S):
        tr = [(int(a), int(b), float(w)) for a, b, w in
              re.findall(r"(\d+)a\s+->\s+(\d+)a\s+:\s+([\d.]+)", m.group(5))]
        tr.sort(key=lambda t: -t[2])
        states.append(dict(n=int(m.group(1)), eV=float(m.group(3)), cm=float(m.group(4)), tr=tr))
    # 只读"电偶极"吸收表这一张：从它的表头到下一张表（速度规范 / CD）之前。
    # 后面几张表的行格式一样，不截断就会被它们的数覆盖。
    i = out.find("ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS")
    j = out.find("ABSORPTION SPECTRUM VIA TRANSITION VELOCITY DIPOLE MOMENTS", i)
    ab = out[i:j if j > 0 else i + 3000]
    for m in re.finditer(r"^\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s", ab, re.M):
        n = int(m.group(1))
        if n <= len(states):
            states[n - 1]["nm"] = float(m.group(3))
            states[n - 1]["f"] = float(m.group(4))
    return states


def main_transitions(st, cutoff=0.15):
    return ", ".join(f"{orb_name(a)}→{orb_name(b)} ({w:.2f})" for a, b, w in st["tr"] if w >= cutoff)


def spectrum(states, nm_grid):
    nu = 1e7 / nm_grid
    eps = np.zeros_like(nu)
    for s in states:
        eps += 2.174e8 * s["f"] / FWHM * np.exp(-2.773 * ((nu - s["cm"]) / FWHM) ** 2)
    return eps


def plot(res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    color = {"PBE": "#2a78d6", "B3LYP": "#eb6834"}          # dataviz 参考色板第 1、2 槽，已校验
    style = {"gas": "-", "water": "--"}
    nm = np.linspace(170, 320, 1500)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.4, 5.6), dpi=300, sharex=True,
                                 gridspec_kw=dict(height_ratios=[2.2, 1], hspace=0.08))
    for m in METHODS:
        fx, env = m.split("_")
        a1.plot(nm, spectrum(res[m], nm) / 1e4, color=color[fx], ls=style[env], lw=1.8, label=LABELS[m])
        x = [s["nm"] for s in res[m]]; f = [s["f"] for s in res[m]]
        off = {"gas": -0.6, "water": 0.6}[env]                 # 气相、水相的竖线左右错开一点，免得重叠
        a2.vlines(np.array(x) + off, 0, f, color=color[fx], ls=style[env], lw=1.4)
        a2.plot(np.array(x) + off, f, "o", ms=4.5, color=color[fx],
                mfc=color[fx] if env == "gas" else "white", mew=1.2)
    a1.set_ylabel("ε  (10$^4$ L mol$^{-1}$ cm$^{-1}$)")
    a1.legend(frameon=False, fontsize=8.5, loc="upper right")
    a2.set_ylabel("oscillator\nstrength f")
    a2.set_xlabel("wavelength (nm)")
    a2.set_xlim(170, 320)
    a2.set_ylim(0, None)
    for a in (a1, a2):
        a.spines[["top", "right"]].set_visible(False)
        a.spines[["left", "bottom"]].set_color("#8a8984")
        a.tick_params(colors="#52514e", labelsize=8.5)
        a.grid(axis="y", color="#e6e5e0", lw=0.6)
        a.set_axisbelow(True)
    a1.set_ylim(0, None)
    path = HERE / "ex4_fig_UV_spectra.png"
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("写出", path.name)


def main():
    res = {m: parse(m) for m in METHODS}
    L = ["# Ex4 TD-DFT, first 5 singlet excited states (def2-TZVP, Ex1 geometries)\n"]
    for m in METHODS:
        L += [f"## {LABELS[m]}\n", "| State | E (eV) | λ (nm) | f | main transitions (weight) |", "|---|---|---|---|---|"]
        for s in res[m]:
            L.append(f"| {s['n']} | {s['eV']:.3f} | {s['nm']:.1f} | {s['f']:.4f} | {main_transitions(s)} |")
        L.append("")
    (HERE / "ex4_excited_states_table.md").write_text("\n".join(L), encoding="utf-8")
    print("写出 ex4_excited_states_table.md")
    plot(res)


if __name__ == "__main__":
    main()
