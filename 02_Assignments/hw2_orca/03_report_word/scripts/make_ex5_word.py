"""生成 Ex5 的 Word：HW2_Ex5_magnetic_exchange_BSDFT.docx（在 03_report_word/ 下）。

数字从三个（以及三个加密格点复核版）ORCA 输出里现读
（复用 Ex5_Cu2_BSDFT/ex5_analysis/ex5_extract_J.py）。复核版还没算完时自动跳过那一段。
用法：D:\\venvs\\cm5235_hw2\\Scripts\\python make_ex5_word.py
"""
import sys

from report_common import (AS2, REPORT_DIR, exercise_title, heading, new_document, para, para_lead, save,
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
    para(doc, "The compound is a paddle-wheel dimer: four trifluoroacetate bridges between the two Cu(II) ions "
              "(Cu–Cu 2.73 Å) and one alkoxide-type O donor on each axial position; total charge −2 as given. Each "
              "Cu(II) is d^{9} with S = 1/2. Keywords: ! UKS B3LYP <basis> <auxiliary basis> RIJCOSX TightSCF "
              "SlowConv with %scf BrokenSym 1,1 end and the coordinate line * xyzfile −2 3, i.e. the high-spin "
              "multiplicity. ORCA first converges the high-spin state (HS, both spins parallel), then flips the "
              "spin on one Cu and converges the broken-symmetry state (BS). The three runs differ only in the "
              "relativistic treatment: non-relativistic (def2-SVP, def2/J), DKH (DKH-def2-SVP, SARC/J) and ZORA "
              "(ZORA-def2-SVP, SARC/J); the functional and the basis-set size are the same in all three, so the "
              "table isolates the relativistic effect. The assignment does not prescribe the non-relativistic "
              "level, so B3LYP/def2-SVP was chosen to match the other two.")

    heading(doc, "Results")
    rows = [["Run", "E(HS) / E_{h}", "E(BS) / E_{h}", "⟨S²⟩_{HS}", "⟨S²⟩_{BS}",
             "E(HS)−E(BS) / cm^{-1}", "J(1)", "J(2)", "J(3)"]]
    for m in METHODS:
        r = R[m]
        rows.append([LABELS[m], f"{r['e_hs']:.6f}", f"{r['e_bs']:.6f}", f"{r['s2_hs']:.4f}", f"{r['s2_bs']:.4f}",
                     f"{r['dE_cm']:+.1f}", f"{r['j1']:+.1f}", f"{r['j2']:+.1f}", f"{r['j3']:+.1f}"])
    if have_v:
        for m in METHODS:
            r = V[m]
            rows.append([LABELS[m] + ", tight grid", f"{r['e_hs']:.6f}", f"{r['e_bs']:.6f}", f"{r['s2_hs']:.4f}",
                         f"{r['s2_bs']:.4f}", f"{r['dE_cm']:+.1f}", f"{r['j1']:+.1f}", f"{r['j2']:+.1f}",
                         f"{r['j3']:+.1f}"])
    table_caption(doc, "Table 1. Total energies of the high-spin and broken-symmetry states, their spin "
                       "expectation values and the exchange coupling constants in cm^{-1}. ORCA uses "
                       "H = −2J S_{A}·S_{B}, so J < 0 means antiferromagnetic coupling. J(1) is the "
                       "Ginsberg–Noodleman expression, J(2) the Bencini–Gatteschi one and J(3) the Yamaguchi "
                       "expression J = (E_{BS} − E_{HS})/(⟨S²⟩_{HS} − ⟨S²⟩_{BS})."
                       + (" The last three rows repeat the calculations with a finer integration grid "
                          "(DefGrid3) and VeryTightSCF." if have_v else ""))
    table(doc, rows, [2.7, 2.3, 2.3, 1.4, 1.4, 1.9, 1.15, 1.15, 1.15])

    para(doc, "The broken-symmetry states are the intended ones: the Mulliken spin populations on the two Cu "
              f"atoms are {R['nonrelativistic']['spin_bs'][0]:+.2f} and {R['nonrelativistic']['spin_bs'][1]:+.2f} "
              f"(non-relativistic; {R['ZORA']['spin_bs'][0]:+.2f} / {R['ZORA']['spin_bs'][1]:+.2f} with ZORA), "
              f"and ⟨S²⟩_{{BS}} ≈ 1.0 against ⟨S²⟩_{{HS}} ≈ 2.0, which is what two localised, antiparallel "
              "S = 1/2 centres give.")

    heading(doc, "What the table shows")
    dEh = max(abs(R[m]["dE_cm"]) for m in METHODS) / HARTREE_CM     # E(HS)−E(BS)，单位 Eh
    dE_nr = R["nonrelativistic"]["e_hs"] - R["DKH"]["e_hs"]
    dE_z = R["nonrelativistic"]["e_hs"] - R["ZORA"]["e_hs"]
    para_lead(doc, "The relativistic correction to the total energy is enormous, and irrelevant for J.",
              f"DKH lowers the total energy by {abs(dE_nr):.1f} E_{{h}} and ZORA by {abs(dE_z):.1f} E_{{h}} "
              f"({abs(dE_nr) * HARTREE_CM / 1e6:.1f} and {abs(dE_z) * HARTREE_CM / 1e6:.1f} million cm^{{-1}}). "
              "This is almost entirely the contraction and stabilisation of the Cu 1s–2p core shells, which is "
              "the same in both spin states and therefore cancels in E(HS) − E(BS). The two relativistic "
              "Hamiltonians are also not on the same absolute scale, so only differences within one Hamiltonian "
              "are meaningful.")
    para_lead(doc, "J itself comes from a tiny energy difference.",
              f"E(HS) − E(BS) is only {min(abs(R[m]['dE_cm']) for m in METHODS):.0f}–"
              f"{max(abs(R[m]['dE_cm']) for m in METHODS):.0f} cm^{{-1}}, i.e. about "
              f"{max(abs(R[m]['dE_cm']) for m in METHODS) / HARTREE_CM * 1e6:.0f}×10^{{-6}} E_{{h}}: "
              f"{_orders(abs(R['nonrelativistic']['e_hs']), dEh):.0f} orders of magnitude smaller than the total "
              f"energy and {_orders(abs(dE_nr), dEh):.0f} orders smaller than the relativistic correction.")
    para_lead(doc, "The three formulas differ by factors, not by physics.",
              "J(1) and J(3) agree closely because ⟨S²⟩_{HS} − ⟨S²⟩_{BS} ≈ 1 here, which is the weak-coupling "
              "limit that the Yamaguchi expression interpolates to; J(2) is smaller by a factor "
              "S_{max}(S_{max}+1)/S_{max}² = 2 by construction. Which one is quoted matters as much as the "
              "relativistic treatment, so the convention has to be stated.")

    j3 = {m: R[m]["j3"] for m in METHODS}
    para_lead(doc, "Relativistic effects on J with the prescribed SVP basis.",
              f"J(3) goes from {j3['nonrelativistic']:+.1f} cm^{{-1}} (non-relativistic) to "
              f"{j3['DKH']:+.1f} cm^{{-1}} (DKH) and {j3['ZORA']:+.1f} cm^{{-1}} (ZORA). The changes, "
              f"{j3['DKH'] - j3['nonrelativistic']:+.0f} and {j3['ZORA'] - j3['nonrelativistic']:+.0f} cm^{{-1}}, "
              "are tiny compared with the change of the total energy, but as large as J itself, and at this "
              "level they even change its sign (weakly ferromagnetic without, weakly antiferromagnetic with "
              "relativity). The two relativistic Hamiltonians also disagree with each other by "
              f"{abs(j3['ZORA'] - j3['DKH']):.0f} cm^{{-1}}. Because such small energy differences are easily "
              "distorted, the SVP results were checked for numerical and basis-set convergence below.")

    if have_v:
        dj = [V[m]["j3"] - R[m]["j3"] for m in METHODS]
        para_lead(doc, "Numerical check.",
                  "E(HS) − E(BS) is of the same order as the error of the chain-of-spheres approximation for the "
                  "exchange integrals, so all three calculations were repeated with a finer integration grid "
                  "(DefGrid3) and VeryTightSCF (last three rows of Table 1). J(3) changes by only "
                  + ", ".join(f"{d:+.2f}" for d in dj)
                  + f" cm^{{-1}}, less than {max(abs(d) for d in dj):.1f} cm^{{-1}}: the numbers are converged "
                    "with respect to the numerical integration.")

    # ---------------------------------------------------------------- 基组和泛函
    X = {k: parse(k) for k in EXTRA}
    fx = [k for k in ["TPSSh", "PBE0"] if X[k]]
    tzk = ["TZVP_nonrel", "TZVP_DKH", "TZVP_ZORA"]
    tz_ok = all(X[k] for k in tzk)
    if fx or tz_ok:
        heading(doc, "Are the SVP results converged? Basis set and functional")
        rows = [["Run", "E(HS)−E(BS) / cm^{-1}", "J(3) / cm^{-1}", "Coupling"]]
        order = []
        if tz_ok:
            order += [("nonrelativistic", "B3LYP/def2-SVP, non-relativistic"),
                      ("DKH", "B3LYP/DKH-def2-SVP, DKH"), ("ZORA", "B3LYP/ZORA-def2-SVP, ZORA")]
            order += [(k, EXTRA[k]) for k in tzk]
        if fx:
            order += [(k, EXTRA[k]) for k in ["TPSSh"] if X[k]]
            order += [("nonrelativistic", "B3LYP/def2-SVP, non-rel. (20% HF exchange)")]
            order += [(k, EXTRA[k]) for k in ["PBE0"] if X[k]]
        for k, lab in order:
            r = R[k] if k in R else X[k]
            rows.append([lab, f"{r['dE_cm']:+.2f}" if k in ("TZVP_DKH", "TZVP_ZORA") else f"{r['dE_cm']:+.1f}",
                         f"{r['j3']:+.2f}" if k in ("TZVP_DKH", "TZVP_ZORA") else f"{r['j3']:+.1f}",
                         "ferromagnetic" if r["j3"] > 0 else "antiferromagnetic"])
        table_caption(doc, "Table 2. Additional B3LYP calculations with the larger TZVP-level basis sets (upper "
                           "block, compared with the SVP results of Table 1) and non-relativistic SVP "
                           "calculations with functionals containing 10%, 20% and 25% exact exchange (lower "
                           "block). Same geometry, charge and BrokenSym setup throughout.")
        table(doc, rows, [6.6, 3.2, 2.2, 3.0])

        if tz_ok:
            t3 = {k: X[k]["j3"] for k in tzk}
            rel = t3["TZVP_DKH"] - t3["TZVP_nonrel"]
            para_lead(doc, "Basis set: the sign change is an SVP artefact.",
                      f"With TZVP-level basis sets all three calculations give antiferromagnetic coupling: "
                      f"J(3) = {t3['TZVP_nonrel']:+.1f} cm^{{-1}} non-relativistic, {t3['TZVP_DKH']:+.2f} "
                      f"cm^{{-1}} with DKH and {t3['TZVP_ZORA']:+.2f} cm^{{-1}} with ZORA. DKH and ZORA now agree "
                      f"to {abs(X['TZVP_DKH']['dE_cm'] - X['TZVP_ZORA']['dE_cm']):.3f} cm^{{-1}} in E(HS) − E(BS) "
                      f"(they differed by {abs(j3['ZORA'] - j3['DKH']):.0f} cm^{{-1}} with SVP), and the "
                      "non-relativistic value changes sign on its own when the basis is enlarged. The ferromagnetic "
                      "SVP result and the DKH/ZORA disagreement therefore come from the small SVP basis, not from "
                      "relativity. With the larger basis the relativistic correction is clean: scalar relativity "
                      f"shifts J by {rel:+.0f} cm^{{-1}}, i.e. it strengthens the antiferromagnetic coupling by "
                      f"about {abs(rel / t3['TZVP_nonrel']) * 100:.0f} %.")
        if fx:
            js = {k: X[k]["j3"] for k in ["TPSSh", "PBE0"] if X.get(k)}
            js["B3LYP"] = R["nonrelativistic"]["j3"]
            span = max(js.values()) - min(js.values())
            para_lead(doc, "Functional: the largest uncertainty.",
                      f"With the same SVP basis J(3) is {js['TPSSh']:+.0f} cm^{{-1}} for TPSSh (10% exact "
                      f"exchange), {js['B3LYP']:+.0f} cm^{{-1}} for B3LYP (20%) and {js['PBE0']:+.0f} cm^{{-1}} "
                      f"for PBE0 (25%), a monotonic trend with the amount of exact exchange spanning "
                      f"{span:.0f} cm^{{-1}}. This is the well-known functional dependence of broken-symmetry "
                      "DFT and is larger than any of the relativistic shifts.")

        heading(doc, "How important are the relativistic effects on J?")
        rel_txt = (f"about {abs(rel):.0f} cm^{{-1}} (≈{abs(rel / t3['TZVP_nonrel']) * 100:.0f} % of |J|)"
                   if tz_ok else "a few tens of cm^{-1}")
        para(doc, "The relativistic Hamiltonian changes the total energy by tens of hartree, but almost all of "
                  "that is the core-electron stabilisation, which is the same in the high-spin and the "
                  "broken-symmetry state and cancels in J. What remains for J is a correction of "
                  + rel_txt + ": for a 3d metal like Cu this is small in absolute terms but not negligible, "
                  "because the exchange coupling itself is a small energy. DKH and ZORA give the same answer "
                  "once the basis set is adequate, so for J the choice between the two scalar-relativistic "
                  "Hamiltonians does not matter. The comparison also shows that such small energy differences "
                  "need a converged basis set before a relativistic effect can be read from them — the SVP "
                  "basis prescribed for the exercise is too small for that — and that the exchange-correlation "
                  "functional, not relativity, is the main source of uncertainty in the computed J.")

    save(doc, REPORT_DIR / "HW2_Ex5_magnetic_exchange_BSDFT.docx")


if __name__ == "__main__":
    main()
