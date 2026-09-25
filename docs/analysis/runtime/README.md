# 运行时代码目录

[返回总目录](../README.md)

覆盖 runtime-cell 的 22 个文件及镜像侧 5 个可读脚本/清单。ELF 工具单列在 [二进制接口清单](../appendices/binaries.md)。

| 文件 | 职责 |
|---|---|
| [pre-start.sh](pre-start.md) | 启动前修复与宿主边界准备 |
| [launch-daemon.sh](launch-daemon.md) | 容器启动与两套渠道可见性合并 |
| [post-start.sh](post-start.md) | 网络策略就绪后发布 readiness |
| [control-daemon.sh](control-daemon.md) | 可信环境导入与 daemon 入口 |
| [control-execd.sh](control-execd.md) | 工具执行服务的独立入口 |
| [runtime-cell-entry.sh](runtime-cell-entry.md) | 共享 Leader、环境和 namespace helper |
| [guest-runtime-env.sh](guest-runtime-env.md) | guest 进程的环境配置 |
| [guest.env](guest.env.md) | 宿主生成的可信 guest 环境值 |
| [run-daemon.sh](run-daemon.md) | 保留的 guest 启动辅助路径 |
| [resolve-rootfs-path.sh](resolve-rootfs-path.md) | 固定运行根目录解析 |
| [ensure-rootfs.sh](ensure-rootfs.md) | 根文件系统创建、修复与版本切换 |
| [hatch-preflight-opportunistic](hatch-preflight-opportunistic.md) | 非阻塞包协调与 OS intent 重放 |
| [build-cell-trust-store.sh](build-cell-trust-store.md) | 宿主证书锚与只读 NSS 数据库发布 |
| [require-modules.sh](require-modules.md) | 在单向锁定前准备内核模块 |
| [is-loopback-rv.sh](is-loopback-rv.md) | 持久卷形态诊断 |
| [stop.sh](stop.md) | 有界停机与数据库完成证明 |
| [post-stop.sh](post-stop.md) | 容器退出后的挂载与链路回收 |
| [skill-scopes.conf](skill-scopes.conf.md) | 技能目录的渠道声明 |
| [bin-scopes.conf](bin-scopes.conf.md) | 独立的工具二进制渠道声明 |
| [etc/hosts](etc/hosts.md) | 容器内固定名称映射 |
| [etc/resolv.conf](etc/resolv.conf.md) | 容器 DNS 模板 |
| [etc/wgetrc](etc/wgetrc.md) | wget 的 TLS 信任默认 |
| [image/convert-cell-intent](image/convert-cell-intent.md) | 旧 rootfs 到包意图的单次转换 |
| [image/hatch-prewarm](image/hatch-prewarm.md) | 有时间和字节预算的页缓存预热 |
| [image/disabled-user-mgmt](image/disabled-user-mgmt.md) | 不可变镜像的账户管理拒绝入口 |
| [image/percona-telemetry-disabled](image/percona-telemetry-disabled.md) | 遥测程序的空操作替代 |
| [image/runtime-cell.kdl](image/runtime-cell.kdl.md) | 基础包与文件的声明式清单 |
