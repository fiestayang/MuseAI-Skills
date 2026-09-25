# skill-scopes.conf：技能目录的渠道声明

[返回运行时目录](README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[skill-scopes.conf](../../../opt/hatch/runtime-cell/skill-scopes.conf#L1)。

技能目录的渠道声明。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

按 channel 映射 scoped skill 目录名，由 launch-daemon 匹配后暴露；空或未知 channel 不增加任何 scoped 技能。

文件声明由 extensions_scoped.toml 生成，真实源文件不在快照。目录名与 frontmatter name 不同，不能按 name 直接查路径。

<a id="bounds"></a>
## 失败路径与证据边界

配置引用大量未附带的 skills-scoped，不表示当前 68 个技能之外的源已可分析。读取声明不证明部署渠道或用户权限。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [skill-scopes.conf](../../../opt/hatch/runtime-cell/skill-scopes.conf#L1) | 1 | 顺序脚本或声明配置 |

仓库内文本引用（不是完整运行调用图；字符串也可能是模板内容）：

| 引用位置 | 原文 |
|---|---|
| [launch-daemon.sh](../../../opt/hatch/runtime-cell/launch-daemon.sh#L101) | `if [ -s "/opt/hatch/runtime-cell/skill-scopes.conf" ]; then` |
| [launch-daemon.sh](../../../opt/hatch/runtime-cell/launch-daemon.sh#L109) | `done < "/opt/hatch/runtime-cell/skill-scopes.conf"` |

<a id="migration"></a>
## 迁移与验证

迁移使用一份权威注册表生成视图，避免手改生成物；未知渠道默认不加新能力。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../09-validation.md)。
