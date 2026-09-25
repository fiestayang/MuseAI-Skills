# 第三方组件与 npm 源码

[返回目录](../README.md) · [全部路径](file-coverage.md)

附带 npm 的本地 package.json 声明版本为 `10.9.4`。目录共有 2,269 个 Git 路径，包含程序、依赖、文档、许可和模块格式配置。解析了 211 份具备 name/version 的包 manifest，以及 44 份模块格式 package.json；这些是包实例，嵌套安装同名包不合并成一个版本。

本报告分析主 CLI 控制流、逐命令入口和每包职责。全量路径索引记录具体文件所属组件与可见符号线索。没有逐函数审计全部约 5.7 MB 的第三方 JavaScript，也没有运行 npm install、包脚本或漏洞审计；因此不声称所有第三方实现安全或已通过测试。

## 主调用流程

1. `bin/npm-cli.js` 把 process 交给 `lib/cli.js`；后者尝试启用 Node compile cache，装入 engine 校验器，延后加载真正入口。
2. `lib/cli/entry.js` 设置 process.title，处理 npmg 全局模式，给 fs 装 graceful-fs，创建 Npm 与 ExitHandler。初次日志只输出 argv 前两个路径，避免把敏感参数直接写出；后续错误日志使用 redact。
3. `Npm.load()` 处理配置并返回 command/args/exec 决策。无命令时输出 usage；有效命令进入 `npm.exec`。update notifier 与命令异步并行，不阻塞主命令完成。
4. command 按类处理参数、workspace 与具体行为。安装命令委托 Arborist reify 依赖树；包获取交给 pacote；本地或远程命令执行交 libnpmexec。
5. 成功和失败统一通过 ExitHandler。entry 的 catch 捕获命令错误，不表示所有 npm 内部失败都可恢复。

入口证据：[bin/npm-cli.js](../../../opt/hatch-image/bin/npm-package/bin/npm-cli.js), [lib/cli.js](../../../opt/hatch-image/bin/npm-package/lib/cli.js), [lib/cli/entry.js](../../../opt/hatch-image/bin/npm-package/lib/cli/entry.js), [lib/npm.js](../../../opt/hatch-image/bin/npm-package/lib/npm.js), [lib/cli/exit-handler.js](../../../opt/hatch-image/bin/npm-package/lib/cli/exit-handler.js)。

`index.js` 被 require 时明确报错：npm v8 起取消 programmatic API。目标工程不能把它作为一般应用库直接 import；使用已存在的包管理器 CLI 或具体底层库。

## install 与 exec 的副作用

`lib/commands/install.js` 区分 global/local prefix，读取 ignore-scripts、force 和 script-shell。更新 npm 自身时检查 engines；过滤把 prefix 安装进自身的参数。随后 Arborist.reify 执行依赖调整；在无显式包参数、非全局且未 ignore-scripts 时，顺序执行项目的 preinstall、install、postinstall、prepublish、preprepare、prepare、postprepare，再 reifyFinish。

`bin/npx-cli.js` 将 argv 改写为 npm exec；兼容旧参数，处理 --package、--script-shell、--yes=false 等，并将位置参数与 npm 自己的选项分开。`lib/commands/exec.js` 决定 localBin、globalPath、pkgPath、runPath 和 workspace，再把参数交 libnpmexec。源码检查无需实际执行这些路径。

包获取的 pacote 入口将 resolve/extract/manifest/packument/tarball 交给对应 fetcher（registry、git、file、directory、remote）。这说明安装可能涉及网络和脚本，而不只是读取本地 JSON；不要为分析该快照而自动安装。

## 67 个命令入口

下表从源码抽取静态 description、基类与方法，作为每个命令的职责/实现定位。继承的行为和委托模块需结合包表阅读，未把静态抽取当成测试结果。

