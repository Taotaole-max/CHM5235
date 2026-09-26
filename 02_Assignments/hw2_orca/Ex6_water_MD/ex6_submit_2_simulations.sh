#!/bin/bash
# Ex6 一键提交：(a) DFT 和 (b) XTB 两条 MD 轨迹各交一个作业，互不依赖，同时排队。
# 在 atlas9 登录节点上运行：  bash Ex6_water_MD/ex6_submit_2_simulations.sh
# 只交其中一个：             bash Ex6_water_MD/ex6_submit_2_simulations.sh 6b_XTB

cd "$(dirname "$0")" || exit 1
SIMS=${*:-"6a_DFT_PBE 6b_XTB"}

for s in $SIMS; do
    case "$s" in
        6a_DFT_PBE) name=ex6a_md_DFT; res="select=1:ncpus=1:mem=10gb" ;;   # DFT 需要内存
        6b_XTB)     name=ex6b_md_XTB; res="select=1:ncpus=1:mem=4gb"  ;;   # xtb 很省内存，申请少一点排得快
        *) echo "!!! 不认识 $s，只能是 6a_DFT_PBE 或 6b_XTB"; continue ;;
    esac
    id=$(qsub -N "$name" -v SIM="$s" -l "$res" -o "$s/ex6_pbs_log_$s.txt" ex6_run_one_simulation.pbs)
    echo "$name -> $id"
done
echo "用 qstat -u \$USER 看排队情况"
