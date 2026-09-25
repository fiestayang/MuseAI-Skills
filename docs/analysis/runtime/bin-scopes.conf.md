# bin-scopes.conf：独立的工具二进制渠道声明

[返回运行时目录](README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[bin-scopes.conf](../../../opt/hatch/runtime-cell/bin-scopes.conf#L1)。

独立的工具二进制渠道声明。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

每个 channel 可多行累加，所有行中出现的程序构成 gated set；构建期剥离到 host-only 目录，启动时按渠道 overlay 回平坦 PATH。

与 skill gate 是两条独立轴。隐藏 cell 二进制不代表 host worker 不存在，也不等于撤销底层能力。

<a id="bounds"></a>
## 失败路径与证据边界

文件注释称构建只检查工具确为 extension，不交叉校验 base skill 的依赖；这是一处明确维护风险。构建剥离脚本也缺失。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [bin-scopes.conf](../../../opt/hatch/runtime-cell/bin-scopes.conf#L1) | 1 | 顺序脚本或声明配置 |

仓库内文本引用（不是完整运行调用图；字符串也可能是模板内容）：

| 引用位置 | 原文 |
|---|---|
| [launch-daemon.sh](../../../opt/hatch/runtime-cell/launch-daemon.sh#L190) | `if [ -s "/opt/hatch/runtime-cell/bin-scopes.conf" ]; then` |
| [launch-daemon.sh](../../../opt/hatch/runtime-cell/launch-daemon.sh#L198) | `done < "/opt/hatch/runtime-cell/bin-scopes.conf"` |

<a id="migration"></a>
## 迁移与验证

迁移最小静态检查应验证每个可见 skill 的必要工具至少有一种可用路径。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../09-validation.md)。
