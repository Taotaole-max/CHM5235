"""生成 Ex3 的 Word：HW2_Ex3_theory_resolution_of_identity.docx（在 03_report_word/ 下）。

理论题 2：RI（密度拟合）的本质，以及加速从哪里来。
举例用的数字（基函数数、辅助基函数数）从 Ex1 的 B3LYP 气相输出里现读，积分个数按公式算。
用法：D:\\venvs\\cm5235_hw2\\Scripts\\python make_ex3_word.py
"""
import re

from report_common import AS2, REPORT_DIR, equation, exercise_title, heading, new_document, para, save

OUT = AS2 / "Ex1_2Cl_phenol" / "B3LYP_gas" / "ex1_optfreq_B3LYP_gas.out"


def sci(x):
    """8.13e8 -> '8.1 × 10^{8}'（用报告里的上标标记）"""
    m, e = f"{x:.1e}".split("e")
    return f"{m} × 10^{{{int(e)}}}"


def main():
    out = OUT.read_text(errors="replace")
    N = int(re.search(r"Number of basis functions\s+\.\.\.\s+(\d+)", out).group(1))
    Naux = int(re.search(r"# of basis functions in Aux-J\s+\.\.\.\s+(\d+)", out).group(1))
    n4 = N ** 4 / 8                       # 独立四中心积分（8 重置换对称）
    n3 = N * (N + 1) / 2 * Naux           # 三中心积分 (μν|P)
    gb4, mb3 = n4 * 8 / 1e9, n3 * 8 / 1e6

    doc = new_document()
    exercise_title(doc, "Exercise 3 - Theoretical question #2: the resolution of the identity (density fitting)")

    heading(doc, "The bottleneck")
    para(doc, "In HF and DFT the Coulomb and exchange matrices are built from four-centre two-electron integrals:")
    equation(doc, "J_{μν} = Σ_{λσ} P_{λσ} (μν|λσ),   K_{μν} = Σ_{λσ} P_{λσ} (μλ|νσ),   "
              "(μν|λσ) = ∫∫ φ_{μ}(1) φ_{ν}(1) r_{12}^{−1} φ_{λ}(2) φ_{σ}(2) dr_{1} dr_{2}.")
    para(doc, f"The number of these integrals grows as N^{{4}}, where N is the number of basis functions. For "
              f"2-chlorophenol with def2-TZVP (N = {N}, Exercise 1) there are about {sci(n4)} unique integrals, "
              f"roughly {gb4:.1f} GB, and they must be recalculated in every SCF iteration or read back from disk. "
              "Correlated methods such as MP2 and coupled cluster also have to transform them to the molecular "
              "orbital basis, which scales as N^{5}.")

    heading(doc, "The idea")
    para(doc, "A four-centre integral is the Coulomb repulsion between two charge distributions, the orbital "
              "products ρ_{μν}(r) = φ_{μ}(r) φ_{ν}(r) and ρ_{λσ}(r). In the resolution of the identity (RI), also "
              "called density fitting, each product is expanded in an auxiliary basis of atom-centred functions "
              "χ_{P}:")
    equation(doc, "ρ_{μν}(r) ≈ Σ_{P} c^{P}_{μν} χ_{P}(r).")
    para(doc, "The coefficients are found by minimising the Coulomb self-repulsion of the fitting error. This gives "
              "c_{μν} = V^{−1} (P|μν) with the Coulomb metric V_{PQ} = (P|Q), and the error in the energy is then "
              "only second order in the error of the fitted density. The four-index integral splits into three- "
              "and two-index integrals:")
    equation(doc, "(μν|λσ) ≈ Σ_{PQ} (μν|P) [V^{−1}]_{PQ} (Q|λσ).")
    para(doc, "This is the same as inserting an approximate identity operator, 1 ≈ Σ_{PQ} |P) [V^{−1}]_{PQ} (Q|, "
              "between the two charge distributions, which is where the name comes from. The accuracy depends on "
              "the auxiliary basis. ORCA has matched auxiliary sets for different purposes, for example def2/J for "
              "Coulomb, def2/JK for Coulomb and exchange, def2-TZVP/C for correlation and SARC/J for relativistic "
              "basis sets, and AutoAux can generate one automatically.")

    heading(doc, "Where the speed-up comes from")
    para(doc, "First, far fewer integrals are needed. Only three-centre (μν|P) and two-centre (P|Q) integrals "
              "appear, and the auxiliary basis is only 1.5–3 times larger than the orbital basis (def2/J: "
              f"N_{{aux}} = {Naux} for 2-chlorophenol). The number of integrals drops from about N^{{4}}/8 = "
              f"{sci(n4)} to N^{{2}}N_{{aux}}/2 = {sci(n3)}, around {n4 / n3:.0f} times fewer. At about {mb3:.0f} MB "
              "they fit in memory, so they do not have to be recalculated or read from disk.")
    para(doc, "Second, the Coulomb matrix is obtained in two cheap steps (RI-J). The density is fitted first, "
              "d = V^{−1} g with g_{Q} = Σ_{λσ} (Q|λσ) P_{λσ}, and then J_{μν} = Σ_{P} (μν|P) d_{P}. Both steps "
              "cost N^{2}N_{aux} instead of N^{4} and are dense matrix operations that run fast on modern "
              "processors. For a GGA functional like PBE, J is the only two-electron term, so RI-J removes the main "
              "bottleneck. The fitting error is small and systematic and largely cancels in energy differences.")
    para(doc, "The exchange matrix couples the indices crosswise and does not factorise as well. ORCA either fits "
              "it too (RIJK, with a /JK auxiliary basis) or uses RIJCOSX, which is RI for J and the "
              "chain-of-spheres method for K. In COSX one electron coordinate is integrated analytically and the "
              "other on a numerical grid, K_{μν} ≈ Σ_{g} w_{g} φ_{μ}(r_{g}) Σ_{λσ} A_{νλ}(r_{g}) P_{λσ} φ_{σ}(r_{g}) "
              "with A_{νλ}(r_{g}) = ∫ φ_{ν}(r) φ_{λ}(r) |r − r_{g}|^{−1} dr, and the cost grows almost linearly for "
              "large molecules. In Exercise 1 the PBE runs used RI-J (def2/J) and the B3LYP runs RIJCOSX (def2/J).")
    para(doc, "The same factorisation speeds up correlated methods. In RI-MP2 the MO integrals are written as "
              "(ia|jb) ≈ Σ_{P} B^{P}_{ia} B^{P}_{jb}, which avoids the expensive four-index transformation and "
              "makes the calculation an order of magnitude or more faster. ORCA's DLPNO methods are also built on "
              "it.")

    save(doc, REPORT_DIR / "HW2_Ex3_theory_resolution_of_identity.docx")


if __name__ == "__main__":
    main()
