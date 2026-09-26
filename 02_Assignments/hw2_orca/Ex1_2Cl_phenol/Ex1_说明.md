# Ex1 2-氯苯酚基态：四种方法的结构优化 + 频率

题目要求：UKS / def2-TZVP，分别用 PBE、B3LYP、PBE+水、B3LYP+水优化结构，比较电荷（Mulliken、Löwdin）、
振动频率、偶极矩、室温熵和 HOMO-LUMO 能隙；另外做 12 号振动模式的动画、HOMO/LUMO 图、电子密度+静电势图。

## 现在有的文件

```
Ex1_2Cl_phenol/
├── Ex1_说明.md                          本文件
├── 2Cl_phenol_cis_start_geometry.xyz    初始结构，四个方法共用
├── ex1_submit_4_methods.sh              提交脚本：一条命令交四个作业
├── ex1_run_one_method.pbs               作业脚本：跑一个方法，跑完自动检查、改名、归档
├── PBE_gas/      ex1_optfreq_PBE_gas.inp          ORCA 输入：PBE，气相
├── B3LYP_gas/    ex1_optfreq_B3LYP_gas.inp        ORCA 输入：B3LYP，气相
├── PBE_water/    ex1_optfreq_PBE_water.inp        ORCA 输入：PBE，水溶剂
├── B3LYP_water/  ex1_optfreq_B3LYP_water.inp      ORCA 输入：B3LYP，水溶剂
├── ex1_analysis/                        结果整理（只在本机用，不用传到集群）
│   ├── ex1_extract_results.py           从四个 .out 里提取题目要的五项数据
│   └── ex1_results_tables.md            上面脚本生成的对比表（英文，直接搬进报告）
└── ex1_figures/                         报告里的图
    ├── ex1_render_figures.py            本机画图脚本（PyVista），一个脚本画全部图
    ├── ex1_fig_atom_numbering.png       原子编号示意图（电荷表用）
    ├── ex1_fig_mode12_displacements_B3LYP_gas.png   12 号振动模式，带位移箭头
    ├── ex1_mode12_animation_B3LYP_gas.gif           12 号振动模式动画（题目要的动画）
    ├── ex1_fig_HOMO_LUMO_B3LYP_gas.png              HOMO / LUMO（格点算完后生成）
    ├── ex1_fig_density_ESP_B3LYP_gas.png            电子密度 + 静电势（格点算完后生成）
    └── cube_job/                        在集群上生成格点文件的小作业
        ├── ex1_sp_for_plots_B3LYP_gas.inp   在 B3LYP 气相结构上重算单点，顺便写 HOMO/LUMO/密度 cube
        ├── ex1_make_cube_files.pbs          作业脚本：跑单点，再用 orca_vpot 算静电势
        ├── ex1_esp_grid_points_bohr.xyz     算静电势的 13 万个格点坐标（Bohr，本机生成）
        └── ex1_esp_grid_box.txt             上面格点的起点、间距、点数
```

- `ex1_analysis/ex1_extract_results.py`：把各方法文件夹从集群拉回本机后运行 `python ex1_extract_results.py`，
  重新生成 `ex1_results_tables.md`。还没算完的方法显示 "—"，可以边算边跑。
  五张表：(a) 每个原子的 Mulliken / Löwdin 电荷，(b) 33 个振动频率，(c) 偶极矩，(d) 298.15 K 的熵（分项 + 总和），
  (e) HOMO、LUMO 和能隙。
- 注意：Löwdin 电荷里 Cl、O 是正的，和 Mulliken 符号相反。这是 ORCA 输出的原值，不是提取错了——
  Löwdin 分析在大基组下本来就会这样，照实列出即可。

- `2Cl_phenol_cis_start_geometry.xyz`：Canvas 给的结构里 OH 的氢垂直于苯环，从那里优化可能停在鞍点。
  这里把氢转到朝向 Cl 的一侧（分子内氢键，能量最低的构象），其它 12 个原子没动。原文件在 `00_题目和原始文件/`。
