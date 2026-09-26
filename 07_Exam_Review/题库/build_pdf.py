# 把 *.src.html 里的图片转成 base64 内嵌，生成单文件 HTML，再用 Edge 无头打印成 PDF
# 用法：python build_pdf.py CM5235_题库_L1-L2.src.html
import base64, re, subprocess, sys, time
from pathlib import Path

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
here = Path(__file__).parent
src = here / sys.argv[1]
stem = src.name.replace(".src.html", "")
html = src.read_text(encoding="utf-8")

def inline(m):
    p = here / m.group(1)
    return 'src="data:image/png;base64,' + base64.b64encode(p.read_bytes()).decode() + '"'

html = re.sub(r'src="(img/[^"]+\.png)"', inline, html)
out_html = here / f"{stem}.html"
out_html.write_text(html, encoding="utf-8")

pdf = here / f"{stem}.pdf"
if pdf.exists():
    pdf.unlink()
subprocess.run([EDGE, "--headless=new", "--no-pdf-header-footer", "--virtual-time-budget=60000",
                f"--print-to-pdf={pdf}", out_html.as_uri()], check=False)
# Edge 可能先返回、后台继续写文件：等文件大小稳定
last, stable = -1, 0
for _ in range(120):
    time.sleep(1)
    size = pdf.stat().st_size if pdf.exists() else -1
    stable = stable + 1 if size == last and size > 0 else 0
    last = size
    if stable >= 3:
        break
print(pdf, last)
