#!/bin/bash
# Ex1 一键提交：四个方法各交一个作业，并行排队。
# 在 atlas9 登录节点上运行：  bash Ex1_2Cl_phenol/ex1_submit_4_methods.sh
# 只重交某一个方法：         bash Ex1_2Cl_phenol/ex1_submit_4_methods.sh B3LYP_water

cd "$(dirname "$0")" || exit 1
METHODS=${*:-"PBE_gas B3LYP_gas PBE_water B3LYP_water"}

for m in $METHODS; do
    if [ ! -f "$m/ex1_optfreq_$m.inp" ]; then
        echo "!!! 没有 $m/ex1_optfreq_$m.inp，跳过"
        continue
    fi
    # 作业日志也放进对应子文件夹
    id=$(qsub -N "ex1_$m" -v METHOD="$m" -o "$m/ex1_pbs_log_$m.txt" ex1_run_one_method.pbs)
    echo "ex1_$m -> $id"
done
echo "用 qstat -u \$USER 看排队情况"
