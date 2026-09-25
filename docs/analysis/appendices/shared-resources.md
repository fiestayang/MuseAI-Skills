# 共享参考与 Spaces 运行契约

[返回目录](../README.md)

这些资源没有独立 SKILL 入口，不额外计入 68 个技能。Artifacts 通用规则被多个产物技能复用；Spaces 文件提供作者工作区和应用接口说明，未附完整 SDK、build pipeline 或服务执行器。

## 逐文件

### artifacts/references/charts.md

来源：[opt/hatch/skills/artifacts/references/charts.md](../../../opt/hatch/skills/artifacts/references/charts.md)。

先核实数值来源，再决定数据到视觉标记的映射；区分 slide、PDF、静态页和 TS runtime 的技术路径。统计值缺失不能由图表组件补造。

### artifacts/references/live-data.md

来源：[opt/hatch/skills/artifacts/references/live-data.md](../../../opt/hatch/skills/artifacts/references/live-data.md)。

动态 fullstack 使用服务端 ctx 通道，静态页只交付带日期的快照；密钥不入浏览器。数据刷新失败和缓存时间必须可见，不能把静态产物包装为实时仪表板。

### artifacts/references/maps.md

来源：[opt/hatch/skills/artifacts/references/maps.md](../../../opt/hatch/skills/artifacts/references/maps.md)。

按信息需求选地图层级，保存结构化地点与已验证坐标，区分导航链接与嵌入地图。名字相同的地点需先消歧，嵌入失败不应引入虚构位置。

### artifacts/references/markdown.md

来源：[opt/hatch/skills/artifacts/references/markdown.md](../../../opt/hatch/skills/artifacts/references/markdown.md)。

约束标题、列表、表格和强调等可编辑文本格式；结构应由 Markdown 语法表达，避免用装饰符号伪造层级。

### artifacts/references/prose.md

来源：[opt/hatch/skills/artifacts/references/prose.md](../../../opt/hatch/skills/artifacts/references/prose.md)。

从范围检查、提纲、陈述型标题到全文回读，剔除生成过程说明和空泛语句。适合转为文档验收清单，不能用措辞规则替代事实检查。

### artifacts/references/social-embeds.md

来源：[opt/hatch/skills/artifacts/references/social-embeds.md](../../../opt/hatch/skills/artifacts/references/social-embeds.md)。

说明何种社交内容可 iframe、应使用的 markup、不同渲染表面的限制及媒体字节处理。页面链接不代表允许直接获取持久媒体副本。

### spaces/templates/space-static/workspace_agents.md

来源：[opt/hatch/skills/spaces/templates/space-static/workspace_agents.md](../../../opt/hatch/skills/spaces/templates/space-static/workspace_agents.md)。

静态 artifact 作者工作区规则，面向构建任务而非独立 skill。其约束只在对应产物任务中适用，不应提升为整个仓库的 Agent 指令。

### spaces/templates/space-ts/workspace_agents.md

来源：[opt/hatch/skills/spaces/templates/space-ts/workspace_agents.md](../../../opt/hatch/skills/spaces/templates/space-ts/workspace_agents.md)。

交互 artifact 的工作区和数据存放约束，区分应用独立数据与用户主状态；是生成模板，完整 SDK 与编译工具没有随包提供。

### spaces/ts-runtime/README.md

来源：[opt/hatch/skills/spaces/ts-runtime/README.md](../../../opt/hatch/skills/spaces/ts-runtime/README.md)。

描述 server actions、client typed transport、本地 SQLite/blob 和 Cloudflare D1/R2 导出。initialDbSnapshot 是一次性单向 seed；不能据此承诺双向同步或完整本地状态迁移。

### spaces/ts-runtime/docs/vertical-tool-schemas.md

来源：[opt/hatch/skills/spaces/ts-runtime/docs/vertical-tool-schemas.md](../../../opt/hatch/skills/spaces/ts-runtime/docs/vertical-tool-schemas.md)。

天气、金融、体育与 web_search 的 ctx.tool 请求/结果契约，注明尚未贯通后端的 knobs；本地接口声明不保证每个可选字段已被真实执行。

## 共享规则的调用思路

先决定交付类型，再读对应技能；只有确实涉及图表、地图、实时数据或嵌入媒体时才追加共享参考。这样能保留共同约束，同时避免每个技能都重复长说明。原系统是否自动收集这些引用未知，文本中的“read”不能证明 loader 自动递归加载。

## 静态页面与交互应用

静态页面交付文件或一次数据快照。交互应用有服务端 action、客户端 typed transport、独立数据库和 blob。密钥与 provider 调用应通过服务端 ctx，不能打进前端 bundle。vertical-tool-schemas 中接口及可选参数只构成契约；文件自己标注尚未贯通的后端选项，不应据此承诺所有字段生效。

`initialDbSnapshot` 是单向初始 seed，不是双向数据同步协议。部署到 D1/R2 所需要的状态映射、迁移和失败恢复不能从一份 README 推导出来。目标仓库已经有数据库时，用已有边界实现类似功能即可。

## 文件交付与完成判定

任务给定的 project_dir 优先，不能一律改为 workspace/your_files。源文件、预览、导出和上传状态分别记录。文档出现的 Artifacts 辅助脚本在快照中不齐，采用其工作流之前必须找到真实实现或使用目标仓库现有工具替代，不能把命令示例当成可运行依赖。
