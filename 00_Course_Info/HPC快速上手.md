# HPC@NUS 快速上手：从登录到第一个作业跑通

> 你已经能登录了，这份文档只解决下一步：**让集群真的帮你算出东西**。
> 带 `⚠️ 待确认` 的地方是我无法替你查的，第一次登录时确认完请直接回填进这个文件。

## 0. 心智模型：集群和你的笔记本不一样

登录后你所在的机器叫**登录节点 (login node)**，它是**所有人共用的**，只能用来编辑文件、传文件、提交作业。
真正算东西的是**计算节点**，你摸不到它，只能写一个脚本描述"我要多少核、多少内存、跑什么命令"，
然后交给**调度系统 (PBS Pro)** 排队。轮到你了，它替你去计算节点上执行。

所以工作流永远是这四步：

```
准备输入文件  →  写 PBS 脚本  →  qsub 提交  →  qstat 等 → 看输出
```

**绝对不要在登录节点直接跑 g16 / orca / vasp**，那会拖慢所有人，管理员会找你。

## 1. 第一次登录要查清的五件事

登录后依次跑下面的命令，把结果填到本文档对应位置。

### 1.1 我的 project code 是什么

PBS 脚本里的 `#PBS -P xxx` 要填它，填错作业直接被拒。

```bash
# 常见查法（不同集群命令不同，挨个试）
groups              # 看你属于哪些组
qstat -Q            # 看有哪些队列
```

> ⚠️ 待确认 — 我的 project code：`________`

### 1.2 有哪些队列，各自限制是什么

```bash
qstat -Q            # 队列列表
qstat -Qf parallel  # 某个队列的详细限制（最大核数、最长 walltime）
```

课程讲义里给的模板用的是 `-q parallel`。确认它存在、以及最长 walltime 是多少
（超过 walltime 作业会被**直接杀掉**，算了 20 小时也白算——这是新手最惨的坑）。

> ⚠️ 待确认 — 可用队列：`________`　最长 walltime：`________`

### 1.3 四个软件的模块名

```bash
module avail                    # 列出全部（很长，建议接 less）
module avail 2>&1 | grep -i gaussian
module avail 2>&1 | grep -i orca
module avail 2>&1 | grep -i -e molcas -e vasp
```

查到后回填，以后写脚本直接抄：

| 软件 | `module load` 名称 | 可执行文件 |
|---|---|---|
| Gaussian | ⚠️ `________` | `g16` 还是 `g09`？`________` |
| ORCA | ⚠️ `________` | 需要**绝对路径**：`________` |
| OpenMOLCAS | ⚠️ 课程可能自带，不走 module | `pymolcas` 路径：`________` |
| VASP | ⚠️ `________` | `vasp_std` / `vasp_gam` / `vasp_ncl` |

`module load xxx` 之后用 `which g16` / `which orca` 就能拿到绝对路径。

### 1.4 scratch 目录在哪

**永远不要把计算中间文件写在家目录或网络盘**——课程讲义原话，这会拖慢整个集群。

```bash
echo $HOME
ls -ld /scratch/$USER /hpctmp/$USER 2>/dev/null   # NUS 常见是 /hpctmp
df -h $HOME                                        # 看家目录配额
```

> ⚠️ 待确认 — scratch 路径：`________`　家目录配额：`________`

### 1.5 存储配额

家目录通常只有几个 GB，而一次 VASP 计算的 `WAVECAR` 就能上 GB。
配额满了作业会**莫名其妙失败且不报错**——遇到诡异失败先 `df -h` 或 `quota`。

## 2. 建议的目录布局

```
$HOME/
├── CHM5235/
│   ├── hw1_gaussian/
│   ├── hw2_orca/
│   ├── hw3_molcas/
│   ├── hw4_vasp/
│   └── templates/        ← 从本仓库 03_Software_Methods/*/templates/ 传上来
└── ...

$SCRATCH/CHM5235/          ← 计算真正的工作目录，大文件都在这
```

原则：**输入文件和脚本放家目录（小、要备份）；计算过程和大输出放 scratch（大、可重算）**。

## 3. 传文件

### 图形界面（推荐先用这个）
WinSCP 或 FileZilla，SFTP 协议，填集群地址和你的 NUSNET 账号。拖拽即可。

### 命令行（熟了更快）
在**你的 Windows 本地**打开 Git Bash 或 PowerShell：

```bash
# 本地 → 集群
scp mol.gjf  你的账号@集群地址:~/CHM5235/hw1_gaussian/

# 集群 → 本地（取回结果）
scp 你的账号@集群地址:~/CHM5235/hw1_gaussian/mol.log  .

# 整个目录
scp -r hw1_gaussian/  你的账号@集群地址:~/CHM5235/
```

