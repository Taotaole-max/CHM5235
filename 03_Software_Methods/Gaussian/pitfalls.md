# Gaussian 踩过的坑

> 每遇到一个新问题就往下加一行。这个文件的价值随时间指数增长。

## 已知高频坑（预填，遇到时对照）

| 现象 | 原因 | 解决方法 |
|---|---|---|
| 作业秒退，`.log` 几乎是空的 | 输入文件**结尾少了空行** | `.gjf` 最后必须有一个空行 |
| `End of file in ZSymb` | 坐标段和结尾之间空行数量不对 | 检查五段结构，段间恰好一个空行 |
| `Out-of-memory` / 作业被杀 | `%mem` ≥ PBS 申请的 `mem` | `%mem` 要比 PBS 的 `mem` 小 1–2GB |
| `galloc: could not allocate memory` | 同上，或 `%nprocshared` 大于实际分到的核数 | `%nprocshared` 要 = PBS 的 `ncpus` |
| 磁盘写满 / `Erroneous write` | `.rwf` 临时文件写在了家目录 | 脚本里设 `export GAUSS_SCRDIR=` 指向 scratch |
| 优化跑满步数不收敛 | 初始结构太差，或用了平坦的势能面 | 加 `opt=(calcfc,maxcycles=200)`；先用小基组预优化 |
| 优化"成功"但有虚频 | 收敛到了鞍点 | 沿虚频模式微扰结构后重新优化 |
| 频率结果无意义 | freq 用的方法/基组和 opt 不一致 | 两步必须完全同一套方法和基组 |
| 开壳层结果不对，⟨S²⟩ 远大于理论值 | 自旋污染 | 加 `stable=opt` 检查波函数稳定性 |
| 阴离子能量异常高 | 基组缺弥散函数 | 用带 `+` 的基组 |
| 本地 GaussView 打不开集群下载的 `.chk` | `.chk` 是二进制，跨平台不通用 | 集群上 `formchk mol.chk mol.fchk`，下载 `.fchk` |
| 脚本报 `bad interpreter: /bin/bash^M` | Windows 的 CRLF 换行 | `dos2unix run_gaussian.pbs` |

## 我自己遇到的

（往这里加，记清楚：现象 / 排查过程 / 根因 / 解决）

### 2026-09-08 · HW1 Ex1 单点秒退，log 里没有 "SCF Done"

- 现象：`grep -c "SCF Done" 01_...log` 返回 0；`tail` 显示
  `Out-of-memory error in routine RdGeom-1 ... Use %mem=11MW`，`Error termination via Lnk1e`。
- 根因：作业 PDF 给的示意输入写的是 `%mem=6MW`（≈48 MB），atlas9 的 g16 RevC.02
  连读几何结构都不够。题目模板只是示意，实际跑要自己调大内存。
- 解决：`%mem=6MW` → `%mem=1GB`。`sed -i 's/%mem=6MW/%mem=1GB/' 文件` 一行搞定。
- 顺带确认：atlas9 上 Gaussian 模块 = `Gaussian/g16`；serial 队列 1 核足够跑双原子；
  scratch 它自己用 `/scratch/<jobid>/`（PBS 设的 TMPDIR），`GAUSS_SCRDIR` 可不设。

### 2026-09-12 · HW1 Ex2：`guess=mix` 对异核双原子(H-F)扫描全程没生效，⟨S²⟩ 全是 0

- 现象：H-F 势能面 rigid scan（UHF/UB3LYP/UCCSD/UCCSD(T)，cc-pVTZ，951 点，0.5→10 Å）算出来
  UHF 的解离能是实验值的 2 倍多（1248 vs 568.6 kJ/mol）；CCSD/CCSD(T) 在 R≈4.6 Å 报
  `*MAX. CYCLES*` + `Error termination via Lnk1e in .../l913.exe`，振幅（T2 amplitude）逼近 1。
- 排查：`grep "S\*\*2" hf_scan_uhf.log`，**从 R=0.5 到 R=10.0 全程 `<S**2>=0.0000`**——
  整条扫描一次都没打破自旋对称性，全程停在错误的闭壳层（部分离子性）解上。
  `guess=mix` 对 **同核**双原子（H₂ 这类）很可靠，对**异核**双原子经常"混了也白混"，
  SCF 会自己弹回闭壳层解——这条坑本课件笔记 `wk02`/`wk04` 只讲了 RHF 解离失败的一般原理，
  没提过 `guess=mix` 本身也可能失效。
