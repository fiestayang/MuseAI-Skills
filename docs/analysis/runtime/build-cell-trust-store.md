# build-cell-trust-store.sh：宿主证书锚与只读 NSS 数据库发布

[返回运行时目录](README.md) · 基线 `61121abf5c4d`

目录：[职责](#scope) · [控制流](#flow) · [边界](#bounds) · [代码定位](#symbols) · [函数与阶段补充](#implementation-details) · [迁移](#migration)

<a id="scope"></a>
## 职责与输入输出

来源：[build-cell-trust-store.sh](../../../opt/hatch/runtime-cell/build-cell-trust-store.sh#L1)。

宿主证书锚与只读 NSS 数据库发布。环境变量、宿主路径和返回状态属于接口的一部分；这些绝对路径均指原 Linux 环境。

<a id="flow"></a>
## 控制流

确保 bind source 目录；计算输入 digest；摘要相同且发布完整时跳过；在 root-only staging 提取 egress/ingress CA，创建两份 NSS DB；在既有目录中逐文件 rename 发布；完整成功才写收敛 marker；缺证书等待后续触发，真正构建失败退出非零。

不读写 guest rootfs 的证书树，避免宿主跟随 guest 路径。目录 bind 保持目录 inode，目录内 rename 对 guest 可见；不能用替换整个 bind source 目录来做发布。NSS 模块配置比 PEM 更敏感，所以宿主构建只读提供。

<a id="bounds"></a>
## 失败路径与证据边界

逐文件原子替换不等于整个多文件数据库事务原子；消费者一致性仍需部署验证。证书链存在不代表网络策略生效。

<a id="symbols"></a>
## 代码定位

| 符号或阶段 | 起始行 | 证据类型 |
|---|---|---|
| [log](../../../opt/hatch/runtime-cell/build-cell-trust-store.sh#L66) | 66 | 函数定义 |
| [ensure_bind_sources](../../../opt/hatch/runtime-cell/build-cell-trust-store.sh#L75) | 75 | 函数定义 |
| [inputs_digest](../../../opt/hatch/runtime-cell/build-cell-trust-store.sh#L82) | 82 | 函数定义 |
| [published_looks_complete](../../../opt/hatch/runtime-cell/build-cell-trust-store.sh#L92) | 92 | 函数定义 |
| [build_nssdb](../../../opt/hatch/runtime-cell/build-cell-trust-store.sh#L114) | 114 | 函数定义 |
| [publish_dir](../../../opt/hatch/runtime-cell/build-cell-trust-store.sh#L144) | 144 | 函数定义 |

未在本次扫描的其他自有文本脚本中找到非注释引用；外部 systemd unit、镜像构建或二进制调用者不在这项搜索的证明范围。

<a id="implementation-details"></a>
## 函数与发布协议

| 函数 | 处理 | 关键约束 |
|---|---|---|
| ensure_bind_sources | 创建 anchors、system NSS、user NSS 目录 | 保持发布目录存在；运行中 bind 持有这些目录 inode |
| inputs_digest | 对 egress CA 与 ingress fullchain 求摘要，缺文件也纳入 absent 标识 | 输入未变与产物完整共同决定是否跳过 |
| published_looks_complete | 检查两份 anchor 和两份 cert9.db | 快速完整性判断，不是逐张证书验证或数据库一致性检测 |
| build_nssdb | certutil 初始化，再按存在的 CA 导入 trust anchor，设读权限 | staging 路径、发布路径和 cell 使用路径不同；NSS 行为验证是源注释中的历史声明，不是本轮重跑 |
| publish_dir | 逐文件复制到 .publishing 名，rename 覆盖，再清过期项 | 必须修改目录内容而非替换整个目录；变量为空时中止危险 rm |
| 最后 marker | 完整成功后记录输入 digest | 一份 marker 不能把多文件更新变成事务；轮转途中读者行为还需集成测试 |

PEM anchors 与 NSS 数据库都是实际产物。没有证书输入时可等待后续触发，不应伪造成功证书；构建失败需要留下可诊断状态。

<a id="migration"></a>
## 迁移与验证

迁移时分离可信 producer 与不可信 consumer，明确 inode 挂载语义；证书轮转必须验证运行中的读者看到新版本。

本次未启动容器、调用宿主控制命令或连接服务。静态语法及离线样例的实际结果统一见 [验证记录](../09-validation.md)。
