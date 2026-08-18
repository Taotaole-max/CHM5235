#!/bin/bash
# 从 .log 里提取 R / 能量 / <S^2>，生成可直接画图的两列数据

for METHOD in RHF UHF ; do
    OUT=results_${METHOD}.dat
    echo "# R(Angstrom)   E(Hartree)" > $OUT

    for f in $(ls ${METHOD}_R_*.log | sort -t_ -k3 -g) ; do
        R=$(echo $f | sed -e "s/${METHOD}_R_//" -e 's/\.log//')
        # 取最后一个 SCF Done 的能量（第 5 个字段）
        E=$(grep 'SCF Done' $f | tail -1 | awk '{print $5}')
        if [ -n "$E" ] ; then
            echo "$R   $E" >> $OUT
        else
            echo "警告: $f 里没有 SCF Done —— 这个点没收敛" >&2
        fi
    done
    echo "生成 $OUT ($(($(wc -l < $OUT) - 1)) 个点)"
done

# UHF 的自旋污染：<S^2> 从 0 涨到约 1，是报告里的关键图
S2OUT=s2_UHF.dat
echo "# R(Angstrom)   <S^2>" > $S2OUT
for f in $(ls UHF_R_*.log | sort -t_ -k3 -g) ; do
    R=$(echo $f | sed -e 's/UHF_R_//' -e 's/\.log//')
    S2=$(grep 'S\*\*2' $f | tail -1 | sed -e 's/.*S\*\*2 *= *//' -e 's/,.*//' | awk '{print $1}')
    [ -n "$S2" ] && echo "$R   $S2" >> $S2OUT
done
echo "生成 $S2OUT"

echo ""
echo "参考：单个 H 原子的能量（UHF/6-31G(d,p)）用来验证解离极限"
echo "  解离时 UHF 应趋近 2 x E(H)，RHF 会明显偏高"
