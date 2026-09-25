# image/percona-telemetry-disabled：遥测程序的空操作替代

[返回运行时目录](../README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[percona-telemetry-disabled](../../../../opt/hatch-image/bin/percona-telemetry-disabled#L1)。

遥测程序的空操作替代。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

脚本仅 exit 0；注释称通过 package diversion 防止软件包重装恢复遥测入口。

让已有调用无错误退出，同时不启动遥测进程。其效果依赖真实 diversion 安装状态。

<a id="bounds"></a>
## 失败路径与证据边界

不能从四行脚本证明整个系统没有任何遥测；只覆盖该稳定程序入口。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [percona-telemetry-disabled](../../../../opt/hatch-image/bin/percona-telemetry-disabled#L1) | 1 | 顺序脚本或声明配置 |

未在本次扫描的其他自有文本脚本中找到非注释引用；外部 systemd unit、镜像构建或二进制调用者不在这项搜索的证明范围。

<a id="migration"></a>
## 迁移与验证

迁移优先软件原生关闭设置；确需 wrapper 时记录替换路径与包升级行为。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../../09-validation.md)。
