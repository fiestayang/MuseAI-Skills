# control-daemon.sh：可信环境导入与 daemon 入口

[返回运行时目录](README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[control-daemon.sh](../../../opt/hatch/runtime-cell/control-daemon.sh#L1)。

可信环境导入与 daemon 入口。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

移除退休 launcher 但失败仅警告；建立 root-owned daemon-ctl；加载宿主 env、可信 guest.env，并再次让 env.override 覆盖；等待 ready 与 Leader；异步排空观测；从白名单文件逐项读生命周期值；记录宿主 boot ID；exec hatch daemon --runtime-cell-leader。

不再 source 来自 guest 可改目录的生命周期脚本，改为 root-owned 单键文件及 allowlist export；read -r 只接受首行普通数据。daemon namespace 进入由二进制自己完成。

<a id="bounds"></a>
## 失败路径与证据边界

注释中仍有到 run-daemon/nsenter 的旧路径描述，当前最后一行直接执行 hatch。不能按旧注释把 run-daemon 画成必经节点。宿主 boot ID 缺失的降级语义也仅由注释描述。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [emit_daemon_lifecycle_event](../../../opt/hatch/runtime-cell/control-daemon.sh#L51) | 51 | 函数定义 |
| [drain_shutdown_observability_async](../../../opt/hatch/runtime-cell/control-daemon.sh#L55) | 55 | 函数定义 |

仓库内文本引用（不是完整运行调用图；字符串也可能是模板内容）：

| 引用位置 | 原文 |
|---|---|
| [run-daemon.sh](../../../opt/hatch/runtime-cell/run-daemon.sh#L17) | `echo "note: run-daemon.sh: ready_file not visible inside cell namespace ($ready_file); control-daemon.sh already confirmed readiness host-side" >&2` |

<a id="migration"></a>
## 迁移与验证

迁移以结构化参数或可信文件传状态，禁止把低信任数据 source 成代码。保留实际入口命令与日志事件对应关系。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../09-validation.md)。
