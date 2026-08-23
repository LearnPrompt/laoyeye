#!/usr/bin/env python3
"""戒指老爷爷（laoyeye）的提示语同步与校验工具。

真理只有一份：sources/prompts.md 里的 12 个代码块。
build   把这 12 段原文灌进各个 SKILL.md。
verify  逐字比对各个 SKILL.md 里的提示语和 sources/prompts.md，有一个字不一样就报错退出 1。
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources" / "prompts.md"
SKILLS = ROOT / "skills"

FENCE = re.compile(r"^``` ?markdown\n(.*?)^```[ \t]*$", re.S | re.M)

# (bucket, dir, 中文名, 一句话, 什么时候用, description, model_invoked, display_name, short_description)
CATALOG = [
    (
        "asking", "socratic-inquiry", "苏格拉底式提问",
        "先别急着要答案，让它把你真正该问的那个问题问出来",
        "嘴上问的和心里想的经常不是一回事。卡在一团乱麻里、说不清自己到底想解决什么的时候，先跑这一条。\n\n它一次只问一个问题，最多六问，最后交给你一个准确、具体、能接着动手的新问题。",
        "苏格拉底式问诊提示语原文。用户说不清自己到底想问什么、问题一团乱、想先把问题问清楚再动手时使用。触发词包括 苏格拉底、苏格拉底式提问、帮我问诊、帮我理清问题、我不知道该问什么、先别给建议、我到底想问什么。一次只问一个问题，最多六问，最后产出一个真正值得回答的新问题。",
        True, "Socratic Inquiry", "Find the question actually worth answering",
    ),
    (
        "learning", "two-layer-explain", "双层解释法",
        "小白版和专业版各讲一遍，别停在好像懂了",
        "只要求讲得通俗，很容易停在类比记住了、机制还是一团雾的阶段。\n\n这一条让它分小白和专家两层各解释一遍，再补上术语对照、易错点和三道自测题。",
        "双层解释法提示语原文。用户遇到听不懂的概念、名词、报错、技术栈，想要一次讲透时使用。触发词包括 双层解释、小白版、专业版、通俗讲一遍、把我当小白、这个概念是什么意思、讲讲什么是。产出小白解释加专业解释，附术语对照表和自测题。",
        True, "Two-Layer Explanation", "Explain it twice, novice then expert",
    ),
    (
        "learning", "reverse-teardown", "反向拆解",
        "看到一个牛逼的成品，把它为什么牛逼拆出来",
        "适合手里有一个优秀范例，网页、产品页、方案、流程、数据看板都行，你想学会它好在哪。\n\n它先说清这东西解决了什么问题，再倒推哪些关键选择拉开了差距，最后给你可复用规律和一个先练的小练习。",
        "反向拆解提示语原文。用户看到一个优秀的产品、网页、方案、流程、数据看板或作品，想学会它为什么有效时使用。触发词包括 反向拆解、拆解这个、它为什么做得好、我想模仿、逆向拆解、复盘这个范例、这个牛在哪。产出可复用规律加一份操作清单。",
        True, "Reverse Teardown", "Break down why a great example works",
    ),
    (
        "learning", "horizontal-vertical-analysis", "横纵分析法",
        "纵轴看它怎么走到今天，横轴看它跟对手差在哪",
        "半小时把一个陌生领域、公司、产品、技术建立起基本框架，配各家的深度研究功能是满血版。\n\n证据规则写得很硬，一手来源优先，事实推断观点分开写，找不到证据就明写暂未核实。报告一万到三万字。",
        "横纵分析法提示语原文。用户想深度研究一个陌生的产品、公司、人物、技术、行业或事件时使用。触发词包括 横纵分析、深度研究、帮我搞懂这家公司、研究一下这个赛道、写份研究报告、纵向历史横向对比、deep research。建议搭配深度研究或联网能力跑，产出一万到三万字可追溯报告。",
        True, "Horizontal-Vertical Analysis", "Deep research along history and rivals",
    ),
    (
        "learning", "fact-check", "事实核查",
        "把事实、推论、价值判断拆开，一条条验",
        "AI 会有幻觉，人的幻觉往往更大。别人的观点、方案、数据，都能拿它过一遍。\n\n它先把说法拆成可验证的事实、从事实推出的结论、藏在里面的价值判断，再分五档标注可信度，最后给一个补强后的版本。",
        "事实核查提示语原文。用户想核实一个说法、观点、结论、数据或方案是否成立时使用。触发词包括 事实核查、帮我核查、这是真的吗、查证一下、有没有幻觉、这个数据靠谱吗、审查这个观点、fact check。需要联网核查，产出五档可信度标注和推理链漏洞。",
        True, "Fact Check", "Split claim into fact, inference, judgement",
    ),
    (
        "solving", "expert-panel", "专家会诊",
        "组一个真正互补的专家团，然后让他们互相质疑",
        "比开头写一句你是拥有二十年经验的世界级专家有用得多，因为很多问题本来就要几个专家配合。\n\n关键那步是互相质疑，真正的信息都藏在分歧里。信息不足时它只问你一个最关键的问题。",
        "专家会诊提示语原文。用户的问题需要多个互补专业视角配合、单一视角给不出好方案时使用。触发词包括 专家会诊、多个视角看看、找几个专家、多学科分析、组个专家团、让他们互相质疑。产出三种互补视角的分歧点和综合方案，含适用条件、最大风险、退出条件。",
        True, "Expert Panel", "Three complementary views that challenge each other",
    ),
    (
        "solving", "first-principles", "第一性原理",
        "别再打补丁了，拆回最底层重新推一遍",
        "最适合处理路径依赖。方案上补丁摞补丁的时候，回到基本事实重新推导，往往比再补一层强。\n\n它会把已确认的基本事实、没验证过的习惯假设、真正的目标、现实约束分开摆，然后只从事实出发重新推路径。改组织流程、做产品架构、修复杂系统都好用。",
        "第一性原理提示语原文。用户的方案在反复打补丁、陷入路径依赖、想回到问题本质重新推导时使用。触发词包括 第一性原理、回到本质、从头推一遍、别打补丁了、推倒重来、这么做的根本原因是什么。产出原方案里只在修补表面的部分，加一条重新推导的新路径和验证第一步。",
        True, "First Principles", "Strip it to bedrock facts and rebuild",
    ),
    (
        "solving", "cross-domain-borrow", "跨领域借解",
        "你这个问题，别的行业可能十几年前就解决了",
        "第一性原理是往下挖回本质，这一条是往外找相通的解法，视角更散。\n\n它先剥掉行业术语把问题抽象成通用结构，再从历史案例和至少三个距离较远的领域找同构问题，最后翻译成你能用的方案和一个低成本可逆实验。",
        "跨领域借解提示语原文。用户在本行业里想不出解法、需要从其他领域借鉴机制时使用。触发词包括 跨领域、别的行业怎么解决、换个视角、类比一下、借鉴其他领域、有没有类似的问题被解决过。产出至少三个远距离领域的同构案例和可迁移机制。",
        True, "Cross-Domain Borrowing", "Steal a mechanism from a distant field",
    ),
    (
        "deciding", "steelman-both-sides", "双向钢人论证",
        "两个选项都有道理的时候，把两边都论证到最强",
        "跟问清问题那一条的分工不一样：那条是帮你把问题提对，这条是你已经有答案了、不知道选哪个的时候拿来做决策。\n\n它先重述你真正要做的选择，再分别给两个方向最强的理由、适用条件、最大收益、最大风险和最难回答的反对意见，最后只问你一个最可能改变结论的问题。",
        "双向钢人论证提示语原文。用户在两个选项之间犹豫不决、需要做决策时使用。触发词包括 钢人、双向钢人、steelman、两个选项选哪个、帮我做个决定、正反两面都说最强理由、我该选 A 还是 B。产出两边的最强论证、真正分歧、关键变量，再问一个最可能改变结论的问题。",
        True, "Steelman Both Sides", "Argue both options at their strongest",
    ),
    (
        "deciding", "minimum-experiment", "最小实验",
        "别再推演了，花七天真跑一次，让现实给你数据",
        "纸上谈兵到头的时候，需要的是现实世界的反馈和数据。\n\n它先找出决定背后最需要验证的三个假设，挑出最可能改变结论的那个，围绕它设计一个低成本、可逆、七天内能做完的实验，最后告诉你明天就能开始的第一个动作。",
        "最小实验提示语原文。用户纠结的事情靠继续想已经不会更清楚、需要用现实反馈来验证时使用。触发词包括 最小实验、先试试、怎么验证、别空想了、跑个实验、小成本试错、七天验证。产出待验证假设、一个低成本可逆实验的完整设计，以及明天就能做的第一个动作。",
        True, "Minimum Experiment", "Replace speculation with a cheap reversible test",
    ),
    (
        "self-knowledge", "hidden-talent", "挖掘隐藏天赋",
        "从你那些看起来毫无关系的经历里，拼出一份天赋说明书",
        "适合还想找到自己天赋的人，也适合觉得自己没什么天赋、正在怀疑自己的人。\n\n它会深度追问你十六岁前的废寝忘食、改不掉的顽固缺点、无意识胜任区、能量地图和你嫉妒过的人，最后写一份一万字左右的个人天赋使用说明书。\n\n动辄半小时以上，答得越真实越具体，产出越有用。中途别跑。",
        "深度天赋挖掘提示语原文。用户想找到自己被忽视或压抑的天赋、怀疑自己没有天赋、想要一份个人天赋使用说明书时使用。这是一次半小时以上的多轮深度对话，一次只问一个问题，最多十个主问题，最后产出一万字左右的说明书。",
        False, "Hidden Talent", "Excavate your buried talents over a deep interview",
    ),
    (
        "self-knowledge", "life-design", "人生设计术",
        "斯坦福人生设计课做成的 Prompt，看的是未来",
        "天赋那条回答我身上到底有啥，往过去看。这条回答我接下来还能往哪去，往未来看。\n\n它带你走四个阶段：你在这里、你的指南针、寻路、摆脱困境与创造可能，最后给三个完全不同、同样值得认真考虑的五年人生版本，以及马上能开始的原型行动。\n\n同样是长对话，要耐心。",
        "人生设计术提示语原文。基于斯坦福人生设计方法，用户想看清现在的位置、分清重力问题和可设计的真问题、规划未来五年时使用。这是一次多轮深度对话，六到九个主问题，最后产出八千到一万两千字的个人人生设计蓝图和三个奥德赛计划。",
        False, "Life Design", "Design three different five-year versions of your life",
    ),
]

BUCKETS = {
    "asking": ("问清问题", "只有知道自己真正想问的是什么，才有后面的一切。"),
    "learning": ("学习", "听懂一个东西有四条路，学会一门东西有第五条。"),
    "solving": ("解决问题", "问题问清楚了，接下来是解。"),
    "deciding": ("决策", "两个答案都有道理的时候，你还是得选一个。"),
    "doing": ("动手", "想清楚之后，把活派出去，再把摊子收干净。"),
    "self-knowledge": ("认识你自己", "人生的底色。这两条要花时间，值得。"),
}

_RUN_WITH_SLOTS = "把【】里的内容换成用户给的真实信息，然后严格照提示语里的规则做事"
_RUN_NO_SLOTS = "直接按提示语里的角色和流程走"

def usage_block(has_slots):
    run = _RUN_WITH_SLOTS if has_slots else _RUN_NO_SLOTS
    return f"""## 怎么用

