"""生成 Ex6 的 Word：HW2_Ex6_molecular_dynamics_water.docx（在 03_report_word/ 下）。

数字从 Ex6_water_MD/ex6_analysis/ 的分析结果和两个作业日志里现读；
图用 ex6_analysis/ 里已经生成好的三张 png。
用法：D:\\venvs\\cm5235_hw2\\Scripts\\python make_ex6_word.py
"""
import re
import sys

from report_common import (AS2, REPORT_DIR, exercise_title, figure, heading, new_document, para, para_lead,
                           save, table, table_caption)

EX6 = AS2 / "Ex6_water_MD"
ANA = EX6 / "ex6_analysis"
sys.path.insert(0, str(ANA))
from ex6_analyze_trajectories import DT, analyse  # noqa: E402

SIMS = ["6a_DFT_PBE", "6b_XTB"]
NICE = {"6a_DFT_PBE": "(a) PBE/def2-SVP", "6b_XTB": "(b) GFN2-xTB"}


def walltime_seconds(sim):
    log = (EX6 / sim / f"ex6_pbs_log_{sim}.txt").read_text(errors="replace")
    h, m, s = re.search(r"Walltime Used:\s+(\d+):(\d+):(\d+)", log).groups()
    return int(h) * 3600 + int(m) * 60 + int(s)


