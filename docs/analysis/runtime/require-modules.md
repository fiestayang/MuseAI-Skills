# require-modules.sh：在单向锁定前准备内核模块

[返回运行时目录](README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[require-modules.sh](../../../opt/hatch/runtime-cell/require-modules.sh#L1)。

在单向锁定前准备内核模块。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

安装不需要模块的 deny 配置；清除旧 readiness markers；尝试加载 runtime 所需模块；有 browser cell 条件时准备 NAT 后端；按各组结果写成功标记。

post-start 只有看到预加载成功才写 modules_disabled；两份 marker 让主 runtime 与 browser NAT 准备状态不混淆。

<a id="bounds"></a>
## 失败路径与证据边界

禁模块是宿主级安全策略，不是每 skill 的功能配置；禁止名单有效性和内核编译形式需要目标 Linux 验证。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [require_runtime_module](../../../opt/hatch/runtime-cell/require-modules.sh#L34) | 34 | 函数定义 |
| [require_browser_module](../../../opt/hatch/runtime-cell/require-modules.sh#L42) | 42 | 函数定义 |

未在本次扫描的其他自有文本脚本中找到非注释引用；外部 systemd unit、镜像构建或二进制调用者不在这项搜索的证明范围。

<a id="migration"></a>
## 迁移与验证

迁移时只在专用受控主机采用不可逆模块锁，先盘点所有后续服务的依赖；普通开发环境不应照抄。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../09-validation.md)。
