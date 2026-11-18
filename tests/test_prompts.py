#!/usr/bin/env python3
"""原文保全：已有提示语对上已合并的 main，新帖逐字，路由不悬空，生成物可重放。"""
import hashlib
import importlib.util
import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "32bd33d26ba69cbe715a06a2714ef16aa861a082"
ARCHIVE_SHA = "bb1f3d820a2950cd07b22f5cdff4bd7b17e3d6efec2e60d9d0bab595522ab2f5"
FENCE = re.compile(r"^(`{3,}) ?markdown\n(.*?)^\1[ \t]*$", re.S | re.M)
PATH_LINE = re.compile(r"^`skills/([^/`]+)/([^/`]+)`\s*$", re.M)

# main 在收录这帖之前的 24 段正文 sha256。正文含代码块收尾前的换行。
FROZEN_SHA = {
    "socratic-inquiry": "0c26c9fc2a40f38b30f3f17bbde06ac4f23ea2fa63e4cf10cb984a8efc9185b7",
    "two-layer-explain": "f198789c2ecf31dc6c0f783610ca01c5ce7e6e070c9deb280402331375d5cf59",
    "reverse-teardown": "430c93bb5bc901990cf05d57a3cb523cb05fcfda726d092f57a1ec78a80a4894",
    "horizontal-vertical-analysis": "6ae29824a4b8e80a8a3133a8e0f479f37b9e535972eaa2aca0294cd0b16bd46f",
    "fact-check": "929ede1efa07a98416d0f85d17516dc1c7c1fc8bf6718d12caadbe7cd31f7f17",
    "expert-panel": "e0c03173126a241c8b2825dcbd71dc2850c6e3beedf34da229d648ce4d2a5617",
    "first-principles": "6bb2653bf22565dd0e5bee7cefc9e046ac27d83720ff583909125d66f9477dda",
    "cross-domain-borrow": "16b75550dbe4b6652757d8b8c1174ac9f1fd38f212e1a34db34fbfe9e6878630",
    "steelman-both-sides": "7ea07484bc1e5df92b893c71a56aec5fa47a4d77cf7994a5c58897adbe44dc6e",
    "minimum-experiment": "7724426a605a65598db81bfa582b8c3653a666ea0518e513e1b28b00af603225",
    "parable": "b3a6a795c9de45fda4d711c28007ea64ba2efba5e65e234893f55d42c876cc4b",
    "hidden-talent": "01255e046eb2479af3dfde6d8937d112ccd923943eaea99caa06a9cc16b78f79",
    "life-design": "6bd52d263893643c6761d2d636284ba62926782c3aead1c6ce18cb6fa81635c4",
    "johari-window": "8ba74930d6ccd3f427d2d41707515af2f73dc9c255082ed4fcbfc07634a5ef9f",
    "memory-parable": "2d25567e88c21ff07ea6b635aeced374188f742a03ba285fb3659390e16f6045",
    "no-fluff-output": "854f54763e858a780eb17fa4dca2d1a9e59dc89174c5e3dd15ff555674c52e2d",
    "eli5": "04e1adef320d96e728ba9e4190a67edc28539a0c0907a6c94c4f04f8bd65a137",
    "inversion": "97f36fbb6d33f1716577649da8805c1cb503e994e82e7449661fe859daa56b92",
    "five-whys": "bc53030f62d2ba7e78fbb97f859f333e32f66a0e73a0d20ece034dc60ec2d35b",
    "opportunity-cost": "6296edbcb7785d74681fd2df84627895b75862a04f0d55aadcfa82a4505fc395",
    "traffic-light": "d298ab8927c26d748757e1bac4e70931397cee5841fd2e3a45f43d0d863fab65",
    "cognitive-reappraisal": "8459c4856ebd00d11032c207b5329533cba362e0dc19e8ec1b088c2753d90bb5",
    "implementation-intention": "9ea7879efe64d544c9fa6d7b3ea9d9ba6e3e1879828d28016620560058205d12",
    "self-framing": "1d312b3c40b5b51f3dde26509cb8c5400095d6ad34dc1d91da0d9d06b1620f13",
}

