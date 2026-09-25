# 目录结构与文件导览

[总目录](README.md)

以下展开完整的一层职责结构；每个实际文件都可在 [覆盖清单](appendices/file-coverage.md) 定位。技能树逐项见 [技能目录](skills/README.md)，因此不在此重复 68 篇列表。

```text
MuseAI-Skills/
├── .gitattributes
├── .gitignore
├── README.md
├── README.en.md
├── PROJECT_ANALYSIS.md
├── SHA256SUMS
├── home/
│   └── hatch/
│       ├── config/
│       ├── docs/
│       ├── assets/onboarding_tour/
│       ├── workspace/
│       └── PROACTIVE_PREFERENCES.md
├── opt/
│   ├── hatch/
│   │   ├── skills/
│   │   ├── bin/
│   │   └── runtime-cell/
│   └── hatch-image/
│       └── bin/
│           ├── npm-package/
│           ├── codex-resources/
│           └── rtc-sidecar-lib/
└── docs/
    └── analysis/
        ├── skills/
        ├── runtime/
        ├── appendices/
        └── checks/
```

## 根文件逐项说明

| 文件 | 处理内容与作用 | 注意事项 |
|---|---|---|
| [README.md](../../README.md) | 中文入口、技能分类、环境布局与可运行性边界 | 是仓库作者说明，仍需核对本地文件 |
| [README.en.md](../../README.en.md) | 英文入口 | 不能当第二份独立实现证据 |
| [PROJECT_ANALYSIS.md](../../PROJECT_ANALYSIS.md) | 旧总体分析与证据索引 | 记录的原始存档口径不等于当前 checkout |
| [SHA256SUMS](../../SHA256SUMS) | 内容完整性基准 | 摘要不证明来源身份；符号链接和自身不按普通文件校验 |
| [.gitattributes](../../.gitattributes) | 字节保留及 LFS 管理 | Git blob 可能是 LFS pointer，本地内容可能是已下载 ELF |
| [.gitignore](../../.gitignore) | 忽略系统元数据 | npm 依赖实际已跟踪，不因通常叫 node_modules 就排除盘点 |

## 技能目录结构

`SKILL.md` 的 frontmatter 为选择提供描述；正文规定流程。`manifest.yaml` 为连接器提供方法权限与可选的 CLI 映射。`references`、`guide`、`creation`、`guides` 和 `assets` 承担长文、分支策略及实际素材。`eval` 保存场景及期望行为。

不能根据目录同名假设内部标识一致。例如 `messenger` 的 name 是 `messenger_read`，`google-calendar` 是 `google_calendar`。别名用符号链接复用，`voice-calls` 指向静态声库入口而非通话工具。

Artifacts 有六个独立子技能，共享 reference 不再计为 skill。Spaces 只有模板和 runtime 说明，没有顶层 SKILL；不能据目录名新增第 69 个技能。

## 运行时目录结构

生命周期：`pre-start` 准备、`launch-daemon` 启容器、`post-start` 配网络和 ready、`stop` 排空与升级停机、`post-stop` 回收。

进程入口：`control-daemon` 与 `control-execd` 读取共享 helper 后执行二进制。`run-daemon` 仍在树中，但当前 controller 没调用它，见 [入口分析](runtime/control-daemon.md)。

状态构建：`ensure-rootfs` 管理 image-local 根；`hatch-preflight-opportunistic` 处理软件包期望和用户意图；`build-cell-trust-store` 发布信任锚；`require-modules` 在锁定前预加载模块。其依赖关系不能靠文件名字排序推断。

## 建议阅读路径

- 技能机制：skill-creator → Gmail 正文/manifest/eval → travel-planning → booking。
- 高风险工作流：forget → shopping/UCP → duffel → muse-mail。
- 产物与应用：artifacts/testing → 目标格式技能 → 共享 references → Spaces。
- 隔离运行：runtime-cell-entry → controllers → pre-start → launch → post-start → ensure/preflight → stop。
- 数据与诊断：muse_db → schema 附录 → self_improvement 与 scheduling 文档。
