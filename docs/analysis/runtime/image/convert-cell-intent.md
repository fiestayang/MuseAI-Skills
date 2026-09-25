# image/convert-cell-intent：旧 rootfs 到包意图的单次转换

[返回运行时目录](../README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [函数与阶段补充](#implementation-details) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[convert-cell-intent](../../../../opt/hatch-image/bin/convert-cell-intent#L1)。

旧 rootfs 到包意图的单次转换。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

parse_dpkg_status 按空行分 stanza，取 Package/Version/Status；is_installed 筛出 installed；emit-base-manifest 排序生成基础包；convert 计算旧已安装包名减 base 包名，追加 converted JSONL，缺省写 dpkg snapshot，最后 atomic_write done marker。

先 ledger 后 done：崩溃可能重复追加，但不会因提前 marker 丢失意图；幂等重放接受重复。只迁移包名，不保留非基础包的精确版本或手工文件改动。atomic_write 用同目录 tmp+replace。

<a id="bounds"></a>
## 失败路径与证据边界

单独脚本没有锁、fsync 或不可信路径的 FD 防护，安全性依赖调用方 staging 和串行运行；不能把 rename 当持久化事务。它从不删除旧 rootfs。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [parse_dpkg_status](../../../../opt/hatch-image/bin/convert-cell-intent#L38) | 38 | 函数定义 |
| [is_installed](../../../../opt/hatch-image/bin/convert-cell-intent#L69) | 69 | 函数定义 |
| [load_status_or_die](../../../../opt/hatch-image/bin/convert-cell-intent#L74) | 74 | 函数定义 |
| [dpkg_state_lines](../../../../opt/hatch-image/bin/convert-cell-intent#L84) | 84 | 函数定义 |
| [atomic_write](../../../../opt/hatch-image/bin/convert-cell-intent#L90) | 90 | 函数定义 |
| [cmd_emit_base_manifest](../../../../opt/hatch-image/bin/convert-cell-intent#L97) | 97 | 函数定义 |
| [read_base_names](../../../../opt/hatch-image/bin/convert-cell-intent#L110) | 110 | 函数定义 |
| [cmd_convert](../../../../opt/hatch-image/bin/convert-cell-intent#L121) | 121 | 函数定义 |
| [main](../../../../opt/hatch-image/bin/convert-cell-intent#L159) | 159 | 函数定义 |

仓库内文本引用（不是完整运行调用图；字符串也可能是模板内容）：

| 引用位置 | 原文 |
|---|---|
| [hatch-preflight-opportunistic](../../../../opt/hatch/runtime-cell/hatch-preflight-opportunistic#L835) | `cutover_converter="/opt/hatch-image/bin/convert-cell-intent"` |

<a id="implementation-details"></a>
## Python 函数逐项

| 函数 | 具体逻辑 | 边界 |
|---|---|---|
| parse_dpkg_status | 逐行读 UTF-8（坏字节替换），空行 flush；提取 Package/Version/Status，EOF 再 flush | 缺 Package 丢弃 stanza；缺其他字段为空；不读取 continuation 为新顶层字段 |
| is_installed | 用 split 后最后一个词是否 installed 判断 | 实现并未严格要求恰好三个词；调用前提是 dpkg 标准状态字段 |
| load_status_or_die | 检查 rootfs/var/lib/dpkg/status 是文件，再调用 parser | 不存在时报 SystemExit，独立函数没有 NOFOLLOW 保护 |
| dpkg_state_lines | 将 name/version/status 拼成行后排序 | 快照包含所有命名记录，不只 installed |
| atomic_write | 同目录 .tmp 写内容、chmod、os.replace | 没有唯一临时名、锁或 fsync；并发与断电保证不由函数提供 |
| cmd_emit_base_manifest | 过滤 installed，写排序后的 name version | 生成镜像基线清单；不修改 dpkg |
| read_base_names | 跳空行和注释，仅取每行第一个词 | 版本不参与差集，名称解析依赖既定格式 |
| cmd_convert | done 存在即跳过；计算 extras 集合，写 converted 事件；仅缺快照才创建；最后 done | ledger 先于 done；崩溃后重跑允许重复事件；不删除旧 rootfs |
| main | argparse 选择 convert 或 emit-base-manifest，路径参数转 Path，派发已绑定函数 | 只在 __main__ 入口执行；离线检查以其他 run_name 加载函数 |

命令 stdout/stderr 与状态文件是不同输出通道。测试日志写到 stderr 不代表转换失败，实际失败靠异常/退出码；调用方还需要核对 ledger 和 marker。

<a id="migration"></a>
## 迁移与验证

迁移时根据恢复目标决定是否锁定版本，保留“已完成”标记最后写入的顺序；需要耐断电再增加 fsync，不默认将该脚本宣传成完整磁盘迁移器。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../../09-validation.md)。
