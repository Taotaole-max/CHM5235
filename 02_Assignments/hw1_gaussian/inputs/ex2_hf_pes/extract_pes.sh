#!/bin/bash
# 从四个 scan 的 .log 里提取 (R, E)，输出 CSV，供 Python/Origin 画图。
# 用法：bash extract_pes.sh   （在四个 .log 所在目录）

set -e

emit () {   # $1 = log 文件  $2 = 能量关键字的 grep 模式  $3 = 输出名
  log="$1"; pat="$2"; out="$3"
  [ -f "$log" ] || { echo "跳过（没找到）：$log"; return; }
  # scan 每个点：Gaussian 先打印 "Scan  ...  R  =  x.xx"，随后是该点的能量
  awk -v pat="$pat" '
    /^ *!? *R +[0-9]/            { r=$3 }
    / R *= *[0-9]/               { for(i=1;i<=NF;i++) if($i=="R"){ r=$(i+2) } }
    $0 ~ pat {
      # 取该行最后一个看起来像能量的数
      for(i=NF;i>=1;i--) if($i ~ /-?[0-9]+\.[0-9]+/){ e=$i; break }
      if(r!="") { print r "," e; r="" }
    }
  ' "$log" > "$out"
  echo "写出 $out  （$(wc -l < "$out") 个点）"
}

emit hf_scan_uhf.log     'SCF Done'    pes_uhf.csv
emit hf_scan_ub3lyp.log  'SCF Done'    pes_ub3lyp.csv
emit hf_scan_uccsd.log   'E\(Corr\)'   pes_uccsd.csv        # 或搜 'Wavefunction amplitudes' 附近的 'ECCSD'
emit hf_scan_uccsdt.log  'CCSD\(T\)='  pes_uccsdt.csv

cat > plot_pes.py <<'PY'
import pandas as pd, matplotlib.pyplot as plt
HARTREE2KJ = 2625.4996
files = {"UHF":"pes_uhf.csv","UB3LYP":"pes_ub3lyp.csv",
         "UCCSD":"pes_uccsd.csv","UCCSD(T)":"pes_uccsdt.csv"}
fig, ax = plt.subplots(figsize=(6,4.2))
summary = []
for name, f in files.items():
    try:
        d = pd.read_csv(f, names=["R","E"]).sort_values("R")
    except Exception as ex:
        print("skip", f, ex); continue
    Emin = d["E"].min(); Rmin = d.loc[d["E"].idxmin(),"R"]
    Ediss = d[d["R"] > 9.0]["E"].mean()          # 解离极限 ~ R>9 Å 的平均
    De = (Ediss - Emin) * HARTREE2KJ
    ax.plot(d["R"], (d["E"]-Emin)*HARTREE2KJ, label=name)
    summary.append((name, Rmin, De))
ax.set_xlabel(r"$R_{\rm H-F}$ / Å"); ax.set_ylabel(r"$E - E_{\min}$ / kJ mol$^{-1}$")
ax.set_xlim(0.5, 6); ax.set_ylim(-20, 700); ax.legend(); fig.tight_layout()
fig.savefig("ex2_pes.png", dpi=200)
print(f"{'method':10s} {'R_e / Å':>10s} {'D_e / kJ/mol':>14s}")
for n,r,de in summary: print(f"{n:10s} {r:10.3f} {de:14.1f}")
print("实验 BDE(H-F) = 568.6 kJ/mol")
PY
echo "已生成 plot_pes.py —— 本地跑： python plot_pes.py"
