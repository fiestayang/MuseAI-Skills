# hatch-preflight-opportunistic：非阻塞包协调与 OS intent 重放

[返回运行时目录](README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [函数与阶段补充](#implementation-details) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[hatch-preflight-opportunistic](../../../opt/hatch/runtime-cell/hatch-preflight-opportunistic#L1)。

非阻塞包协调与 OS intent 重放。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

等 cell ready，进入相应 cgroup；让服务启动优先，最多等待 execution-ready；以单次 open O_NOFOLLOW/O_NONBLOCK+fstat 复制不可信 ledger；保留最多 16 MiB 并计算有 64 MiB 上限的完整摘要；按输入摘要与五次失败阈值退避；cell 内 reconcile manifest；迁移旧 rootfs 后重新快照再重放 intent；记录 receipt 和 strikes。

包意图持久化替代持久整棵 rootfs。基础包 reconcile 与用户 package intent 分开；旧迁移后再次快照防止本轮漏掉新追加条目。尾部始终 exit 0 体现 opportunistic，不表示包安装全部成功。

<a id="bounds"></a>
## 失败路径与证据边界

重放用 sed/tr 等解析限定 JSONL 形状，并校验包 token；不是通用 JSON 解析器。超过保留上限的后部意图不会全部应用，摘要变化只解决检测，不解决重放完整性。host/guest 文件信任边界仍依赖实际挂载和所有权。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [Yield to serving startup (bounded) ---](../../../opt/hatch/runtime-cell/hatch-preflight-opportunistic#L117) | 117 | 阶段注释；需结合相邻实现 |
| [Failure backoff (host-side state, guest-unwritable) ---](../../../opt/hatch/runtime-cell/hatch-preflight-opportunistic#L140) | 140 | 阶段注释；需结合相邻实现 |
| [One-open ledger snapshot (RT-11) ---](../../../opt/hatch/runtime-cell/hatch-preflight-opportunistic#L156) | 156 | 阶段注释；需结合相邻实现 |
| [snapshot_os_intent_ledger](../../../opt/hatch/runtime-cell/hatch-preflight-opportunistic#L189) | 189 | 函数定义 |
| [Recorder snapshot reset (MUST precede the reconcile) ---](../../../opt/hatch/runtime-cell/hatch-preflight-opportunistic#L356) | 356 | 阶段注释；需结合相邻实现 |
| [Per-VM package-intent ledger replay ---](../../../opt/hatch/runtime-cell/hatch-preflight-opportunistic#L436) | 436 | 阶段注释；需结合相邻实现 |
| [replay_os_intent_ledger](../../../opt/hatch/runtime-cell/hatch-preflight-opportunistic#L464) | 464 | 函数定义 |
| [One-time cutover conversion: old serving rootfs -> os-intent ledger ---](../../../opt/hatch/runtime-cell/hatch-preflight-opportunistic#L763) | 763 | 阶段注释；需结合相邻实现 |
| [convert_via_staging](../../../opt/hatch/runtime-cell/hatch-preflight-opportunistic#L784) | 784 | 函数定义 |
| [safe_fd](../../../opt/hatch/runtime-cell/hatch-preflight-opportunistic#L799) | 799 | 函数定义 |

未在本次扫描的其他自有文本脚本中找到非注释引用；外部 systemd unit、镜像构建或二进制调用者不在这项搜索的证明范围。

<a id="implementation-details"></a>
## 内部数据流程细解

| 阶段/函数 | 处理 | 可观察结果或限制 |
|---|---|---|
| serving startup 让路 | 等 runtime ready，进入维护身份，有限等待执行服务可用 | 包维护不是启动正确性的前置事务 |
| snapshot_os_intent_ledger | 单次安全 open，fstat 普通文件，复制前 16 MiB，对最多 64 MiB 输入求哈希 | 3/4 区分拒绝打开或非普通文件，5 表示超过上限；其他错误归宿主错误，避免把 ENOSPC 都叫攻击 |
| snapshot sidecars | 写 sha256 和 skipped-bytes 到宿主私有位置 | 哈希随尾部变化，但尾部不会被重放；变更检测不等于完整处理 |
| backoff | 用 ledger+manifest 摘要绑定连续失败次数，达到 5 次抑制 apt 阶段 | 输入变化解除退避；不是跨所有任务共享的失败计数 |
| recorder snapshot reset | 在 reconcile 前重置记录基准 | 避免系统包协调被错误归因成用户删除意图 |
| in_cell_reconcile | 设内存上限，尽力 dpkg --configure -a，优先镜像目录找 hatch-manifest 和清单 | 不删除 apt/dpkg 锁文件；锁等待失败应留待下一轮，不能破坏活锁保护 |
| replay_os_intent_ledger | 只读快照，读取并清洗 guest receipt 摘要，判断是否可跳过 | receipt 是 guest 可控性能状态，不作为宿主权限凭据 |
| extract_pkg_tokens | 从有限 JSONL 形状抽数组，关闭 glob，校验首字符和允许字符集 | 正规 JSON 的转义、嵌套和任意空白格式不能凭此承诺；只接受对应生产者格式 |
| drop_token 与 fold | converted/apt-install/dpkg-post-invoke 折叠成 net_install/net_remove，后事件取消相反意图 | baseline 不带 delta；空版本升级记录可跳过；列表身份是包名，不是精确版本 |
| 实际 replay | 在 cell 内处理依赖状态、删除与安装，成功后写 receipt | shell 执行与 apt 外部效果未在本次运行；失败不能称恢复完成 |
| convert_via_staging | Python converter 先写 root-only staging，再以 NOFOLLOW/NONBLOCK+fstat 写目标 ledger、snapshot、done | 比直接让 converter 输出到 guest 可写目录多一道边界；仍不能从本文件推导所有父目录/并发安全 |
| 迁移后再次 snapshot | conversion 可能新增 ledger，必须用新副本进入 replay | 若复用脚本初始快照，会漏掉本次迁移包 |
| strike accounting | reconcile 和 replay 都成功才清失败计数，否则记录本轮输入摘要 | 总脚本仍 exit 0，真实结果必须看阶段日志和状态 |

这里同时存在外层 Shell、内嵌 Python 和 guest shell 字符串。语法检查外层 Shell 不会覆盖所有内嵌语言；本报告不把 `sh -n` 写成端到端检查。

<a id="migration"></a>
## 迁移与验证

迁移时保留不可变快照、明确容量上限、幂等重放和可见退化状态；普通项目可直接使用标准 JSON parser 与小型追加日志，避免 shell 手工解析。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../09-validation.md)。