| 命令文件 | 描述 | 基类 | 本文件方法 |
|---|---|---|---|
| [access.js](../../../opt/hatch-image/bin/npm-package/lib/commands/access.js) | Set access level on published packages | `BaseCommand` | `completion`, `exec` |
| [adduser.js](../../../opt/hatch-image/bin/npm-package/lib/commands/adduser.js) | Add a registry user account | `BaseCommand` | `exec` |
| [audit.js](../../../opt/hatch-image/bin/npm-package/lib/commands/audit.js) | Run a security audit | `ArboristWorkspaceCmd` | `completion`, `exec`, `auditAdvisories`, `auditSignatures` |
| [bugs.js](../../../opt/hatch-image/bin/npm-package/lib/commands/bugs.js) | Report bugs for a package in a web browser | `PackageUrlCmd` | `getUrl` |
| [cache.js](../../../opt/hatch-image/bin/npm-package/lib/commands/cache.js) | Manipulates packages cache | `BaseCommand` | `for`, `completion`, `exec`, `clean`, `add`, `verify`, `ls` |
| [ci.js](../../../opt/hatch-image/bin/npm-package/lib/commands/ci.js) | Clean install a project | `ArboristWorkspaceCmd` | `exec` |
| [completion.js](../../../opt/hatch-image/bin/npm-package/lib/commands/completion.js) | Tab Completion for npm | `BaseCommand` | `completion`, `exec`, `wrap`, `if` |
| [config.js](../../../opt/hatch-image/bin/npm-package/lib/commands/config.js) | Manage the npm configuration files | `BaseCommand` | `for`, `if`, `completion`, `exec`, `set`, `get`, `del`, `edit`, `fix`, `list`, `listJson` |
| [dedupe.js](../../../opt/hatch-image/bin/npm-package/lib/commands/dedupe.js) | Reduce duplication in the package tree | `ArboristWorkspaceCmd` | `exec` |
| [deprecate.js](../../../opt/hatch-image/bin/npm-package/lib/commands/deprecate.js) | Deprecate a version of a package | `BaseCommand` | `completion`, `exec` |
| [diff.js](../../../opt/hatch-image/bin/npm-package/lib/commands/diff.js) | The registry diff command | `BaseCommand` | `exec`, `execWorkspaces`, `packageName`, `retrieveSpecs`, `convertVersionsToSpecs`, `findVersionsByPackageName` |
| [dist-tag.js](../../../opt/hatch-image/bin/npm-package/lib/commands/dist-tag.js) | Modify package distribution tags | `BaseCommand` | `completion`, `exec`, `execWorkspaces`, `add`, `remove`, `list`, `listWorkspaces`, `fetchTags` |
| [docs.js](../../../opt/hatch-image/bin/npm-package/lib/commands/docs.js) | Open documentation for a package in a web browser | `PackageUrlCmd` | `getUrl` |
| [doctor.js](../../../opt/hatch-image/bin/npm-package/lib/commands/doctor.js) | Check the health of your npm environment | `BaseCommand` | `if`, `exec`, `checkPing`, `getLatestNpmVersion`, `getLatestNodejsVersion`, `getBinPath`, `checkCachePermission`, `checkLocalModulesPermission`, `checkGlobalModulesPermission`, `checkLocalBinPermission`, `checkGlobalBinPermission`, `checkFilesPermission`, `getGitPath`, `verifyCachedFiles`, `checkNpmRegistry`, `output`, `actions` |
| [edit.js](../../../opt/hatch-image/bin/npm-package/lib/commands/edit.js) | Edit an installed package | `BaseCommand` | `completion`, `exec` |
| [exec.js](../../../opt/hatch-image/bin/npm-package/lib/commands/exec.js) | Run a command from a local or remote npm package | `BaseCommand` | `exec`, `execWorkspaces`, `callExec` |
| [explain.js](../../../opt/hatch-image/bin/npm-package/lib/commands/explain.js) | Explain installed packages | `ArboristWorkspaceCmd` | `completion`, `exec`, `getNodes`, `getNodesByVersion` |
| [explore.js](../../../opt/hatch-image/bin/npm-package/lib/commands/explore.js) | Browse an installed package | `BaseCommand` | `completion`, `exec` |
| [find-dupes.js](../../../opt/hatch-image/bin/npm-package/lib/commands/find-dupes.js) | Find duplication in the package tree | `ArboristWorkspaceCmd` | `exec` |
| [fund.js](../../../opt/hatch-image/bin/npm-package/lib/commands/fund.js) | Retrieve funding information | `ArboristWorkspaceCmd` | `usageMessage`, `completion`, `exec`, `printHuman`, `openFundingUrl`, `urlMessage` |
| [get.js](../../../opt/hatch-image/bin/npm-package/lib/commands/get.js) | Get a value from the npm configuration | `BaseCommand` | `completion`, `exec` |
| [help-search.js](../../../opt/hatch-image/bin/npm-package/lib/commands/help-search.js) | Search npm help documentation | `BaseCommand` | `exec`, `readFiles`, `searchFiles`, `formatResults` |
| [help.js](../../../opt/hatch-image/bin/npm-package/lib/commands/help.js) | Get help on npm | `BaseCommand` | `completion`, `exec`, `helpSearch`, `viewMan`, `htmlMan` |
| [hook.js](../../../opt/hatch-image/bin/npm-package/lib/commands/hook.js) | Manage registry hooks | `BaseCommand` | `exec`, `add`, `ls`, `rm`, `update`, `hookName` |
| [init.js](../../../opt/hatch-image/bin/npm-package/lib/commands/init.js) | Create a package.json file | `BaseCommand` | `exec`, `execWorkspaces`, `execCreate`, `template`, `setWorkspace`, `update` |
| [install-ci-test.js](../../../opt/hatch-image/bin/npm-package/lib/commands/install-ci-test.js) | Install a project with a clean slate and run tests | `CI` | `exec` |
| [install-test.js](../../../opt/hatch-image/bin/npm-package/lib/commands/install-test.js) | Install package(s) and run tests | `Install` | `exec` |
| [install.js](../../../opt/hatch-image/bin/npm-package/lib/commands/install.js) | Install a package | `ArboristWorkspaceCmd` | `completion`, `exec` |
| [link.js](../../../opt/hatch-image/bin/npm-package/lib/commands/link.js) | Symlink a package folder | `ArboristWorkspaceCmd` | `completion`, `exec`, `linkInstall`, `linkPkg`, `missingArgsFromTree` |
| [ll.js](../../../opt/hatch-image/bin/npm-package/lib/commands/ll.js) | 描述来自继承或运行时构造，见源码 | `LS` | `exec` |
| [login.js](../../../opt/hatch-image/bin/npm-package/lib/commands/login.js) | Login to a registry user account | `BaseCommand` | `exec` |
| [logout.js](../../../opt/hatch-image/bin/npm-package/lib/commands/logout.js) | Log out of the registry | `BaseCommand` | `exec` |
| [ls.js](../../../opt/hatch-image/bin/npm-package/lib/commands/ls.js) | List installed packages | `ArboristWorkspaceCmd` | `completion`, `exec`, `initTree`, `if`, `for` |
| [org.js](../../../opt/hatch-image/bin/npm-package/lib/commands/org.js) | Manage orgs | `BaseCommand` | `completion`, `exec`, `set`, `rm`, `ls` |
| [outdated.js](../../../opt/hatch-image/bin/npm-package/lib/commands/outdated.js) | Check for outdated packages | `ArboristWorkspaceCmd` | `exec` |
| [owner.js](../../../opt/hatch-image/bin/npm-package/lib/commands/owner.js) | Manage package owners | `BaseCommand` | `completion`, `exec`, `execWorkspaces`, `ls`, `getPkg`, `changeOwners` |
| [pack.js](../../../opt/hatch-image/bin/npm-package/lib/commands/pack.js) | Create a tarball from a package | `BaseCommand` | `exec`, `execWorkspaces` |
| [ping.js](../../../opt/hatch-image/bin/npm-package/lib/commands/ping.js) | Ping npm registry | `BaseCommand` | `exec` |
| [pkg.js](../../../opt/hatch-image/bin/npm-package/lib/commands/pkg.js) | Manages your package.json | `BaseCommand` | `exec`, `execWorkspaces`, `get`, `set`, `delete` |
| [prefix.js](../../../opt/hatch-image/bin/npm-package/lib/commands/prefix.js) | Display prefix | `BaseCommand` | `exec` |
| [profile.js](../../../opt/hatch-image/bin/npm-package/lib/commands/profile.js) | Change settings on your registry profile | `BaseCommand` | `completion`, `exec`, `get`, `set`, `enable2fa`, `disable2fa` |
| [prune.js](../../../opt/hatch-image/bin/npm-package/lib/commands/prune.js) | Remove extraneous packages | `ArboristWorkspaceCmd` | `exec` |
| [publish.js](../../../opt/hatch-image/bin/npm-package/lib/commands/publish.js) | Publish a package | `BaseCommand` | `exec`, `execWorkspaces` |
| [query.js](../../../opt/hatch-image/bin/npm-package/lib/commands/query.js) | Retrieve a filtered list of packages | `BaseCommand` | `constructor`, `exec`, `execWorkspaces` |
| [rebuild.js](../../../opt/hatch-image/bin/npm-package/lib/commands/rebuild.js) | Rebuild a package | `ArboristWorkspaceCmd` | `completion`, `exec`, `isNode` |
| [repo.js](../../../opt/hatch-image/bin/npm-package/lib/commands/repo.js) | Open package repository page in the browser | `PackageUrlCmd` | `getUrl` |
| [restart.js](../../../opt/hatch-image/bin/npm-package/lib/commands/restart.js) | Restart a package | `LifecycleCmd` |  |
| [root.js](../../../opt/hatch-image/bin/npm-package/lib/commands/root.js) | Display npm root | `BaseCommand` | `exec` |
| [run-script.js](../../../opt/hatch-image/bin/npm-package/lib/commands/run-script.js) | Run arbitrary package scripts | `BaseCommand` | `completion`, `exec`, `execWorkspaces` |
| [sbom.js](../../../opt/hatch-image/bin/npm-package/lib/commands/sbom.js) | Generate a Software Bill of Materials (SBOM) | `BaseCommand` | `exec`, `execWorkspaces`, `for` |
| [search.js](../../../opt/hatch-image/bin/npm-package/lib/commands/search.js) | Search for packages | `BaseCommand` | `exec` |
| [set.js](../../../opt/hatch-image/bin/npm-package/lib/commands/set.js) | Set a value in the npm configuration | `BaseCommand` | `completion`, `exec` |
| [shrinkwrap.js](../../../opt/hatch-image/bin/npm-package/lib/commands/shrinkwrap.js) | Lock down dependency versions for publication | `BaseCommand` | `exec` |
| [star.js](../../../opt/hatch-image/bin/npm-package/lib/commands/star.js) | Mark your favorite packages | `BaseCommand` | `exec` |
| [stars.js](../../../opt/hatch-image/bin/npm-package/lib/commands/stars.js) | View packages marked as favorites | `BaseCommand` | `exec` |
| [start.js](../../../opt/hatch-image/bin/npm-package/lib/commands/start.js) | Start a package | `LifecycleCmd` |  |
| [stop.js](../../../opt/hatch-image/bin/npm-package/lib/commands/stop.js) | Stop a package | `LifecycleCmd` |  |
| [team.js](../../../opt/hatch-image/bin/npm-package/lib/commands/team.js) | Manage organization teams and team memberships | `BaseCommand` | `completion`, `exec`, `create`, `destroy`, `add`, `rm`, `listUsers`, `listTeams` |
| [test.js](../../../opt/hatch-image/bin/npm-package/lib/commands/test.js) | Test a package | `LifecycleCmd` |  |
| [token.js](../../../opt/hatch-image/bin/npm-package/lib/commands/token.js) | Manage your authentication tokens | `BaseCommand` | `completion`, `exec`, `list`, `rm`, `create`, `invalidCIDRError`, `generateTokenIds`, `validateCIDRList` |
| [uninstall.js](../../../opt/hatch-image/bin/npm-package/lib/commands/uninstall.js) | Remove a package | `ArboristWorkspaceCmd` | `completion`, `exec` |
| [unpublish.js](../../../opt/hatch-image/bin/npm-package/lib/commands/unpublish.js) | Remove a package from the registry | `BaseCommand` | `getKeysOfVersions`, `completion`, `exec`, `execWorkspaces` |
| [unstar.js](../../../opt/hatch-image/bin/npm-package/lib/commands/unstar.js) | Remove an item from your favorite packages | `Star` |  |
| [update.js](../../../opt/hatch-image/bin/npm-package/lib/commands/update.js) | Update packages | `ArboristWorkspaceCmd` | `completion`, `exec` |
| [version.js](../../../opt/hatch-image/bin/npm-package/lib/commands/version.js) | Bump a package version | `BaseCommand` | `completion`, `exec`, `execWorkspaces`, `change`, `changeWorkspaces`, `list`, `listWorkspaces` |
| [view.js](../../../opt/hatch-image/bin/npm-package/lib/commands/view.js) | View registry info | `BaseCommand` | `completion`, `exec`, `execWorkspaces`, `if` |
| [whoami.js](../../../opt/hatch-image/bin/npm-package/lib/commands/whoami.js) | Display npm username | `BaseCommand` | `exec` |

## 功能分层

