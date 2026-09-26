#!/bin/bash
# 完整构建：两遍排版回填页码，再盖页眉和书签。成品：../CM5235_开卷知识点汇总_L1-L6.pdf
set -e
cd "$(dirname "$0")"
export NODE_PATH=/opt/node22/lib/node_modules
for i in 1 2 3; do
  node build.mjs
  python3 post.py scan | tee /dev/stderr | grep -q "changed=False" && break
done
python3 post.py stamp
