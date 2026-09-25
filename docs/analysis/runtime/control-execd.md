# control-execd.sh：工具执行服务的独立入口

[返回运行时目录](README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[control-execd.sh](../../../opt/hatch/runtime-cell/control-execd.sh#L1)。

工具执行服务的独立入口。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

source 共享 entry helper，导入可信 guest.env，等 ready 与 Leader，直接 exec hatch-execd --runtime-cell-leader。保留 systemd LISTEN_* socket activation 环境。

与 daemon 共用就绪及环境逻辑，降低两个入口漂移。注释描述 host anchor 保持 service cgroup、child 进入 cell，避免用外部 nsenter wrapper 破坏 socket FD 生命周期。

<a id="bounds"></a>
## 失败路径与证据边界

源码只显示入口和 flags；fork、fd 转交、SO_PEERCRED 校验及 seccomp 机制均在缺失实现中。不要把注释当端到端隔离实测。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [control-execd.sh](../../../opt/hatch/runtime-cell/control-execd.sh#L1) | 1 | 顺序脚本或声明配置 |

未在本次扫描的其他自有文本脚本中找到非注释引用；外部 systemd unit、镜像构建或二进制调用者不在这项搜索的证明范围。

<a id="migration"></a>
## 迁移与验证

迁移时优先系统原生 socket activation，明确父子生命周期和 FD 所有权；应用层不要再搭重复进程监督器。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../09-validation.md)。
