# image/disabled-user-mgmt：不可变镜像的账户管理拒绝入口

[返回运行时目录](../README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[disabled-user-mgmt](../../../../opt/hatch-image/bin/disabled-user-mgmt#L1)。

不可变镜像的账户管理拒绝入口。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

取调用名，向 stderr 说明用户与组在构建期配置，退出 1；用于替代运行时账号管理工具。

把不支持的系统变更明确失败，而非假装成功；原工具保留的 break-glass 路径由宿主运维控制。

<a id="bounds"></a>
## 失败路径与证据边界

只是拒绝 wrapper，安装替换逻辑与所有 alias 不在快照，不能据此证明所有账户修改路径都被封锁。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [disabled-user-mgmt](../../../../opt/hatch-image/bin/disabled-user-mgmt#L1) | 1 | 顺序脚本或声明配置 |

未在本次扫描的其他自有文本脚本中找到非注释引用；外部 systemd unit、镜像构建或二进制调用者不在这项搜索的证明范围。

<a id="migration"></a>
## 迁移与验证

迁移使用镜像构建声明用户，运行时服务只使用既有身份。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../../09-validation.md)。
