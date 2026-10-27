#!/usr/bin/env python3
"""Installed at <project>/.codex/codex-highway/load_context.py."""

import json
from pathlib import Path
import sys

def main():
    # Model and project requirements are documented, not enforced by this hook.
    sys.stdin.read()  # Consume the event without using it to gate loading.
    context_path = Path(__file__).resolve().with_name("developer-context.md")
    context = context_path.read_text(encoding="utf-8-sig")
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (OSError, UnicodeError) as error:
        print("codex上高速：读取 developer-context.md 失败：" + str(error), file=sys.stderr)
        sys.exit(1)
