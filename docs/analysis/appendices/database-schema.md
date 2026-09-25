# 数据库逐表导航

[返回目录](../README.md) · [muse.db 技能](../skills/muse_db.md)

来源：[opt/hatch/skills/muse_db/references/schema.md](../../../opt/hatch/skills/muse_db/references/schema.md)。覆盖 195 个关系。该文件是生成的查询契约，migration-set fingerprint 为 `b502d161e045c1cd1ac4e973e3960739f366aca730006c32f4cb52a6997343dd`。没有数据库实例或 migrations 源码，因此以下是字段与关系分析，不是运行态数据审计。

## 查询边界

一个有界、只读 SELECT；必须用 schema-qualified 名称。非递归 CTE 名以 `hatch_cte_` 开头，禁止递归 CTE。函数和 cast 采取允许清单，不能因为是 SELECT 就允许任意 PostgreSQL 函数。`json_agg`、`jsonb_agg`、`array_agg`、`string_agg` 可能在外层限额之前形成无界值，因此不开放。多表投影需要唯一列别名。

credentials、系统目录、迁移记录、备份、Sentinel 独立审批库和每 artifact 的 app.db 不在表面内。Stripe Link spend 生命周期元数据不属于卡号或 CVC，部分可在 runtime 查询。不要把审批 ID 当成能从这里读取完整审批数据。

内部推理的脱敏规则按表声明。行过滤与列移除有不同失败表现：前者查不到行，后者查询该列报未知列。没有过滤说明时不能随意以“可能被隐藏”解释真实缺口。

## 关联方法

先根据用户问题确定领域，再选择真实 owner 表，检查主键、外键和 Identifier resolver index。软引用没有数据库外键的完整性保证；同名 `run_id`、`event_id`、`action_id` 可能属于不同领域。外部 opaque ID 没有本地 owner，不应猜测 JOIN。

下文每表列出全部可见字段（类型；是否允许空），键和原始脱敏说明。字段用途先按明确标识语义读取；领域/命名推断只是阅读导航，不代表已恢复写入代码。行号定位保留在每节来源链接。

## 领域目录

