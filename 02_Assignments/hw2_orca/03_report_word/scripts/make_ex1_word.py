"""生成 Ex1 的 Word：HW2_Ex1_ground_state_2-chlorophenol.docx（在 03_report_word/ 下）。

所有数字都从四个 ORCA 输出里现读（复用 Ex1_2Cl_phenol/ex1_analysis/ex1_extract_results.py），不手抄；
图来自 Ex1_2Cl_phenol/ex1_figures/。缺哪张图，就在那个位置写一行 [MISSING FIGURE ...]。
用法：D:\\venvs\\cm5235_hw2\\Scripts\\python make_ex1_word.py
"""
import re
import sys
from pathlib import Path

import numpy as np

from report_common import (AS2, GIF_EX1_AVO12, GIF_EX1_ORCA12, REPORT_DIR, caption, exercise_title, figure,
                           heading, new_document, para, save, table, table_caption)

EX1 = AS2 / "Ex1_2Cl_phenol"
FIG = EX1 / "ex1_figures"
sys.path.insert(0, str(EX1 / "ex1_analysis"))
from ex1_extract_results import METHODS, atom_labels, parse  # noqa: E402

KCAL = 627.509474
COLS = ["PBE gas", "B3LYP gas", "PBE water", "B3LYP water"]


def esp_range_on_surface():
    """静电势在 0.001 a.u. 密度面上的最小/最大值：和 ex1_render_figures.py 同一套数据和做法。"""
    sys.path.insert(0, str(FIG))
    import pyvista as pv
    from ex1_render_figures import BOHR, read_cube
    dens, _, _ = read_cube(FIG / "cube_job" / "cube_files" / "ex1_cube_density_B3LYP_gas.cube")
    surf = dens.contour([0.001], scalars="v").smooth_taubin(n_iter=40, pass_band=0.05)
    box = np.loadtxt(FIG / "cube_job" / "ex1_esp_grid_box.txt")
    npts = box[:, 2].astype(int)
    v = np.loadtxt(FIG / "cube_job" / "cube_files" / "ex1_esp_values_on_grid_B3LYP_gas.txt", skiprows=1)[:, 3]
    esp = pv.ImageData(dimensions=npts, spacing=box[:, 1] * BOHR, origin=box[:, 0] * BOHR)
    esp.point_data["ESP"] = v.reshape(npts).flatten(order="F")
    vals = surf.sample(esp).point_data["ESP"]
    return float(vals.min()), float(vals.max())


AVO = None  # 见 avogadro_figure()


def _trim_white(path, pad=24):
    """Avogadro 导出的是整个视口，分子周围一大片白。把白边裁掉再放进报告，
    否则图在 Word 里被整体缩小、分子看不清。返回裁好的 PIL 图像。"""
    from PIL import Image, ImageChops
    im = Image.open(path)
    # Avogadro 导出的 PNG 背景是透明的（透明像素的 RGB 是黑的），直接 convert("RGB")
    # 会得到黑底。先压到白底上再处理。
    if im.mode in ("RGBA", "LA"):
        flat = Image.new("RGB", im.size, (255, 255, 255))
        flat.paste(im, mask=im.split()[-1])
        im = flat
    else:
        im = im.convert("RGB")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    # 容差：Avogadro 的白底有一点渐变，差值小于 8 视为白
    box = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 8 else 0).getbbox()
    if box is None:
        return im
    l, t, r, b = box
    return im.crop((max(l - pad, 0), max(t - pad, 0),
                    min(r + pad, im.width), min(b + pad, im.height)))


