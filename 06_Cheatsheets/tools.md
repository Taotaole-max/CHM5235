# 常用工具速查

## 可视化 / 前处理后处理

| 工具 | 用途 | 链接 |
|---|---|---|
| GaussView | Gaussian 配套可视化 | 随 Gaussian 提供 |
| Avogadro | 分子编辑与可视化 (免费) | https://avogadro.cc |
| Chemcraft | 计算结果可视化 (商业，150天试用) | http://www.chemcraftprog.com |
| Luscus | OpenMOLCAS 配套可视化 | 随 OpenMOLCAS 提供 |
| VESTA | 晶体结构可视化 (免费) | — |
| vaspkit | VASP 后处理 (免费) | — |
| py4vasp | VASP 后处理 Python 库 (免费) | — |
| VMD | 分子动力学/大分子可视化 (免费) | https://www.ks.uiuc.edu/Research/vmd/ |
| Multiwfn | 波函数分析计算 (免费) | http://sobereva.com/multiwfn/ |
| JMOL | 分子编辑可视化 (免费) | http://jmol.sourceforge.net |
| MOLDEN | 波函数可视化计算 (免费) | https://www3.cmbi.umcn.nl/molden/ |
| Material Studio | 材料建模 (商业，NUS 有限授权) | — |

## HPC 连接与传输

| 工具 | 用途 |
|---|---|
| PuTTY | Windows SSH 客户端 |
| FileZilla / WinSCP | 文件传输 (SFTP) |
| Notepad++ | 文本文件查看编辑 |

## Linux 常用命令

```bash
ssh user@server           # 连接 HPC
scp file user@server:~/   # 传输文件到服务器
qsub job.pbs               # 提交 PBS 作业
cat file | grep 'pattern' | wc -l   # 统计匹配行数
diff file1 file2           # 比较文件
```

**注意**：永远不要用 local/network filesystem 做 scratch 存储，会拖慢整个集群。用集群管理员指定的 `scratch` 目录。
