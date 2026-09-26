"""Ex1 结果提取：从四个方法的 ORCA 输出里取出题目要的五项数据，生成对比表。

用法（在本机）：python ex1_extract_results.py
读取：../<方法>/ex1_optfreq_<方法>.out
写出：ex1_results_tables.md（同一文件夹）

还没算完的方法在表里显示为 "—"，所以可以边算边跑。
表格用英文，因为要直接搬进英文报告。
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
EX1 = HERE.parent
METHODS = ["PBE_gas", "B3LYP_gas", "PBE_water", "B3LYP_water"]
LABELS = {"PBE_gas": "PBE (gas)", "B3LYP_gas": "B3LYP (gas)",
          "PBE_water": "PBE (water)", "B3LYP_water": "B3LYP (water)"}
HARTREE_TO_KCAL = 627.509474


def last_block(lines, header):
    """返回最后一次出现 header 的行号，没有就返回 None。"""
    idx = [i for i, l in enumerate(lines) if header in l]
    return idx[-1] if idx else None


def parse_charges(lines, header):
    i = last_block(lines, header)
    out = []
    for l in lines[i + 2:]:
        m = re.match(r"^\s*(\d+)\s+([A-Za-z]+)\s*:\s+(-?\d+\.\d+)", l)
        if not m:
            break
        out.append(float(m.group(3)))
    return out


def parse_geometry(lines):
    """最后一次 CARTESIAN COORDINATES (ANGSTROEM)，即优化好的结构。"""
    i = last_block(lines, "CARTESIAN COORDINATES (ANGSTROEM)")
    atoms = []
    for l in lines[i + 2:]:
        p = l.split()
        if len(p) != 4:
            break
        atoms.append((p[0], tuple(float(v) for v in p[1:])))
    return atoms


def parse_orbitals(lines):
    """α 轨道（SPIN UP）；闭壳层 UKS 下 β 与 α 相同。"""
    i = last_block(lines, "ORBITAL ENERGIES")
    orbs, started = [], False
    for l in lines[i:]:
        m = re.match(r"^\s*(\d+)\s+(\d\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", l)
        if m:
            started = True
            orbs.append((int(m.group(1)), float(m.group(2)), float(m.group(4))))
        elif started:
            break  # SPIN UP 段结束
    homo = max(o for o in orbs if o[1] > 0.5)
    lumo = min((o for o in orbs if o[1] < 0.5), key=lambda o: o[0])
    return homo, lumo


def parse_frequencies(lines):
    i = last_block(lines, "VIBRATIONAL FREQUENCIES")
    freqs = []
    for l in lines[i:]:
        m = re.match(r"^\s*(\d+):\s+(-?\d+\.\d+) cm\*\*-1", l)
        if m:
            freqs.append((int(m.group(1)), float(m.group(2))))
        elif freqs and l.strip() == "":
            break
    return freqs


def parse_entropy(lines):
    def eh(key):
        # 要求带 "... 数字 Eh"，避开 "Vibrational entropy computed according to ..." 这种说明行
        for l in lines:
            m = re.match(re.escape(key) + r"\s+\.\.\.\s+(-?\d+\.\d+) Eh", l)
            if m:
                return float(m.group(1))
        return None
    T = float(re.search(r"(\d+\.\d+) K", next(l for l in lines if l.startswith("Temperature"))).group(1))
    parts = {k: eh(k + " entropy") for k in ["Electronic", "Vibrational", "Rotational", "Translational"]}
    total = eh("Final entropy term")
    return T, parts, total


def parse(method):
    out = EX1 / method / f"ex1_optfreq_{method}.out"
    if not out.exists():
        return None
    text = out.read_text(errors="replace")
    if "ORCA TERMINATED NORMALLY" not in text:
        return None
    lines = text.splitlines()
    r = {}
    r["geom"] = parse_geometry(lines)
    r["mulliken"] = parse_charges(lines, "MULLIKEN ATOMIC CHARGES")
    r["loewdin"] = parse_charges(lines, "LOEWDIN ATOMIC CHARGES")
    r["homo"], r["lumo"] = parse_orbitals(lines)
    r["dipole"] = float(re.search(r"Magnitude \(Debye\)\s+:\s+(-?\d+\.\d+)",
                                  text[text.rfind("DIPOLE MOMENT"):]).group(1))
    r["freqs"] = parse_frequencies(lines)
    r["T"], r["S_parts"], r["TS"] = parse_entropy(lines)
    r["imag"] = [f for _, f in r["freqs"] if f < 0]
    return r


def atom_labels(geom):
    """给 13 个原子起化学名：C1 连 OH，C2 连 Cl，沿环编号；H 按所连的原子命名。"""
    import math
    d = lambda a, b: math.dist(geom[a][1], geom[b][1])
    n = len(geom)
    O = next(i for i in range(n) if geom[i][0] == "O")
    Cl = next(i for i in range(n) if geom[i][0] == "Cl")
    C = [i for i in range(n) if geom[i][0] == "C"]
    c1 = min(C, key=lambda i: d(i, O))
    c2 = min(C, key=lambda i: d(i, Cl))
    ring = [c1, c2]
    while len(ring) < 6:  # 沿着环往下走
        nxt = min((i for i in C if i not in ring), key=lambda i: d(i, ring[-1]))
        ring.append(nxt)
    lab = {c: f"C{k + 1}" for k, c in enumerate(ring)}
    lab[O], lab[Cl] = "O", "Cl"
    for h in (i for i in range(n) if geom[i][0] == "H"):
        host = min((i for i in range(n) if geom[i][0] != "H"), key=lambda i: d(h, i))
        lab[h] = "H(O)" if host == O else f"H({lab[host]})"
    order = [Cl, O, c1] + ring[1:] + sorted((i for i in range(n) if geom[i][0] == "H"),
                                            key=lambda h: (lab[h] != "H(O)", lab[h]))
    return lab, order


def fmt(x, nd):
    return "—" if x is None else f"{x:.{nd}f}"


def main():
    res = {m: parse(m) for m in METHODS}
    done = [m for m in METHODS if res[m]]
    if not done:
        print("还没有算完的方法")
        return
    lab, order = atom_labels(res[done[0]]["geom"])
    L = []
    L.append("# Ex1 results: 2-chlorophenol, UKS / def2-TZVP\n")
    L.append("Finished: " + ", ".join(LABELS[m] for m in done)
             + ("" if len(done) == 4 else "  (other columns still running)") + "\n")

    # 虚频检查
    for m in done:
        if res[m]["imag"]:
            L.append(f"**WARNING {LABELS[m]}: imaginary frequencies {res[m]['imag']}**\n")

    # (a) 电荷
    L.append("## (a) Atomic charges (e)\n")
    L.append("Atom numbering: C1 bears OH, C2 bears Cl; H(Cn) is the H on Cn.\n")
    head = "| Atom | " + " | ".join(f"{LABELS[m]} Mulliken | {LABELS[m]} Löwdin" for m in METHODS) + " |"
    L += [head, "|" + "---|" * (1 + 2 * len(METHODS))]
    for a in order:
        row = [lab[a]]
        for m in METHODS:
            r = res[m]
            row += [fmt(r and r["mulliken"][a], 4), fmt(r and r["loewdin"][a], 4)]
        L.append("| " + " | ".join(row) + " |")
    L.append("")

    # (b) 频率
    L.append("## (b) Vibrational frequencies (cm⁻¹)\n")
    L.append("ORCA mode numbers; modes 0–5 are translations/rotations (0 cm⁻¹) and are omitted.\n")
    L += ["| Mode | " + " | ".join(LABELS[m] for m in METHODS) + " |", "|" + "---|" * (1 + len(METHODS))]
    nmodes = len(res[done[0]]["freqs"])
    for k in range(6, nmodes):
        L.append(f"| {k} | " + " | ".join(fmt(res[m] and res[m]["freqs"][k][1], 2) for m in METHODS) + " |")
    L.append("")

    # (c) 偶极矩
    L.append("## (c) Electric dipole moment\n")
    L += ["| | " + " | ".join(LABELS[m] for m in METHODS) + " |", "|" + "---|" * (1 + len(METHODS))]
    L.append("| μ (Debye) | " + " | ".join(fmt(res[m] and res[m]["dipole"], 3) for m in METHODS) + " |")
    L.append("")

    # (d) 熵
    T = res[done[0]]["T"]
    L.append(f"## (d) Entropy at {T:.2f} K\n")
    L.append("ORCA prints T·S; S = (T·S)/T. Vibrational part uses Grimme's quasi-RRHO (ORCA default).\n")
    L += ["| | " + " | ".join(LABELS[m] for m in METHODS) + " |", "|" + "---|" * (1 + len(METHODS))]
    for part in ["Electronic", "Vibrational", "Rotational", "Translational"]:
        L.append(f"| S({part[:5].lower()}) (cal mol⁻¹ K⁻¹) | " + " | ".join(
            fmt(res[m] and res[m]["S_parts"][part] * HARTREE_TO_KCAL * 1000 / T, 2) for m in METHODS) + " |")
    L.append("| **S total (cal mol⁻¹ K⁻¹)** | " + " | ".join(
        fmt(res[m] and res[m]["TS"] * HARTREE_TO_KCAL * 1000 / T, 2) for m in METHODS) + " |")
    L.append("| T·S (kcal mol⁻¹) | " + " | ".join(
        fmt(res[m] and res[m]["TS"] * HARTREE_TO_KCAL, 2) for m in METHODS) + " |")
    L.append("")

    # (e) HOMO-LUMO
    L.append("## (e) HOMO–LUMO gap\n")
    L += ["| | " + " | ".join(LABELS[m] for m in METHODS) + " |", "|" + "---|" * (1 + len(METHODS))]
    L.append("| HOMO (eV) | " + " | ".join(fmt(res[m] and res[m]["homo"][2], 3) for m in METHODS) + " |")
    L.append("| LUMO (eV) | " + " | ".join(fmt(res[m] and res[m]["lumo"][2], 3) for m in METHODS) + " |")
    L.append("| **Gap (eV)** | " + " | ".join(
        fmt(res[m] and res[m]["lumo"][2] - res[m]["homo"][2], 3) for m in METHODS) + " |")
    L.append("")
    homo_idx = res[done[0]]["homo"][0]
    L.append(f"HOMO = orbital {homo_idx}, LUMO = orbital {homo_idx + 1} (ORCA numbering, α spin; "
             "β orbitals are identical for this closed-shell molecule).\n")

    (HERE / "ex1_results_tables.md").write_text("\n".join(L), encoding="utf-8")
    print("写出", HERE / "ex1_results_tables.md", "；已完成：", done)


if __name__ == "__main__":
    main()