- [activity](#domain-activity)：8 个关系。面向用户的活动线程、章节和动作视图；关联执行记录用于解释进度，不等于底层任务已经完成。
- [agent](#domain-agent)：26 个关系。Agent 身份、会话、上下文、压缩、子任务通信和恢复归属；注意当前投影对内部推理的隐藏。
- [device](#domain-device)：13 个关系。配对设备、同步状态、联系人、日历和通信数据；区分设备内部标识与外部 provider ID。
- [feed](#domain-feed)：16 个关系。Feed 内容、运行、用户交互与共享分发记录；生成、收取和投递是不同阶段。
- [goals](#domain-goals)：12 个关系。目标、关联、行动、更新和进展；目标父子关系不应与通用 Agent 父子关系混用。
- [health](#domain-health)：8 个关系。摄取后的健康记录、数值、聚合、睡眠和训练；单位、时间和来源决定可比较性，表存在不保证完整样本。
- [ideas](#domain-ideas)：22 个关系。建议、卡片、来源、排序状态和反馈；可观察排序相关状态，无法由表恢复模型和学习公式。
- [ingest](#domain-ingest)：1 个关系。源数据事件摄取与归属；摄取存在不证明所有下游投影更新成功。
- [media](#domain-media)：4 个关系。媒体实体、描述、位置和 EXIF；元数据、媒体字节和分享范围需要分别确认。
- [memory](#domain-memory)：6 个关系。记忆 claims、entries、索引与模型元数据；删除主项后还要考虑派生索引和重新生产。
- [messages](#domain-messages)：1 个关系。消息相关持久状态；以字段声明的真实 owner 解析，不以字段名猜测连接。
- [podcasts](#domain-podcasts)：3 个关系。节目、feed 与 episode 身份；本地生成、上传 provider 和发布不是同一状态。
- [runtime](#domain-runtime)：41 个关系。请求、工作、消息、调用、浏览器、付款及交付状态；业务对象和执行实例需保留各自 ID。
- [scheduler](#domain-scheduler)：12 个关系。任务定义、发生实例、调度事件、恢复与交付；排队、成功执行和送达分别追踪。
- [self_improvement](#domain-self_improvement)：12 个关系。后台学习、目标研究、关系整理、反馈与交接记录；证据链与最终建议内容分离。
- [shell](#domain-shell)：1 个关系。用户壳层状态；按 source 与 item key 解读，不视为任意文件系统镜像。
- [spaces](#domain-spaces)：9 个关系。应用/产物身份、动作、提案和分享等主库元数据；不包含每产物 app.db 的内部业务表。

<a id="domain-activity"></a>
## activity

面向用户的活动线程、章节和动作视图；关联执行记录用于解释进度，不等于底层任务已经完成。

### activity.activity_monitor_agent_threads

来源：[activity.activity_monitor_agent_threads](../../../opt/hatch/skills/muse_db/references/schema.md#L246)。可见字段 4 个。

阅读重点：从 `created_at`, `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `agent_id` | `text` | no |  | Local row identifier (primary key). |
| `activity_thread_id` | `text` | no |  | Potential local reference; resolve by domain context in: `activity.activity_monitor_thread_sections.activity_thread_id`, `activity.activity_monitor_threads.activity_thread_id`. |
| `created_at` | `text` | no |  |  |
| `updated_at` | `text` | no |  |  |

键与约束：

- PRIMARY KEY `activity_monitor_agent_threads_pkey`: `agent_id`

### activity.activity_monitor_carrier_user_messages

来源：[activity.activity_monitor_carrier_user_messages](../../../opt/hatch/skills/muse_db/references/schema.md#L259)。可见字段 5 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 3 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `link_seq` | `bigint` | no | `nextval('activity.activity_monitor_carrier_user_messages_link_seq_seq'::regclass)` | Local row identifier (primary key). |
| `carrier_message_id` | `text` | no |  | Soft local reference → `runtime.messages.message_id`. |
| `user_message_id` | `text` | no |  | Soft local reference → `runtime.messages.message_id`. |
| `root_agent_id` | `text` | yes |  | Soft local reference → `agent.agents.agent_id`. |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `activity_monitor_carrier_user_messages_pkey`: `link_seq`
- UNIQUE `activity_monitor_carrier_user_carrier_message_id_user_messa_key`: `carrier_message_id`, `user_message_id`

### activity.activity_monitor_message_threads

来源：[activity.activity_monitor_message_threads](../../../opt/hatch/skills/muse_db/references/schema.md#L274)。可见字段 4 个。

阅读重点：从 `created_at`, `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `message_id` | `text` | no |  | Local row identifier (primary key). |
| `activity_thread_id` | `text` | no |  | Potential local reference; resolve by domain context in: `activity.activity_monitor_thread_sections.activity_thread_id`, `activity.activity_monitor_threads.activity_thread_id`. |
| `created_at` | `text` | no |  |  |
| `updated_at` | `text` | no |  |  |

键与约束：

- PRIMARY KEY `activity_monitor_message_threads_pkey`: `message_id`

### activity.activity_monitor_runtime_work_threads

来源：[activity.activity_monitor_runtime_work_threads](../../../opt/hatch/skills/muse_db/references/schema.md#L287)。可见字段 4 个。

阅读重点：从 `created_at`, `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `work_id` | `text` | no |  | Local row identifier (primary key). |
| `activity_thread_id` | `text` | no |  | FK → `activity.activity_monitor_threads.activity_thread_id` |
| `created_at` | `text` | no |  |  |
| `updated_at` | `text` | no |  |  |

键与约束：

- FOREIGN KEY `activity_monitor_runtime_work_threads_goal_id_fkey`: `activity_thread_id` → `activity.activity_monitor_threads` (`activity_thread_id`)
- PRIMARY KEY `activity_monitor_runtime_work_threads_pkey`: `work_id`

### activity.activity_monitor_thread_actions

来源：[activity.activity_monitor_thread_actions](../../../opt/hatch/skills/muse_db/references/schema.md#L301)。可见字段 18 个。

阅读重点：从 `status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `action_seq` | `bigint` | no | `nextval('activity.activity_monitor_thread_actions_action_seq_seq'::regclass)` |  |
| `action_id` | `text` | no |  | Local row identifier (primary key). |
| `activity_thread_id` | `text` | no |  | Potential local reference; resolve by domain context in: `activity.activity_monitor_thread_sections.activity_thread_id`, `activity.activity_monitor_threads.activity_thread_id`. |
| `action_index` | `bigint` | no |  |  |
| `agent_id` | `text` | yes |  | Soft local reference → `agent.agents.agent_id`. |
| `agent_depth` | `integer` | yes |  |  |
| `icon` | `text` | no |  |  |
| `title` | `text` | no |  |  |
| `subtitle` | `text` | yes |  |  |
| `report` | `text` | no |  |  |
| `status` | `text` | no |  |  |
| `created_at` | `text` | no |  |  |
| `section_key` | `text` | yes |  |  |
| `section_title` | `text` | yes |  |  |
| `section_order` | `integer` | yes |  |  |
| `section_depth` | `integer` | yes |  |  |
| `parent_section_key` | `text` | yes |  |  |
| `ordinal_label` | `text` | yes |  |  |

键与约束：

- PRIMARY KEY `activity_monitor_thread_actions_pkey`: `action_id`
- UNIQUE `activity_monitor_thread_actions_action_seq_key`: `action_seq`

### activity.activity_monitor_thread_sections

来源：[activity.activity_monitor_thread_sections](../../../opt/hatch/skills/muse_db/references/schema.md#L329)。可见字段 10 个。

阅读重点：从 `status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `activity_thread_id` | `text` | no |  | FK → `activity.activity_monitor_threads.activity_thread_id` |
| `section_key` | `text` | no |  | Local row identifier (primary key). |
| `title` | `text` | no |  |  |
| `status` | `text` | no |  |  |
| `section_order` | `integer` | yes |  |  |
| `section_depth` | `integer` | yes |  |  |
| `parent_section_key` | `text` | yes |  |  |
| `ordinal_label` | `text` | yes |  |  |
| `created_at` | `text` | no |  |  |
| `updated_at` | `text` | no |  |  |

键与约束：

- FOREIGN KEY `activity_monitor_thread_sections_goal_id_fkey`: `activity_thread_id` → `activity.activity_monitor_threads` (`activity_thread_id`)
- PRIMARY KEY `activity_monitor_thread_sections_pkey`: `activity_thread_id`, `section_key`

### activity.activity_monitor_threads

来源：[activity.activity_monitor_threads](../../../opt/hatch/skills/muse_db/references/schema.md#L349)。可见字段 16 个。

阅读重点：从 `status_title`, `status`, `finish_status`, `finish_status_reason` 检查状态或失败信息；字段存在不说明允许哪些状态转换。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `activity_thread_id` | `text` | no |  | Local row identifier (primary key). |
| `name` | `text` | no |  |  |
| `subtitle` | `text` | no |  |  |
| `status_title` | `text` | yes |  |  |
| `icon` | `text` | no |  |  |
| `emoji` | `text` | yes |  |  |
| `activity_thread_kind` | `text` | yes |  |  |
| `space_slug` | `text` | yes |  |  |
| `expected_finish_description` | `text` | yes |  |  |
| `status` | `text` | no |  |  |
| `finish_status` | `text` | yes |  |  |
| `finish_status_reason` | `text` | yes |  |  |
| `created_at` | `text` | no |  |  |
| `finished_at` | `text` | yes |  |  |
| `finish_message` | `text` | yes |  |  |
| `artifact_slug` | `text` | yes |  |  |

键与约束：

- PRIMARY KEY `activity_monitor_threads_pkey`: `activity_thread_id`

### activity.feed_entries

来源：[activity.feed_entries](../../../opt/hatch/skills/muse_db/references/schema.md#L374)。可见字段 16 个。

阅读重点：从 `status_title`, `status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `activity_key` | `text` | no |  | Local row identifier (primary key). |
| `activity_type` | `text` | no |  |  |
| `is_goal` | `boolean` | no | `false` |  |
| `message_id` | `text` | yes |  | Soft local reference → `runtime.messages.message_id`. |
| `title` | `text` | yes |  |  |
| `status_title` | `text` | yes |  |  |
| `subtitle` | `text` | yes |  |  |
| `details_json` | `text` | yes |  |  |
| `status` | `text` | no |  |  |
| `task_label` | `text` | yes |  |  |
| `created_at_ms` | `bigint` | no |  |  |
| `updated_at_ms` | `bigint` | no |  |  |
| `finished_at_ms` | `bigint` | yes |  |  |
| `created_at` | `timestamp with time zone` | yes |  |  |
| `updated_at` | `timestamp with time zone` | yes |  |  |
| `finished_at` | `timestamp with time zone` | yes |  |  |

键与约束：

- PRIMARY KEY `feed_entries_pkey`: `activity_key`

<a id="domain-agent"></a>
## agent

Agent 身份、会话、上下文、压缩、子任务通信和恢复归属；注意当前投影对内部推理的隐藏。

### agent.agent_ancestors

来源：[agent.agent_ancestors](../../../opt/hatch/skills/muse_db/references/schema.md#L401)。可见字段 3 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `descendant_id` | `text` | no |  | Local row identifier (primary key). |
| `ancestor_id` | `text` | no |  | Local row identifier (primary key). |
| `distance` | `integer` | no |  |  |

键与约束：

- PRIMARY KEY `agent_ancestors_pkey`: `descendant_id`, `ancestor_id`

### agent.agent_compactions

来源：[agent.agent_compactions](../../../opt/hatch/skills/muse_db/references/schema.md#L413)。可见字段 11 个。

脱敏契约：Redacted. The compaction detail payload is withheld because it carries the model reasoning retained across the checkpoint. Queries against this table run against the security-barrier view `inspection.agent_compactions`, which projects the columns listed below. Withheld columns: `details_json`.

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `id` | `bigint` | no | `nextval('agent.agent_compactions_id_seq'::regclass)` | Local row identifier (primary key). |
| `agent_id` | `text` | no |  | Soft local reference → `agent.agents.agent_id`. |
| `summary` | `text` | no |  |  |
| `first_kept_seq` | `bigint` | yes |  |  |
| `checkpoint_seq` | `bigint` | yes |  |  |
| `tokens_before` | `bigint` | yes |  |  |
| `tokens_after` | `bigint` | yes |  |  |
| `trigger` | `text` | no |  |  |
| `will_retry` | `boolean` | no | `false` |  |
| `created_at` | `bigint` | no |  |  |
| `has_replacement_history` | `boolean` | no | `false` |  |

键与约束：

- PRIMARY KEY `agent_compactions_pkey`: `id`

### agent.agent_message_token_usage

来源：[agent.agent_message_token_usage](../../../opt/hatch/skills/muse_db/references/schema.md#L435)。可见字段 5 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `agent_id` | `text` | no |  | Local row identifier (primary key). |
| `message_id` | `text` | no |  | Local row identifier (primary key). |
| `input_tokens` | `bigint` | no |  |  |
| `output_tokens` | `bigint` | no |  |  |
| `created_at` | `bigint` | no |  |  |

键与约束：

- PRIMARY KEY `agent_message_token_usage_pkey`: `agent_id`, `message_id`

### agent.agents

来源：[agent.agents](../../../opt/hatch/skills/muse_db/references/schema.md#L449)。可见字段 22 个。

阅读重点：从 `status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 6 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `agent_id` | `text` | no |  | Local row identifier (primary key). |
| `id` | `text` | yes |  | Legacy local agent identity owned by this row; `agent.agents.parent_id` points here. |
| `session_id` | `text` | yes |  | Soft local reference → `agent.sessions.session_id`. |
| `kind` | `text` | no | `'root'::text` |  |
| `parent_id` | `text` | yes |  | Soft local reference → `agent.agents.id`. |
| `parent_agent_id` | `text` | yes |  | Soft local reference → `agent.agents.agent_id`. |
| `root_session_id` | `text` | yes |  | Soft local reference → `agent.sessions.session_id`. |
| `request_id` | `text` | yes |  | FK → `runtime.requests.request_id` |
| `model` | `text` | no | `''::text` |  |
| `status` | `text` | no |  |  |
| `depth` | `integer` | no | `0` |  |
| `created_at` | `bigint` | no | `(EXTRACT(epoch FROM now()))::bigint` |  |
| `updated_at` | `bigint` | no | `(EXTRACT(epoch FROM now()))::bigint` |  |
| `last_assistant_message` | `text` | yes |  |  |
| `seen_at_ms` | `bigint` | yes |  |  |
| `prompt_floor_seq` | `bigint` | yes |  |  |
| `ephemeral` | `boolean` | no | `false` |  |
| `last_assistant_resources` | `text` | yes |  |  |
| `agent_type` | `text` | yes |  |  |
| `presentation_root_session_id` | `text` | yes |  | Soft local reference → `agent.sessions.session_id`. |
| `spawn_metadata_json` | `text` | yes |  |  |
| `originating_location_context_json` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `agents_request_id_fkey`: `request_id` → `runtime.requests` (`request_id`)
- PRIMARY KEY `agents_pkey`: `agent_id`
- UNIQUE `agents_id_key`: `id`

### agent.chat_preferences

来源：[agent.chat_preferences](../../../opt/hatch/skills/muse_db/references/schema.md#L482)。可见字段 5 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `id` | `integer` | no |  | Local row identifier (primary key). |
| `active_root_id` | `text` | no |  | Soft local reference → `agent.agents.id`. |
| `verbose` | `bigint` | no | `0` |  |
| `usage_mode` | `text` | no | `'off'::text` |  |
| `active_root_cleared_at_ms` | `bigint` | yes |  |  |

键与约束：

- PRIMARY KEY `chat_preferences_pkey`: `id`

### agent.compactions

来源：[agent.compactions](../../../opt/hatch/skills/muse_db/references/schema.md#L496)。可见字段 7 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `compaction_id` | `bigint` | no | `nextval('agent.compactions_compaction_id_seq'::regclass)` | Local row identifier (primary key). |
| `agent_id` | `text` | no |  | Soft local reference → `agent.agents.agent_id`. |
| `checkpoint_context_item_id` | `bigint` | yes |  | FK → `agent.context_items.context_item_id` |
| `replacement_history_first_seq` | `integer` | yes |  |  |
| `replacement_history_last_seq` | `integer` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `summary_text` | `text` | no |  |  |

键与约束：

- FOREIGN KEY `compactions_checkpoint_context_item_id_fkey`: `checkpoint_context_item_id` → `agent.context_items` (`context_item_id`)
- PRIMARY KEY `compactions_pkey`: `compaction_id`

### agent.context_item_derived_write_backlog

来源：[agent.context_item_derived_write_backlog](../../../opt/hatch/skills/muse_db/references/schema.md#L513)。可见字段 6 个。

阅读重点：从 `attempts`, `last_error` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `context_item_id` | `bigint` | no |  | FK → `agent.context_items.context_item_id` |
| `attempts` | `integer` | no | `0` |  |
| `last_error` | `text` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |
| `deadlettered_at` | `timestamp with time zone` | yes |  |  |

键与约束：

- FOREIGN KEY `context_item_derived_write_backlog_context_item_id_fkey`: `context_item_id` → `agent.context_items` (`context_item_id`)
- PRIMARY KEY `context_item_derived_write_backlog_pkey`: `context_item_id`

### agent.context_item_fields

来源：[agent.context_item_fields](../../../opt/hatch/skills/muse_db/references/schema.md#L529)。可见字段 6 个。

脱敏契约：Redacted. Legacy field rows whose owning item is model reasoning (thinking or redacted-thinking) are withheld. Queries against this table run against the security-barrier view `inspection.context_item_fields`, which projects the columns listed below.

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `context_item_field_id` | `bigint` | no | `nextval('agent.context_item_fields_context_item_field_id_seq'::regclass)` | Local row identifier (primary key). |
| `context_item_id` | `bigint` | no |  | FK → `agent.context_items.context_item_id` |
| `field_path` | `text` | no |  |  |
| `scalar_type` | `text` | no |  |  |
| `scalar_value` | `text` | yes |  |  |
| `field_text_content` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `context_item_fields_context_item_id_fkey`: `context_item_id` → `agent.context_items` (`context_item_id`)
- PRIMARY KEY `context_item_fields_pkey`: `context_item_field_id`
- UNIQUE `context_item_fields_context_item_id_field_path_key`: `context_item_id`, `field_path`

### agent.context_item_resume_projection

来源：[agent.context_item_resume_projection](../../../opt/hatch/skills/muse_db/references/schema.md#L548)。可见字段 12 个。

脱敏契约：Redacted. Rows projected from model-reasoning items (thinking or redacted-thinking) are withheld, and the legacy item copy is withheld because it can hold model reasoning. Queries against this table run against the security-barrier view `inspection.context_item_resume_projection`, which projects the columns listed below. Withheld columns: `item_json`.

阅读重点：从 `created_at`, `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `agent_id` | `text` | no |  | Local row identifier (primary key). |
| `seq` | `bigint` | no |  | Local row identifier (primary key). |
| `context_item_id` | `bigint` | yes |  | FK → `agent.context_items.context_item_id` |
| `created_at` | `bigint` | yes |  |  |
| `message_source` | `text` | yes |  |  |
| `client_context_json` | `text` | yes |  |  |
| `reply_prefix` | `text` | yes |  |  |
| `provenance_json` | `text` | yes |  |  |
| `client_context_projected` | `boolean` | no | `false` |  |
| `reply_prefix_projected` | `boolean` | no | `false` |  |
| `provenance_projected` | `boolean` | no | `false` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `context_item_resume_projection_context_item_id_fkey`: `context_item_id` → `agent.context_items` (`context_item_id`)
- PRIMARY KEY `context_item_resume_projection_pkey`: `agent_id`, `seq`

### agent.context_items

来源：[agent.context_items](../../../opt/hatch/skills/muse_db/references/schema.md#L572)。可见字段 21 个。

脱敏契约：Redacted. Rows holding model reasoning (thinking and redacted-thinking items) are withheld; commentary text stays readable. Queries against this table run against the security-barrier view `inspection.context_items`, which projects the columns listed below.

阅读重点：从 `created_at`, `data_cleanup_checked_at`, `data_summarized_at`, `data_expires_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 5 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `context_item_id` | `bigint` | no | `nextval('agent.context_items_context_item_id_seq'::regclass)` | Local row identifier (primary key). |
| `agent_id` | `text` | no |  | Soft local reference → `agent.agents.agent_id`. |
| `seq` | `bigint` | no |  |  |
| `item_kind` | `agent.context_item_kind` | no |  |  |
| `message_id` | `text` | yes |  | FK → `runtime.messages.message_id` |
| `tool_call_id` | `bigint` | yes |  | FK → `runtime.tool_calls.tool_call_id` |
| `tool_output_id` | `bigint` | yes |  | FK → `runtime.tool_outputs.tool_output_id` |
| `role` | `runtime.message_role` | yes |  |  |
| `call_id` | `text` | yes |  | Soft local reference to `runtime.workflow_agent_calls.call_id`. |
| `tool_name` | `text` | yes |  |  |
| `success` | `boolean` | yes |  |  |
| `message_source` | `text` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `data_fbids` | `bigint[]` | yes |  |  |
| `data_message_ids` | `text[]` | yes |  | Source-system message identifiers carried for retention cleanup; resolve them from the context item's provenance, not by assuming runtime message ids. |
| `data_cleanup_checked_at` | `timestamp with time zone` | yes |  |  |
| `data_summarized_at` | `timestamp with time zone` | yes |  |  |
| `data_thread_ids` | `text[]` | yes |  | Source-system thread identifiers carried for retention cleanup; no single Muse PostgreSQL owner table. |
| `data_expires_at` | `timestamp with time zone` | yes |  |  |
| `text_content` | `text` | yes |  |  |
| `item_json` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `context_items_message_id_fkey`: `message_id` → `runtime.messages` (`message_id`)
- FOREIGN KEY `context_items_tool_call_id_fkey`: `tool_call_id` → `runtime.tool_calls` (`tool_call_id`)
- FOREIGN KEY `context_items_tool_output_id_fkey`: `tool_output_id` → `runtime.tool_outputs` (`tool_output_id`)
- PRIMARY KEY `context_items_pkey`: `context_item_id`
- UNIQUE `context_items_agent_id_seq_key`: `agent_id`, `seq`

### agent.context_text_segments

来源：[agent.context_text_segments](../../../opt/hatch/skills/muse_db/references/schema.md#L608)。可见字段 4 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `context_text_segment_id` | `bigint` | no | `nextval('agent.context_text_segments_context_text_segment_id_seq'::regclass)` | Local row identifier (primary key). |
| `context_item_id` | `bigint` | no |  | FK → `agent.context_items.context_item_id` |
| `ordinal` | `integer` | no |  |  |
| `text_content` | `text` | no |  |  |

键与约束：

- FOREIGN KEY `context_text_segments_context_item_id_fkey`: `context_item_id` → `agent.context_items` (`context_item_id`)
- PRIMARY KEY `context_text_segments_pkey`: `context_text_segment_id`
- UNIQUE `context_text_segments_context_item_id_ordinal_key`: `context_item_id`, `ordinal`

### agent.message_mailbox

来源：[agent.message_mailbox](../../../opt/hatch/skills/muse_db/references/schema.md#L623)。可见字段 14 个。

阅读重点：从 `state` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 3 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `submission_id` | `text` | no |  | Local row identifier (primary key). |
| `accepted_ordinal` | `bigint` | no |  |  |
| `agent_id` | `text` | no |  | FK → `agent.agents.agent_id` |
| `conversation_epoch` | `bigint` | no |  |  |
| `submission_kind` | `text` | no |  |  |
| `routing_scope` | `text` | no |  |  |
| `state` | `text` | no |  |  |
| `stream_owner_message_id` | `text` | yes |  | Soft local reference → `runtime.messages.message_id`. |
| `submission_json` | `text` | no |  |  |
| `transcript_event_seq` | `bigint` | yes |  | FK → `runtime.events.event_seq` |
| `accepted_at` | `timestamp with time zone` | no | `now()` |  |
| `attached_at` | `timestamp with time zone` | yes |  |  |
| `terminalized_at` | `timestamp with time zone` | yes |  |  |
| `checkpoint_custody` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `message_mailbox_agent_id_fkey`: `agent_id` → `agent.agents` (`agent_id`)
- FOREIGN KEY `message_mailbox_transcript_event_seq_fkey`: `transcript_event_seq` → `runtime.events` (`event_seq`)
- PRIMARY KEY `message_mailbox_pkey`: `submission_id`
- UNIQUE `message_mailbox_agent_id_conversation_epoch_accepted_ordina_key`: `agent_id`, `conversation_epoch`, `accepted_ordinal`

### agent.recovery_owner_terminal_events

来源：[agent.recovery_owner_terminal_events](../../../opt/hatch/skills/muse_db/references/schema.md#L649)。可见字段 5 个。

阅读重点：从 `claimed_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `recovery_class` | `text` | no |  | FK → `agent.recovery_owners.recovery_class` |
| `owner_id` | `text` | no |  | FK → `agent.recovery_owners.owner_id` |
| `generation` | `bigint` | no |  | Local row identifier (primary key). |
| `event_type` | `text` | no |  | Local row identifier (primary key). |
| `claimed_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `recovery_owner_terminal_events_recovery_class_owner_id_fkey`: `recovery_class`, `owner_id` → `agent.recovery_owners` (`recovery_class`, `owner_id`)
- PRIMARY KEY `recovery_owner_terminal_events_pkey`: `recovery_class`, `owner_id`, `generation`, `event_type`

### agent.recovery_owners

来源：[agent.recovery_owners](../../../opt/hatch/skills/muse_db/references/schema.md#L664)。可见字段 8 个。

阅读重点：从 `terminal_status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `recovery_class` | `text` | no |  | Local row identifier (primary key). |
| `owner_id` | `text` | no |  | Local row identifier (primary key). |
| `generation` | `bigint` | no | `1` |  |
| `agent_id` | `text` | no |  | Soft local reference → `agent.agents.agent_id`. |
| `message_id` | `text` | no |  | Soft local reference → `runtime.messages.message_id`. |
| `active_at` | `timestamp with time zone` | no | `now()` |  |
| `terminal_at` | `timestamp with time zone` | yes |  |  |
| `terminal_status` | `text` | yes |  |  |

键与约束：

- PRIMARY KEY `recovery_owners_pkey`: `recovery_class`, `owner_id`
- UNIQUE `recovery_owners_agent_id_key`: `agent_id`

### agent.runtime_restart_checkpoints

来源：[agent.runtime_restart_checkpoints](../../../opt/hatch/skills/muse_db/references/schema.md#L682)。可见字段 8 个。

阅读重点：从 `created_at`, `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `agent_id` | `text` | no |  | Local row identifier (primary key). |
| `mode` | `text` | no |  |  |
| `payload_json` | `text` | yes |  |  |
| `created_at` | `bigint` | no |  |  |
| `updated_at` | `bigint` | no |  |  |
| `recovery_class` | `text` | yes |  |  |
| `recovery_owner_id` | `text` | yes |  | Soft local reference → `agent.recovery_owners.owner_id`. |
| `execution_config_json` | `text` | yes |  |  |

键与约束：

- PRIMARY KEY `runtime_restart_checkpoints_pkey`: `agent_id`

### agent.runtime_state

来源：[agent.runtime_state](../../../opt/hatch/skills/muse_db/references/schema.md#L699)。可见字段 4 个。

阅读重点：从 `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `agent_id` | `text` | no |  | Local row identifier (primary key). |
| `current_context_seq` | `integer` | no | `0` |  |
| `last_event_seq` | `bigint` | yes |  | FK → `runtime.events.event_seq` |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `runtime_state_last_event_seq_fkey`: `last_event_seq` → `runtime.events` (`event_seq`)
- PRIMARY KEY `runtime_state_pkey`: `agent_id`

### agent.session_memory_capture_deadlines

来源：[agent.session_memory_capture_deadlines](../../../opt/hatch/skills/muse_db/references/schema.md#L713)。可见字段 6 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `root_session_id` | `text` | no |  | FK → `agent.agents.agent_id` |
| `session_id` | `text` | yes |  | Soft local reference → `agent.sessions.session_id`. |
| `reason` | `text` | no |  |  |
| `due_at_ms` | `bigint` | no |  |  |
| `created_at_ms` | `bigint` | no |  |  |
| `updated_at_ms` | `bigint` | no |  |  |

键与约束：

- FOREIGN KEY `session_memory_capture_deadlines_root_session_id_fkey`: `root_session_id` → `agent.agents` (`agent_id`)
- PRIMARY KEY `session_memory_capture_deadlines_pkey`: `root_session_id`

### agent.session_metadata

来源：[agent.session_metadata](../../../opt/hatch/skills/muse_db/references/schema.md#L729)。可见字段 15 个。

阅读重点：从 `status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `session_id` | `text` | no |  | Local row identifier (primary key). |
| `origin` | `text` | no |  |  |
| `lifecycle` | `text` | no |  |  |
| `status` | `text` | no |  |  |
| `thread_title` | `text` | yes |  |  |
| `source_session_id` | `text` | yes |  | Soft local reference → `agent.sessions.session_id`. |
| `source_prompt_seq_upper_bound` | `bigint` | yes |  |  |
| `source_message_id_boundary` | `text` | yes |  |  |
| `created_at` | `bigint` | no |  |  |
| `updated_at` | `bigint` | no |  |  |
| `pinned` | `boolean` | no | `false` |  |
| `channel` | `text` | yes |  |  |
| `channel_conversation_id` | `text` | yes |  | External channel-provider conversation identifier; no Muse PostgreSQL owner table. |
| `channel_delivery_target` | `text` | yes |  |  |
| `pinned_order` | `bigint` | yes |  |  |

键与约束：

- PRIMARY KEY `session_metadata_pkey`: `session_id`

### agent.sessions

来源：[agent.sessions](../../../opt/hatch/skills/muse_db/references/schema.md#L753)。可见字段 5 个。

阅读重点：从 `created_at`, `updated_at`, `archived_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `session_id` | `text` | no |  | Local row identifier (primary key). |
| `root_request_id` | `text` | yes |  | FK → `runtime.requests.request_id` |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |
| `archived_at` | `timestamp with time zone` | yes |  |  |

键与约束：

- FOREIGN KEY `sessions_root_request_id_fkey`: `root_request_id` → `runtime.requests` (`request_id`)
- PRIMARY KEY `sessions_pkey`: `session_id`

### agent.subagent_monitor_decisions

来源：[agent.subagent_monitor_decisions](../../../opt/hatch/skills/muse_db/references/schema.md#L768)。可见字段 15 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 6 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `decision_id` | `bigint` | no | `nextval('agent.subagent_monitor_decisions_decision_id_seq'::regclass)` | Local row identifier (primary key). |
| `coordinator_agent_id` | `text` | no |  | Soft local reference → `agent.agents.agent_id`. |
| `child_agent_id` | `text` | no |  | Soft local reference → `agent.agents.agent_id`. |
| `parent_agent_id` | `text` | no |  | Soft local reference → `agent.agents.agent_id`. |
| `parent_message_id` | `text` | no |  | Soft local reference → `runtime.messages.message_id`. |
| `monitor_event_id` | `bigint` | no |  | Local monitor-event reference; use `monitor_event_kind` to resolve `agent.subagent_progress_message_events.event_id` or `agent.subagent_progress_tool_events.event_id`. |
| `monitor_event_kind` | `text` | no |  |  |
| `inference_request_id` | `text` | no |  | Inference/telemetry correlation identifier; no Muse PostgreSQL owner table. |
| `assistant_text` | `text` | yes |  |  |
| `tool_call_id` | `text` | yes |  | Soft local reference → `runtime.tool_calls.tool_call_id`. |
| `tool_name` | `text` | yes |  |  |
| `tool_arguments` | `text` | yes |  |  |
| `tool_result_json` | `text` | no |  |  |
| `decision_kind` | `text` | no |  |  |
| `created_at` | `bigint` | no |  |  |

键与约束：

- PRIMARY KEY `subagent_monitor_decisions_pkey`: `decision_id`
- UNIQUE `subagent_monitor_decisions_inference_request_id_key`: `inference_request_id`

### agent.subagent_progress

来源：[agent.subagent_progress](../../../opt/hatch/skills/muse_db/references/schema.md#L793)。可见字段 6 个。

阅读重点：从 `status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `progress_id` | `bigint` | no | `nextval('agent.subagent_progress_progress_id_seq'::regclass)` | Local row identifier (primary key). |
| `child_agent_id` | `text` | no |  | Soft local reference → `agent.agents.agent_id`. |
| `event_seq` | `bigint` | yes |  | FK → `runtime.events.event_seq` |
| `status` | `text` | no |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `progress_text` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `subagent_progress_event_seq_fkey`: `event_seq` → `runtime.events` (`event_seq`)
- PRIMARY KEY `subagent_progress_pkey`: `progress_id`

### agent.subagent_progress_message_events

来源：[agent.subagent_progress_message_events](../../../opt/hatch/skills/muse_db/references/schema.md#L809)。可见字段 7 个。

阅读重点：从 `delivered_at` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 3 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `event_id` | `bigint` | no | `nextval('agent.subagent_progress_message_events_event_id_seq'::regclass)` | Local row identifier (primary key). |
| `child_agent_id` | `text` | no |  | Soft local reference → `agent.agents.agent_id`. |
| `parent_agent_id` | `text` | no |  | Soft local reference → `agent.agents.agent_id`. |
| `parent_message_id` | `text` | no |  | Soft local reference → `runtime.messages.message_id`. |
| `message_text` | `text` | no |  |  |
| `created_at` | `bigint` | no |  |  |
| `delivered_at` | `bigint` | yes |  |  |

键与约束：

- PRIMARY KEY `subagent_progress_message_events_pkey`: `event_id`

### agent.subagent_progress_tool_events

来源：[agent.subagent_progress_tool_events](../../../opt/hatch/skills/muse_db/references/schema.md#L825)。可见字段 11 个。

阅读重点：从 `tool_status`, `delivered_at` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 3 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `event_id` | `bigint` | no | `nextval('agent.subagent_progress_tool_events_event_id_seq'::regclass)` | Local row identifier (primary key). |
| `child_agent_id` | `text` | no |  | Soft local reference → `agent.agents.agent_id`. |
| `parent_agent_id` | `text` | no |  | Soft local reference → `agent.agents.agent_id`. |
| `parent_message_id` | `text` | no |  | Soft local reference → `runtime.messages.message_id`. |
| `tool_name` | `text` | no |  |  |
| `tool_description` | `text` | no |  |  |
| `tool_status` | `text` | no |  |  |
| `tool_result_preview` | `text` | yes |  |  |
| `created_at` | `bigint` | no |  |  |
| `delivered_at` | `bigint` | yes |  |  |
| `run_id` | `text` | yes |  | Producer-specific tool or workflow run identifier; no single owner table. |

键与约束：

- PRIMARY KEY `subagent_progress_tool_events_pkey`: `event_id`

### agent.subagent_spawns

来源：[agent.subagent_spawns](../../../opt/hatch/skills/muse_db/references/schema.md#L845)。可见字段 21 个。

阅读重点：从 `status`, `deferred_terminal_status`, `completed_at` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 8 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `spawn_id` | `bigint` | no | `nextval('agent.subagent_spawns_spawn_id_seq'::regclass)` | Local row identifier (primary key). |
| `parent_agent_id` | `text` | no |  | Soft local reference → `agent.agents.agent_id`. |
| `child_agent_id` | `text` | no |  | Soft local reference → `agent.agents.agent_id`. |
| `parent_message_id` | `text` | yes |  | Soft local reference → `runtime.messages.message_id`. |
| `parent_request_id` | `text` | yes |  | Soft local reference → `runtime.requests.request_id`. |
| `root_request_id` | `text` | yes |  | Soft local reference → `runtime.requests.request_id`. |
| `root_message_execution_id` | `text` | yes |  | Soft local reference → `runtime.messages.message_id`. |
| `request_id` | `text` | yes |  | FK → `runtime.requests.request_id` |
| `created_at` | `bigint` | no | `(EXTRACT(epoch FROM now()))::bigint` |  |
| `status` | `text` | yes |  |  |
| `deferred_terminal_status` | `text` | yes |  |  |
| `final_response` | `text` | yes |  |  |
| `completed_at` | `bigint` | yes |  |  |
| `prompt` | `text` | yes |  |  |
| `requester_source` | `text` | yes |  |  |
| `requester_channel_context_json` | `text` | yes |  |  |
| `seen_at` | `bigint` | yes |  |  |
| `child_depth` | `integer` | no | `0` |  |
| `agent_type` | `text` | yes |  |  |
| `metadata_json` | `text` | yes |  |  |
| `spawn_call_id` | `text` | yes |  | Soft local reference → `runtime.tool_calls.tool_call_id`. |

键与约束：

- FOREIGN KEY `subagent_spawns_request_id_fkey`: `request_id` → `runtime.requests` (`request_id`)
- PRIMARY KEY `subagent_spawns_pkey`: `spawn_id`
- UNIQUE `subagent_spawns_child_agent_id_key`: `child_agent_id`
- UNIQUE `subagent_spawns_parent_agent_id_child_agent_id_key`: `parent_agent_id`, `child_agent_id`

### agent.token_usage

来源：[agent.token_usage](../../../opt/hatch/skills/muse_db/references/schema.md#L878)。可见字段 8 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `token_usage_id` | `bigint` | no | `nextval('agent.token_usage_token_usage_id_seq'::regclass)` | Local row identifier (primary key). |
| `agent_id` | `text` | no |  | Soft local reference → `agent.agents.agent_id`. |
| `request_id` | `text` | yes |  | FK → `runtime.requests.request_id` |
| `input_tokens` | `integer` | no | `0` |  |
| `output_tokens` | `integer` | no | `0` |  |
| `cached_input_tokens` | `integer` | no | `0` |  |
| `reasoning_tokens` | `integer` | no | `0` |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `token_usage_request_id_fkey`: `request_id` → `runtime.requests` (`request_id`)
- PRIMARY KEY `token_usage_pkey`: `token_usage_id`

### agent.volatile_context_pins

来源：[agent.volatile_context_pins](../../../opt/hatch/skills/muse_db/references/schema.md#L896)。可见字段 7 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `agent_id` | `text` | no |  | Local row identifier (primary key). |
| `variant_hash` | `text` | no |  | Local row identifier (primary key). |
| `variant_json` | `text` | no |  |  |
| `prompt_floor_seq` | `bigint` | no |  |  |
| `checkpoint_seq` | `bigint` | no |  |  |
| `body` | `text` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `volatile_context_pins_pkey`: `agent_id`, `variant_hash`

<a id="domain-device"></a>
## device

配对设备、同步状态、联系人、日历和通信数据；区分设备内部标识与外部 provider ID。

### device.calendar_events

来源：[device.calendar_events](../../../opt/hatch/skills/muse_db/references/schema.md#L914)。可见字段 18 个。

阅读重点：从 `event_status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `node_id` | `text` | no |  | FK → `device.nodes.node_id` |
| `external_event_id` | `text` | no |  | Local row identifier (primary key). |
| `title` | `text` | no |  |  |
| `start_at` | `timestamp with time zone` | no |  |  |
| `end_at` | `timestamp with time zone` | no |  |  |
| `is_all_day` | `boolean` | no |  |  |
| `external_calendar_id` | `text` | no |  | External/provider identifier; no Muse PostgreSQL owner table. |
| `calendar_name` | `text` | no |  |  |
| `availability` | `text` | no |  |  |
| `location` | `text` | yes |  |  |
| `notes` | `text` | yes |  |  |
| `time_zone` | `text` | yes |  |  |
| `start_local_date` | `date` | yes |  |  |
| `end_local_date` | `date` | yes |  |  |
| `is_recurring` | `boolean` | no |  |  |
| `url` | `text` | yes |  |  |
| `event_status` | `text` | no |  |  |
| `calendar_color` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `calendar_events_node_id_fkey`: `node_id` → `device.nodes` (`node_id`)
- PRIMARY KEY `calendar_events_pkey`: `node_id`, `external_event_id`

### device.call_log

来源：[device.call_log](../../../opt/hatch/skills/muse_db/references/schema.md#L942)。可见字段 10 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `call_log_id` | `bigint` | no | `nextval('device.call_log_call_log_id_seq'::regclass)` | Local row identifier (primary key). |
| `producer_id` | `text` | no |  | Source-producer identifier supplied with device data; no standalone owner table. |
| `external_id` | `text` | no |  | External/provider identifier; no Muse PostgreSQL owner table. |
| `phone_number` | `text` | yes |  |  |
| `contact_name` | `text` | yes |  |  |
| `call_type` | `text` | yes |  |  |
| `occurred_at_unix_ms` | `bigint` | yes |  |  |
| `duration_seconds` | `bigint` | yes |  |  |
| `platform` | `text` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `call_log_pkey`: `call_log_id`
- UNIQUE `call_log_producer_id_external_id_key`: `producer_id`, `external_id`

### device.client_contexts

来源：[device.client_contexts](../../../opt/hatch/skills/muse_db/references/schema.md#L962)。可见字段 14 个。

阅读重点：从 `presence_status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `connection_id` | `text` | no |  | Local row identifier (primary key). |
| `device_id` | `text` | no |  | Client-supplied device identifier; distinct from `device.nodes.node_id`. |
| `session_id` | `text` | yes |  | Soft local reference → `agent.sessions.session_id`. |
| `root_session_id` | `text` | yes |  | Soft local reference → `agent.sessions.session_id`. |
| `platform` | `text` | yes |  |  |
| `view` | `text` | yes |  |  |
| `mode` | `text` | yes |  |  |
| `is_visible` | `boolean` | yes | `true` |  |
| `presence_status` | `text` | no |  |  |
| `metadata_json` | `jsonb` | yes |  |  |
| `connected_at_ms` | `bigint` | no |  |  |
| `last_active_at_ms` | `bigint` | no |  |  |
| `updated_at_ms` | `bigint` | no |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `client_contexts_pkey`: `connection_id`

### device.contact_addresses

来源：[device.contact_addresses](../../../opt/hatch/skills/muse_db/references/schema.md#L985)。可见字段 8 个。

阅读重点：从 `state` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `contact_address_id` | `bigint` | no | `nextval('device.contact_addresses_contact_address_id_seq'::regclass)` | Local row identifier (primary key). |
| `contact_id` | `bigint` | no |  | FK → `device.contacts.contact_id` |
| `label` | `text` | yes |  |  |
| `street` | `text` | yes |  |  |
| `city` | `text` | yes |  |  |
| `state` | `text` | yes |  |  |
| `postal_code` | `text` | yes |  |  |
| `country` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `contact_addresses_contact_id_fkey`: `contact_id` → `device.contacts` (`contact_id`)
- PRIMARY KEY `contact_addresses_pkey`: `contact_address_id`

### device.contact_emails

来源：[device.contact_emails](../../../opt/hatch/skills/muse_db/references/schema.md#L1003)。可见字段 4 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `contact_email_id` | `bigint` | no | `nextval('device.contact_emails_contact_email_id_seq'::regclass)` | Local row identifier (primary key). |
| `contact_id` | `bigint` | no |  | FK → `device.contacts.contact_id` |
| `label` | `text` | yes |  |  |
| `email` | `text` | no |  |  |

键与约束：

- FOREIGN KEY `contact_emails_contact_id_fkey`: `contact_id` → `device.contacts` (`contact_id`)
- PRIMARY KEY `contact_emails_pkey`: `contact_email_id`

### device.contact_phones

来源：[device.contact_phones](../../../opt/hatch/skills/muse_db/references/schema.md#L1017)。可见字段 5 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `contact_phone_id` | `bigint` | no | `nextval('device.contact_phones_contact_phone_id_seq'::regclass)` | Local row identifier (primary key). |
| `contact_id` | `bigint` | no |  | FK → `device.contacts.contact_id` |
| `label` | `text` | yes |  |  |
| `phone_e164` | `text` | yes |  |  |
| `phone_raw` | `text` | no |  |  |

键与约束：

- FOREIGN KEY `contact_phones_contact_id_fkey`: `contact_id` → `device.contacts` (`contact_id`)
- PRIMARY KEY `contact_phones_pkey`: `contact_phone_id`

### device.contacts

来源：[device.contacts](../../../opt/hatch/skills/muse_db/references/schema.md#L1032)。可见字段 15 个。

阅读重点：从 `deleted_at`, `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `contact_id` | `bigint` | no | `nextval('device.contacts_contact_id_seq'::regclass)` | Local row identifier (primary key). |
| `node_id` | `text` | no |  | FK → `device.nodes.node_id` |
| `platform` | `text` | no |  |  |
| `external_contact_id` | `text` | no |  | External/provider identifier; no Muse PostgreSQL owner table. |
| `display_name` | `text` | yes |  |  |
| `given_name` | `text` | yes |  |  |
| `family_name` | `text` | yes |  |  |
| `organization` | `text` | yes |  |  |
| `job_title` | `text` | yes |  |  |
| `birthday_text` | `text` | yes |  |  |
| `note` | `text` | yes |  |  |
| `synced_at_text` | `text` | no |  |  |
| `deleted_at` | `timestamp with time zone` | yes |  |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |
| `thumbnail` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `contacts_node_id_fkey`: `node_id` → `device.nodes` (`node_id`)
- PRIMARY KEY `contacts_pkey`: `contact_id`
- UNIQUE `contacts_node_id_external_contact_id_key`: `node_id`, `external_contact_id`

### device.data_sync_state

来源：[device.data_sync_state](../../../opt/hatch/skills/muse_db/references/schema.md#L1058)。可见字段 14 个。

阅读重点：从 `next_full_sync_at`, `current_full_sync_expires_at`, `last_full_sync_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 3 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `node_id` | `text` | no |  | FK → `device.nodes.node_id` |
| `data_source` | `text` | no |  | Local row identifier (primary key). |
| `next_full_sync_at` | `timestamp with time zone` | yes |  |  |
| `current_full_sync_id` | `text` | yes |  | Soft local reference → `device.upload_sessions.upload_session_id`. |
| `current_full_sync_expires_at` | `timestamp with time zone` | yes |  |  |
| `current_full_sync_range_start` | `timestamp with time zone` | yes |  |  |
| `current_full_sync_range_end` | `timestamp with time zone` | yes |  |  |
| `changed_during_full_sync` | `boolean` | no | `false` |  |
| `last_full_sync_at` | `timestamp with time zone` | yes |  |  |
| `last_full_sync_range_start` | `timestamp with time zone` | yes |  |  |
| `last_full_sync_range_end` | `timestamp with time zone` | yes |  |  |
| `search_trigger_pending` | `boolean` | no | `false` |  |
| `current_full_sync_requester_root_session_id` | `text` | yes |  | Soft local reference → `agent.sessions.session_id`. |
| `current_full_sync_requester_presentation_locale` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `data_sync_state_node_id_fkey`: `node_id` → `device.nodes` (`node_id`)
- PRIMARY KEY `data_sync_state_pkey`: `node_id`, `data_source`

### device.media_upload_batches

来源：[device.media_upload_batches](../../../opt/hatch/skills/muse_db/references/schema.md#L1082)。可见字段 6 个。

阅读重点：从 `claimed_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `lane` | `text` | no |  | Local row identifier (primary key). |
| `batch_id` | `text` | no |  | Soft local reference → `device.media_upload_batches.batch_id`. |
| `high_water_global_seq` | `bigint` | no |  |  |
| `pending_count` | `bigint` | no |  |  |
| `oldest_received_at_unix_ms` | `bigint` | no |  |  |
| `claimed_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `media_upload_batches_pkey`: `lane`
- UNIQUE `media_upload_batches_batch_id_key`: `batch_id`

### device.media_upload_events

来源：[device.media_upload_events](../../../opt/hatch/skills/muse_db/references/schema.md#L1098)。可见字段 17 个。

阅读重点：从 `status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 3 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `media_upload_event_id` | `bigint` | no | `nextval('device.media_upload_events_media_upload_event_id_seq'::regclass)` | Local row identifier (primary key). |
| `global_seq` | `bigint` | no | `nextval('device.media_upload_events_global_seq_seq'::regclass)` |  |
| `event_id` | `text` | no |  | Device-source event identifier; no Muse PostgreSQL owner table. |
| `media_id` | `text` | no |  | Soft local reference to `media.items.media_id`. |
| `node_id` | `text` | yes |  | FK → `device.nodes.node_id` |
| `lane` | `text` | no |  |  |
| `received_at_text` | `text` | no |  |  |
| `received_at_unix_ms` | `bigint` | no |  |  |
| `received_at` | `timestamp with time zone` | no | `now()` |  |
| `status` | `text` | no |  |  |
| `processed_at_text` | `text` | yes |  |  |
| `processed_at_unix_ms` | `bigint` | yes |  |  |
| `processed_at` | `timestamp with time zone` | yes |  |  |
| `handoff_message_id` | `text` | yes |  | Soft local reference → `runtime.messages.message_id`. |
| `summary_preview` | `text` | yes |  |  |
| `failure_code` | `text` | yes |  |  |
| `failure_message` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `media_upload_events_node_id_fkey`: `node_id` → `device.nodes` (`node_id`)
- PRIMARY KEY `media_upload_events_pkey`: `media_upload_event_id`
- UNIQUE `media_upload_events_event_id_key`: `event_id`
- UNIQUE `media_upload_events_global_seq_key`: `global_seq`

### device.nodes

来源：[device.nodes](../../../opt/hatch/skills/muse_db/references/schema.md#L1127)。可见字段 31 个。

阅读重点：从 `status`, `contacts_last_sync_status`, `contacts_last_sync_error`, `health_last_sync_status`, `health_last_sync_error`, `pairing_status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `node_id` | `text` | no |  | Local row identifier (primary key). |
| `node_kind` | `text` | no |  |  |
| `display_name` | `text` | yes |  |  |
| `platform` | `text` | no | `'unknown'::text` |  |
| `enabled_permissions_json` | `text` | no | `'[]'::text` |  |
| `commands_json` | `text` | no | `'[]'::text` |  |
| `version` | `text` | yes |  |  |
| `device_family` | `text` | yes |  |  |
| `model_id` | `text` | yes |  | Model or device-provider identifier; no single Muse PostgreSQL owner table. |
| `is_wakeup_supported` | `boolean` | yes |  |  |
| `delivery_app` | `text` | yes |  |  |
| `paired_at_text` | `text` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `last_seen_at_text` | `text` | yes |  |  |
| `last_seen_at` | `timestamp with time zone` | yes |  |  |
| `status` | `text` | no | `'registered'::text` |  |
| `revoked` | `boolean` | no | `false` |  |
| `contacts_last_synced_at` | `text` | yes |  |  |
| `contacts_last_received_at` | `text` | yes |  |  |
| `contacts_last_sync_status` | `text` | no | `'never'::text` |  |
| `contacts_last_sync_error` | `text` | yes |  |  |
| `contacts_contact_count` | `bigint` | no | `0` |  |
| `health_last_received_at` | `text` | yes |  |  |
| `health_last_sync_status` | `text` | no | `'never'::text` |  |
| `health_last_sync_error` | `text` | yes |  |  |
| `data_sources_json` | `text` | no | `'{}'::text` |  |
| `invoke_protocol` | `text` | no | `'node'::text` |  |
| `pairing_status` | `text` | no | `'ok'::text` |  |
| `contacts_content_sha256` | `text` | yes |  |  |
| `metadata_json` | `text` | no | `'{}'::text` |  |
| `location_sharing_mode` | `text` | yes |  |  |

键与约束：

- PRIMARY KEY `nodes_pkey`: `node_id`

### device.upload_chunks

来源：[device.upload_chunks](../../../opt/hatch/skills/muse_db/references/schema.md#L1167)。可见字段 6 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `upload_session_id` | `text` | no |  | FK → `device.upload_sessions.upload_session_id` |
| `chunk_index` | `integer` | no |  | Local row identifier (primary key). |
| `payload_digest` | `text` | no |  |  |
| `created_at_text` | `text` | no |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `payload` | `text` | no |  |  |

键与约束：

- FOREIGN KEY `upload_chunks_upload_session_id_fkey`: `upload_session_id` → `device.upload_sessions` (`upload_session_id`)
- PRIMARY KEY `upload_chunks_pkey`: `upload_session_id`, `chunk_index`

### device.upload_sessions

来源：[device.upload_sessions](../../../opt/hatch/skills/muse_db/references/schema.md#L1183)。可见字段 14 个。

阅读重点：从 `status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `upload_session_id` | `text` | no |  | Local row identifier (primary key). |
| `node_id` | `text` | no |  | Soft local reference → `device.nodes.node_id`. |
| `route_kind` | `text` | no |  |  |
| `request_id` | `text` | yes |  | Soft local reference → `runtime.requests.request_id`. |
| `datatype` | `text` | no |  |  |
| `sync_mode` | `text` | yes |  |  |
| `chunk_count` | `integer` | no |  |  |
| `status` | `text` | no |  |  |
| `created_at_text` | `text` | no |  |  |
| `updated_at_text` | `text` | no |  |  |
| `expires_at_text` | `text` | no |  |  |
| `expires_at` | `timestamp with time zone` | no |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `response` | `text` | yes |  |  |

键与约束：

- PRIMARY KEY `upload_sessions_pkey`: `upload_session_id`

<a id="domain-feed"></a>
## feed

Feed 内容、运行、用户交互与共享分发记录；生成、收取和投递是不同阶段。

### feed.fleet_engagement_contributions

来源：[feed.fleet_engagement_contributions](../../../opt/hatch/skills/muse_db/references/schema.md#L1208)。可见字段 5 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `contribution_id` | `text` | no |  | Local row identifier (primary key). |
| `origin_id` | `text` | no |  | Fleet-learning origin identifier; its owner is outside this VM database. |
| `engagement_version` | `bigint` | no | `0` |  |
| `created_at_ms` | `bigint` | no |  |  |
| `updated_at_ms` | `bigint` | no |  |  |

键与约束：

- PRIMARY KEY `fleet_engagement_contributions_pkey`: `contribution_id`

### feed.fleet_engagement_outbox

来源：[feed.fleet_engagement_outbox](../../../opt/hatch/skills/muse_db/references/schema.md#L1222)。可见字段 11 个。

阅读重点：从 `attempt_count`, `next_attempt_at_ms` 检查状态或失败信息；字段存在不说明允许哪些状态转换。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `contribution_id` | `text` | no |  | Local row identifier (primary key). |
| `origin_id` | `text` | no |  | Fleet-learning origin identifier; its owner is outside this VM database. |
| `deleted_count` | `bigint` | no |  |  |
| `discuss_count` | `bigint` | no |  |  |
| `share_count` | `bigint` | no |  |  |
| `seed_use_count` | `bigint` | no |  |  |
| `mutation_version` | `bigint` | no |  |  |
| `attempt_count` | `integer` | no | `0` |  |
| `next_attempt_at_ms` | `bigint` | no |  |  |
| `created_at_ms` | `bigint` | no |  |  |
| `updated_at_ms` | `bigint` | no |  |  |

键与约束：

- PRIMARY KEY `fleet_engagement_outbox_pkey`: `contribution_id`

### feed.fleet_fetch_receipts

来源：[feed.fleet_fetch_receipts](../../../opt/hatch/skills/muse_db/references/schema.md#L1242)。可见字段 3 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `payload_hash` | `text` | no |  | Local row identifier (primary key). |
| `first_fetched_at_ms` | `bigint` | no |  |  |
| `origin_id` | `text` | yes |  | Fleet-learning origin identifier; its owner is outside this VM database. |

键与约束：

- PRIMARY KEY `fleet_fetch_receipts_pkey`: `payload_hash`

### feed.fleet_publish_state

来源：[feed.fleet_publish_state](../../../opt/hatch/skills/muse_db/references/schema.md#L1254)。可见字段 2 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `singleton` | `boolean` | no | `true` | Local row identifier (primary key). |
| `published_watermark_ms` | `bigint` | no |  |  |

键与约束：

- PRIMARY KEY `fleet_publish_state_pkey`: `singleton`

### feed.fleet_reaction_outbox

来源：[feed.fleet_reaction_outbox](../../../opt/hatch/skills/muse_db/references/schema.md#L1265)。可见字段 8 个。

阅读重点：从 `attempt_count`, `next_attempt_at_ms` 检查状态或失败信息；字段存在不说明允许哪些状态转换。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `unit_id` | `text` | no |  | Local row identifier (primary key). |
| `origin_id` | `text` | no |  | Fleet-learning origin identifier; its owner is outside this VM database. |
| `liked` | `boolean` | no |  |  |
| `mutation_version` | `bigint` | no |  |  |
| `attempt_count` | `integer` | no | `0` |  |
| `next_attempt_at_ms` | `bigint` | no |  |  |
| `created_at_ms` | `bigint` | no |  |  |
| `updated_at_ms` | `bigint` | no |  |  |

键与约束：

- PRIMARY KEY `fleet_reaction_outbox_pkey`: `unit_id`

### feed.interactions

来源：[feed.interactions](../../../opt/hatch/skills/muse_db/references/schema.md#L1282)。可见字段 5 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `interaction_id` | `text` | no |  | Local row identifier (primary key). |
| `unit_id` | `text` | no |  | Potential local reference; resolve by domain context in: `feed.fleet_reaction_outbox.unit_id`, `feed.promptless_unit_orders.unit_id`, `feed.units.unit_id`. |
| `kind` | `text` | no |  |  |
| `value` | `text` | yes |  |  |
| `created_at_ms` | `bigint` | no |  |  |

键与约束：

- PRIMARY KEY `interactions_pkey`: `interaction_id`

### feed.null_state_seed

来源：[feed.null_state_seed](../../../opt/hatch/skills/muse_db/references/schema.md#L1296)。可见字段 2 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `singleton` | `boolean` | no | `true` | Local row identifier (primary key). |
| `seeded_at_ms` | `bigint` | no |  |  |

键与约束：

- PRIMARY KEY `null_state_seed_pkey`: `singleton`

### feed.preferences_projection

来源：[feed.preferences_projection](../../../opt/hatch/skills/muse_db/references/schema.md#L1307)。可见字段 5 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `singleton_id` | `smallint` | no | `1` | Local row identifier (primary key). |
| `preferences_md` | `text` | no |  |  |
| `folded_through_ms` | `bigint` | no |  |  |
| `updated_by_run` | `text` | no |  |  |
| `updated_at_ms` | `bigint` | no |  |  |

键与约束：

- PRIMARY KEY `preferences_projection_pkey`: `singleton_id`

### feed.prompt_scope_verdict

来源：[feed.prompt_scope_verdict](../../../opt/hatch/skills/muse_db/references/schema.md#L1321)。可见字段 6 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `singleton` | `boolean` | no | `true` | Local row identifier (primary key). |
| `prompt_sha256` | `text` | no |  |  |
| `needs_interpretation` | `boolean` | no |  |  |
| `reason` | `text` | no |  |  |
| `classifier_version` | `integer` | no |  |  |
| `classified_at_ms` | `bigint` | no |  |  |

键与约束：

- PRIMARY KEY `prompt_scope_verdict_pkey`: `singleton`

### feed.prompt_seed

来源：[feed.prompt_seed](../../../opt/hatch/skills/muse_db/references/schema.md#L1336)。可见字段 2 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `singleton` | `boolean` | no | `true` | Local row identifier (primary key). |
| `seeded_at_ms` | `bigint` | no |  |  |

键与约束：

- PRIMARY KEY `prompt_seed_pkey`: `singleton`

### feed.promptless_unit_orders

来源：[feed.promptless_unit_orders](../../../opt/hatch/skills/muse_db/references/schema.md#L1347)。可见字段 4 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `prompt_id` | `text` | no |  | Local row identifier (primary key). |
| `unit_id` | `text` | no |  | FK → `feed.units.unit_id` |
| `local_date` | `date` | no |  |  |
| `manual_order` | `double precision` | no |  |  |

键与约束：

- FOREIGN KEY `promptless_unit_orders_unit_id_fkey`: `unit_id` → `feed.units` (`unit_id`)
- PRIMARY KEY `promptless_unit_orders_pkey`: `prompt_id`, `unit_id`

### feed.prompts

来源：[feed.prompts](../../../opt/hatch/skills/muse_db/references/schema.md#L1361)。可见字段 11 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `prompt_id` | `text` | no |  | Local row identifier (primary key). |
| `template_id` | `text` | yes |  | Legacy built-in Feed template key; the template catalog is code-owned, not a table. |
| `slot_values` | `jsonb` | no | `'{}'::jsonb` |  |
| `free_text` | `text` | no | `''::text` |  |
| `enabled` | `boolean` | no | `true` |  |
| `created_at_ms` | `bigint` | no |  |  |
| `updated_at_ms` | `bigint` | no |  |  |
| `slot_ingredients` | `jsonb` | no | `'[]'::jsonb` |  |
| `generation_queued_at_ms` | `bigint` | yes |  |  |
| `full_prompt` | `text` | yes |  |  |
| `generation_queued_requester` | `jsonb` | yes |  |  |

键与约束：

- PRIMARY KEY `prompts_pkey`: `prompt_id`

### feed.run_steps

来源：[feed.run_steps](../../../opt/hatch/skills/muse_db/references/schema.md#L1381)。可见字段 13 个。

阅读重点：从 `attempt`, `status`, `error` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `run_id` | `text` | no |  | Local row identifier (primary key). |
| `step_id` | `text` | no |  | Local row identifier (primary key). |
| `attempt` | `integer` | no | `0` | Local row identifier (primary key). |
| `input_hash` | `text` | no |  |  |
| `status` | `text` | no |  |  |
| `agent_id` | `text` | yes |  | Soft local reference → `agent.agents.agent_id`. |
| `message_id` | `text` | yes |  | Soft local reference → `runtime.messages.message_id`. |
| `output_json` | `jsonb` | no | `'{}'::jsonb` |  |
| `error` | `text` | yes |  |  |
| `started_at_ms` | `bigint` | no |  |  |
| `finished_at_ms` | `bigint` | yes |  |  |
| `updated_at_ms` | `bigint` | no |  |  |
| `submitted_at_ms` | `bigint` | yes |  |  |

键与约束：

- PRIMARY KEY `run_steps_pkey`: `run_id`, `step_id`, `attempt`

### feed.runs

来源：[feed.runs](../../../opt/hatch/skills/muse_db/references/schema.md#L1403)。可见字段 18 个。

阅读重点：从 `status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `run_id` | `text` | no |  | Local row identifier (primary key). |
| `trigger` | `text` | no |  |  |
| `edition_kind` | `text` | no |  |  |
| `local_date` | `date` | no |  |  |
| `tz` | `text` | no |  |  |
| `prompt_id` | `text` | yes |  | Potential local reference; resolve by domain context in: `feed.promptless_unit_orders.prompt_id`, `feed.prompts.prompt_id`. |
| `prompt_snapshot` | `text` | yes |  |  |
| `requester` | `jsonb` | yes |  |  |
| `slot_fulfillment` | `jsonb` | no | `'{}'::jsonb` |  |
| `interactions_watermark_ms` | `bigint` | yes |  |  |
| `status` | `text` | no | `'queued'::text` |  |
| `failure_reason` | `text` | yes |  |  |
| `started_at_ms` | `bigint` | yes |  |  |
| `finished_at_ms` | `bigint` | yes |  |  |
| `created_at_ms` | `bigint` | no |  |  |
| `updated_at_ms` | `bigint` | no |  |  |
| `hour_slot` | `smallint` | yes |  |  |
| `search_query_keys` | `text[]` | yes |  |  |

键与约束：

- PRIMARY KEY `runs_pkey`: `run_id`

### feed.surface_state

来源：[feed.surface_state](../../../opt/hatch/skills/muse_db/references/schema.md#L1430)。可见字段 2 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `singleton` | `boolean` | no | `true` | Local row identifier (primary key). |
| `first_fetched_at_ms` | `bigint` | no |  |  |

键与约束：

- PRIMARY KEY `surface_state_pkey`: `singleton`

### feed.units

来源：[feed.units](../../../opt/hatch/skills/muse_db/references/schema.md#L1441)。可见字段 49 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。 有 3 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `unit_id` | `text` | no |  | Local row identifier (primary key). |
| `run_id` | `text` | no |  | Potential local reference; resolve by domain context in: `feed.run_steps.run_id`, `feed.runs.run_id`. |
| `prompt_id` | `text` | yes |  | Potential local reference; resolve by domain context in: `feed.promptless_unit_orders.prompt_id`, `feed.prompts.prompt_id`. |
| `edition_kind` | `text` | no |  |  |
| `edition_local_date` | `date` | no |  |  |
| `edition_generated_at_ms` | `bigint` | no |  |  |
| `position` | `integer` | no |  |  |
| `kicker` | `text` | no |  |  |
| `body_md` | `text` | no |  |  |
| `attachment_kind` | `text` | no |  |  |
| `header_image_path` | `text` | yes |  |  |
| `image_urls` | `text[]` | yes |  |  |
| `widget_html` | `text` | yes |  |  |
| `social_embed_url` | `text` | yes |  |  |
| `category` | `text` | no |  |  |
| `connector_attribution` | `text` | yes |  |  |
| `stats` | `jsonb` | yes |  |  |
| `reaction` | `text` | yes |  |  |
| `reaction_updated_at_ms` | `bigint` | yes |  |  |
| `share_count` | `bigint` | no | `0` |  |
| `discuss_count` | `bigint` | no | `0` |  |
| `origin` | `text` | no |  |  |
| `share_instructions` | `jsonb` | yes |  |  |
| `share_artifact_generated_at_ms` | `bigint` | yes |  |  |
| `share_artifact_stale` | `boolean` | no | `false` |  |
| `created_at_ms` | `bigint` | no |  |  |
| `updated_at_ms` | `bigint` | no |  |  |
| `embedding` | `vector(384)` | yes |  |  |
| `manual_order` | `double precision` | yes |  |  |
| `seen_at_ms` | `bigint` | yes |  |  |
| `title` | `text` | yes |  |  |
| `search_vector` | `tsvector` | yes | `to_tsvector('simple'::regconfig, "left"(((((((COALESCE(kicker, ''::text) \ | \ |
| `last_seen_at_ms` | `bigint` | yes |  |  |
| `timespent_ms` | `bigint` | yes |  |  |
| `social_thumbnail_url` | `text` | yes |  |  |
| `social_thumbnail_aspect_ratio` | `double precision` | yes |  |  |
| `social_attribution_text` | `text` | yes |  |  |
| `social_post_username` | `text` | yes |  |  |
| `why_did_i_see_this` | `text` | yes |  |  |
| `source_post_url` | `text` | yes |  |  |
| `video_media_path` | `text` | yes |  |  |
| `carousel_clip_paths` | `text[]` | yes |  |  |
| `source_fleet_origin_id` | `text` | yes |  | Fleet-learning origin identifier; its owner is outside this VM database. |
| `fleet_reaction_version` | `bigint` | no | `0` |  |
| `emoji` | `text` | yes |  |  |
| `source_idea_id` | `text` | yes |  | Soft local reference → `ideas.ideas.idea_id`. |
| `icon_key` | `text` | yes |  |  |
| `source_url_keys` | `text[]` | yes |  |  |
| `activity_tier` | `text` | yes |  |  |

键与约束：

- PRIMARY KEY `units_pkey`: `unit_id`

<a id="domain-goals"></a>
## goals

目标、关联、行动、更新和进展；目标父子关系不应与通用 Agent 父子关系混用。

### goals.actions

来源：[goals.actions](../../../opt/hatch/skills/muse_db/references/schema.md#L1501)。可见字段 6 个。

阅读重点：从 `status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `action_id` | `bigint` | no | `nextval('goals.actions_action_id_seq'::regclass)` | Local row identifier (primary key). |
| `goal_id` | `text` | no |  | FK → `goals.goals.goal_id` |
| `status` | `text` | no |  |  |
| `created_at` | `timestamp with time zone` | no |  |  |
| `updated_at` | `timestamp with time zone` | no |  |  |
| `action_text` | `text` | no |  |  |

键与约束：

- FOREIGN KEY `actions_goal_id_fkey`: `goal_id` → `goals.goals` (`goal_id`)
- PRIMARY KEY `actions_pkey`: `action_id`

### goals.associations

来源：[goals.associations](../../../opt/hatch/skills/muse_db/references/schema.md#L1517)。可见字段 9 个。

阅读重点：从 `created_at`, `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `association_id` | `text` | no |  | Local row identifier (primary key). |
| `goal_id` | `text` | no |  | FK → `goals.goals.goal_id` |
| `association_type` | `text` | no |  |  |
| `target_id` | `text` | no |  | Polymorphic target selected by `association_type`: cron job id (`scheduler.jobs.job_id`), artifact slug (`spaces.spaces.space_slug`), or an on-disk document path. |
| `details_json` | `text` | no | `'{}'::text` |  |
| `created_at` | `text` | no |  |  |
| `updated_at` | `text` | no |  |  |
| `created_at_ts` | `timestamp with time zone` | yes |  |  |
| `updated_at_ts` | `timestamp with time zone` | yes |  |  |

键与约束：

- FOREIGN KEY `associations_goal_id_fkey`: `goal_id` → `goals.goals` (`goal_id`)
- PRIMARY KEY `associations_pkey`: `association_id`
- UNIQUE `associations_goal_id_association_type_target_id_key`: `goal_id`, `association_type`, `target_id`

### goals.briefings

来源：[goals.briefings](../../../opt/hatch/skills/muse_db/references/schema.md#L1537)。可见字段 10 个。

阅读重点：从 `created_at`, `updated_at`, `last_opened_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `briefing_id` | `text` | no |  | Local row identifier (primary key). |
| `goal_id` | `text` | no |  | FK → `goals.goals.goal_id` |
| `path` | `text` | no |  |  |
| `created_at` | `text` | no |  |  |
| `updated_at` | `text` | no |  |  |
| `last_opened_at` | `text` | yes |  |  |
| `created_at_ts` | `timestamp with time zone` | yes |  |  |
| `updated_at_ts` | `timestamp with time zone` | yes |  |  |
| `last_opened_at_ts` | `timestamp with time zone` | yes |  |  |
| `hero_image_path` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `briefings_goal_id_fkey`: `goal_id` → `goals.goals` (`goal_id`)
- PRIMARY KEY `briefings_pkey`: `briefing_id`
- UNIQUE `briefings_goal_id_path_key`: `goal_id`, `path`

### goals.engagement_events

来源：[goals.engagement_events](../../../opt/hatch/skills/muse_db/references/schema.md#L1558)。可见字段 8 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `event_id` | `text` | no |  | Local row identifier (primary key). |
| `goal_id` | `text` | no |  | FK → `goals.goals.goal_id` |
| `event_type` | `text` | no |  | Engagement/feedback event type. Canonical vocab (shared with ideas.idea_events): impression, click, engagement, feedback_up, feedback_down. |
| `surface` | `text` | yes |  |  |
| `value` | `double precision` | yes |  | Optional numeric depth for engagement rows (e.g. dwell seconds / value weight); null for impression/click/feedback rows. |
| `request_id` | `text` | no |  | Soft local reference → `runtime.requests.request_id`. |
| `metadata` | `jsonb` | no | `'{}'::jsonb` |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `engagement_events_goal_id_fkey`: `goal_id` → `goals.goals` (`goal_id`)
- PRIMARY KEY `engagement_events_pkey`: `event_id`

### goals.goals

来源：[goals.goals](../../../opt/hatch/skills/muse_db/references/schema.md#L1576)。可见字段 43 个。

阅读重点：从 `momentum_status`, `icon_generation_status`, `status`, `completed_at`, `completed_at_ts` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `goal_id` | `text` | no |  | Local row identifier (primary key). |
| `activity_key` | `text` | yes |  |  |
| `slug` | `text` | yes |  |  |
| `title` | `text` | no |  |  |
| `summary` | `text` | yes |  |  |
| `description` | `text` | yes |  |  |
| `momentum` | `text` | yes |  |  |
| `momentum_status` | `text` | yes |  |  |
| `emoji` | `text` | yes |  |  |
| `image_relpath` | `text` | yes |  |  |
| `icon_generation_status` | `text` | yes |  |  |
| `status` | `text` | no |  |  |
| `created_at` | `text` | no |  |  |
| `updated_at` | `text` | no |  |  |
| `parent_goal_id` | `text` | yes |  | FK → `goals.goals.goal_id` |
| `sort_order` | `double precision` | no | `0` |  |
| `completed_at` | `text` | yes |  |  |
| `created_at_ts` | `timestamp with time zone` | yes |  |  |
| `updated_at_ts` | `timestamp with time zone` | yes |  |  |
| `last_activity_at` | `text` | yes |  |  |
| `last_activity_at_ts` | `timestamp with time zone` | yes |  |  |
| `pushable` | `boolean` | no | `true` |  |
| `category` | `text` | yes |  |  |
| `goal_kind` | `text` | yes |  |  |
| `value_alignment` | `text` | yes |  |  |
| `user_words` | `text` | yes |  |  |
| `assistant_distillation` | `text` | yes |  |  |
| `woop` | `jsonb` | yes |  |  |
| `implementation_intentions` | `jsonb` | yes |  |  |
| `monitoring_signal` | `text` | yes |  |  |
| `review_cadence` | `text` | yes |  |  |
| `next_review_question` | `text` | yes |  |  |
| `momentum_dimensions` | `jsonb` | yes |  |  |
| `adjustment_recommendation` | `text` | yes |  |  |
| `provenance` | `jsonb` | yes |  |  |
| `completed_at_ts` | `timestamp with time zone` | yes |  |  |
| `source` | `text` | no | `'user_goal'::text` |  |
| `attention_kind` | `text` | no | `'does_not_need_attention'::text` |  |
| `attention_updated_at` | `timestamp with time zone` | no | `now()` |  |
| `next_due_at` | `timestamp with time zone` | yes |  |  |
| `escalation` | `jsonb` | yes |  |  |
| `escalation_due_at` | `timestamp with time zone` | yes |  |  |
| `fixed_position` | `bigint` | yes |  |  |

键与约束：

- FOREIGN KEY `goals_parent_goal_id_fkey`: `parent_goal_id` → `goals.goals` (`goal_id`)
- PRIMARY KEY `goals_pkey`: `goal_id`
- UNIQUE `goals_slug_key`: `slug`

### goals.learning_state

来源：[goals.learning_state](../../../opt/hatch/skills/muse_db/references/schema.md#L1630)。可见字段 13 个。

阅读重点：从 `transfer_status`, `study_status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `goal_id` | `text` | no |  | FK → `goals.goals.goal_id` |
| `target_skill` | `text` | yes |  |  |
| `prerequisites` | `jsonb` | no | `'[]'::jsonb` |  |
| `mastery_estimate` | `double precision` | yes |  |  |
| `mastery_evidence` | `jsonb` | no | `'[]'::jsonb` |  |
| `misconceptions` | `jsonb` | no | `'[]'::jsonb` |  |
| `last_retrieval_at` | `timestamp with time zone` | yes |  |  |
| `next_review_at` | `timestamp with time zone` | yes |  |  |
| `confidence` | `double precision` | yes |  |  |
| `transfer_status` | `text` | yes |  |  |
| `study_status` | `text` | no | `'queued'::text` |  |
| `last_studied_at` | `timestamp with time zone` | yes |  |  |
| `updated_at_ts` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `learning_state_goal_id_fkey`: `goal_id` → `goals.goals` (`goal_id`)
- PRIMARY KEY `learning_state_pkey`: `goal_id`

### goals.momentum_history

来源：[goals.momentum_history](../../../opt/hatch/skills/muse_db/references/schema.md#L1653)。可见字段 9 个。

阅读重点：从 `momentum_status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `history_id` | `bigint` | no | `nextval('goals.momentum_history_history_id_seq'::regclass)` | Local row identifier (primary key). |
| `goal_id` | `text` | no |  | FK → `goals.goals.goal_id` |
| `momentum_status` | `text` | yes |  |  |
| `momentum_dimensions` | `jsonb` | yes |  |  |
| `adjustment_recommendation` | `text` | yes |  |  |
| `source` | `text` | no |  |  |
| `run_id` | `text` | yes |  | Producer-run correlation identifier; no single Muse PostgreSQL owner table. |
| `observed_at` | `timestamp with time zone` | no | `now()` |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `momentum_history_goal_id_fkey`: `goal_id` → `goals.goals` (`goal_id`)
- PRIMARY KEY `momentum_history_pkey`: `history_id`

### goals.sessions

来源：[goals.sessions](../../../opt/hatch/skills/muse_db/references/schema.md#L1672)。可见字段 3 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。 有 3 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `root_goal_id` | `text` | no |  | FK → `goals.goals.goal_id` |
| `root_agent_id` | `text` | no |  | Soft local reference → `agent.agents.agent_id`. |
| `session_id` | `text` | no |  | Soft local reference → `agent.sessions.session_id`. |

键与约束：

- FOREIGN KEY `sessions_root_goal_id_fkey`: `root_goal_id` → `goals.goals` (`goal_id`)
- PRIMARY KEY `sessions_pkey`: `root_goal_id`

### goals.suggestions

来源：[goals.suggestions](../../../opt/hatch/skills/muse_db/references/schema.md#L1685)。可见字段 8 个。

阅读重点：从 `status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `suggestion_id` | `text` | no |  | Local row identifier (primary key). |
| `goal_id` | `text` | no |  | FK → `goals.goals.goal_id` |
| `idea_id` | `text` | no |  | Soft local reference → `ideas.ideas.idea_id`. |
| `status` | `text` | no |  |  |
| `created_at` | `text` | no |  |  |
| `updated_at` | `text` | no |  |  |
| `created_at_ts` | `timestamp with time zone` | yes |  |  |
| `updated_at_ts` | `timestamp with time zone` | yes |  |  |

键与约束：

- FOREIGN KEY `suggestions_goal_id_fkey`: `goal_id` → `goals.goals` (`goal_id`)
- PRIMARY KEY `suggestions_pkey`: `suggestion_id`
- UNIQUE `suggestions_goal_id_idea_id_key`: `goal_id`, `idea_id`

### goals.thread_actions

来源：[goals.thread_actions](../../../opt/hatch/skills/muse_db/references/schema.md#L1704)。可见字段 4 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `thread_action_id` | `bigint` | no | `nextval('goals.thread_actions_thread_action_id_seq'::regclass)` | Local row identifier (primary key). |
| `thread_id` | `bigint` | no |  | FK → `goals.threads.thread_id` |
| `action_id` | `bigint` | yes |  | FK → `goals.actions.action_id` |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `thread_actions_action_id_fkey`: `action_id` → `goals.actions` (`action_id`)
- FOREIGN KEY `thread_actions_thread_id_fkey`: `thread_id` → `goals.threads` (`thread_id`)
- PRIMARY KEY `thread_actions_pkey`: `thread_action_id`

### goals.threads

来源：[goals.threads](../../../opt/hatch/skills/muse_db/references/schema.md#L1719)。可见字段 4 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `thread_id` | `bigint` | no | `nextval('goals.threads_thread_id_seq'::regclass)` | Local row identifier (primary key). |
| `goal_id` | `text` | no |  | FK → `goals.goals.goal_id` |
| `request_id` | `text` | yes |  | FK → `runtime.requests.request_id` |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `threads_goal_id_fkey`: `goal_id` → `goals.goals` (`goal_id`)
- FOREIGN KEY `threads_request_id_fkey`: `request_id` → `runtime.requests` (`request_id`)
- PRIMARY KEY `threads_pkey`: `thread_id`

### goals.updates

来源：[goals.updates](../../../opt/hatch/skills/muse_db/references/schema.md#L1734)。可见字段 11 个。

阅读重点：从 `effective_at`, `created_at`, `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `update_id` | `text` | no |  | Local row identifier (primary key). |
| `goal_id` | `text` | no |  | FK → `goals.goals.goal_id` |
| `title` | `text` | yes |  |  |
| `summary` | `text` | yes |  |  |
| `description` | `text` | yes |  |  |
| `effective_at` | `text` | yes |  |  |
| `created_at` | `text` | no |  |  |
| `updated_at` | `text` | no |  |  |
| `effective_at_ts` | `timestamp with time zone` | yes |  |  |
| `updated_at_ts` | `timestamp with time zone` | yes |  |  |
| `author_source` | `text` | no | `'user'::text` |  |

键与约束：

- FOREIGN KEY `updates_goal_id_fkey`: `goal_id` → `goals.goals` (`goal_id`)
- PRIMARY KEY `updates_pkey`: `update_id`

<a id="domain-health"></a>
## health

摄取后的健康记录、数值、聚合、睡眠和训练；单位、时间和来源决定可比较性，表存在不保证完整样本。

### health.aggregates

来源：[health.aggregates](../../../opt/hatch/skills/muse_db/references/schema.md#L1757)。可见字段 9 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `aggregate_id` | `bigint` | no | `nextval('health.aggregates_aggregate_id_seq'::regclass)` | Local row identifier (primary key). |
| `provider` | `text` | no |  |  |
| `node_id` | `text` | yes |  | Soft local reference → `device.nodes.node_id`. |
| `timezone` | `text` | yes |  |  |
| `aggregate_type` | `text` | no |  |  |
| `period_start` | `timestamp with time zone` | no |  |  |
| `period_end` | `timestamp with time zone` | no |  |  |
| `numeric_value` | `double precision` | yes |  |  |
| `unit` | `text` | yes |  |  |

键与约束：

- PRIMARY KEY `aggregates_pkey`: `aggregate_id`
- UNIQUE `aggregates_provider_node_id_aggregate_type_period_start_per_key`: `provider`, `node_id`, `aggregate_type`, `period_start`, `period_end`

### health.events

来源：[health.events](../../../opt/hatch/skills/muse_db/references/schema.md#L1776)。可见字段 10 个。

阅读重点：从 `event_at`, `event_end_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `health_event_id` | `bigint` | no | `nextval('health.events_health_event_id_seq'::regclass)` | Local row identifier (primary key). |
| `provider` | `text` | no |  |  |
| `node_id` | `text` | yes |  | Soft local reference → `device.nodes.node_id`. |
| `external_event_id` | `text` | yes |  | External/provider identifier; no Muse PostgreSQL owner table. |
| `bundle_id` | `text` | yes |  | Source application bundle identifier. |
| `timezone` | `text` | yes |  |  |
| `event_type` | `text` | no |  |  |
| `event_at` | `timestamp with time zone` | no |  |  |
| `event_end_at` | `timestamp with time zone` | yes |  |  |
| `event_text` | `text` | yes |  |  |

键与约束：

- PRIMARY KEY `events_pkey`: `health_event_id`

### health.record_values

来源：[health.record_values](../../../opt/hatch/skills/muse_db/references/schema.md#L1795)。可见字段 7 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `record_value_id` | `bigint` | no | `nextval('health.record_values_record_value_id_seq'::regclass)` | Local row identifier (primary key). |
| `record_table` | `text` | no |  |  |
| `record_id` | `bigint` | no |  | Polymorphic local reference selected by `record_table`: `health.aggregates.aggregate_id`, `health.events.health_event_id`, `health.sleep_sessions.sleep_session_id`, or `health.workouts.workout_id`. |
| `value_name` | `text` | no |  |  |
| `unit` | `text` | yes |  |  |
| `numeric_value` | `double precision` | yes |  |  |
| `text_value` | `text` | yes |  |  |

键与约束：

- PRIMARY KEY `record_values_pkey`: `record_value_id`
- UNIQUE `record_values_record_table_record_id_value_name_key`: `record_table`, `record_id`, `value_name`

### health.sample_values

来源：[health.sample_values](../../../opt/hatch/skills/muse_db/references/schema.md#L1812)。可见字段 6 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `sample_value_id` | `bigint` | no | `nextval('health.sample_values_sample_value_id_seq'::regclass)` | Local row identifier (primary key). |
| `sample_id` | `bigint` | no |  | FK → `health.samples.sample_id` |
| `value_name` | `text` | no |  |  |
| `unit` | `text` | yes |  |  |
| `numeric_value` | `double precision` | yes |  |  |
| `text_value` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `sample_values_sample_id_fkey`: `sample_id` → `health.samples` (`sample_id`)
- PRIMARY KEY `sample_values_pkey`: `sample_value_id`
- UNIQUE `sample_values_sample_id_value_name_key`: `sample_id`, `value_name`

### health.samples

来源：[health.samples](../../../opt/hatch/skills/muse_db/references/schema.md#L1829)。可见字段 14 个。

阅读重点：从 `start_at`, `end_at`, `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `sample_id` | `bigint` | no | `nextval('health.samples_sample_id_seq'::regclass)` | Local row identifier (primary key). |
| `provider` | `text` | no |  |  |
| `node_id` | `text` | yes |  | Soft local reference → `device.nodes.node_id`. |
| `external_sample_id` | `text` | no |  | External/provider identifier; no Muse PostgreSQL owner table. |
| `bundle_id` | `text` | yes |  | Source application bundle identifier. |
| `sample_type` | `text` | no |  |  |
| `start_at` | `timestamp with time zone` | no |  |  |
| `end_at` | `timestamp with time zone` | yes |  |  |
| `unit` | `text` | yes |  |  |
| `numeric_value` | `double precision` | yes |  |  |
| `text_value` | `text` | yes |  |  |
| `source_name` | `text` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `timezone` | `text` | yes |  |  |

键与约束：

- PRIMARY KEY `samples_pkey`: `sample_id`

### health.sleep_sessions

来源：[health.sleep_sessions](../../../opt/hatch/skills/muse_db/references/schema.md#L1852)。可见字段 17 个。

阅读重点：从 `start_at`, `end_at`, `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `sleep_session_id` | `bigint` | no | `nextval('health.sleep_sessions_sleep_session_id_seq'::regclass)` | Local row identifier (primary key). |
| `provider` | `text` | no |  |  |
| `node_id` | `text` | yes |  | Soft local reference → `device.nodes.node_id`. |
| `external_sleep_id` | `text` | no |  | External/provider identifier; no Muse PostgreSQL owner table. |
| `bundle_id` | `text` | yes |  | Source application bundle identifier. |
| `timezone` | `text` | yes |  |  |
| `start_at` | `timestamp with time zone` | no |  |  |
| `end_at` | `timestamp with time zone` | no |  |  |
| `quality_score` | `double precision` | yes |  |  |
| `awake_seconds` | `double precision` | yes |  |  |
| `core_seconds` | `double precision` | yes |  |  |
| `deep_seconds` | `double precision` | yes |  |  |
| `rem_seconds` | `double precision` | yes |  |  |
| `asleep_unspecified_seconds` | `double precision` | yes |  |  |
| `asleep_seconds` | `integer` | yes |  |  |
| `in_bed_seconds` | `integer` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `sleep_sessions_pkey`: `sleep_session_id`

### health.synced_ranges

来源：[health.synced_ranges](../../../opt/hatch/skills/muse_db/references/schema.md#L1878)。可见字段 6 个。

阅读重点：从 `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `synced_range_id` | `bigint` | no | `nextval('health.synced_ranges_synced_range_id_seq'::regclass)` | Local row identifier (primary key). |
| `provider` | `text` | no |  |  |
| `node_id` | `text` | yes |  | Soft local reference → `device.nodes.node_id`. |
| `category` | `text` | no |  |  |
| `span` | `tstzrange` | no |  |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `synced_ranges_pkey`: `synced_range_id`

### health.workouts

来源：[health.workouts](../../../opt/hatch/skills/muse_db/references/schema.md#L1893)。可见字段 15 个。

阅读重点：从 `start_at`, `end_at`, `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `workout_id` | `bigint` | no | `nextval('health.workouts_workout_id_seq'::regclass)` | Local row identifier (primary key). |
| `provider` | `text` | no |  |  |
| `node_id` | `text` | yes |  | Soft local reference → `device.nodes.node_id`. |
| `external_workout_id` | `text` | no |  | External/provider identifier; no Muse PostgreSQL owner table. |
| `bundle_id` | `text` | yes |  | Source application bundle identifier. |
| `timezone` | `text` | yes |  |  |
| `workout_type` | `text` | no |  |  |
| `start_at` | `timestamp with time zone` | no |  |  |
| `end_at` | `timestamp with time zone` | yes |  |  |
| `active_seconds` | `double precision` | yes |  |  |
| `energy_kcal` | `double precision` | yes |  |  |
| `distance_meters` | `double precision` | yes |  |  |
| `hr_max_bpm` | `double precision` | yes |  |  |
| `hr_average_bpm` | `double precision` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `workouts_pkey`: `workout_id`

<a id="domain-ideas"></a>
## ideas

建议、卡片、来源、排序状态和反馈；可观察排序相关状态，无法由表恢复模型和学习公式。

### ideas.bandit_arm_state

来源：[ideas.bandit_arm_state](../../../opt/hatch/skills/muse_db/references/schema.md#L1919)。可见字段 9 个。

阅读重点：从 `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `policy_id` | `text` | no |  | FK → `ideas.explore_policy.policy_id` |
| `domain` | `text` | no |  | Local row identifier (primary key). |
| `lane` | `text` | no |  | Local row identifier (primary key). |
| `decision_points` | `bigint` | no | `0` |  |
| `terminal_rewards` | `bigint` | no | `0` |  |
| `terminal_observations` | `bigint` | no | `0` |  |
| `fast_reward_sum` | `double precision` | no | `0` |  |
| `fast_observations` | `bigint` | no | `0` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `bandit_arm_state_policy_id_fkey`: `policy_id` → `ideas.explore_policy` (`policy_id`)
- PRIMARY KEY `bandit_arm_state_pkey`: `policy_id`, `domain`, `lane`

### ideas.bandit_fold_state

来源：[ideas.bandit_fold_state](../../../opt/hatch/skills/muse_db/references/schema.md#L1938)。可见字段 4 个。

阅读重点：从 `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `policy_id` | `text` | no |  | FK → `ideas.explore_policy.policy_id` |
| `folded_until` | `timestamp with time zone` | yes |  |  |
| `folded_event_id` | `text` | yes |  | Soft local reference → `ideas.bandit_folded_events.event_id`. |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `bandit_fold_state_policy_id_fkey`: `policy_id` → `ideas.explore_policy` (`policy_id`)
- PRIMARY KEY `bandit_fold_state_pkey`: `policy_id`

### ideas.bandit_folded_events

来源：[ideas.bandit_folded_events](../../../opt/hatch/skills/muse_db/references/schema.md#L1952)。可见字段 3 个。

阅读重点：从 `folded_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `policy_id` | `text` | no |  | FK → `ideas.explore_policy.policy_id` |
| `event_id` | `text` | no |  | FK → `ideas.idea_events.event_id` |
| `folded_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `bandit_folded_events_event_id_fkey`: `event_id` → `ideas.idea_events` (`event_id`)
- FOREIGN KEY `bandit_folded_events_policy_id_fkey`: `policy_id` → `ideas.explore_policy` (`policy_id`)
- PRIMARY KEY `bandit_folded_events_pkey`: `policy_id`, `event_id`

### ideas.discovery_pool_history

来源：[ideas.discovery_pool_history](../../../opt/hatch/skills/muse_db/references/schema.md#L1966)。可见字段 4 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `snapshot_id` | `text` | no |  | Local row identifier (primary key). |
| `source` | `text` | no |  |  |
| `payload_json` | `jsonb` | no |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `flock_explore_history_pkey`: `snapshot_id`

### ideas.discovery_pool_meta

来源：[ideas.discovery_pool_meta](../../../opt/hatch/skills/muse_db/references/schema.md#L1979)。可见字段 4 个。

阅读重点：从 `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `key` | `text` | no |  | Local row identifier (primary key). |
| `source` | `text` | no |  |  |
| `payload_json` | `jsonb` | no |  |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `flock_explore_meta_pkey`: `key`

### ideas.explore_policy

来源：[ideas.explore_policy](../../../opt/hatch/skills/muse_db/references/schema.md#L1992)。可见字段 5 个。

阅读重点：从 `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `policy_id` | `text` | no |  | Local row identifier (primary key). |
| `explore_floor` | `integer` | no |  |  |
| `per_domain_min` | `integer` | no |  |  |
| `version` | `text` | no |  |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `explore_policy_pkey`: `policy_id`

### ideas.feed_snapshot_cards

来源：[ideas.feed_snapshot_cards](../../../opt/hatch/skills/muse_db/references/schema.md#L2006)。可见字段 12 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `snapshot_id` | `text` | no |  | FK → `ideas.feed_snapshot_sections.snapshot_id` |
| `section_id` | `text` | no |  | FK → `ideas.feed_snapshot_sections.section_id` |
| `position` | `integer` | no |  | Local row identifier (primary key). |
| `source_key` | `text` | no |  |  |
| `origin` | `text` | no |  |  |
| `display_title` | `text` | yes |  |  |
| `display_summary` | `text` | yes |  |  |
| `context_label` | `text` | yes |  |  |
| `detail_description` | `text` | yes |  |  |
| `build_summary` | `text` | yes |  |  |
| `type_label` | `text` | yes |  |  |
| `prerequisite_notes` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `feed_snapshot_cards_snapshot_id_section_id_fkey`: `snapshot_id`, `section_id` → `ideas.feed_snapshot_sections` (`snapshot_id`, `section_id`)
- PRIMARY KEY `feed_snapshot_cards_pkey`: `snapshot_id`, `section_id`, `position`

### ideas.feed_snapshot_sections

来源：[ideas.feed_snapshot_sections](../../../opt/hatch/skills/muse_db/references/schema.md#L2028)。可见字段 6 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `snapshot_id` | `text` | no |  | FK → `ideas.feed_snapshots.snapshot_id` |
| `section_id` | `text` | no |  | Local row identifier (primary key). |
| `position` | `integer` | no |  |  |
| `role` | `text` | no |  |  |
| `title` | `text` | no |  |  |
| `subtitle` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `feed_snapshot_sections_snapshot_id_fkey`: `snapshot_id` → `ideas.feed_snapshots` (`snapshot_id`)
- PRIMARY KEY `feed_snapshot_sections_pkey`: `snapshot_id`, `section_id`
- UNIQUE `feed_snapshot_sections_snapshot_id_position_key`: `snapshot_id`, `position`

### ideas.feed_snapshots

来源：[ideas.feed_snapshots](../../../opt/hatch/skills/muse_db/references/schema.md#L2045)。可见字段 3 个。

阅读重点：从 `generated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `snapshot_id` | `text` | no |  | Local row identifier (primary key). |
| `generated_at` | `timestamp with time zone` | no | `now()` |  |
| `is_active` | `boolean` | no | `false` |  |

键与约束：

- PRIMARY KEY `feed_snapshots_pkey`: `snapshot_id`

### ideas.icon_embeddings

来源：[ideas.icon_embeddings](../../../opt/hatch/skills/muse_db/references/schema.md#L2057)。可见字段 5 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `icon_key` | `text` | no |  | Local row identifier (primary key). |
| `model_name` | `text` | no |  | Local row identifier (primary key). |
| `descriptions_digest` | `text` | no |  | Local row identifier (primary key). |
| `embedding` | `vector(384)` | no |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `icon_embeddings_pkey`: `icon_key`, `model_name`, `descriptions_digest`

### ideas.idea_anchors

来源：[ideas.idea_anchors](../../../opt/hatch/skills/muse_db/references/schema.md#L2071)。可见字段 11 个。

阅读重点：从 `lifecycle_status`, `build_status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `idea_id` | `text` | no |  | FK → `ideas.ideas.idea_id` |
| `anchor_kind` | `text` | no |  | Local row identifier (primary key). |
| `anchor_id` | `text` | no |  | Local row identifier (primary key). |
| `lifecycle_status` | `text` | no | `'candidate'::text` |  |
| `build_status` | `text` | yes |  |  |
| `surfaced_at` | `timestamp with time zone` | yes |  |  |
| `impression_count` | `integer` | no | `0` |  |
| `decided_at` | `timestamp with time zone` | yes |  |  |
| `dismiss_reason` | `text` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `idea_anchors_idea_id_fkey`: `idea_id` → `ideas.ideas` (`idea_id`)
- PRIMARY KEY `idea_anchors_pkey`: `idea_id`, `anchor_kind`, `anchor_id`

### ideas.idea_build_status

来源：[ideas.idea_build_status](../../../opt/hatch/skills/muse_db/references/schema.md#L2092)。可见字段 6 个。

阅读重点：从 `status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `source_namespace` | `text` | no |  | Local row identifier (primary key). |
| `source_kind` | `text` | no |  | Local row identifier (primary key). |
| `source_id` | `text` | no |  | Local row identifier (primary key). |
| `status` | `text` | no |  |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |
| `selected_item_ids` | `text[]` | yes |  | Soft local reference → `ideas.idea_items.idea_item_id`. Accepted idea item ids for the build; NULL means no selection provenance, empty array means full-card acceptance. |

键与约束：

- PRIMARY KEY `idea_build_status_pkey`: `source_namespace`, `source_kind`, `source_id`

### ideas.idea_card_feeds

来源：[ideas.idea_card_feeds](../../../opt/hatch/skills/muse_db/references/schema.md#L2107)。可见字段 5 个。

阅读重点：从 `generated_at`, `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `feed_id` | `text` | no |  | Local row identifier (primary key). |
| `source` | `text` | no |  |  |
| `payload_json` | `jsonb` | no |  |  |
| `generated_at` | `timestamp with time zone` | no | `now()` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `idea_card_feeds_pkey`: `feed_id`

### ideas.idea_dedup

来源：[ideas.idea_dedup](../../../opt/hatch/skills/muse_db/references/schema.md#L2121)。可见字段 7 个。

阅读重点：从 `merged_at`, `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `idea_id` | `text` | no |  | FK → `ideas.ideas.idea_id` |
| `content_fingerprint` | `text` | no |  |  |
| `embedding_ref` | `text` | yes |  |  |
| `canonical_idea_id` | `text` | yes |  | FK → `ideas.ideas.idea_id` |
| `merged_at` | `timestamp with time zone` | yes |  |  |
| `merge_reason` | `text` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `idea_dedup_canonical_idea_id_fkey`: `canonical_idea_id` → `ideas.ideas` (`idea_id`)
- FOREIGN KEY `idea_dedup_idea_id_fkey`: `idea_id` → `ideas.ideas` (`idea_id`)
- PRIMARY KEY `idea_dedup_pkey`: `idea_id`

### ideas.idea_events

来源：[ideas.idea_events](../../../opt/hatch/skills/muse_db/references/schema.md#L2139)。可见字段 10 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 3 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `event_id` | `text` | no |  | Local row identifier (primary key). |
| `idea_id` | `text` | no |  | FK → `ideas.ideas.idea_id` |
| `event_type` | `text` | no |  | Engagement/lifecycle event type. Canonical engagement vocab (shared with goals.engagement_events): impression, click, engagement, feedback_up, feedback_down. Lifecycle/decision types (surfaced, accepted, dismissed, built, ...) also flow through this ledger. |
| `dismissal_reason` | `text` | yes |  |  |
| `anchor_kind` | `text` | yes |  |  |
| `anchor_id` | `text` | yes |  | Potential local reference; resolve by domain context in: `ideas.idea_anchors.anchor_id`. |
| `lane` | `text` | yes |  |  |
| `request_id` | `text` | no |  | Soft local reference → `runtime.requests.request_id`. |
| `metadata` | `jsonb` | no | `'{}'::jsonb` |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `idea_events_idea_id_fkey`: `idea_id` → `ideas.ideas` (`idea_id`)
- PRIMARY KEY `idea_events_pkey`: `event_id`

### ideas.idea_feedback_state

来源：[ideas.idea_feedback_state](../../../opt/hatch/skills/muse_db/references/schema.md#L2159)。可见字段 7 个。

阅读重点：从 `created_at`, `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `idea_id` | `text` | no |  | FK → `ideas.ideas.idea_id` |
| `feedback` | `text` | no |  |  |
| `reason` | `text` | yes |  |  |
| `event_id` | `text` | no |  | Potential local reference; resolve by domain context in: `ideas.bandit_folded_events.event_id`, `ideas.idea_events.event_id`. |
| `surface` | `text` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `idea_feedback_state_idea_id_fkey`: `idea_id` → `ideas.ideas` (`idea_id`)
- PRIMARY KEY `idea_feedback_state_pkey`: `idea_id`

### ideas.idea_install_assets

来源：[ideas.idea_install_assets](../../../opt/hatch/skills/muse_db/references/schema.md#L2176)。可见字段 6 个。

阅读重点：从 `created_at`, `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `asset_id` | `text` | no |  | Local row identifier (primary key). |
| `idea_id` | `text` | no |  | FK → `ideas.ideas.idea_id` |
| `asset_type` | `text` | no |  |  |
| `asset_json` | `jsonb` | no |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `idea_install_assets_idea_id_fkey`: `idea_id` → `ideas.ideas` (`idea_id`)
- PRIMARY KEY `idea_install_assets_pkey`: `asset_id`

### ideas.idea_items

来源：[ideas.idea_items](../../../opt/hatch/skills/muse_db/references/schema.md#L2192)。可见字段 12 个。

阅读重点：从 `status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `idea_item_id` | `text` | no |  | Local row identifier (primary key). |
| `idea_id` | `text` | no |  | FK → `ideas.ideas.idea_id` |
| `position` | `integer` | no |  |  |
| `kind` | `text` | no |  |  |
| `title` | `text` | no |  |  |
| `summary` | `text` | no |  |  |
| `detail_description` | `text` | yes |  |  |
| `instructions` | `text` | yes |  |  |
| `build_plan_markdown` | `text` | yes |  |  |
| `status` | `text` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `idea_items_idea_id_fkey`: `idea_id` → `ideas.ideas` (`idea_id`)
- PRIMARY KEY `idea_items_pkey`: `idea_item_id`
- UNIQUE `idea_items_idea_id_position_key`: `idea_id`, `position`

### ideas.idea_quality

来源：[ideas.idea_quality](../../../opt/hatch/skills/muse_db/references/schema.md#L2215)。可见字段 11 个。

阅读重点：从 `scored_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `idea_id` | `text` | no |  | FK → `ideas.ideas.idea_id` |
| `relevance_score` | `double precision` | no |  |  |
| `novelty_score` | `double precision` | no |  |  |
| `feasibility_score` | `double precision` | no |  |  |
| `composite_score` | `double precision` | no |  |  |
| `composite_version` | `text` | no |  |  |
| `scorer` | `text` | no |  |  |
| `decision_outcome` | `text` | no |  |  |
| `decision_reasons` | `jsonb` | no | `'[]'::jsonb` |  |
| `scored_at` | `timestamp with time zone` | no | `now()` |  |
| `value_score` | `double precision` | no | `0` |  |

键与约束：

- FOREIGN KEY `idea_quality_idea_id_fkey`: `idea_id` → `ideas.ideas` (`idea_id`)
- PRIMARY KEY `idea_quality_pkey`: `idea_id`

### ideas.idea_sources

来源：[ideas.idea_sources](../../../opt/hatch/skills/muse_db/references/schema.md#L2236)。可见字段 6 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `source_namespace` | `text` | no |  | Local row identifier (primary key). |
| `source_kind` | `text` | no |  | Local row identifier (primary key). |
| `source_id` | `text` | no |  | Local row identifier (primary key). |
| `idea_id` | `text` | no |  | FK → `ideas.ideas.idea_id` |
| `position` | `integer` | yes |  |  |
| `metadata_json` | `jsonb` | no | `'{}'::jsonb` |  |

键与约束：

- FOREIGN KEY `idea_sources_idea_id_fkey`: `idea_id` → `ideas.ideas` (`idea_id`)
- PRIMARY KEY `idea_sources_pkey`: `source_namespace`, `source_kind`, `source_id`

### ideas.idea_tags

来源：[ideas.idea_tags](../../../opt/hatch/skills/muse_db/references/schema.md#L2252)。可见字段 3 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `idea_id` | `text` | no |  | FK → `ideas.ideas.idea_id` |
| `position` | `integer` | no |  | Local row identifier (primary key). |
| `tag` | `text` | no |  |  |

键与约束：

- FOREIGN KEY `idea_tags_idea_id_fkey`: `idea_id` → `ideas.ideas` (`idea_id`)
- PRIMARY KEY `idea_tags_pkey`: `idea_id`, `position`

### ideas.ideas

来源：[ideas.ideas](../../../opt/hatch/skills/muse_db/references/schema.md#L2265)。可见字段 21 个。

阅读重点：从 `created_at`, `updated_at`, `expires_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `idea_id` | `text` | no |  | Local row identifier (primary key). |
| `kind` | `text` | no |  |  |
| `title` | `text` | no |  |  |
| `summary` | `text` | no |  |  |
| `rationale` | `text` | yes |  |  |
| `category_label` | `text` | yes |  |  |
| `date_label` | `text` | yes |  |  |
| `audience` | `text` | yes |  |  |
| `lane` | `text` | yes |  |  |
| `install_markdown` | `text` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |
| `domain` | `text` | no |  |  |
| `dedup_key` | `text` | yes |  |  |
| `expires_at` | `timestamp with time zone` | yes |  |  |
| `generator` | `text` | yes |  |  |
| `search_vector` | `tsvector` | yes | `to_tsvector('simple'::regconfig, "left"(((((((COALESCE(title, ''::text) \ | \ |
| `prerequisite_notes` | `text` | yes |  |  |
| `build_summary` | `text` | yes |  |  |
| `category_index` | `bigint` | yes |  |  |
| `embedding` | `vector(384)` | yes |  |  |

键与约束：

- PRIMARY KEY `ideas_pkey`: `idea_id`

<a id="domain-ingest"></a>
## ingest

源数据事件摄取与归属；摄取存在不证明所有下游投影更新成功。

### ingest.data_source_events

来源：[ingest.data_source_events](../../../opt/hatch/skills/muse_db/references/schema.md#L2297)。可见字段 22 个。

阅读重点：从 `status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `event_id` | `bigint` | no | `nextval('ingest.data_source_events_event_id_seq'::regclass)` | Local row identifier (primary key). |
| `global_seq` | `bigint` | no | `nextval('ingest.data_source_events_global_seq_seq'::regclass)` |  |
| `ingest_id` | `text` | no |  | Soft local reference → `ingest.data_source_events.ingest_id`. |
| `producer_id` | `text` | no |  | Data-source producer identifier; no standalone owner table. |
| `source` | `text` | no |  |  |
| `origin` | `text` | no |  |  |
| `processing_lane` | `text` | no |  |  |
| `received_at_text` | `text` | no |  |  |
| `received_at_unix_ms` | `bigint` | no |  |  |
| `payload_representation` | `text` | no |  |  |
| `payload_sha256` | `text` | yes |  |  |
| `status` | `text` | no |  |  |
| `received_at` | `timestamp with time zone` | no | `now()` |  |
| `processed_at_text` | `text` | yes |  |  |
| `processed_at_unix_ms` | `bigint` | yes |  |  |
| `processed_at` | `timestamp with time zone` | yes |  |  |
| `handoff_message_id` | `text` | yes |  | Soft local reference → `runtime.messages.message_id`. |
| `summary_preview` | `text` | yes |  |  |
| `failure_code` | `text` | yes |  |  |
| `failure_message` | `text` | yes |  |  |
| `payload` | `text` | no |  |  |
| `presentation_locale` | `text` | yes |  |  |

键与约束：

- PRIMARY KEY `data_source_events_pkey`: `event_id`
- UNIQUE `data_source_events_global_seq_key`: `global_seq`
- UNIQUE `data_source_events_ingest_id_key`: `ingest_id`

<a id="domain-media"></a>
## media

媒体实体、描述、位置和 EXIF；元数据、媒体字节和分享范围需要分别确认。

### media.descriptions

来源：[media.descriptions](../../../opt/hatch/skills/muse_db/references/schema.md#L2332)。可见字段 12 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `media_id` | `text` | no |  | Local row identifier (primary key). |
| `model` | `text` | yes |  |  |
| `version` | `bigint` | no | `1` |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `description_text` | `text` | no |  |  |
| `summary_short_text` | `text` | no |  |  |
| `summary_full_text` | `text` | yes |  |  |
| `people_text` | `text` | yes |  |  |
| `activity_text` | `text` | yes |  |  |
| `objects_text` | `text` | yes |  |  |
| `ocr_text` | `text` | yes |  |  |
| `location_hint_text` | `text` | yes |  |  |

键与约束：

- PRIMARY KEY `descriptions_pkey`: `media_id`

### media.exif_values

来源：[media.exif_values](../../../opt/hatch/skills/muse_db/references/schema.md#L2353)。可见字段 5 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `exif_value_id` | `bigint` | no | `nextval('media.exif_values_exif_value_id_seq'::regclass)` | Local row identifier (primary key). |
| `media_id` | `text` | no |  | Potential local reference; resolve by domain context in: `media.descriptions.media_id`, `media.items.media_id`, `media.locations.media_id`. |
| `tag_name` | `text` | no |  |  |
| `scalar_type` | `text` | no |  |  |
| `scalar_value` | `text` | no |  |  |

键与约束：

- PRIMARY KEY `exif_values_pkey`: `exif_value_id`
- UNIQUE `exif_values_media_id_tag_name_key`: `media_id`, `tag_name`

### media.items

来源：[media.items](../../../opt/hatch/skills/muse_db/references/schema.md#L2368)。可见字段 17 个。

阅读重点：从 `description_status`, `description_attempt_count` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `media_id` | `text` | no |  | Local row identifier (primary key). |
| `source` | `text` | no |  |  |
| `source_media_id` | `text` | no |  | Soft local reference → `media.items.media_id`. |
| `node_id` | `text` | yes |  | Soft local reference → `device.nodes.node_id`. |
| `file_uri` | `text` | no |  |  |
| `media_type` | `text` | no |  |  |
| `sha256` | `bytea` | yes |  |  |
| `byte_len` | `bigint` | yes |  |  |
| `taken_at` | `timestamp with time zone` | yes |  |  |
| `taken_at_local` | `text` | yes |  |  |
| `taken_at_local_date` | `date` | yes |  |  |
| `uploaded_at` | `timestamp with time zone` | no | `now()` |  |
| `uploaded_at_unix` | `bigint` | no | `0` |  |
| `local_identifier` | `text` | yes |  |  |
| `description_status` | `text` | no | `'pending'::text` |  |
| `description_attempt_count` | `integer` | no | `0` |  |
| `description_next_retry_at_unix` | `bigint` | yes |  |  |

键与约束：

- PRIMARY KEY `items_pkey`: `media_id`

### media.locations

来源：[media.locations](../../../opt/hatch/skills/muse_db/references/schema.md#L2394)。可见字段 8 个。

阅读重点：从 `geocode_attempt_count` 检查状态或失败信息；字段存在不说明允许哪些状态转换。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `media_id` | `text` | no |  | Local row identifier (primary key). |
| `latitude` | `double precision` | yes |  |  |
| `longitude` | `double precision` | yes |  |  |
| `altitude_meters` | `double precision` | yes |  |  |
| `location_source` | `text` | yes |  |  |
| `geocode_attempt_count` | `integer` | no | `0` |  |
| `geocode_next_retry_at_unix` | `bigint` | yes |  |  |
| `location_text` | `text` | yes |  |  |

键与约束：

- PRIMARY KEY `locations_pkey`: `media_id`

<a id="domain-memory"></a>
## memory

记忆 claims、entries、索引与模型元数据；删除主项后还要考虑派生索引和重新生产。

### memory.claims

来源：[memory.claims](../../../opt/hatch/skills/muse_db/references/schema.md#L2413)。可见字段 18 个。

阅读重点：从 `status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `claim_id` | `text` | no |  | Local row identifier (primary key). |
| `run_id` | `text` | no |  | Opaque correlation identifier; no declared local table relationship. |
| `kind` | `text` | no |  |  |
| `salience` | `text` | no |  |  |
| `claim_text` | `text` | no |  |  |
| `quote` | `text` | yes |  |  |
| `speaker` | `text` | no |  |  |
| `evidence_handles` | `jsonb` | no | `'[]'::jsonb` |  |
| `supersedes_claim_id` | `text` | yes |  | Opaque correlation identifier; no declared local table relationship. |
| `status` | `text` | no | `'active'::text` |  |
| `confidence` | `double precision` | no |  |  |
| `first_seen` | `timestamp with time zone` | no | `now()` |  |
| `reinforced_at` | `timestamp with time zone` | no | `now()` |  |
| `valid_until` | `timestamp with time zone` | yes |  |  |
| `source_path` | `text` | no |  |  |
| `source_line` | `bigint` | no |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `claims_pkey`: `claim_id`

### memory.embedding_models

来源：[memory.embedding_models](../../../opt/hatch/skills/muse_db/references/schema.md#L2440)。可见字段 5 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `embedding_model_id` | `bigint` | no | `nextval('memory.embedding_models_embedding_model_id_seq'::regclass)` | Local row identifier (primary key). |
| `model_name` | `text` | no |  |  |
| `dimensions` | `integer` | no |  |  |
| `distance_metric` | `text` | no |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `embedding_models_pkey`: `embedding_model_id`
- UNIQUE `embedding_models_model_name_dimensions_distance_metric_key`: `model_name`, `dimensions`, `distance_metric`

### memory.embeddings

来源：[memory.embeddings](../../../opt/hatch/skills/muse_db/references/schema.md#L2455)。可见字段 5 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `memory_embedding_id` | `bigint` | no | `nextval('memory.embeddings_memory_embedding_id_seq'::regclass)` | Local row identifier (primary key). |
| `memory_entry_id` | `bigint` | no |  | FK → `memory.entries.memory_entry_id` |
| `embedding_model_id` | `bigint` | no |  | FK → `memory.embedding_models.embedding_model_id` |
| `embedding` | `vector(384)` | no |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `embeddings_embedding_model_id_fkey`: `embedding_model_id` → `memory.embedding_models` (`embedding_model_id`)
- FOREIGN KEY `embeddings_memory_entry_id_fkey`: `memory_entry_id` → `memory.entries` (`memory_entry_id`)
- PRIMARY KEY `embeddings_pkey`: `memory_embedding_id`
- UNIQUE `embeddings_memory_entry_id_embedding_model_id_key`: `memory_entry_id`, `embedding_model_id`

### memory.entries

来源：[memory.entries](../../../opt/hatch/skills/muse_db/references/schema.md#L2472)。可见字段 15 个。

阅读重点：从 `status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `memory_entry_id` | `bigint` | no | `nextval('memory.entries_memory_entry_id_seq'::regclass)` | Local row identifier (primary key). |
| `memory_uri` | `text` | no |  |  |
| `chunk_id` | `text` | no |  | Memory chunk identity owned by this row; it has no separate owner table. |
| `source_type` | `text` | no |  |  |
| `status` | `text` | no |  |  |
| `privacy_class` | `text` | no |  |  |
| `confidence` | `double precision` | no | `1.0` |  |
| `citation_path` | `text` | yes |  |  |
| `line_start` | `bigint` | no | `0` |  |
| `line_end` | `bigint` | no | `0` |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `created_at_unix` | `bigint` | no | `0` |  |
| `title_text` | `text` | yes |  |  |
| `body_text` | `text` | no |  |  |
| `reason_text` | `text` | yes |  |  |

键与约束：

- PRIMARY KEY `entries_pkey`: `memory_entry_id`
- UNIQUE `entries_memory_uri_key`: `memory_uri`

### memory.entry_attributes

来源：[memory.entry_attributes](../../../opt/hatch/skills/muse_db/references/schema.md#L2497)。可见字段 4 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `memory_entry_attribute_id` | `bigint` | no | `nextval('memory.entry_attributes_memory_entry_attribute_id_seq'::regclass)` | Local row identifier (primary key). |
| `memory_entry_id` | `bigint` | no |  | FK → `memory.entries.memory_entry_id` |
| `attribute_name` | `text` | no |  |  |
| `scalar_value` | `text` | no |  |  |

键与约束：

- FOREIGN KEY `entry_attributes_memory_entry_id_fkey`: `memory_entry_id` → `memory.entries` (`memory_entry_id`)
- PRIMARY KEY `entry_attributes_pkey`: `memory_entry_attribute_id`
- UNIQUE `entry_attributes_memory_entry_id_attribute_name_key`: `memory_entry_id`, `attribute_name`

### memory.metadata

来源：[memory.metadata](../../../opt/hatch/skills/muse_db/references/schema.md#L2512)。可见字段 3 个。

阅读重点：从 `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `key` | `text` | no |  | Local row identifier (primary key). |
| `value` | `text` | no |  |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `metadata_pkey`: `key`

<a id="domain-messages"></a>
## messages

消息相关持久状态；以字段声明的真实 owner 解析，不以字段名猜测连接。

### messages.native

来源：[messages.native](../../../opt/hatch/skills/muse_db/references/schema.md#L2526)。可见字段 12 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `message_id` | `bigint` | no | `nextval('messages.native_message_id_seq'::regclass)` | Local row identifier (primary key). |
| `node_id` | `text` | no |  | Soft local reference → `device.nodes.node_id`. |
| `external_id` | `text` | no |  | External/provider identifier; no Muse PostgreSQL owner table. |
| `thread_id` | `text` | yes |  | Provider-native message-thread identifier; no Muse PostgreSQL owner table. |
| `address` | `text` | yes |  |  |
| `contact_name` | `text` | yes |  |  |
| `body` | `text` | yes |  |  |
| `direction` | `text` | yes |  |  |
| `kind` | `text` | yes |  |  |
| `is_read` | `boolean` | yes |  |  |
| `sent_at_unix_ms` | `bigint` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `native_pkey`: `message_id`
- UNIQUE `native_node_id_external_id_key`: `node_id`, `external_id`

<a id="domain-podcasts"></a>
## podcasts

节目、feed 与 episode 身份；本地生成、上传 provider 和发布不是同一状态。

### podcasts.episodes

来源：[podcasts.episodes](../../../opt/hatch/skills/muse_db/references/schema.md#L2550)。可见字段 14 个。

阅读重点：从 `created_at`, `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `slug` | `text` | no |  | Local row identifier (primary key). |
| `title` | `text` | no |  |  |
| `description` | `text` | no | `''::text` |  |
| `created_at` | `text` | no |  |  |
| `duration_secs` | `bigint` | no |  |  |
| `audio_path` | `text` | no |  |  |
| `chunk_count` | `bigint` | no |  |  |
| `cover_path` | `text` | yes |  |  |
| `episode_url` | `text` | yes |  |  |
| `feed_url` | `text` | yes |  |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |
| `spotify_episode_uri` | `text` | yes |  |  |
| `script` | `text` | yes |  |  |
| `topics` | `text` | yes |  |  |

键与约束：

- PRIMARY KEY `episodes_pkey`: `slug`

### podcasts.feed

来源：[podcasts.feed](../../../opt/hatch/skills/muse_db/references/schema.md#L2573)。可见字段 8 个。

阅读重点：从 `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `singleton` | `boolean` | no | `true` | Local row identifier (primary key). |
| `feed_title` | `text` | no |  |  |
| `feed_id` | `text` | yes |  | Soft local reference → `podcasts.feeds.feed_id`, naming whichever feed was published to most recently. `podcasts.feeds` is the full catalog; join episodes to it on `feed_url`, not through this row. |
| `feed_url` | `text` | yes |  |  |
| `cover_path` | `text` | yes |  |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |
| `spotify_show_url` | `text` | yes |  |  |
| `spotify_show_id` | `text` | yes |  | Spotify provider identifier; no Muse PostgreSQL owner table. |

键与约束：

- PRIMARY KEY `feed_pkey`: `singleton`

### podcasts.feeds

来源：[podcasts.feeds](../../../opt/hatch/skills/muse_db/references/schema.md#L2590)。可见字段 8 个。

阅读重点：从 `created_at`, `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `feed_id` | `text` | no |  | Local row identifier (primary key). |
| `feed_title` | `text` | no |  |  |
| `feed_url` | `text` | yes |  |  |
| `cover_path` | `text` | yes |  |  |
| `spotify_show_url` | `text` | yes |  |  |
| `spotify_show_id` | `text` | yes |  | Spotify provider identifier; no Muse PostgreSQL owner table. |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `feeds_pkey`: `feed_id`

<a id="domain-runtime"></a>
## runtime

请求、工作、消息、调用、浏览器、付款及交付状态；业务对象和执行实例需保留各自 ID。

### runtime.agent_todo_snapshots

来源：[runtime.agent_todo_snapshots](../../../opt/hatch/skills/muse_db/references/schema.md#L2609)。可见字段 5 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `conversation_id` | `text` | no |  | Local row identifier (primary key). |
| `agent_identity` | `text` | no |  | Local row identifier (primary key). |
| `items_json` | `text` | no | `'[]'::text` |  |
| `revision` | `bigint` | no | `1` |  |
| `updated_at_ms` | `bigint` | no | `((EXTRACT(epoch FROM now()) * (1000)::numeric))::bigint` |  |

键与约束：

- PRIMARY KEY `agent_todo_snapshots_pkey`: `conversation_id`, `agent_identity`

### runtime.avatar_state

来源：[runtime.avatar_state](../../../opt/hatch/skills/muse_db/references/schema.md#L2623)。可见字段 19 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `singleton` | `boolean` | no | `true` | Local row identifier (primary key). |
| `active_stem` | `text` | no | `''::text` |  |
| `image_path` | `text` | no | `''::text` |  |
| `darkmode_image_path` | `text` | yes |  |  |
| `chat_theme_color` | `text` | yes |  |  |
| `chat_theme_color_override` | `text` | yes |  |  |
| `static_frame_paths` | `text[]` | no | `'{}'::text[]` |  |
| `video_variants_json` | `text` | no | `'{}'::text` |  |
| `darkmode_video_variants_json` | `text` | no | `'{}'::text` |  |
| `video_variant_repair_json` | `text` | no | `'{}'::text` |  |
| `darkmode_video_variant_repair_json` | `text` | no | `'{}'::text` |  |
| `revision` | `bigint` | no | `0` |  |
| `updated_at_ms` | `bigint` | no | `((EXTRACT(epoch FROM now()) * (1000)::numeric))::bigint` |  |
| `image_variant_assets_json` | `text` | no | `'{"assets":[]}'::text` |  |
| `avatar_asset_repair_json` | `text` | no | `'{"repairs":[]}'::text` |  |
| `choreography_profile_json` | `text` | yes |  |  |
| `finalization_id` | `text` | yes |  | Opaque correlation identifier; no declared local table relationship. |
| `avatar_milestones_json` | `text` | no | `'{}'::text` |  |
| `legacy_folded_at_ms` | `bigint` | yes |  |  |

键与约束：

- PRIMARY KEY `avatar_state_pkey`: `singleton`

### runtime.browser_tasks

来源：[runtime.browser_tasks](../../../opt/hatch/skills/muse_db/references/schema.md#L2651)。可见字段 50 个。

阅读重点：从 `status`, `completed_at`, `state_revision`, `outcome_status`, `browser_navigation_attempted` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 9 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `task_id` | `text` | no |  | Local row identifier (primary key). |
| `browser_session_id` | `text` | no | `'default'::text` | Browser-runtime identifier; no Muse PostgreSQL owner table. |
| `root_session_id` | `text` | no |  | Soft local reference → `agent.sessions.session_id`. |
| `owner_agent_id` | `text` | yes |  | For agent-created tasks, including historical null `owner_kind`, soft local reference → `agent.agents.agent_id`. When `owner_kind` is `user`, NULL; no executing agent or owner row. |
| `root_message_id` | `text` | no |  | For agent-created tasks, including historical null `owner_kind`, soft local reference → `runtime.messages.message_id`. When `owner_kind` is `user`, repeats this row's `task_id`; no message owner row. |
| `stream_owner_message_id` | `text` | no |  | For agent-created tasks, including historical null `owner_kind`, soft local reference → `runtime.messages.message_id`. When `owner_kind` is `user`, repeats this row's `task_id`; no message owner row. |
| `status` | `text` | no |  |  |
| `title` | `text` | no | `'Browser task'::text` |  |
| `step_count` | `integer` | no | `0` |  |
| `channel_context_json` | `text` | yes |  |  |
| `latest_action_id` | `text` | yes |  | Browser-runtime action identifier; no Muse PostgreSQL owner table. |
| `latest_tab_json` | `text` | yes |  |  |
| `latest_screenshot_json` | `text` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |
| `completed_at` | `timestamp with time zone` | yes |  |  |
| `terminal_reason` | `text` | yes |  |  |
| `admission_seq` | `bigint` | yes |  |  |
| `presentation_root_session_id` | `text` | yes |  | Soft local reference → `agent.sessions.session_id`. |
| `parent_agent_id` | `text` | yes |  | Soft local reference → `agent.agents.agent_id`. |
| `tool_call_id` | `text` | yes |  | For agent-created tasks, including historical null `owner_kind`, soft local reference → `runtime.tool_calls.call_id` (the text correlation identifier, not its numeric `tool_call_id`). When `owner_kind` is `user`, repeats this row's `task_id`; no tool call or owner row. |
| `request_trace_context_json` | `text` | yes |  |  |
| `requester_source` | `text` | yes |  |  |
| `requester_channel` | `text` | yes |  |  |
| `requester_model` | `text` | yes |  |  |
| `requester_effective_model` | `text` | yes |  |  |
| `request_mode_json` | `text` | yes |  |  |
| `max_training_tier_json` | `text` | yes |  |  |
| `is_task_card_visible` | `boolean` | no | `false` |  |
| `initial_instruction` | `text` | yes |  |  |
| `history_source_agent_id` | `text` | yes |  | Soft local reference → `agent.agents.agent_id`. |
| `state_revision` | `bigint` | no | `0` |  |
| `deadline_at` | `timestamp with time zone` | yes |  |  |
| `continuation_root_task_id` | `text` | yes |  | Soft local reference → `runtime.browser_tasks.task_id`. |
| `terminal_interrupt_subtype` | `text` | yes |  |  |
| `outcome_status` | `text` | yes |  |  |
| `outcome_reason` | `text` | yes |  |  |
| `outcome_at` | `timestamp with time zone` | yes |  |  |
| `retention_end_reason` | `text` | yes |  |  |
| `card_generation` | `bigint` | no | `0` |  |
| `input_grants_json` | `text` | no | `'{"version":1,"grants":[]}'::text` |  |
| `browser_navigation_attempted` | `boolean` | no | `false` |  |
| `terminal_user_update_due_at` | `timestamp with time zone` | yes |  | Non-null while this terminal occurrence still owes its user-facing ending update; also serves as the worker retry/claim time. |
| `egress_profile` | `text` | yes |  |  |
| `run_number` | `bigint` | yes |  |  |
| `run_started_at` | `timestamp with time zone` | yes |  |  |
| `run_presentation_locale` | `text` | yes |  | BCP 47 presentation locale frozen for the current BrowserTask run; null legacy rows read as en-US |
| `run_location_context_json` | `text` | yes |  |  |
| `owner_kind` | `text` | yes |  | Creation origin: user, main_agent, or cron; null when unknown. Immutable across takeover and continuation. User leases have a null owner_agent_id and reserve root_message_id, stream_owner_message_id and tool_call_id with task_id and have no executing agent, chat card or terminal chat delivery. Rust owns the vocabulary and lifecycle. |
| `broker_instance` | `text` | no | `'user'::text` | Immutable physical browser owner selected by trusted admission: user or cron. Independent of logical owner_kind and retained across continuation. |

键与约束：

- PRIMARY KEY `browser_tasks_pkey`: `task_id`

### runtime.channel_deliveries

来源：[runtime.channel_deliveries](../../../opt/hatch/skills/muse_db/references/schema.md#L2710)。可见字段 14 个。

阅读重点：从 `state`, `attempt_count`, `next_attempt_at_utc`, `last_error` 检查状态或失败信息；字段存在不说明允许哪些状态转换。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `delivery_key` | `text` | no |  | Local row identifier (primary key). |
| `delivery_kind` | `text` | no |  |  |
| `surface` | `text` | no |  |  |
| `target` | `text` | yes |  |  |
| `payload_json` | `text` | no |  |  |
| `state` | `text` | no |  |  |
| `dispatch_boot_generation` | `text` | yes |  |  |
| `attempt_count` | `integer` | no | `0` |  |
| `next_attempt_at_utc` | `bigint` | no |  |  |
| `result_json` | `text` | yes |  |  |
| `last_error` | `text` | yes |  |  |
| `created_at_utc` | `bigint` | no |  |  |
| `updated_at_utc` | `bigint` | no |  |  |
| `terminal_at_utc` | `bigint` | yes |  |  |

键与约束：

- PRIMARY KEY `channel_deliveries_pkey`: `delivery_key`

### runtime.channel_message_bindings

来源：[runtime.channel_message_bindings](../../../opt/hatch/skills/muse_db/references/schema.md#L2733)。可见字段 9 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `binding_id` | `bigint` | no | `nextval('runtime.channel_message_bindings_binding_id_seq'::regclass)` | Local row identifier (primary key). |
| `channel_message_id` | `text` | yes |  | Provider-native channel message identifier; no Muse PostgreSQL owner table. |
| `channel` | `text` | yes |  |  |
| `jarvis_message_id` | `text` | no |  | Soft local reference → `runtime.messages.message_id`. |
| `provider` | `text` | yes |  |  |
| `provider_channel_id` | `text` | yes |  | External/provider identifier; no Muse PostgreSQL owner table. |
| `provider_message_id` | `text` | yes |  | External/provider identifier; no Muse PostgreSQL owner table. |
| `created_at_ms` | `bigint` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `channel_message_bindings_pkey`: `binding_id`
- UNIQUE `channel_message_bindings_channel_message_id_channel_key`: `channel_message_id`, `channel`
- UNIQUE `channel_message_bindings_provider_provider_channel_id_provi_key`: `provider`, `provider_channel_id`, `provider_message_id`

### runtime.chat_event_derived_write_backlog

来源：[runtime.chat_event_derived_write_backlog](../../../opt/hatch/skills/muse_db/references/schema.md#L2753)。可见字段 7 个。

阅读重点：从 `attempts`, `last_error` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `event_seq` | `bigint` | no |  | FK → `runtime.events.event_seq` |
| `resources_json` | `text` | no | `'[]'::text` |  |
| `attempts` | `integer` | no | `0` |  |
| `last_error` | `text` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |
| `deadlettered_at` | `timestamp with time zone` | yes |  |  |

键与约束：

- FOREIGN KEY `chat_event_derived_write_backlog_event_seq_fkey`: `event_seq` → `runtime.events` (`event_seq`)
- PRIMARY KEY `chat_event_derived_write_backlog_pkey`: `event_seq`

### runtime.checkout_spend_checkpoints

来源：[runtime.checkout_spend_checkpoints](../../../opt/hatch/skills/muse_db/references/schema.md#L2770)。可见字段 7 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `operation_id` | `text` | no |  | FK → `runtime.checkout_spend_operations.operation_id` |
| `provider` | `text` | no |  |  |
| `checkpoint_key` | `text` | no |  | Local row identifier (primary key). |
| `external_id` | `text` | yes |  | External/provider identifier; no Muse PostgreSQL owner table. |
| `detail` | `jsonb` | yes |  |  |
| `claimed_at_ms` | `bigint` | no |  |  |
| `bound_at_ms` | `bigint` | yes |  |  |

键与约束：

- FOREIGN KEY `checkout_spend_checkpoints_operation_id_fkey`: `operation_id` → `runtime.checkout_spend_operations` (`operation_id`)
- PRIMARY KEY `checkout_spend_checkpoints_pkey`: `operation_id`, `checkpoint_key`

### runtime.checkout_spend_operations

来源：[runtime.checkout_spend_operations](../../../opt/hatch/skills/muse_db/references/schema.md#L2787)。可见字段 12 个。

阅读重点：从 `state` 检查状态或失败信息；字段存在不说明允许哪些状态转换。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `operation_id` | `text` | no |  | Local row identifier (primary key). |
| `client_task_key` | `text` | no |  |  |
| `checkout_request_id` | `text` | yes |  | Checkout correlation key owned by this operation row; no separate owner table. |
| `wallet_request_id` | `text` | yes |  | Wallet-provider request identifier; no Muse PostgreSQL owner table. |
| `approval_id` | `text` | yes |  | Sentinel approval identifier; Stripe Link spend rows mirror it in `runtime.stripe_link_spend_requests`. |
| `state` | `text` | no |  |  |
| `expires_at_ms` | `bigint` | no |  |  |
| `created_at_ms` | `bigint` | no |  |  |
| `updated_at_ms` | `bigint` | no |  |  |
| `terminal_result` | `jsonb` | yes |  |  |
| `recovery_epoch` | `smallint` | no | `0` |  |
| `wallet_provider` | `text` | no | `'stripe-link'::text` |  |

键与约束：

- PRIMARY KEY `checkout_spend_operations_pkey`: `operation_id`

### runtime.client_rendering_capabilities

来源：[runtime.client_rendering_capabilities](../../../opt/hatch/skills/muse_db/references/schema.md#L2808)。可见字段 6 个。

阅读重点：从 `declared_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `singleton` | `boolean` | no | `true` | Local row identifier (primary key). |
| `client_id` | `text` | no |  | Client installation identifier; no separate Muse PostgreSQL owner table. |
| `platform` | `text` | no |  |  |
| `supported_presentations` | `text[]` | no | `'{}'::text[]` |  |
| `supported_inline_presentations` | `text[]` | no | `'{}'::text[]` |  |
| `declared_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `client_rendering_capabilities_pkey`: `singleton`

### runtime.context_snapshots

来源：[runtime.context_snapshots](../../../opt/hatch/skills/muse_db/references/schema.md#L2823)。可见字段 12 个。

阅读重点：从 `state_json`, `last_error` 检查状态或失败信息；字段存在不说明允许哪些状态转换。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `snapshot_kind` | `text` | no |  | Local row identifier (primary key). |
| `owner_key` | `text` | no |  | Local row identifier (primary key). |
| `version` | `bigint` | no |  |  |
| `source_watermark` | `text` | yes |  |  |
| `fingerprint` | `text` | yes |  |  |
| `freshness_class` | `text` | no |  |  |
| `state_json` | `text` | no | `'{}'::text` |  |
| `refreshed_at` | `timestamp with time zone` | no | `now()` |  |
| `invalidated_at` | `timestamp with time zone` | yes |  |  |
| `stale_after` | `timestamp with time zone` | yes |  |  |
| `last_error` | `text` | yes |  |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `context_snapshots_pkey`: `snapshot_kind`, `owner_key`

### runtime.dev_notice_watermark

来源：[runtime.dev_notice_watermark](../../../opt/hatch/skills/muse_db/references/schema.md#L2844)。可见字段 2 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `singleton` | `boolean` | no | `true` | Local row identifier (primary key). |
| `last_seen_version_id` | `bigint` | no |  | Version from the code-owned developer-notice catalog; no owner table. |

键与约束：

- PRIMARY KEY `dev_notice_watermark_pkey`: `singleton`

### runtime.event_channels

来源：[runtime.event_channels](../../../opt/hatch/skills/muse_db/references/schema.md#L2855)。可见字段 2 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `channel` | `text` | no |  | Local row identifier (primary key). |
| `event_seq` | `bigint` | no |  | FK → `runtime.events.event_seq` |

键与约束：

- FOREIGN KEY `event_channels_event_seq_fkey`: `event_seq` → `runtime.events` (`event_seq`)
- PRIMARY KEY `event_channels_pkey`: `channel`, `event_seq`

### runtime.event_hook_space_owners

来源：[runtime.event_hook_space_owners](../../../opt/hatch/skills/muse_db/references/schema.md#L2867)。可见字段 4 个。

阅读重点：从 `created_at`, `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `hook_id` | `text` | no |  | Local row identifier (primary key). |
| `space_slug` | `text` | no |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `event_hook_space_owners_pkey`: `hook_id`

### runtime.event_payload_fields

来源：[runtime.event_payload_fields](../../../opt/hatch/skills/muse_db/references/schema.md#L2880)。可见字段 6 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `event_payload_field_id` | `bigint` | no | `nextval('runtime.event_payload_fields_event_payload_field_id_seq'::regclass)` | Local row identifier (primary key). |
| `event_seq` | `bigint` | no |  | FK → `runtime.events.event_seq` |
| `field_path` | `text` | no |  |  |
| `scalar_type` | `text` | no |  |  |
| `scalar_value` | `text` | yes |  |  |
| `text_value` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `event_payload_fields_event_seq_fkey`: `event_seq` → `runtime.events` (`event_seq`)
- PRIMARY KEY `event_payload_fields_pkey`: `event_payload_field_id`
- UNIQUE `event_payload_fields_event_seq_field_path_key`: `event_seq`, `field_path`

### runtime.events

来源：[runtime.events](../../../opt/hatch/skills/muse_db/references/schema.md#L2897)。可见字段 24 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 9 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `event_seq` | `bigint` | no | `nextval('runtime.events_event_seq_seq'::regclass)` | Local row identifier (primary key). |
| `event_id` | `uuid` | no | `gen_random_uuid()` | Stable local event identifier owned by this row; `event_seq` is its primary key. |
| `event_kind` | `runtime.event_kind` | no |  |  |
| `event_name` | `text` | no |  |  |
| `request_id` | `text` | yes |  | FK → `runtime.requests.request_id` |
| `root_request_id` | `text` | yes |  | FK → `runtime.requests.request_id` |
| `parent_request_id` | `text` | yes |  | FK → `runtime.requests.request_id` |
| `transcript_surface` | `runtime.transcript_surface` | no |  |  |
| `visibility` | `runtime.visibility` | no |  |  |
| `source` | `text` | no |  |  |
| `role` | `runtime.message_role` | yes |  |  |
| `chat_kind` | `text` | no | `'direct'::text` |  |
| `stream_lane` | `text` | no | `'main'::text` |  |
| `message_id` | `text` | yes |  | Soft local reference → `runtime.messages.message_id`. |
| `parent_message_id` | `text` | yes |  | Soft local reference → `runtime.messages.message_id`. |
| `reply_to_message_id` | `text` | yes |  | Soft local reference → `runtime.messages.message_id`. |
| `reply_target_message_id` | `text` | yes |  | Soft local reference → `runtime.messages.message_id`. |
| `parent_agent_id` | `text` | yes |  | Soft local reference → `agent.agents.agent_id`. |
| `agent_id` | `text` | yes |  | Soft local reference → `agent.agents.agent_id`. |
| `idempotency_key` | `text` | yes |  |  |
| `display_text_ready` | `boolean` | no | `true` |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `payload_json` | `text` | yes |  |  |
| `channel_context_json` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `events_parent_request_id_fkey`: `parent_request_id` → `runtime.requests` (`request_id`)
- FOREIGN KEY `events_request_id_fkey`: `request_id` → `runtime.requests` (`request_id`)
- FOREIGN KEY `events_root_request_id_fkey`: `root_request_id` → `runtime.requests` (`request_id`)
- PRIMARY KEY `events_pkey`: `event_seq`
- UNIQUE `events_event_id_key`: `event_id`
- UNIQUE `events_idempotency_key_key`: `idempotency_key`

### runtime.execute_resolve_runs

来源：[runtime.execute_resolve_runs](../../../opt/hatch/skills/muse_db/references/schema.md#L2935)。可见字段 19 个。

阅读重点：从 `status`, `last_error_stage`, `last_error_message` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 4 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `run_id` | `text` | no |  | Local row identifier (primary key). |
| `worker_kind` | `text` | no |  |  |
| `source_ref` | `text` | no |  |  |
| `lane_key` | `text` | no |  |  |
| `status` | `text` | no |  |  |
| `terminal_decision` | `text` | yes |  |  |
| `terminal_message` | `text` | yes |  |  |
| `handoff_message_id` | `text` | yes |  | Soft local reference → `runtime.messages.message_id`. |
| `last_error_stage` | `text` | yes |  |  |
| `last_error_message` | `text` | yes |  |  |
| `metadata_json` | `jsonb` | no | `'{}'::jsonb` |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |
| `worker_generation` | `bigint` | no | `0` |  |
| `worker_phase` | `text` | yes |  |  |
| `worker_agent_id` | `text` | yes |  | Soft local reference → `agent.agents.agent_id`. |
| `worker_started_at` | `timestamp with time zone` | yes |  |  |
| `execute_message_id` | `text` | yes |  | Soft local reference → `runtime.messages.message_id`. |
| `resolve_message_id` | `text` | yes |  | Soft local reference → `runtime.messages.message_id`. |

键与约束：

- PRIMARY KEY `execute_resolve_runs_pkey`: `run_id`
- UNIQUE `execute_resolve_runs_source_unique`: `worker_kind`, `source_ref`

### runtime.idea_execution_pending

来源：[runtime.idea_execution_pending](../../../opt/hatch/skills/muse_db/references/schema.md#L2964)。可见字段 7 个。

阅读重点：从 `dispatched_at`, `reconciled_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 3 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `activation_id` | `text` | no |  | Local row identifier (primary key). |
| `root_submission_message_id` | `text` | no |  | Soft local reference → `runtime.messages.message_id`. |
| `session_id` | `text` | no |  | Soft local reference → `agent.sessions.session_id`. |
| `idea_card_id` | `text` | no |  | Soft local reference → `ideas.ideas.idea_id`. |
| `idea_card_kind` | `text` | no |  |  |
| `dispatched_at` | `timestamp with time zone` | no | `now()` |  |
| `reconciled_at` | `timestamp with time zone` | yes |  |  |

键与约束：

- PRIMARY KEY `idea_execution_pending_pkey`: `activation_id`

### runtime.invite_badge_seen_state

来源：[runtime.invite_badge_seen_state](../../../opt/hatch/skills/muse_db/references/schema.md#L2980)。可见字段 2 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `singleton` | `boolean` | no | `true` | Local row identifier (primary key). |
| `last_seen_badge_version` | `bigint` | no | `0` |  |

键与约束：

- PRIMARY KEY `invite_badge_seen_state_pkey`: `singleton`

### runtime.maintenance_markers

来源：[runtime.maintenance_markers](../../../opt/hatch/skills/muse_db/references/schema.md#L2991)。可见字段 3 个。

阅读重点：从 `completed_at` 检查状态或失败信息；字段存在不说明允许哪些状态转换。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `marker_key` | `text` | no |  | Local row identifier (primary key). |
| `completed_at` | `timestamp with time zone` | no | `now()` |  |
| `detail_json` | `jsonb` | no | `'{}'::jsonb` |  |

键与约束：

- PRIMARY KEY `maintenance_markers_pkey`: `marker_key`

### runtime.message_attachments

来源：[runtime.message_attachments](../../../opt/hatch/skills/muse_db/references/schema.md#L3003)。可见字段 10 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `attachment_id` | `bigint` | no | `nextval('runtime.message_attachments_attachment_id_seq'::regclass)` | Local row identifier (primary key). |
| `message_id` | `text` | no |  | FK → `runtime.messages.message_id` |
| `ordinal` | `integer` | no |  |  |
| `attachment_kind` | `text` | no |  |  |
| `file_uri` | `text` | no |  |  |
| `media_type` | `text` | yes |  |  |
| `byte_len` | `bigint` | yes |  |  |
| `sha256` | `bytea` | yes |  |  |
| `caption_text` | `text` | yes |  |  |
| `transcription_text` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `message_attachments_message_id_fkey`: `message_id` → `runtime.messages` (`message_id`)
- PRIMARY KEY `message_attachments_pkey`: `attachment_id`
- UNIQUE `message_attachments_message_id_ordinal_key`: `message_id`, `ordinal`

### runtime.message_reactions

来源：[runtime.message_reactions](../../../opt/hatch/skills/muse_db/references/schema.md#L3024)。可见字段 3 个。

阅读重点：从 `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `message_id` | `text` | no |  | FK → `runtime.messages.message_id` |
| `reaction_emoji` | `text` | yes |  |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `message_reactions_message_id_fkey`: `message_id` → `runtime.messages` (`message_id`)
- PRIMARY KEY `message_reactions_pkey`: `message_id`

### runtime.messages

来源：[runtime.messages](../../../opt/hatch/skills/muse_db/references/schema.md#L3037)。可见字段 8 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `message_id` | `text` | no |  | Local row identifier (primary key). |
| `event_seq` | `bigint` | no |  | FK → `runtime.events.event_seq` |
| `role` | `runtime.message_role` | no |  |  |
| `prompt_rendering_id` | `bigint` | yes |  | Prompt-rendering identifier; no queryable owner table. |
| `author_label` | `text` | yes |  |  |
| `provider_message_id` | `text` | yes |  | External/provider identifier; no Muse PostgreSQL owner table. |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `body` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `messages_event_seq_fkey`: `event_seq` → `runtime.events` (`event_seq`)
- PRIMARY KEY `messages_pkey`: `message_id`
- UNIQUE `messages_event_seq_key`: `event_seq`

### runtime.product_improvements_preference

来源：[runtime.product_improvements_preference](../../../opt/hatch/skills/muse_db/references/schema.md#L3056)。可见字段 3 个。

阅读重点：从 `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `singleton` | `boolean` | no | `true` | Local row identifier (primary key). |
| `enabled` | `boolean` | no |  |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `product_improvements_preference_pkey`: `singleton`

### runtime.raw_signal_collections

来源：[runtime.raw_signal_collections](../../../opt/hatch/skills/muse_db/references/schema.md#L3068)。可见字段 12 个。

阅读重点：从 `fetched_at`, `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `collection_id` | `uuid` | no |  | Local row identifier (primary key). |
| `tool` | `text` | no |  |  |
| `mode` | `text` | no |  |  |
| `fetched_at` | `timestamp with time zone` | no |  |  |
| `partial` | `boolean` | no |  |  |
| `skipped` | `boolean` | no |  |  |
| `per_request_timeout_secs` | `integer` | no |  |  |
| `max_total_secs` | `integer` | no |  |  |
| `source_names` | `text[]` | no |  |  |
| `entry_count` | `integer` | no |  |  |
| `metadata_json` | `jsonb` | no | `'{}'::jsonb` |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `raw_signal_collections_pkey`: `collection_id`

### runtime.raw_signal_entries

来源：[runtime.raw_signal_entries](../../../opt/hatch/skills/muse_db/references/schema.md#L3089)。可见字段 15 个。

阅读重点：从 `status`, `error` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `entry_id` | `bigint` | no | `nextval('runtime.raw_signal_entries_entry_id_seq'::regclass)` | Local row identifier (primary key). |
| `collection_id` | `uuid` | no |  | FK → `runtime.raw_signal_collections.collection_id` |
| `ordinal` | `integer` | no |  |  |
| `source` | `text` | no |  |  |
| `name` | `text` | no |  |  |
| `method` | `text` | no |  |  |
| `logical_url` | `text` | no |  |  |
| `ok` | `boolean` | no |  |  |
| `status` | `integer` | yes |  |  |
| `logical_path` | `text` | yes |  |  |
| `error` | `text` | yes |  |  |
| `duration_ms` | `bigint` | no |  |  |
| `bytes` | `bigint` | yes |  |  |
| `body_json` | `jsonb` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `raw_signal_entries_collection_id_fkey`: `collection_id` → `runtime.raw_signal_collections` (`collection_id`)
- PRIMARY KEY `raw_signal_entries_pkey`: `entry_id`
- UNIQUE `raw_signal_entries_collection_ordinal_unique`: `collection_id`, `ordinal`

### runtime.requests

来源：[runtime.requests](../../../opt/hatch/skills/muse_db/references/schema.md#L3115)。可见字段 7 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `request_id` | `text` | no |  | Local row identifier (primary key). |
| `root_request_id` | `text` | yes |  | FK → `runtime.requests.request_id` |
| `parent_request_id` | `text` | yes |  | FK → `runtime.requests.request_id` |
| `request_origin` | `text` | no |  |  |
| `transcript_surface` | `runtime.transcript_surface` | no |  |  |
| `root_work_class` | `text` | no |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `requests_parent_request_id_fkey`: `parent_request_id` → `runtime.requests` (`request_id`)
- FOREIGN KEY `requests_root_request_id_fkey`: `root_request_id` → `runtime.requests` (`request_id`)
- PRIMARY KEY `requests_pkey`: `request_id`

### runtime.resources

来源：[runtime.resources](../../../opt/hatch/skills/muse_db/references/schema.md#L3133)。可见字段 10 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `resource_id` | `bigint` | no | `nextval('runtime.resources_resource_id_seq'::regclass)` | Local row identifier (primary key). |
| `event_seq` | `bigint` | no |  | FK → `runtime.events.event_seq` |
| `ordinal` | `integer` | no | `0` |  |
| `resource_kind` | `text` | no |  |  |
| `resource_key` | `text` | no |  |  |
| `label` | `text` | yes |  |  |
| `mime_type` | `text` | yes |  |  |
| `size_bytes` | `bigint` | yes |  |  |
| `metadata_json` | `text` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `resources_event_seq_fkey`: `event_seq` → `runtime.events` (`event_seq`)
- PRIMARY KEY `resources_pkey`: `resource_id`
- UNIQUE `resources_event_seq_ordinal_key`: `event_seq`, `ordinal`

### runtime.search_documents

来源：[runtime.search_documents](../../../opt/hatch/skills/muse_db/references/schema.md#L3154)。可见字段 7 个。

阅读重点：从 `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `search_document_id` | `bigint` | no | `nextval('runtime.search_documents_search_document_id_seq'::regclass)` | Local row identifier (primary key). |
| `owner_table` | `text` | no |  |  |
| `owner_key` | `text` | no |  |  |
| `language` | `regconfig` | no | `'english'::regconfig` |  |
| `search_vector` | `tsvector` | no |  |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |
| `search_text` | `text` | no |  |  |

键与约束：

- PRIMARY KEY `search_documents_pkey`: `search_document_id`
- UNIQUE `search_documents_owner_table_owner_key_key`: `owner_table`, `owner_key`

### runtime.skill_invalidation_state

来源：[runtime.skill_invalidation_state](../../../opt/hatch/skills/muse_db/references/schema.md#L3171)。可见字段 5 个。

阅读重点：从 `last_delivered_invalidation_hash` 检查状态或失败信息；字段存在不说明允许哪些状态转换。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `skill_name` | `text` | no |  | Local row identifier (primary key). |
| `used` | `boolean` | no | `false` |  |
| `pending_invalidation_hash` | `text` | yes |  |  |
| `pending_manifest_rel_path` | `text` | yes |  |  |
| `last_delivered_invalidation_hash` | `text` | yes |  |  |

键与约束：

- PRIMARY KEY `skill_invalidation_state_pkey`: `skill_name`

### runtime.stripe_link_spend_requests

来源：[runtime.stripe_link_spend_requests](../../../opt/hatch/skills/muse_db/references/schema.md#L3185)。可见字段 21 个。

阅读重点：从 `lifecycle_state`, `create_attempt_id`, `cancel_attempt_id`, `cancellation_confirmation_task_state_revision` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 4 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `approval_id` | `text` | no |  | Local row identifier (primary key). |
| `continuation_root_task_id` | `text` | no |  | Soft local reference → `runtime.browser_tasks.task_id`. |
| `merchant_origin` | `text` | no |  |  |
| `checkout_metadata` | `jsonb` | no |  |  |
| `approved_amount_minor` | `bigint` | no |  |  |
| `approved_currency` | `text` | no |  |  |
| `lifecycle_state` | `text` | no |  |  |
| `create_attempt_id` | `uuid` | no |  | Idempotency token owned by this spend-request row. |
| `stripe_spend_request_id` | `text` | yes |  | Stripe Link provider identifier; no Muse PostgreSQL owner table. |
| `expires_at` | `timestamp with time zone` | no |  |  |
| `assigned_browser_task_id` | `text` | yes |  | Soft local reference → `runtime.browser_tasks.task_id`. |
| `assigned_at` | `timestamp with time zone` | yes |  |  |
| `cancel_attempt_id` | `uuid` | yes |  | Cancellation idempotency token owned by this spend-request row. |
| `closed_at` | `timestamp with time zone` | yes |  |  |
| `close_reason` | `text` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `owner_browser_task_id` | `text` | yes |  | Soft local reference → `runtime.browser_tasks.task_id`. Exact current BrowserTask command owner. Null only for carried rows whose owner was not durably provable. |
| `claiming_browser_task_lineage_id` | `text` | yes |  | Browser-runtime lineage claim; no standalone Muse PostgreSQL owner table. Movable current-owner lineage claim; retained after successful checkout and cleared by cancellation/no-effect/expiry. |
| `cancellation_confirmation_task_state_revision` | `bigint` | yes |  | Exact parked challenge revision before response, then exact resumed running revision after response. |
| `cancellation_confirmation_response_message_id` | `text` | yes |  | Soft local reference → `runtime.messages.message_id`. Authentic User-authority message admitted to resume the retained BrowserTask. |
| `wallet_provider` | `text` | no | `'stripe-link'::text` | Wallet provider owning this direct BrowserTask lifecycle. The table name is retained only for rolling compatibility. |

键与约束：

- PRIMARY KEY `stripe_link_spend_requests_pkey`: `approval_id`

### runtime.summaries

来源：[runtime.summaries](../../../opt/hatch/skills/muse_db/references/schema.md#L3215)。可见字段 4 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `id` | `bigint` | no | `nextval('runtime.summaries_id_seq'::regclass)` | Local row identifier (primary key). |
| `summary_key` | `text` | yes |  |  |
| `summary_text` | `text` | yes |  |  |
| `created_at_ms` | `bigint` | no | `((EXTRACT(epoch FROM now()))::bigint * 1000)` |  |

键与约束：

- PRIMARY KEY `summaries_pkey`: `id`

### runtime.tool_calls

来源：[runtime.tool_calls](../../../opt/hatch/skills/muse_db/references/schema.md#L3228)。可见字段 8 个。

阅读重点：从 `status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `tool_call_id` | `bigint` | no | `nextval('runtime.tool_calls_tool_call_id_seq'::regclass)` | Local row identifier (primary key). |
| `event_seq` | `bigint` | no |  | FK → `runtime.events.event_seq` |
| `call_id` | `text` | no |  | Potential local reference; resolve by domain context in: `runtime.workflow_agent_calls.call_id`. |
| `tool_name` | `text` | no |  |  |
| `server_name` | `text` | yes |  |  |
| `status` | `text` | no |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `arguments_json` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `tool_calls_event_seq_fkey`: `event_seq` → `runtime.events` (`event_seq`)
- PRIMARY KEY `tool_calls_pkey`: `tool_call_id`
- UNIQUE `tool_calls_call_id_key`: `call_id`
- UNIQUE `tool_calls_event_seq_key`: `event_seq`

### runtime.tool_outputs

来源：[runtime.tool_outputs](../../../opt/hatch/skills/muse_db/references/schema.md#L3248)。可见字段 7 个。

阅读重点：从 `status`, `error_text` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `tool_output_id` | `bigint` | no | `nextval('runtime.tool_outputs_tool_output_id_seq'::regclass)` | Local row identifier (primary key). |
| `event_seq` | `bigint` | no |  | FK → `runtime.events.event_seq` |
| `call_id` | `text` | no |  | Potential local reference; resolve by domain context in: `runtime.workflow_agent_calls.call_id`. |
| `status` | `text` | no |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `output_text` | `text` | yes |  |  |
| `error_text` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `tool_outputs_event_seq_fkey`: `event_seq` → `runtime.events` (`event_seq`)
- PRIMARY KEY `tool_outputs_pkey`: `tool_output_id`
- UNIQUE `tool_outputs_event_seq_key`: `event_seq`

### runtime.widgets

来源：[runtime.widgets](../../../opt/hatch/skills/muse_db/references/schema.md#L3266)。可见字段 9 个。

阅读重点：从 `state_bundle_json`, `state_version`, `state_updated_at_ms` 检查状态或失败信息；字段存在不说明允许哪些状态转换。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `widget_id` | `text` | no |  | Local row identifier (primary key). |
| `kind` | `text` | no |  |  |
| `data_json` | `text` | no |  |  |
| `display_text` | `text` | yes |  |  |
| `state_bundle_json` | `text` | no | `'{}'::text` |  |
| `state_version` | `bigint` | no | `0` |  |
| `state_updated_at_ms` | `bigint` | yes |  |  |
| `created_at_ms` | `bigint` | no |  |  |
| `updated_at_ms` | `bigint` | no |  |  |

键与约束：

- PRIMARY KEY `widgets_pkey`: `widget_id`

### runtime.work_items

来源：[runtime.work_items](../../../opt/hatch/skills/muse_db/references/schema.md#L3284)。可见字段 29 个。

阅读重点：从 `state` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 8 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `work_id` | `text` | no |  | Local row identifier (primary key). |
| `root_work_id` | `text` | yes |  | FK → `runtime.work_items.work_id` |
| `parent_work_id` | `text` | yes |  | FK → `runtime.work_items.work_id` |
| `request_id` | `text` | yes |  | FK → `runtime.requests.request_id` |
| `root_session_id` | `text` | yes |  | Soft local reference → `agent.sessions.session_id`. |
| `session_id` | `text` | yes |  | Soft local reference → `agent.sessions.session_id`. |
| `agent_id` | `text` | yes |  | Soft local reference → `agent.agents.agent_id`. |
| `root_message_id` | `text` | yes |  | Soft local reference → `runtime.messages.message_id`. |
| `stream_owner_message_id` | `text` | yes |  | Soft local reference → `runtime.messages.message_id`. |
| `source` | `text` | yes |  |  |
| `request_origin` | `text` | yes |  |  |
| `work_class` | `text` | no |  |  |
| `transcript_surface` | `text` | yes |  |  |
| `state` | `text` | no |  |  |
| `phase` | `text` | yes |  |  |
| `subphase` | `text` | yes |  |  |
| `priority` | `integer` | no | `0` |  |
| `preemptibility` | `text` | no |  |  |
| `deadline_at` | `timestamp with time zone` | yes |  |  |
| `heartbeat_at` | `timestamp with time zone` | no | `now()` |  |
| `lease_owner` | `text` | yes |  |  |
| `retry_policy_json` | `text` | yes |  |  |
| `metadata_json` | `text` | no | `'{}'::text` |  |
| `terminal_reason` | `text` | yes |  |  |
| `terminal_detail` | `text` | yes |  |  |
| `diagnostic_json` | `text` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |
| `terminalized_at` | `timestamp with time zone` | yes |  |  |

键与约束：

- FOREIGN KEY `work_items_parent_work_id_fkey`: `parent_work_id` → `runtime.work_items` (`work_id`)
- FOREIGN KEY `work_items_request_id_fkey`: `request_id` → `runtime.requests` (`request_id`)
- FOREIGN KEY `work_items_root_work_id_fkey`: `root_work_id` → `runtime.work_items` (`work_id`)
- PRIMARY KEY `work_items_pkey`: `work_id`

### runtime.workflow_agent_calls

来源：[runtime.workflow_agent_calls](../../../opt/hatch/skills/muse_db/references/schema.md#L3325)。可见字段 22 个。

阅读重点：从 `status`, `completed_at`, `error` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 5 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `call_id` | `text` | no |  | Local row identifier (primary key). |
| `run_id` | `text` | no |  | FK → `runtime.workflow_runs.run_id` |
| `phase_run_id` | `text` | yes |  | FK → `runtime.workflow_phase_runs.phase_run_id` |
| `replay_key` | `text` | no |  |  |
| `cache_key` | `text` | no |  |  |
| `call_ordinal` | `integer` | no |  |  |
| `prompt` | `text` | no |  |  |
| `options_json` | `jsonb` | no | `'{}'::jsonb` |  |
| `child_agent_id` | `text` | yes |  | Soft local reference → `agent.agents.agent_id`. |
| `status` | `text` | no |  |  |
| `cached_from_call_id` | `text` | yes |  | FK → `runtime.workflow_agent_calls.call_id` |
| `final_response` | `text` | yes |  |  |
| `input_tokens` | `bigint` | no | `0` |  |
| `output_tokens` | `bigint` | no | `0` |  |
| `tool_call_count` | `bigint` | no | `0` |  |
| `duration_ms` | `bigint` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `started_at` | `timestamp with time zone` | yes |  |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |
| `completed_at` | `timestamp with time zone` | yes |  |  |
| `error` | `text` | yes |  |  |
| `child_message_id` | `text` | yes |  | Soft local reference → `runtime.messages.message_id`. |

键与约束：

- FOREIGN KEY `workflow_agent_calls_cached_from_call_id_fkey`: `cached_from_call_id` → `runtime.workflow_agent_calls` (`call_id`)
- FOREIGN KEY `workflow_agent_calls_phase_run_id_fkey`: `phase_run_id` → `runtime.workflow_phase_runs` (`phase_run_id`)
- FOREIGN KEY `workflow_agent_calls_run_id_fkey`: `run_id` → `runtime.workflow_runs` (`run_id`)
- PRIMARY KEY `workflow_agent_calls_pkey`: `call_id`

### runtime.workflow_launch_occurrence_aliases

来源：[runtime.workflow_launch_occurrence_aliases](../../../opt/hatch/skills/muse_db/references/schema.md#L3359)。可见字段 6 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `launch_occurrence_agent_id` | `text` | no |  | Local row identifier (primary key). |
| `launch_occurrence_message_id` | `text` | no |  | Local row identifier (primary key). |
| `launch_occurrence_tool_call_id` | `text` | no |  | Local row identifier (primary key). |
| `run_id` | `text` | no |  | FK → `runtime.workflow_runs.run_id` |
| `contract_fingerprint` | `text` | no |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `workflow_launch_occurrence_aliases_run_id_fkey`: `run_id` → `runtime.workflow_runs` (`run_id`)
- PRIMARY KEY `workflow_launch_occurrence_aliases_pkey`: `launch_occurrence_agent_id`, `launch_occurrence_message_id`, `launch_occurrence_tool_call_id`

### runtime.workflow_legacy_launch_occurrence_blocks

来源：[runtime.workflow_legacy_launch_occurrence_blocks](../../../opt/hatch/skills/muse_db/references/schema.md#L3375)。可见字段 6 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `launch_occurrence_agent_id` | `text` | no |  | Local row identifier (primary key). |
| `launch_occurrence_message_id` | `text` | no |  | Local row identifier (primary key). |
| `launch_occurrence_tool_call_id` | `text` | no |  | Local row identifier (primary key). |
| `legacy_run_id` | `text` | no |  | FK → `runtime.workflow_runs.run_id` |
| `reason` | `text` | no |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `workflow_legacy_launch_occurrence_blocks_legacy_run_id_fkey`: `legacy_run_id` → `runtime.workflow_runs` (`run_id`)
- PRIMARY KEY `workflow_legacy_launch_occurrence_blocks_pkey`: `launch_occurrence_agent_id`, `launch_occurrence_message_id`, `launch_occurrence_tool_call_id`

### runtime.workflow_phase_runs

来源：[runtime.workflow_phase_runs](../../../opt/hatch/skills/muse_db/references/schema.md#L3391)。可见字段 13 个。

阅读重点：从 `status`, `agent_completed`, `completed_at`, `error` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `phase_run_id` | `text` | no |  | Local row identifier (primary key). |
| `run_id` | `text` | no |  | FK → `runtime.workflow_runs.run_id` |
| `phase_name` | `text` | no |  |  |
| `ordinal` | `integer` | no |  |  |
| `status` | `text` | no |  |  |
| `agent_total` | `integer` | no | `0` |  |
| `agent_completed` | `integer` | no | `0` |  |
| `input_tokens` | `bigint` | no | `0` |  |
| `output_tokens` | `bigint` | no | `0` |  |
| `started_at` | `timestamp with time zone` | yes |  |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |
| `completed_at` | `timestamp with time zone` | yes |  |  |
| `error` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `workflow_phase_runs_run_id_fkey`: `run_id` → `runtime.workflow_runs` (`run_id`)
- PRIMARY KEY `workflow_phase_runs_pkey`: `phase_run_id`
- UNIQUE `workflow_phase_runs_unique_phase`: `run_id`, `phase_name`, `ordinal`

### runtime.workflow_runs

来源：[runtime.workflow_runs](../../../opt/hatch/skills/muse_db/references/schema.md#L3415)。可见字段 47 个。

阅读重点：从 `execution_attempt`, `status`, `error`, `completed_at`, `terminal_handoff_delivered_at`, `terminal_handoff_attempt_count`, `terminal_handoff_last_attempt_at`, `terminal_handoff_next_attempt_at`, `terminal_handoff_last_error` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 11 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `run_id` | `text` | no |  | Local row identifier (primary key). |
| `root_agent_id` | `text` | no |  | Soft local reference → `agent.agents.agent_id`. |
| `parent_message_id` | `text` | yes |  | Soft local reference → `runtime.messages.message_id`. |
| `launching_agent_id` | `text` | yes |  | Soft local reference → `agent.agents.agent_id`. |
| `launching_message_id` | `text` | yes |  | Soft local reference → `runtime.messages.message_id`. |
| `launching_tool_call_id` | `text` | yes |  | Soft local reference → `runtime.tool_calls.tool_call_id`. |
| `task_id` | `text` | no |  | Potential local reference; resolve by domain context in: `runtime.browser_tasks.task_id`. |
| `resume_from_run_id` | `text` | yes |  | FK → `runtime.workflow_runs.run_id` |
| `workflow_name` | `text` | no |  |  |
| `description` | `text` | no | `''::text` |  |
| `phases_json` | `jsonb` | no | `'[]'::jsonb` |  |
| `args_json` | `jsonb` | yes |  |  |
| `workspace_root` | `text` | no |  |  |
| `script_path` | `text` | no |  |  |
| `script_sha256` | `text` | no |  |  |
| `request_trace_json` | `jsonb` | yes |  |  |
| `executor_id` | `text` | yes |  | Ephemeral workflow lease-owner identifier; no separate owner table. |
| `execution_attempt` | `integer` | no | `0` |  |
| `heartbeat_at` | `timestamp with time zone` | no | `now()` |  |
| `lease_expires_at` | `timestamp with time zone` | yes |  |  |
| `recovery_count` | `integer` | no | `0` |  |
| `last_recovery_reason` | `text` | yes |  |  |
| `last_recovered_at` | `timestamp with time zone` | yes |  |  |
| `status` | `text` | no |  |  |
| `error` | `text` | yes |  |  |
| `final_result` | `text` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `started_at` | `timestamp with time zone` | yes |  |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |
| `completed_at` | `timestamp with time zone` | yes |  |  |
| `launch_mode` | `text` | no | `'sync'::text` |  |
| `terminal_handoff_channel` | `text` | yes |  |  |
| `terminal_handoff_delivery_target` | `text` | yes |  |  |
| `terminal_handoff_channel_context_json` | `jsonb` | yes |  |  |
| `terminal_handoff_message_id` | `text` | yes |  | Soft local reference → `runtime.messages.message_id`. |
| `terminal_handoff_delivered_at` | `timestamp with time zone` | yes |  |  |
| `terminal_handoff_attempt_count` | `integer` | no | `0` |  |
| `terminal_handoff_last_attempt_at` | `timestamp with time zone` | yes |  |  |
| `terminal_handoff_next_attempt_at` | `timestamp with time zone` | yes |  |  |
| `terminal_handoff_last_error` | `text` | yes |  |  |
| `launch_occurrence_agent_id` | `text` | yes |  | Potential local reference; resolve by domain context in: `runtime.workflow_launch_occurrence_aliases.launch_occurrence_agent_id`, `runtime.workflow_legacy_launch_occurrence_blocks.launch_occurrence_agent_id`. |
| `launch_occurrence_message_id` | `text` | yes |  | Potential local reference; resolve by domain context in: `runtime.workflow_launch_occurrence_aliases.launch_occurrence_message_id`, `runtime.workflow_legacy_launch_occurrence_blocks.launch_occurrence_message_id`. |
| `launch_occurrence_tool_call_id` | `text` | yes |  | Potential local reference; resolve by domain context in: `runtime.workflow_launch_occurrence_aliases.launch_occurrence_tool_call_id`, `runtime.workflow_legacy_launch_occurrence_blocks.launch_occurrence_tool_call_id`. |
| `sync_wait_deadline_at` | `timestamp with time zone` | yes |  |  |
| `terminal_handoff_disposition` | `text` | yes |  |  |
| `terminal_handoff_generation` | `integer` | no | `0` |  |
| `magi_workload_class` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `workflow_runs_resume_from_run_id_fkey`: `resume_from_run_id` → `runtime.workflow_runs` (`run_id`)
- PRIMARY KEY `workflow_runs_pkey`: `run_id`
- UNIQUE `workflow_runs_task_unique`: `task_id`

### runtime.writer_epoch

来源：[runtime.writer_epoch](../../../opt/hatch/skills/muse_db/references/schema.md#L3473)。可见字段 3 个。

阅读重点：从 `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `singleton` | `boolean` | no | `true` | Local row identifier (primary key). |
| `rv_epoch` | `bigint` | no | `0` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `writer_epoch_pkey`: `singleton`

<a id="domain-scheduler"></a>
## scheduler

任务定义、发生实例、调度事件、恢复与交付；排队、成功执行和送达分别追踪。

### scheduler.cron_mutations

来源：[scheduler.cron_mutations](../../../opt/hatch/skills/muse_db/references/schema.md#L3487)。可见字段 9 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 5 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `mutation_seq` | `bigint` | no | `nextval('scheduler.cron_mutations_mutation_seq_seq'::regclass)` | Local row identifier (primary key). |
| `job_id` | `text` | no |  | Soft local reference → `scheduler.jobs.job_id`. |
| `action` | `text` | no |  |  |
| `occurred_at_ms` | `bigint` | no |  |  |
| `carrier_message_id` | `text` | no |  | Soft local reference → `runtime.messages.message_id`. |
| `request_id` | `text` | no |  | Soft local reference → `runtime.requests.request_id`. |
| `tool_call_id` | `text` | no |  | Soft local reference → `runtime.tool_calls.tool_call_id`. |
| `input_message_ids` | `text[]` | no |  | Soft local reference → `runtime.messages.message_id`. |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `cron_mutations_pkey`: `mutation_seq`
- UNIQUE `cron_mutations_request_id_tool_call_id_job_id_key`: `request_id`, `tool_call_id`, `job_id`

### scheduler.delivery_outbox

来源：[scheduler.delivery_outbox](../../../opt/hatch/skills/muse_db/references/schema.md#L3506)。可见字段 12 个。

阅读重点：从 `state`, `attempt_count`, `next_attempt_at_utc`, `last_error`, `delivered_at_utc` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `delivery_key` | `text` | no |  | Local row identifier (primary key). |
| `job_id` | `text` | no |  | Soft local reference → `scheduler.jobs.job_id`. |
| `run_id` | `text` | no |  | Potential local reference; resolve by domain context in: `scheduler.doctor_run_plans.run_id`, `scheduler.job_runs.run_id`, `scheduler.terminal_signals.run_id`. |
| `payload_json` | `text` | no |  |  |
| `state` | `text` | no |  |  |
| `dispatch_boot_generation` | `text` | yes |  |  |
| `attempt_count` | `integer` | no | `0` |  |
| `next_attempt_at_utc` | `bigint` | no |  |  |
| `last_error` | `text` | yes |  |  |
| `created_at_utc` | `bigint` | no |  |  |
| `updated_at_utc` | `bigint` | no |  |  |
| `delivered_at_utc` | `bigint` | yes |  |  |

键与约束：

- PRIMARY KEY `delivery_outbox_pkey`: `delivery_key`

### scheduler.doctor_run_plans

来源：[scheduler.doctor_run_plans](../../../opt/hatch/skills/muse_db/references/schema.md#L3527)。可见字段 3 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `run_id` | `text` | no |  | FK → `scheduler.job_runs.run_id` |
| `tasks_json` | `jsonb` | no |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `doctor_run_plans_run_id_fkey`: `run_id` → `scheduler.job_runs` (`run_id`)
- PRIMARY KEY `doctor_run_plans_pkey`: `run_id`

### scheduler.doctor_task_state

来源：[scheduler.doctor_task_state](../../../opt/hatch/skills/muse_db/references/schema.md#L3540)。可见字段 5 个。

阅读重点：从 `last_success_scheduled_for_utc`, `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `task_name` | `text` | no |  | Local row identifier (primary key). |
| `evidence_hash` | `text` | no |  |  |
| `last_success_run_id` | `text` | no |  | Soft local reference to `scheduler.job_runs.run_id`. |
| `last_success_scheduled_for_utc` | `bigint` | no |  |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `doctor_task_state_pkey`: `task_name`

### scheduler.events

来源：[scheduler.events](../../../opt/hatch/skills/muse_db/references/schema.md#L3554)。可见字段 6 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `scheduler_event_id` | `bigint` | no | `nextval('scheduler.events_scheduler_event_id_seq'::regclass)` | Local row identifier (primary key). |
| `job_id` | `text` | yes |  | Soft local reference → `scheduler.jobs.job_id`. |
| `run_id` | `text` | yes |  | Potential local reference; resolve by domain context in: `scheduler.doctor_run_plans.run_id`, `scheduler.job_runs.run_id`, `scheduler.terminal_signals.run_id`. |
| `event_name` | `text` | no |  |  |
| `detail` | `text` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `events_pkey`: `scheduler_event_id`

### scheduler.job_definitions

来源：[scheduler.job_definitions](../../../opt/hatch/skills/muse_db/references/schema.md#L3569)。可见字段 7 个。

阅读重点：从 `created_at`, `retired_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `job_definition_id` | `bigint` | no | `nextval('scheduler.job_definitions_job_definition_id_seq'::regclass)` | Local row identifier (primary key). |
| `job_id` | `text` | no |  | FK → `scheduler.jobs.job_id` |
| `version` | `integer` | no |  |  |
| `prompt_template_id` | `bigint` | yes |  | Prompt-template identifier; no queryable owner table. |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `retired_at` | `timestamp with time zone` | yes |  |  |
| `task_text` | `text` | no |  |  |

键与约束：

- FOREIGN KEY `job_definitions_job_id_fkey`: `job_id` → `scheduler.jobs` (`job_id`)
- PRIMARY KEY `job_definitions_pkey`: `job_definition_id`
- UNIQUE `job_definitions_job_id_version_key`: `job_id`, `version`

### scheduler.job_idea_scope

来源：[scheduler.job_idea_scope](../../../opt/hatch/skills/muse_db/references/schema.md#L3587)。可见字段 4 个。

阅读重点：从 `created_at`, `updated_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `job_id` | `text` | no |  | FK → `scheduler.jobs.job_id` |
| `idea_provenance_json` | `text` | no |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- FOREIGN KEY `job_idea_scope_job_id_fkey`: `job_id` → `scheduler.jobs` (`job_id`)
- PRIMARY KEY `job_idea_scope_pkey`: `job_id`

### scheduler.job_runs

来源：[scheduler.job_runs](../../../opt/hatch/skills/muse_db/references/schema.md#L3601)。可见字段 27 个。

阅读重点：从 `status`, `error_text`, `attempt`, `worker_phase_attempt` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 6 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `run_id` | `text` | no |  | Local row identifier (primary key). |
| `job_id` | `text` | no |  | FK → `scheduler.jobs.job_id` |
| `job_definition_id` | `bigint` | yes |  | FK → `scheduler.job_definitions.job_definition_id` |
| `request_id` | `text` | yes |  | FK → `runtime.requests.request_id` |
| `scheduled_for` | `timestamp with time zone` | no |  |  |
| `scheduled_for_utc` | `bigint` | no |  |  |
| `trigger_reason` | `text` | yes |  |  |
| `started_at` | `timestamp with time zone` | yes |  |  |
| `started_at_utc` | `bigint` | yes |  |  |
| `finished_at` | `timestamp with time zone` | yes |  |  |
| `finished_at_utc` | `bigint` | yes |  |  |
| `status` | `scheduler.run_status` | no |  |  |
| `result_summary` | `text` | yes |  |  |
| `error_text` | `text` | yes |  |  |
| `attempt` | `integer` | no | `1` |  |
| `worker_phase` | `text` | yes |  |  |
| `worker_phase_attempt` | `integer` | yes |  |  |
| `worker_agent_id` | `text` | yes |  | Soft local reference → `agent.agents.agent_id`. |
| `worker_boot_generation` | `text` | yes |  |  |
| `worker_claimed_at_utc` | `bigint` | yes |  |  |
| `worker_execution_timed_out` | `boolean` | no | `false` |  |
| `worker_history_agent_id` | `text` | yes |  | Soft local reference → `agent.agents.agent_id`. |
| `product_endpoint_deadline_at_ms` | `bigint` | yes |  |  |
| `presentation_locale` | `text` | no | `'en-US'::text` | Immutable locale for user-visible output authored by this run; not a user, session, or device preference. |
| `onboarding_tour_body` | `text` | yes |  |  |
| `pending_terminal_result_json` | `text` | yes |  |  |
| `worker_approval_wait_json` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `job_runs_job_definition_id_fkey`: `job_definition_id` → `scheduler.job_definitions` (`job_definition_id`)
- FOREIGN KEY `job_runs_job_id_fkey`: `job_id` → `scheduler.jobs` (`job_id`)
- FOREIGN KEY `job_runs_request_id_fkey`: `request_id` → `runtime.requests` (`request_id`)
- PRIMARY KEY `job_runs_pkey`: `run_id`
- UNIQUE `job_runs_job_id_scheduled_for_utc_key`: `job_id`, `scheduled_for_utc`

### scheduler.jobs

来源：[scheduler.jobs](../../../opt/hatch/skills/muse_db/references/schema.md#L3641)。可见字段 24 个。

阅读重点：从 `last_status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `job_id` | `text` | no |  | Local row identifier (primary key). |
| `is_heartbeat` | `boolean` | no | `false` |  |
| `source_path` | `text` | yes |  |  |
| `source_hash` | `text` | yes |  |  |
| `schedule_kind` | `text` | no |  |  |
| `enabled` | `boolean` | no | `true` |  |
| `schedule_expr` | `text` | no |  |  |
| `timezone` | `text` | no | `'UTC'::text` |  |
| `retry_on_failure` | `boolean` | no | `false` |  |
| `max_retries` | `integer` | no | `0` |  |
| `delivery_targets_json` | `text` | no | `'[]'::text` |  |
| `next_run_at` | `timestamp with time zone` | yes |  |  |
| `next_run_at_utc` | `bigint` | no | `0` |  |
| `last_run_at_utc` | `bigint` | yes |  |  |
| `last_success_at_utc` | `bigint` | yes |  |  |
| `last_status` | `text` | yes |  |  |
| `consecutive_failures` | `bigint` | no | `0` |  |
| `updated_at_utc` | `bigint` | no | `0` |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |
| `blocked_reason` | `text` | yes |  |  |
| `blocked_dependency` | `text` | yes |  |  |
| `blocked_at_utc` | `bigint` | yes |  |  |
| `next_blocked_probe_at_utc` | `bigint` | yes |  |  |

键与约束：

- PRIMARY KEY `jobs_pkey`: `job_id`

### scheduler.scheduled_resume_registrations

来源：[scheduler.scheduled_resume_registrations](../../../opt/hatch/skills/muse_db/references/schema.md#L3674)。可见字段 10 个。

阅读重点：从 `acknowledgement_attempts`, `registration_attempts`, `acknowledgement_next_attempt_at_ms` 检查状态或失败信息；字段存在不说明允许哪些状态转换。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `resume_at_utc` | `bigint` | no |  | Local row identifier (primary key). |
| `schedule_id` | `text` | yes |  | Host scheduler registration identifier; no Muse PostgreSQL owner table. |
| `dispatch_at_ms` | `bigint` | yes |  |  |
| `acknowledgement_attempts` | `integer` | no | `0` |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `job_name` | `text` | yes |  |  |
| `shadow` | `boolean` | no | `false` |  |
| `registration_attempts` | `integer` | no | `0` |  |
| `acknowledgement_next_attempt_at_ms` | `bigint` | no | `0` |  |
| `environment_id` | `text` | yes |  | Opaque correlation identifier; no declared local table relationship. |

键与约束：

- PRIMARY KEY `scheduled_resume_registrations_pkey`: `resume_at_utc`

### scheduler.scheduled_resume_state

来源：[scheduler.scheduled_resume_state](../../../opt/hatch/skills/muse_db/references/schema.md#L3693)。可见字段 7 个。

阅读重点：从 `next_resume_at_utc`, `registration_resume_at_utc` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `singleton` | `boolean` | no | `true` | Local row identifier (primary key). |
| `next_resume_at_utc` | `bigint` | yes |  |  |
| `registered_dispatch_at_ms` | `bigint` | yes |  |  |
| `projection_complete` | `boolean` | no | `true` |  |
| `registration_resume_at_utc` | `bigint` | yes |  |  |
| `registered_schedule_id` | `text` | yes |  | Host scheduler registration identifier mirrored from `scheduler.scheduled_resume_registrations.schedule_id`. |
| `next_resume_job_name` | `text` | yes |  |  |

键与约束：

- PRIMARY KEY `scheduled_resume_state_pkey`: `singleton`

### scheduler.terminal_signals

来源：[scheduler.terminal_signals](../../../opt/hatch/skills/muse_db/references/schema.md#L3709)。可见字段 11 个。

阅读重点：从 `producer_phase_attempt` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `run_id` | `text` | no |  | Local row identifier (primary key). |
| `signal_type` | `text` | no |  |  |
| `message` | `text` | yes |  |  |
| `producer_request_trace_json` | `text` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `created_at_utc` | `bigint` | no | `0` |  |
| `producer_agent_id` | `text` | yes |  | Soft local reference → `agent.agents.agent_id`. |
| `producer_phase_attempt` | `integer` | yes |  |  |
| `producer_boot_generation` | `text` | yes |  |  |
| `blocked_reason` | `text` | yes |  |  |
| `blocked_dependency` | `text` | yes |  |  |

键与约束：

- PRIMARY KEY `terminal_signals_pkey`: `run_id`

<a id="domain-self_improvement"></a>
## self_improvement

后台学习、目标研究、关系整理、反馈与交接记录；证据链与最终建议内容分离。

### self_improvement.backfill_day_runs

来源：[self_improvement.backfill_day_runs](../../../opt/hatch/skills/muse_db/references/schema.md#L3731)。可见字段 12 个。

阅读重点：从 `status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 3 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `backfill_day_run_id` | `text` | no |  | Local row identifier (primary key). |
| `objective_id` | `text` | no |  | Potential local reference; resolve by domain context in: `self_improvement.handoff_dedupe.objective_id`, `self_improvement.objective_markers.objective_id`, `self_improvement.objective_state.objective_id`. |
| `day` | `date` | no |  |  |
| `run_id` | `text` | no |  | Potential local reference; resolve by domain context in: `self_improvement.runs.run_id`. |
| `request_id` | `text` | no |  | Soft local reference → `runtime.requests.request_id`. |
| `replay_hash` | `text` | no |  |  |
| `status` | `text` | no | `'pending'::text` |  |
| `diagnostics` | `jsonb` | no | `'{}'::jsonb` |  |
| `started_at` | `timestamp with time zone` | yes |  |  |
| `finished_at` | `timestamp with time zone` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `backfill_day_runs_pkey`: `backfill_day_run_id`

### self_improvement.calculation_records

来源：[self_improvement.calculation_records](../../../opt/hatch/skills/muse_db/references/schema.md#L3752)。可见字段 10 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `replay_id` | `text` | no |  | Local row identifier (primary key). |
| `card_id` | `text` | no |  | Code-defined self-improvement measurement card key; no owner table. |
| `objective_id` | `text` | no |  | Potential local reference; resolve by domain context in: `self_improvement.handoff_dedupe.objective_id`, `self_improvement.objective_markers.objective_id`, `self_improvement.objective_state.objective_id`. |
| `config_hash` | `text` | no |  |  |
| `code_version` | `text` | no |  |  |
| `source_handles` | `jsonb` | no | `'[]'::jsonb` |  |
| `normalized_inputs` | `jsonb` | no | `'{}'::jsonb` |  |
| `formulas` | `jsonb` | no | `'{}'::jsonb` |  |
| `outputs` | `jsonb` | no | `'{}'::jsonb` |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `calculation_records_pkey`: `replay_id`

### self_improvement.calibration_records

来源：[self_improvement.calibration_records](../../../opt/hatch/skills/muse_db/references/schema.md#L3771)。可见字段 10 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `calibration_id` | `text` | no |  | Local row identifier (primary key). |
| `card_id` | `text` | no |  | Code-defined self-improvement measurement card key; no owner table. |
| `objective_id` | `text` | no |  | Potential local reference; resolve by domain context in: `self_improvement.handoff_dedupe.objective_id`, `self_improvement.objective_markers.objective_id`, `self_improvement.objective_state.objective_id`. |
| `change_id` | `text` | no |  | Measured change identifier supplied by the objective; no owner table. |
| `classification` | `text` | no |  |  |
| `window_start` | `timestamp with time zone` | yes |  |  |
| `window_end` | `timestamp with time zone` | yes |  |  |
| `source_handles` | `jsonb` | no | `'[]'::jsonb` |  |
| `diagnostics` | `jsonb` | no | `'{}'::jsonb` |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `calibration_records_pkey`: `calibration_id`

### self_improvement.connector_read_audit

来源：[self_improvement.connector_read_audit](../../../opt/hatch/skills/muse_db/references/schema.md#L3790)。可见字段 11 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `audit_id` | `bigint` | no | `nextval('self_improvement.connector_read_audit_audit_id_seq'::regclass)` | Local row identifier (primary key). |
| `connector_id` | `text` | yes |  | Connector identity owned by authd; no Muse PostgreSQL owner table. |
| `device_node_id` | `text` | yes |  | Soft local reference → `device.nodes.node_id`. |
| `method_key` | `text` | no |  |  |
| `purpose` | `text` | no |  |  |
| `request_id` | `text` | no |  | Soft local reference → `runtime.requests.request_id`. |
| `request_origin` | `text` | no |  |  |
| `sensitivity` | `text` | no |  |  |
| `source_handle` | `text` | yes |  |  |
| `metadata` | `jsonb` | no | `'{}'::jsonb` |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `connector_read_audit_pkey`: `audit_id`

### self_improvement.conversation_follow_up_attempts

来源：[self_improvement.conversation_follow_up_attempts](../../../opt/hatch/skills/muse_db/references/schema.md#L3810)。可见字段 14 个。

阅读重点：从 `state` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `occurrence` | `text` | no |  | Local row identifier (primary key). |
| `delivery_submission_id` | `text` | no |  | Soft local reference → `agent.message_mailbox.submission_id`. |
| `selector_decision` | `text` | yes |  |  |
| `selector_message` | `text` | yes |  |  |
| `feedback_note` | `text` | yes |  |  |
| `selected_at` | `timestamp with time zone` | yes |  |  |
| `state` | `text` | no | `'pending'::text` |  |
| `disposition_reason` | `text` | yes |  |  |
| `surfaced_at` | `timestamp with time zone` | yes |  |  |
| `terminal_at` | `timestamp with time zone` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |
| `source_root_agent_id` | `text` | yes |  | Soft local reference → `agent.agents.agent_id`. |
| `selector_priority` | `smallint` | yes |  |  |

键与约束：

- PRIMARY KEY `conversation_follow_up_attempts_pkey`: `occurrence`

### self_improvement.handoff_dedupe

来源：[self_improvement.handoff_dedupe](../../../opt/hatch/skills/muse_db/references/schema.md#L3833)。可见字段 4 个。

阅读重点：从 `emitted_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `objective_id` | `text` | no |  | Local row identifier (primary key). |
| `content_hash` | `text` | no |  | Local row identifier (primary key). |
| `run_id` | `text` | no |  | Potential local reference; resolve by domain context in: `self_improvement.runs.run_id`. |
| `emitted_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `handoff_dedupe_pkey`: `objective_id`, `content_hash`

### self_improvement.learning_adoption_events

来源：[self_improvement.learning_adoption_events](../../../opt/hatch/skills/muse_db/references/schema.md#L3846)。可见字段 7 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `id` | `bigint` | no |  | Local row identifier (primary key). |
| `learning_id` | `text` | no |  | Learning identifier; no queryable owner table. |
| `objective_id` | `text` | no |  | Potential local reference; resolve by domain context in: `self_improvement.handoff_dedupe.objective_id`, `self_improvement.objective_markers.objective_id`, `self_improvement.objective_state.objective_id`. |
| `run_id` | `text` | no |  | Potential local reference; resolve by domain context in: `self_improvement.runs.run_id`. |
| `outcome` | `text` | no |  |  |
| `detail` | `jsonb` | no | `'{}'::jsonb` |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `learning_adoption_events_pkey`: `id`

### self_improvement.leases

来源：[self_improvement.leases](../../../opt/hatch/skills/muse_db/references/schema.md#L3862)。可见字段 8 个。

阅读重点：从 `acquired_at`, `expires_at`, `heartbeat_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `lease_key` | `text` | no |  | Local row identifier (primary key). |
| `owner` | `text` | no |  |  |
| `objective_id` | `text` | yes |  | Potential local reference; resolve by domain context in: `self_improvement.handoff_dedupe.objective_id`, `self_improvement.objective_markers.objective_id`, `self_improvement.objective_state.objective_id`. |
| `run_id` | `text` | yes |  | FK → `self_improvement.runs.run_id` |
| `acquired_at` | `timestamp with time zone` | no | `now()` |  |
| `expires_at` | `timestamp with time zone` | no |  |  |
| `heartbeat_at` | `timestamp with time zone` | no | `now()` |  |
| `metadata` | `jsonb` | no | `'{}'::jsonb` |  |

键与约束：

- FOREIGN KEY `leases_run_id_fkey`: `run_id` → `self_improvement.runs` (`run_id`)
- PRIMARY KEY `leases_pkey`: `lease_key`

### self_improvement.objective_markers

来源：[self_improvement.objective_markers](../../../opt/hatch/skills/muse_db/references/schema.md#L3880)。可见字段 3 个。

阅读重点：从 `set_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `objective_id` | `text` | no |  | Local row identifier (primary key). |
| `marker` | `text` | no |  | Local row identifier (primary key). |
| `set_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `objective_markers_pkey`: `objective_id`, `marker`

### self_improvement.objective_state

来源：[self_improvement.objective_state](../../../opt/hatch/skills/muse_db/references/schema.md#L3892)。可见字段 7 个。

阅读重点：从 `status`, `state_json` 检查状态或失败信息；字段存在不说明允许哪些状态转换。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `objective_id` | `text` | no |  | Local row identifier (primary key). |
| `current_file_hash` | `text` | yes |  |  |
| `projection_hash` | `text` | yes |  |  |
| `status` | `text` | no |  |  |
| `last_run_utc` | `timestamp with time zone` | yes |  |  |
| `state_json` | `jsonb` | no | `'{}'::jsonb` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `objective_state_pkey`: `objective_id`

### self_improvement.relationship_briefs

来源：[self_improvement.relationship_briefs](../../../opt/hatch/skills/muse_db/references/schema.md#L3908)。可见字段 7 个。

阅读重点：从 `created_at`, `last_opened_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `brief_id` | `text` | no |  | Local row identifier (primary key). |
| `title` | `text` | no |  |  |
| `body_html` | `text` | no |  |  |
| `anchored_idea_ids` | `jsonb` | no | `'[]'::jsonb` | Soft local reference → `ideas.ideas.idea_id`. |
| `request_id` | `text` | no |  | Soft local reference → `runtime.requests.request_id`. |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `last_opened_at` | `timestamp with time zone` | yes |  |  |

键与约束：

- PRIMARY KEY `relationship_briefs_pkey`: `brief_id`

### self_improvement.runs

来源：[self_improvement.runs](../../../opt/hatch/skills/muse_db/references/schema.md#L3924)。可见字段 18 个。

阅读重点：从 `state` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 2 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `run_id` | `text` | no |  | Local row identifier (primary key). |
| `objective_id` | `text` | no |  | Potential local reference; resolve by domain context in: `self_improvement.handoff_dedupe.objective_id`, `self_improvement.objective_markers.objective_id`, `self_improvement.objective_state.objective_id`. |
| `state` | `text` | no |  |  |
| `request_id` | `text` | no |  | Soft local reference → `runtime.requests.request_id`. |
| `request_origin` | `text` | no |  |  |
| `phase` | `text` | yes |  |  |
| `subphase` | `text` | yes |  |  |
| `diagnostics` | `jsonb` | no | `'{}'::jsonb` |  |
| `queued_at` | `timestamp with time zone` | no | `now()` |  |
| `started_at` | `timestamp with time zone` | yes |  |  |
| `finished_at` | `timestamp with time zone` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |
| `run_clock` | `timestamp with time zone` | no |  |  |
| `available_at` | `timestamp with time zone` | no | `now()` |  |
| `recovery_phase_version` | `integer` | yes |  |  |
| `recovery_admitted_at` | `timestamp with time zone` | yes |  |  |
| `recovery_admission_boot_id` | `text` | yes |  | Daemon boot-generation identifier; no Muse PostgreSQL owner table. |

键与约束：

- PRIMARY KEY `runs_pkey`: `run_id`

<a id="domain-shell"></a>
## shell

用户壳层状态；按 source 与 item key 解读，不视为任意文件系统镜像。

### shell.user_state

来源：[shell.user_state](../../../opt/hatch/skills/muse_db/references/schema.md#L3953)。可见字段 10 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `source` | `text` | no |  | Local row identifier (primary key). |
| `item_key` | `text` | no |  | Local row identifier (primary key). |
| `is_favorite` | `boolean` | no | `false` |  |
| `accessed_at_ms` | `bigint` | yes |  |  |
| `frequency_score` | `double precision` | yes |  |  |
| `favorite_order` | `double precision` | yes |  |  |
| `display_name` | `text` | yes |  |  |
| `icon` | `text` | yes |  |  |
| `updated_at_ms` | `bigint` | no | `((EXTRACT(epoch FROM now()) * (1000)::numeric))::bigint` |  |
| `last_opened_at_ms` | `bigint` | yes |  |  |

键与约束：

- PRIMARY KEY `user_state_pkey`: `source`, `item_key`

<a id="domain-spaces"></a>
## spaces

应用/产物身份、动作、提案和分享等主库元数据；不包含每产物 app.db 的内部业务表。

### spaces.action_arguments

来源：[spaces.action_arguments](../../../opt/hatch/skills/muse_db/references/schema.md#L3974)。可见字段 5 个。

阅读重点：按主键与字段定位具体对象；不从单行存在推断关联流程已完成。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `action_argument_id` | `bigint` | no | `nextval('spaces.action_arguments_action_argument_id_seq'::regclass)` | Local row identifier (primary key). |
| `invocation_id` | `text` | no |  | FK → `spaces.action_invocations.invocation_id` |
| `argument_name` | `text` | no |  |  |
| `scalar_value` | `text` | yes |  |  |
| `text_content` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `action_arguments_invocation_id_fkey`: `invocation_id` → `spaces.action_invocations` (`invocation_id`)
- PRIMARY KEY `action_arguments_pkey`: `action_argument_id`
- UNIQUE `action_arguments_invocation_id_argument_name_key`: `invocation_id`, `argument_name`

### spaces.action_invocations

来源：[spaces.action_invocations](../../../opt/hatch/skills/muse_db/references/schema.md#L3990)。可见字段 23 个。

阅读重点：从 `status`, `error` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `global_seq` | `bigint` | no | `nextval('spaces.action_invocations_global_seq_seq'::regclass)` |  |
| `invocation_id` | `text` | no |  | Local row identifier (primary key). |
| `space_slug` | `text` | no |  |  |
| `space_display_name` | `text` | yes |  |  |
| `action` | `text` | no |  |  |
| `transport` | `text` | no | `'unknown'::text` |  |
| `request_id` | `text` | yes |  | FK → `runtime.requests.request_id` |
| `status` | `text` | no |  |  |
| `invoked_at_text` | `text` | yes |  |  |
| `invoked_at_unix_ms` | `bigint` | no | `0` |  |
| `invoked_at` | `timestamp with time zone` | no |  |  |
| `settled_at_text` | `text` | yes |  |  |
| `settled_at_unix_ms` | `bigint` | yes |  |  |
| `duration_ms` | `bigint` | yes |  |  |
| `args_preview` | `text` | yes |  |  |
| `result_preview` | `text` | yes |  |  |
| `error` | `text` | yes |  |  |
| `stream_protocol_messages` | `bigint` | yes |  |  |
| `stream_data_messages` | `bigint` | yes |  |  |
| `finished_at` | `timestamp with time zone` | yes |  |  |
| `source_kind` | `text` | yes |  |  |
| `source_ref` | `text` | yes |  |  |
| `trigger_ref` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `action_invocations_request_id_fkey`: `request_id` → `runtime.requests` (`request_id`)
- PRIMARY KEY `action_invocations_pkey`: `invocation_id`
- UNIQUE `action_invocations_global_seq_key`: `global_seq`

### spaces.action_results

来源：[spaces.action_results](../../../opt/hatch/skills/muse_db/references/schema.md#L4024)。可见字段 3 个。

阅读重点：从 `error_text` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `invocation_id` | `text` | no |  | FK → `spaces.action_invocations.invocation_id` |
| `result_text` | `text` | yes |  |  |
| `error_text` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `action_results_invocation_id_fkey`: `invocation_id` → `spaces.action_invocations` (`invocation_id`)
- PRIMARY KEY `action_results_pkey`: `invocation_id`

### spaces.backfill_markers

来源：[spaces.backfill_markers](../../../opt/hatch/skills/muse_db/references/schema.md#L4037)。可见字段 2 个。

阅读重点：从 `completed_at` 检查状态或失败信息；字段存在不说明允许哪些状态转换。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `marker` | `text` | no |  | Local row identifier (primary key). |
| `completed_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `backfill_markers_pkey`: `marker`

### spaces.file_artifact_identities

来源：[spaces.file_artifact_identities](../../../opt/hatch/skills/muse_db/references/schema.md#L4048)。可见字段 3 个。

阅读重点：从 `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `slug` | `text` | no |  | Local row identifier (primary key). |
| `artifact_id` | `uuid` | no | `gen_random_uuid()` | Stable local artifact identifier owned by this row; `slug` is the primary key. |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `file_artifact_identities_pkey`: `slug`

### spaces.proposals

来源：[spaces.proposals](../../../opt/hatch/skills/muse_db/references/schema.md#L4060)。可见字段 9 个。

阅读重点：从 `confirmed_at`, `created_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `proposal_id` | `text` | no |  | Local row identifier (primary key). |
| `root_session_id` | `text` | no |  | Soft local reference → `agent.sessions.session_id`. |
| `space_slug` | `text` | no |  |  |
| `proposed_name` | `text` | no |  |  |
| `params_json` | `text` | no |  |  |
| `confirmed_at_text` | `text` | yes |  |  |
| `confirmed_at` | `timestamp with time zone` | yes |  |  |
| `created_at_text` | `text` | no |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |

键与约束：

- PRIMARY KEY `proposals_pkey`: `proposal_id`

### spaces.shares

来源：[spaces.shares](../../../opt/hatch/skills/muse_db/references/schema.md#L4078)。可见字段 12 个。

阅读重点：从 `cloudflare_deploy_status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 1 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `space_slug` | `text` | no |  | FK → `spaces.spaces.space_slug` |
| `share_type` | `text` | no |  |  |
| `shortcode` | `text` | no |  |  |
| `is_active` | `boolean` | no | `true` |  |
| `share_id` | `text` | yes |  | Artifact-publishing service share identifier; no local owner table. |
| `cloudflare_deploy_status` | `text` | yes |  |  |
| `cloudflare_public_url` | `text` | yes |  |  |
| `cloudflare_actions_url` | `text` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |
| `cloudflare_storage_mode` | `text` | no | `'d1_r2'::text` |  |
| `published_manifest_sha256` | `text` | yes |  |  |

键与约束：

- FOREIGN KEY `shares_space_slug_fkey`: `space_slug` → `spaces.spaces` (`space_slug`)
- PRIMARY KEY `shares_pkey`: `space_slug`
- UNIQUE `shares_shortcode_key`: `shortcode`

### spaces.spaces

来源：[spaces.spaces](../../../opt/hatch/skills/muse_db/references/schema.md#L4101)。可见字段 32 个。

阅读重点：从 `construction_status` 检查状态或失败信息；字段存在不说明允许哪些状态转换。 有 3 个字段带关联提示，须按下表目标解析。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `space_slug` | `text` | no |  | Local row identifier (primary key). |
| `display_name` | `text` | no |  |  |
| `space_root_path` | `text` | yes |  |  |
| `db_path` | `text` | yes |  |  |
| `force_order` | `bigint` | yes |  |  |
| `session_id` | `text` | yes |  | Soft local reference → `agent.sessions.session_id`. |
| `construction_status` | `text` | yes |  |  |
| `construction_updated_at_text` | `text` | yes |  |  |
| `created_at_text` | `text` | yes |  |  |
| `updated_at_text` | `text` | yes |  |  |
| `created_at` | `timestamp with time zone` | no | `now()` |  |
| `updated_at` | `timestamp with time zone` | no | `now()` |  |
| `archived_at` | `timestamp with time zone` | yes |  |  |
| `current_build_id` | `text` | yes |  | Current artifact-build correlation id stored on this artifact row; the build workspace is on disk and has no separate PostgreSQL owner table. |
| `created_from_proposal_id` | `text` | yes |  | Soft local reference → `spaces.proposals.proposal_id`. |
| `space_id` | `uuid` | no | `gen_random_uuid()` | Soft local reference → `spaces.spaces.space_id`. |
| `source` | `text` | no | `'local'::text` |  |
| `shortcode` | `text` | yes |  |  |
| `source_url` | `text` | yes |  |  |
| `has_server_actions` | `boolean` | no | `true` |  |
| `cloudflare_share_manifest_sha256` | `text` | yes |  |  |
| `content_share_allowed` | `boolean` | yes |  |  |
| `content_share_review_sha256` | `text` | yes |  |  |
| `declared_capabilities_json` | `jsonb` | no | `'{"connectors": [], "schema_version": 1, "public_web_read": false}'::jsonb` |  |
| `capability_manifest_revision` | `bigint` | no | `0` |  |
| `builder_provenance_pending_build_id` | `text` | yes |  | Opaque correlation identifier; no declared local table relationship. Current build id whose builder provenance capture has not completed. |
| `builder_provenance_lost_build_id` | `text` | yes |  | Opaque correlation identifier; no declared local table relationship. Successful served build id whose builder provenance was lost; retained across later edit attempts until a newer build records evidence. |
| `builder_provenance_build_id` | `text` | yes |  | Opaque correlation identifier; no declared local table relationship. Build id whose bounded builder tool-evidence projection is stored on this row. |
| `builder_provenance_evidence_jsonl` | `text` | yes |  | Daemon-owned bounded JSONL of provenance-capable builder tool calls and outputs. |
| `share_disclosure_review` | `jsonb` | yes |  |  |
| `is_promoted` | `boolean` | no | `false` | UI placement: false means Library; true means Spaces in the sidebar. Independent of runtime kind and pinning. |
| `artifact_audit_review` | `jsonb` | yes |  | Runtime-owned artifact review record for the current build: bounded recent public chat turns that authorize the artifact, reviewed-coverage identities, and retained critic verdicts. |

键与约束：

- PRIMARY KEY `spaces_pkey`: `space_slug`

### spaces.user_state

来源：[spaces.user_state](../../../opt/hatch/skills/muse_db/references/schema.md#L4142)。可见字段 8 个。

阅读重点：从 `last_accessed_at`, `pinned_at` 区分写入时间与业务事件时间；不能用更新时间替代送达证明。

| 字段 | 类型 | 可空 | 默认 | 标识或关联契约 |
|---|---|---|---|---|
| `space_slug` | `text` | no |  | Local row identifier (primary key). |
| `is_favorite` | `boolean` | no | `false` |  |
| `accessed_at_ms` | `bigint` | yes |  |  |
| `frequency_score` | `double precision` | yes |  |  |
| `favorite_order` | `double precision` | yes |  |  |
| `last_accessed_at` | `timestamp with time zone` | yes |  |  |
| `pinned_at` | `timestamp with time zone` | yes |  |  |
| `last_opened_at_ms` | `bigint` | yes |  |  |

键与约束：

- PRIMARY KEY `user_state_pkey`: `space_slug`
