# Ex4 激发态与 UV 光谱：四个 Ex1 结构上的 TD-DFT

题目要求：在 Ex1 优化好的四个结构上，用 TD-DFT 算 2-氯苯酚的前 5 个激发态；列表比较四组激发能，
说明溶剂效应有多大影响；画 UV 光谱。

## 现在有的文件

```
Ex4_TDDFT/
├── Ex4_说明.md                  本文件
├── ex4_submit_4_methods.sh      提交脚本：一条命令交四个作业
├── ex4_run_one_method.pbs       作业脚本：跑一个方法，跑完自动检查、归档
├── PBE_gas/      ex4_tddft_PBE_gas.inp        ORCA 输入：PBE，气相
├── B3LYP_gas/    ex4_tddft_B3LYP_gas.inp      ORCA 输入：B3LYP，气相
├── PBE_water/    ex4_tddft_PBE_water.inp      ORCA 输入：PBE，水溶剂
├── B3LYP_water/  ex4_tddft_B3LYP_water.inp    ORCA 输入：B3LYP，水溶剂
└── ex4_analysis/                  结果整理（只在本机用）
    ├── ex4_extract_and_plot_uv.py     读出激发能、波长、振子强度、主要跃迁，并画 UV 光谱
    ├── ex4_excited_states_table.md    上面脚本生成的核对表
    └── ex4_fig_UV_spectra.png         UV 光谱图（报告用）
```

注意：比较溶剂效应时要按"主要跃迁"配对，不能按态的编号——加了水以后态的顺序会变（B3LYP 的 S₂、S₃ 互换，
最亮的 HOMO−1→LUMO 态在水里掉进了前 5 个）。

- `ex4_submit_4_methods.sh`：在集群上运行它。它会看 Ex1 对应方法的情况自动处理：
  Ex1 已算完 → 直接提交；Ex1 还在排队或在算 → 也提交，但挂上 PBS 依赖，等那个 Ex1 作业成功结束才开始
  （这段时间 `qstat` 里状态显示 `H`）；Ex1 没结果（比如有虚频）→ 跳过并提示。
- `ex4_run_one_method.pbs`：不用手动运行。它做四件事：把 Ex1 的优化结构复制过来 → 跑 ORCA →
  把激发态表打到日志里 → 把 ORCA 的中间文件收进 `orca_raw_files/`。
- 四个 `.inp`：内容只差泛函和有没有水溶剂，与 Ex1 一一对应。

## 算完之后，每个方法文件夹里会有什么

以 `PBE_gas/` 为例：

| 文件 | 干什么用 |
|---|---|
| `ex4_tddft_PBE_gas.inp` | 输入（不变） |
| `ex4_tddft_PBE_gas.out` | ORCA 主输出。5 个激发态的能量（eV、nm）、振子强度都在这里 |
| `ex4_input_geometry_from_ex1_PBE_gas.xyz` | 这次计算用的结构，从 Ex1 复制来的，留着备查 |
| `ex4_pbs_log_PBE_gas.txt` | 作业日志，里面直接有激发态那张表 |
| `orca_raw_files/` | ORCA 的中间文件，一般不用打开 |

## 怎么跑

`bash Ex4_TDDFT/ex4_submit_4_methods.sh`（在集群上 `~/CHM5235/as2` 里运行）。
每个作业单核、8 GB、限时 4 小时；TD-DFT 单点预计十几分钟到半小时。

## 设置和理由

- 关键字：`! RKS <泛函> def2-TZVP def2/J TightSCF`，B3LYP 加 `RIJCOSX`，水溶剂加 `CPCM(Water)`；
  `%tddft NRoots 5  TDA false end`。泛函、基组、溶剂都和 Ex1 保持一致，四组才可比。
- **用 RKS 不用 UKS**：2-氯苯酚是闭壳层，基态两者完全一样；但 UKS 上做 TD-DFT，5 个根里会混进三重态
  （振子强度为 0，光谱上不出峰），RKS 上算出来的全是单重态，正好是 UV 光谱要的。
- **关掉 TDA**（`TDA false`）：ORCA 默认用 Tamm-Dancoff 近似，完整 TD-DFT 的振子强度更可靠，画光谱更合适。
- 带溶剂的两组，CPCM 同时作用在激发态上（线性响应 CPCM），所以气相和水相的差别就是溶剂效应。
- walltime 只申请 4 小时（Ex1 申请的是 24 小时）：申请得越短，调度器越容易把作业塞进空档，排队更快。