> ⚠️ 待确认 — 集群登录地址：`________`

**换行符的坑**：Windows 编辑的文本文件是 CRLF 换行，传到 Linux 上脚本会报
`bad interpreter: /bin/bash^M`。解决：用 `dos2unix 脚本名`，或在 Notepad++ 里
「编辑 → 档案格式转换 → 转换为 UNIX 格式」再传。

## 4. 你的第一个作业：先用一个什么都不算的脚本验证流程

**不要**一上来就提交真实计算。先提交这个只打印信息的脚本，确认整条链路通了。

```bash
# 在集群上：mkdir -p ~/CHM5235/test && cd ~/CHM5235/test
cat > hello.pbs <<'PBS'
#!/bin/bash
#PBS -P 你的project_code
#PBS -q parallel
#PBS -N hello_test
#PBS -l select=1:ncpus=4:mem=4GB
#PBS -l walltime=00:05:00
#PBS -j oe

cd $PBS_O_WORKDIR

echo "=== 作业在哪台机器上跑 ==="
hostname
echo "=== 工作目录 ==="
pwd
echo "=== 分到了几个核 ==="
cat $PBS_NODEFILE | wc -l
echo "=== 开始时间 ==="
date
sleep 30
echo "=== 结束时间 ==="
date
PBS

qsub hello.pbs
```

提交后会返回一个作业号，比如 `12345.venus`。然后：

```bash
qstat -u $USER        # 看状态：Q=排队中  R=运行中  没了=结束了
```

结束后当前目录会多出 `hello_test.o12345`，`cat` 它。
**能看到 hostname 和 30 秒的时间差 = 你已经会用集群了。**

### PBS 指令逐行解释

| 指令 | 含义 | 注意 |
|---|---|---|
| `#PBS -P xxx` | project code，算账用 | 填错直接被拒 |
| `#PBS -q parallel` | 提交到哪个队列 | 不同队列资源上限不同 |
| `#PBS -N hello_test` | 作业名 | 决定输出文件名，起有意义的名字 |
| `#PBS -l select=1:ncpus=4:mem=4GB` | 要 1 个节点、4 核、4GB 内存 | **内存要和软件输入里写的一致**，见下 |
| `#PBS -l walltime=00:05:00` | 最长跑 5 小时…不，是 5 分钟（时:分:秒） | 超时直接杀，宁可多申请 |
| `#PBS -j oe` | 把标准错误并进标准输出 | 只生成一个日志文件，方便看 |
| `cd $PBS_O_WORKDIR` | 切回你提交作业时所在的目录 | **不写这行，作业会在家目录跑，找不到输入文件** |

`$PBS_O_WORKDIR` 忘了写是新手第一大坑。

## 5. 资源申请的两条原则

**原则一：内存要三处一致。**
PBS 的 `mem=8GB`、Gaussian 的 `%mem=6GB`、ORCA 的 `%maxcore` 必须协调。
给软件的值要**小于**问 PBS 要的值（留 1–2GB 给系统和 I/O），否则作业被 OOM 杀掉。

**原则二：核数不是越多越快。**
小分子给 24 核可能比 8 核还慢（通信开销超过计算收益），而且排队时间更长。
课程作业的体系普遍不大，`ncpus=8` 或 `12` 是合理起点。

## 6. 作业挂了怎么查

```bash
qstat -u $USER              # 还在不在
qstat -f 作业号             # 详细状态（含被杀原因）
cat 作业名.o作业号          # PBS 日志，最先看这个
tail -50 计算输出.log       # 软件自己的输出
```

排查顺序：
1. **`.o` 文件里有 `command not found`** → module 没 load 或名字写错
2. **`.o` 文件里有 `No such file or directory`** → 忘了 `cd $PBS_O_WORKDIR`，或文件没传上来
3. **作业秒结束、日志几乎空白** → 输入文件格式错（比如 Gaussian 结尾少空行）
4. **跑到一半突然没了** → walltime 到了，或内存超了，或磁盘配额满了
5. **算完但结果离谱** → 不是集群问题，是化学问题，去看 `notes.md`

**每查明一个，就写进对应软件的 `pitfalls.md`。**

## 7. 常用命令速查

```bash
qsub  job.pbs            # 提交
qstat -u $USER           # 我的作业
qstat -f 作业号          # 某作业详情
qdel  作业号             # 撤销
qstat -Q                 # 队列列表

module avail             # 有哪些软件
module load  名字        # 加载
module list              # 当前加载了哪些
module purge             # 全部卸载（脚本开头建议先 purge 再 load，避免环境冲突）
```
