"""生成 Ex6 的 Word：HW2_Ex6_molecular_dynamics_water.docx（在 03_report_word/ 下）。

数字从 Ex6_water_MD/ex6_analysis/ 的分析结果和两个作业日志里现读；
图用 ex6_analysis/ 里已经生成好的三张 png。
用法：D:\\venvs\\cm5235_hw2\\Scripts\\python make_ex6_word.py
"""
import re
import sys

from report_common import (AS2, GIF_EX6, REPORT_DIR, exercise_title, figure, heading, new_document, para,
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
              "Nosé–Hoover chain thermostat (time constant 10 fs) and a time step of 0.5 fs, the largest step the "
              "manual recommends for systems with hydrogen atoms. The 50 Å sphere was taken as the diameter, so "
              "Cell Sphere was set to a radius of 25 Å, centred on the cluster because the input coordinates are "
              "not centred on the origin. The sphere is a soft repulsive wall that stops evaporated molecules "
              "from flying away. The clusters themselves have radii of only 6.4 Å (a) and 13.7 Å (b), so the wall "
              "does not affect the cluster itself and a 50 Å radius would give the same result. "
              "Keywords: ! MD PBE def2-SVP def2/J for (a) and ! MD XTB2 for (b).")

    heading(doc, "Setup")
    rows = [["", "(a) PBE/def2-SVP", "(b) GFN2-xTB"],
            ["Water molecules", f"{R['6a_DFT_PBE']['nwat']}", f"{R['6b_XTB']['nwat']}"],
            ["Atoms", f"{R['6a_DFT_PBE']['nwat'] * 3}", f"{R['6b_XTB']['nwat'] * 3}"],
            ["Steps × 0.5 fs", f"{R['6a_DFT_PBE']['nfr'] - 1} = "
                               f"{(R['6a_DFT_PBE']['nfr'] - 1) * DT:g} fs",
             f"{R['6b_XTB']['nfr'] - 1} = {(R['6b_XTB']['nfr'] - 1) * DT / 1000:g} ps"],
            ["Wall time (1 core)", f"{wt['6a_DFT_PBE'] / 3600:.1f} h", f"{wt['6b_XTB'] / 3600:.1f} h"],
            ["Time per step", f"{per_step['6a_DFT_PBE']:.0f} s", f"{per_step['6b_XTB']:.1f} s"]]
    table_caption(doc, "Table 1. The two simulations.")
    table(doc, rows, [5.0, 4.6, 4.6])

    heading(doc, "Trajectory in Avogadro")
    avo = EX6 / "ex6_avogadro_animation" / "ex6b_trajectory_filmstrip_from_avogadro.png"
    figure(doc, avo, 12.5,
           "Figure 1. The xTB trajectory (b) opened in Avogadro 2, frames at 500 fs intervals. Red: O, white: H. "
           "Because the movie export of Avogadro does not work, the trajectory was displayed frame by frame in "
           "Avogadro (every 100th MD step, 51 frames) and the rendered frames were joined into an animated GIF, "
           "which is sent with this report as " + GIF_EX6 + ".")

    heading(doc, "Structures at the beginning and at the end")
    figure(doc, ANA / "ex6_fig_snapshots.png", 14.0,
           "Figure 2. First and last frame of each trajectory. Red: O, white: H, grey sticks: covalent O–H bonds, "
           "thin blue lines: hydrogen bonds (H···O < 2.2 Å). Same viewing direction and scale within each row.")

    heading(doc, "Temperature and structure along the trajectories")
    figure(doc, ANA / "ex6_fig_temperature_structure.png", 14.0,
           "Figure 3. Top: instantaneous temperature (dashed line: the 400 K set point). Middle: hydrogen bonds per "
           "water molecule (O···O < 3.5 Å and ∠(H–O···O) < 30°). Bottom: tetrahedral order parameter q averaged "
           "over the molecules that start with four neighbours within 3.2 Å (2 of 20 and 48 of 128). "
           "Thin lines are per-step values, thick lines a running average.")
    figure(doc, ANA / "ex6_fig_OO_distance_distribution.png", 14.0,
           "Figure 4. O–O pair distance distribution, n(r)/4πr², at the beginning and at the end of each run, "
           "scaled to the same maximum.")

    heading(doc, "What the simulations show")
    a, b = R["6a_DFT_PBE"], R["6b_XTB"]
    para(doc, "In the xTB run the ice cluster melts, and this shows up in the structure rather than in the "
              f"temperature. The tetrahedral order of the interior molecules drops from {b['q'][:b['k']].mean():.2f} "
              f"to {b['q'][-b['k']:].mean():.2f} within the first ~800 fs and then stays there. In the O–O "
              "distribution the second-neighbour peak at 4.4 Å disappears and the minimum at 3.5 Å fills in "
              "(Figure 4b). The number of hydrogen bonds hardly changes "
              f"({b['hb'][:b['k']].mean():.2f} → {b['hb'][-b['k']:].mean():.2f} per molecule), so the molecules "
              "keep their hydrogen bonds but lose the tetrahedral arrangement and the long-range order of the "
              "crystal.")
    para(doc, f"The 100 fs DFT run is too short to see this: q only falls from {a['q'][:a['k']].mean():.2f} to "
              f"{a['q'][-a['k']:].mean():.2f} and the pair distribution still has the ice peaks. Hydrogen bonds in "
              "water rearrange on a picosecond time scale, so 100 fs only samples vibrations around the starting "
              "structure.")
    para(doc, f"In the xTB run some molecules evaporate. The largest O distance from the cluster centre grows from "
              f"{b['rmax'][0]:.1f} Å to {b['rmax'].max():.1f} Å, close to the 25 Å wall, so without the confining "
              "sphere these molecules would leave the cluster.")
    para(doc, "The thermostat keeps the average temperature at the set point: over the second half of the xTB run "
              f"the mean is {b['E'][len(b['E']) // 2:, 1].mean():.0f} K with a standard deviation of "
              f"{b['E'][len(b['E']) // 2:, 1].std():.0f} K. The 60-atom DFT cluster fluctuates by about ±50 K, "
              "because relative temperature fluctuations scale as 1/√N and are large in small systems.")

    heading(doc, "What else can be obtained from the trajectories")
    para(doc, "Besides the melting, the trajectory and the per-step energies that ORCA writes can be used for:")
    para(doc, "Structure: radial distribution functions g(r) for O–O, O–H and H–H and the coordination numbers "
              "from their integrals, hydrogen-bond distance and angle distributions, and the size and shape of "
              "the cluster.")
    para(doc, "Dynamics: the mean square displacement and the diffusion coefficient, hydrogen-bond lifetimes and "
              "reorientation times, and the velocity autocorrelation function, whose Fourier transform gives the "
              "vibrational density of states. The dipole autocorrelation function gives the IR spectrum including "
              "anharmonic and temperature effects, which a harmonic frequency calculation as in Exercise 1 "
              "cannot provide.")
    para(doc, "Thermodynamics and checks: kinetic and potential energy distributions (the heat capacity follows "
              "from their fluctuations), the evaporation rate, and the drift of the conserved energy as a check of "
              f"the integration, here {(b['E'][-1, 3] - b['E'][1, 3]) * 627.5095:+.1f} kcal mol^{{-1}} over 2.5 ps "
              f"for xTB and {(a['E'][-1, 3] - a['E'][1, 3]) * 627.5095:+.2f} kcal mol^{{-1}} over 100 fs for DFT.")
    para(doc, "Snapshots from the trajectory can also serve as starting structures for further calculations, for "
              "example spectra of solvated molecules averaged over the sampled configurations.")

    save(doc, REPORT_DIR / "HW2_Ex6_molecular_dynamics_water.docx")


if __name__ == "__main__":
    main()
