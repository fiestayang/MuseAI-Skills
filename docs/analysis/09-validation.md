# 实际验证记录

[返回目录](README.md) · [检查脚本](checks/validate.py)

## 验证对象与方法

所有检查围绕基线 `61121abf5c4da12fe32ef970a861108b16a0731b` 及本次新增报告。只读检查原始文件；converter 的执行样例仅使用自动清理的临时目录，不触碰真实 rootfs、dpkg、ledger 或外部服务。

检查脚本使用 Python 标准库。Shell 仅执行 `sh -n` 或 `bash -n`，不运行脚本主流程。Python 用 AST 解析；converter 通过非 main 的 runpy 加载函数，在临时目录构造输入。

```sh
python3 docs/analysis/checks/validate.py --checksums
git diff --check
```

## 检查结果

本轮在 2026-09-25 执行，检查通过。结果范围如下：

| 项目 | 结果 | 证明范围 |
|---|---|---|
| 基线路径覆盖 | 2,658 / 2,658，无重复、无遗漏 | 每个原路径有报告归属，机器清单与 Markdown 索引一致 |
| 技能覆盖 | 68 个独立报告，4 个别名解析成功 | 每篇具备触发、流程、文件、权限、评测、迁移和证据章节 |
| manifest / eval 清点 | 38 个独立 manifest、2 个别名、12 个 eval 文件 | 与本地文件盘点一致 |
| YAML 解析 | 38 份 manifest 和 12 份 eval 解析成功，共 187 场景 | 使用系统 Ruby YAML，未添加依赖；未运行行为场景 |
| Markdown | 115 篇，所有本地目标链接和源码行号有效 | 检查文件存在与行号边界；不等于逐个浏览器渲染检查 |
| Shell 静态语法 | 19 个脚本通过 | 使用其 shebang 对应的 sh/bash -n；不验证 Linux 运行效果 |
| Python 静态语法 | converter 与本次检查脚本通过 AST 解析 | 不生成 pyc，不修改源文件 |
| converter 离线样例 | 9 项显式结果检查通过 | 仅在临时目录运行受控输入，无真实系统包操作 |
| SHA256SUMS | 2,649 / 2,649 一致 | 不含校验清单自身和符号链接；不认证发行者身份 |
| 原始文件变更 | 无 | Git 原跟踪文件保持不变，新增内容仅在 docs/analysis |
| 文档空白检查 | 通过 | 检查尾空白和最终换行；另运行 git diff --check |

YAML 解析采用本机已有 Ruby 的 YAML/JSON 标准库，按文件读取；表格将方法 default 覆盖组 default。原文件中的命令、eval 用户消息和便携记忆 prompt 均只作为材料读取。

## 离线样例覆盖

converter 检查包括：忽略无 Package 的 stanza、保留缺失字段、按包名而非版本做差集、只计已安装包、生成 done marker、快照保留非 installed 状态、done 后不再读取旧状态或追加 ledger、保留已有快照、输出基线 manifest，以及缺少 dpkg 状态时报错。这些断言不能验证断电恢复、并发写入或真实 apt replay。

## 未执行的部分

没有启动随包 ELF、Linux runtime cell、浏览器服务或连接器。没有调用 provider API、支付、发信、部署、遗忘执行器或原产品评测 runner。没有对 npm 依赖运行安装脚本、CVE 扫描或全量测试；第三方源码按包与关键入口分析。

因此“检查通过”限于覆盖、链接、语法、内容摘要和已列离线样例，不代表线上功能、授权执行、供应链或隔离安全已通过验收。
