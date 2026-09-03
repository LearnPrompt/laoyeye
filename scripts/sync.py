#!/usr/bin/env python3
"""戒指老爷爷（laoyeye）的提示语同步与校验工具。

真理只有一份：sources/prompts.md 里的 17 个代码块。
build   把这 17 段原文灌进各个 SKILL.md。
verify  逐字比对各个 SKILL.md 里的提示语和 sources/prompts.md，有一个字不一样就报错退出 1。
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources" / "prompts.md"
SKILLS = ROOT / "skills"


# 反引号数量不写死成 3：no-fluff-output 那段原文自带一个三反引号的嵌套代码示例，
# 外层围栏必须比原文里出现的最长反引号串多一个才不会被误判成提前收尾。
# \1 反向引用逼着收尾围栏跟开头反引号数量一致，2/3/4 条其余段落照旧用三个。
FENCE = re.compile(r"^(`{3,}) ?markdown\n(.*?)^\1[ \t]*$", re.S | re.M)

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
        "双层解释法提示语原文。用户遇到听不懂的概念、名词、报错、技术栈，想要一次讲透时使用。触发词包括 双层解释、小白版、专业版、通俗讲一遍、把我当小白、这个概念是什么意思、讲讲什么是、贴着代码或文档问、这个报错什么意思、马上就要用。产出小白解释加专业解释，附术语对照表和自测题。",
        True, "Two-Layer Explanation", "Explain it twice, novice then expert",
    ),
    (
        "learning", "reverse-teardown", "反向拆解",
        "看到一个牛逼的成品，把它为什么牛逼拆出来",
        "适合手里有一个优秀范例，网页、产品页、方案、流程、数据看板都行，你想学会它好在哪。\n\n它先说清这东西解决了什么问题，再倒推哪些关键选择拉开了差距，最后给你可复用规律和一个先练的小练习。",
        "反向拆解提示语原文。用户看到一个优秀的产品、网页、方案、流程、数据看板或作品，想学会它为什么有效时使用。触发词包括 反向拆解、拆解这个、它为什么做得好、我想模仿、逆向拆解、拆解这个好范例、这个牛在哪。产出可复用规律加一份操作清单。只拆做得好的，项目黄了、上线炸了这种失败复盘不用它。",
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
        "第一性原理提示语原文。用户的方案在反复打补丁、陷入路径依赖、想回到问题本质重新推导时使用。触发词包括 第一性原理、回到本质、从头推一遍、别打补丁了、推倒重来、这么做的根本原因是什么。产出原方案里只在修补表面的部分，加一条重新推导的新路径和验证第一步。适合你自己读自己想，不需要 Agent 代跑流程。要的是让人挑毛病、拆台，用 carl-idea-king。",
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
        "最小实验提示语原文。用户纠结的事情靠继续想已经不会更清楚、需要用现实反馈来验证时使用。触发词包括 最小实验、先试试、怎么验证、别空想了、跑个实验、小成本试错、七天验证、已经反复纠结过很多轮、想了很久还是选不出来。产出待验证假设、一个低成本可逆实验的完整设计，以及明天就能做的第一个动作。",
        True, "Minimum Experiment", "Replace speculation with a cheap reversible test",
    ),
    (
        "learning", "parable", "寓言故事",
        "不直接讲这个概念，给你讲个故事，读完你自己悟到",
        "硬啃定义记不住，故事能记一辈子。这条让 AI 围绕一个概念写一则寓言，全程不出现概念名称、不用术语，只在接近结尾时才让你隐约意识到讲的是什么。\n\n故事讲完再给概念解析，最后出两道题：一道验你是不是真懂了核心而不只是记住情节，一道验你能不能把它迁移到别的领域。\n\n提示语里带一份防套路黑名单（意象、地名、结构、角色、开头），因为 AI 写故事特别爱掉进钟表匠、河流、回声城那套模板。",
        "寓言故事提示语原文，帮你理解并记住一个概念，最后带两道检验题。用户看了几遍还是不懂、别人解释过还是没听懂、直接解释已经失败过时使用。触发词包括 用寓言讲讲、讲个故事帮我理解、给我打个比方、寓言、5 分钟搞懂、看了几遍还是不懂、别人解释过我没听懂、直接解释失败过。产出一则不点破概念的寓言，加概念解析，再加两道检验题。原始思路来自 Anthropic 的 Amanda Askell。",
        True, "Parable", "Explain a concept through a fable that never names it",
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
    (
        "asking", "johari-window", "乔哈里视窗",
        "先分清这件事你知我知谁不知，再决定怎么答",
        "不解决某一个具体问题，是给整段协作定规矩：AI 先判断当前信息落在哪个区，再选回应方式。\n\n开放区（都知道）直接答不啰嗦；隐藏区（只有你知道）先问最关键的一两个问题；盲区（只有它知道）主动指出你忽略的角度而不是原地微调；未知区（都不知道）切成共同探索，给多个方向不替你锁定答案。\n\n嫌 AI 要么话太多、要么不问就猜的时候，把这条挂在会话开头。",
        "乔哈里视窗协作提示语原文。用户想设定 AI 的协作方式、抱怨回答不贴需求、嫌追问太多或不问就猜、希望先判断信息状态再回应时使用。触发词包括 乔哈里、视窗、开放区、盲区、隐藏区、未知区、协作模式、别猜我的需求、先搞清楚再答。整段挂在会话或任务开头，约束之后的全部协作。",
        True, "Johari Window", "Judge who knows what before choosing how to respond",
    ),
    (
        "learning", "memory-parable", "记忆寓言法",
        "换个领域讲个故事，故事记住了，概念也就记住了",
        "跟第 13 段寓言故事同一个思路，但这是更短、留原样英文的版本：陈乔维Justin 在一次采访里听 Anthropic 的 Amanda Askell 提到这个方法后原样整理出来的，没有卡兹克那份加的防套路清单和检验题。\n\n适合无聊的时候不想刷手机、想顺手学一个陌生领域的概念又怕学完就忘时使用。领域现填，什么专业都能套。",
        "记忆寓言提示语原文，重点是记住，理解交给别的，寓言讲完还会逐个隐喻对应，无聊的时候拿来消遣也合适。用户想用故事记住一个抽象或陌生的概念，或者只是无聊想让 AI 讲个有意思的东西时使用。触发词包括 记忆寓言、用故事帮我记、别让我背概念、研究生水平的概念、无聊的时候讲个故事、Amanda Askell 那个提示词。产出一则不点破概念的寓言，再解释概念和寓言里每个隐喻的对应关系。",
        True, "Memory Parable", "Turn a concept into a story worth remembering",
    ),
    (
        "asking", "no-fluff-output", "直给输出法",
        "先给能做的下一步，寒暄客套和自我总结一律砍掉",
        "GitHub 上 ayghri 发布的开源 Skill i-have-adhd，小门道在抖音视频里翻译演示后卡尔收录。核心思路：不是让回答更短，是让回答的结构适合注意力容易断的人直接照着做，先说下一步动作，多步骤编号，结尾给一件两分钟内能做的事，报错直说原因和修法，不说客套话。\n\n适合嫌 AI 回答绕、爱兜圈子、结尾总来一句「希望有帮助」的时候，把这条挂在会话开头。跟乔哈里视窗一样是设定协作规则，不是解决单次问题；说「恢复正常模式」或「stop adhd mode」就关掉。",
        "直给输出法提示语原文。用户抱怨 AI 说话啰嗦绕圈子、想要更直接可执行的回答、看长篇容易走神时使用。触发词包括 别废话、直接说重点、说结论、别绕弯子、有话直说、别来虚的、先说怎么做、拒绝废话、ADHD 友好、专注力不够。整段挂在会话开头，约束之后所有回答的结构，说恢复正常模式才关掉。",
        True, "No-Fluff Output", "Lead with the next action, cut the padding",
    ),
    (
        "learning", "eli5", "大图小字讲解法",
        "把你当成完全不懂的人，用大图配几个字的 HTML 讲清楚",
        "苏乐在 X 上转述的 Anthropic 内部 Skill，名字就叫 eli5（explain like I'm 5）。核心只有一句话：把用户当成对这个主题一无所知的人，生成一个 HTML artifact，图占大头，字尽量少。\n\n适合想快速看懂一个陌生主题、又不想啃长篇文字时使用。原帖全文经 fxtwitter 镜像核对过，提示语本身就是这一句英文，作者附的中文版写在下面「作者附的中文版」一节。",
        "大图小字讲解法提示语原文。用户想快速看懂一个陌生主题、希望图多字少地讲清楚、提到 eli5 或完全不懂某个东西时使用。要图、要一个能打开的页面时用它，只要文字讲清楚就不用它。触发词包括 大图小字、eli5、当我什么都不懂、图文讲解、少量文字讲清楚、我完全不懂给我讲讲、生成一个讲解页面。产出一个大图配少量文字的 HTML 讲解页面。",
        True, "Big Picture, Few Words", "Explain it with a big picture and barely any words",
    ),
]

BUCKETS = {
    "asking": ("问清问题", "只有知道自己真正想问的是什么，才有后面的一切。"),
    "learning": ("学习", "听懂一个东西有几条路，直着讲绕着讲各一条；学会一门东西另有一条。"),
    "solving": ("解决问题", "问题问清楚了，接下来是解。"),
    "deciding": ("决策", "两个答案都有道理的时候，你还是得选一个。"),
    "doing": ("动手", "想清楚之后，把活派出去，再把摊子收干净。"),
    "self-knowledge": ("认识你自己", "人生的底色。这两条要花时间，值得。"),
}

# 按条挂在代码块外面的执行注记。原文的缺口只能在这里补，不许伸进代码块。
NOTES = {
    "socratic-inquiry": """## 首轮怎么办

