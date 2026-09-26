"""生成 Ex4 的 Word：HW2_Ex4_excited_states_UV.docx（在 03_report_word/ 下）。

数字从四个 TD-DFT 输出里现读（复用 Ex4_TDDFT/ex4_analysis/ex4_extract_and_plot_uv.py）；
UV 光谱图用同一个脚本画好的 ex4_fig_UV_spectra.png。
比较溶剂效应时按"主要跃迁"配对，而不是按态的编号：加了溶剂以后态的顺序会变。
用法：D:\\venvs\\cm5235_hw2\\Scripts\\python make_ex4_word.py
"""
import sys

from report_common import (AS2, REPORT_DIR, exercise_title, figure, heading, new_document, para, save,
                           table, table_caption)

EX4 = AS2 / "Ex4_TDDFT"
sys.path.insert(0, str(EX4 / "ex4_analysis"))
from ex4_extract_and_plot_uv import LABELS, METHODS, main_transitions, orb_name, parse  # noqa: E402


def key(st):
    """主要跃迁（权重最大的那一对轨道），用来在气相和水相之间配对同一个态。"""
    a, b, _ = st["tr"][0]
    return f"{orb_name(a)}→{orb_name(b)}"


def main():
    R = {m: parse(m) for m in METHODS}

    doc = new_document()
    exercise_title(doc, "Exercise 4 - Excited states and spectra")
    para(doc, "TD-DFT for the first five singlet excited states at the four optimised structures of Exercise 1, "
              "with the same functional, basis and solvent model as the optimisation: ! RKS <PBE | B3LYP> "
              "def2-TZVP def2/J TightSCF (RIJCOSX for B3LYP, CPCM(Water) for the solvated runs) and %tddft "
              "NRoots 5  TDA false end, i.e. full linear-response TD-DFT rather than the Tamm–Dancoff "
              "approximation. The ground state is closed-shell, so a restricted reference was used; it gives the "
              "same ground state as the unrestricted one of Exercise 1 but pure singlet excited states.")

    # ---------------------------------------------------------------- 总表
    heading(doc, "Excitation energies of the first five excited states")
    rows = [["Method", "State", "E (eV)", "λ (nm)", "f", "Main transitions (weight)"]]
    for m in METHODS:
        for k, s in enumerate(R[m]):
            rows.append([LABELS[m] if k == 0 else "", f"S_{{{s['n']}}}", f"{s['eV']:.3f}", f"{s['nm']:.1f}",
                         f"{s['f']:.4f}", main_transitions(s)])
    table_caption(doc, "Table 1. TD-DFT/def2-TZVP singlet excitations: energy E, wavelength λ, oscillator strength "
                       "f and the orbital transitions with weight ≥ 0.15 (HOMO = orbital 32, LUMO = orbital 33).")
    t = table(doc, rows, [2.2, 1.1, 1.5, 1.5, 1.5, 7.2])
    for r in t.rows[1:]:                 # 最后一列（跃迁）左对齐更好读
        r.cells[5].paragraphs[0].alignment = 0

    # ---------------------------------------------------------------- 溶剂效应
    heading(doc, "Influence of the solvent")
    rows = [["Main transition", "PBE gas", "PBE water", "ΔE", "B3LYP gas", "B3LYP water", "ΔE"]]
    shifts = {"PBE": {}, "B3LYP": {}}
    keys = []
    for m in METHODS:
        for s in R[m]:
            if key(s) not in keys:
                keys.append(key(s))
    for kk in keys:
        row = [kk]
        for fx in ["PBE", "B3LYP"]:
            g = next((s for s in R[f"{fx}_gas"] if key(s) == kk), None)
            w = next((s for s in R[f"{fx}_water"] if key(s) == kk), None)
            row += [f"{g['eV']:.3f} (S_{{{g['n']}}})" if g else "–", f"{w['eV']:.3f} (S_{{{w['n']}}})" if w else "–"]
            if g and w:
                shifts[fx][kk] = w["eV"] - g["eV"]
                row.append(f"{w['eV'] - g['eV']:+.3f}")
            else:
                row.append("–")
        rows.append(row)
    table_caption(doc, "Table 2. Excitation energies (eV) in the gas phase and in water, matched by their main "
                       "transition (the state number is given in brackets, because the order changes), and the "
                       "solvent shift ΔE = E(water) − E(gas). \u201c–\u201d: not among the first five states.")
    table(doc, rows, [3.0, 2.1, 2.1, 1.4, 2.1, 2.1, 1.4])

    s1 = {m: R[m][0] for m in METHODS}
    allshift = [abs(v) for d in shifts.values() for v in d.values()]
    para(doc, "Water changes the excitation energies only slightly: by at most "
              f"{max(allshift):.2f} eV for the states that appear in both phases. The lowest state, S_{{1}}, is "
              "the HOMO→LUMO excitation for all four methods and moves by only "
              f"{s1['PBE_water']['eV'] - s1['PBE_gas']['eV']:+.3f} eV with PBE and "
              f"{s1['B3LYP_water']['eV'] - s1['B3LYP_gas']['eV']:+.3f} eV with B3LYP "
              f"({s1['PBE_gas']['nm']:.1f} → {s1['PBE_water']['nm']:.1f} nm and "
              f"{s1['B3LYP_gas']['nm']:.1f} → {s1['B3LYP_water']['nm']:.1f} nm). The states dominated by the "
              "HOMO→LUMO+1 and HOMO−1→LUMO configurations are lowered by water, whereas the two states that "
              "excite into LUMO+2 are raised by 0.06–0.09 eV, so S_{2} and S_{3} swap order for B3LYP. The effect on the "
              "intensities is larger than on the energies: the oscillator strength of S_{1} grows from "
              f"{s1['PBE_gas']['f']:.3f} to {s1['PBE_water']['f']:.3f} (PBE) and from {s1['B3LYP_gas']['f']:.3f} "
              f"to {s1['B3LYP_water']['f']:.3f} (B3LYP). The choice of functional matters much more than the "
              "solvent: B3LYP places every state 0.3–0.5 eV above PBE.")

    # ---------------------------------------------------------------- UV 谱
    heading(doc, "UV spectra")
    figure(doc, EX4 / "ex4_analysis" / "ex4_fig_UV_spectra.png", 13.5,
           "Figure 1. Simulated UV spectra of 2-chlorophenol. Top: each transition broadened by a Gaussian of FWHM "
           "3000 cm^{-1} (≈0.37 eV) in wavenumber, ε = Σ 2.174×10^{8} f_{i}/FWHM · exp[−2.773 (ν̃ − ν̃_{i})^{2}/FWHM^{2}]. "
           "Bottom: oscillator strengths (filled: gas, open: water; gas and water sticks are offset by ±0.6 nm "
           "for visibility). Only five states were computed, so the spectra are incomplete below about 200 nm.")

    save(doc, REPORT_DIR / "HW2_Ex4_excited_states_UV.docx")


if __name__ == "__main__":
    main()
