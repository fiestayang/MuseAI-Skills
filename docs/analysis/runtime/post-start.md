# post-start.sh：网络策略就绪后发布 readiness

[返回运行时目录](README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [函数与阶段补充](#implementation-details) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[post-start.sh](../../../opt/hatch/runtime-cell/post-start.sh#L1)。

网络策略就绪后发布 readiness。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

等待 host veth；设置 IPv4/IPv6 gateway 并拉起链路；attach-veth-filter；等待 machine Leader 与 guest host0；进入 net namespace 配置地址及默认路由；记录网络阶段；最后创建 ready marker；模块预加载成功时关闭后续内核模块加载。

readiness 在网络策略附加之后发布，避免服务早启动到未受控网络。两个阶段独立 failure reason，使“容器创建成功”与“可服务”可诊断。

<a id="bounds"></a>
## 失败路径与证据边界

BPF filter 实现不在源码；部分 ip addr 错误被容忍，最终路径依赖路由命令成功。modules_disabled 是宿主级单向锁，顺序要求 browser NAT 模块事先加载。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [queue_runtime_cell_bootstrap_phase](../../../opt/hatch/runtime-cell/post-start.sh#L17) | 17 | 函数定义 |
| [log_post_start](../../../opt/hatch/runtime-cell/post-start.sh#L36) | 36 | 函数定义 |
| [queue_post_start_failure](../../../opt/hatch/runtime-cell/post-start.sh#L40) | 40 | 函数定义 |
| [queue_ready_failure](../../../opt/hatch/runtime-cell/post-start.sh#L54) | 54 | 函数定义 |
| [wait_for_runtime_cell_leader](../../../opt/hatch/runtime-cell/post-start.sh#L68) | 68 | 函数定义 |
| [wait_for_guest_host0](../../../opt/hatch/runtime-cell/post-start.sh#L96) | 96 | 函数定义 |

未在本次扫描的其他自有文本脚本中找到非注释引用；外部 systemd unit、镜像构建或二进制调用者不在这项搜索的证明范围。

<a id="implementation-details"></a>
## 就绪判定细节

观测 helper 记录 network-ready 和 ready 两阶段及失败原因。`wait_for_runtime_cell_leader` 等有效 leader；`wait_for_guest_host0` 在 guest net namespace 等接口。有限等待解决设备创建时序，不能用无限 sleep 掩盖配置错误。

宿主先等 veth、配 gateway、拉起链路，再 attach-veth-filter。只有过滤器成功，才进入 guest 配地址和默认路由；最后发布 ready marker。ready 因而承诺的是这段网络准备已走过，不是每个 connector、数据库或 artifact 工具都健康。

内核 module 锁定发生在预加载成功之后。`modules_disabled` 是单向宿主状态，需要主 runtime 与浏览器 NAT 模块都已准备；不能在目标开发机作为通用开关试跑。

<a id="migration"></a>
## 迁移与验证

迁移先明确 ready 的实际保证，把 policy attach 放在 ready 前。重试应有上限且只用于尚未出现的基础设施，不吞掉关键策略错误。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../09-validation.md)。
