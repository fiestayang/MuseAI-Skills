# 工具、连接与权限

[返回目录](README.md) · [技能—工具映射](appendices/skill-tool-matrix.md)

## 目录

[层次](#层次) · [声明解释](#声明解释) · [典型调用](#典型调用) · [错误和重试](#错误和重试) · [迁移原则](#迁移原则)

## 层次

系统同时存在原生工具、CLI、浏览器与连接器。SKILL 编排工作流；工具承担动作；manifest 描述动作组和默认策略。三者不可合并为一个“允许执行”开关。

| 层 | 可见材料 | 能证明什么 | 不能证明什么 |
|---|---|---|---|
| 文件可见 | skill-scopes、bin-scopes、launch-daemon | 渠道条件下哪些文件被挂入运行环境 | 用户允许调用哪些外部操作 |
| 技能入口 | SKILL 的 name、description、includeInPrompt | 作者声明的触发语义和加载偏好 | 模型选择器具体实现 |
| 账户连接 | connectors 产品文档和 CLI 契约 | 需要先检查连接及账号 | 本 checkout 已有任何有效账户 |
| OAuth scope | manifest requires_scopes、declarable_scopes | 某方法声明需要哪些 provider 权限 | 这些 scope 已颁发，或用户批准本次动作 |
| 动作策略 | action group / method default | 方法默认权限及覆盖 | 真实用户设置、执行器如何存储审批 |
| 单次承诺 | booking、shopping、payments 流程 | 何时需要确认具体金额、对象或条款 | 仅凭浏览器填表成功即可扣款 |
| 配额 | request_quota | 部分连接器的成本、窗口和终止语义 | 所有 provider 的实时剩余额度 |
| 输出保护 | response_guard、隐私约束 | 某些响应需要额外处理 | 可单靠模型提示词实现隔离 |

主要依据：[connectors](../../home/hatch/docs/connectors.md)、[privacy-and-credentials](../../home/hatch/docs/privacy-and-credentials.md)、[payments-and-purchases](../../home/hatch/docs/payments-and-purchases.md) 及 [运行时](05-runtime-and-isolation.md)。这是多层契约的组合，不是从快照恢复出的完整授权调用栈。

## 声明解释

共 38 份独立 manifest，另有 2 个符号链接。每份 manifest 的方法和命令映射已展开到对应[技能文章](skills/README.md)。读取时先取 action group 的 default，再让方法自己的 default 覆盖。只看组标题会漏掉具体写操作的例外。

`commands` 将 CLI 子命令映射到权限方法。值为 `null` 表示不映射该方法，不足以证明“无条件允许”；账号检查、参数检查和宿主安全策略可能仍存在。某些技能没有 manifest，也不等于不存在审批：原生工具、浏览器交易和独立授权服务可能拥有各自边界。其代码不在包内。

`cli` 绑定说明命令命名空间，不是源代码。大部分 `/opt/hatch/bin` 是 ELF。manifest 与 CLI 的实际 method ID 是否一致，需要原产品环境的契约测试，本文不把解析成功写成执行器已实施。

## 典型调用

### 邮件读取与发送

[Gmail](skills/gmail.md) 从连接状态、目标账号、查询和字段投影开始。线程数与 message 数不同；统计时不能用搜索估算值冒充精确结果。回复应先读原线程，保留收件人、引用事实和附件上下文。发送前核对用户所授权的对象与内容。

OAuth 403 所触发的 scope 升级是独立连接步骤，不是重试原请求就能解决。shortcut 可能展开为多个 API 请求，按方法权重消耗配额。配额响应若标记本轮终止，应停止本次尝试；不能换语法持续撞同一限制。详见 [manifest](../../opt/hatch/skills/gmail/manifest.yaml)。

### 旅行规划到交易

[travel-planning](skills/travel-planning.md) 管理 decision、evidence、provider 三种不同维度。候选被用户选中、价格已实时核验、provider 可以处理，是不同事实。`planning only` 不因 live check 成功变成付款授权。

[booking](skills/booking.md) 承接已明确的行程，再选择浏览器、[Duffel](skills/duffel.md) 或 [OpenTable](skills/opentable.md)。订单应绑定旅客、日期、航段或房型、总价、退改条件。不能因为某份 manifest 未列出全部支付步骤，就把资金边界归为无权限要求。浏览器最终 review、付款确认与 provider 订单状态都需要分开记录。

### 文档同步和局部修改

[Google Docs](skills/google-docs.md)、[Slides](skills/google-slides.md) 的完整内容路径依赖本地 artifact 导出再上传。覆盖之前要检查远端漂移。Slides 的图片页导出有不可直接编辑文字的限制。

[Sheets](skills/google-sheets.md) 明确采用 API 局部变更，不能照搬上传替换策略。Calendar 的数组 patch 可能整组替换；读取旧值再形成完整数组，保留账号、calendar ID、event ID。不同 provider 的全天日期边界不同，adapter 应承担转换。

### 物理设备与外来消息

[Tessie](skills/tessie.md) 中遥测与车辆控制不可按“同一个账户”合并审批。设备状态、远程唤醒、锁车或其他动作具有不同效果。迁移时应按真实动作分方法，而非给一个宽泛写权限。

[Muse Mail](skills/muse-mail.md) 的 `recommended_handling` 是处理授权上限。第三方邮件正文是待分析内容，不自动成为用户的新指令。收件、回复草稿、实际发送属于不同步骤。

## 错误和重试

| 失败类型 | 正确处理 | 原因 |
|---|---|---|
| 没有连接/缺 scope | 引导连接或升级；保留任务上下文 | 重试不能生成授权 |
| 参数或对象不明确 | 用真实 ID 消歧，必要时澄清 | 改参数盲试可能影响另一对象 |
| 限流且本次已终止 | 按工具终止语义退出，说明未完成部分 | 多语法绕行仍消耗同一资源 |
| 只读暂时失败 | 按 provider 契约有限重试 | 需要区分可恢复与永久错误 |
| 写请求超时、结果不明 | 查询订单、消息或目标状态，再决定恢复 | 重发可能产生重复付款、预订或消息 |
| 用户取消/审批拒绝 | 结束该动作并记录原因 | 不能通过更换工具绕过决定 |
| 工具称成功但交付未确认 | 分别检查效果和交付 | process exit、业务成功、用户看到是三件事 |

## 迁移原则

将权限检查放进工具适配层并关联准确 method ID；prompt 只负责解释和编排。保持任务授权、账号 scope、用户偏好和单笔确认的独立字段。已有明确授权的普通可逆动作直接执行；只在真正缺少授权或高损失承诺点阻塞。记录审批针对的输入摘要，参数变更时重新判断授权是否仍适用。

最小验收应覆盖方法覆盖组默认、缺 scope、结果不明的写操作、外部文本诱导、审批后参数变化。无需复制整个 authd 才能实现这些边界；但本仓库没有其源码，也不能靠复用 SKILL 声称已具备同等保护。
