"""生成 Ex5 的 Word：HW2_Ex5_magnetic_exchange_BSDFT.docx（在 03_report_word/ 下）。

数字从三个（以及三个加密格点复核版）ORCA 输出里现读
（复用 Ex5_Cu2_BSDFT/ex5_analysis/ex5_extract_J.py）。复核版还没算完时自动跳过那一段。
用法：D:\\venvs\\cm5235_hw2\\Scripts\\python make_ex5_word.py
"""
import sys

from report_common import (AS2, REPORT_DIR, exercise_title, heading, new_document, para, save,
                           table, table_caption)

EX5 = AS2 / "Ex5_Cu2_BSDFT"
sys.path.insert(0, str(EX5 / "ex5_analysis"))
from ex5_extract_J import EXTRA, LABELS, METHODS, parse  # noqa: E402

HARTREE_CM = 219474.63


def _orders(big, small):
    """差几个数量级（四舍五入到整数），避免手写口径说错。"""
    import math
    return round(math.log10(big / small))


def main():
    R = {m: parse(m) for m in METHODS}
    V = {m: parse(m, verify=True) for m in METHODS}
    if any(r is None for r in R.values()):
        sys.exit("还没算完：" + str([m for m in METHODS if R[m] is None]))
    have_v = all(V[m] for m in METHODS)

    doc = new_document()
    exercise_title(doc, "Exercise 5 - Magnetic exchange coupling in a Cu(II) dimer from broken-symmetry DFT")
    para(doc, "The compound is a paddle-wheel dimer with four trifluoroacetate bridges between the two Cu(II) ions "
              "(Cu–Cu 2.73 Å) and an alkoxide-type O donor in each axial position; the total charge is −2 as "
              "given. Each Cu(II) is d^{9} with S = 1/2. Keywords: ! UKS B3LYP <basis> <auxiliary basis> RIJCOSX "
              "TightSCF SlowConv, with %scf BrokenSym 1,1 end and the coordinate line * xyzfile −2 3 (high-spin "
              "triplet). ORCA first converges the high-spin state (HS, both spins parallel), then flips the spin "
              "on one Cu and converges the broken-symmetry state (BS). The three runs differ only in the "
              "relativistic treatment: non-relativistic (def2-SVP, def2/J), DKH (DKH-def2-SVP, SARC/J) and ZORA "
              "(ZORA-def2-SVP, SARC/J). The assignment does not specify the non-relativistic level, so "
              "B3LYP/def2-SVP was used to keep the functional and basis-set size the same in all three.")

    heading(doc, "Results")
    rows = [["Run", "E(HS) / E_{h}", "E(BS) / E_{h}", "⟨S²⟩_{HS}", "⟨S²⟩_{BS}",
             "E(HS)−E(BS) / cm^{-1}", "J(1)", "J(2)", "J(3)"]]
    for m in METHODS:
        r = R[m]
        rows.append([LABELS[m], f"{r['e_hs']:.6f}", f"{r['e_bs']:.6f}", f"{r['s2_hs']:.4f}", f"{r['s2_bs']:.4f}",
                     f"{r['dE_cm']:+.1f}", f"{r['j1']:+.1f}", f"{r['j2']:+.1f}", f"{r['j3']:+.1f}"])
    table_caption(doc, "Table 1. Total energies of the high-spin and broken-symmetry states, ⟨S²⟩ values and "
                       "exchange coupling constants J in cm^{-1}. ORCA uses H = −2J S_{A}·S_{B}, so J < 0 means "
                       "antiferromagnetic coupling. J(1): Ginsberg–Noodleman, J(2): Bencini–Gatteschi, J(3): "
                       "Yamaguchi, J = (E_{BS} − E_{HS})/(⟨S²⟩_{HS} − ⟨S²⟩_{BS}).")
    table(doc, rows, [2.7, 2.3, 2.3, 1.4, 1.4, 1.9, 1.15, 1.15, 1.15])

    para(doc, "The broken-symmetry states are the intended ones. The Mulliken spin populations on the two Cu "
              f"atoms are {R['nonrelativistic']['spin_bs'][0]:+.2f} and {R['nonrelativistic']['spin_bs'][1]:+.2f} "
              f"(non-relativistic; {R['ZORA']['spin_bs'][0]:+.2f} / {R['ZORA']['spin_bs'][1]:+.2f} with ZORA), "
              "and ⟨S²⟩_{BS} ≈ 1.0 compared with ⟨S²⟩_{HS} ≈ 2.0, as expected for two localised S = 1/2 centres "
              "with opposite spins.")

    heading(doc, "What the table shows")
    dEh = max(abs(R[m]["dE_cm"]) for m in METHODS) / HARTREE_CM     # E(HS)−E(BS)，单位 Eh
    dE_nr = R["nonrelativistic"]["e_hs"] - R["DKH"]["e_hs"]
    dE_z = R["nonrelativistic"]["e_hs"] - R["ZORA"]["e_hs"]
    para(doc, f"The relativistic treatment lowers the total energy by {abs(dE_nr):.1f} E_{{h}} (DKH) and "
              f"{abs(dE_z):.1f} E_{{h}} (ZORA). Almost all of this comes from the contraction of the Cu 1s–2p core "
              "shells, which is the same in both spin states and cancels in E(HS) − E(BS). The absolute energies "
              "of different relativistic Hamiltonians cannot be compared with each other; only energy differences "
              "within one Hamiltonian are meaningful.")
    para(doc, f"J comes from a very small energy difference: E(HS) − E(BS) is only "
              f"{min(abs(R[m]['dE_cm']) for m in METHODS):.0f}–{max(abs(R[m]['dE_cm']) for m in METHODS):.0f} "
              f"cm^{{-1}}, about {max(abs(R[m]['dE_cm']) for m in METHODS) / HARTREE_CM * 1e6:.0f}×10^{{-6}} "
              f"E_{{h}}, which is {_orders(abs(R['nonrelativistic']['e_hs']), dEh):.0f} orders of magnitude smaller "
              f"than the total energy and {_orders(abs(dE_nr), dEh):.0f} orders smaller than the relativistic "
              "energy shift. J(1) and J(3) are nearly equal because ⟨S²⟩_{HS} − ⟨S²⟩_{BS} ≈ 1 here (weak "
              "coupling), and J(2) is half of J(1) by definition, so the formula used must always be stated.")

    j3 = {m: R[m]["j3"] for m in METHODS}
    para(doc, f"With the SVP basis sets, J(3) changes from {j3['nonrelativistic']:+.1f} cm^{{-1}} "
              f"(non-relativistic) to {j3['DKH']:+.1f} cm^{{-1}} (DKH) and {j3['ZORA']:+.1f} cm^{{-1}} (ZORA). "
              "These changes are negligible compared with the change in total energy, but they are as large as "
              "J itself and even change its sign, from weakly ferromagnetic to weakly antiferromagnetic. DKH and "
              f"ZORA also differ from each other by {abs(j3['ZORA'] - j3['DKH']):.0f} cm^{{-1}}."
              + (" Repeating the three runs with a finer grid (DefGrid3, VeryTightSCF) changed J(3) by less than "
                 f"{max(abs(V[m]['j3'] - R[m]['j3']) for m in METHODS):.1f} cm^{{-1}}, so these numbers are not "
                 "grid noise." if have_v else "")
              + " To see whether they are converged with respect to the basis set, the calculations were repeated "
                "with TZVP basis sets.")

    # ---------------------------------------------------------------- 基组（泛函只留一句）
    X = {k: parse(k) for k in EXTRA}
    tzk = ["TZVP_nonrel", "TZVP_DKH", "TZVP_ZORA"]
    tz_ok = all(X[k] for k in tzk)
    rel = None
    if tz_ok:
        rows = [["", "E(HS)−E(BS) / cm^{-1}", None, "J(3) / cm^{-1}", None],
                ["Treatment", "SVP", "TZVP", "SVP", "TZVP"]]
        for m, k, lab in [("nonrelativistic", "TZVP_nonrel", "Non-relativistic"),
                          ("DKH", "TZVP_DKH", "DKH"), ("ZORA", "TZVP_ZORA", "ZORA")]:
            rows.append([lab, f"{R[m]['dE_cm']:+.1f}", f"{X[k]['dE_cm']:+.2f}",
                         f"{R[m]['j3']:+.1f}", f"{X[k]['j3']:+.2f}"])
        table_caption(doc, "Table 2. B3LYP results with SVP-level (def2-SVP, DKH-def2-SVP, ZORA-def2-SVP) and "
                           "TZVP-level (def2-TZVP, DKH-def2-TZVP, ZORA-def2-TZVP) basis sets, same geometry and "
                           "BrokenSym setup.")
        table(doc, rows, [3.4, 2.8, 2.8, 2.4, 2.4], header_rows=2, merges=[(0, 1, 2), (0, 3, 4)])
        t3 = {k: X[k]["j3"] for k in tzk}
        rel = t3["TZVP_DKH"] - t3["TZVP_nonrel"]
        para(doc, f"With the larger basis all three calculations give antiferromagnetic coupling, J(3) = "
                  f"{t3['TZVP_nonrel']:+.1f} cm^{{-1}} (non-relativistic), {t3['TZVP_DKH']:+.2f} cm^{{-1}} (DKH) "
                  f"and {t3['TZVP_ZORA']:+.2f} cm^{{-1}} (ZORA). DKH and ZORA now agree to "
                  f"{abs(X['TZVP_DKH']['dE_cm'] - X['TZVP_ZORA']['dE_cm']):.3f} cm^{{-1}}, and the non-relativistic "
                  "value is already negative without relativity. The sign change and the DKH/ZORA difference seen "
                  "with SVP therefore come from the small basis set, not from relativity. With TZVP, scalar "
                  f"relativistic effects shift J by {rel:+.0f} cm^{{-1}} and make the antiferromagnetic coupling "
                  f"about {abs(rel / t3['TZVP_nonrel']) * 100:.0f} % stronger.")
        fx = {k: X[k]["j3"] for k in ["TPSSh", "PBE0"] if X.get(k)}
        if len(fx) == 2:
            para(doc, "For comparison, changing the functional at the non-relativistic SVP level changes J(3) much "
                      f"more: {fx['TPSSh']:+.0f} cm^{{-1}} with TPSSh (10% exact exchange), "
                      f"{R['nonrelativistic']['j3']:+.0f} cm^{{-1}} with B3LYP (20%) and {fx['PBE0']:+.0f} "
                      "cm^{-1} with PBE0 (25%).")

    heading(doc, "How important are the relativistic effects on J?")
    rel_txt = (f"about {abs(rel):.0f} cm^{{-1}}, or {abs(rel / t3['TZVP_nonrel']) * 100:.0f} % of |J|"
               if rel is not None else "a few tens of cm^{-1}")
    para(doc, "Relativity changes the total energy by tens of hartree, but this is core-electron stabilisation "
              "that is the same in the high-spin and broken-symmetry states and cancels in J. The effect that "
              "remains on J is " + rel_txt + ". For a 3d metal such as Cu this is small in absolute terms, but it "
              "is not negligible because J itself is a small energy. DKH and ZORA give the same J once the basis "
              "set is large enough, so the choice between them does not matter here. The table also shows that "
              "the SVP basis is too small to resolve the relativistic effect on such a small energy difference, "
              "and that the choice of functional affects J more than relativity does.")

    save(doc, REPORT_DIR / "HW2_Ex5_magnetic_exchange_BSDFT.docx")


if __name__ == "__main__":
    main()