原文规则四要求每次提问前，用一句话说明上一条回答让你更新了什么判断。第一问之前还没有任何回答，这条在首轮无从执行。首轮直接问第一个问题，不要编造一句判断更新来凑格式；规则四从第二问起逐问执行。

这是写在代码块外的下游补丁，原文未动。

## 跑完接哪条

新问题定下来以后，按处境找下一条：还没答案的，去学习或解决那几条里选一条对的路子；已经有两个答案，用 Skill 工具唤起 `steelman-both-sides`。拿不准就让用户回 `/laoyeye` 重新对号。""",
    "two-layer-explain": """## 跑完接哪条

这次听懂就够了，到此为止。想真学成一门本事、跨多次会话留课件，让用户自己敲 `/matt-teach`。听懂了但记不住，用 Skill 工具唤起 `parable`。""",
    "parable": """## 跑完接哪条

故事把直觉装进去了，要把术语挂上，用 Skill 工具唤起 `two-layer-explain`。""",
    "memory-parable": """## 领域怎么填

原文最后一行 `Domain: [your field]` 里的 `[your field]` 要换成用户想学的领域，比如经济学、心理学、计算机、哲学。用户没说清楚就先问，别自己替他挑。

## 跑完接哪条

记住了还想搞懂原理，用 Skill 工具唤起 `two-layer-explain`。""",
    "eli5": """## 作者附的中文版

