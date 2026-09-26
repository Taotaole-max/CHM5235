# 从讲义 PDF 按区域截图 → img/Lx_pN[_tag].png，自动去白边
# 坐标是讲义页面的 pt（页面 780×540 或按各讲实际大小），用 view.py 看好了再填
import sys
from pathlib import Path
import pymupdf
from PIL import Image, ImageChops

here = Path(__file__).parent
slides = here.parents[2] / "01_Lecture_Notes" / "slides"
img = here / "img"
img.mkdir(exist_ok=True)

# (文件名, 讲次, 页, (x0, y0, x1, y1) 或 None 表示整页)
CROPS = [
    ("L1_p15_cluster", 1, 15, (40, 90, 600, 430)),
    ("L1_p21_moore", 1, 21, (120, 128, 445, 468)),
    ("L2_p5_bohr", 2, 5, (30, 150, 700, 440)),
    ("L2_p8_twolevel", 2, 8, (20, 180, 712, 482)),
    ("L2_p9_boltz", 2, 9, (60, 215, 700, 505)),
    ("L2_p53_Ylm", 2, 53, (25, 78, 665, 485)),
    ("L2_p54_levels", 2, 54, (35, 232, 705, 492)),
    ("L2_p55_radial", 2, 55, (140, 25, 570, 495)),
    ("L2_p75_penetration", 2, 75, (35, 278, 705, 510)),
    ("L2_p89_scf", 2, 89, (40, 140, 710, 375)),
    ("L3_p44_sdenergy", 3, 44, (20, 95, 700, 470)),
    ("L3_p45_bs", 3, 45, (20, 85, 700, 395)),
    ("L3_p47_koopmans", 3, 47, (20, 110, 700, 520)),
    ("L3_p51_rohf", 3, 51, (190, 235, 580, 525)),
    ("L3_p60_scf", 3, 60, (20, 88, 710, 535)),
    ("L3_p66_damping", 3, 66, (20, 178, 700, 470)),
    ("L3_p67_levelshift", 3, 67, (150, 245, 650, 450)),
    ("L3_p72_stogto", 3, 72, None),
    ("L3_p76_basisname", 3, 76, (20, 82, 710, 530)),
    ("L3_p79_mcscf", 3, 79, (20, 95, 710, 530)),
    ("L3_p69_symmetry", 3, 69, (20, 255, 710, 470)),
    ("L4_p4_h2diss", 4, 4, (380, 140, 690, 345)),
    ("L4_p5_basisconv", 4, 5, (10, 250, 350, 505)),
    ("L4_p11_ci", 4, 11, (20, 120, 700, 420)),
    ("L4_p18_cimatrix", 4, 18, (20, 222, 640, 385)),
    ("L4_p21_h2pes", 4, 21, (100, 90, 580, 475)),
    ("L4_p37_bsse", 4, 37, (25, 115, 700, 480)),
    ("L4_p38_cp", 4, 38, (40, 60, 690, 440)),
    ("L4_p43_cbs", 4, 43, (20, 120, 700, 530)),
    ("L4_p44_density", 4, 44, (20, 90, 700, 530)),
    ("L5_p10_maps", 5, 10, (20, 120, 700, 440)),
    ("L5_p16_hk1", 5, 16, (20, 70, 700, 460)),
    ("L5_p20_hk2", 5, 20, (60, 103, 560, 262)),
    ("L5_p23_hfdft", 5, 23, (20, 15, 700, 505)),
    ("L5_p33_sie", 5, 33, (20, 15, 700, 530)),
    ("L5_p39_mag", 5, 39, (20, 75, 710, 530)),
    ("L6_p9_bondorder", 6, 9, (20, 228, 700, 525)),
    ("L6_p10_mep", 6, 10, (20, 85, 710, 520)),
    ("L6_p13_loc", 6, 13, (20, 100, 710, 530)),
    ("L6_p17_dirac", 6, 17, (20, 55, 710, 470)),
    ("L6_p22_cube", 6, 22, (20, 20, 710, 470)),
    ("L6_p29_surface", 6, 29, (20, 80, 710, 470)),
    ("L6_p30_pcm", 6, 30, (20, 78, 710, 470)),
    ("L6_p39_vertical", 6, 39, (20, 305, 710, 500)),
]
exec((here / "crops_list.py").read_text(encoding="utf-8")) if (here / "crops_list.py").exists() else None


def trim(im, pad=6):
    bg = Image.new(im.mode, im.size, (255, 255, 255))
    diff = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 18 else 0)
    box = diff.getbbox()
    if not box:
        return im
    x0, y0, x1, y1 = box
    return im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))


def main(only=None):
    docs = {}
    for name, L, p, clip in CROPS:
        if only and name not in only:
            continue
        d = docs.setdefault(L, pymupdf.open(slides / f"CM5235_Lecture_0{L}.pdf"))
        page = d[p - 1]
        pix = page.get_pixmap(dpi=220, clip=pymupdf.Rect(*clip) if clip else None)
        im = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        trim(im).save(img / f"{name}.png", optimize=True)
        print("ok", name)


if __name__ == "__main__":
    main(set(sys.argv[1:]) or None)
