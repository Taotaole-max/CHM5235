#!/bin/bash
# Ex5 一键提交：非相对论、DKH、ZORA 三种处理各交一个作业，互不依赖，同时排队。
# 在 atlas9 登录节点上运行：  bash Ex5_Cu2_BSDFT/ex5_submit_3_methods.sh
# 只交某一个：               bash Ex5_Cu2_BSDFT/ex5_submit_3_methods.sh ZORA
# 交加密格点的复核版：       VERIFY=1 bash Ex5_Cu2_BSDFT/ex5_submit_3_methods.sh

cd "$(dirname "$0")" || exit 1
METHODS=${*:-"nonrelativistic DKH ZORA"}

for m in $METHODS; do
    if [ "${VERIFY:-0}" = 1 ]; then
        d="verify_$m"; inp="$d/ex5_bsdft_verify_$m.inp"; tag="ex5v"
    else
        d="$m"; inp="$d/ex5_bsdft_$m.inp"; tag="ex5"
    fi
    if [ ! -f "$inp" ]; then
        echo "!!! 没有 $inp，跳过"
        continue
    fi
    # 作业名缩写：部分 PBS 版本限制作业名不超过 15 个字符
    name="${tag}_${m/nonrelativistic/nonrel}"
    id=$(qsub -N "$name" -v METHOD="$m",VERIFY="${VERIFY:-0}" -o "$d/ex5_pbs_log_$(basename $d).txt" ex5_run_one_method.pbs)
    echo "$name -> $id"
done
echo "用 qstat -u \$USER 看排队情况"
