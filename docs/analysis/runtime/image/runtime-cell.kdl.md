# image/runtime-cell.kdl：基础包与文件的声明式清单

[返回运行时目录](../README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[runtime-cell.kdl](../../../../opt/hatch-image/bin/runtime-cell.kdl#L1)。

基础包与文件的声明式清单。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

声明 runtime-cell 所需 package/file，由 hatch-manifest 的协调阶段消费；与 base 镜像、用户 OS intent 重放分工。

清单提供期望状态，hatch-manifest 才执行差异收敛。脚本引用它不代表清单内资源全部存于仓库。

<a id="bounds"></a>
## 失败路径与证据边界

KDL 解析器和协调器源码未提供，不能验证全部 schema 约束或升级原子性。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [runtime-cell.kdl](../../../../opt/hatch-image/bin/runtime-cell.kdl#L1) | 1 | 顺序脚本或声明配置 |

仓库内文本引用（不是完整运行调用图；字符串也可能是模板内容）：

| 引用位置 | 原文 |
|---|---|
| [hatch-preflight-opportunistic](../../../../opt/hatch/runtime-cell/hatch-preflight-opportunistic#L268) | `manifest_hash_now="$(cat /opt/hatch-image/bin/runtime-cell.kdl /opt/hatch/bin/runtime-cell.kdl 2>/dev/null &#124; sha256sum &#124; cut -d" " -f1)"` |
| [hatch-preflight-opportunistic](../../../../opt/hatch/runtime-cell/hatch-preflight-opportunistic#L336) | `for cand in /opt/hatch-image/bin/runtime-cell.kdl /opt/hatch/bin/runtime-cell.kdl; do` |
| [hatch-preflight-opportunistic](../../../../opt/hatch/runtime-cell/hatch-preflight-opportunistic#L351) | `echo "preflight-opportunistic: no runtime-cell manifest found (/opt/hatch-image/manifests dir or runtime-cell.kdl)" >&2` |

<a id="migration"></a>
## 迁移与验证

迁移先使用目标发行版的原生包管理及一份小清单，不把包期望与用户业务状态混写。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../../09-validation.md)。
