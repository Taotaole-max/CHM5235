#!/bin/bash
# 在 atlas9 登录节点上跑一次：  bash 01_cluster_setup/check_orca_on_cluster.sh
# 只查询不计算，几秒钟结束。把输出贴回来就能确定 orca_env_settings.sh 该怎么填。

echo "===== 1. module avail 里带 orca / xtb 的模块"
module -t avail 2>&1 | grep -i -E 'orca|xtb'

echo "===== 2. home 里自己装的 ORCA"
ls -d "$HOME"/software/orca* "$HOME"/orca* 2>/dev/null

echo "===== 3. 按 orca_env_settings.sh 当前设置加载"
cd "$(dirname "$0")"
source ./orca_env_settings.sh || exit 1
ORCA_BIN_DIR=$(dirname "$ORCA_EXE")
ls "$ORCA_BIN_DIR" | grep -E '^orca$|^orca_2mkl$|^orca_pltvib$|^orca_mapspc$|^otool_xtb$'

echo "===== 4. ORCA 版本（看安装路径里的版本号；登录节点上不跑 orca 本身）"
readlink -f "$ORCA_EXE"

echo "===== 5. Ex6b 要用 xtb：ORCA 目录里有没有 otool_xtb"
if [ -x "$ORCA_BIN_DIR/otool_xtb" ]; then
    echo "有 otool_xtb，Ex6b 可以直接跑"
else
    echo "没有 otool_xtb —— Ex6b 暂时跑不了，把这段输出贴回来再处理"
fi
