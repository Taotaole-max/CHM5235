"""Ex1 的全部图：本机用 PyVista 离屏渲染。

用法（用 D 盘的虚拟环境）：
    D:\\venvs\\cm5235_hw2\\Scripts\\python ex1_render_figures.py [mode | orbitals | esp | all]

输入：
    ../B3LYP_gas/ex1_mode12_animation_ORCAindex12_B3LYP_gas.xyz   orca_pltvib 写的 12 号模式（20 帧，第 1 帧带位移矢量）
    ../B3LYP_gas/ex1_optfreq_B3LYP_gas.out                          读 12 号模式的频率和 IR 强度
    cube_job/cube_files/ex1_cube_{HOMO,LUMO,density}_B3LYP_gas.cube 集群上 ORCA %plots 写的格点
    cube_job/cube_files/ex1_esp_values_on_grid_B3LYP_gas.txt        orca_vpot 算的静电势（Bohr，原子单位）
    cube_job/ex1_esp_grid_box.txt                                   上面静电势格点的起点、间距、点数
输出（本文件夹）：
    ex1_fig_mode12_displacements_B3LYP_gas.png    报告用：12 号模式的位移箭头
    ex1_mode12_animation_B3LYP_gas.gif            题目要的动画
    ex1_fig_HOMO_LUMO_B3LYP_gas.png               报告用：HOMO、LUMO
    ex1_fig_density_ESP_B3LYP_gas.png             报告用：电子密度等值面上映射静电势
"""
import re
import sys
from pathlib import Path

import numpy as np
import pyvista as pv
from PIL import Image

pv.OFF_SCREEN = True
HERE = Path(__file__).resolve().parent
EX1 = HERE.parent
BOHR = 0.529177210903  # Å
HARTREE_KCAL = 627.509474

CPK = {"H": "#ffffff", "C": "#8c8c8c", "O": "#e8231a", "Cl": "#1fc41f"}
COV = {"H": 0.31, "C": 0.76, "O": 0.66, "Cl": 1.02}       # 共价半径，Å，用来判断成键
BALL = {"H": 0.22, "C": 0.34, "O": 0.34, "Cl": 0.42}     # 画图用的球半径，Å


# ---------------------------------------------------------------- 分子骨架
def add_molecule(p, sym, xyz_A, scale=1.0, bond_color="#b0b0b0"):
    """球棍模型；坐标单位 Å，scale 用于整体换算到别的单位（例如 Bohr）。"""
    n = len(sym)
    for i in range(n):
        p.add_mesh(pv.Sphere(radius=BALL[sym[i]] * scale, center=xyz_A[i] * scale,
                             theta_resolution=36, phi_resolution=36),
                   color=CPK[sym[i]], smooth_shading=True, specular=0.4)
    for i in range(n):
        for j in range(i + 1, n):
            d = np.linalg.norm(xyz_A[i] - xyz_A[j])
            if d < 1.2 * (COV[sym[i]] + COV[sym[j]]):
                a, b = xyz_A[i] * scale, xyz_A[j] * scale
                p.add_mesh(pv.Cylinder(center=(a + b) / 2, direction=b - a, radius=0.09 * scale,
                                       height=np.linalg.norm(b - a), resolution=24),
                           color=bond_color, smooth_shading=True)


def ring_normal(xyz):
    """最小二乘平面的法向量（苯环平面垂直方向），用来摆相机。"""
    c = xyz - xyz.mean(0)
    return np.linalg.svd(c)[2][2]


def set_camera(p, center, normal, up, dist, tilt_deg=0.0):
    """沿苯环法线看过去；tilt_deg 让视线绕 up 轴转一点，能看出 π 轨道上下两瓣。"""
    t = np.radians(tilt_deg)
    right = np.cross(up, normal)
    view = normal * np.cos(t) + right * np.sin(t)
    p.camera_position = [tuple(center + view * dist), tuple(center), tuple(up)]


# ---------------------------------------------------------------- 12 号振动模式
def read_pltvib(path):
    """orca_pltvib 的多帧 xyz：每帧 13 行原子；第 1 帧有 3 列额外的位移矢量。"""
    lines = Path(path).read_text().splitlines()
    n = int(lines[0])
    frames, sym, disp = [], None, None
    k = 0
    while k < len(lines) and lines[k].strip():
        block = [l.split() for l in lines[k + 2:k + 2 + n]]
        if sym is None:
            sym = [b[0] for b in block]
            disp = np.array([[float(v) for v in b[4:7]] for b in block])
        frames.append(np.array([[float(v) for v in b[1:4]] for b in block]))
        k += n + 2
    return sym, frames, disp


