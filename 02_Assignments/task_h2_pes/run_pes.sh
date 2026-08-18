#!/bin/bash
# H2 势能面扫描：RHF 和 UHF 各跑一遍，相同基组
# 基于讲义 p.101 的循环，但 R 列表已扩展到 0.5-10 Angstrom / 25 个点
# （讲义原版只到 1.25 Angstrom / 16 点，不满足题目要求）

# 25 个点：键长附近密，解离区疏。0.74 是 H2 的实验平衡键长
R_LIST="0.50 0.60 0.70 0.74 0.80 0.90 1.00 1.10 1.20 1.30 1.40 1.50 1.60 1.80 2.00 2.25 2.50 2.75 3.00 3.50 4.00 5.00 6.00 8.00 10.00"

for METHOD in RHF UHF ; do
    TEMPLATE=H2_${METHOD}.gjf
    echo "=============== $METHOD ==============="

    for R in $R_LIST ; do
        JOB=${METHOD}_R_${R}
        sed -e "s/DISTANCE/$R/g" $TEMPLATE > ${JOB}.gjf
        g16 < ${JOB}.gjf > ${JOB}.log
        echo "  R = $R  done"
    done
done

echo "全部计算完成，运行 bash extract.sh 提取数据"
