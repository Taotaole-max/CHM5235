# ORCA 踩过的坑

## 已知高频坑（预填，遇到时对照）

| 现象 | 原因 | 解决方法 |
|---|---|---|
| 并行时报错或退化成串行 | **没用可执行文件的绝对路径** | 脚本里 `$(which orca) mol.inp`，绝不能只写 `orca` |
| MPI 相关报错 / 启动即崩 | ORCA 编译时绑定了特定 OpenMPI 版本 | `module load` 对应版本的 openmpi，版本必须精确匹配 |
| 作业被 OOM 杀掉 | `%maxcore` 是**每核**内存，误当成总量 | 总内存 = nprocs × maxcore，要小于 PBS 的 mem |
| `Error: Cannot open ... def2/J` | 用了 RIJCOSX 但没写辅助基组 | 关键字行加 `def2/J` |
| SCF 不收敛 | 开壳层/过渡金属体系初始猜测差 | 加 `! SlowConv` 或 `%scf MaxIter 500 end`；先小基组算好再 `MOREAD` |
| 频率有虚频但优化"收敛"了 | 收敛判据太松 | 加 `TightOpt` + `TightSCF` 重做 |
| BS 计算给出的 J 符号看不懂 | 不同公式/不同 Hamiltonian 约定 | 明确写出你用的约定，别混用 |
| 结果和 Gaussian 差很多 | 默认积分格点、RI 近似、色散校正不同 | 对比时两边设置要对齐，或在报告里解释差异来源 |
| 脚本报 `bad interpreter: ^M` | Windows CRLF 换行 | `dos2unix run_orca.pbs` |

## 我自己遇到的

（往这里加）
