# VASP 模板使用说明

VASP 没有单一输入文件，它靠**当前目录下四个固定文件名**驱动：

| 文件 | 管什么 | 从哪来 |
|---|---|---|
| `POSCAR` | **结构**：晶格矢量 + 原子坐标 | 自己写 / VESTA 导出 / Materials Project 下载 |
| `INCAR` | **算什么、怎么算**：所有参数 | 抄本目录的 `INCAR.*` 模板 |
| `KPOINTS` | **倒空间取样** | 抄本目录的 `KPOINTS.*` 模板 |
| `POTCAR` | **赝势**：元素的电子-离子相互作用 | 从课程提供的赝势库按元素顺序拼接 |

**POTCAR 的元素顺序必须和 POSCAR 里的顺序完全一致**，否则算的是别的物质而**不会报错**。

```bash
cat $POTCAR_DIR/Mo/POTCAR $POTCAR_DIR/S/POTCAR > POTCAR   # 顺序对应 POSCAR 的 "Mo  S"
grep TITEL POTCAR                                          # 检查拼对了没有
```

## 使用顺序

1. 准备 `POSCAR`（用 VESTA 建/看结构）
2. 拼 `POTCAR`
3. **收敛测试**：先扫 ENCUT，再扫 k 点密度（见 `../notes.md`）
4. `cp INCAR.1_relax INCAR` + `cp KPOINTS.gamma KPOINTS` → 提交 `run_vasp.pbs`
5. **`cp CONTCAR POSCAR`**（弛豫的产物是 CONTCAR！）
6. `INCAR.2_scf` → 得到 `CHGCAR`
7. `INCAR.3_band` + `KPOINTS.line` → 能带；`INCAR.4_dos` + 密网格 → DOS

嫌麻烦就直接提交 `run_vasp_workflow.pbs`，它把 4 步串起来一次跑完。

## 关键输出文件

| 文件 | 内容 |
|---|---|
| `OUTCAR` | 全部细节。信息最全但最长 |
| `OSZICAR` | 每个电子步/离子步的能量，用来看收敛过程 |
| `CONTCAR` | **优化后的结构**（下一步的输入） |
| `CHGCAR` | 电荷密度（能带/DOS 的输入，很大） |
| `WAVECAR` | 波函数（极大，算完可删） |
| `EIGENVAL` | 本征值 → 能带图 |
| `DOSCAR` | 态密度 |
| `PROCAR` | 轨道投影（`LORBIT=11` 才有） |
| `vasprun.xml` | 结构化的全部结果，**py4vasp / pymatgen 读的就是它** |