| 组件 | 职责与关联 | 迁移判断 |
|---|---|---|
| @npmcli/arborist | 实际/理想依赖树、reify、去重和安装协调 | 属包管理器实现，无需搬进技能路由 |
| @npmcli/config | 选项定义、来源、展开和 CLI 配置 | 可借鉴明确配置优先级，不复制完整 npm 参数系统 |
| pacote / npm-registry-fetch | 解析包来源、取 metadata/tarball、registry 请求 | 保留认证和来源边界；不能把所有 URL 视为可信 |
| cacache / ssri | 内容缓存和完整性摘要 | 摘要校验不等于发行者信任 |
| @npmcli/run-script / promise-spawn / libnpmexec | 生命周期与程序执行、环境/stdio 管理 | 是真实执行边界，文档分析时不调用 |
| node-gyp | 原生扩展编译与平台工具链 | 环境附带能力，不表示技能本身需要编译器 |
| semver / npm-package-arg / validate-npm-package-name | 版本、包规格和名称解析 | 只有产品真正处理 npm 包时才复用 |
| tar / minipass / glob / minimatch | 归档、流处理和文件匹配 | 底层通用依赖；涉及路径与解包的安全不能凭名称认证 |
| proc-log / redact / error utilities | 日志、输出及错误表达 | 保留敏感参数最小输出原则 |

## 全部包实例

职责来自包自己的 description，版本与许可来自本地 manifest，均是声明。许可需要结合该包 LICENSE 文件，而非仅靠这张表决定再分发权利。dist 下只有 type 的 package.json 另列，不能算独立包。

