# guest.env：宿主生成的可信 guest 环境值

[返回运行时目录](README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[guest.env](../../../opt/hatch/runtime-cell/guest.env#L1)。

宿主生成的可信 guest 环境值。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

提供静态代理、CA、路径和套接字变量，供两个 host controller 通过共享 helper 导出；与 guest-runtime-env 的交互式初始化用途不同。

配置文件是可 source 的代码形式，可信性来自宿主所有权与发布链，而非扩展名。为多语言工具建立同一出口及证书默认。

<a id="bounds"></a>
## 失败路径与证据边界

快照没有验证部署时权限或最终 override。home 路径是原 Linux 运行环境，不是读者当前电脑路径。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [guest.env](../../../opt/hatch/runtime-cell/guest.env#L1) | 1 | 顺序脚本或声明配置 |

仓库内文本引用（不是完整运行调用图；字符串也可能是模板内容）：

| 引用位置 | 原文 |
|---|---|
| [runtime-cell-entry.sh](../../../opt/hatch/runtime-cell/runtime-cell-entry.sh#L58) | `if [ -r "/opt/hatch/runtime-cell/guest.env" ]; then` |
| [runtime-cell-entry.sh](../../../opt/hatch/runtime-cell/runtime-cell-entry.sh#L59) | `. "/opt/hatch/runtime-cell/guest.env"` |

<a id="migration"></a>
## 迁移与验证

迁移可使用 service EnvironmentFile 或结构化配置；保持 override 顺序明确，避免同名环境键从低信任目录进入特权入口。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../09-validation.md)。
