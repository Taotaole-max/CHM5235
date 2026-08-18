# PBS 作业调度速查

## 提交与管理

```bash
qsub  job.pbs              # 提交，返回作业号如 12345.venus
qstat -u $USER             # 我的所有作业（Q=排队 R=运行 E=退出中 H=挂起）
qstat -f 12345             # 某作业的完整信息（含被杀原因）
qstat -Q                   # 有哪些队列
qstat -Qf parallel         # 某队列的资源上限和 walltime 限制
qdel  12345                # 撤销作业
qsub -I -l select=1:ncpus=4 -q parallel   # 申请交互式节点（调试用，不要用来长跑）
```

## 脚本骨架

```bash
#!/bin/bash
#PBS -P project_code             # 算账用，必填且必须正确
#PBS -q parallel                 # 队列
#PBS -N job_name                 # 作业名（决定日志文件名）
#PBS -l select=1:ncpus=8:mem=16GB   # 1 节点 8 核 16GB
#PBS -l walltime=12:00:00        # 时:分:秒，超时直接杀
#PBS -j oe                       # 标准错误并入标准输出
#PBS -M 你的邮箱                  # 可选：作业状态邮件
#PBS -m ae                       # 可选：a=中止时发 e=结束时发

cd $PBS_O_WORKDIR                # ★ 不写这行，作业在家目录跑，找不到输入文件

module purge
module load 软件模块名

<真正的计算命令>
```

## 有用的环境变量

| 变量 | 含义 |
|---|---|
| `$PBS_O_WORKDIR` | **你提交作业时所在的目录** |
| `$PBS_JOBID` | 作业号，拿来给临时目录命名很方便 |
| `$PBS_NODEFILE` | 分到的核心列表文件，`cat $PBS_NODEFILE \| wc -l` 得到核数 |
| `$PBS_JOBNAME` | 作业名 |

## 资源申请的三条经验

1. **内存三处一致**：PBS 的 `mem` > 软件自己要的内存 + 1~2GB 余量
   - Gaussian `%mem` / ORCA `nprocs × maxcore` / MOLCAS `MOLCAS_MEM`
2. **核数不是越多越好**：小体系给太多核反而慢（通信开销），且排队更久。8~12 核是课程作业的合理起点
3. **walltime 宁多勿少**：超时会直接杀掉，之前算的全白费；但要得太离谱会排队更久

## 排查失败的顺序

```bash
cat  job_name.o12345          # ① PBS 日志，先看这个
qstat -f 12345                # ② 若还在系统里，看被杀原因
tail -50 计算输出.log          # ③ 软件自己的输出
df -h $HOME; quota            # ④ 磁盘配额满了？（会导致无声失败）
```

| 日志里看到 | 多半是 |
|---|---|
| `command not found` | module 没 load 或名字错 |
| `No such file or directory` | 忘了 `cd $PBS_O_WORKDIR`，或文件没传上来 |
| `bad interpreter: /bin/bash^M` | Windows CRLF 换行 → `dos2unix 脚本` |
| 日志几乎空白、作业秒退 | 输入文件格式错 |
| 跑到一半消失 | walltime 到 / 内存超 / 磁盘满 |

## Linux 常用命令（集群上够用的一小撮）

```bash
ls -lh              # 看文件大小
du -sh *            # 各目录占多大（查磁盘时用）
df -h $HOME         # 家目录还剩多少
tail -f 文件         # 实时跟踪输出（看计算跑到哪了），Ctrl+C 退出
grep -n "关键词" 文件 # 带行号搜索
nano 文件            # 最简单的编辑器（Ctrl+O 存，Ctrl+X 退）
cp -r 目录 备份       # 递归复制
```
