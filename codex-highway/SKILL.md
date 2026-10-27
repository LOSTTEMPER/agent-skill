---
name: codex-highway
description: 为 Codex 配置“codex上高速”项目级 hook，将技能附带的文本文件加载为 developer 上下文，并引导用户完成项目与 hook 信任。用于用户要求启用、更新、检查或停用 codex上高速；仅支持 gpt-5.6-sol。
---

# codex上高速

在用户指定的项目中配置 hook，加载本技能的 `assets/developer-context.md`。只支持 **GPT-5.6 Sol（`gpt-5.6-sol`）**，且必须在**已信任的项目**中使用，同时由用户审阅并信任 hook。

## 附带文件由用户自行审阅

安装、配置、更新或停用技能时，不预读 `assets/developer-context.md` 或项目内 `developer-context.md` 的正文，不把正文放入模型上下文，不摘录、总结或代替用户审阅。不要通过试运行 hook 来提前读取正文。只向用户提供文件路径，请用户自行打开、审阅，并决定是否信任 hook。

配置脚本为复制、比较和备份而进行的本地文件字节读写可以正常执行；不要额外输出正文。此要求只约束配置过程，不改变 hook 在正常触发时读取并输出附带文件的运行逻辑。

## 配置

1. 确定目标项目的绝对路径。若用户正在该项目中要求启用，可使用当前项目；不要把技能目录当成目标项目。支持 macOS / Linux，要求 Python 3.9+ 及支持项目 hook 和 hook 信任的 Codex 客户端。
2. 提醒用户仅在 `gpt-5.6-sol` 下使用。模型要求只作说明，不检查模型，不因为模型不同或未知而拒绝配置、跳过加载或增加运行时限制。
3. 阅读 [README.md](README.md) 中的使用与信任步骤。附带文件是用户维护的内容，不擅自补写。以本技能目录为起点运行：

   ```bash
   python3 scripts/configure.py --project "/目标项目的绝对路径"
   ```

   实际执行时使用脚本的绝对路径，避免依赖当前工作目录。脚本只写目标项目，合并已有 `.codex/hooks.json`，改动前备份被替换文件。若检测到已安装脚本或文本内容不同，会停止；只有用户要求更新时才追加 `--replace`。安装记录不是 hook 已获信任或实际加载的证据。

4. 配置完成后，必须告诉用户：**仅对 5.6 Sol 有效；必须在已信任项目中使用；还需手动信任 hook。**给出目标路径以及下面的操作步骤，不能只说“请信任”。
   - 在目标项目中打开 Codex，确认项目为 trusted；需要时按 README 的项目配置示例操作。
   - 用该项目启动 Codex CLI，输入 `/hooks`，找到目标 `.codex/hooks.json` 中的“codex上高速：加载项目上下文”，由用户自行审阅命令及其读取的文本，再选择信任。
   - 新建 `gpt-5.6-sol` 聊天并发送消息，检查 hook 的执行结果。桌面端没有相应入口时，使用同一主机、同一 Codex 配置目录的 CLI 完成信任，再重新打开项目。
5. 区分“文件已生成”“用户已信任”“客户端已执行”“模型行为符合文本”四种状态。没有相应证据，不宣称已生效。不要替用户写入信任状态或跳过信任审阅。

## 运行、更新和停用

- `UserPromptSubmit` 在每次提交消息时读取项目内的文本，通过 `hookSpecificOutput.additionalContext` 发送给 Codex，由 Codex 加入 developer 上下文。文本是数据，不作为脚本执行；不调用外部模型 API。
- 用户编辑 `assets/developer-context.md` 后，重新运行配置脚本并使用 `--replace` 才会更新项目副本。也可以直接编辑项目的 `.codex/codex-highway/developer-context.md`。
- hook 不检测模型、项目是否受信任、文本长度或内容；每次触发均读取并输出文件。项目与 hook 的信任由 Codex 原生机制管理，技能不自行授予信任。
- 模型或项目变化后使用新聊天；停用不清除旧聊天中已加载的上下文。
- 停用时运行 `scripts/configure.py --project "/目标项目的绝对路径" --remove`。只移除本技能的 hook 条目，保留项目文本与备份；需要恢复旧版本时按 README 操作。
- 运行限制、信任操作和检查方式以 [README.md](README.md) 为准。若客户端缺少所需功能，说明缺项并停止声称可用。
