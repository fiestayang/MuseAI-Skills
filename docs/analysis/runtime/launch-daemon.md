# launch-daemon.sh：容器启动与两套渠道可见性合并

[返回运行时目录](README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [函数与阶段补充](#implementation-details) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[launch-daemon.sh](../../../opt/hatch/runtime-cell/launch-daemon.sh#L1)。

容器启动与两套渠道可见性合并。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

解析固定 rootfs，准备 nspawn 参数，要求 private-users-ownership=map；按 JARVIS_CD_CHANNEL 从 skill-scopes 收集目录，用受限源拷贝到 upper，再 overlay 到 base skills；按 bin-scopes 独立执行同一合并；最后 exec nspawn。scoped reveal 失败卸载清理并只保留 base。

渠道匹配允许多行累加；二进制项在 upper 中去重。未知源跳过，空集合不挂载。文件显示的技能集合由宿主形成，模型无法仅靠路径猜测打开 host-only scoped source。

<a id="bounds"></a>
## 失败路径与证据边界

“fail-closed”仅指没有额外暴露 scoped 项，base 本身仍可用。工具可见性不等于授权边界；host privsep worker 仍另行配置。watcher 清理由 shell trap 表达，成功 exec 后其生命周期还依赖外层服务管理。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [queue_runtime_cell_bootstrap_phase](../../../opt/hatch/runtime-cell/launch-daemon.sh#L7) | 7 | 函数定义 |
| [start_runtime_cell_bootstrap_watcher](../../../opt/hatch/runtime-cell/launch-daemon.sh#L16) | 16 | 函数定义 |
| [stop_launch_watchers](../../../opt/hatch/runtime-cell/launch-daemon.sh#L22) | 22 | 函数定义 |
| [Per-channel scoped-SKILL visibility (merged into /opt/hatch/skills via overlay) ----](../../../opt/hatch/runtime-cell/launch-daemon.sh#L58) | 58 | 阶段注释；需结合相邻实现 |
| [_reveal_scoped_skills](../../../opt/hatch/runtime-cell/launch-daemon.sh#L120) | 120 | 函数定义 |
| [opt/hatch/runtime-cell/launch-daemon.sh](../../../opt/hatch/runtime-cell/launch-daemon.sh#L154) | 154 | 阶段注释；需结合相邻实现 |
| [Per-channel scoped-BINARY visibility (merged into /opt/hatch/bin via overlay) --](../../../opt/hatch/runtime-cell/launch-daemon.sh#L156) | 156 | 阶段注释；需结合相邻实现 |
| [_reveal_scoped_binaries](../../../opt/hatch/runtime-cell/launch-daemon.sh#L210) | 210 | 函数定义 |
| [opt/hatch/runtime-cell/launch-daemon.sh](../../../opt/hatch/runtime-cell/launch-daemon.sh#L246) | 246 | 阶段注释；需结合相邻实现 |

未在本次扫描的其他自有文本脚本中找到非注释引用；外部 systemd unit、镜像构建或二进制调用者不在这项搜索的证明范围。

<a id="implementation-details"></a>
## 选择与启动的具体机制

`queue_runtime_cell_bootstrap_phase` 发送观测事件，失败容忍；`start_runtime_cell_bootstrap_watcher` 启动后台 watcher，`stop_launch_watchers` 在退出/信号处理时回收它。最终用 exec 交给 nspawn，之后进程管理还依赖外部 unit，不由这个 shell 循环监督。

参数使用 `set --` 逐项组合，保留参数边界。必须支持 `--private-users-ownership=map`，否则直接停止。它利用 ID-mapped mount，不在每次启动递归 chown 整棵树。

`_reveal_scoped_skills` 先清 upper/work，复制当前渠道每个已存在目录，检查非空，再 bind base 到 lower、overlay upper 到原 bind source。挂在 source 上是为了后面的 whole /opt/hatch 递归 bind 不遮掉修改。每个可能失败的 mutation 都有显式返回，避免函数在 if 条件中执行时 errexit 被抑制后继续错误流程。

`_reveal_scoped_binaries` 采用相同机制，并去重多行匹配的命令名。两类 reveal 独立降级：失败不增加 scoped 文件，base 仍可启动。源码注释还指出 revealed skill 需要 extensions_scoped 的 acceptance；相关加载器与完整配置没有附带，因此挂出来不是完整的启用证明。

<a id="migration"></a>
## 迁移与验证

迁移时可先用过滤后的 registry 列表；只有需要物理隔离时再用文件挂载。skill 和 executable 的配置必须增加一致性检查，避免可见技能依赖隐藏工具。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../09-validation.md)。