- `ex1_submit_4_methods.sh`：在集群上运行它，四个方法各交一个作业。只重交一个就在后面写方法名，
  例如 `bash Ex1_2Cl_phenol/ex1_submit_4_methods.sh B3LYP_water`。
- `ex1_run_one_method.pbs`：不用手动运行，由提交脚本调用。它做四件事：跑 ORCA → 查虚频 →
  生成画图和动画要用的文件 → 把 ORCA 的中间文件收进 `orca_raw_files/`。
- 四个 `.inp`：ORCA 的输入，内容只差泛函（PBE / B3LYP）和有没有水溶剂（`CPCM(Water)`）。

## 算完之后，每个方法文件夹里会有什么

以 `PBE_gas/` 为例，外层只留写报告用得上的：

| 文件 | 干什么用 |
|---|---|
| `ex1_optfreq_PBE_gas.inp` | 输入（不变） |
| `ex1_optfreq_PBE_gas.out` | ORCA 主输出。表格里的电荷、频率、偶极矩、熵、HOMO/LUMO 能量都从这里取 |
| `ex1_optimized_geometry_PBE_gas.xyz` | 优化好的结构，Ex4 的 TD-DFT 要用。**有虚频时不生成这个文件** |
| `ex1_orbitals_density_PBE_gas.molden` | 用 Avogadro / Chemcraft 打开，画 HOMO、LUMO、电子密度+静电势 |
| `ex1_mode12_animation_ORCAindex12_PBE_gas.xyz` | 振动动画：ORCA 输出里标 "12:" 的模式 |
| `ex1_mode12_animation_12thVibration_PBE_gas.xyz` | 振动动画：第 12 个真振动（ORCA 编号 17） |
| `ex1_pbs_log_PBE_gas.txt` | 作业日志，写着有没有虚频、有没有正常结束 |
| `orca_raw_files/` | ORCA 的中间文件（波函数 .gbw、Hessian .hess、优化过程轨迹等），一般不用打开 |

两个动画文件的区别：ORCA 的振动编号从 0 开始，0–5 是平动和转动，所以 ORCA 的 "12" 其实是第 7 个真振动；
而 Avogadro/Chemcraft 的振动列表可能从第一个真振动开始数。题目的 "mode 12" 指哪个说不准，
两个都生成了，写报告时选一个并注明编号方式。

## 怎么跑

1. 连上 NUS VPN，把 `01_cluster_setup/` 和 `Ex1_2Cl_phenol/` 两个文件夹传到 atlas9 的同一个目录下
   （`00_题目和原始文件/` 不用传）。
2. 第一次用 ORCA，先查一次环境（只查询，几秒钟）：`bash 01_cluster_setup/check_orca_on_cluster.sh`，
   把输出贴回来，确认 `01_cluster_setup/orca_env_settings.sh` 怎么填。
3. `bash Ex1_2Cl_phenol/ex1_submit_4_methods.sh`。四个作业单核 `serial` 队列并行排队，每个预计几十分钟到两小时。

## 设置和理由

- 关键字：`! UKS <泛函> def2-TZVP def2/J TightSCF TightOpt Opt Freq`，水溶剂加 `CPCM(Water)`。
  B3LYP 多加 `RIJCOSX`（RI 近似加速，正好是 Ex3 理论题讲的东西），PBE 没有 HF 交换项，只需要 RI-J。
- 电荷、偶极矩、轨道能量、298.15 K 的热化学（含熵）ORCA 默认就会打印，不用额外关键字。
- 2-氯苯酚是闭壳层，UKS 结果会和 RKS 完全一样，α、β 轨道能量相同，这是正常的。
- `.inp` 里的注释用英文，文件名和文件夹名都用英文：免得 ORCA 在集群上碰到中文路径出问题；中文说明都放在这个文件里。
