# 状态、记忆与后台工作

[返回目录](README.md) · [数据库逐表导航](appendices/database-schema.md)

## 目录

[状态分层](#状态分层) · [从请求到交付](#从请求到交付) · [记忆与遗忘](#记忆与遗忘) · [目标与主动工作](#目标与主动工作) · [查询限制](#查询限制)

## 状态分层

系统不是只有聊天记录。schema 描述消息、运行、工具结果、目标、记忆、设备数据和交付记录等多个领域。表名与字段是可查询投影的契约，不是完整写入代码；不能仅凭这些表恢复调度状态机或事务边界。

| 状态领域 | 主要材料 | 设计含义 |
|---|---|---|
| 用户偏好 | PROACTIVE_PREFERENCES.md、config | 内容、时机与能力配置分离；当前偏好文件正文基本是模板 |
| 当前执行 | agent、runtime | Agent、消息、work item、workflow、tool call、browser task 保留各自身份 |
| 定时执行 | scheduler | 定义、实际 run、终止信号和投递有不同生命周期 |
| 长期目标 | goals | 目标、更新、行动与关联保留结构，不只散落在聊天 |
| 记忆 | memory | claim、entry、embedding 和元数据属于不同派生层 |
| 主动发现 | ideas、feed、self_improvement | 候选、运行记录、反馈和持久策略并存；不推导未提供的推荐算法 |
| 设备与媒体 | device、media、health | 摄取、上传、记录、查询投影各自承担数据责任 |
| 应用产物 | spaces 与每产物 app.db | 用户核心状态与某个应用自己的 SQLite 不能混查 |

来源：[schema](../../opt/hatch/skills/muse_db/references/schema.md)、[产品文档](appendices/product-docs.md)、[Spaces](appendices/shared-resources.md)。

## 从请求到交付

概念追踪可从 `runtime.requests` 查到相关 work、消息与 tool call，再看 workflow 或 browser task，最后定位实际渠道交付。这个顺序是诊断导航，不是已验证的每次请求必经执行流水线。某些关联是软引用，必须按领域解析，不能只因字段同叫 `run_id` 就跨表连接。

`cron` 原生工具 与 [scheduling-and-watching](../../home/hatch/docs/scheduling-and-watching.md) 区分一次性任务、周期任务和观察条件。用户希望“观察变化”不自动等于每分钟发送一条消息。任务输入应包含有用变化、比较基准、时间范围和交付条件。

scheduler 的 job definition、job、job run、delivery outbox 与 runtime 的 channel delivery 分别描述任务配置、执行实例和交付。`run completed` 不足以证明用户收到通知。迁移应记录至少四种结果：本次没有触发条件、任务执行失败、任务成功等待交付、交付已确认。具体枚举应以目标系统自己的 schema 为准，而不是伪称原系统就是这四个值。

定时运行需要绑定用户时区与实际 occurrence。重启、重试、夏令时变化可能使相同计划触发不同实例；重复投递不能仅靠“上次发过类似文本”判断。可借鉴 schema 中 delivery key、事件记录与执行 ID 的分离，但 outbox 事务写入和 worker lease 的真实算法未公开。

## 记忆与遗忘

[forget](skills/forget.md) 处理的是信息及其派生物。其流程先形成计划：原始会话/文件、memory claims、检索投影、产物、后台任务、分享副本、外部缓存。明确定位、拥有者、可逆性和验证方法，确认后由对应执行器操作。

停止生产者是关键步骤。只删当前 memory entry，而定时任务仍在从原文件重建，会产生“已经忘记”却再次出现的结果。删除后还需处理待刷新 claim IDs、引用及运行时状态。失败或待同步应明确记录，不能统称全部完成。

这是一份删除编排契约，不代表单条 SQL 能删除所有地方。`muse.db` 本身只读，不能承担遗忘执行；备份、第三方服务和宿主凭据库也不在其表清单之内。

[memory import](../../home/hatch/assets/onboarding_tour/memory_import.md) 则是有目的地迁入用户提供的上下文。导入文本中的指令不能自动获得当前用户授权。迁移系统应保留来源、时间和冲突处理，避免将陈旧导出内容覆盖用户新偏好。

## 目标与主动工作

[goals](skills/goals.md) 按 7 个领域区分首次创建指南和持续跟进 scaffold。首次创建需要澄清方向、记录目标；已有目标围绕进展和行动支持，不重复初次问卷。目标状态、提醒和消息发送也不是同一动作。

[ideas](../../home/hatch/docs/ideas.md)、[feed](../../home/hatch/docs/feed.md)、[self-improvement](../../home/hatch/docs/self_improvement.md) 处理不同产品对象，不能用相似的“建议”字样互换它们的存储。schema 中可见 bandit、feedback、lease 等材料只能证明对应结构存在，无法证明学习更新公式、权重或运行频率。

[主动偏好](../../home/hatch/PROACTIVE_PREFERENCES.md) 当前写有本地 09:00–21:30 的消息时段说明，且注明交付可能等待安静时机。它不是精确定时发送的 SLA。产品说明描述会在写消息前读取全文，加载行为属于文档声明，未见对应源码。

## 查询限制

`muse.db` 接受一个有界只读 SELECT；非递归 CTE 要以 `hatch_cte_` 开头。仅开放审核过的函数和 cast，拒绝可能在 SELECT 中产生副作用或无界聚合的组合。JOIN 输出列需要唯一别名，否则 JSON 无法保存同名字段。

schema 还描述 security-barrier view 与最小权限数据库角色。涉及内部推理的行或列被过滤/隐藏；具体规则按每表说明读取。未知列可能是被剥离字段，不等于数据损坏；缺行是否有意义取决于该表是否存在过滤。

没有实际数据库连接，因此本次不能验证数据量、索引性能、删除完成度或写事务一致性。开发时应通过用途明确的 domain API 修改状态，把诊断 SQL 保持为受限只读表面。