| 包与路径 | 版本 | 许可声明 | 声明职责 |
|---|---|---|---|
| [ansi-regex](../../../opt/hatch-image/bin/npm-package/node_modules/@isaacs/cliui/node_modules/ansi-regex/package.json) | `6.1.0` | MIT | Regular expression for matching ANSI escape codes |
| [emoji-regex](../../../opt/hatch-image/bin/npm-package/node_modules/@isaacs/cliui/node_modules/emoji-regex/package.json) | `9.2.2` | MIT | A regular expression to match all Emoji-only symbols as per the Unicode Standard. |
| [string-width](../../../opt/hatch-image/bin/npm-package/node_modules/@isaacs/cliui/node_modules/string-width/package.json) | `5.1.2` | MIT | Get the visual width of a string - the number of columns required to display it |
| [strip-ansi](../../../opt/hatch-image/bin/npm-package/node_modules/@isaacs/cliui/node_modules/strip-ansi/package.json) | `7.1.0` | MIT | Strip ANSI escape codes from a string |
| [@isaacs/cliui](../../../opt/hatch-image/bin/npm-package/node_modules/@isaacs/cliui/package.json) | `8.0.2` | ISC | easily create complex multi-column command-line-interfaces |
| [@isaacs/fs-minipass](../../../opt/hatch-image/bin/npm-package/node_modules/@isaacs/fs-minipass/package.json) | `4.0.1` | ISC | fs read and write streams based on minipass |
| [@isaacs/string-locale-compare](../../../opt/hatch-image/bin/npm-package/node_modules/@isaacs/string-locale-compare/package.json) | `1.1.0` | ISC | Compare strings with Intl.Collator if available, falling back to String.localeCompare otherwise |
| [@npmcli/agent](../../../opt/hatch-image/bin/npm-package/node_modules/@npmcli/agent/package.json) | `3.0.0` | ISC | the http/https agent used by the npm cli |
| [@npmcli/arborist](../../../opt/hatch-image/bin/npm-package/node_modules/@npmcli/arborist/package.json) | `8.0.1` | ISC | Manage node_modules trees |
| [@npmcli/config](../../../opt/hatch-image/bin/npm-package/node_modules/@npmcli/config/package.json) | `9.0.0` | ISC | Configuration management for the npm cli |
| [@npmcli/fs](../../../opt/hatch-image/bin/npm-package/node_modules/@npmcli/fs/package.json) | `4.0.0` | ISC | filesystem utilities for the npm cli |
| [@npmcli/git](../../../opt/hatch-image/bin/npm-package/node_modules/@npmcli/git/package.json) | `6.0.3` | ISC | a util for spawning git from npm CLI contexts |
| [@npmcli/installed-package-contents](../../../opt/hatch-image/bin/npm-package/node_modules/@npmcli/installed-package-contents/package.json) | `3.0.0` | ISC | Get the list of files installed in a package in node_modules, including bundled dependencies |
| [@npmcli/map-workspaces](../../../opt/hatch-image/bin/npm-package/node_modules/@npmcli/map-workspaces/package.json) | `4.0.2` | ISC | Retrieves a name:pathname Map for a given workspaces config |
| [pacote](../../../opt/hatch-image/bin/npm-package/node_modules/@npmcli/metavuln-calculator/node_modules/pacote/package.json) | `20.0.0` | ISC | JavaScript package downloader |
| [@npmcli/metavuln-calculator](../../../opt/hatch-image/bin/npm-package/node_modules/@npmcli/metavuln-calculator/package.json) | `8.0.1` | ISC | Calculate meta-vulnerabilities from package security advisories |
| [@npmcli/name-from-folder](../../../opt/hatch-image/bin/npm-package/node_modules/@npmcli/name-from-folder/package.json) | `3.0.0` | ISC | Get the package name from a folder path |
| [@npmcli/node-gyp](../../../opt/hatch-image/bin/npm-package/node_modules/@npmcli/node-gyp/package.json) | `4.0.0` | ISC | Tools for dealing with node-gyp packages |
| [@npmcli/package-json](../../../opt/hatch-image/bin/npm-package/node_modules/@npmcli/package-json/package.json) | `6.2.0` | ISC | Programmatic API to update package.json |
| [@npmcli/promise-spawn](../../../opt/hatch-image/bin/npm-package/node_modules/@npmcli/promise-spawn/package.json) | `8.0.2` | ISC | spawn processes the way the npm cli likes to do |
| [@npmcli/query](../../../opt/hatch-image/bin/npm-package/node_modules/@npmcli/query/package.json) | `4.0.1` | ISC | npm query parser and tools |
| [@npmcli/redact](../../../opt/hatch-image/bin/npm-package/node_modules/@npmcli/redact/package.json) | `3.2.2` | ISC | Redact sensitive npm information from output |
| [@npmcli/run-script](../../../opt/hatch-image/bin/npm-package/node_modules/@npmcli/run-script/package.json) | `9.1.0` | ISC | Run a lifecycle script for a package (descendant of npm-lifecycle) |
| [@pkgjs/parseargs](../../../opt/hatch-image/bin/npm-package/node_modules/@pkgjs/parseargs/package.json) | `0.11.0` | MIT | Polyfill of future proposal for `util.parseArgs()` |
| [@sigstore/protobuf-specs](../../../opt/hatch-image/bin/npm-package/node_modules/@sigstore/protobuf-specs/package.json) | `0.4.3` | Apache-2.0 | code-signing for npm packages |
| [@sigstore/tuf](../../../opt/hatch-image/bin/npm-package/node_modules/@sigstore/tuf/package.json) | `3.1.1` | Apache-2.0 | Client for the Sigstore TUF repository |
| [@tufjs/canonical-json](../../../opt/hatch-image/bin/npm-package/node_modules/@tufjs/canonical-json/package.json) | `2.0.0` | MIT | OLPC JSON canonicalization |
| [abbrev](../../../opt/hatch-image/bin/npm-package/node_modules/abbrev/package.json) | `3.0.1` | ISC | Like ruby's abbrev module, but in js |
| [agent-base](../../../opt/hatch-image/bin/npm-package/node_modules/agent-base/package.json) | `7.1.3` | MIT | Turn a function into an `http.Agent` instance |
| [ansi-regex](../../../opt/hatch-image/bin/npm-package/node_modules/ansi-regex/package.json) | `5.0.1` | MIT | Regular expression for matching ANSI escape codes |
| [ansi-styles](../../../opt/hatch-image/bin/npm-package/node_modules/ansi-styles/package.json) | `6.2.1` | MIT | ANSI escape codes for styling strings in the terminal |
| [aproba](../../../opt/hatch-image/bin/npm-package/node_modules/aproba/package.json) | `2.0.0` | ISC | A ridiculously light-weight argument validator (now browser friendly) |
| [archy](../../../opt/hatch-image/bin/npm-package/node_modules/archy/package.json) | `1.0.0` | MIT | render nested hierarchies `npm ls` style with unicode pipes |
| [balanced-match](../../../opt/hatch-image/bin/npm-package/node_modules/balanced-match/package.json) | `1.0.2` | MIT | Match balanced character pairs, like "{" and "}" |
| [bin-links](../../../opt/hatch-image/bin/npm-package/node_modules/bin-links/package.json) | `5.0.0` | ISC | JavaScript package binary linker |
| [binary-extensions](../../../opt/hatch-image/bin/npm-package/node_modules/binary-extensions/package.json) | `2.3.0` | MIT | List of binary file extensions |
| [brace-expansion](../../../opt/hatch-image/bin/npm-package/node_modules/brace-expansion/package.json) | `2.0.2` | MIT | Brace expansion as known from sh/bash |
| [chownr](../../../opt/hatch-image/bin/npm-package/node_modules/cacache/node_modules/chownr/package.json) | `3.0.0` | BlueOak-1.0.0 | like `chown -R` |
| [mkdirp](../../../opt/hatch-image/bin/npm-package/node_modules/cacache/node_modules/mkdirp/dist/cjs/package.json) | `3.0.1` | MIT | Recursively mkdir, like `mkdir -p` |
| [mkdirp](../../../opt/hatch-image/bin/npm-package/node_modules/cacache/node_modules/mkdirp/package.json) | `3.0.1` | MIT | Recursively mkdir, like `mkdir -p` |
| [tar](../../../opt/hatch-image/bin/npm-package/node_modules/cacache/node_modules/tar/package.json) | `7.4.3` | ISC | tar for node |
| [yallist](../../../opt/hatch-image/bin/npm-package/node_modules/cacache/node_modules/yallist/package.json) | `5.0.0` | BlueOak-1.0.0 | Yet Another Linked List |
| [cacache](../../../opt/hatch-image/bin/npm-package/node_modules/cacache/package.json) | `19.0.1` | ISC | Fast, fault-tolerant, cross-platform, disk-based, data-agnostic, content-addressable cache. |
| [chalk](../../../opt/hatch-image/bin/npm-package/node_modules/chalk/package.json) | `5.4.1` | MIT | Terminal string styling done right |
| [chownr](../../../opt/hatch-image/bin/npm-package/node_modules/chownr/package.json) | `2.0.0` | ISC | like `chown -R` |
| [ci-info](../../../opt/hatch-image/bin/npm-package/node_modules/ci-info/package.json) | `4.2.0` | MIT | Get details about the current Continuous Integration environment |
| [cidr-regex](../../../opt/hatch-image/bin/npm-package/node_modules/cidr-regex/package.json) | `4.1.3` | BSD-2-Clause | Regular expression for matching IP addresses in CIDR notation |
| [cli-columns](../../../opt/hatch-image/bin/npm-package/node_modules/cli-columns/package.json) | `4.0.0` | MIT | Columnated lists for the CLI. |
| [cmd-shim](../../../opt/hatch-image/bin/npm-package/node_modules/cmd-shim/package.json) | `7.0.0` | ISC | Used in npm for command line application support |
| [color-convert](../../../opt/hatch-image/bin/npm-package/node_modules/color-convert/package.json) | `2.0.1` | MIT | Plain color conversion functions |
| [color-name](../../../opt/hatch-image/bin/npm-package/node_modules/color-name/package.json) | `1.1.4` | MIT | A list of color names and its values |
| [common-ancestor-path](../../../opt/hatch-image/bin/npm-package/node_modules/common-ancestor-path/package.json) | `1.0.1` | ISC | Find the common ancestor of 2 or more paths on Windows or Unix |
| [which](../../../opt/hatch-image/bin/npm-package/node_modules/cross-spawn/node_modules/which/package.json) | `2.0.2` | ISC | Like which(1) unix command. Find the first instance of an executable in the PATH. |
| [cross-spawn](../../../opt/hatch-image/bin/npm-package/node_modules/cross-spawn/package.json) | `7.0.6` | MIT | Cross platform child_process#spawn and child_process#spawnSync |
| [cssesc](../../../opt/hatch-image/bin/npm-package/node_modules/cssesc/package.json) | `3.0.0` | MIT | A JavaScript library for escaping CSS strings and identifiers while generating the shortest possible ASCII-only output. |
| [debug](../../../opt/hatch-image/bin/npm-package/node_modules/debug/package.json) | `4.4.1` | MIT | Lightweight debugging utility for Node.js and the browser |
| [diff](../../../opt/hatch-image/bin/npm-package/node_modules/diff/package.json) | `5.2.0` | BSD-3-Clause | A JavaScript text diff implementation. |
| [eastasianwidth](../../../opt/hatch-image/bin/npm-package/node_modules/eastasianwidth/package.json) | `0.2.0` | MIT | Get East Asian Width from a character. |
| [emoji-regex](../../../opt/hatch-image/bin/npm-package/node_modules/emoji-regex/package.json) | `8.0.0` | MIT | A regular expression to match all Emoji-only symbols as per the Unicode Standard. |
| [encoding](../../../opt/hatch-image/bin/npm-package/node_modules/encoding/package.json) | `0.1.13` | MIT | Convert encodings, uses iconv-lite |
| [env-paths](../../../opt/hatch-image/bin/npm-package/node_modules/env-paths/package.json) | `2.2.1` | MIT | Get paths for storing things like data, config, cache, etc |
| [err-code](../../../opt/hatch-image/bin/npm-package/node_modules/err-code/package.json) | `2.0.3` | MIT | Create an error with a code |
| [exponential-backoff](../../../opt/hatch-image/bin/npm-package/node_modules/exponential-backoff/package.json) | `3.1.2` | Apache-2.0 | A utility that allows retrying a function with an exponential delay between attempts. |
| [fastest-levenshtein](../../../opt/hatch-image/bin/npm-package/node_modules/fastest-levenshtein/package.json) | `1.0.16` | MIT | Fastest Levenshtein distance implementation in JS. |
| [foreground-child](../../../opt/hatch-image/bin/npm-package/node_modules/foreground-child/package.json) | `3.3.1` | ISC | Run a child as if it's the foreground process. Give it stdio. Exit when it exits. |
| [fs-minipass](../../../opt/hatch-image/bin/npm-package/node_modules/fs-minipass/package.json) | `3.0.3` | ISC | fs read and write streams based on minipass |
| [glob](../../../opt/hatch-image/bin/npm-package/node_modules/glob/package.json) | `10.4.5` | ISC | the most correct and second fastest glob implementation in JavaScript |
| [graceful-fs](../../../opt/hatch-image/bin/npm-package/node_modules/graceful-fs/package.json) | `4.2.11` | ISC | A drop-in replacement for fs, making various improvements. |
| [hosted-git-info](../../../opt/hatch-image/bin/npm-package/node_modules/hosted-git-info/package.json) | `8.1.0` | ISC | Provides metadata and conversions from repository urls for GitHub, Bitbucket and GitLab |
| [http-cache-semantics](../../../opt/hatch-image/bin/npm-package/node_modules/http-cache-semantics/package.json) | `4.2.0` | BSD-2-Clause | Parses Cache-Control and other headers. Helps building correct HTTP caches and proxies |
| [http-proxy-agent](../../../opt/hatch-image/bin/npm-package/node_modules/http-proxy-agent/package.json) | `7.0.2` | MIT | An HTTP(s) proxy `http.Agent` implementation for HTTP |
| [https-proxy-agent](../../../opt/hatch-image/bin/npm-package/node_modules/https-proxy-agent/package.json) | `7.0.6` | MIT | An HTTP(s) proxy `http.Agent` implementation for HTTPS |
| [iconv-lite](../../../opt/hatch-image/bin/npm-package/node_modules/iconv-lite/package.json) | `0.6.3` | MIT | Convert character encodings in pure javascript. |
| [ignore-walk](../../../opt/hatch-image/bin/npm-package/node_modules/ignore-walk/package.json) | `7.0.0` | ISC | Nested/recursive `.gitignore`/`.npmignore` parsing and filtering. |
| [imurmurhash](../../../opt/hatch-image/bin/npm-package/node_modules/imurmurhash/package.json) | `0.1.4` | MIT | An incremental implementation of MurmurHash3 |
| [ini](../../../opt/hatch-image/bin/npm-package/node_modules/ini/package.json) | `5.0.0` | ISC | An ini encoder/decoder for node |
| [init-package-json](../../../opt/hatch-image/bin/npm-package/node_modules/init-package-json/package.json) | `7.0.2` | ISC | A node module to get your node module started |
| [ip-address](../../../opt/hatch-image/bin/npm-package/node_modules/ip-address/package.json) | `9.0.5` | MIT | A library for parsing IPv4 and IPv6 IP addresses in node and the browser. |
| [ip-regex](../../../opt/hatch-image/bin/npm-package/node_modules/ip-regex/package.json) | `5.0.0` | MIT | Regular expression for matching IP addresses (IPv4 & IPv6) |
| [is-cidr](../../../opt/hatch-image/bin/npm-package/node_modules/is-cidr/package.json) | `5.1.1` | BSD-2-Clause | Check if a string is an IP address in CIDR notation |
| [is-fullwidth-code-point](../../../opt/hatch-image/bin/npm-package/node_modules/is-fullwidth-code-point/package.json) | `3.0.0` | MIT | Check if the character represented by a given Unicode code point is fullwidth |
| [isexe](../../../opt/hatch-image/bin/npm-package/node_modules/isexe/package.json) | `2.0.0` | ISC | Minimal module to check if a file is executable. |
| [jackspeak](../../../opt/hatch-image/bin/npm-package/node_modules/jackspeak/package.json) | `3.4.3` | BlueOak-1.0.0 | A very strict and proper argument parser. |
| [jsbn](../../../opt/hatch-image/bin/npm-package/node_modules/jsbn/package.json) | `1.1.0` | MIT | The jsbn library is a fast, portable implementation of large-number math in pure JavaScript, enabling public-key crypto and other applications on desktop and mobile browsers. |
| [json-parse-even-better-errors](../../../opt/hatch-image/bin/npm-package/node_modules/json-parse-even-better-errors/package.json) | `4.0.0` | MIT | JSON.parse with context information on error |
| [json-stringify-nice](../../../opt/hatch-image/bin/npm-package/node_modules/json-stringify-nice/package.json) | `1.1.4` | ISC | Stringify an object sorting scalars before objects, and defaulting to 2-space indent |
| [jsonparse](../../../opt/hatch-image/bin/npm-package/node_modules/jsonparse/package.json) | `1.3.1` | MIT | This is a pure-js JSON streaming parser for node.js |
| [just-diff](../../../opt/hatch-image/bin/npm-package/node_modules/just-diff/package.json) | `6.0.2` | MIT | Return an object representing the diffs between two objects. Supports jsonPatch protocol |
| [just-diff-apply](../../../opt/hatch-image/bin/npm-package/node_modules/just-diff-apply/package.json) | `5.5.0` | MIT | Apply a diff to an object. Optionally supports jsonPatch protocol |
| [libnpmaccess](../../../opt/hatch-image/bin/npm-package/node_modules/libnpmaccess/package.json) | `9.0.0` | ISC | programmatic library for `npm access` commands |
| [libnpmdiff](../../../opt/hatch-image/bin/npm-package/node_modules/libnpmdiff/package.json) | `7.0.1` | ISC | The registry diff |
| [libnpmexec](../../../opt/hatch-image/bin/npm-package/node_modules/libnpmexec/package.json) | `9.0.1` | ISC | npm exec (npx) programmatic API |
| [libnpmfund](../../../opt/hatch-image/bin/npm-package/node_modules/libnpmfund/package.json) | `6.0.1` | ISC | Programmatic API for npm fund |
| [libnpmhook](../../../opt/hatch-image/bin/npm-package/node_modules/libnpmhook/package.json) | `11.0.0` | ISC | programmatic API for managing npm registry hooks |
| [libnpmorg](../../../opt/hatch-image/bin/npm-package/node_modules/libnpmorg/package.json) | `7.0.0` | ISC | Programmatic api for `npm org` commands |
| [libnpmpack](../../../opt/hatch-image/bin/npm-package/node_modules/libnpmpack/package.json) | `8.0.1` | ISC | Programmatic API for the bits behind npm pack |
| [libnpmpublish](../../../opt/hatch-image/bin/npm-package/node_modules/libnpmpublish/package.json) | `10.0.1` | ISC | Programmatic API for the bits behind npm publish and unpublish |
| [libnpmsearch](../../../opt/hatch-image/bin/npm-package/node_modules/libnpmsearch/package.json) | `8.0.0` | ISC | Programmatic API for searching in npm and compatible registries. |
| [libnpmteam](../../../opt/hatch-image/bin/npm-package/node_modules/libnpmteam/package.json) | `7.0.0` | ISC | npm Team management APIs |
| [libnpmversion](../../../opt/hatch-image/bin/npm-package/node_modules/libnpmversion/package.json) | `7.0.0` | ISC | library to do the things that 'npm version' does |
| [lru-cache](../../../opt/hatch-image/bin/npm-package/node_modules/lru-cache/package.json) | `10.4.3` | ISC | A cache object that deletes the least-recently-used items. |
| [negotiator](../../../opt/hatch-image/bin/npm-package/node_modules/make-fetch-happen/node_modules/negotiator/package.json) | `1.0.0` | MIT | HTTP content negotiation |
| [make-fetch-happen](../../../opt/hatch-image/bin/npm-package/node_modules/make-fetch-happen/package.json) | `14.0.3` | ISC | Opinionated, caching, retrying fetch client |
| [minimatch](../../../opt/hatch-image/bin/npm-package/node_modules/minimatch/package.json) | `9.0.5` | ISC | a glob matcher in javascript |
| [minipass](../../../opt/hatch-image/bin/npm-package/node_modules/minipass/package.json) | `7.1.2` | ISC | minimal implementation of a PassThrough stream |
| [minipass-collect](../../../opt/hatch-image/bin/npm-package/node_modules/minipass-collect/package.json) | `2.0.1` | ISC | A Minipass stream that collects all the data into a single chunk |
| [minipass-fetch](../../../opt/hatch-image/bin/npm-package/node_modules/minipass-fetch/package.json) | `4.0.1` | MIT | An implementation of window.fetch in Node.js using Minipass streams |
| [minipass](../../../opt/hatch-image/bin/npm-package/node_modules/minipass-flush/node_modules/minipass/package.json) | `3.3.6` | ISC | minimal implementation of a PassThrough stream |
| [minipass-flush](../../../opt/hatch-image/bin/npm-package/node_modules/minipass-flush/package.json) | `1.0.5` | ISC | A Minipass stream that calls a flush function before emitting 'end' |
| [minipass](../../../opt/hatch-image/bin/npm-package/node_modules/minipass-pipeline/node_modules/minipass/package.json) | `3.3.6` | ISC | minimal implementation of a PassThrough stream |
| [minipass-pipeline](../../../opt/hatch-image/bin/npm-package/node_modules/minipass-pipeline/package.json) | `1.2.4` | ISC | create a pipeline of streams using Minipass |
| [minipass](../../../opt/hatch-image/bin/npm-package/node_modules/minipass-sized/node_modules/minipass/package.json) | `3.3.6` | ISC | minimal implementation of a PassThrough stream |
| [minipass-sized](../../../opt/hatch-image/bin/npm-package/node_modules/minipass-sized/package.json) | `1.0.3` | ISC | A Minipass stream that raises an error if you get a different number of bytes than expected |
| [minizlib](../../../opt/hatch-image/bin/npm-package/node_modules/minizlib/package.json) | `3.0.2` | MIT | A small fast zlib stream built on [minipass](http://npm.im/minipass) and Node.js's zlib binding. |
| [mkdirp](../../../opt/hatch-image/bin/npm-package/node_modules/mkdirp/package.json) | `1.0.4` | MIT | Recursively mkdir, like `mkdir -p` |
| [ms](../../../opt/hatch-image/bin/npm-package/node_modules/ms/package.json) | `2.1.3` | MIT | Tiny millisecond conversion utility |
| [mute-stream](../../../opt/hatch-image/bin/npm-package/node_modules/mute-stream/package.json) | `2.0.0` | ISC | Bytes go in, but they don't come out (when muted). |
| [chownr](../../../opt/hatch-image/bin/npm-package/node_modules/node-gyp/node_modules/chownr/package.json) | `3.0.0` | BlueOak-1.0.0 | like `chown -R` |
| [mkdirp](../../../opt/hatch-image/bin/npm-package/node_modules/node-gyp/node_modules/mkdirp/dist/cjs/package.json) | `3.0.1` | MIT | Recursively mkdir, like `mkdir -p` |
| [mkdirp](../../../opt/hatch-image/bin/npm-package/node_modules/node-gyp/node_modules/mkdirp/package.json) | `3.0.1` | MIT | Recursively mkdir, like `mkdir -p` |
| [tar](../../../opt/hatch-image/bin/npm-package/node_modules/node-gyp/node_modules/tar/package.json) | `7.4.3` | ISC | tar for node |
| [yallist](../../../opt/hatch-image/bin/npm-package/node_modules/node-gyp/node_modules/yallist/package.json) | `5.0.0` | BlueOak-1.0.0 | Yet Another Linked List |
| [node-gyp](../../../opt/hatch-image/bin/npm-package/node_modules/node-gyp/package.json) | `11.2.0` | MIT | Node.js native addon build tool |
| [nopt](../../../opt/hatch-image/bin/npm-package/node_modules/nopt/package.json) | `8.1.0` | ISC | Option parsing for Node, supporting types, shorthands, etc. Used by npm. |
| [normalize-package-data](../../../opt/hatch-image/bin/npm-package/node_modules/normalize-package-data/package.json) | `7.0.0` | BSD-2-Clause | Normalizes data that can be found in package.json files. |
| [npm-audit-report](../../../opt/hatch-image/bin/npm-package/node_modules/npm-audit-report/package.json) | `6.0.0` | ISC | Given a response from the npm security api, render it into a variety of security reports |
| [npm-bundled](../../../opt/hatch-image/bin/npm-package/node_modules/npm-bundled/package.json) | `4.0.0` | ISC | list things in node_modules that are bundledDependencies, or transitive dependencies thereof |
| [npm-install-checks](../../../opt/hatch-image/bin/npm-package/node_modules/npm-install-checks/package.json) | `7.1.1` | BSD-2-Clause | Check the engines and platform fields in package.json |
| [npm-normalize-package-bin](../../../opt/hatch-image/bin/npm-package/node_modules/npm-normalize-package-bin/package.json) | `4.0.0` | ISC | Turn any flavor of allowable package.json bin into a normalized object |
| [npm-package-arg](../../../opt/hatch-image/bin/npm-package/node_modules/npm-package-arg/package.json) | `12.0.2` | ISC | Parse the things that can be arguments to `npm install` |
| [npm-packlist](../../../opt/hatch-image/bin/npm-package/node_modules/npm-packlist/package.json) | `9.0.0` | ISC | Get a list of the files to add from a folder into an npm package |
| [npm-pick-manifest](../../../opt/hatch-image/bin/npm-package/node_modules/npm-pick-manifest/package.json) | `10.0.0` | ISC | Resolves a matching manifest from a package metadata document according to standard npm semver resolution rules. |
| [npm-profile](../../../opt/hatch-image/bin/npm-package/node_modules/npm-profile/package.json) | `11.0.1` | ISC | Library for updating an npmjs.com profile |
| [npm-registry-fetch](../../../opt/hatch-image/bin/npm-package/node_modules/npm-registry-fetch/package.json) | `18.0.2` | ISC | Fetch-based http client for use with npm registry APIs |
| [npm-user-validate](../../../opt/hatch-image/bin/npm-package/node_modules/npm-user-validate/package.json) | `3.0.0` | BSD-2-Clause | User validations for npm |
| [p-map](../../../opt/hatch-image/bin/npm-package/node_modules/p-map/package.json) | `7.0.3` | MIT | Map over promises concurrently |
| [package-json-from-dist](../../../opt/hatch-image/bin/npm-package/node_modules/package-json-from-dist/package.json) | `1.0.1` | BlueOak-1.0.0 | Load the local package.json from either src or dist folder |
| [pacote](../../../opt/hatch-image/bin/npm-package/node_modules/pacote/package.json) | `19.0.1` | ISC | JavaScript package downloader |
| [parse-conflict-json](../../../opt/hatch-image/bin/npm-package/node_modules/parse-conflict-json/package.json) | `4.0.0` | ISC | Parse a JSON string that has git merge conflicts, resolving if possible |
| [path-key](../../../opt/hatch-image/bin/npm-package/node_modules/path-key/package.json) | `3.1.1` | MIT | Get the PATH environment variable key cross-platform |
| [path-scurry](../../../opt/hatch-image/bin/npm-package/node_modules/path-scurry/package.json) | `1.11.1` | BlueOak-1.0.0 | walk paths fast and efficiently |
| [postcss-selector-parser](../../../opt/hatch-image/bin/npm-package/node_modules/postcss-selector-parser/package.json) | `7.1.0` | MIT | 未声明 |
| [proc-log](../../../opt/hatch-image/bin/npm-package/node_modules/proc-log/package.json) | `5.0.0` | ISC | just emit 'log' events on the process object |
| [proggy](../../../opt/hatch-image/bin/npm-package/node_modules/proggy/package.json) | `3.0.0` | ISC | Progress bar updates at a distance |
| [promise-all-reject-late](../../../opt/hatch-image/bin/npm-package/node_modules/promise-all-reject-late/package.json) | `1.0.1` | ISC | Like Promise.all, but save rejections until all promises are resolved |
| [promise-call-limit](../../../opt/hatch-image/bin/npm-package/node_modules/promise-call-limit/package.json) | `3.0.2` | ISC | Call an array of promise-returning functions, restricting concurrency to a specified limit. |
| [promise-retry](../../../opt/hatch-image/bin/npm-package/node_modules/promise-retry/package.json) | `2.0.1` | MIT | Retries a function that returns a promise, leveraging the power of the retry module. |
| [promzard](../../../opt/hatch-image/bin/npm-package/node_modules/promzard/package.json) | `2.0.0` | ISC | prompting wizardly |
| [qrcode-terminal](../../../opt/hatch-image/bin/npm-package/node_modules/qrcode-terminal/package.json) | `0.12.0` | [{"type": "Apache 2.0"}] | QRCodes, in the terminal |
| [read](../../../opt/hatch-image/bin/npm-package/node_modules/read/package.json) | `4.1.0` | ISC | read(1) for node programs |
| [read-cmd-shim](../../../opt/hatch-image/bin/npm-package/node_modules/read-cmd-shim/package.json) | `5.0.0` | ISC | Figure out what a cmd-shim is pointing at. This acts as the equivalent of fs.readlink. |
| [read-package-json-fast](../../../opt/hatch-image/bin/npm-package/node_modules/read-package-json-fast/package.json) | `4.0.0` | ISC | Like read-package-json, but faster |
| [retry](../../../opt/hatch-image/bin/npm-package/node_modules/retry/package.json) | `0.12.0` | MIT | Abstraction for exponential and custom retry strategies for failed operations. |
| [safer-buffer](../../../opt/hatch-image/bin/npm-package/node_modules/safer-buffer/package.json) | `2.1.2` | MIT | Modern Buffer API polyfill without footguns |
| [semver](../../../opt/hatch-image/bin/npm-package/node_modules/semver/package.json) | `7.7.2` | ISC | The semantic version parser used by npm. |
| [shebang-command](../../../opt/hatch-image/bin/npm-package/node_modules/shebang-command/package.json) | `2.0.0` | MIT | Get the command from a shebang |
| [shebang-regex](../../../opt/hatch-image/bin/npm-package/node_modules/shebang-regex/package.json) | `3.0.0` | MIT | Regular expression for matching a shebang line |
| [signal-exit](../../../opt/hatch-image/bin/npm-package/node_modules/signal-exit/package.json) | `4.1.0` | ISC | when you want to fire an event no matter how a process exits. |
| [@sigstore/bundle](../../../opt/hatch-image/bin/npm-package/node_modules/sigstore/node_modules/@sigstore/bundle/package.json) | `3.1.0` | Apache-2.0 | Sigstore bundle type |
| [@sigstore/core](../../../opt/hatch-image/bin/npm-package/node_modules/sigstore/node_modules/@sigstore/core/package.json) | `2.0.0` | Apache-2.0 | Base library for Sigstore |
| [@sigstore/sign](../../../opt/hatch-image/bin/npm-package/node_modules/sigstore/node_modules/@sigstore/sign/package.json) | `3.1.0` | Apache-2.0 | Sigstore signing library |
| [@sigstore/verify](../../../opt/hatch-image/bin/npm-package/node_modules/sigstore/node_modules/@sigstore/verify/package.json) | `2.1.1` | Apache-2.0 | Verification of Sigstore signatures |
| [sigstore](../../../opt/hatch-image/bin/npm-package/node_modules/sigstore/package.json) | `3.1.0` | Apache-2.0 | code-signing for npm packages |
| [smart-buffer](../../../opt/hatch-image/bin/npm-package/node_modules/smart-buffer/package.json) | `4.2.0` | MIT | smart-buffer is a Buffer wrapper that adds automatic read & write offset tracking, string operations, data insertions, and more. |
| [socks](../../../opt/hatch-image/bin/npm-package/node_modules/socks/package.json) | `2.8.5` | MIT | Fully featured SOCKS proxy client supporting SOCKSv4, SOCKSv4a, and SOCKSv5. Includes Bind and Associate functionality. |
| [socks-proxy-agent](../../../opt/hatch-image/bin/npm-package/node_modules/socks-proxy-agent/package.json) | `8.0.5` | MIT | A SOCKS proxy `http.Agent` implementation for HTTP and HTTPS |
| [spdx-expression-parse](../../../opt/hatch-image/bin/npm-package/node_modules/spdx-correct/node_modules/spdx-expression-parse/package.json) | `3.0.1` | MIT | parse SPDX license expressions |
| [spdx-correct](../../../opt/hatch-image/bin/npm-package/node_modules/spdx-correct/package.json) | `3.2.0` | Apache-2.0 | correct invalid SPDX expressions |
| [spdx-exceptions](../../../opt/hatch-image/bin/npm-package/node_modules/spdx-exceptions/package.json) | `2.5.0` | CC-BY-3.0 | list of SPDX standard license exceptions |
| [spdx-expression-parse](../../../opt/hatch-image/bin/npm-package/node_modules/spdx-expression-parse/package.json) | `4.0.0` | MIT | parse SPDX license expressions |
| [spdx-license-ids](../../../opt/hatch-image/bin/npm-package/node_modules/spdx-license-ids/package.json) | `3.0.21` | CC0-1.0 | A list of SPDX license identifiers |
| [sprintf-js](../../../opt/hatch-image/bin/npm-package/node_modules/sprintf-js/package.json) | `1.1.3` | BSD-3-Clause | JavaScript sprintf implementation |
| [ssri](../../../opt/hatch-image/bin/npm-package/node_modules/ssri/package.json) | `12.0.0` | ISC | Standard Subresource Integrity library -- parses, serializes, generates, and verifies integrity metadata according to the SRI spec. |
| [string-width](../../../opt/hatch-image/bin/npm-package/node_modules/string-width/package.json) | `4.2.3` | MIT | Get the visual width of a string - the number of columns required to display it |
| [string-width](../../../opt/hatch-image/bin/npm-package/node_modules/string-width-cjs/package.json) | `4.2.3` | MIT | Get the visual width of a string - the number of columns required to display it |
| [strip-ansi](../../../opt/hatch-image/bin/npm-package/node_modules/strip-ansi/package.json) | `6.0.1` | MIT | Strip ANSI escape codes from a string |
| [strip-ansi](../../../opt/hatch-image/bin/npm-package/node_modules/strip-ansi-cjs/package.json) | `6.0.1` | MIT | Strip ANSI escape codes from a string |
| [supports-color](../../../opt/hatch-image/bin/npm-package/node_modules/supports-color/package.json) | `9.4.0` | MIT | Detect whether a terminal supports color |
| [minipass](../../../opt/hatch-image/bin/npm-package/node_modules/tar/node_modules/fs-minipass/node_modules/minipass/package.json) | `3.3.6` | ISC | minimal implementation of a PassThrough stream |
| [fs-minipass](../../../opt/hatch-image/bin/npm-package/node_modules/tar/node_modules/fs-minipass/package.json) | `2.1.0` | ISC | fs read and write streams based on minipass |
| [minipass](../../../opt/hatch-image/bin/npm-package/node_modules/tar/node_modules/minipass/package.json) | `5.0.0` | ISC | minimal implementation of a PassThrough stream |
| [minipass](../../../opt/hatch-image/bin/npm-package/node_modules/tar/node_modules/minizlib/node_modules/minipass/package.json) | `3.3.6` | ISC | minimal implementation of a PassThrough stream |
| [minizlib](../../../opt/hatch-image/bin/npm-package/node_modules/tar/node_modules/minizlib/package.json) | `2.1.2` | MIT | A small fast zlib stream built on [minipass](http://npm.im/minipass) and Node.js's zlib binding. |
| [tar](../../../opt/hatch-image/bin/npm-package/node_modules/tar/package.json) | `6.2.1` | ISC | tar for node |
| [text-table](../../../opt/hatch-image/bin/npm-package/node_modules/text-table/package.json) | `0.2.0` | MIT | borderless text tables with alignment |
| [tiny-relative-date](../../../opt/hatch-image/bin/npm-package/node_modules/tiny-relative-date/package.json) | `1.3.0` | MIT | Tiny function that provides relative, human-readable dates. |
| [fdir](../../../opt/hatch-image/bin/npm-package/node_modules/tinyglobby/node_modules/fdir/package.json) | `6.4.6` | MIT | The fastest directory crawler & globbing alternative to glob, fast-glob, & tiny-glob. Crawls 1m files in < 1s |
| [picomatch](../../../opt/hatch-image/bin/npm-package/node_modules/tinyglobby/node_modules/picomatch/package.json) | `4.0.2` | MIT | Blazing fast and accurate glob matcher written in JavaScript, with no dependencies and full support for standard and extended Bash glob features, including braces, extglobs, POSIX brackets, and regular expressions. |
| [tinyglobby](../../../opt/hatch-image/bin/npm-package/node_modules/tinyglobby/package.json) | `0.2.14` | MIT | A fast and minimal alternative to globby and fast-glob |
| [treeverse](../../../opt/hatch-image/bin/npm-package/node_modules/treeverse/package.json) | `3.0.0` | ISC | Walk any kind of tree structure depth- or breadth-first. Supports promises and advanced map-reduce operations with a very small API. |
| [@tufjs/models](../../../opt/hatch-image/bin/npm-package/node_modules/tuf-js/node_modules/@tufjs/models/package.json) | `3.0.1` | MIT | TUF metadata models |
| [tuf-js](../../../opt/hatch-image/bin/npm-package/node_modules/tuf-js/package.json) | `3.0.1` | MIT | JavaScript implementation of The Update Framework (TUF) |
| [unique-filename](../../../opt/hatch-image/bin/npm-package/node_modules/unique-filename/package.json) | `4.0.0` | ISC | Generate a unique filename for use in temporary directories or caches. |
| [unique-slug](../../../opt/hatch-image/bin/npm-package/node_modules/unique-slug/package.json) | `5.0.0` | ISC | Generate a unique character string suitible for use in files and URLs. |
| [util-deprecate](../../../opt/hatch-image/bin/npm-package/node_modules/util-deprecate/package.json) | `1.0.2` | MIT | The Node.js `util.deprecate()` function with browser support |
| [spdx-expression-parse](../../../opt/hatch-image/bin/npm-package/node_modules/validate-npm-package-license/node_modules/spdx-expression-parse/package.json) | `3.0.1` | MIT | parse SPDX license expressions |
| [validate-npm-package-license](../../../opt/hatch-image/bin/npm-package/node_modules/validate-npm-package-license/package.json) | `3.0.4` | Apache-2.0 | Give me a string and I'll tell you if it's a valid npm package license string |
| [validate-npm-package-name](../../../opt/hatch-image/bin/npm-package/node_modules/validate-npm-package-name/package.json) | `6.0.1` | ISC | Give me a string and I'll tell you if it's a valid npm package name |
| [walk-up-path](../../../opt/hatch-image/bin/npm-package/node_modules/walk-up-path/package.json) | `3.0.1` | ISC | Given a path string, return a generator that walks up the path, emitting each dirname. |
| [isexe](../../../opt/hatch-image/bin/npm-package/node_modules/which/node_modules/isexe/package.json) | `3.1.1` | ISC | Minimal module to check if a file is executable. |
| [which](../../../opt/hatch-image/bin/npm-package/node_modules/which/package.json) | `5.0.0` | ISC | Like which(1) unix command. Find the first instance of an executable in the PATH. |
| [ansi-regex](../../../opt/hatch-image/bin/npm-package/node_modules/wrap-ansi/node_modules/ansi-regex/package.json) | `6.1.0` | MIT | Regular expression for matching ANSI escape codes |
| [emoji-regex](../../../opt/hatch-image/bin/npm-package/node_modules/wrap-ansi/node_modules/emoji-regex/package.json) | `9.2.2` | MIT | A regular expression to match all Emoji-only symbols as per the Unicode Standard. |
| [string-width](../../../opt/hatch-image/bin/npm-package/node_modules/wrap-ansi/node_modules/string-width/package.json) | `5.1.2` | MIT | Get the visual width of a string - the number of columns required to display it |
| [strip-ansi](../../../opt/hatch-image/bin/npm-package/node_modules/wrap-ansi/node_modules/strip-ansi/package.json) | `7.1.0` | MIT | Strip ANSI escape codes from a string |
| [wrap-ansi](../../../opt/hatch-image/bin/npm-package/node_modules/wrap-ansi/package.json) | `8.1.0` | MIT | Wordwrap a string with ANSI escape codes |
| [ansi-styles](../../../opt/hatch-image/bin/npm-package/node_modules/wrap-ansi-cjs/node_modules/ansi-styles/package.json) | `4.3.0` | MIT | ANSI escape codes for styling strings in the terminal |
| [wrap-ansi](../../../opt/hatch-image/bin/npm-package/node_modules/wrap-ansi-cjs/package.json) | `7.0.0` | MIT | Wordwrap a string with ANSI escape codes |
| [write-file-atomic](../../../opt/hatch-image/bin/npm-package/node_modules/write-file-atomic/package.json) | `6.0.0` | ISC | Write files in an atomic fashion w/configurable ownership |
| [yallist](../../../opt/hatch-image/bin/npm-package/node_modules/yallist/package.json) | `4.0.0` | ISC | Yet Another Linked List |
| [npm](../../../opt/hatch-image/bin/npm-package/package.json) | `10.9.4` | Artistic-2.0 | a package manager for JavaScript |

## 模块格式配置

这些文件只决定 dist 目录的 CommonJS/ESM 解释方式；不是额外业务模块。

- [opt/hatch-image/bin/npm-package/node_modules/@isaacs/fs-minipass/dist/commonjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/@isaacs/fs-minipass/dist/commonjs/package.json)：`commonjs`。
- [opt/hatch-image/bin/npm-package/node_modules/@isaacs/fs-minipass/dist/esm/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/@isaacs/fs-minipass/dist/esm/package.json)：`module`。
- [opt/hatch-image/bin/npm-package/node_modules/cacache/node_modules/chownr/dist/commonjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/cacache/node_modules/chownr/dist/commonjs/package.json)：`commonjs`。
- [opt/hatch-image/bin/npm-package/node_modules/cacache/node_modules/chownr/dist/esm/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/cacache/node_modules/chownr/dist/esm/package.json)：`module`。
- [opt/hatch-image/bin/npm-package/node_modules/cacache/node_modules/mkdirp/dist/mjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/cacache/node_modules/mkdirp/dist/mjs/package.json)：`module`。
- [opt/hatch-image/bin/npm-package/node_modules/cacache/node_modules/tar/dist/commonjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/cacache/node_modules/tar/dist/commonjs/package.json)：`commonjs`。
- [opt/hatch-image/bin/npm-package/node_modules/cacache/node_modules/tar/dist/esm/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/cacache/node_modules/tar/dist/esm/package.json)：`module`。
- [opt/hatch-image/bin/npm-package/node_modules/cacache/node_modules/yallist/dist/commonjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/cacache/node_modules/yallist/dist/commonjs/package.json)：`commonjs`。
- [opt/hatch-image/bin/npm-package/node_modules/cacache/node_modules/yallist/dist/esm/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/cacache/node_modules/yallist/dist/esm/package.json)：`module`。
- [opt/hatch-image/bin/npm-package/node_modules/foreground-child/dist/commonjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/foreground-child/dist/commonjs/package.json)：`commonjs`。
- [opt/hatch-image/bin/npm-package/node_modules/foreground-child/dist/esm/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/foreground-child/dist/esm/package.json)：`module`。
- [opt/hatch-image/bin/npm-package/node_modules/glob/dist/commonjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/glob/dist/commonjs/package.json)：`commonjs`。
- [opt/hatch-image/bin/npm-package/node_modules/glob/dist/esm/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/glob/dist/esm/package.json)：`module`。
- [opt/hatch-image/bin/npm-package/node_modules/jackspeak/dist/commonjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/jackspeak/dist/commonjs/package.json)：`commonjs`。
- [opt/hatch-image/bin/npm-package/node_modules/jackspeak/dist/esm/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/jackspeak/dist/esm/package.json)：`module`。
- [opt/hatch-image/bin/npm-package/node_modules/lru-cache/dist/commonjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/lru-cache/dist/commonjs/package.json)：`commonjs`。
- [opt/hatch-image/bin/npm-package/node_modules/lru-cache/dist/esm/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/lru-cache/dist/esm/package.json)：`module`。
- [opt/hatch-image/bin/npm-package/node_modules/minimatch/dist/commonjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/minimatch/dist/commonjs/package.json)：`commonjs`。
- [opt/hatch-image/bin/npm-package/node_modules/minimatch/dist/esm/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/minimatch/dist/esm/package.json)：`module`。
- [opt/hatch-image/bin/npm-package/node_modules/minipass/dist/commonjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/minipass/dist/commonjs/package.json)：`commonjs`。
- [opt/hatch-image/bin/npm-package/node_modules/minipass/dist/esm/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/minipass/dist/esm/package.json)：`module`。
- [opt/hatch-image/bin/npm-package/node_modules/minizlib/dist/commonjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/minizlib/dist/commonjs/package.json)：`commonjs`。
- [opt/hatch-image/bin/npm-package/node_modules/minizlib/dist/esm/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/minizlib/dist/esm/package.json)：`module`。
- [opt/hatch-image/bin/npm-package/node_modules/node-gyp/node_modules/chownr/dist/commonjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/node-gyp/node_modules/chownr/dist/commonjs/package.json)：`commonjs`。
- [opt/hatch-image/bin/npm-package/node_modules/node-gyp/node_modules/chownr/dist/esm/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/node-gyp/node_modules/chownr/dist/esm/package.json)：`module`。
- [opt/hatch-image/bin/npm-package/node_modules/node-gyp/node_modules/mkdirp/dist/mjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/node-gyp/node_modules/mkdirp/dist/mjs/package.json)：`module`。
- [opt/hatch-image/bin/npm-package/node_modules/node-gyp/node_modules/tar/dist/commonjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/node-gyp/node_modules/tar/dist/commonjs/package.json)：`commonjs`。
- [opt/hatch-image/bin/npm-package/node_modules/node-gyp/node_modules/tar/dist/esm/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/node-gyp/node_modules/tar/dist/esm/package.json)：`module`。
- [opt/hatch-image/bin/npm-package/node_modules/node-gyp/node_modules/yallist/dist/commonjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/node-gyp/node_modules/yallist/dist/commonjs/package.json)：`commonjs`。
- [opt/hatch-image/bin/npm-package/node_modules/node-gyp/node_modules/yallist/dist/esm/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/node-gyp/node_modules/yallist/dist/esm/package.json)：`module`。
- [opt/hatch-image/bin/npm-package/node_modules/package-json-from-dist/dist/commonjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/package-json-from-dist/dist/commonjs/package.json)：`commonjs`。
- [opt/hatch-image/bin/npm-package/node_modules/package-json-from-dist/dist/esm/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/package-json-from-dist/dist/esm/package.json)：`module`。
- [opt/hatch-image/bin/npm-package/node_modules/path-scurry/dist/commonjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/path-scurry/dist/commonjs/package.json)：`commonjs`。
- [opt/hatch-image/bin/npm-package/node_modules/path-scurry/dist/esm/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/path-scurry/dist/esm/package.json)：`module`。
- [opt/hatch-image/bin/npm-package/node_modules/promise-call-limit/dist/commonjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/promise-call-limit/dist/commonjs/package.json)：`commonjs`。
- [opt/hatch-image/bin/npm-package/node_modules/promise-call-limit/dist/esm/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/promise-call-limit/dist/esm/package.json)：`module`。
- [opt/hatch-image/bin/npm-package/node_modules/read/dist/commonjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/read/dist/commonjs/package.json)：`commonjs`。
- [opt/hatch-image/bin/npm-package/node_modules/read/dist/esm/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/read/dist/esm/package.json)：`module`。
- [opt/hatch-image/bin/npm-package/node_modules/signal-exit/dist/cjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/signal-exit/dist/cjs/package.json)：`commonjs`。
- [opt/hatch-image/bin/npm-package/node_modules/signal-exit/dist/mjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/signal-exit/dist/mjs/package.json)：`module`。
- [opt/hatch-image/bin/npm-package/node_modules/walk-up-path/dist/cjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/walk-up-path/dist/cjs/package.json)：`commonjs`。
- [opt/hatch-image/bin/npm-package/node_modules/walk-up-path/dist/mjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/walk-up-path/dist/mjs/package.json)：`module`。
- [opt/hatch-image/bin/npm-package/node_modules/which/node_modules/isexe/dist/cjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/which/node_modules/isexe/dist/cjs/package.json)：`commonjs`。
- [opt/hatch-image/bin/npm-package/node_modules/which/node_modules/isexe/dist/mjs/package.json](../../../opt/hatch-image/bin/npm-package/node_modules/which/node_modules/isexe/dist/mjs/package.json)：`module`。

## npm/npx 链接

- [opt/hatch-image/bin/npm](../../../opt/hatch-image/bin/npm) → `npm-package/bin/npm-cli.js`。按当前仓库相对路径解析，实际 Node 解释器由调用环境提供。
- [opt/hatch-image/bin/npx](../../../opt/hatch-image/bin/npx) → `npm-package/bin/npx-cli.js`。按当前仓库相对路径解析，实际 Node 解释器由调用环境提供。