def mode_info(idx):
    """从 IR 谱表里取某个 ORCA 模式编号的频率和 IR 强度。"""
    out = (EX1 / "B3LYP_gas" / "ex1_optfreq_B3LYP_gas.out").read_text()
    ir = out[out.rfind("IR SPECTRUM"):]
    m = re.search(rf"^\s*{idx}:\s+([\d.]+)\s+[\d.]+\s+([\d.]+)", ir, re.M)
    return float(m.group(1)), float(m.group(2))


# 题目说的 "normal mode number 12" 有两种理解，两个都出图：
#   ORCA 编号 12 —— ORCA 输出里字面标 "12:" 的那个模式（第 7 个真振动）
#   ORCA 编号 17 —— Avogadro / Chemcraft 的振动列表只列真振动、从 1 开始数，它们的第 12 个
MODES = {12: ("ORCAindex12", "ORCA numbering"), 17: ("12thVibration", "12th real vibration")}


def render_mode(idx):
    tag, _ = MODES[idx]
    sym, frames, disp = read_pltvib(EX1 / "B3LYP_gas" / f"ex1_mode12_animation_{tag}_B3LYP_gas.xyz")
    freq, ir = mode_info(idx)
    eq = frames[0]  # 第 1 帧（Energy -1000 那帧）是平衡结构
    heavy = np.array([i for i, s in enumerate(sym) if s != "H"])
    normal = ring_normal(eq[[i for i, s in enumerate(sym) if s == "C"]])
    up = np.array([0.0, 1.0, 0.0]); up -= up.dot(normal) * normal; up /= np.linalg.norm(up)
    center = eq[heavy].mean(0)
    # 面外振动（位移垂直于环平面）正对环看时箭头正对镜头、完全看不见，这种要侧着看：
    # 视线沿环平面内的一个轴，画面上方取环的法线方向，于是面外位移在画面里是上下方向。
    oop = ((disp @ normal) ** 2).sum() / (disp ** 2).sum()
    side_view = oop > 0.5
    if side_view:
        right = np.cross(up, normal)
        view = right * 0.90 + up * 0.28 + normal * 0.25   # 略偏离环平面，画面有立体感又不挡箭头
        view /= np.linalg.norm(view)
        cam = [tuple(center + view * 17), tuple(center), tuple(normal)]

    # 静态图：平衡结构 + 位移箭头
    p = pv.Plotter(window_size=(1400, 1400))
    p.set_background("white")
    add_molecule(p, sym, eq)
    amp = 1.3 / np.linalg.norm(disp, axis=1).max()   # 最长的箭头 1.3 Å
    for i in range(len(sym)):
        v = disp[i] * amp
        if np.linalg.norm(v) > 0.15:
            p.add_mesh(pv.Arrow(start=eq[i] + v / np.linalg.norm(v) * BALL[sym[i]], direction=v,
                                scale=float(np.linalg.norm(v)), tip_length=0.3, tip_radius=0.1,
                                shaft_radius=0.035), color="#1a4fd6", smooth_shading=True)
    if side_view:
        p.camera_position = cam
    else:
        set_camera(p, center, normal, up, dist=17)
    p.enable_parallel_projection()
    p.reset_camera(); p.camera.zoom(0.95)   # 视野包住原子和箭头
    out = HERE / f"ex1_fig_mode{idx}_displacements_B3LYP_gas.png"
    p.screenshot(out); p.close()
    print("写出", out.name, f"(ORCA mode {idx}: {freq:.1f} cm-1, IR {ir:.2f} km/mol)")

    # 动画：orca_pltvib 的 20 帧是一个完整周期
    imgs = []
    for fr in frames:
        p = pv.Plotter(window_size=(700, 700))
        p.set_background("white")
        add_molecule(p, sym, fr)
        if side_view:
            p.camera_position = cam
        else:
            set_camera(p, center, normal, up, dist=17)
        p.enable_parallel_projection()
        p.add_text(f"2-chlorophenol, B3LYP/def2-TZVP\nORCA mode {idx} ({MODES[idx][1]}): {freq:.1f} cm-1",
                   position="upper_left", font_size=11, color="black")
        imgs.append(Image.fromarray(p.screenshot(return_img=True)))
        p.close()
    gif = HERE / f"ex1_mode{idx}_animation_B3LYP_gas.gif"
    imgs[0].save(gif, save_all=True, append_images=imgs[1:], duration=60, loop=0, optimize=True)
    print("写出", gif.name, f"({len(imgs)} 帧)")


