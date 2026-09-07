# HW1 开跑前：在 atlas9 上确认 5 件事

> 登录 `atlas9.nus.edu.sg` 后，把下面这段整块粘进去跑一次，
> 然后把**全部输出**贴回给 Claude。我用它把 `submit_*.pbs` 里的
> `<<<...>>>` 占位符全部填死，你就能直接 `qsub` 了。

```bash
echo "===== 1. 我属于哪些组 / project ====="
groups
id

echo "===== 2. 有哪些队列 ====="
qstat -Q

echo "===== 3. Gaussian 模块名 ====="
module avail 2>&1 | grep -i gaussian
# 如果上面没输出，试：
source /app1/ebenv 2>/dev/null; module avail 2>&1 | grep -i -e gaussian -e g16

echo "===== 4. scratch 路径和配额 ====="
echo "HOME = $HOME"
ls -ld /hpctmp/$USER /scratch/$USER /home/svu/$USER 2>/dev/null
df -h $HOME
[ -d /hpctmp/$USER ] && df -h /hpctmp/$USER

echo "===== 5. 一个样例 PBS 头（看集群文档里推荐的写法） ====="
cat /etc/motd 2>/dev/null | head -40
ls /app1/common/documentation 2>/dev/null
```

## 需要回填的四个值

| 占位符 | 含义 | 来自上面第几步 |
|---|---|---|
| `<<<PROJECT>>>` | `#PBS -P` 的值（算账用的 project code） | 1（`groups` 里那个不是 `svu`/普通组的名字）|
| `<<<QUEUE>>>` | `#PBS -q` 的值 | 2（课程讲义模板用 `parallel`，确认它在列表里）|
| `<<<GAUSSIAN_MODULE>>>` | `module load` 的完整名字 | 3（例如 `Gaussian/16.C.02-AVX2`）|
| `<<<SCRATCH>>>` | 大临时文件目录（`GAUSS_SCRDIR`）| 4（NUS 常见是 `/hpctmp/$USER`）|

## 然后先跑一次“什么都不算”的测试

确认链路通了再交真计算。用仓库 `00_Course_Info/HPC快速上手.md` 第 4 节的 `hello.pbs`。
看到 `hostname` 和 30 秒时间差 = 可以开跑 HW1。
