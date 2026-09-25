# is-loopback-rv.sh：持久卷形态诊断

[返回运行时目录](README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[is-loopback-rv.sh](../../../opt/hatch/runtime-cell/is-loopback-rv.sh#L1)。

持久卷形态诊断。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

判断 /hatch 是否存在以及与根目录设备号关系，再查看挂载 backing device 是否为 loop；用不同退出码区分 loopback、真实卷、无卷和未知；解释只发 stderr。

以退出码承载多态结果，避免把“无法判断”误判为真实持久卷。当前 ensure-rootfs 对 overlayfs 使用它做诊断，其他文件系统才可能依赖判定。

<a id="bounds"></a>
## 失败路径与证据边界

头部关于 resolve-rootfs 调用者的注释已落后。该脚本依赖 Linux stat/mount 信息，macOS 语法检查不能证明实际判定正确。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [verdict](../../../opt/hatch/runtime-cell/is-loopback-rv.sh#L39) | 39 | 函数定义 |

仓库内文本引用（不是完整运行调用图；字符串也可能是模板内容）：

| 引用位置 | 原文 |
|---|---|
| [ensure-rootfs.sh](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L733) | `"/opt/hatch/runtime-cell/is-loopback-rv.sh" &#124;&#124; true` |
| [ensure-rootfs.sh](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L749) | `if ! "/opt/hatch/runtime-cell/is-loopback-rv.sh"; then` |
| [ensure-rootfs.sh](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L750) | `echo "runtime-cell bootstrap: $rootfs_parent is neither btrfs nor overlayfs ($rootfs_parent_fstype) and is-loopback-rv.sh did not confirm a loopback RV (reason above); refusing to link rootfs -> rootfs-base" >&2` |

<a id="migration"></a>
## 迁移与验证

迁移时显式返回 unknown，不把检测异常塞进 false；调用方要逐个处理退出码。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../09-validation.md)。
