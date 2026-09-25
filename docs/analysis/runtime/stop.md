# stop.sh：有界停机与数据库完成证明

[返回运行时目录](README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [函数与阶段补充](#implementation-details) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[stop.sh](../../../opt/hatch/runtime-cell/stop.sh#L1)。

有界停机与数据库完成证明。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

先发布 host drain fence，特定 operator brake 时清除 fence；支持只发布模式；清 ready 和交接状态；查询 machine/Leader；异步请求 poweroff 并限时等待；结合本代数据库 clean-stop proof 允许提前清理；随后 terminate、kill 分阶段升级，始终受停机预算约束。

数据库停止证明要来自当前 cell 生命周期，旧 inactive 状态不够。machinectl 请求与等待分离，防止一个卡住的客户端耗尽整个 systemd TimeoutStopSec。

<a id="bounds"></a>
## 失败路径与证据边界

清理 scope、卸载和进程 kill 有破坏性，本报告不执行。时间预算使用 date 毫秒读数，真正超时和信号传播需 Linux 集成验证；shell 代码存在不代表数据已安全落盘。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [log_stop](../../../opt/hatch/runtime-cell/stop.sh#L50) | 50 | 函数定义 |
| [emit_mount_stop_lifecycle_event](../../../opt/hatch/runtime-cell/stop.sh#L54) | 54 | 函数定义 |
| [emit_daemon_lifecycle_event](../../../opt/hatch/runtime-cell/stop.sh#L73) | 73 | 函数定义 |
| [read_machine_leader](../../../opt/hatch/runtime-cell/stop.sh#L77) | 77 | 函数定义 |
| [machine_leader_is_live](../../../opt/hatch/runtime-cell/stop.sh#L81) | 81 | 函数定义 |
| [start_machinectl_request](../../../opt/hatch/runtime-cell/stop.sh#L89) | 89 | 函数定义 |
| [finish_machinectl_request](../../../opt/hatch/runtime-cell/stop.sh#L94) | 94 | 函数定义 |
| [clear_stale_machine_state](../../../opt/hatch/runtime-cell/stop.sh#L109) | 109 | 函数定义 |
| [wait_for_machine_gone_until](../../../opt/hatch/runtime-cell/stop.sh#L121) | 121 | 函数定义 |
| [unit_active_state](../../../opt/hatch/runtime-cell/stop.sh#L138) | 138 | 函数定义 |
| [unit_monotonic_timestamp](../../../opt/hatch/runtime-cell/stop.sh#L143) | 143 | 函数定义 |
| [unit_is_running_or_stopping](../../../opt/hatch/runtime-cell/stop.sh#L153) | 153 | 函数定义 |
| [unit_is_inactive](../../../opt/hatch/runtime-cell/stop.sh#L161) | 161 | 函数定义 |
| [unit_was_active_in_current_cell](../../../opt/hatch/runtime-cell/stop.sh#L165) | 165 | 函数定义 |
| [unit_is_current_or_running](../../../opt/hatch/runtime-cell/stop.sh#L171) | 171 | 函数定义 |
| [arm_database_stop_shortcut](../../../opt/hatch/runtime-cell/stop.sh#L176) | 176 | 函数定义 |
| [database_stop_is_complete](../../../opt/hatch/runtime-cell/stop.sh#L199) | 199 | 函数定义 |
| [wait_for_graceful_machine_stop](../../../opt/hatch/runtime-cell/stop.sh#L208) | 208 | 函数定义 |
| [attempt_machine_terminate](../../../opt/hatch/runtime-cell/stop.sh#L241) | 241 | 函数定义 |
| [attempt_machine_kill](../../../opt/hatch/runtime-cell/stop.sh#L253) | 253 | 函数定义 |
| [fast_cleanup_machine](../../../opt/hatch/runtime-cell/stop.sh#L265) | 265 | 函数定义 |

未在本次扫描的其他自有文本脚本中找到非注释引用；外部 systemd unit、镜像构建或二进制调用者不在这项搜索的证明范围。

<a id="implementation-details"></a>
## 停机状态与函数细解

| 函数组 | 处理思路 | 返回/失败含义 |
|---|---|---|
| log_stop / emit_* | 记录 daemon 与 mount 生命周期 | 观测失败多为容忍分支，不改变真实机器状态 |
| read_machine_leader / machine_leader_is_live | 查询 machinectl，再排除空/0 并 kill -0 | 注册记录存在与 PID 活着分开 |
| start_machinectl_request / finish_machinectl_request | 请求在后台执行，按阶段轮询效果，结束后回收本地客户端 | kill 的是卡住的 machinectl 客户端；不是据其结束就认定 guest 已退出 |
| clear_stale_machine_state | 尽力 UnregisterMachine，删残留 machine/link/propagate | 清注册状态不等于干净停止数据库 |
| wait_for_machine_gone_until | 用截止时间查 leader 和活性，发现死 PID 后清陈旧注册 | 到期返回失败，供上层升级动作 |
| unit_active_state / unit_monotonic_timestamp | 查询 systemd 状态和单调时钟时间；异常时间归 0 | 0 不构成当前代的停止证明 |
| unit_is_running_or_stopping / unit_is_inactive | 区分 active、activating、reloading、deactivating 与 inactive | 只查 inactive 会误用旧代状态 |
| unit_was_active_in_current_cell / unit_is_current_or_running | 比较服务 ActiveExit 与当前 cell ActiveEnter | 建立本代相关性，防止旧停止记录放行新生命周期 |
| arm_database_stop_shortcut | postgres/proof 正运行时置 armed，或校验 target 本代停止与两个 unit 的本代归属 | 不能在缺少当前代证据时直接走快捷清理 |
| database_stop_is_complete | armed 且 postgres 与 proof 都 inactive | proof unit 的真正 fsync 和 ordering 属外部实现，源码此处只消费状态 |
| wait_for_graceful_machine_stop | 同时轮询 machine 与数据库停止，数据库完成后再给短暂宽限 | 0 为机器消失，1 为到期，2 为可采用数据库完成快捷路径 |
| attempt_machine_terminate / attempt_machine_kill | 分别使用独立预算执行 terminate 和 KILL，再核实机器消失 | 不让单个请求耗尽外层服务停机预算 |
| fast_cleanup_machine | 清陈旧状态，逐级强停，再尽力最终清理 | 末尾可返回 0，不能只凭此证明资源全部消失 |

默认 poweroff 预算 5 秒、数据库完成宽限 1 秒、检查间隔 500 ms、terminate 1 秒、kill 500 ms，来自脚本变量并可被环境覆盖。截止比较使用 wall-clock 毫秒读数；unit 归属判断使用 systemd 单调时间，两者承担不同用途。

<a id="migration"></a>
## 迁移与验证

迁移时明确拒绝新请求、排空、业务安全点、最终 kill 四个阶段；记录每一阶段结果，不用固定 sleep 代替状态证明。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../09-validation.md)。
