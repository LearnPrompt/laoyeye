#!/usr/bin/env python3
"""老师们的 skill 收录与校验。

vendor/ 下是上游的 pristine 副本，钉在具体 commit 上，一个字节都不许改。
build   把它们生成到 skills/ 下，只做 PATCHES 里声明过的那几处改名。
verify  两道关：vendor/ 的 sha256 对不对得上 vendor.lock.json；skills/ 下的成品能不能从
        vendor/ 原样重放出来。任何手改都会被抓住。
pull    重新从上游拉一遍，报告上游是不是动了（要联网）。
"""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENDOR = ROOT / "vendor"
LOCK = VENDOR / "vendor.lock.json"
SKILLS = ROOT / "skills"

# (bucket, 收录后的名字, vendor 里的目录, 中文名, 一句话, 改名补丁)
# 前缀只为解决重名：上游已经用这个名字发布过，用户可能同时装着两边。
VENDORED = [
    ("asking", "matt-grilling", "mattpocock-skills/skills/productivity/grilling", "拷问 grilling",
     "决策树走空为止的无限拷问，苏格拉底那条最多六问就收，这条不收",
     [("name: grilling", "name: matt-grilling")]),
    ("asking", "matt-grill-me", "mattpocock-skills/skills/productivity/grill-me", "拷问我 grill-me",
     "上面那条的用户唤起版，敲了才出现",
     [("name: grill-me", "name: matt-grill-me"),
      ('Call the Skill tool with "grilling".', 'Call the Skill tool with "matt-grilling".')]),
    ("learning", "matt-teach", "mattpocock-skills/skills/productivity/teach", "教 teach",
     "跨会话把一门东西真学下来，留下课件和速查表，学习那节其余四条都是单次的",
     [("name: teach", "name: matt-teach")]),
    ("solving", "carl-idea-king", "partner-skill/idea-king", "点子王 idea-king",
     "第一性原理拆解加对抗式审查，方案成型之后找人拆台用",
     [("name: idea-king", "name: carl-idea-king")]),
    ("doing", "kaz-leader", "khazix-skills/leader", "领导 leader",
     "把一句话的想法拆成 agent 能独立跑完的任务书",
     [("name: leader", "name: kaz-leader")]),
    ("doing", "kaz-neat-freak", "khazix-skills/neat-freak", "洁癖 neat-freak",
     "干完活跑一下，把文档、规则文件、agent 记忆跟代码真实状态对齐",
     [("name: neat-freak", "name: kaz-neat-freak")]),
]

TEACHERS = {
    "mattpocock-skills": ("Matt Pocock", "https://github.com/mattpocock/skills", "MIT"),
    "khazix-skills": ("数字生命卡兹克", "https://github.com/KKKKhazix/khazix-skills", "MIT"),
    "partner-skill": ("卡尔（本人）", "https://github.com/LearnPrompt/partner-skill", "MIT"),
}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_lock():
    return json.loads(LOCK.read_text(encoding="utf-8"))


def render(src_dir, patches):
    """把一个 vendor 目录重放成成品，返回 {相对路径: bytes}。"""
    out = {}
    base = VENDOR / src_dir
    for f in sorted(base.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(base).as_posix()
        data = f.read_bytes()
        if rel == "SKILL.md":
            text = data.decode("utf-8")
            for old, new in patches:
                if old not in text:
                    sys.exit(f"补丁打不上：{src_dir} 里找不到 {old!r}。上游可能改了，先跑 pull。")
                text = text.replace(old, new)
            data = text.encode("utf-8")
        out[rel] = data
    return out


def build():
    for bucket, name, src, _cn, _one, patches in VENDORED:
        target = SKILLS / bucket / name
        if target.exists():
            shutil.rmtree(target)
        for rel, data in render(src, patches).items():
            p = target / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
            if p.suffix == ".sh":
                p.chmod(0o755)
    print(f"built {len(VENDORED)} vendored skills")


def verify():
    bad = 0
    lock = load_lock()

    for repo, entry in lock["sources"].items():
        for rel, want in entry["files"].items():
            p = VENDOR / repo / rel
            if not p.exists():
                print(f"MISSING  vendor/{repo}/{rel}")
                bad += 1
            elif sha(p) != want:
                print(f"TAMPERED vendor/{repo}/{rel} 跟 vendor.lock.json 对不上")
                bad += 1

    for bucket, name, src, _cn, _one, patches in VENDORED:
        target = SKILLS / bucket / name
        expect = render(src, patches)
        actual = {}
        if target.exists():
            for f in sorted(target.rglob("*")):
                if f.is_file():
                    actual[f.relative_to(target).as_posix()] = f.read_bytes()
        if actual != expect:
            only_e = sorted(set(expect) - set(actual))
            only_a = sorted(set(actual) - set(expect))
            diff = sorted(k for k in set(expect) & set(actual) if expect[k] != actual[k])
            print(f"DRIFT    {bucket}/{name}  缺{only_e or '-'} 多{only_a or '-'} 改{diff or '-'}")
            bad += 1
        else:
            print(f"ok       {bucket}/{name}  ({len(expect)} 个文件，来自 {src})")

    if bad:
        sys.exit(f"\n{bad} 处不一致。老师们的东西不许手改，改 vendor/ 再 build，或者跑 pull 同步上游。")
    print(f"\n{len(VENDORED)} 个收录 skill 与 vendor/ 逐字一致，vendor/ 与 lock 逐字一致。")


def pull():
    lock = load_lock()
    changed = 0
    for repo, entry in lock["sources"].items():
        if not entry.get("raw"):
            print(f"skip     {repo}（本地来源，没有上游 URL）")
            continue
        for rel, want in entry["files"].items():
            url = entry["raw"].replace("{commit}", entry["commit"]) + "/" + rel
            got = subprocess.run(["curl", "-sS", "--max-time", "25", url], capture_output=True).stdout
            now = hashlib.sha256(got).hexdigest()
            if now != want:
                print(f"UPSTREAM {repo}/{rel} 在钉住的 commit 上已经变了（不该发生，检查网络或 URL）")
                changed += 1
    print("上游对照完成" if not changed else f"{changed} 处异常")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "verify"
    {"build": build, "verify": verify, "pull": pull}.get(cmd, lambda: sys.exit("用法: vendor.py build|verify|pull"))()
