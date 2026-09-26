"""Ex5 结果提取：三种相对论处理（以及加密格点的复核版）的 BS-DFT 结果。

用法：D:\\venvs\\cm5235_hw2\\Scripts\\python ex5_extract_J.py
读取：../<方法>/ex5_bsdft_<方法>.out 和 ../verify_<方法>/ex5_bsdft_verify_<方法>.out（有才读）
写出：ex5_results_table.md（给人看的核对表）
报告脚本 03_report_word/scripts/make_ex5_word.py 直接 import 这里的 parse()。

ORCA 的约定是 H = −2J·S_A·S_B，J < 0 反铁磁。三个公式里 J(3) 是 Yamaguchi 式
J = (E_BS − E_HS)/(⟨S²⟩_HS − ⟨S²⟩_BS)，讲义 L05 用的就是这个。
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
EX5 = HERE.parent
METHODS = ["nonrelativistic", "DKH", "ZORA"]
LABELS = {"nonrelativistic": "non-relativistic", "DKH": "DKH", "ZORA": "ZORA"}

# 题目之外补做的敏感性计算：看 J 的符号是被什么决定的
EXTRA = {"TPSSh":       "TPSSh/def2-SVP, non-rel. (10% HF exchange)",
         "PBE0":        "PBE0/def2-SVP, non-rel. (25% HF exchange)",
         "TZVP_nonrel": "B3LYP/def2-TZVP, non-rel.",
         "TZVP_DKH":    "B3LYP/DKH-def2-TZVP, DKH",
         "TZVP_ZORA":   "B3LYP/ZORA-def2-TZVP, ZORA"}


def out_path(method, verify=False):
    if verify:
        return EX5 / f"verify_{method}" / f"ex5_bsdft_verify_{method}.out"
    return EX5 / method / f"ex5_bsdft_{method}.out"   # 对 EXTRA 里的文件夹也适用


def parse(method, verify=False):
    p = out_path(method, verify)
    if not p.exists():
        return None
    out = p.read_text(errors="replace")
    if "ORCA TERMINATED NORMALLY" not in out:
        return None
    blk = out[out.rfind("BROKEN SYMMETRY MAGNETIC COUPLING ANALYSIS"):]
    g = lambda pat: float(re.search(pat, blk).group(1))
    r = dict(
        s2_hs=g(r"<S\*\*2>\(High-Spin\)\s*=\s*([\d.]+)"),
        s2_bs=g(r"<S\*\*2>\(BrokenSym\)\s*=\s*([\d.]+)"),
        e_hs=g(r"E\(High-Spin\)\s*=\s*(-?[\d.]+) Eh"),
        e_bs=g(r"E\(BrokenSym\)\s*=\s*(-?[\d.]+) Eh"),
        dE_cm=g(r"E\(High-Spin\)-E\(BrokenSym\)=\s*-?[\d.]+ eV\s+(-?[\d.]+) cm"),
        j1=g(r"J\(1\)\s*=\s*(-?[\d.]+) cm"),
        j2=g(r"J\(2\)\s*=\s*(-?[\d.]+) cm"),
        j3=g(r"J\(3\)\s*=\s*(-?[\d.]+) cm"),
    )
    # 两个态里 Cu 上的 Mulliken 自旋布居：确认破缺对称态确实是"一上一下"
    spins = []
    for m in re.finditer(r"MULLIKEN ATOMIC CHARGES AND SPIN POPULATIONS(.*?)Sum of atomic charges", out, re.S):
        cu = re.findall(r"^\s*\d+ Cu\s*:\s*-?[\d.]+\s+(-?[\d.]+)", m.group(1), re.M)
        if len(cu) == 2:
            spins.append((float(cu[0]), float(cu[1])))
    r["spin_hs"], r["spin_bs"] = (spins[0], spins[-1]) if len(spins) >= 2 else (None, None)
    r["walltime"] = re.search(r"TOTAL RUN TIME:.*?(\d+) hours (\d+) minutes", out)
    r["hours"] = (int(r["walltime"].group(1)) + int(r["walltime"].group(2)) / 60) if r["walltime"] else None
    return r


def main():
    L = ["# Ex5 BS-DFT results (B3LYP, SVP-level basis, charge −2, HS multiplicity 3)\n",
         "ORCA convention H = −2J·S_A·S_B, so J < 0 = antiferromagnetic.\n",
         "| Run | E(HS) / Eh | E(BS) / Eh | ⟨S²⟩HS | ⟨S²⟩BS | E(HS)−E(BS) / cm⁻¹ | J(1) | J(2) | J(3) | Cu spins (HS / BS) |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for verify, names in [(False, METHODS), (True, METHODS), (False, list(EXTRA))]:
        for m in names:
            r = parse(m, verify)
            if not r:
                continue
            tag = LABELS.get(m, EXTRA.get(m, m)) + (" (DefGrid3, VeryTightSCF)" if verify else "")
            sp = (f"{r['spin_hs'][0]:+.2f}/{r['spin_hs'][1]:+.2f} · {r['spin_bs'][0]:+.2f}/{r['spin_bs'][1]:+.2f}"
                  if r["spin_hs"] else "–")
            L.append(f"| {tag} | {r['e_hs']:.6f} | {r['e_bs']:.6f} | {r['s2_hs']:.4f} | {r['s2_bs']:.4f} | "
                     f"{r['dE_cm']:+.1f} | {r['j1']:+.2f} | {r['j2']:+.2f} | {r['j3']:+.2f} | {sp} |")
    (HERE / "ex5_results_table.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