# ---------------------------------------------------------------- cube 文件
def read_cube(path):
    """Gaussian cube → (pv.ImageData, 原子符号, 原子坐标 Å)。数据顺序：x 最慢、z 最快。"""
    lines = Path(path).read_text().splitlines()
    nat, *org = lines[2].split()
    nat = abs(int(nat)); org = np.array([float(v) for v in org[:3]])
    ax = [lines[3 + i].split() for i in range(3)]
    npts = [int(a[0]) for a in ax]
    step = [float(ax[i][1 + i]) for i in range(3)]
    zsym = {1: "H", 6: "C", 8: "O", 17: "Cl"}
    atoms = [lines[6 + i].split() for i in range(nat)]
    sym = [zsym[int(a[0])] for a in atoms]
    xyz = np.array([[float(v) for v in a[2:5]] for a in atoms]) * BOHR
    start = 6 + nat
    if lines[2].split()[0].startswith("-"):      # 负原子数：MO cube 多一行轨道编号
        start += 1
    data = np.array(" ".join(lines[start:]).split(), dtype=float).reshape(npts)
    grid = pv.ImageData(dimensions=npts, spacing=[s * BOHR for s in step], origin=org * BOHR)
    grid.point_data["v"] = data.flatten(order="F")
    return grid, sym, xyz


def render_orbitals(iso=0.02):
    cf = HERE / "cube_job" / "cube_files"
    # 轨道能量用 ex1_extract_results.py 里验证过的解析（只读 SPIN UP 那一段，读到空行就停）
    sys.path.insert(0, str(EX1 / "ex1_analysis"))
    from ex1_extract_results import parse_orbitals
    lines = (EX1 / "B3LYP_gas" / "ex1_optfreq_B3LYP_gas.out").read_text().splitlines()
    homo, lumo = parse_orbitals(lines)
    e = {homo[0]: homo[2], lumo[0]: lumo[2]}
    panels = []
    for name, idx in [("HOMO", 32), ("LUMO", 33)]:
        grid, sym, xyz = read_cube(cf / f"ex1_cube_{name}_B3LYP_gas.cube")
        normal = ring_normal(xyz[[i for i, s in enumerate(sym) if s == "C"]])
        up = np.array([0.0, 1.0, 0.0]); up -= up.dot(normal) * normal; up /= np.linalg.norm(up)
        p = pv.Plotter(window_size=(1000, 1000))
        p.set_background("white")
        add_molecule(p, sym, xyz)
        p.add_mesh(grid.contour([iso], scalars="v"), color="#d7301f", opacity=1.0, smooth_shading=True,
                   specular=0.3)
        p.add_mesh(grid.contour([-iso], scalars="v"), color="#2166ac", opacity=1.0, smooth_shading=True,
                   specular=0.3)
        set_camera(p, xyz.mean(0), normal, up, dist=17, tilt_deg=25)
        p.enable_parallel_projection()
        p.add_text(f"{name} (orbital {idx}),  E = {e[idx]:.2f} eV", position="upper_edge",
                   font_size=16, color="black")
        panels.append(p.screenshot(return_img=True)); p.close()
    img = Image.fromarray(np.concatenate(panels, axis=1))
    path = HERE / "ex1_fig_HOMO_LUMO_B3LYP_gas.png"
    img.save(path)
    print("写出", path.name, f"(isovalue ±{iso} a.u.)")


