# VASP 踩过的坑

## 已知高频坑（预填，遇到时对照）

| 现象 | 原因 | 解决方法 |
|---|---|---|
| **结果完全不对但程序不报错** | POTCAR 元素顺序和 POSCAR 不一致 | `grep TITEL POTCAR` 核对顺序 |
| 后续计算用的还是旧结构 | 忘了 `cp CONTCAR POSCAR` | 弛豫产物是 CONTCAR，不是 POSCAR |
| 优化"跑完了"但结构没优化好 | 没检查 `reached required accuracy` | 没这句就是 NSW 用完了还没收敛，接着 `cp CONTCAR POSCAR` 再跑一轮 |
| 变胞优化 (ISIF=3) 结果不可靠 | ENCUT 不够导致 Pulay 应力 | ENCUT 提到 ENMAX 的 1.3 倍以上；或收敛后固定晶胞再跑一次 |
| 能带图是一条平线 / 完全错乱 | `ICHARG=11` 但 CHGCAR 没拷过来，或 KPOINTS 没换成线模式 | 两个都要有 |
| DOS 很毛糙 | k 点太少或 NEDOS 太小 | 加密 k 网格，NEDOS 调到 3001 |
| 用 ISMEAR=-5 弛豫，力很奇怪 | 四面体法算出的力不准 | 弛豫用 ISMEAR=0/1，只有最终 DOS/总能才用 -5 |
| 金属体系能量抖动、SCF 不收敛 | ISMEAR/SIGMA 选错 | 金属用 ISMEAR=1、SIGMA=0.2 |
| 2D 材料层间距被压扁 | 用了 ISIF=3，真空方向也被优化 | 2D 用 ISIF=4，或固定 c 轴 |
| 2D / 层状材料层间距明显偏大 | 纯 GGA 描述不了范德华力 | 加 `IVDW = 12` |
| 表面吸附能不合理 | 周期镜像之间有静电相互作用 | `IDIPOL=3` + `LDIPOL=.TRUE.`；真空层加到 15–20 Å |
| 过渡金属氧化物带隙远小于实验 | GGA 的自相互作用误差 | 用 DFT+U (`LDAU`)，或杂化泛函 HSE06（很贵） |
| 作业跑得异常慢 | NCORE 设得不合理 | NCORE ≈ √(总核数)，且要能整除每节点核数 |
| 磁盘配额爆掉 | WAVECAR / CHGCAR 累积 | 中间步骤设 `LWAVE=.FALSE.`；算完及时删 WAVECAR |
| `ZBRENT: fatal error in bracketing` | 优化过程中能量面出问题 | `cp CONTCAR POSCAR` 后重启；或换 IBRION=1 |
| SCF 不收敛（电子步跑满 NELM） | 初始猜测差 / 展宽不当 | 调 `ALGO=All` 或 `AMIX/BMIX`；先粗后精 |

## 我自己遇到的

（往这里加）
