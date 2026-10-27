# codex上高速

一个可通过 GitHub 分发的 Codex 技能。启用后，在目标项目中建立 `UserPromptSubmit` hook，每次发送消息时读取附带文本，并通过 Codex 的 `additionalContext` 接口加载到 **developer 上下文**。

**使用要求：仅在 GPT-5.6 Sol（`gpt-5.6-sol`）下使用，且必须在已信任的项目中使用；用户还必须审阅并信任 hook。**

5.6 Sol 是本技能声明的适用范围，不代表 Codex 的 hook 接口只支持该模型。hook 本身不检查模型、不判断项目受信任状态，也不按文本长度或内容跳过加载。项目与 hook 的信任检查由 Codex 原生机制完成。

## 作者先改这个文件

把 [assets/developer-context.md](assets/developer-context.md) 中的占位符换成自己的文本。技能在本仓库中的目录为 `codex-highway/`；只需改这个文件，不用改加载脚本。文件采用 UTF-8 编码。

该文本会进入模型上下文；脚本只读取文本，不把它当程序执行。加载本身不代表模型一定按文本产生某种结果。

## 配置时由用户自行审阅

安装、配置、更新或停用技能时，执行配置的 Codex 不预读附带文件或项目副本的正文，不输出正文，不总结或代替用户审阅，也不通过试运行 hook 提前读取。配置完成后提供文件路径，由用户自行打开并决定是否信任。

配置脚本为复制、比较和备份而进行的本地文件字节读写照常执行，不会打印正文。这个约定不改变 hook 的正常运行逻辑：用户信任后，每次触发仍读取文件并输出到 developer 上下文。

## 安装技能与启用项目 hook

运行环境为 macOS / Linux、Python 3.9+，以及支持项目 hook 和 `/hooks` 信任审阅的 Codex 客户端。Windows 用户可以在 WSL 内使用 WSL 版本的 Codex 与 Python；原生 Windows 命令尚未适配。

### 方式一：让 Codex 配置

1. 将本仓库中的 `codex-highway/` 文件夹安装到你使用的 Codex 技能目录，例如 `~/.codex/skills/codex-highway/`，然后重新打开 Codex。也可让 Codex 从已下载的 `codex-highway/SKILL.md` 执行配置。
2. 在准备启用的项目中，选择 **GPT-5.6 Sol**。
3. 输入：`使用 $codex-highway 为当前项目配置 codex上高速，并告诉我如何信任项目和 hook。`
4. 完成下文的两项信任操作，再新建聊天、发送消息。

### 方式二：直接配置，不安装技能

下载或克隆仓库后，运行以下命令，把路径换成实际位置：

```bash
python3 "/下载位置/codex-highway/scripts/configure.py" --project "/你的项目绝对路径"
```

脚本会创建或合并下面的项目文件：

```text
你的项目/
└── .codex/
    ├── hooks.json
    └── codex-highway/
        ├── load_context.py
        ├── developer-context.md
        └── backups/               # 替换已有文件时才创建
```

项目中的文本是技能附带文件的副本，因此项目启用后不依赖技能的原始下载目录。hook 命令使用配置时 Python 解释器及项目脚本的绝对路径；移动项目或删除该 Python 解释器后，需要重新运行配置。

脚本保留其他事件与 hook，只管理带有 `codex上高速：加载项目上下文` 标识的 command handler。若已有文件与分发文件内容不同，会先停止并说明；重复配置相同内容不会重复添加 hook。

## 必须完成的两项信任操作

### 1. 信任目标项目

在目标项目打开 Codex，如果出现项目是否可信的提示，审阅项目后选择信任。项目必须为 trusted，Codex 才会加载该项目的 `.codex/` 配置。

也可以手动检查用户级配置文件：默认是 `~/.codex/config.toml`；自定义了 `CODEX_HOME` 时使用该目录下的 `config.toml`。备份后，在文件中合并或更新对应项目条目，不要重复添加同名 TOML 表：

