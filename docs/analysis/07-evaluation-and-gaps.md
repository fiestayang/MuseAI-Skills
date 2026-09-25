# 行为评测、缺项与维护问题

[返回目录](README.md)

## 目录

[场景覆盖](#场景覆盖) · [问题清单](#问题清单) · [验证分级](#验证分级)

## 场景覆盖

12 份 YAML 共 187 个场景，覆盖 12/68 个独立技能。场景主要是任务输入与应检查行为，不是附带可直接运行的测试框架。本次仅解析和整理，没有连接 Muse 服务执行。完整 tests 文本已放进对应技能文章，避免把场景标题当成完整规格。

| 技能 | 场景数 | 分析 |
|---|---|---|
| `booking` | 16 | [booking](skills/booking.md) |
| `duffel` | 19 | [duffel](skills/duffel.md) |
| `flightaware` | 13 | [flightaware](skills/flightaware.md) |
| `gmail` | 20 | [gmail](skills/gmail.md) |
| `google-calendar` | 15 | [google-calendar](skills/google-calendar.md) |
| `google-contacts` | 11 | [google-contacts](skills/google-contacts.md) |
| `google-drive` | 17 | [google-drive](skills/google-drive.md) |
| `google-tasks` | 16 | [google-tasks](skills/google-tasks.md) |
| `opentable` | 19 | [opentable](skills/opentable.md) |
| `places-search` | 9 | [places-search](skills/places-search.md) |
| `plaid` | 8 | [plaid](skills/plaid.md) |
| `travel-planning` | 24 | [travel-planning](skills/travel-planning.md) |

数量不能代表正确率。无 YAML 的技能可能受产品层或私有评测覆盖，但仓库没有给出证据；不能说它们“没有任何测试”。本地 eval 中出现真实服务目标，不应在普通文档检查时自动调用。

## 问题清单

以下均不修改原代码。P1 表示移植或操作前应先解决的正确性边界；P2 表示维护与可运行性缺口。这些是本报告排序，不是作者给出的严重级别。

| 优先级 | 观察与证据 | 影响 | 建议与验证 |
|---|---|---|---|
| P1 | [runtime-cell-entry](runtime/runtime-cell-entry.md) 两个 leader 检查对 0 的处理不同 | 可能对无效 leader 的接受条件不一致；尚未集成复现 | 明确 CLI 返回约定，测试空/0/已退出 PID/有效 PID |
| P1 | [shopping backends](skills/shopping.md) 的仅展示字段投影丢 product_id，与主文件保留身份要求冲突 | 后续购物车/支付可能失去准确对象 | 搜索到 checkout 全链保留 product_id、变体和商户 ID |
| P1 | [Artifacts](skills/README.md) 所依赖 scripts 未附齐 | 文档流程不能在该快照直接完成 | 先核对真实工具，使用现有渲染/导出实现替代，并做实际产物检查 |
| P1 | [convert-cell-intent](runtime/image/convert-cell-intent.md) 用包名差集，没有版本 pin；无锁/fsync | 不能宣称精确还原旧版本或并发/掉电事务安全 | 确认单写者与故障模型，按需求补测试；不无条件增加复杂事务 |
| P2 | [withings commands](skills/withings.md) 重复大章节且认证描述不一致 | 维护源不唯一，操作路径易混淆 | 核定 query 与 legacy passthrough 的现行接口，再合并重复说明 |
| P2 | [control-daemon](runtime/control-daemon.md) 的旧说明与实际直接 exec 不一致 | 按注释绘图会得到错误调用链 | 以末尾实现为准，未来同步注释 |
| P2 | [resolve-rootfs-path](runtime/resolve-rootfs-path.md) 已固定路径，is-loopback 的引用说明陈旧 | 容易高估动态选择分支仍生效 | 搜索实际调用者，区分历史入口和当前代码 |
| P2 | [skill-creator](skills/skill-creator.md) 的 scaffold helper 未随包 | 创建流程不可照命令直接运行 | 用仓库现有模板手工生成，或取得真实 helper |
| P2 | [magic-moment](skills/magic-moment.md) 的 mm/cmm 等实现不齐 | 有详细作者规范和 HTML，缺完整视频流水线，HTML 引用的字体也未附带 | 明确外部 bundle，不能把静态 kit 当成 renderer |
| P2 | [voice-selector](skills/voice-selector.md) 引用的 voice_source.json 未附 | 无法重建声库生成来源 | 保留当前表为快照，另核真实 provider 与版本 |
| P2 | [generate_podcast](skills/generate_podcast.md) 引用 podcast-helper，vendored 说明也不等于完整源码 | 生成目录与上传发布流程可能缺段 | 验证 helper 与账号前提，分别检查本地 episode 和外部状态 |
| P2 | [Spaces](appendices/shared-resources.md) 缺 SDK/build 与服务实现 | 接口声明不足以直接构建运行 | 使用目标工程现有服务端工具层，契约测试支持字段 |
| P2 | `opt/hatch-image/bin/gws` 是空文件 | 不能把路径存在当可用 CLI | 区分安装占位和真正命令；不要用该文件冒充 gws 实现 |
| P2 | [历史审计](appendices/product-docs.md) 与 [旧总报告](../../PROJECT_ANALYSIS.md) 描述旧 inode/环境 | 旧硬链接数、无 Git 等不能套用当前 checkout | 当前用 Git 基线和内容哈希重新确认，保留历史材料来源 |

## 验证分级

本次能验证文件覆盖、链接、配置可解析、脚本静态语法、converter 临时目录样例和原文件摘要。没有凭据与完整运行环境，不验证连接器权限真正执行、订单幂等、跨进程隔离、调度可靠性或线上产品可用性。

[FlightAware 历史 findings](../../opt/hatch/skills/flightaware/eval/findings.md) 记录过代理路由和 smoke 问题。它们是原作者在当时环境的观察，不是本轮结果。历史“clean”或“passed”同样不能作为当前快照已通过的证据。

迁移时先给高损失路径写可观察断言，再验证普通业务成功路径。无需把所有场景一次变成测试；但实际移植的能力不能只检验正向 happy path。
