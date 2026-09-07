# Ex6 — CFH₂-OH 激发态与光谱（5 分）

分子：**氟甲醇 CH₂F–OH**（C 接 2H + F + OH）。

`ch2foh_excited.gjf` 一个文件三段：
1. B3LYP/cc-pVTZ **opt + freq**（基态几何，检查无虚频）
2. **TDA**（Tamm–Dancoff 近似的 TD-DFT），前 5 个激发态，B3LYP/cc-pVTZ
3. **CIS**/cc-pVTZ，前 5 个激发态

后两个用 `geom=check guess=read` 从第 1 步的 chk 读优化几何。

## 要交什么

- **对比表**：两套方法的 5 个激发能（eV 和 nm）、振子强度 f、主要跃迁指认（HOMO→LUMO 等）。
  搜 `Excited State   1:` 之类的行。

  | 态 | TDA E/eV | TDA λ/nm | TDA f | CIS E/eV | CIS λ/nm | CIS f | 主跃迁 |
  |---|---|---|---|---|---|---|---|

  讨论差异：CIS 通常**系统性高估**激发能（缺相关，类似 HF 之于基态）；
  TDA-TDDFT 更接近实验，但对电荷转移/里德堡态两者都不好。

- **UV/Vis 谱**：用激发能 + 振子强度做高斯展宽卷积。
  方法见 https://gaussian.com/uvvisplot/ ——GaussView 里直接 Results → UV-Vis，
  或用下面的脚本。两套结果画在同一张图对比。

```python
# plot_uvvis.py  —— 填入你从 log 里读到的数值
import numpy as np, matplotlib.pyplot as plt
def spectrum(exc_eV, fosc, fwhm_eV=0.4, grid=np.linspace(3,10,700)):
    s = np.zeros_like(grid)
    sigma = fwhm_eV/2.3548
    for e,f in zip(exc_eV,fosc):
        s += f*np.exp(-0.5*((grid-e)/sigma)**2)
    return 1239.84/grid, s          # 返回 (nm, 强度)
tda = ([ , , , , ], [ , , , , ])   # <-- TDA: [激发能eV], [f]
cis = ([ , , , , ], [ , , , , ])   # <-- CIS
for name,(e,f) in {"TDA":tda,"CIS":cis}.items():
    x,y = spectrum(np.array(e),np.array(f)); plt.plot(x,y,label=name)
plt.xlabel("λ / nm"); plt.ylabel("rel. absorption"); plt.legend()
plt.savefig("ex6_uvvis.png",dpi=200)
```

## 跑法
```bash
qsub submit_ex6.pbs
```
