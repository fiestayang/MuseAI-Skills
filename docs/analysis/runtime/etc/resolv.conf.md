# etc/resolv.conf：容器 DNS 模板

[返回运行时目录](../README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[resolv.conf](../../../../opt/hatch/runtime-cell/etc/resolv.conf#L1)。

容器 DNS 模板。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

提供运行环境的 resolver 参数；ensure-rootfs 修复 systemd-resolved stub symlink，保证只读 bind 落到正确文件。

将 guest DNS 默认固定到系统认可出口，避免启动时落在失效的 stub 路径。

<a id="bounds"></a>
## 失败路径与证据边界

DNS 配置成功不证明代理或权威 DNS 可用；实际响应需运行环境验证。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [resolv.conf](../../../../opt/hatch/runtime-cell/etc/resolv.conf#L1) | 1 | 顺序脚本或声明配置 |

仓库内文本引用（不是完整运行调用图；字符串也可能是模板内容）：

| 引用位置 | 原文 |
|---|---|
| [ensure-rootfs.sh](../../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L186) | `for _rf in "etc/hosts" "etc/resolv.conf"; do` |
| [ensure-rootfs.sh](../../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L195) | `safe_chmod 0644 "etc/hosts" "etc/resolv.conf"` |
| [ensure-rootfs.sh](../../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L196) | `guest_root_chown "etc/hosts" "etc/resolv.conf"` |

<a id="migration"></a>
## 迁移与验证

迁移区分配置就绪、DNS 可解析和目标服务可达三种健康状态。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../../09-validation.md)。
