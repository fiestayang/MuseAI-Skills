# tailscale：私有网络的受限 TCP 访问

[返回技能目录](README.md) · 基线 `61121abf5c4d`

目录：[职责与触发](#scope) · [执行流程](#flow) · [设计与边界](#design) · [逐文件分析](#files) · [权限契约](#permissions) · [评测](#eval) · [迁移指引](#migration) · [源码导航](#source)

<a id="scope"></a>
## 职责与触发

私有网络的受限 TCP 访问。入口：[SKILL.md](../../../opt/hatch/skills/tailscale/SKILL.md#L1)。

| 元数据 | 本地声明 |
|---|---|
| 目录标识 | `tailscale` |
| frontmatter name | `tailscale` |
| includeInPrompt | `false` |
| 独立正文 | 是；别名另列 |

原始触发描述（声明，不是已验证的匹配算法）：

> Set up Muse's built-in Tailscale connector, join a tailnet or Headscale network, check status, and reach private machines through the TCP tunnel proxy. Read for Tailscale, VPN, MagicDNS, network egress, exit-node, or browser routing questions and supported limits.

<a id="flow"></a>
## 执行流程与输入输出

先读产品网络说明；使用随包 tailscale 连接 Tailnet 或 Headscale；用户批准后 status；访问私有机器使用现有代理的 3130 端口；按实际 DNS 路由和 TCP 结果诊断。

<a id="design"></a>
## 实现思路、异常与限制

该客户端只出站、不承载入站服务；代理传输 TCP，不是把整个 Agent 网络切到 VPN。MagicDNS、split DNS 的能力作用于这条代理路径。

ping/UDP 失败不说明设备离线；浏览器、exit node 和全局路由能力需按文档限制解释。随包 CLI 不是让用户安装 upstream tailscaled 的指令。

实现可见性：本篇解读技能文本、配套声明及调用契约；除另有说明外，不代表已读取 CLI 内部源码或已实测服务。

<a id="files"></a>
## 逐文件分析

| 文件 | 作用、处理流程与阅读边界 |
|---|---|
| [SKILL.md](../../../opt/hatch/skills/tailscale/SKILL.md) | 主入口：触发元数据、任务分流与操作流程；按本篇流程和源码章节导航阅读。 |

<a id="permissions"></a>
## 工具与权限契约

目录未提供独立 manifest；不能据此认定没有授权检查。对应工具、宿主产品规则或交易系统仍可能实施审批。

<a id="eval"></a>
## 已有评测与覆盖

此技能目录没有独立 eval YAML。下方最小验收建议是迁移建议，不是仓库已有测试。

<a id="migration"></a>
## 迁移开发指引

迁移时将 network transport 作为显式依赖传入客户端，保留 TCP 与 DNS 失败原因，不用 ICMP 做唯一健康探针。

最小验收建议：TCP 可达但 ping 失败应判可用；普通出口不能访问 tailnet 时应选择正确代理而非重装客户端。

<a id="source"></a>
## 源码与配套章节导航

行号对应分析基线；本地阅读器若不支持 `#L`，可按同名标题定位。这里只列真实章节，不将代码示例里的注释误认为文档标题。

### SKILL.md

| 源章节 | 起始行 |
|---|---|
| [Tailscale](../../../opt/hatch/skills/tailscale/SKILL.md#L8) | 8 |
