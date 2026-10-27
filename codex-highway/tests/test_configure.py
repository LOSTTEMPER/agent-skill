import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


PACKAGE = Path(__file__).resolve().parents[1]
CONFIGURE = PACKAGE / "scripts" / "configure.py"
STATUS = "codex上高速：加载项目上下文"


@unittest.skipUnless(os.name == "posix", "macOS / Linux package")
class ProjectHookTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="codex-highway-test-")
        self.addCleanup(self.temporary.cleanup)
        self.project = Path(self.temporary.name) / "项目 with ' quotes $HOME `printf BAD`"
        self.project.mkdir()
        self.config_path = self.project / ".codex" / "hooks.json"
        self.target = self.project / ".codex" / "codex-highway"

    def configure(self, *flags, expected=0):
        result = subprocess.run(
            [sys.executable, str(CONFIGURE), "--project", str(self.project), *flags],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def read_config(self):
        return json.loads(self.config_path.read_text(encoding="utf-8"))

    def seed(self):
        original = {
            "description": "Keep existing metadata",
            "hooks": {
                "SessionStart": [{"hooks": [{"type": "command", "command": "echo existing"}]}],
                "UserPromptSubmit": [{"hooks": [{"type": "command", "command": "echo other"}]}],
            },
        }
        self.config_path.parent.mkdir(parents=True)
        self.config_path.write_text(json.dumps(original), encoding="utf-8")
        return original

    def runner(self, event=None):
        config = self.read_config()
        handlers = [handler for group in config["hooks"]["UserPromptSubmit"]
                    for handler in group["hooks"] if handler.get("statusMessage") == STATUS]
        self.assertEqual(len(handlers), 1)
        return subprocess.run(
            handlers[0]["command"], shell=True, cwd=self.temporary.name,
            input=json.dumps(event if event is not None else {}),
            text=True, capture_output=True,
        )

    def test_fresh_install_is_idempotent(self):
        self.configure()
        before = self.config_path.read_bytes()
        self.configure()
        self.assertEqual(before, self.config_path.read_bytes())
        self.assertFalse((self.target / "backups").exists())
        self.assertEqual((self.target / "developer-context.md").read_bytes(),
                         (PACKAGE / "assets" / "developer-context.md").read_bytes())

    def test_merge_preserves_other_hooks_and_backs_up_original(self):
        original = self.seed()
        original_bytes = self.config_path.read_bytes()
        self.configure()
        current = self.read_config()
        self.assertEqual(current["description"], original["description"])
        self.assertEqual(current["hooks"]["SessionStart"], original["hooks"]["SessionStart"])
        self.assertEqual(current["hooks"]["UserPromptSubmit"][0],
                         original["hooks"]["UserPromptSubmit"][0])
        backups = list((self.target / "backups").glob("*/hooks.json"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), original_bytes)

    def test_edited_payload_is_not_overwritten_without_replace(self):
        self.configure()
        payload = self.target / "developer-context.md"
        payload.write_text("用户自定义内容", encoding="utf-8")
        before = self.config_path.read_bytes()
        self.configure(expected=1)
        self.assertEqual(payload.read_text(encoding="utf-8"), "用户自定义内容")
        self.assertEqual(before, self.config_path.read_bytes())
        self.assertFalse((self.target / "backups").exists())
        self.configure("--replace")
        backups = list((self.target / "backups").glob("*/developer-context.md"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(encoding="utf-8"), "用户自定义内容")

    def test_hook_outputs_payload_for_any_or_missing_model(self):
        self.configure()
        expected = "测试短语\n\"引号\"与\\字符\n"
        (self.target / "developer-context.md").write_text(expected, encoding="utf-8")
        for event in ({}, {"model": "gpt-5.6-sol"}, {"model": "gpt-6.1-sol"},
                      {"model": None, "cwd": "/outside-project"}):
            with self.subTest(event=event):
                result = self.runner(event)
                self.assertEqual(result.returncode, 0, result.stderr)
                output = json.loads(result.stdout)
                self.assertEqual(output, {"hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit", "additionalContext": expected}})

    def test_hook_has_no_size_or_empty_content_gate(self):
        self.configure()
        for content in ("", "中文长文本" * 10000):
            with self.subTest(length=len(content)):
                (self.target / "developer-context.md").write_text(content, encoding="utf-8")
                result = self.runner()
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"], content)

    def test_missing_payload_reports_error(self):
        self.configure()
        (self.target / "developer-context.md").unlink()
        result = self.runner()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("developer-context.md", result.stderr)

    def test_remove_restores_other_configuration_and_keeps_payload(self):
        original = self.seed()
        self.configure()
        self.configure("--remove")
        self.assertEqual(self.read_config(), original)
        self.assertTrue((self.target / "developer-context.md").exists())
        before = self.config_path.read_bytes()
        self.configure("--remove")
        self.assertEqual(before, self.config_path.read_bytes())

    def test_invalid_configuration_is_left_untouched(self):
        self.config_path.parent.mkdir(parents=True)
        for invalid in (b"not-json", b'[]', b'{"hooks":[]}',
                        b'{"hooks":{"UserPromptSubmit":[{"hooks":[4]}]}}'):
            with self.subTest(invalid=invalid):
                self.config_path.write_bytes(invalid)
                self.configure(expected=1)
                self.assertEqual(self.config_path.read_bytes(), invalid)
                self.assertFalse(self.target.exists())

    def test_symlinked_configuration_is_left_untouched(self):
        outside = Path(self.temporary.name) / "outside.json"
        outside.write_text("{}", encoding="utf-8")
        self.config_path.parent.mkdir(parents=True)
        self.config_path.symlink_to(outside)
        self.configure(expected=1)
        self.assertEqual(outside.read_text(encoding="utf-8"), "{}")

    def test_remove_when_absent_creates_nothing(self):
        self.configure("--remove")
        self.assertFalse((self.project / ".codex").exists())


if __name__ == "__main__":
    unittest.main()
