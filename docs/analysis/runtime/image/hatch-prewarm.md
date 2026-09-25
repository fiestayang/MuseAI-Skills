# image/hatch-prewarm：有时间和字节预算的页缓存预热

[返回运行时目录](../README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[hatch-prewarm](../../../../opt/hatch-image/bin/hatch-prewarm#L1)。

有时间和字节预算的页缓存预热。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

收集 PostgreSQL 与宿主 nspawn 的受信 ldd 依赖，daemon 仅取文件本身；canonicalize、deny-filter、去重并逐文件计入 CAP_BYTES；超预算文件跳过但继续后续；vmtouch 只触页不锁页；限时执行并原子写 timing JSON。

将性能优化移出正确性依赖。ldd 会执行 ELF interpreter，因此仅用于 measured rootfs，不能对可更新 bundle 任意执行；该信任区分比“都先热一下”更关键。

<a id="bounds"></a>
## 失败路径与证据边界

缺工具、超时或预热失败均不该阻断启动。非 GNU 平台 timeout fallback 的约束不同；报告不把本机结果当生产性能数据。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [log](../../../../opt/hatch-image/bin/hatch-prewarm#L56) | 56 | 函数定义 |
| [with_deadline](../../../../opt/hatch-image/bin/hatch-prewarm#L61) | 61 | 函数定义 |
| [now_ms](../../../../opt/hatch-image/bin/hatch-prewarm#L74) | 74 | 函数定义 |
| [write_timing](../../../../opt/hatch-image/bin/hatch-prewarm#L89) | 89 | 函数定义 |
| [deny_listed](../../../../opt/hatch-image/bin/hatch-prewarm#L103) | 103 | 函数定义 |
| [add_file](../../../../opt/hatch-image/bin/hatch-prewarm#L122) | 122 | 函数定义 |
| [add_closure](../../../../opt/hatch-image/bin/hatch-prewarm#L150) | 150 | 函数定义 |
| [PostgreSQL server (measured rootfs): binary + loader/library closure.](../../../../opt/hatch-image/bin/hatch-prewarm#L162) | 162 | 阶段注释；需结合相邻实现 |
| [Hatch daemon (live-update bundle; unit is condition-gated on it).](../../../../opt/hatch-image/bin/hatch-prewarm#L168) | 168 | 阶段注释；需结合相邻实现 |
| [Cell boot files (identityless preboot): host nspawn closure plus the](../../../../opt/hatch-image/bin/hatch-prewarm#L177) | 177 | 阶段注释；需结合相邻实现 |

未在本次扫描的其他自有文本脚本中找到非注释引用；外部 systemd unit、镜像构建或二进制调用者不在这项搜索的证明范围。

<a id="migration"></a>
## 迁移与验证

迁移先测冷启动，再只预热证据支持的热点；保留 bytes/files/skipped 与时长，持续评估收益。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../../09-validation.md)。