# 帖子序号后的空白按原样写死。第 3 条没有空格，第 10 条是两个空格。
PREFIXES = ["1. ", "2. ", "3.", "4. ", "5. ", "6. ", "7. ", "8. ", "9. ", "10.  "]
NEW_SKILLS = {
    2: "align-then-three",
    3: "challenge-the-question",
    4: "second-order-effects",
    6: "strongest-opponent",
    7: "historical-baggage",
    8: "cognitive-cost",
    9: "slow-pr-review",
    10: "common-cause-retro",
}
MAPPED = {1: "first-principles", 5: "cross-domain-borrow"}
RELAYS = [
    ("align-then-three", "steelman-both-sides", "三版里剩下两个都有道理、分不开"),
    ("align-then-three", "opportunity-cost", "三版还要排先后"),
    ("align-then-three", "carl-idea-king", "选出一版，想先被拆台"),
    ("challenge-the-question", None, "指出来的新问题手上还没答案"),
    ("second-order-effects", "first-principles", "推出来的影响让方案站不住，要重推"),
    ("second-order-effects", "inversion", "影响可接受，但想先列出致命点建防线"),
    ("second-order-effects", "kaz-leader", "影响可接受，开始派活"),
    ("strongest-opponent", "first-principles", "方案被推翻，要重推"),
    ("strongest-opponent", "kaz-leader", "方案扛住了，开始派活"),
    ("historical-baggage", "kaz-leader", "建议移除的部分要交给 agent 落地"),
    ("historical-baggage", "inversion", "移除风险大，想先排雷"),
    ("cognitive-cost", "kaz-leader", "简化方案要交给 agent 落地"),
    ("slow-pr-review", "kaz-leader", "要动手优化"),
    ("slow-pr-review", "matt-diagnosing-bugs", "东西已经在线上变慢，要先复现修好"),
    ("common-cause-retro", "kaz-leader", "要沉淀成规则、自动化或 Skill"),
    ("common-cause-retro", "kaz-neat-freak", "同时发现文档、规则和记忆已经跟代码对不上"),
    ("common-cause-retro", "five-whys", "某一件单独的事故还要往下挖"),
    ("five-whys", "common-cause-retro", "要看的是一段时间里的一批 Bug、返工、回滚，找共同根因"),
]


