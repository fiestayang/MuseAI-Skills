# etc/wgetrc：wget 的 TLS 信任默认

[返回运行时目录](../README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[wgetrc](../../../../opt/hatch/runtime-cell/etc/wgetrc#L1)。

wget 的 TLS 信任默认。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

为 wget 指向 runtime CA bundle，使 wget 与其他语言 HTTP 客户端采用一致证书根。

它是特定客户端补充配置；不能用它替代系统证书或强制网络出口。

<a id="bounds"></a>
## 失败路径与证据边界

文件依赖实际发布的 CA 路径，本快照没有可用于该环境的动态证书。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [wgetrc](../../../../opt/hatch/runtime-cell/etc/wgetrc#L1) | 1 | 顺序脚本或声明配置 |

仓库内文本引用（不是完整运行调用图；字符串也可能是模板内容）：

| 引用位置 | 原文 |
|---|---|
| [guest-runtime-env.sh](../../../../opt/hatch/runtime-cell/guest-runtime-env.sh#L58) | `export WGETRC="/opt/hatch/runtime-cell/etc/wgetrc"` |
| [guest.env](../../../../opt/hatch/runtime-cell/guest.env#L36) | `WGETRC=/opt/hatch/runtime-cell/etc/wgetrc` |

<a id="migration"></a>
## 迁移与验证

迁移保留证书验证，不用关闭 TLS 检查修复代理兼容问题。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../../09-validation.md)。