苏乐原帖里跟着英文提示语附了一句中文版：

「把我当成一个完全不懂这个主题的人，用大图 + 少量文字的 HTML 页面，把这件事解释清楚」

这是苏乐自己的翻译，不是提示语原文的一部分，不进代码块。

## 跑完接哪条

页面看完想往深挖，用 Skill 工具唤起 `two-layer-explain`；想系统研究整个领域，用 Skill 工具唤起 `horizontal-vertical-analysis`。""",
    "reverse-teardown": """## 跑完接哪条

拿着操作清单要派给 agent 干，用 Skill 工具唤起 `kaz-leader`。""",
    "horizontal-vertical-analysis": """## 跑完接哪条

报告里的关键说法要核实，用 Skill 工具唤起 `fact-check`；研究完要在两条路里选，用 Skill 工具唤起 `steelman-both-sides`。

## 没联网怎么办

没有联网或深度研究能力时，先跟用户明说这是降级跑法。只出分析框架，加一份待检索清单，每条标「暂未核实」，不要拿记忆冒充研究。""",
    "fact-check": """## 跑完接哪条

结论分三支。别人的说法立不住，到此结束；自己的方案立不住，用 Skill 工具唤起 `first-principles` 重推；两边都站得住选不出，用 Skill 工具唤起 `steelman-both-sides`。

## 没联网或核不了的时候

没联网只能拆事实、推论、价值判断，事实项一律标「证据不足」，先跟用户说清。待核的是内部数据、私有文档这类网上查不到的，只能帮拆推理链，核不了事实本身，要把这一点如实告诉用户。""",
    "expert-panel": """## 跑完接哪条