def avogadro_figure(kind):
    """优先用 Avogadro 的截图（题目要求这几张图用 Avogadro 画）；没有就退回 PyVista 渲染的版本。
    kind = "orbitals"：把 HOMO、LUMO 两张截图并排拼成一张；kind = "esp"：直接用那一张。
    两种情况都先裁掉 Avogadro 视口的白边。"""
    from PIL import Image
    shots = FIG / "avogadro_screenshots"
    if kind == "orbitals":
        h, l = shots / "ex1_avogadro_HOMO.png", shots / "ex1_avogadro_LUMO.png"
        if h.exists() and l.exists():
            from PIL import ImageDraw, ImageFont
            ims = [_trim_white(x) for x in (h, l)]
            H = max(i.height for i in ims)
            ims = [i.resize((round(i.width * H / i.height), H)) for i in ims]
            gap = round(H * 0.06)
            try:
                font = ImageFont.truetype("arial.ttf", round(H * 0.085))
            except OSError:
                font = ImageFont.load_default()
            band = round(H * 0.13)          # 顶上留一条写 HOMO / LUMO
            out = Image.new("RGB", (sum(i.width for i in ims) + gap, H + band), "white")
            draw = ImageDraw.Draw(out)
            x = 0
            for i, label in zip(ims, ("HOMO", "LUMO")):
                out.paste(i, (x, band))
                w = draw.textlength(label, font=font)
                draw.text((x + (i.width - w) / 2, round(band * 0.12)), label,
                          fill=(0, 0, 0), font=font)
                x += i.width + gap
            path = shots / "ex1_avogadro_HOMO_LUMO_combined.png"
            out.save(path)
            return path, True
        return FIG / "ex1_fig_HOMO_LUMO_B3LYP_gas.png", False
    p = shots / "ex1_avogadro_density_ESP.png"
    if p.exists():
        trimmed = shots / "ex1_avogadro_density_ESP_trimmed.png"
        _trim_white(p).save(trimmed)
        return trimmed, True
    return FIG / "ex1_fig_density_ESP_B3LYP_gas.png", False


def conformer_note():
    """cis / trans 对照：证明报告里用的 cis 确实是更低的构象（数字从两个输出里现读）。"""
    import re as _re
    out = EX1 / "trans_B3LYP_gas" / "ex1_optfreq_trans_B3LYP_gas.out"
    if not out.exists():
        return ""
    def vals(p):
        s = p.read_text(errors="replace")
        return (float(_re.findall(r"FINAL SINGLE POINT ENERGY\s+(-?[\d.]+)", s)[-1]),
                float(_re.search(r"Final Gibbs free energy\s+\.\.\.\s+(-?[\d.]+)", s).group(1)),
                "imaginary mode" in s)
    e_t, g_t, imag_t = vals(out)
    e_c, g_c, _ = vals(EX1 / "B3LYP_gas" / "ex1_optfreq_B3LYP_gas.out")
    if imag_t:
        return ""
    return (f" This conformer was chosen because it is {(e_t - e_c) * KCAL:.1f} kcal mol^{{-1}} "
            f"({(g_t - g_c) * KCAL:.1f} kcal mol^{{-1}} in G at 298 K) below the trans conformer, which is also a "
            "minimum (B3LYP/def2-TZVP, gas phase).")


def fig_or_note(doc, name, width, cap, trim=False):
    path = FIG / name
    if path.exists():
        if trim:   # PyVista 渲染的图四周白边很大，裁掉后另存一份再放进报告
            out = FIG / (path.stem + "_trimmed.png")
            _trim_white(path).save(out)
            path = out
        figure(doc, path, width, cap)
    else:
        para(doc, f"[MISSING FIGURE {name}]", bold=True)


