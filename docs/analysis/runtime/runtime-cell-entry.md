# runtime-cell-entry.sh：共享 Leader、环境和 namespace helper

[返回运行时目录](README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[runtime-cell-entry.sh](../../../opt/hatch/runtime-cell/runtime-cell-entry.sh#L1)。

共享 Leader、环境和 namespace helper。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

rce_runtime_cell_leader 查询并拒绝空或 0；rce_wait_for_ready_leader 轮询 ready marker 与非空 Leader，最多 200 次；rce_source_guest_env 导出可信配置；rce_join_cell_cgroup 解析 /proc cgroup 并写 cgroup.procs；rce_enter_guest_root 拒绝 preserve-credentials 后进入全部 namespace 并清组切 guest root。

namespace 视图与 cgroup 成员身份不是一件事，authd 文档要求两者对应。helper 避免 host launcher 读取 guest 可写环境脚本。

<a id="bounds"></a>
## 失败路径与证据边界

静态发现：wait 版本仅检查非空，没有与直接查询版本同样拒绝 Leader=0；这是条件不一致，实际触发概率及后果未做集成验证。cgroup 解析假定目标层级格式，不能无条件推广到所有宿主。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [rce_runtime_cell_leader](../../../opt/hatch/runtime-cell/runtime-cell-entry.sh#L12) | 12 | 函数定义 |
| [rce_wait_for_ready_leader](../../../opt/hatch/runtime-cell/runtime-cell-entry.sh#L29) | 29 | 函数定义 |
| [rce_source_guest_env](../../../opt/hatch/runtime-cell/runtime-cell-entry.sh#L56) | 56 | 函数定义 |
| [rce_join_cell_cgroup](../../../opt/hatch/runtime-cell/runtime-cell-entry.sh#L72) | 72 | 函数定义 |
| [rce_enter_guest_root](../../../opt/hatch/runtime-cell/runtime-cell-entry.sh#L98) | 98 | 函数定义 |

仓库内文本引用（不是完整运行调用图；字符串也可能是模板内容）：

| 引用位置 | 原文 |
|---|---|
| [control-daemon.sh](../../../opt/hatch/runtime-cell/control-daemon.sh#L28) | `. "/opt/hatch/runtime-cell/runtime-cell-entry.sh"` |
| [control-execd.sh](../../../opt/hatch/runtime-cell/control-execd.sh#L5) | `. "/opt/hatch/runtime-cell/runtime-cell-entry.sh"` |

<a id="migration"></a>
## 迁移与验证

迁移时把 Leader 验证收敛到一个共享判定并测试空、0、消失 PID；运行环境和授权身份分别校验。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../09-validation.md)。
