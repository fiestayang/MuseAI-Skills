# 证据、推断与未知项

[返回目录](../README.md) · [实际验证](../09-validation.md)

## 基线与范围

本报告以 Git 提交 `61121abf5c4da12fe32ef970a861108b16a0731b` 和本地实际文件为分析对象。上游地址是 [win4r/MuseAI-Skills](https://github.com/win4r/MuseAI-Skills)，本地 [README](../../../README.md) 解释其快照性质。报告不认证仓库是产品官方完整源码，也不认证文档里的发布日期、模型名和区域状态。

源码引用的行号绑定该基线；新提交改变文件时应重新核对。新增报告没有回写原 SKILL、manifest、程序或历史分析。机器可读覆盖信息在 [source-inventory.json](source-inventory.json)，逐项入口在[覆盖表](file-coverage.md)。

## 关键结论对照

| 结论 | 证据类别与来源 | 允许的判断 | 保留的未知 |
|---|---|---|---|
| 68 个独立技能、4 个别名 | 文件与 symlink 盘点，[技能目录](../skills/README.md) | 当前目录的独立入口数量 | 线上动态或用户自建技能总数 |
| 31 个 available 条目 | [skills.yaml](../../../home/hatch/config/skills.yaml) | 配置声明可用 | 账户是否连接、授权是否有效 |
| 渠道控制技能文件集合 | Shell，[launch-daemon](../runtime/launch-daemon.md) | 特定环境变量与 scopes 影响挂载 | 完整 scoped 目录内容与服务配置 |
| binary 暴露是另一条轴 | [bin-scopes](../runtime/bin-scopes.conf.md) | 文件可见性不能替代全部授权 | 宿主 worker 的完整权限集合 |
| 元数据指导任务分流 | SKILL 与 [skill-creator](../skills/skill-creator.md) | 描述与显式工作流形成选择依据 | loader、排序器、检索与裁剪算法 |
| 按需读参考 | [Travel Planning](../skills/travel-planning.md)、[Goals](../skills/goals.md) | 文本明确指定哪些分支读哪些文件 | 运行时是否自动跟踪和加载链接 |
| 方法覆盖组默认 | manifest，[Gmail](../skills/gmail.md) | 可计算静态有效默认 | 用户覆盖值与执行器强制检查 |
| OAuth 与动作授权不同 | manifest 与[连接器说明](product-docs.md) | scope 不能替代本次用户意图 | authd 内部 token 生命周期 |
| 计划与付款分开 | [Booking](../skills/booking.md)、[Shopping](../skills/shopping.md) | live availability 不是承诺授权 | provider 完成与幂等恢复的实现 |
| 195 个数据库关系 | 生成 [schema](database-schema.md) | 表、字段、键、脱敏查询契约 | 写入事务、真实索引性能、当前数据 |
| 只读工具限制查询 | schema 前言与 [muse_db](../skills/muse_db.md) | 文档声明 allowlist/视图/角色 | SQL parser 与数据库权限实际部署 |
| 有技能失效状态 | `runtime.skill_invalidation_state` | 存在该数据契约 | 失效触发、分发和刷新算法 |
| 后台任务与交付分开 | scheduler/runtime 表及产品说明 | run 成功不能证明 delivered | worker lease、原子 outbox 和调度 SLA |
| rootfs 按 digest 协调 | [ensure-rootfs](../runtime/ensure-rootfs.md) | 可见重建与分支策略 | fsop 二进制的路径安全实现 |
| 软件包迁移按名称差集 | Python，[convert-cell-intent](../runtime/image/convert-cell-intent.md) | 版本差异不会单独成为 extras | 包安装 replay 的完整外部效果 |
| 信任文件逐项替换 | [build-cell-trust-store](../runtime/build-cell-trust-store.md) | staging/rename 与只读分发 | 多文件读者的一致性保证 |
| leader 条件不一致 | [runtime-cell-entry](../runtime/runtime-cell-entry.md) | 空与 0 的判定分支不同 | 在真实 CLI 返回约定下是否可达 |
| 静态 HTML kit | [magic-moment](../skills/magic-moment.md) | markup/CSS 组件样例可读 | 缺失 renderer 的运行效果 |
| ELF 内容有重复 | [二进制清单](binaries.md) | SHA-256 相同证明字节相同 | 原环境 inode、符号分发与内部行为 |
| npm 10.9.4 | [package.json](../../../opt/hatch-image/bin/npm-package/package.json) | 本地版本声明及入口源码 | 原发行来源、全依赖安全与当前兼容性 |
| 187 个行为场景 | 12 个 YAML，[评测章](../07-evaluation-and-gaps.md) | 场景与期望可枚举 | 原产品 runner、实际通过率 |

## 旧材料与当前观察

[PROJECT_ANALYSIS.md](../../../PROJECT_ANALYSIS.md) 和 [muse-security-audit.md](../../../home/hatch/workspace/muse-security-audit.md) 保留历史方法和限制。原环境文件系统、未导出资源、时间戳和硬链接不能仅凭 Git 快照复现。报告遇到两份材料不同，以当前具体文件为分析事实，并明确旧观察的时间和范围。

已运行的语法检查只证明语法可解析；临时目录 converter 样例只证明那些受控输入的结果；SHA 清单只检查内容一致性。它们不能累加成“整个系统已安全运行”的结论。

## 开发时需要补充的证据

选择器需要真实任务与期望技能标注；权限需要方法映射和越权测试；非幂等写需要状态不明的恢复场景；后台任务需要 occurrence 和送达链；隔离运行需要真实 Linux 宿主集成测试。仅在目标仓库实际采用相应能力时补齐，不为一份技能说明搭建整套私有平台。
