# post-stop.sh：容器退出后的挂载与链路回收

[返回运行时目录](README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[post-stop.sh](../../../opt/hatch/runtime-cell/post-stop.sh#L1)。

容器退出后的挂载与链路回收。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

记录阶段开始，删除 ready；进入 PID 1 mount namespace 委派 rv-graft teardown whole-home bridge；有 timeout 才有界删除 veth；记录结束。

whole-home bridge 在 machine 完全停止后释放，避免仍运行 cell 失去数据路径。veth 清理失败不阻塞停机，下次 pre-start 再清理。

<a id="bounds"></a>
## 失败路径与证据边界

多处容忍失败意味着 completed 事件只证明脚本走到结束，不证明每个清理动作成功；观测者需同时检查日志与实际资源。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [emit_mount_stop_lifecycle_event](../../../opt/hatch/runtime-cell/post-stop.sh#L7) | 7 | 函数定义 |

未在本次扫描的其他自有文本脚本中找到非注释引用；外部 systemd unit、镜像构建或二进制调用者不在这项搜索的证明范围。

<a id="migration"></a>
## 迁移与验证

迁移将非关键清理设计为可重入，关键持久卷释放仍需检查真实引用与顺序。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../09-validation.md)。