def render_esp(iso=0.001):
    cf = HERE / "cube_job" / "cube_files"
    dens, sym, xyz = read_cube(cf / "ex1_cube_density_B3LYP_gas.cube")
    # 等值面在凹角处（Cl 和苯环之间）会因格点偏粗出现台阶，Taubin 平滑能去掉台阶又不让曲面收缩
    surf = dens.contour([iso], scalars="v").smooth_taubin(n_iter=40, pass_band=0.05)
    # 静电势格点：orca_vpot 输出（Bohr, a.u.），顺序与 ex1_esp_grid_box.txt 一致（x 最慢）
    box = np.loadtxt(HERE / "cube_job" / "ex1_esp_grid_box.txt")
    npts = box[:, 2].astype(int)
    v = np.loadtxt(cf / "ex1_esp_values_on_grid_B3LYP_gas.txt", skiprows=1)[:, 3]
    esp = pv.ImageData(dimensions=npts, spacing=box[:, 1] * BOHR, origin=box[:, 0] * BOHR)
    esp.point_data["ESP"] = v.reshape(npts).flatten(order="F")
    surf = surf.sample(esp)
    vals = surf.point_data["ESP"]
    lim = float(np.percentile(np.abs(vals), 98))
    normal = ring_normal(xyz[[i for i, s in enumerate(sym) if s == "C"]])
    up = np.array([0.0, 1.0, 0.0]); up -= up.dot(normal) * normal; up /= np.linalg.norm(up)
    panels = []
    # 左：正对苯环看，表面半透明，能看到里面的分子（开 depth peeling，半透明才不会出条纹伪影）
    # 右：斜 45° 看，表面不透明，只看颜色分布
    for tilt, opac, label in [(0, 0.8, "view perpendicular to the ring (surface semi-transparent)"),
                              (45, 1.0, "tilted by 45° (surface opaque)")]:
        p = pv.Plotter(window_size=(1000, 1000))
        p.set_background("white")
        p.enable_depth_peeling(number_of_peels=12)
        add_molecule(p, sym, xyz)
        p.add_mesh(surf, scalars="ESP", cmap="RdBu", clim=[-lim, lim], smooth_shading=True,
                   opacity=opac, show_scalar_bar=False)
        if tilt == 45:
            p.add_scalar_bar(title="ESP (a.u.)", n_labels=5, fmt="%.3f", color="black",
                             vertical=True, position_x=0.80, position_y=0.2, height=0.6, width=0.07,
                             title_font_size=34, label_font_size=30)
        set_camera(p, xyz.mean(0), normal, up, dist=20, tilt_deg=tilt)
        p.enable_parallel_projection()
        p.reset_camera(); p.camera.zoom(1.1)    # reset 后按分子大小取景，再放大一点；右边留出色标的位置
        p.add_text(label, position="upper_edge", font_size=14, color="black")
        panels.append(p.screenshot(return_img=True)); p.close()
    img = Image.fromarray(np.concatenate(panels, axis=1))
    path = HERE / "ex1_fig_density_ESP_B3LYP_gas.png"
    img.save(path)
    print("写出", path.name, f"(density isovalue {iso} a.u.; ESP on surface {vals.min():.4f} … {vals.max():.4f} a.u.,"
          f" colour range ±{lim:.3f} a.u. = ±{lim * HARTREE_KCAL:.1f} kcal/mol)")


def render_numbering():
    """原子编号示意图（2D，投影到苯环平面）：和 ex1_extract_results.py 的编号一致（C1 连 OH，C2 连 Cl）。"""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    sys.path.insert(0, str(EX1 / "ex1_analysis"))
    from ex1_extract_results import atom_labels
    L = (EX1 / "B3LYP_gas" / "ex1_optimized_geometry_B3LYP_gas.xyz").read_text().splitlines()
    n = int(L[0])
    sym = [l.split()[0] for l in L[2:2 + n]]
    xyz = np.array([[float(v) for v in l.split()[1:4]] for l in L[2:2 + n]])
    lab, _ = atom_labels([(s, tuple(x)) for s, x in zip(sym, xyz)])
    ring = [i for i, s in enumerate(sym) if s == "C"]
    normal = ring_normal(xyz[ring])
    up = np.array([0.0, 1.0, 0.0]); up -= up.dot(normal) * normal; up /= np.linalg.norm(up)
    right = np.cross(up, normal)
    P = np.c_[(xyz - xyz[ring].mean(0)) @ right, (xyz - xyz[ring].mean(0)) @ up]
    fig, ax = plt.subplots(figsize=(4.2, 4.6), dpi=300)
    for i in range(n):
        for j in range(i + 1, n):
            if np.linalg.norm(xyz[i] - xyz[j]) < 1.2 * (COV[sym[i]] + COV[sym[j]]):
                ax.plot(*P[[i, j]].T, color="#555555", lw=2.2, zorder=1)
    for i in range(n):
        ax.scatter(*P[i], s=(BALL[sym[i]] * 420) ** 2 / 40, color=CPK[sym[i]], edgecolor="black",
                   linewidth=0.8, zorder=2)
    for i in range(n):
        if sym[i] == "H" and lab[i] != "H(O)":
            continue
        d = P[i] / (np.linalg.norm(P[i]) + 1e-9)          # 从环心指向外
        if sym[i] == "C":
            pos = P[i] - d * 0.62                          # 碳的编号写在环内侧
        else:
            pos = P[i] + d * 0.62
        ax.text(*pos, lab[i], ha="center", va="center", fontsize=11, fontweight="bold", zorder=3)
    ax.set_aspect("equal"); ax.axis("off")
    ax.margins(0.12)
    path = HERE / "ex1_fig_atom_numbering.png"
    fig.savefig(path, bbox_inches="tight", facecolor="white"); plt.close(fig)
    print("写出", path.name)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("numbering", "all"):
        render_numbering()
    if what in ("mode", "all"):
        for idx in MODES:
            render_mode(idx)
    if what in ("orbitals", "all"):
        render_orbitals()
    if what in ("esp", "all"):
        render_esp()