def main():
    R = {m: parse(m) for m in METHODS}
    missing = [m for m in METHODS if R[m] is None]
    if missing:
        sys.exit(f"还没算完：{missing}")
    lab, order = atom_labels(R["B3LYP_gas"]["geom"])
    T = R["PBE_gas"]["T"]

    doc = new_document()
    exercise_title(doc, "Exercise 1 - Study of the ground state of 2-chlorophenol with different computational methods")
    para(doc, "ORCA 5.0.2, spin-unrestricted Kohn–Sham, def2-TZVP basis; geometry optimisation followed by an "
              "analytic frequency calculation: ! UKS <PBE | B3LYP> def2-TZVP def2/J TightSCF TightOpt Opt Freq, "
              "with RIJCOSX for B3LYP and CPCM(Water) for the two solvated runs.")
    para(doc, "In the supplied structure the hydroxyl hydrogen was perpendicular to the ring. Before optimisation "
              "it was rotated into the ring plane on the Cl side (cis conformer, intramolecular O–H···Cl contact); "
              "all other atoms were left as given. All four optimised structures have 33 real frequencies and no "
              "imaginary mode, so they are minima." + conformer_note())

    # ---------------------------------------------------------------- a) 电荷
    heading(doc, "a) Mulliken and Löwdin atomic charges")
    fig_or_note(doc, "ex1_fig_atom_numbering.png", 5.2,
                "Figure 1. Atom numbering used in Table 1. H(Cn) is the hydrogen bonded to Cn; H(O) is the "
                "hydroxyl hydrogen.")
    rows = [["", "Mulliken", None, None, None, "Löwdin", None, None, None],
            ["Atom"] + COLS + COLS]
    for a in order:
        rows.append([lab[a]] + [f"{R[m]['mulliken'][a]:+.4f}" for m in METHODS]
                    + [f"{R[m]['loewdin'][a]:+.4f}" for m in METHODS])
    table_caption(doc, "Table 1. Atomic charges (e), UKS/def2-TZVP.")
    table(doc, rows, [1.45] + [1.72] * 8, header_rows=2, merges=[(0, 1, 4), (0, 5, 8)])

    o = order[1]            # O
    h = [a for a in order if lab[a] == "H(O)"][0]
    mq = {m: R[m]["mulliken"] for m in METHODS}
    lw = {m: R[m]["loewdin"] for m in METHODS}
    cl = order[0]
    para(doc, "Water increases the charge separation in the hydroxyl group. The Mulliken charge on O goes from "
              f"{mq['PBE_gas'][o]:.3f} to {mq['PBE_water'][o]:.3f} (PBE) and from {mq['B3LYP_gas'][o]:.3f} to "
              f"{mq['B3LYP_water'][o]:.3f} (B3LYP), and the hydroxyl H goes from +{mq['PBE_gas'][h]:.3f} to "
              f"+{mq['PBE_water'][h]:.3f} and from +{mq['B3LYP_gas'][h]:.3f} to +{mq['B3LYP_water'][h]:.3f}. "
              "B3LYP puts more negative charge on O than PBE. The two partitioning schemes disagree most for the "
              f"heteroatoms: Löwdin gives Cl a positive charge (+{min(lw[m][cl] for m in METHODS):.2f} to "
              f"+{max(lw[m][cl] for m in METHODS):.2f}) and O a small positive one, where Mulliken gives negative "
              "values. Atomic charges are not observables, and the two schemes divide the overlap density "
              "differently, so only the trends within one scheme should be compared.")

    # ---------------------------------------------------------------- b) 频率
    heading(doc, "b) Vibrational frequencies")
    nm = len(R["PBE_gas"]["freqs"])
    rows = [["Mode"] + COLS]
    for k in range(6, nm):
        rows.append([str(k)] + [f"{R[m]['freqs'][k][1]:.1f}" for m in METHODS])
    table_caption(doc, "Table 2. Harmonic vibrational frequencies (cm^{-1}), ORCA mode numbering "
                       "(modes 0–5 are translations and rotations).")
    table(doc, rows, [1.6, 2.4, 2.4, 2.4, 2.4])
    f = {m: np.array([R[m]["freqs"][k][1] for k in range(6, nm)]) for m in METHODS}
    ratio = np.mean(f["B3LYP_gas"] / f["PBE_gas"] - 1) * 100
    oh = {m: f[m][-1] for m in METHODS}
    para(doc, f"B3LYP gives higher frequencies than PBE for nearly every mode (on average by {ratio:.1f} % in the "
              "gas phase). The largest difference is the O–H stretch (mode 38): "
              f"{oh['PBE_gas']:.0f} cm^{{-1}} with PBE and {oh['B3LYP_gas']:.0f} cm^{{-1}} with B3LYP. Water shifts "
              "most modes by only a few cm^{-1}; the O–H stretch is lowered by "
              f"{oh['PBE_gas'] - oh['PBE_water']:.0f} cm^{{-1}} (PBE) and "
              f"{oh['B3LYP_gas'] - oh['B3LYP_water']:.0f} cm^{{-1}} (B3LYP).")

    # ---------------------------------------------------------------- c)–e) 偶极矩、熵、能隙
    heading(doc, "c)–e) Electric dipole moment, entropy at room temperature and HOMO–LUMO gap")
    S = lambda m, part: R[m]["S_parts"][part] * KCAL * 1000 / T
    rows = [["Quantity"] + COLS,
            ["Dipole moment μ (D)"] + [f"{R[m]['dipole']:.3f}" for m in METHODS],
            ["S_{vib} (cal mol^{-1} K^{-1})"] + [f"{S(m, 'Vibrational'):.2f}" for m in METHODS],
            ["S_{rot} (cal mol^{-1} K^{-1})"] + [f"{S(m, 'Rotational'):.2f}" for m in METHODS],
            ["S_{trans} (cal mol^{-1} K^{-1})"] + [f"{S(m, 'Translational'):.2f}" for m in METHODS],
            ["S total (cal mol^{-1} K^{-1})"] + [f"{R[m]['TS'] * KCAL * 1000 / T:.2f}" for m in METHODS],
            ["T·S (kcal mol^{-1})"] + [f"{R[m]['TS'] * KCAL:.2f}" for m in METHODS],
            ["E_{HOMO} (eV)"] + [f"{R[m]['homo'][2]:.3f}" for m in METHODS],
            ["E_{LUMO} (eV)"] + [f"{R[m]['lumo'][2]:.3f}" for m in METHODS],
            ["HOMO–LUMO gap (eV)"] + [f"{R[m]['lumo'][2] - R[m]['homo'][2]:.3f}" for m in METHODS]]
    table_caption(doc, f"Table 3. Dipole moment, entropy at {T:.2f} K and frontier orbital energies. "
                       "S_{el} = 0 (closed-shell singlet); ORCA treats the low-frequency vibrations with "
                       "Grimme's quasi-RRHO model. HOMO = orbital 32, LUMO = orbital 33 (α and β identical).")
    table(doc, rows, [4.6, 2.3, 2.3, 2.3, 2.3])
    mu = {m: R[m]["dipole"] for m in METHODS}
    Stot = [R[m]["TS"] * KCAL * 1000 / T for m in METHODS]
    gap = {m: R[m]["lumo"][2] - R[m]["homo"][2] for m in METHODS}
    para(doc, f"The dipole moment grows from PBE to B3LYP and from gas to water ({mu['PBE_gas']:.2f} D for PBE in "
              f"the gas phase, {mu['B3LYP_water']:.2f} D for B3LYP in water): the continuum polarises the molecule. "
              f"The entropy is almost method-independent ({min(Stot):.1f}–{max(Stot):.1f} cal mol^{{-1}} K^{{-1}}); "
              "the translational and rotational parts depend only on mass and geometry, and only the vibrational "
              "part changes a little through the low-frequency modes. The HOMO–LUMO gap is "
              f"{gap['B3LYP_gas'] - gap['PBE_gas']:.1f} eV larger with the hybrid functional "
              f"({gap['B3LYP_gas']:.2f} vs {gap['PBE_gas']:.2f} eV in the gas phase), while water changes it by "
              + (f"only {abs(gap['PBE_water'] - gap['PBE_gas']):.2f} eV with both functionals."
                 if f"{abs(gap['PBE_water'] - gap['PBE_gas']):.2f}" == f"{abs(gap['B3LYP_water'] - gap['B3LYP_gas']):.2f}"
                 else f"only {abs(gap['PBE_water'] - gap['PBE_gas']):.2f} eV (PBE) and "
                      f"{abs(gap['B3LYP_water'] - gap['B3LYP_gas']):.2f} eV (B3LYP)."))

    # ---------------------------------------------------------------- 12 号模式（两种编号都给）
    heading(doc, "Normal mode 12")
    out = (EX1 / "B3LYP_gas" / "ex1_optfreq_B3LYP_gas.out").read_text()
    ir = out[out.rfind("IR SPECTRUM"):]

    def mode(idx):
        m = re.search(rf"^\s*{idx}:\s+([\d.]+)\s+[\d.]+\s+([\d.]+)", ir, re.M)
        return float(m.group(1)), float(m.group(2))

    f12, i12 = mode(12)
    f17, i17 = mode(17)
    para(doc, "ORCA numbers all 3N modes from 0, so modes 0–5 are translations and rotations and mode 12 is the "
              "seventh vibration. Avogadro and Chemcraft list only the 33 vibrations, starting from 1, so their "
              "twelfth entry is ORCA mode 17. Since the numbering in the question could mean either, both modes "
              "are shown.")
    rows = [["", "ORCA mode 12", "ORCA mode 17"],
            ["Position in the list", "12th of all modes (7th vibration)", "17th of all modes (12th vibration)"],
            ["Frequency (cm^{-1})"] + [f"{f12:.1f}", f"{f17:.1f}"],
            ["IR intensity (km mol^{-1})"] + [f"{i12:.1f}", f"{i17:.1f}"],
            ["PBE gas / B3LYP gas / PBE water / B3LYP water (cm^{-1})",
             " / ".join(f"{R[m]['freqs'][12][1]:.1f}" for m in METHODS),
             " / ".join(f"{R[m]['freqs'][17][1]:.1f}" for m in METHODS)]]
    table_caption(doc, "Table 4. The two modes that “mode 12” can refer to, B3LYP/def2-TZVP gas phase.")
    table(doc, rows, [5.6, 4.6, 4.6])
    fig_or_note(doc, "ex1_fig_mode12_displacements_B3LYP_gas.png", 4.6,
                f"Figure 2a. ORCA mode 12 (7th vibration), {f12:.1f} cm^{{-1}}, IR intensity {i12:.1f} km "
                "mol^{-1}: in-plane ring deformation coupled to C–O–H bending; the hydroxyl H moves most. "
                "Arrows show the atomic displacements.", trim=True)
    fig_or_note(doc, "ex1_mode12_filmstrip_B3LYP_gas.png", 14.0,
                "Figure 2b. ORCA mode 12 at four points of one vibrational period T. "
                "The animation is sent with this report as " + GIF_EX1_ORCA12 + ".")
    fig_or_note(doc, "ex1_fig_mode17_displacements_B3LYP_gas.png", 6.5,
                f"Figure 3. ORCA mode 17 (12th vibration in the Avogadro list), {f17:.1f} cm^{{-1}}, IR intensity "
                f"{i17:.1f} km mol^{{-1}}: out-of-plane bending of the ring C–H bonds. The animation is sent as "
                + GIF_EX1_AVO12 + ".", trim=True)
    para(doc, "The frames of both modes were generated with orca_pltvib and rendered with Python (PyVista), since the "
              "movie export of Avogadro does not work.")

    # ---------------------------------------------------------------- HOMO / LUMO
    heading(doc, "HOMO and LUMO (B3LYP/def2-TZVP, gas phase)")
    hb = R["B3LYP_gas"]
    path, is_avo = avogadro_figure("orbitals")
    figure(doc, path, 15.0,
           f"Figure 4. HOMO (orbital 32, {hb['homo'][2]:.2f} eV) and LUMO (orbital 33, {hb['lumo'][2]:.2f} eV), "
           "isovalue ±0.02 a.u.; the two colours are the two phases of the orbital. "
           + ("Plotted with Avogadro 2 directly from the ORCA wavefunction (Molden file); Avogadro numbers the "
              "same orbitals 33 and 34, because it counts from 1 and ORCA from 0."
              if is_avo else "Cube files from ORCA (%plots), rendered with PyVista."))
    para(doc, "Both frontier orbitals are π orbitals. The HOMO is a ring π orbital with one nodal plane across the "
              "ring and antibonding contributions from the p lone pairs of O and Cl. The LUMO is a ring π* orbital "
              "with a small Cl contribution and almost none on O. The HOMO→LUMO excitation is the main component "
              "of the lowest excited state in Exercise 4.")

    # ---------------------------------------------------------------- 密度 + 静电势
    heading(doc, "Electron density and electrostatic potential (B3LYP/def2-TZVP, gas phase)")
    esp_lo, esp_hi = esp_range_on_surface()
    path, is_avo = avogadro_figure("esp")
    figure(doc, path, 10.5,
           "Figure 5. Electron density isosurface (0.001 a.u.) coloured by the electrostatic potential: red = "
           "negative, blue = positive. "
           + ("Plotted with Avogadro 2 from the ORCA wavefunction (Molden file). The surface is the B3LYP "
              "density; the colours come from Avogadro's point-charge (EEM) potential."
              if is_avo else "Density from ORCA (%plots), potential from orca_vpot, rendered with PyVista."))
    para(doc, f"On the 0.001 a.u. density surface the potential calculated from the wavefunction with orca_vpot "
              f"ranges from {esp_lo:.3f} to +{esp_hi:.3f} a.u. The most negative region is the oxygen lone pair on "
              "the side away from Cl, and the π face of the ring is also negative. The most positive region is the "
              "hydroxyl hydrogen, which points towards Cl (intramolecular O–H···Cl contact); the ring hydrogens are "
              "moderately positive."
              + (" Because Avogadro's colouring uses atom-centred point charges, it misses the negative π region "
                 "above and below the ring, so the values above are taken from orca_vpot." if is_avo else ""))

    save(doc, REPORT_DIR / "HW2_Ex1_ground_state_2-chlorophenol.docx")


if __name__ == "__main__":
    main()
