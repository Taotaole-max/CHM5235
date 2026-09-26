"""生成 Ex2 的 Word：HW2_Ex2_theory_solvent_effects.docx（在 03_report_word/ 下）。

理论题 1：Ex1 里的溶剂效应是怎么算进去的（CPCM 的原理），ORCA 里还有哪些溶剂模型。
引用的数字（ε、半径、表面点数、溶剂化能）都从 Ex1 两个水相输出里现读。
用法：D:\\venvs\\cm5235_hw2\\Scripts\\python make_ex2_word.py
"""
import re

from report_common import AS2, REPORT_DIR, exercise_title, heading, new_document, para, para_lead, save

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
    para(doc, "The water calculations of Exercise 1 used the conductor-like polarizable continuum model, "
              "CPCM(Water). It is an implicit solvent model: no water molecules are present. The solvent is "
              f"replaced by a homogeneous, polarizable dielectric with the macroscopic constants of water, "
              f"ε = {eps:.1f} and refractive index n = {n:.2f}.")
    para_lead(doc, "Cavity.",
              "The molecule sits in a cavity of molecular shape built from overlapping atomic spheres. By "
              "default ORCA 5 uses a van der Waals type surface with sphere radii 1.2 times the atomic van der "
              "Waals radii (C 1.70, H 1.10, O 1.52, Cl 1.75 Å); for 2-chlorophenol this gives "
              f"C {r2(radii['C'])}, H {r2(radii['H'])}, O {r2(radii['O'])} and Cl {r2(radii['Cl'])} Å. "
              f"The surface is discretised on Lebedev points ({npts} points here), and each point carries one "
              "surface charge.")
    para_lead(doc, "Apparent surface charges.",
              "The charge distribution of the solute polarises the dielectric, and this polarisation is "
              "represented by charges q_{i} on the cavity surface. For a perfect conductor (ε → ∞) the total "
              "electrostatic potential on the surface must vanish, V(r_{i}) + Σ_{j} V_{q,j}(r_{i}) = 0, which in "
              "matrix form is A q = −V: V_{i} is the potential of the solute (electrons and nuclei) at point i and "
              "A is the Coulomb interaction matrix between the surface charges. For a real dielectric the "
              "conductor charges are scaled down, A q = −f(ε) V with f(ε) = (ε − 1)/(ε + x). CPCM uses x = 0, "
              f"so f = {f_eps:.4f} for water; x = 0.5 would give the COSMO variant.")
    para_lead(doc, "Gaussian charges.",
              "ORCA 5 smears each surface charge into a spherical Gaussian instead of using a point charge, so "
              "that A_{ii} = ζ_{i} (2/π)^{1/2}/F_{i} and A_{ij} = erf(ζ_{ij} r_{ij})/r_{ij}. The switching function F_{i} "
              "smoothly removes charges that move inside a neighbouring sphere. With point charges, surface "
              "points appear and disappear as the atoms move, and the energy jumps; with Gaussian charges the "
              "energy and its derivatives are continuous. This is what makes the analytic gradients and Hessians "
              "usable, and both were needed for the Opt and Freq runs in water.")
    para_lead(doc, "Self-consistent reaction field.",
              "The surface charges add a potential V_{solv}(r) = Σ_{i} q_{i}/|r − r_{i}| (with Gaussian smearing) to "
              "the one-electron part of the Kohn–Sham operator. The charges depend on the density and the "
              "density depends on the charges, so both are updated in every SCF iteration until they are "
              "converged together. The SCF minimises the free energy G = ⟨Ψ|Ĥ^{0}|Ψ⟩ + ½⟨Ψ|V̂|Ψ⟩; the factor ½ "
              "accounts for the work spent polarising the solvent. The orbitals, charges, dipole moment and "
              "frequencies of Exercise 1 are therefore those of the polarised, solvated molecule, which is why "
              "the dipole moment and the O–H charge separation increase in water.")
    para_lead(doc, "What the energy contains.",
              "The solvent term printed as \u201cCPCM Dielectric\u201d is the electrostatic part of the solvation "
              f"free energy: {e_pbe:.5f} Eh ({e_pbe * KCAL:.2f} kcal mol^{{-1}}) with PBE and {e_b3:.5f} Eh "
              f"({e_b3 * KCAL:.2f} kcal mol^{{-1}}) with B3LYP at the optimised structures. Plain CPCM in ORCA 5 "
              "does not add the non-electrostatic terms (cavity formation, dispersion, repulsion); the output "
              "states that the cavity-dispersion term is not included.")

    heading(doc, "Other ways to treat solvent effects in ORCA")
    para_lead(doc, "CPCM with the COSMO scaling.",
              "! CPCMC(solvent) keeps the same model but uses x = 0.5 in f(ε).")
    para_lead(doc, "SMD.",
              "The Solvation Model based on Density (Marenich, Cramer and Truhlar) uses the CPCM electrostatics "
              "with its own intrinsic radii and adds a non-electrostatic cavity–dispersion–solvent-structure "
              "(CDS) term, computed from atomic surface tensions and solvent descriptors (refractive index, "
              "hydrogen-bond acidity and basicity, surface tension, aromaticity, halogenicity). It is "
              "parameterised against experimental solvation free energies and is the usual choice when ΔG_{solv} "
              "itself is needed (%cpcm smd true end in ORCA 5, ! SMD(solvent) in ORCA 6).")
    para_lead(doc, "OpenCOSMO-RS (ORCA 6).",
              "Starts from the conductor-screening charges and adds a statistical-thermodynamics treatment of "
              "the interacting surface segments. It gives solvation free energies in pure solvents and mixtures "
              "and their temperature dependence.")
    para_lead(doc, "Implicit models for xTB.",
              "For semi-empirical GFN-xTB calculations ORCA passes the solvent to the xtb program: ALPB, "
              "ddCOSMO or CPCM-X.")
    para_lead(doc, "Explicit and mixed solvation.",
              "Specific solute–solvent interactions, such as a water molecule hydrogen-bonded to the OH group of "
              "2-chlorophenol, are not described by a continuum. They can be added as explicit solvent "
              "molecules, either placed by hand or automatically with the ORCA SOLVATOR (ORCA 6), and the "
              "solvated cluster can itself be embedded in CPCM (cluster–continuum model). Larger explicit "
              "solvent shells can be treated with QM/MM, using the ORCA MM module for the solvent, and molecular "
              "dynamics with explicit solvent (as in Exercise 6) samples the solvent configurations.")
    para_lead(doc, "Excited states.",
              "For TD-DFT, CPCM is applied in linear-response form; vertical excitations are normally computed "
              "with non-equilibrium solvation, in which only the electronic polarisation of the solvent "
              "(ε_{∞} = n^{2}) follows the fast change of the density.")

    save(doc, REPORT_DIR / "HW2_Ex2_theory_solvent_effects.docx")


if __name__ == "__main__":
    main()