def load_sync():
    spec = importlib.util.spec_from_file_location("sync", ROOT / "scripts" / "sync.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_vendor():
    spec = importlib.util.spec_from_file_location("vendor", ROOT / "scripts" / "vendor.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fences(text):
    return [body for _fence, body in FENCE.findall(text)]


def git_show(path):
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)


def skill_dirs():
    return sorted(p.parent for p in (ROOT / "skills").rglob("SKILL.md"))


class PromptArchiveTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sync = load_sync()
        cls.vendor = load_vendor()
        cls.archive = (ROOT / "sources" / "khazix-2026-11-16-agent-prompts.txt").read_bytes()
        cls.note = cls.archive.decode("utf-8")
        cls.parts = cls.note.split("\n\n")
        cls.prompts = (ROOT / "sources" / "prompts.md").read_text(encoding="utf-8")
        cls.blocks = fences(cls.prompts)
        cls.paths = PATH_LINE.findall(cls.prompts)
        cls.router = (ROOT / "skills" / "laoyeye" / "SKILL.md").read_text(encoding="utf-8")

    def test_archive_bytes(self):
        self.assertEqual(hashlib.sha256(self.archive).hexdigest(), ARCHIVE_SHA)
        self.assertEqual(len(self.archive), 1908)
        self.assertEqual(len(self.note), 694)
        self.assertFalse(self.archive.endswith(b"\n"))
        self.assertEqual(len(self.parts), 11)
        self.assertEqual(self.parts[0], "翻了一下最近两个月，我用Agent干活最爱说的几句Prompt：")
        self.assertEqual("\n\n".join(self.parts), self.note)

    def test_ten_lines_keep_numbering_and_blanks(self):
        self.assertTrue(self.parts[3].startswith("3.不要"))
        self.assertFalse(self.parts[3].endswith("。"))
        self.assertIn("XX天", self.parts[9])
        self.assertIn("XX时间", self.parts[10])
        self.assertTrue(self.parts[10].startswith("10.  全面复盘"))
        for i, prefix in enumerate(PREFIXES, start=1):
            raw = self.parts[i]
            self.assertTrue(raw.startswith(prefix), raw[:12])
            sentence = raw[len(prefix):]
            self.assertNotIn("\n", sentence)
            if i == 3:
                self.assertTrue(sentence.endswith("直接指出来"))
                self.assertFalse(sentence.endswith("。"))
            if i in (9, 10):
                self.assertNotIn("【", sentence)

    def test_existing_prompt_bodies_match_merged_main(self):
        old_prompts = git_show("sources/prompts.md").decode("utf-8")
        old_blocks = fences(old_prompts)
        old_paths = PATH_LINE.findall(old_prompts)
        self.assertEqual(len(old_blocks), 24)
        self.assertEqual(self.blocks[:24], old_blocks)
        self.assertEqual(self.paths[:24], old_paths)
        for (bucket, name), body in zip(self.paths[:24], self.blocks[:24]):
            self.assertEqual(hashlib.sha256(body.encode()).hexdigest(), FROZEN_SHA[name])
            old_skill = git_show(f"skills/{bucket}/{name}/SKILL.md").decode("utf-8")
            old_fence = fences(old_skill)
            new_fence = fences((ROOT / "skills" / bucket / name / "SKILL.md").read_text(encoding="utf-8"))
            self.assertEqual(len(old_fence), 1)
            self.assertEqual(new_fence, old_fence)
            self.assertEqual(new_fence[0], body)

    def test_new_prompts_are_archive_sentences(self):
        by_name = {name: body for (_bucket, name), body in zip(self.paths, self.blocks)}
        seen = []
        for index, slug in NEW_SKILLS.items():
            sentence = self.parts[index][len(PREFIXES[index - 1]):]
            self.assertEqual(by_name[slug].rstrip("\n"), sentence)
            self.assertTrue(by_name[slug].endswith("\n"))
            skill = next(p for p in skill_dirs() if p.name == slug) / "SKILL.md"
            got = fences(skill.read_text(encoding="utf-8"))
            self.assertEqual(got, [by_name[slug]])
            seen.append(sentence)
        # 第 6 条和第 9 条各留在自己的代码块里，不拼进同一条。
        self.assertEqual(len(seen), 8)
        opponent = by_name["strongest-opponent"]
        slow = by_name["slow-pr-review"]
        self.assertNotIn(slow.strip(), opponent)
        self.assertNotIn(opponent.strip(), slow)

    def test_mapped_oral_lines_stay_out_of_new_skills(self):
        sentences = {i: self.parts[i][len(PREFIXES[i - 1]):] for i in (1, 5)}
        bodies = [body.rstrip("\n") for body in self.blocks]
        for index, slug in MAPPED.items():
            sentence = sentences[index]
            self.assertNotIn(sentence, bodies)
            skill = next(p for p in skill_dirs() if p.name == slug) / "SKILL.md"
            text = skill.read_text(encoding="utf-8")
            fence = fences(text)[0]
            self.assertNotIn(sentence, fence)
            self.assertIn(sentence, text)
            self.assertIn(sentence, self.router)
        self.assertIn("sources/khazix-2026-11-16-agent-prompts.txt", self.router)

    def test_router_skills_exist_and_every_skill_is_routed(self):
        names = {p.name for p in skill_dirs()}
        for name in names - {"laoyeye"}:
            self.assertTrue(
                f"`{name}`" in self.router or f"/{name}" in self.router,
                name,
            )
        for token in re.findall(r"`([^`]+)`", self.router):
            raw = token[1:] if token.startswith("/") else token
            if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", raw):
                self.assertIn(raw, names, token)

    def test_relays_match_notes(self):
        for src, dst, condition in RELAYS:
            if dst is None:
                row = f"| `{src}` → 拿新问题重新对号 | {condition} |"
            else:
                row = f"| `{src}` → `{dst}` | {condition} |"
                self.assertIn(dst, self.sync.NOTES[src])
            self.assertIn(row, self.router)
            self.assertIn(condition, self.sync.NOTES[src])

    def test_counts_and_plugin_list(self):
        catalog = len(self.sync.CATALOG)
        vendored = len(self.vendor.VENDORED)
        self.assertEqual(catalog, 32)
        self.assertEqual(vendored, 7)
        self.assertEqual(catalog + vendored, 39)
        self.assertEqual(len(self.blocks), catalog)
        self.assertIn("全部 39 件", self.router)
        self.assertNotIn("31 件", self.router)
        self.assertIn("32 条提示语", self.router)
        plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        listed = plugin["skills"]
        self.assertEqual(len(listed), 40)
        self.assertEqual(len(skill_dirs()), 40)
        for rel in listed:
            self.assertTrue((ROOT / rel / "SKILL.md").is_file(), rel)
        listed_names = {Path(rel).name for rel in listed}
        self.assertEqual(listed_names, {p.name for p in skill_dirs()})
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        readme_en = (ROOT / "README.en.md").read_text(encoding="utf-8")
        for text in (readme, readme_en):
            self.assertNotIn("31 件", text)
            self.assertNotIn("31 pieces", text)
        self.assertIn("一共 39 件", readme)
        self.assertIn("40 个目录", readme)
        self.assertIn("39 pieces", readme_en)
        self.assertIn("40 new directories", readme_en)

    def test_vendor_tree_untouched(self):
        diff = subprocess.check_output(["git", "diff", "--name-only", BASE, "--", "vendor"], cwd=ROOT)
        self.assertEqual(diff, b"")

    def test_build_is_idempotent(self):
        before = {
            p.relative_to(ROOT): p.read_bytes()
            for p in (ROOT / "skills").rglob("*")
            if p.is_file()
        }
        subprocess.check_call(["python3", "scripts/sync.py", "build"], cwd=ROOT)
        after = {
            p.relative_to(ROOT): p.read_bytes()
            for p in (ROOT / "skills").rglob("*")
            if p.is_file()
        }
        self.assertEqual(before, after)
        subprocess.check_call(["python3", "scripts/sync.py", "verify"], cwd=ROOT)
        subprocess.check_call(["python3", "scripts/vendor.py", "verify"], cwd=ROOT)


if __name__ == "__main__":
    unittest.main()
