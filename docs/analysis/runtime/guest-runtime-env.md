# guest-runtime-env.sh：guest 进程的环境配置

[返回运行时目录](README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[guest-runtime-env.sh](../../../opt/hatch/runtime-cell/guest-runtime-env.sh#L1)。

guest 进程的环境配置。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

先保留继承的 sandbox API socket；source cell 内 env/override 后恢复该 socket；设置 JARVIS_HOME、工具目录、authd/proxy sockets、HOME/XDG、临时目录、代理大小写变量、各语言 CA 变量和 PATH。

同一代理同时覆盖 HTTP 库、Node、Git、AWS 等客户端；NODE_USE_ENV_PROXY 显式开启 Node 路由。socket 的继承优先防止 generic env 抹掉当前执行上下文。

<a id="bounds"></a>
## 失败路径与证据边界

这是 guest 内脚本，不应被 host root source；大小写代理变量一致仍不等于所有程序都无法直连，真正网络限制在宿主 gate。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [env_value_or_empty](../../../opt/hatch/runtime-cell/guest-runtime-env.sh#L10) | 10 | 函数定义 |

仓库内文本引用（不是完整运行调用图；字符串也可能是模板内容）：

| 引用位置 | 原文 |
|---|---|
| [run-daemon.sh](../../../opt/hatch/runtime-cell/run-daemon.sh#L20) | `. "/opt/hatch/runtime-cell/guest-runtime-env.sh"` |

<a id="migration"></a>
## 迁移与验证

迁移让工具运行环境集中产生，避免每个 skill 重复设置代理和凭据；安全边界不能只靠 env。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../09-validation.md)。
