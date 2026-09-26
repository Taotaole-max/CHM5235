# ORCA 环境设置，每道题的提交脚本都会 source 这个文件。
# 集群上的 ORCA 在哪里，只在这里改一次。
#
# 两种装法二选一：
#   1) 集群有 ORCA 模块：填 ORCA_MODULE（module avail 查到的全名，例如 ORCA/5.0.4）。
#      留空的话会自动在 module avail 里找名字带 orca 的最后一个。
#   2) 按 Lecture 02 p.95 自己装在 home 里：填 ORCA_DIR，ORCA_MODULE 就不用管了。
#      例：ORCA_DIR=$HOME/software/orca_5_0_3_linux_x86-64_openmpi411

# 2026-09-19 查过 atlas9：有 orca/4.2、orca/5.0（实际 5.0.0）、orca/5.2（实际 5.0.2）。
# 固定用 orca/5.2，即 ORCA 5.0.2；ORCA 目录里自带 otool_xtb，Ex6b 的 xtb 也能用。
ORCA_MODULE="orca/5.2"
ORCA_DIR=""

if [ -n "$ORCA_DIR" ]; then
    export PATH="$ORCA_DIR:$PATH"
    export LD_LIBRARY_PATH="$ORCA_DIR:$LD_LIBRARY_PATH"
else
    if [ -z "$ORCA_MODULE" ]; then
        ORCA_MODULE=$(module -t avail 2>&1 | grep -i 'orca' | grep -v ':$' | sed 's/(default)//' | tail -n 1)
    fi
    if [ -n "$ORCA_MODULE" ]; then
        module load "$ORCA_MODULE"
    fi
fi

# 单核跑，ORCA 不走 MPI；xtb 用 OpenMP，线程数也限制成 1，免得超出申请的核数
export OMP_NUM_THREADS=1

ORCA_EXE=$(command -v orca)
if [ -z "$ORCA_EXE" ]; then
    echo "!!! 找不到 orca。先在登录节点跑 bash 01_cluster_setup/check_orca_on_cluster.sh，按结果填这个文件" >&2
    return 1 2>/dev/null || exit 1
fi
echo ">>> ORCA_MODULE=${ORCA_MODULE:-无}  ORCA_EXE=$ORCA_EXE"
