# ensure-rootfs.sh：根文件系统创建、修复与版本切换

[返回运行时目录](README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [函数与阶段补充](#implementation-details) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[ensure-rootfs.sh](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L1)。

根文件系统创建、修复与版本切换。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

先区分 full bootstrap 与 repair-hosts-only；建立受控 rootfs 路径和操作 wrappers；修复 resolver 文件、CA units、临时清理与 Chromium policy；完整模式核对 image digest，变化时重建；btrfs snapshot 或 overlayfs base 链接；检查 uid/gid；生成 guest 配置并屏蔽宿主专用服务。

可见的 safe_* 写操作多数委派 spawnd fsop，注释要求 openat2 beneath/no-symlink；现存路径解析按 guest 根解释绝对 symlink，最多 40 跳。root ownership 用一次 stat 作为构建流程哨兵，不是全树权限证明。

<a id="bounds"></a>
## 失败路径与证据边界

缺 digest、base 或 ownership 不符退出 78，依赖外部 unit 的 RestartPreventExitStatus。部分 rm/rmdir/ln 仍走路径操作，是否具备完整竞态防护需要结合停机时序和 spawnd 审计。digest 与 root ownership 验证不能互相替代。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [Symlink-safe rootfs traversal ---](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L53) | 53 | 阶段注释；需结合相邻实现 |
| [ensure_not_symlink](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L63) | 63 | 函数定义 |
| [Safe rootfs operation wrappers ---](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L83) | 83 | 阶段注释；需结合相邻实现 |
| [fsop](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L98) | 98 | 函数定义 |
| [safe_mkdir](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L102) | 102 | 函数定义 |
| [safe_write](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L110) | 110 | 函数定义 |
| [safe_append](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L115) | 115 | 函数定义 |
| [safe_touch](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L125) | 125 | 函数定义 |
| [safe_chmod](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L132) | 132 | 函数定义 |
| [safe_rm](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L140) | 140 | 函数定义 |
| [safe_rmdir](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L147) | 147 | 函数定义 |
| [safe_ln](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L154) | 154 | 函数定义 |
| [safe_install](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L162) | 162 | 函数定义 |
| [guest_root_chown](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L168) | 168 | 函数定义 |
| [ensure_resolver_files_are_regular](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L185) | 185 | 函数定义 |
| [install_guest_ca_trust_units](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L220) | 220 | 函数定义 |
| [install_guest_scratch_cleanup](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L288) | 288 | 函数定义 |
| [install_guest_chromium_policy](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L337) | 337 | 函数定义 |
| [normalize_rootfs_relpath](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L385) | 385 | 函数定义 |
| [resolve_rootfs_existing_relpath](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L438) | 438 | 函数定义 |
| [rootfs_path_is_executable](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L531) | 531 | 函数定义 |
| [assert_rootfs_ownership_is_baked](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L577) | 577 | 函数定义 |
| [remove_retired_browser_aliases](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L589) | 589 | 函数定义 |
| [Image-local, digest-keyed base ---](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L657) | 657 | 阶段注释；需结合相邻实现 |
| [nspawn_run](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L982) | 982 | 函数定义 |
| [preseed_rootfs_timezone](../../../opt/hatch/runtime-cell/ensure-rootfs.sh#L1022) | 1022 | 函数定义 |

仓库内文本引用（不是完整运行调用图；字符串也可能是模板内容）：

| 引用位置 | 原文 |
|---|---|
| [pre-start.sh](../../../opt/hatch/runtime-cell/pre-start.sh#L131) | `"/opt/hatch/runtime-cell/ensure-rootfs.sh"` |
| [pre-start.sh](../../../opt/hatch/runtime-cell/pre-start.sh#L204) | `"/opt/hatch/runtime-cell/ensure-rootfs.sh" --repair-hosts-only` |

<a id="implementation-details"></a>
## 函数与阶段细解

| 函数/阶段 | 输入与处理 | 输出及不可忽略的边界 |
|---|---|---|
| ensure_not_symlink | 逐段走 rootfs 相对路径，遇链接先删除 | 是修复步骤；路径检查后再使用仍有竞争窗口，不能单独作安全边界 |
| fsop / safe_mkdir / safe_write / safe_chmod / safe_install / guest_root_chown | 把根目录、相对路径、权限、来源或 owner 交给 spawnd | FD/openat2 安全性由二进制实现承担，Shell 只证明参数和失败传播 |
| safe_append | 先读旧内容，再接入 stdin，最后通过 fsop 写入 | 写边界与读取边界不同；读取仍按路径，不是普通原子 append |
| safe_touch | 向 fsop write 送空输入 | 语义是写空文件，不能按 Unix touch 理解为只改时间；调用者需确保不会误清现有内容 |
| safe_rm / safe_rmdir / safe_ln | 修复路径后 rm、rm -rf、ln -sfn | 仍有基于路径的操作，不能笼统称所有 safe_* 都是持有 FD 的操作 |
| ensure_resolver_files_are_regular | 把 hosts/resolv.conf 的链接或异常类型变成普通 bind 目标，设 mode 和 owner | 保留已有普通文件内容，防止只读 bind 被 stub 链接导向错误位置 |
| install_guest_ca_trust_units | 写 guest service/path，让 guest 自己更新系统 CA | host 不直接重写 guest 的整个证书树；轻量修复模式也安装这些 units |
| install_guest_scratch_cleanup | 写临时区清理配置 | 清理策略是运行环境规则，不能推广成对任意用户文件的删除授权 |
| install_guest_chromium_policy | 写 Chromium 运行策略 | 只解释落地配置，实际浏览器策略支持由版本决定 |
| normalize_rootfs_relpath | 去前导斜杠，折叠 . 与 ..，不越过虚拟根 | 纯字符串归一化，不提供 FD 级路径竞争防护 |
| resolve_rootfs_existing_relpath | 在 guest 根语义内解释相对和绝对 symlink，检查最终类型 | 最多 40 跳；绝对目标仍回到 guest 根，不能用宿主 realpath 语义替代 |
| rootfs_path_is_executable | 先按 guest 语义解析，再检查 -x | 证明路径和执行位，不证明 ABI、动态链接器或运行结果 |
| assert_rootfs_ownership_is_baked | stat -L 检查根的 131072:131072 | 不匹配或不能 stat 时 exit 78；跟随 serving-rootfs 链接才能检查目标树 |
| remove_retired_browser_aliases | 删除两个退休的 google-chrome wrapper | 限定兼容清理，不代表卸载全部浏览器 |
| image digest 阶段 | 比较 image digest 和记录 stamp，变化时丢弃旧 serving snapshot | 不能跨 image 复用未知写层；无 digest 是明确拒绝启动 |
| 文件系统分支 | btrfs 建可写 snapshot；overlayfs 链到 base；其他 FS 需 loopback 佐证 | overlay 下 loopback 探测只作诊断；链接自身也设置映射 owner |
| 旧版本清理与非 apt 迁移 | overlay 清过时 base generation；btrfs 新建时可从旧树 no-clobber 复制 /usr/local | 当前 base 冲突项优先；旧 usr/usr/local 链接被拒绝；这不保证迁移之后所有手装内容永久保留 |
| nspawn_run | 为每次 bootstrap 创建唯一 machine 名，捕获输出与返回码 | 只针对目录 busy 最多尝试 30 次；其他错误立即返回，不是通用无限重试 |
| preseed_rootfs_timezone | 写 Etc/UTC 及 localtime 链接 | 是系统基线时区，不等于用户的业务/旅行时区 |
| 环境与服务阶段 | 清过时 proxy，重写 steady-state 代理/CA，生成目录并屏蔽宿主专用服务 | 当前已把软件包 reconcile 移到启动后的 preflight；不能把旧注释当同步安装流程 |

函数名中的 safe 表达作者意图，具体保证必须逐条看实现及外部调用者。单次语法检查不会验证其 root 权限、mount 或竞争条件。

<a id="migration"></a>
## 迁移与验证

迁移时不复制整套 Linux 生命周期到普通应用；仅在确有不可信 rootfs 时采用 FD 相对写和镜像版本边界。将快速检查与完整验证的保证写清楚。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../09-validation.md)。
