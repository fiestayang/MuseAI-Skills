# pre-start.sh：启动前修复与宿主边界准备

[返回运行时目录](README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [函数与阶段补充](#implementation-details) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[pre-start.sh](../../../opt/hatch/runtime-cell/pre-start.sh#L1)。

启动前修复与宿主边界准备。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

宿主入口先 attach-cell-gate，失败直接停止；验证 rootfs 的 shell 和目录，必要时调用 ensure-rootfs；清理旧 machine/veth；在 PID 1 mount namespace 建 whole-home bridge 和 assets 发布；准备 pre-RV 的 os-intent、apt cache、resume、TLS 与 privsep bind sources；清除上代 ready/交接文件；发布阶段事件。

rootfs_is_ready 是快速结构检查，不等于重新计算 base digest。root-owned daemon-ctl 与 guest-owned socket 目录分离；mountpoint guard 防止重启时对已经 graft 的真实 RV 状态做 chown。assets 发布失败可保持服务可用，但单独记录退化。

<a id="bounds"></a>
## 失败路径与证据边界

spawnd 的 gate、fsop 与 rv-graft 是 ELF 调用，Shell 只能证明调用及错误处理，不能证明底层实现。脚本依赖 systemd/nspawn 和宿主 mounts，不适合在本机直接执行。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [queue_runtime_cell_bootstrap_phase](../../../opt/hatch/runtime-cell/pre-start.sh#L32) | 32 | 函数定义 |
| [queue_pre_start_failure](../../../opt/hatch/runtime-cell/pre-start.sh#L52) | 52 | 函数定义 |
| [fail_rootfs_not_ready](../../../opt/hatch/runtime-cell/pre-start.sh#L67) | 67 | 函数定义 |
| [rootfs_is_ready](../../../opt/hatch/runtime-cell/pre-start.sh#L86) | 86 | 函数定义 |
| [assert_rootfs_ready](../../../opt/hatch/runtime-cell/pre-start.sh#L118) | 118 | 函数定义 |
| [machine_exists](../../../opt/hatch/runtime-cell/pre-start.sh#L140) | 140 | 函数定义 |
| [machine_leader](../../../opt/hatch/runtime-cell/pre-start.sh#L144) | 144 | 函数定义 |
| [machine_leader_is_live](../../../opt/hatch/runtime-cell/pre-start.sh#L148) | 148 | 函数定义 |
| [wait_for_machine_gone](../../../opt/hatch/runtime-cell/pre-start.sh#L153) | 153 | 函数定义 |
| [clear_stale_machine_state](../../../opt/hatch/runtime-cell/pre-start.sh#L170) | 170 | 函数定义 |
| [Pre-RV bind sources ---](../../../opt/hatch/runtime-cell/pre-start.sh#L205) | 205 | 阶段注释；需结合相邻实现 |

未在本次扫描的其他自有文本脚本中找到非注释引用；外部 systemd unit、镜像构建或二进制调用者不在这项搜索的证明范围。

<a id="implementation-details"></a>
## 阶段及状态边界

`queue_runtime_cell_bootstrap_phase` 记录阶段，`queue_pre_start_failure` 补失败原因；`fail_rootfs_not_ready` 形成明确错误，避免后续挂载在半成品目录继续。`rootfs_is_ready` 是目录和可执行文件的快速判断，`assert_rootfs_ready` 决定是否需要完整 ensure；之后仍执行 repair-hosts-only 保持 resolver 等轻量配置收敛。

`machine_exists`、`machine_leader` 与 `machine_leader_is_live` 分别读注册、取 PID、验证 PID。`wait_for_machine_gone` 有界等待；`clear_stale_machine_state` 清理残留 machine 信息。机器注册与进程活性不同，不能只删一个文件就称旧 cell 已停。

顺序上先 attach-cell-gate，再做 rootfs 与 mount 准备；网络 gate 失败不能忽略。whole-home bridge 建在 PID 1 mount namespace，以便后续生命周期共享；assets 发布失败作为退化状态记录。pre-RV bind sources 为持久卷尚未 graft 时提供合法目录，mountpoint guard 防止对已挂入的真实用户状态再执行错误 chown。

最后清旧 ready 和生命周期交接文件，建立 root-owned daemon-ctl 数据通道。socket 目录与生命周期元数据目录分开，减少低信任服务通过可写目录注入宿主状态的机会。实际 spawnd 与 rv-graft 如何实施仍需其源码和部署测试。

<a id="migration"></a>
## 迁移与验证

迁移保留准备、就绪和退化状态，避免所有失败都当 fatal 或所有失败都忽略。不可执行检查与不可信 rootfs 变更应隔离，写操作使用持有目录 FD 的内核边界。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../09-validation.md)。
