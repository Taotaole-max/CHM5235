# Gaussian 踩过的坑

> 每遇到一个新问题就往下加一行。这个文件的价值随时间指数增长。

## 已知高频坑（预填，遇到时对照）

| 现象 | 原因 | 解决方法 |
|---|---|---|
| 作业秒退，`.log` 几乎是空的 | 输入文件**结尾少了空行** | `.gjf` 最后必须有一个空行 |
| `End of file in ZSymb` | 坐标段和结尾之间空行数量不对 | 检查五段结构，段间恰好一个空行 |
| `Out-of-memory` / 作业被杀 | `%mem` ≥ PBS 申请的 `mem` | `%mem` 要比 PBS 的 `mem` 小 1–2GB |
| `galloc: could not allocate memory` | 同上，或 `%nprocshared` 大于实际分到的核数 | `%nprocshared` 要 = PBS 的 `ncpus` |
| 磁盘写满 / `Erroneous write` | `.rwf` 临时文件写在了家目录 | 脚本里设 `export GAUSS_SCRDIR=` 指向 scratch |
| 优化跑满步数不收敛 | 初始结构太差，或用了平坦的势能面 | 加 `opt=(calcfc,maxcycles=200)`；先用小基组预优化 |
| 优化"成功"但有虚频 | 收敛到了鞍点 | 沿虚频模式微扰结构后重新优化 |
| 频率结果无意义 | freq 用的方法/基组和 opt 不一致 | 两步必须完全同一套方法和基组 |
| 开壳层结果不对，⟨S²⟩ 远大于理论值 | 自旋污染 | 加 `stable=opt` 检查波函数稳定性 |
| 阴离子能量异常高 | 基组缺弥散函数 | 用带 `+` 的基组 |
| 本地 GaussView 打不开集群下载的 `.chk` | `.chk` 是二进制，跨平台不通用 | 集群上 `formchk mol.chk mol.fchk`，下载 `.fchk` |
| 脚本报 `bad interpreter: /bin/bash^M` | Windows 的 CRLF 换行 | `dos2unix run_gaussian.pbs` |

## 我自己遇到的

（往这里加，记清楚：现象 / 排查过程 / 根因 / 解决）

### 2026-09-08 · HW1 Ex1 单点秒退，log 里没有 "SCF Done"

- 现象：`grep -c "SCF Done" 01_...log` 返回 0；`tail` 显示
  `Out-of-memory error in routine RdGeom-1 ... Use %mem=11MW`，`Error termination via Lnk1e`。
- 根因：作业 PDF 给的示意输入写的是 `%mem=6MW`（≈48 MB），atlas9 的 g16 RevC.02
  连读几何结构都不够。题目模板只是示意，实际跑要自己调大内存。
- 解决：`%mem=6MW` → `%mem=1GB`。`sed -i 's/%mem=6MW/%mem=1GB/' 文件` 一行搞定。
- 顺带确认：atlas9 上 Gaussian 模块 = `Gaussian/g16`；serial 队列 1 核足够跑双原子；
  scratch 它自己用 `/scratch/<jobid>/`（PBS 设的 TMPDIR），`GAUSS_SCRDIR` 可不设。