三个视角收敛成两个选项，用 Skill 工具唤起 `steelman-both-sides`；只剩一个待验证的假设，用 Skill 工具唤起 `minimum-experiment`。""",
    "first-principles": """## 跑完接哪条

新路径的验证第一步，用 Skill 工具唤起 `minimum-experiment` 设计成七天实验；想让人来拆台，用 Skill 工具唤起 `carl-idea-king`。""",
    "cross-domain-borrow": """## 跑完接哪条

借来的机制要在本行业验一次，用 Skill 工具唤起 `minimum-experiment`。""",
    "steelman-both-sides": """## 跑完接哪条

最后那个关键问题靠想答不出来，用 Skill 工具唤起 `minimum-experiment` 让现实回答。""",
    "minimum-experiment": """## 跑完接哪条

实验设计好了要交给 agent 跑，用 Skill 工具唤起 `kaz-leader` 写任务书。""",
    "johari-window": """## 跑完接哪条

这条是会话级设定，没有下游。可以跟 `no-fluff-output` 一起挂在会话开头，互不冲突。""",
    "no-fluff-output": """## 跑完接哪条

这条是会话级设定，没有下游。可以跟 `johari-window` 一起挂在会话开头，互不冲突。""",
    "hidden-talent": """## 跑完接哪条

产出正好是 `life-design` 第三阶段要用的素材，让用户自己敲 `/life-design` 接着往前看。""",
    "life-design": """## 跑完接哪条

三个奥德赛计划选不出，用 Skill 工具唤起 `steelman-both-sides`；选出来了想先小试一下，用 Skill 工具唤起 `minimum-experiment`。""",
}

# 每条提示语代码块下方的署名句，按 slug 查；查不到的用 DEFAULT_ATTRIBUTION。
# 这张表本身也是"改动原文出处要走 sync.py"这条铁律管的对象，手改 SKILL.md
# 里的署名句会被 verify 当成逐字漂移拦下。
DEFAULT_ATTRIBUTION = "提示语原文来自数字生命卡兹克，出处见仓库 README 的致谢。改动这段原文要走 `scripts/sync.py`，手改会被 verify 拦下。"
ATTRIBUTION = {
    "johari-window": "提示语原文流传于网络、无署名，出处见仓库 README 的致谢。改动这段原文要走 `scripts/sync.py`，手改会被 verify 拦下。",
    "memory-parable": "提示语原文来自陈乔维Justin（抖音），出处见仓库 README 的致谢。改动这段原文要走 `scripts/sync.py`，手改会被 verify 拦下。",
    "no-fluff-output": "提示语原文来自 ayghri（GitHub 项目 i-have-adhd，经小门道抖音转发），出处见仓库 README 的致谢。改动这段原文要走 `scripts/sync.py`，手改会被 verify 拦下。",
    "eli5": "提示语原文来自苏乐（X），出处见仓库 README 的致谢。改动这段原文要走 `scripts/sync.py`，手改会被 verify 拦下。",
}

_RUN_WITH_SLOTS = "先把本轮对话里用户已经说过的处境填进【】，只补真正缺的那一项，别让用户把说过的话再说一遍，然后严格照提示语里的规则做事"
_RUN_NO_SLOTS = "直接按提示语里的角色和流程走"

def usage_block(has_slots):
    run = _RUN_WITH_SLOTS if has_slots else _RUN_NO_SLOTS
    if has_slots:
        raw_line = "用户要原文（明确说要复制、要粘贴、发我原文、给我提示语这类话才算）：打空白版，【】保持不填，一个字不改。用户只是说「看看这条提示语」「这条是干嘛的」，不算要原文，用一两句说清它干什么、什么时候用，再问要不要现在跑，别直接倒原文。"
    else:
        raw_line = "用户要原文（明确说要复制、要粘贴、发我原文、给我提示语这类话才算）：把整段原样打出来，一个字不改。用户只是说「看看这条提示语」「这条是干嘛的」，不算要原文，用一两句说清它干什么、什么时候用，再问要不要现在跑，别直接倒原文。"
    return f"""## 怎么用

下面代码块里的提示语是原文，逐字使用。代码块里的「我」指用户，「请你」「你」指你自己，照它做事，不要把填好的提示语打给用户看。

