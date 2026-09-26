# 两件事：
# 1) 从 raw.pdf 的命名目标里读每个 id 的页码，写 out/pages.json（build.mjs 下一遍用来填目录、索引、页码引用）
# 2) 给每页盖页眉、页码和外侧书签（双面打印：奇数页在右、偶数页在左），输出成品 PDF
# 用法：python post.py scan   → 只更新 pages.json，打印是否有变化
#       python post.py stamp  → 生成成品
import json, re, sys
from pathlib import Path
import pymupdf

here = Path(__file__).parent
out = here / "out"
raw = out / "raw.pdf"
FONT = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
MK = re.compile(r"@@([^@\s]+)@@")


def find_markers(doc):
    # Chrome 把被 <a href="#id"> 链接到的 id 写成 PDF 命名目标，直接读它们所在页
    return {k: v["page"] + 1 for k, v in doc.resolve_names().items()}, []


def scan():
    doc = pymupdf.open(raw)
    pages, _ = find_markers(doc)
    f = out / "pages.json"
    old = json.loads(f.read_text()) if f.exists() else {}
    f.write_text(json.dumps(pages, ensure_ascii=False, indent=0))
    changed = old != pages
    print(f"pages={len(doc)} markers={len(pages)} changed={changed}")
    return changed


def stamp():
    doc = pymupdf.open(raw)
    pages, rects = find_markers(doc)

    html = (out / "handbook.html").read_text(encoding="utf-8")
    chaps = []  # (起始页, 书签名, 页眉标题)
    for m in re.finditer(r'<h1 class="chap" data-tab="([^"]+)" id="([^"]+)"[^>]*>([\s\S]*?)</h1>', html):
        tab, cid, inner = m.groups()
        inner = re.sub(r'<span class="mk">[^<]*</span>', "", inner)
        inner = re.sub(r'<span class="katex-mathml">[\s\S]*?</span>', "", inner)
        inner = re.sub(r'<span class="(en|no)">[\s\S]*?</span>', "", inner)
        title = re.sub(r"<[^>]+>", "", inner).strip()
        title = re.sub(r"\s+", " ", title)
        chaps.append((pages.get(cid, 1), tab, title))
    chaps.sort()
    tabs = [c[1] for c in chaps]

    W, H = pymupdf.paper_size("a4")
    zh = pymupdf.Font(fontfile=FONT)
    top, bot = 50, H - 48
    slot = (bot - top) / max(len(tabs), 1)
    gray, dark = (0.35, 0.35, 0.35), (0.1, 0.1, 0.1)

    def put(page, x, y, text, fs, color, align="l"):
        w = zh.text_length(text, fontsize=fs)
        if align == "r":
            x -= w
        elif align == "c":
            x -= w / 2
        page.insert_text((x, y), text, fontname="zh", fontsize=fs, color=color)

    for pno, page in enumerate(doc, 1):
        cur = None
        for c in chaps:
            if c[0] <= pno:
                cur = c
        if pno == 1 or cur is None:
            continue
        odd = pno % 2 == 1
        page.insert_font(fontname="zh", fontfile=FONT)
        page.draw_line((48, 38), (W - 48, 38), color=(0.45, 0.45, 0.45), width=0.5)
        left, right = "CM5235 开卷知识点汇总", f"{cur[1]} · {cur[2]}" if cur[1] not in cur[2] else cur[2]
        if odd:
            put(page, 48, 34, left, 8, gray)
            put(page, W - 48, 34, right, 8.5, dark, "r")
            put(page, W - 48, H - 24, str(pno), 9, dark, "r")
        else:
            put(page, 48, 34, right, 8.5, dark)
            put(page, W - 48, 34, left, 8, gray, "r")
            put(page, 48, H - 24, str(pno), 9, dark)
        # 外侧书签：所有讲次排成一列，当前讲次涂黑
        for i, t in enumerate(tabs):
            y0 = top + i * slot + 2
            y1 = y0 + slot - 4
            x0, x1 = (W - 22, W) if odd else (0, 22)
            r = pymupdf.Rect(x0, y0, x1, y1)
            if t == cur[1]:
                page.draw_rect(r, color=None, fill=(0, 0, 0))
                col = (1, 1, 1)
            else:
                page.draw_rect(r, color=(0.6, 0.6, 0.6), fill=(0.93, 0.93, 0.93), width=0.4)
                col = (0.3, 0.3, 0.3)
            # 汉字竖排逐字写；拉丁字母+数字（如 L3）作为一个整体横写
            items = [t] if t.isascii() else list(t)
            fs = 9
            step = fs * 1.15
            ystart = (y0 + y1) / 2 - step * len(items) / 2 + fs * 0.85
            for k, c in enumerate(items):
                put(page, (x0 + x1) / 2, ystart + k * step, c, fs, col, "c")
    doc.set_toc([[1 if c[1] else 1, f"{c[1]}  {c[2]}", c[0]] for c in chaps])
    dst = here.parent / "CM5235_开卷知识点汇总_L1-L6.pdf"
    doc.save(dst, garbage=4, deflate=True)
    print(dst, len(doc))


if __name__ == "__main__":
    {"scan": scan, "stamp": stamp}[sys.argv[1]]()
