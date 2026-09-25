# run-daemon.sh：保留的 guest 启动辅助路径

[返回运行时目录](README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[run-daemon.sh](../../../opt/hatch/runtime-cell/run-daemon.sh#L1)。

保留的 guest 启动辅助路径。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

guest 内检查 ready marker，不可见只记录诊断；加载 guest-runtime-env；通过 setpriv 去掉 sys_ptrace 的 bounding/inheritable/ambient capabilities 后运行 hatch daemon。

不重复把 host 已验证的 marker 在不同 mount namespace 中当硬门槛，减少启动抖动。能力裁剪在真正 exec 前完成。

<a id="bounds"></a>
## 失败路径与证据边界

当前 control-daemon 直接执行二进制，不调用本文件；它可能是兼容/诊断路径，不能确认线上仍被使用。保留文件不代表活跃调用链。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [run-daemon.sh](../../../opt/hatch/runtime-cell/run-daemon.sh#L1) | 1 | 顺序脚本或声明配置 |

未在本次扫描的其他自有文本脚本中找到非注释引用；外部 systemd unit、镜像构建或二进制调用者不在这项搜索的证明范围。

<a id="migration"></a>
## 迁移与验证

迁移以所有调用者核实旧入口是否还有用途，再考虑删除；不能仅凭名字猜主入口。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../09-validation.md)。