- 用户要你执行：{run}。它说先别给建议就先别给，说一次只问一个问题就一次只问一个，说按顺序输出就按那个顺序输出。
- {raw_line}
- 除了明确要原文的情况，其余一律当执行处理。

禁止改写、精简、扩写、翻译、重排、加小标题，禁止把它替换成你自己的流程，也禁止把多轮追问压缩成一次性问卷。用户手上有原始材料（文档、截图、链接、聊天记录）就一并读进来，上下文多不是问题。"""


PATH_LINE = re.compile(r"^`skills/([^/`]+)/([^/`]+)`\s*$", re.M)


def read_source_blocks():
    """按顺序取出 12+ 段原文，并确认每段上面那行路径跟 CATALOG 一一对上。

    只比对数量是不够的：块的顺序和 CATALOG 的顺序一旦错位，build 会把每段
    原文写进错误的 SKILL.md，而 verify 用同一套错位配对再比一遍，照样全绿。
    路径行是唯一能钉死配对关系的东西，所以它才是真正的校验。
    """
    text = SOURCES.read_text(encoding="utf-8")
    blocks = [body for _fence, body in FENCE.findall(text)]
    if len(blocks) != len(CATALOG):
        sys.exit(f"sources/prompts.md 里有 {len(blocks)} 段提示语，CATALOG 里有 {len(CATALOG)} 条，对不上")
    paths = PATH_LINE.findall(text)
    if len(paths) != len(CATALOG):
        sys.exit(f"sources/prompts.md 里有 {len(paths)} 行 `skills/<bucket>/<name>` 路径，CATALOG 里有 {len(CATALOG)} 条，对不上")
    for i, ((bucket, name), (cb, cn, *_rest)) in enumerate(zip(paths, CATALOG)):
        if (bucket, name) != (cb, cn):
            sys.exit(f"第 {i + 1} 段错位：sources 写的是 skills/{bucket}/{name}，CATALOG 第 {i + 1} 条是 skills/{cb}/{cn}。"
                     f"\n两边顺序必须一一对应，否则原文会被写进错误的 SKILL.md 而校验发现不了。")
    return blocks


def skill_dir(bucket, name):
    return SKILLS / bucket / name


def fence_for(body):
    """围栏反引号数量：比原文里最长的一串反引号多一个，最少 3 个。

    大多数段落原文里压根没有反引号，走默认的 3 个。no-fluff-output 那段
    原文自己嵌了一段三反引号代码示例，这里就会算出 4，SKILL.md 里生成的
    外层围栏跟着变成 4 个，两边不会互相咬到。
    """
    runs = re.findall(r"`+", body)
    longest = max((len(r) for r in runs), default=0)
    return "`" * max(3, longest + 1)


def build():
    blocks = read_source_blocks()
    for (bucket, name, cn, _one_liner, when, desc, model_invoked, display, short), body in zip(CATALOG, blocks):
        d = skill_dir(bucket, name)
        (d / "agents").mkdir(parents=True, exist_ok=True)

        fm = ["---", f"name: {name}", f"description: {desc}"]
        if not model_invoked:
            fm.append("disable-model-invocation: true")
        fm.append("---")

        # 跨行的【…】是原文自带的引用括号（如乔哈里视窗整段），不是待填槽位。
        # parable 原文的槽位写的是 {concept} 不是【】，两种写法都要认，缺一种
        # 就会漏判 has_slots，也漏掉「用户要填的位置」段。
        placeholders = sorted(set(re.findall(r"【[^】\n]{1,40}】|\{[a-z_]+\}", body)))
        parts = ["\n".join(fm), "", f"# {cn}", "", when, "", usage_block(bool(placeholders))]
        if name in NOTES:
            parts += ["", NOTES[name]]
        fence = fence_for(body)
        parts += ["", f"{fence}markdown", body.rstrip("\n"), fence]
        if placeholders:
            parts += ["", "## 用户要填的位置", ""]
            parts += [f"- `{p}`" for p in placeholders]
            parts += ["", "用户没给全就先问缺的那一条，别自己替他编。"]
        parts += ["", "---", "", ATTRIBUTION.get(name, DEFAULT_ATTRIBUTION), ""]
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
    """每个 bucket 一份目录，本仓库原生的 17 条和收录来的老师们的 skill 一起列。"""
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
        if found[0][1] != body:
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
