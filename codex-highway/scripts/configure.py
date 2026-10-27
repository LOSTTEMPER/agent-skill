#!/usr/bin/env python3
"""Configure only a specified project's hook; never grant trust or install skills."""

import argparse
import copy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shlex
import shutil
import sys
import tempfile

STATUS = "codex上高速：加载项目上下文"
PACKAGE = Path(__file__).resolve().parents[1]


def read_config(path):
    if not path.exists():
        return {}
    config = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError("hooks.json 顶层必须是对象")
    hooks = config.get("hooks", {})
    if not isinstance(hooks, dict):
        raise ValueError("hooks 必须是对象")
    groups = hooks.get("UserPromptSubmit", [])
    if not isinstance(groups, list):
        raise ValueError("UserPromptSubmit 必须是数组")
    for group in groups:
        if not isinstance(group, dict) or not isinstance(group.get("hooks"), list):
            raise ValueError("UserPromptSubmit 分组格式不正确")
        if not all(isinstance(handler, dict) for handler in group["hooks"]):
            raise ValueError("hook handler 必须是对象")
    return config


def is_ours(handler):
    return handler.get("type") == "command" and handler.get("statusMessage") == STATUS


def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".codex-highway-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(content)
        if path.exists():
            os.chmod(temporary, path.stat().st_mode & 0o777)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def configure(args):
    project = Path(args.project).expanduser().resolve(strict=True)
    if not project.is_dir():
        raise ValueError("目标必须是已存在的项目目录")
    if os.name != "posix":
        raise ValueError("此版本支持 macOS / Linux；Windows 请使用 WSL 内的 Codex 和 Python")
    destination = project / ".codex" / "codex-highway"
    config_path = project / ".codex" / "hooks.json"
    # Avoid unexpectedly modifying a different project's linked configuration.
    for path in (project / ".codex", destination, config_path,
                 destination / "load_context.py", destination / "developer-context.md",
                 destination / "backups"):
        if path.is_symlink():
            raise ValueError("目标包含符号链接，请先明确实际项目位置：" + str(path))

    previous = read_config(config_path)
    config = copy.deepcopy(previous)
    hooks = config.setdefault("hooks", {})
    groups = hooks.setdefault("UserPromptSubmit", [])
    retained = []
    for group in groups:
        remaining = [h for h in group["hooks"] if not is_ours(h)]
        if len(remaining) == len(group["hooks"]):
            retained.append(group)
        elif remaining:
            retained.append({**group, "hooks": remaining})

    writes = {}
    if not args.remove:
        command = " ".join(shlex.quote(str(p)) for p in (
            Path(sys.executable).resolve(), destination / "load_context.py"))
        retained.append({"hooks": [{
            "type": "command", "command": command, "timeout": 10,
            "statusMessage": STATUS, "additionalContextLimit": 0,
        }]})
        for source, target in (
            (PACKAGE / "scripts" / "load_context.py", destination / "load_context.py"),
            (PACKAGE / "assets" / "developer-context.md", destination / "developer-context.md"),
        ):
            content = source.read_bytes()
            if target.exists():
                if target.read_bytes() == content:
                    continue
                if not args.replace:
                    raise ValueError("已安装文件内容不同，未作修改；更新请使用 --replace：" + str(target))
            writes[target] = content
    hooks["UserPromptSubmit"] = retained
    if not retained:
        hooks.pop("UserPromptSubmit", None)
    if not hooks:
        config.pop("hooks", None)
    if config != previous:
        writes[config_path] = (json.dumps(config, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

    backup = None
    existing = [path for path in writes if path.exists()]
    if existing:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
        backup = destination / "backups" / stamp
        backup.mkdir(parents=True, exist_ok=False)
        for path in existing:
            shutil.copy2(path, backup / path.name)
    # Payload and runner first; the hook definition is activated last.
    for path, content in writes.items():
        atomic_write(path, content)

    print("项目：", project)
    print("结果：", "已移除本技能的 hook 条目，保留文本与备份。" if args.remove else
          "项目 hook 配置已就绪。" if writes else "已是相同配置，无需改动。")
    if backup:
        print("备份：", backup)
    if not args.remove:
        print("文本：", destination / "developer-context.md")
        print("仅对 5.6 Sol（gpt-5.6-sol）有效，必须在已信任项目中使用。")
        print("下一步：在此项目的 Codex CLI 中输入 /hooks，审阅并手动信任“" + STATUS + "”。")
        print("信任后请新建 gpt-5.6-sol 聊天并发送消息；配置成功不等于已实际加载。")


def main():
    parser = argparse.ArgumentParser(description="配置 codex上高速项目 hook；不安装技能、不授予信任。")
    parser.add_argument("--project", required=True, help="目标项目路径")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--replace", action="store_true", help="备份后更新已存在的脚本及文本")
    mode.add_argument("--remove", action="store_true", help="移除本技能 hook 条目，保留文件")
    args = parser.parse_args()
    try:
        configure(args)
    except (OSError, ValueError) as error:
        print("未完成配置：" + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
