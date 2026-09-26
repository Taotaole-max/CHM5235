"""把两个振动模式的 GIF 动画拆成"分解帧"，印进报告。

为什么要这个：作业要求报告是**单个 PDF**，而 PDF 里放不进动画。只在图注里写 GIF 的
文件名，改卷人拿到 PDF 时什么都看不到。所以把动画在一个周期里的四个相位取出来排成一张图，
动画的内容就直接印在纸上了；GIF 文件仍然一起交。

一个简正模式是简谐振动，一个周期取 0、T/4、T/2、3T/4 四帧就够：T/4 和 3T/4 是两个折返点
（位移最大、方向相反），0 和 T/2 是过平衡位置。GIF 是 20 帧一个周期，所以取第 0、5、10、15 帧。

输出：ex1_mode12_filmstrip_B3LYP_gas.png、ex1_mode17_filmstrip_B3LYP_gas.png
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
TITLE_BAND = 90      # GIF 每帧顶部自带两行标题，裁掉，信息放到 Word 图注里
PHASES = [(0, "0"), (5, "T/4"), (10, "T/2"), (15, "3T/4")]


def font(size):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def common_bbox(frames):
    """四帧共用一个裁剪框，否则并排时分子会忽大忽小。"""
    l = t = 10 ** 9
    r = b = 0
    for im in frames:
        bg = Image.new("RGB", im.size, (255, 255, 255))
        box = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 8 else 0).getbbox()
        if box is None:
            continue
        l, t = min(l, box[0]), min(t, box[1])
        r, b = max(r, box[2]), max(b, box[3])
    pad = 20
    w, h = frames[0].size
    return (max(l - pad, 0), max(t - pad, 0), min(r + pad, w), min(b + pad, h))


def build(gif_name, out_name):
    gif = Image.open(HERE / gif_name)
    frames = []
    for i, _ in PHASES:
        gif.seek(i)
        im = gif.convert("RGB")
        frames.append(im.crop((0, TITLE_BAND, im.width, im.height)))
    box = common_bbox(frames)
    cells = [f.crop(box) for f in frames]

    cw, ch = cells[0].size
    band = round(ch * 0.13)
    gap = round(cw * 0.04)
    sheet = Image.new("RGB", (4 * cw + 3 * gap, ch + band), "white")
    draw = ImageDraw.Draw(sheet)
    fnt = font(round(band * 0.60))
    for k, (cell, (_, label)) in enumerate(zip(cells, PHASES)):
        x = k * (cw + gap)
        tw = draw.textlength(label, font=fnt)
        draw.text((x + (cw - tw) / 2, band * 0.12), label, fill=(0, 0, 0), font=fnt)
        sheet.paste(cell, (x, band))
    out = HERE / out_name
    sheet.save(out)
    print(f"写出 {out.name}  {sheet.size}")


if __name__ == "__main__":
    build("ex1_mode12_animation_B3LYP_gas.gif", "ex1_mode12_filmstrip_B3LYP_gas.png")
    build("ex1_mode17_animation_B3LYP_gas.gif", "ex1_mode17_filmstrip_B3LYP_gas.png")
