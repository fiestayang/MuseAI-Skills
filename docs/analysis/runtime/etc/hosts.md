# etc/hosts：容器内固定名称映射

[返回运行时目录](../README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[hosts](../../../../opt/hatch/runtime-cell/etc/hosts#L1)。

容器内固定名称映射。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

提供本地和宿主代理等名称解析模板；ensure-rootfs 保证 bind 目标是普通文件，nspawn 再覆盖内容。

配置承担网络名字到受控地址的定位，不是服务发现或访问授权。

<a id="bounds"></a>
## 失败路径与证据边界

绑定配置及实际 host gateway 缺失时不能凭此保证可解析/可连接；更不能修改当前机器 hosts。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [hosts](../../../../opt/hatch/runtime-cell/etc/hosts#L1) | 1 | 顺序脚本或声明配置 |

仓库内文本引用（不是完整运行调用图；字符串也可能是模板内容）：

| 引用位置 | 原文 |
|---|---|
| [ensure-rootfs.sh](../../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L12) | `no_proxy_hosts="localhost,127.0.0.1,::1,[::1],$gateway_ip,$cell_ip,$gateway_ipv6,[$gateway_ipv6],$cell_ipv6,[$cell_ipv6]"` |
| [ensure-rootfs.sh](../../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L22) | `repair_hosts_only=0` |
| [ensure-rootfs.sh](../../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L26) | `--repair-hosts-only)` |
| [ensure-rootfs.sh](../../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L27) | `repair_hosts_only=1` |
| [ensure-rootfs.sh](../../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L30) | `echo "usage: $0 [--repair-hosts-only]" >&2` |
| [ensure-rootfs.sh](../../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L186) | `for _rf in "etc/hosts" "etc/resolv.conf"; do` |
| [ensure-rootfs.sh](../../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L195) | `safe_chmod 0644 "etc/hosts" "etc/resolv.conf"` |
| [ensure-rootfs.sh](../../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L196) | `guest_root_chown "etc/hosts" "etc/resolv.conf"` |
| [ensure-rootfs.sh](../../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L620) | `if [ "$repair_hosts_only" -eq 1 ]; then` |
| [ensure-rootfs.sh](../../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L1054) | `NO_PROXY=$no_proxy_hosts` |
| [ensure-rootfs.sh](../../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L1058) | `no_proxy=$no_proxy_hosts` |
| [ensure-rootfs.sh](../../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L1073) | `NO_PROXY=$no_proxy_hosts` |
| [ensure-rootfs.sh](../../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L1077) | `no_proxy=$no_proxy_hosts` |
| [ensure-rootfs.sh](../../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L1092) | `export NO_PROXY=$no_proxy_hosts` |
| [guest-runtime-env.sh](../../../../opt/hatch/runtime-cell/guest-runtime-env.sh#L8) | `no_proxy_hosts="localhost,127.0.0.1,::1,[::1],198.19.0.1,198.19.0.2,fd8b:4f84:7d32:99::1,[fd8b:4f84:7d32:99::1],fd8b:4f84:7d32:99::2,[fd8b:4f84:7d32:99::2]"` |
| [guest-runtime-env.sh](../../../../opt/hatch/runtime-cell/guest-runtime-env.sh#L50) | `export NO_PROXY="$no_proxy_hosts"` |
| [pre-start.sh](../../../../opt/hatch/runtime-cell/pre-start.sh#L204) | `"/opt/hatch/runtime-cell/ensure-rootfs.sh" --repair-hosts-only` |

<a id="migration"></a>
## 迁移与验证

迁移使代理名称与网络地址从同一配置生成，避免脚本和 hosts 手工漂移。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../../09-validation.md)。
