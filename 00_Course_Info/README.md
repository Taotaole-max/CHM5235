# Course Info — CM5235 Applied Computational Chemistry

- **授课教师**: Liviu Ungur
- **课程代码**: CM5235 (NUS)

## 课程结构

**理论课**：计算化学概述、原子/粗粒化力场方法、量子力学基础、Hartree-Fock 理论与 Roothaan-Hall 方程、波函数分析（原子电荷/电子密度/轨道局域化）、电子相关方法（MP2/CCSD）、分子动力学（DFT/半经验）。

**实践课**：Linux OS、脚本、作业提交，使用四个量子化学软件包：
- **Gaussian + GaussView**：几何优化、振动频率、轨道/密度可视化、BS-DFT 磁交换、TD-DFT 激发态
- **ORCA + Avogadro/Chemcraft**：同上任务（Lecture 02 显示实际版本为 ORCA 5.0.3）
- **OpenMOLCAS + Luscus**：多组态方法 RASSCF/CASPT2/RASSI，过渡金属与镧系化合物激发态
- **VASP + VESTA/vaspkit/py4vasp**：固体周期性材料、2D 层状材料、表面吸附

## 评分 (Assessments)

| 项目 | 权重 |
|---|---|
| HW1: Gaussian / GaussView | 15% |
| HW2: ORCA / Avogadro / Chemcraft | 15% |
| HW3: OpenMOLCAS / Luscus | 15% |
| HW4: VASP / VESTA / vaspkit / py4vasp | 15% |
| Mid-Term quiz (Tue 29 Sep, 7–8pm) | 15% |
| Final Exam | 25% |

- 四次作业均需在 HPC@NUS 集群上完成实际计算
- 报告需提交为**单个 PDF 文件**/学生（手写也可以，但要保证可读）
- 期中/期末考试为理论概念题，不需要实际计算

## ⚠️ 待澄清：到底用哪个集群

课程大纲写的是 **HPC@NUS**，但 **Lecture 02 p.92** 写的是
"Installation of the ORCA / MOLCAS software on **NSCC**"（新加坡国家超算中心）。

**这是两个不同机构，账号不通用。** 需要跟老师或 Canvas 确认。
下面的接入说明是按 HPC@NUS 写的；若实际用 NSCC，登录地址、队列名、
project code 的申请流程都要换，但 PBS 脚本的写法是一样的。

另外 Lecture 02 p.95 显示课程用的 ORCA 版本是 **5.0.3 (openmpi411)**，
不是本文档下面写的 ORCA 6。

## HPC@NUS 接入

1. 安装 NUS VPN（校外访问需要）：https://nusit.nus.edu.sg/eguides/
2. 申请 HPC 账号：https://nusit.nus.edu.sg/hpc/get-an-hpc-account/ （需先登录 VPN，用 Chrome/Edge/Firefox）
3. SSH 登录：
   - Windows: PuTTY (https://www.putty.org)
   - Mac: 直接用 Terminal 的 `ssh` 命令
4. 文件传输：FileZilla / WinSCP (`https://winscp.net`)
5. 必读：
   - HPC 新手指南 https://nusit.nus.edu.sg/services/getting-started/introductory-guide-for-new-hpc-users/
   - 批处理作业提交 (#PBS) https://nusit.nus.edu.sg/services/getting-started/how-to-run-batch-job/

### PBS 作业脚本模板

```bash
#!/bin/bash
#PBS -P test_script
#PBS -q parallel
#PBS -l select=1:ncpus=12:mem=2GB
#PBS -j oe

cd $PBS_O_WORKDIR
# 计算命令写在这里
exit
```

## 推荐阅读书目

- Frank Jensen, *Introduction to Computational Chemistry* (3rd ed.)
- Ira N. Levine, *Quantum Chemistry* (7th ed.)
- Engel & Reid, *Quantum Chemistry and Spectroscopy* (4th ed.)
- Szabo & Ostlund, *Modern Quantum Chemistry*
- Christopher J. Cramer, *Essentials of Computational Chemistry* (2nd ed.)
- F. Albert Cotton, *Chemical Applications of Group Theory* (3rd ed.)
- David B. Cook, *Handbook of Computational Quantum Chemistry*

## 教师联系方式 / 评分标准细则

（待补充）
