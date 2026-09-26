#!/bin/bash
# Ex4 一键提交：四个方法各交一个 TD-DFT 作业。
# 在 atlas9 登录节点上运行：  bash Ex4_TDDFT/ex4_submit_4_methods.sh
# 只交某一个方法：           bash Ex4_TDDFT/ex4_submit_4_methods.sh B3LYP_water
#
# 每个方法按 Ex1 的情况自动处理：
#   Ex1 已算完且无虚频      -> 直接提交
#   Ex1 还在排队或正在算    -> 提交并挂 PBS 依赖，等 Ex1 成功结束后自动开始（Ex1 失败就不跑）
#   Ex1 既没在跑也没有结果  -> 跳过并提示

cd "$(dirname "$0")" || exit 1
METHODS=${*:-"PBE_gas B3LYP_gas PBE_water B3LYP_water"}

for m in $METHODS; do
    if [ ! -f "$m/ex4_tddft_$m.inp" ]; then
        echo "!!! 没有 $m/ex4_tddft_$m.inp，跳过"
        continue
    fi
    geo="../Ex1_2Cl_phenol/$m/ex1_optimized_geometry_$m.xyz"
    ex1_job=$(qselect -u "$USER" -N "ex1_$m" 2>/dev/null | head -n 1)
    if [ -f "$geo" ]; then
        dep=""
        note="Ex1 已算完，直接提交"
    elif [ -n "$ex1_job" ]; then
        dep="-W depend=afterok:$ex1_job"
        note="等 Ex1 作业 $ex1_job 结束后自动开始"
    else
        echo "!!! ex4_$m：Ex1 的 $m 既没在跑也没有优化结构（可能有虚频），跳过"
        continue
    fi
    id=$(qsub -N "ex4_$m" -v METHOD="$m" -o "$m/ex4_pbs_log_$m.txt" $dep ex4_run_one_method.pbs)
    echo "ex4_$m -> $id    （$note）"
done
echo "用 qstat -u \$USER 看排队情况；挂了依赖的作业状态显示为 H（等待中）"
