"""把 Avogadro 逐帧渲染出来的截图合成 (a) 题目要的 GIF 动画、(b) 报告里印的分解帧。

背景：Avogadro 2 自带的"录像"功能一点就崩（作业原文也写了 "In Avogadro, the function of
saving the video is not working properly"，并允许改用录屏）。所以做法是：轨迹在 Avogadro
里逐帧显示，外部把三维视口一帧一帧抓下来，再在这里拼成 GIF。每一帧的画面都是 Avogadro 渲染的。

输入：<frames_dir>/frame_001.png ... frame_051.png   （2070x1310 的视口截图）
输出：
    ex6b_trajectory_animation_from_avogadro.gif        51 帧，2.5 ps
    ex6b_trajectory_filmstrip_from_avogadro.png        6 张分解帧，带时间标注（报告用）

用法：python ex6_build_animation_from_avogadro_frames.py <frames_dir>
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FRAME_FS = 50.0        # 每张截图之间隔 100 个 MD 步 x 0.5 fs
PAD = 40               # 裁剪时在分子外留的白边（像素）


def bbox_over_all(paths):
    """所有帧共用一个裁剪框，否则动画会因为逐帧裁剪而抖动。"""
    l = t = 10 ** 9
    r = b = 0
    for p in paths:
        a = np.asarray(Image.open(p).convert("L"))
        ys, xs = np.where(a < 240)
        l, r = min(l, xs.min()), max(r, xs.max())
        t, b = min(t, ys.min()), max(b, ys.max())
    h, w = a.shape
    return (max(l - PAD, 0), max(t - PAD, 0), min(r + PAD, w), min(b + PAD, h))


def flatten(p, box):
    """截图是 RGBA，透明像素的 RGB 是黑的，先压到白底再裁。"""
    im = Image.open(p)
    if im.mode in ("RGBA", "LA"):
        flat = Image.new("RGB", im.size, (255, 255, 255))
        flat.paste(im, mask=im.split()[-1])
        im = flat
    else:
        im = im.convert("RGB")
    return im.crop(box)


def font(size):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def main(frames_dir):
    paths = sorted(Path(frames_dir).glob("frame_*.png"))
    if not paths:
        sys.exit(f"{frames_dir} 里没有 frame_*.png")
    box = bbox_over_all(paths)
    print(f"{len(paths)} 帧，公共裁剪框 {box}")

    # ---- GIF：宽度压到 640 px，控制文件大小
    frames = [flatten(p, box) for p in paths]
    w0, h0 = frames[0].size
    scale = 640 / w0
    gif = [f.resize((640, round(h0 * scale)), Image.LANCZOS) for f in frames]
    out_gif = HERE / "ex6b_trajectory_animation_from_avogadro.gif"
    gif[0].save(out_gif, save_all=True, append_images=gif[1:], duration=100, loop=0, optimize=True)
    print(f"写出 {out_gif.name}  {len(gif)} 帧, {out_gif.stat().st_size/1e6:.1f} MB")

    # ---- 分解帧：等时间间隔取 6 张，3 x 2 排版，每格标时间
    idx = np.linspace(0, len(frames) - 1, 6).round().astype(int)
    cell_w = 900
    cells = [frames[i].resize((cell_w, round(frames[i].height * cell_w / frames[i].width)),
                              Image.LANCZOS) for i in idx]
    cw, ch = cells[0].size
    band = round(ch * 0.10)
    gap = round(cw * 0.03)
    cols, rows = 3, 2
    sheet = Image.new("RGB", (cols * cw + (cols - 1) * gap,
                              rows * (ch + band) + (rows - 1) * gap), "white")
    draw = ImageDraw.Draw(sheet)
    fnt = font(round(band * 0.62))
    for k, (i, cell) in enumerate(zip(idx, cells)):
        cx = (k % cols) * (cw + gap)
        cy = (k // cols) * (ch + band + gap)
        label = f"t = {i * FRAME_FS:.0f} fs"
        tw = draw.textlength(label, font=fnt)
        draw.text((cx + (cw - tw) / 2, cy + band * 0.15), label, fill=(0, 0, 0), font=fnt)
        sheet.paste(cell, (cx, cy + band))
    out_png = HERE / "ex6b_trajectory_filmstrip_from_avogadro.png"
    sheet.save(out_png)
    print(f"写出 {out_png.name}  {sheet.size}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else HERE / "原始逐帧截图")