def main():
    R = {s: analyse(EX6, s) for s in SIMS}
    wt = {s: walltime_seconds(s) for s in SIMS}
    per_step = {s: wt[s] / (R[s]["nfr"] - 1) for s in SIMS}

    doc = new_document()
    exercise_title(doc, "Exercise 6 - Ab initio and semi-empirical molecular dynamics of a water cluster")
    para(doc, "Both runs use the ORCA %md module on a cluster cut from an ice crystal, at 400 K with a "
              "Nosé–Hoover chain thermostat (time constant 10 fs) and a time step of 0.5 fs, which is the "
              "largest step the manual recommends for systems containing hydrogen. The exercise asks for a "
              "sphere of size 50 Å; this was read as a diameter, so the ORCA keyword Cell Sphere was given a "
              "radius of 25 Å, centred on the cluster (the input files are not centred on the origin). The "
              "sphere is a soft repulsive wall that keeps evaporated molecules from flying away; the clusters "
              "themselves have radii of only 6.4 Å (a) and 13.7 Å (b), so the wall never acts on the bulk of "
              "the cluster, and the results would be the same if the 50 Å were read as a radius. "
              "Keywords: ! MD PBE def2-SVP def2/J for (a) and ! MD XTB2 for (b).")

    heading(doc, "Setup and cost")
    rows = [["", "(a) PBE/def2-SVP", "(b) GFN2-xTB"],
            ["Water molecules", f"{R['6a_DFT_PBE']['nwat']}", f"{R['6b_XTB']['nwat']}"],
            ["Atoms", f"{R['6a_DFT_PBE']['nwat'] * 3}", f"{R['6b_XTB']['nwat'] * 3}"],
            ["Steps × 0.5 fs", f"{R['6a_DFT_PBE']['nfr'] - 1} = "
                               f"{(R['6a_DFT_PBE']['nfr'] - 1) * DT:g} fs",
             f"{R['6b_XTB']['nfr'] - 1} = {(R['6b_XTB']['nfr'] - 1) * DT / 1000:g} ps"],
            ["Wall time (1 core)", f"{wt['6a_DFT_PBE'] / 3600:.1f} h", f"{wt['6b_XTB'] / 3600:.1f} h"],
            ["Time per step", f"{per_step['6a_DFT_PBE']:.0f} s", f"{per_step['6b_XTB']:.1f} s"],
            ["Time per step and atom", f"{per_step['6a_DFT_PBE'] / (R['6a_DFT_PBE']['nwat'] * 3) * 1000:.0f} ms",
             f"{per_step['6b_XTB'] / (R['6b_XTB']['nwat'] * 3) * 1000:.1f} ms"]]
    table_caption(doc, "Table 1. The two simulations and what they cost on one core.")
    table(doc, rows, [5.0, 4.6, 4.6])

    heading(doc, "Structures at the beginning and at the end")
    figure(doc, ANA / "ex6_fig_snapshots.png", 14.0,
           "Figure 1. First and last frame of each trajectory. Red: O, white: H, grey sticks: covalent O–H bonds, "
           "thin blue lines: hydrogen bonds (H···O < 2.2 Å). Same viewing direction and scale within each row.")

    heading(doc, "Temperature and structure along the trajectories")
    figure(doc, ANA / "ex6_fig_temperature_structure.png", 14.0,
           "Figure 2. Top: instantaneous temperature (dashed line: the 400 K set point). Middle: hydrogen bonds per "
           "water molecule (O···O < 3.5 Å and ∠(H–O···O) < 30°). Bottom: tetrahedral order parameter q averaged "
           "over the molecules that start with four neighbours within 3.2 Å (2 of 20 and 48 of 128). "
           "Thin lines are per-step values, thick lines a running average.")
    figure(doc, ANA / "ex6_fig_OO_distance_distribution.png", 14.0,
           "Figure 3. O–O pair distance distribution, n(r)/4πr², at the beginning and at the end of each run, "
           "scaled to the same maximum.")

    heading(doc, "What the simulations show")
    a, b = R["6a_DFT_PBE"], R["6b_XTB"]
    para_lead(doc, "The ice cluster melts, and the melting is visible in the structure, not in the temperature.",
              f"In the xTB run the tetrahedral order of the interior molecules falls from {b['q'][:b['k']].mean():.2f} "
              f"to {b['q'][-b['k']:].mean():.2f} during the first ~800 fs and then stays there; the second-neighbour "
              "peak at 4.4 Å in the O–O distribution disappears and the minimum at 3.5 Å fills in (Figure 3b). "
              "That is the crystal-to-liquid change the exercise describes: the molecules keep their hydrogen bonds "
              f"({b['hb'][:b['k']].mean():.2f} → {b['hb'][-b['k']:].mean():.2f} per molecule) but lose the "
              "tetrahedral arrangement and the long-range order.")
    para_lead(doc, "100 fs of ab initio MD is not enough to see it.",
              f"In the DFT run q only falls from {a['q'][:a['k']].mean():.2f} to {a['q'][-a['k']:].mean():.2f} and "
              "the pair distribution still shows the ice peaks. Hydrogen-bond rearrangement in water takes of the "
              "order of a picosecond, so a 100 fs trajectory only samples the vibrations around the initial "
              "structure.")
    para_lead(doc, "Molecules evaporate, and the wall is needed.",
              f"The largest O distance from the centre of the cluster grows from {b['rmax'][0]:.1f} Å to "
              f"{b['rmax'].max():.1f} Å in the xTB run: single molecules leave the hot surface and travel almost to "
              "the 25 Å wall. Without the confining sphere they would simply fly away and the cluster would "
              "slowly evaporate.")
    para_lead(doc, "The thermostat works, but small clusters fluctuate strongly.",
              f"Over the second half of the xTB run the mean temperature is {b['E'][len(b['E']) // 2:, 1].mean():.0f} K "
              f"with a standard deviation of {b['E'][len(b['E']) // 2:, 1].std():.0f} K. In the 60-atom DFT cluster "
              "the same thermostat gives swings of ±50 K around the set point, because the temperature of a small "
              "system is a strongly fluctuating quantity (the relative fluctuation goes as 1/√N).")
    para_lead(doc, "Cost decides what is possible.",
              f"One DFT step costs {per_step['6a_DFT_PBE']:.0f} s for 60 atoms, one xTB step {per_step['6b_XTB']:.1f} s "
              f"for 384 atoms, i.e. about {per_step['6a_DFT_PBE'] / (a['nwat'] * 3) / (per_step['6b_XTB'] / (b['nwat'] * 3)):.0f} "
              "times more expensive per atom and step. This is why the ab initio run is limited to a small cluster "
              "and 100 fs while the semi-empirical run reaches 128 molecules and 2.5 ps in a comparable wall time.")

    heading(doc, "What else can be obtained from the trajectories")
    para(doc, "The stored trajectory (and the per-step energies in the .csv file that ORCA writes) contains much "
              "more than the melting itself:")
    para_lead(doc, "Structure.",
              "Radial distribution functions g(r) for O–O, O–H and H–H and the coordination numbers obtained by "
              "integrating them; the distribution of hydrogen-bond distances and angles; the distribution of the "
              "tetrahedral order parameter; the size and shape of the cluster.")
    para_lead(doc, "Dynamics.",
              "Mean square displacement and from it the diffusion coefficient; hydrogen-bond lifetimes and "
              "reorientation correlation times; velocity autocorrelation, whose Fourier transform gives the "
              "vibrational density of states; the dipole autocorrelation function, which gives the infrared "
              "spectrum including anharmonic and temperature effects, something a harmonic frequency calculation "
              "like Exercise 1 cannot provide.")
    para_lead(doc, "Thermodynamics and quality control.",
              "The distributions of kinetic and potential energy (and from their fluctuations the heat capacity); "
              "the evaporation rate; and, as a check on the integration, the drift of the conserved quantity — here "
              f"{(b['E'][-1, 3] - b['E'][1, 3]) * 627.5095:+.1f} kcal mol^{{-1}} over 2.5 ps for xTB and "
              f"{(a['E'][-1, 3] - a['E'][1, 3]) * 627.5095:+.2f} kcal mol^{{-1}} over 100 fs for DFT.")
    para(doc, "Snapshots from the trajectory can also be used as starting structures for other calculations, for "
              "example to compute spectra of solvated molecules on configurations sampled by the dynamics.")
    para(doc, "The animation of the xTB trajectory (every 25th step, 201 frames) is supplied as "
              "ex6b_trajectory_animation_XTB.gif.")

    save(doc, REPORT_DIR / "HW2_Ex6_molecular_dynamics_water.docx")


if __name__ == "__main__":
    main()