下面代码块里的提示语是原文，逐字使用。

- 用户要你执行：{run}。它说先别给建议就先别给，说一次只问一个问题就一次只问一个，说按顺序输出就按那个顺序输出。
- 用户要原文（说「给我提示语」「我要复制」「原文发我」）：把整段原样打出来，一个字不改。

禁止改写、精简、扩写、翻译、重排、加小标题，禁止把它替换成你自己的流程，也禁止把多轮追问压缩成一次性问卷。用户手上有原始材料（文档、截图、链接、聊天记录）就一并读进来，上下文多不是问题。"""


def read_source_blocks():
    text = SOURCES.read_text(encoding="utf-8")
    blocks = FENCE.findall(text)
    if len(blocks) != len(CATALOG):
        sys.exit(f"sources/prompts.md 里有 {len(blocks)} 段提示语，CATALOG 里有 {len(CATALOG)} 条，对不上")
    return blocks


def skill_dir(bucket, name):
    return SKILLS / bucket / name


def build():
    blocks = read_source_blocks()
    for (bucket, name, cn, _one_liner, when, desc, model_invoked, display, short), body in zip(CATALOG, blocks):
        d = skill_dir(bucket, name)
        (d / "agents").mkdir(parents=True, exist_ok=True)

        fm = ["---", f"name: {name}", f"description: {desc}"]
        if not model_invoked:
            fm.append("disable-model-invocation: true")
        fm.append("---")

        placeholders = sorted(set(re.findall(r"【[^】]*】", body)))
        parts = ["\n".join(fm), "", f"# {cn}", "", when, "", usage_block(bool(placeholders)), "", "```markdown", body.rstrip("\n"), "```"]
        if placeholders:
            parts += ["", "## 用户要填的位置", ""]
            parts += [f"- `{p}`" for p in placeholders]
            parts += ["", "用户没给全就先问缺的那一条，别自己替他编。"]
        parts += ["", "---", "", "提示语原文来自数字生命卡兹克，出处见仓库 README 的致谢。改动这段原文要走 `scripts/sync.py`，手改会被 verify 拦下。", ""]
        (d / "SKILL.md").write_text("\n".join(parts), encoding="utf-8")

        yaml = ["interface:", f'  display_name: "{display}"', f'  short_description: "{short}"']
        if not model_invoked:
            yaml += ["policy:", "  allow_implicit_invocation: false"]
        (d / "agents" / "openai.yaml").write_text("\n".join(yaml) + "\n", encoding="utf-8")

    write_bucket_readmes()


def _user_invoked(bucket, name):
    fm = (SKILLS / bucket / name / "SKILL.md").read_text(encoding="utf-8")
    return "disable-model-invocation: true" in fm.split("---")[1]


def write_bucket_readmes():
    """每个 bucket 一份目录，本仓库原生的 12 条和收录来的老师们的 skill 一起列。"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("vendor", ROOT / "scripts" / "vendor.py")
    vendor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vendor)

    for bucket, (cn, tagline) in BUCKETS.items():
        native = [(c[1], c[2], c[3], None) for c in CATALOG if c[0] == bucket]
        guest = [(v[1], v[3], v[4], v[2].split("/")[0]) for v in vendor.VENDORED if v[0] == bucket]
        rows = native + guest
        model = [r for r in rows if not _user_invoked(bucket, r[0])]
        user = [r for r in rows if _user_invoked(bucket, r[0])]

        def fmt(r):
            slug, title, one, src = r
            tail = f"（`{slug}`，收录自 {src}）" if src else f"（`{slug}`）"
            return f"- **[{title}](./{slug}/SKILL.md)**{tail}：{one}。"

        lines = [f"# {cn}", "", tagline, ""]
        if model:
            lines += ["## 模型可唤起", "", "你说到相关的事，Agent 自己就会拿出来用。", ""]
            lines += [fmt(r) for r in model] + [""]
        if user:
            lines += ["## 只有你能唤起", "", "太长太黏人，只有你亲口叫它才出现。", ""]
            lines += [fmt(r) for r in user] + [""]
        (SKILLS / bucket / "README.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"built {len(CATALOG)} skills")


def verify():
    blocks = read_source_blocks()
    bad = 0
    for (bucket, name, cn, *_rest), body in zip(CATALOG, blocks):
        p = skill_dir(bucket, name) / "SKILL.md"
        if not p.exists():
            print(f"MISSING  {bucket}/{name}")
            bad += 1
            continue
        found = FENCE.findall(p.read_text(encoding="utf-8"))
        if len(found) != 1:
            print(f"FENCE    {bucket}/{name} 里有 {len(found)} 个 markdown 代码块，应该只有 1 个")
            bad += 1
            continue
        if found[0] != body:
            print(f"DRIFT    {bucket}/{name} 的提示语和 sources/prompts.md 不一致")
            bad += 1
            continue
        print(f"ok       {bucket}/{name}  {cn}  sha256={hashlib.sha256(body.encode()).hexdigest()[:12]}")
    if bad:
        sys.exit(f"\n{bad} 处不一致。提示语原文不许手改，改 sources/prompts.md 再跑 build。")
    print(f"\n{len(CATALOG)} 条提示语逐字一致。")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "verify"
    {"build": build, "verify": verify}.get(cmd, lambda: sys.exit("用法: sync.py build|verify"))()