```toml
[projects."/你的项目绝对路径"]
trust_level = "trusted"
```

这一步由用户操作。项目路径应使用实际绝对路径，不能把上面的示例原样照抄。

### 2. 审阅并信任 hook

1. 在终端进入目标项目，用 5.6 Sol 启动 Codex：

   ```bash
   codex -C "/你的项目绝对路径" -m gpt-5.6-sol
   ```

2. 在 **Codex 聊天输入框**中输入 `/hooks`；它不是终端 shell 命令。
3. 找到来源为该项目 `.codex/hooks.json`、状态文字为 **codex上高速：加载项目上下文** 的 hook。
4. 由你自行查看执行命令、打开项目的 `load_context.py` 与 `developer-context.md`，确认内容符合预期，再在 hook 审阅界面选择信任。执行配置的 Codex 不代你预读附带正文。不同客户端版本的按钮文字可能不同。
5. 重新打开项目并新建 5.6 Sol 聊天，发送一条消息，让 `UserPromptSubmit` 触发。

如果桌面端没有 hook 审阅入口，可在同一台主机、使用同一 `CODEX_HOME` 的 Codex CLI 中完成，再重新打开桌面端项目。远程环境需要在实际运行 hook 的主机上配置。客户端没有 `/hooks` 时，先使用支持此功能的版本。

项目受信任与 hook 受信任是两项操作。新建或更改 hook 定义后，Codex 可能要求重新审阅；请按实际提示处理。

## 修改、停用与恢复

**修改项目文本：**直接编辑项目的 `.codex/codex-highway/developer-context.md`。下一次发送消息时，hook 会重新读取。空文件也会原样作为空上下文输出；文件缺失或编码错误会报告执行错误。

**把分发版本同步到项目：**修改仓库中的 `assets/developer-context.md` 后，运行：

```bash
python3 "/下载位置/codex-highway/scripts/configure.py" --project "/你的项目绝对路径" --replace
```

`--replace` 会用分发版脚本及文本替换不同的项目副本，替换前自动备份。现有自定义文本会先进入 `.codex/codex-highway/backups/时间戳/`。不要把这个选项当作只检查配置的操作。

**停用：**

```bash
python3 "/下载位置/codex-highway/scripts/configure.py" --project "/你的项目绝对路径" --remove
```

只移除本技能的 hook 条目，保留文本与备份。已经进入旧聊天的上下文不会被撤回，停用或换模型后应新建聊天。

**恢复：**从脚本输出的备份目录，按文件名恢复相应文件。恢复 `hooks.json` 前先比对当前配置，保留备份之后新增的其他 hook；恢复定义后重新检查 `/hooks` 是否需要信任。

## 检查是否工作

- 文件配置：目标项目存在上述文件，`hooks.json` 包含本技能的 `UserPromptSubmit` 条目。
- 客户端执行：项目与 hook 均已信任，发送消息后查看客户端提供的 hook 执行结果及错误提示。
- 加载效果：可暂时在项目文本中加入一个独特的测试短语，在新建的 5.6 Sol 聊天中检验预期行为，再还原文本。模型复述短语只能作为观察结果，不单独证明消息角色。

仓库自带的脚本测试只在临时目录验证配置、合并、备份和输出协议，不授予信任、不启动模型请求。执行：

```bash
python3 -m unittest discover -s tests -v
```

`additionalContextLimit` 配为 `0`，让 Codex 直接接收完整附带文本。hook 不添加长度限制；实际可接受的上下文仍取决于客户端和模型能力。

## 官方依据

- [Hooks](https://learn.chatgpt.com/docs/hooks)：项目 hook、信任审阅、`UserPromptSubmit` 及 developer 上下文输出协议。
- [配置参考](https://learn.chatgpt.com/docs/config-file/config-reference)：`projects.<path>.trust_level`。
- [GPT-5.6 Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol)：模型名称。

本文的流程依据 2026-10-27 查阅的官方文档；未在用户真实项目中安装或执行验收。
