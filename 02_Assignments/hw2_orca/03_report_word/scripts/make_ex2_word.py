"""生成 Ex2 的 Word：HW2_Ex2_theory_solvent_effects.docx（在 03_report_word/ 下）。

理论题 1：Ex1 里的溶剂效应是怎么算进去的（CPCM 的原理），ORCA 里还有哪些溶剂模型。
引用的数字（ε、半径、表面点数、溶剂化能）都从 Ex1 两个水相输出里现读。
用法：D:\\venvs\\cm5235_hw2\\Scripts\\python make_ex2_word.py
"""
import re

from report_common import AS2, REPORT_DIR, exercise_title, heading, new_document, para, save

EX1 = AS2 / "Ex1_2Cl_phenol"
KCAL = 627.509474


def r2(s):
    """2.0400 -> 2.04，1.8240 -> 1.824"""
    return f"{float(s):.3f}".rstrip("0").rstrip(".")


def cpcm_info(method):
    out = (EX1 / method / f"ex1_optfreq_{method}.out").read_text(errors="replace")
    eps = float(re.search(r"Epsilon\s+\.\.\.\s+([\d.]+)", out).group(1))
    n = float(re.search(r"Refrac\s+\.\.\.\s+([\d.]+)", out).group(1))
    radii = dict(re.findall(r"Radius for (\w+)\s+used is\s+[\d.]+ Bohr \(=\s+([\d.]+) Ang", out))
    npts = int(re.findall(r"GEPOL surface points\s+\.\.\.\s+(\d+)", out)[-1])
    ediel = float(re.findall(r"CPCM Dielectric\s+:\s+(-?[\d.]+) Eh", out)[-1])
    return eps, n, radii, npts, ediel


def main():
    eps, n, radii, npts, e_b3 = cpcm_info("B3LYP_water")
    e_pbe = cpcm_info("PBE_water")[4]
    f_eps = (eps - 1) / eps

    doc = new_document()
    exercise_title(doc, "Exercise 2 - Theoretical question #1: solvent effects")

    heading(doc, "How the solvent was included in Exercise 1")
    para(doc, "The water calculations in Exercise 1 used the conductor-like polarizable continuum model, "
              "CPCM(Water). This is an implicit model: there are no water molecules in the calculation. Instead, "
              "the molecule is placed in a cavity inside a uniform dielectric that has the bulk properties of "
              f"water, ε = {eps:.1f} and refractive index n = {n:.2f}.")
    para(doc, "The cavity is built from overlapping spheres on the atoms. ORCA 5 takes 1.2 times the van der Waals "
              "radius of each element (C 1.70, H 1.10, O 1.52, Cl 1.75 Å), which gives "
              f"C {r2(radii['C'])}, H {r2(radii['H'])}, O {r2(radii['O'])} and Cl {r2(radii['Cl'])} Å for "
              f"2-chlorophenol. The cavity surface is divided into small elements, {npts} Lebedev points in this "
              "case, and each element carries one charge.")
    para(doc, "These surface charges q_{i} represent the polarisation of the solvent by the solute. If the "
              "surrounding medium were a perfect conductor (ε → ∞), the total electrostatic potential on the "
              "surface would be zero. Written for all surface points this gives the linear equations A q = −V, "
              "where V_{i} is the potential of the solute (electrons and nuclei) at point i and A contains the "
              "Coulomb interactions between the surface charges. Water is not a conductor, so the charges are "
              f"scaled by f(ε) = (ε − 1)/(ε + x): A q = −f(ε) V. CPCM uses x = 0 (f = {f_eps:.4f} for water), "
              "while the original COSMO model uses x = 0.5.")
    para(doc, "In ORCA 5 each surface charge is a small Gaussian rather than a point charge, "
              "A_{ii} = ζ_{i} (2/π)^{1/2}/F_{i} and A_{ij} = erf(ζ_{ij} r_{ij})/r_{ij}, where the switching "
              "function F_{i} gradually removes a charge when it moves into a neighbouring sphere. With point "
              "charges, surface points would appear and disappear as the atoms move and the energy would jump. "
              "The Gaussian charges keep the energy and its derivatives smooth, which is needed for the analytic "
              "gradients and Hessians used in the Opt and Freq runs.")
    para(doc, "The surface charges and the electron density depend on each other, so they are solved together in "
              "the SCF (self-consistent reaction field). In each iteration the potential of the charges, "
              "V_{solv}(r) = Σ_{i} q_{i}/|r − r_{i}|, is added to the one-electron part of the Kohn–Sham "
              "operator, the new density gives new charges, and this is repeated until both are converged. The "
              "quantity minimised is the free energy G = ⟨Ψ|Ĥ^{0}|Ψ⟩ + ½⟨Ψ|V̂|Ψ⟩, where the factor ½ accounts for "
              "the work needed to polarise the solvent. All properties in Exercise 1 (orbitals, charges, dipole "
              "moment, frequencies) therefore belong to the polarised molecule in solution, which explains the "
              "larger dipole moment and the larger O–H charge separation in water.")
    para(doc, "The “CPCM Dielectric” energy in the output is the electrostatic part of the solvation free "
              f"energy: {e_pbe:.5f} Eh ({e_pbe * KCAL:.2f} kcal mol^{{-1}}) with PBE and {e_b3:.5f} Eh "
              f"({e_b3 * KCAL:.2f} kcal mol^{{-1}}) with B3LYP. Plain CPCM in ORCA 5 does not include the "
              "non-electrostatic terms (cavity formation, dispersion and repulsion), as the output also states.")

    heading(doc, "Other ways to treat solvent effects in ORCA")
    para(doc, "SMD (Marenich, Cramer and Truhlar) uses the same CPCM electrostatics with its own atomic radii and "
              "adds a non-electrostatic term for cavitation, dispersion and solvent structure, calculated from "
              "atomic surface tensions and solvent parameters. It is fitted to experimental solvation free "
              "energies, so it is the better choice when ΔG_{solv} itself is needed (%cpcm smd true end in "
              "ORCA 5, ! SMD(solvent) in ORCA 6).")
    para(doc, "openCOSMO-RS (ORCA 6) starts from the screening charges of a conductor calculation and treats the "
              "contacts between surface segments of solute and solvent with statistical thermodynamics. It gives "
              "solvation free energies in pure solvents and mixtures, including their temperature dependence.")
    para(doc, "A continuum cannot describe specific interactions such as a hydrogen bond between a water molecule "
              "and the OH group of 2-chlorophenol. For this, a few explicit water molecules can be added around "
              "the solute, by hand or with the SOLVATOR tool in ORCA 6, and the whole cluster can then be placed "
              "in CPCM (cluster–continuum model).")
    para(doc, "For a larger explicit solvent shell, ORCA offers QM/MM, where the solute is treated quantum "
              "mechanically and the solvent with a force field. Molecular dynamics with explicit solvent, as in "
              "Exercise 6, samples many solvent configurations instead of a single averaged one.")

    save(doc, REPORT_DIR / "HW2_Ex2_theory_solvent_effects.docx")


if __name__ == "__main__":
    main()