- CCSD 报错是同一个根因的下游后果：post-HF 在一个"本该开壳层却是闭壳层"的参考态上强行加相关，
  键越拉越长，振幅越修越震荡，最后收敛不了——不是内存/磁盘问题。
- 验证 + 修复：单点测试 `#p uhf/cc-pVTZ guess=mix stable=opt scf=(xqc,tight)` 在 R=5.00 Å，
  能量比原来低 0.293 Hartree(≈769 kJ/mol)，`<S**2>` 从 0 变成 1.003——`stable=opt`（波函数稳定性
  检验，不稳定就自动跳到更低能量的解）才是真正管用的破对称手段。UB3LYP 这个体系反而不需要手动修，
  它在 R≈2.9 Å 附近自己"跳"过去了（DFT 比 HF 更容易自发破对称）。
- **新坑**：`stable=opt` 不能跟 `scan` 一起写（`CompJT: unrecognized IType=15`，秒退），
  也不能直接接在 `CCSD`/`CCSD(T)` 后面（`Unrecognized post-SCF IPrc10 in PutPrc`，秒退）——
  这个 Gaussian 版本（RevC.02）里 `stable=opt` 只支持配 HF/DFT 这类纯 SCF 方法的**单点**。
  要用在 post-HF 上，得分两步：先单独用 UHF+`stable=opt` 稳定化一次、存 `.chk`；
  再另开一个 job 用 `%oldchk=` 读那个**已经稳定的**参考态做 CCSD（不用再叫 `stable=opt`）。
  即使这样，`geom=check` 从一个 stable=opt 产生的 chk 读几何有时会报
  `Internal consistency failure #1 in ROv08`——保险起见几何坐标在新 job 里重新显式写一遍，
  别偷懒用 `geom=check`。
- 对付大规模 rigid scan：**一个点出错，整条 951 点的 scan 全部作废**（不是只丢那一个点）。
  时间紧的时候：与其死磕修好全曲线，不如老实报告"曲线算到哪个 R 为止、后面为什么算不了"，
  这本身就是单参考方法解离失败的真实案例，比一条"看起来很干净"但可能仍有问题的曲线更有说服力。

### 2026-09-13 · 用 Word COM (`InsertFile` / `SaveAs2`) 合并多个 docx 转 PDF 会莫名卡死

- 现象：PowerShell 里 `New-Object -ComObject Word.Application`，对同一个 Document 反复
  `Selection.InsertFile()` 插 5 个 docx 再 `SaveAs2` 存 PDF——CPU 一直在烧、`Responding=True`，
  但十几分钟都不出文件，不是卡死（还在跑），就是异常地慢。**同一个操作换一次单文件转 PDF
  又几秒钟就好**，复现不稳定，原因不明（可能跟嵌入图片多、或某个样式/域更新触发的重排版有关）。
- 解决（更稳，别再赌 InsertFile+多文件合并这条路）：
  1. **每个 docx 单独 `Documents.Open` → `SaveAs2(path, 17)` 转 PDF**，一个个来，不合并——
     这条路径每次都很快（几秒/文件），没再卡过。
  2. 转完各自的 PDF 后，用 Python **`pypdf`**（`pip install pypdf`）的 `PdfWriter().append()`
     把几个 PDF 合并成一个——纯 Python，不经过 Word，稳定快速。
  3. 如果后续还要能编辑的 **合并 Word 版**（不只是 PDF），用 `pip install docxcompose`：
     `docxcompose.composer.Composer` + `python-docx` 的 `add_page_break()`，同样不经过
     Word COM，一次成功，图片/表格都能正常带过去。
  4. 只需要"临时补一小段文字转 PDF"（比如加一页声明）时，**别为了几行字启动 Word**，
     用 `msedge --headless=new --no-pdf-header-footer --print-to-pdf=out.pdf <file-URI>`
     写个 HTML 直接转，几乎瞬间完成（`msedge.exe` 在
     `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`，不在默认 PATH 里）。
- 教训：Word COM 自动化能用，但**不可靠、容易莫名奇妙挂起且没有报错信息**，卡住了直接
  `Stop-Process` 杀掉换路子，别在同一个卡住的调用上反复等——这次等了三次、每次好几分钟才放弃。
