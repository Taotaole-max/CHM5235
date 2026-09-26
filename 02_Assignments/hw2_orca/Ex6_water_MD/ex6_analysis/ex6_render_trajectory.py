"""Ex6 轨迹渲染：报告用的首/末帧快照，以及题目要的动画（GIF）。

用法：D:\\venvs\\cm5235_hw2\\Scripts\\python ex6_render_trajectory.py [--root <Ex6_water_MD 目录>]
写出（本文件夹）：
    ex6_fig_snapshots.png                 (a) 和 (b) 各自的第一帧 / 最后一帧
    ex6b_trajectory_animation_XTB.gif     (b) 128 个水的轨迹动画，每 25 步取一帧（12.5 fs 一帧）
画法：O 红、H 白；O–H 共价键灰色；氢键（H···O < 2.2 Å）淡蓝细线。相机固定，所有帧同一视角。
"""
import argparse
from pathlib import Path

import numpy as np
import pyvista as pv
from PIL import Image

pv.OFF_SCREEN = True
HERE = Path(__file__).resolve().parent
SIMS = {"6a_DFT_PBE": ("ex6a_trajectory_DFT_PBE.xyz", "(a) PBE/def2-SVP, 20 H2O"),
        "6b_XTB": ("ex6b_trajectory_XTB.xyz", "(b) GFN2-xTB, 128 H2O")}
DT = 0.5


def read_traj(path):
    lines = Path(path).read_text().splitlines()
    n = int(lines[0]); nfr = len(lines) // (n + 2)
    sym = np.array([lines[2 + i].split()[0] for i in range(n)])
    X = np.empty((nfr, n, 3))
    for f in range(nfr):
        X[f] = [[float(v) for v in l.split()[1:4]] for l in lines[f * (n + 2) + 2:f * (n + 2) + 2 + n]]
    return sym, X


def segments(a, b, cutoff_lo, cutoff_hi):
    d = np.linalg.norm(a[:, None] - b[None], axis=-1)
    i, j = np.where((d > cutoff_lo) & (d < cutoff_hi))
    if len(i) == 0:
        return None
    pts = np.empty((2 * len(i), 3)); pts[0::2] = a[i]; pts[1::2] = b[j]
    lines = np.column_stack([np.full(len(i), 2), np.arange(0, 2 * len(i), 2), np.arange(1, 2 * len(i), 2)])
    return pv.PolyData(pts, lines=lines.ravel())


def render(sym, x, cam, size, label=None, scale=None):
    O = x[sym == "O"]; H = x[sym == "H"]
    p = pv.Plotter(window_size=size)
    p.set_background("white")
    p.add_mesh(pv.PolyData(O).glyph(geom=pv.Sphere(radius=0.33, theta_resolution=20, phi_resolution=20),
                                    scale=False, orient=False), color="#e8231a", smooth_shading=True)
    p.add_mesh(pv.PolyData(H).glyph(geom=pv.Sphere(radius=0.2, theta_resolution=16, phi_resolution=16),
                                    scale=False, orient=False), color="#f2f2f2", smooth_shading=True)
    cov = segments(O, H, 0.0, 1.25)
    if cov is not None:
        p.add_mesh(cov.tube(radius=0.07), color="#9a9a9a", smooth_shading=True)
    hb = segments(H, O, 1.25, 2.2)
    if hb is not None:
        p.add_mesh(hb, color="#6fa8dc", line_width=1.5)
    p.camera_position = cam
    p.enable_parallel_projection()
    if scale:
        p.camera.parallel_scale = scale     # 同一条轨迹所有帧同一比例
    if label:
        p.add_text(label, position="upper_left", font_size=12, color="black")
    img = p.screenshot(return_img=True, scale=1)
    ps = p.camera.parallel_scale
    p.close()
    return img, ps


def fixed_camera(X, sym):
    """相机：大致沿团簇最"扁"的主轴看过去（投影面积最大），再斜一点，免得正对晶面、分子前后重叠。
    返回相机位置和比例；比例按第一帧团簇在画面上的半径定，整条轨迹不变。"""
    O = X[0][sym == "O"]
    c = O.mean(0)
    w, v = np.linalg.eigh(np.cov((O - c).T))
    view = v[:, 0] + 0.45 * v[:, 1] + 0.30 * v[:, 2]
    view /= np.linalg.norm(view)
    up = v[:, 2] - v[:, 2].dot(view) * view; up /= np.linalg.norm(up)
    rel = O - c
    proj = rel - np.outer(rel @ view, view)
    scale = 1.15 * np.linalg.norm(proj, axis=1).max() + 2.0
    return [tuple(c + view * 60), tuple(c), tuple(up)], scale


def main(root):
    panels = []
    for sim, (traj, title) in SIMS.items():
        path = root / sim / traj
        if not path.exists():
            print("跳过", sim); continue
        sym, X = read_traj(path)
        cam, scale = fixed_camera(X, sym)
        row = []
        for f, tag in [(0, "start"), (len(X) - 1, "end")]:
            img, _ = render(sym, X[f], cam, (900, 900), f"{title}\n{tag}: t = {f * DT:g} fs", scale)
            row.append(img)
        panels.append(np.concatenate(row, axis=1))
        if sim == "6b_XTB":
            step = 25
            frames = []
            for f in range(0, len(X), step):
                img, _ = render(sym, X[f], cam, (560, 560), f"{title}, 400 K\nt = {f * DT:6.1f} fs", scale)
                frames.append(Image.fromarray(img).convert("P", palette=Image.ADAPTIVE, colors=128))
            gif = HERE / "ex6b_trajectory_animation_XTB.gif"
            frames[0].save(gif, save_all=True, append_images=frames[1:], duration=80, loop=0, optimize=True)
            print("写出", gif.name, f"({len(frames)} 帧，每 {step} 步一帧)")
    if panels:
        wmax = max(p.shape[1] for p in panels)
        panels = [np.pad(p, ((0, 0), (0, wmax - p.shape[1]), (0, 0)), constant_values=255) for p in panels]
        out = HERE / "ex6_fig_snapshots.png"
        Image.fromarray(np.concatenate(panels, axis=0)).save(out)
        print("写出", out.name)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(HERE.parent))
    main(Path(ap.parse_args().root))
