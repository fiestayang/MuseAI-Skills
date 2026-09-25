# resolve-rootfs-path.sh：固定运行根目录解析

[返回运行时目录](README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[resolve-rootfs-path.sh](../../../opt/hatch/runtime-cell/resolve-rootfs-path.sh#L1)。

固定运行根目录解析。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

接受兼容参数但始终输出 image-local /var/lib/hatch-runtime/rootfs；只向 stdout 输出路径，其余说明走 stderr。当前不再选择旧 RV serving tree。

这是一个纯路径协议，调用方通过命令替换直接使用结果；任何日志混入 stdout 都会破坏下游启动。

<a id="bounds"></a>
## 失败路径与证据边界

脚本保留的参数并不影响行为。is-loopback-rv 中声称本脚本使用它的注释已陈旧，应以实际调用为准。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [resolve-rootfs-path.sh](../../../opt/hatch/runtime-cell/resolve-rootfs-path.sh#L1) | 1 | 顺序脚本或声明配置 |

仓库内文本引用（不是完整运行调用图；字符串也可能是模板内容）：

| 引用位置 | 原文 |
|---|---|
| [ensure-rootfs.sh](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L595) | `rootfs=$("/opt/hatch/runtime-cell/resolve-rootfs-path.sh" "$rootfs")` |
| [launch-daemon.sh](../../../opt/hatch/runtime-cell/launch-daemon.sh#L34) | `rootfs=$("/opt/hatch/runtime-cell/resolve-rootfs-path.sh" "/var/lib/hatch-runtime/rootfs")` |
| [pre-start.sh](../../../opt/hatch/runtime-cell/pre-start.sh#L87) | `rootfs="$("/opt/hatch/runtime-cell/resolve-rootfs-path.sh" "/var/lib/hatch-runtime/rootfs")" &#124;&#124; {` |

<a id="migration"></a>
## 迁移与验证

迁移时路径解析函数只返回数据；诊断与机器接口分通道。固定需求无需通用策略工厂。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../09-validation.md)。
