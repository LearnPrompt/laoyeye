[中文](./README.md) · **English**

# laoyeye 戒指老爷爷

In Chinese web novels the hero always has an old man living in his ring, who steps in with a plan when it matters. So why shouldn't we have our own old man, now that we work with AI all day.

I took every thinking prompt I actually used this year and forged them into one ring. 老爷爷, laoyeye, the old man. Anyone can have one.

21 pieces across six situations. You do not memorise them. You say what you are stuck on, and he picks.

## Install

```bash
npx skills@latest add LearnPrompt/laoyeye
```

That is the whole setup. For a single piece (note the space, not an equals sign — `--skill=fact-check` does not error, it quietly installs all 20):

```bash
npx skills@latest add LearnPrompt/laoyeye --skill fact-check
```

If you do not know which one fits, type `/laoyeye` in a session, say what you are stuck on, and he routes you and fires the right one.

No skill support in your agent? The 14 prompts never needed an install anyway. Open [sources/prompts.md](./sources/prompts.md), copy the one you want, paste it into any AI. Those 12 are in Chinese, which is how their author wrote them and how they are kept here. Most models answer in whatever language you write back in.

## Why this exists

It started as a small annoyance.

I knew these prompts existed. I tried importing them through a plugin. I tried keeping them in a notes app so I could search. Every one of those is too heavy: when the moment comes, you first have to remember that you saved it, then go dig it out, then copy and paste.

Later I was using Matt Pocock's skills. There is a pile of them and I had no idea which to reach for, so I just asked his [ask-matt](https://github.com/mattpocock/skills/tree/main/skills/engineering/ask-matt): here is my situation, which one do I want.

That was the shape. One situation, several possible answers, and you do not have to remember any of them. You only have to describe where you are. Better than copying text around, better than burying it in an agent's docs, faster than installing a plugin.

That is where the old man came from, and his routing is modelled on ask-matt.

## The teachers

What lives in the ring is not mine alone. Whoever taught it owns it, and not one character changes.

| Teacher | What they taught | Kept here | License |
|---|---|---|---|
| [数字生命卡兹克 / Khazix](https://github.com/KKKKhazix/khazix-skills) | Asking, learning, deciding, knowing yourself | 13 prompts, plus leader and neat-freak | article / MIT |
| [Matt Pocock](https://github.com/mattpocock/skills) | Being interrogated until every branch is settled, actually learning a subject, and diagnosing a stubborn bug | grilling, grill-me, teach, diagnosing-bugs | MIT |
| [Carl (me)](https://github.com/LearnPrompt/partner-skill) | Tearing a finished-looking plan apart | idea-king | MIT |

One more prompt, the Johari window, circulates online unsigned; if you are its author, open an issue and claim it.

The 13 prompts come from [this piece](https://mp.weixin.qq.com/s/NAdhdFrUq9-BKelqzqpwBQ) and [this one](https://mp.weixin.qq.com/s/L1ISA0FvxY_7OR994RttWw) by Khazix. The fable method started with Anthropic's [Amanda Askell](https://askell.io/); Khazix added the anti-cliche blacklists and the two check questions. The repo layout, the user-invoked versus model-invoked split, and the shape of the laoyeye router all follow Matt's [ask-matt](https://github.com/mattpocock/skills/tree/main/skills/engineering/ask-matt) and grill-me.

## The twenty-one

Replace the 【…】 placeholders with your own details. Bring your raw material along, context is cheap.

The trigger column is what you actually say. The ones showing a slash command never appear on their own, and only start when you type them.

### 1. Ask a sharper question

| | Trigger | One line |
|---|---|---|
| [苏格拉底式提问 / Socratic inquiry](./skills/asking/socratic-inquiry/SKILL.md) | 我不知道我到底想问什么 | No advice yet, one question at a time, six at most, until the real question surfaces |
| [grilling](./skills/asking/matt-grilling/SKILL.md) · Matt | 把这个方案盘到底 | Maps the plan as a design tree and works every branch until the frontier is empty |
| [grill-me](./skills/asking/matt-grill-me/SKILL.md) · Matt | `/matt-grill-me` | The same interrogation, started only when you ask for it by name |
| [乔哈里视窗 / Johari window](./skills/asking/johari-window/SKILL.md) | 别猜我的需求，先搞清楚再答 | Judge who knows what before choosing how to respond |

### 2. Learn

| | Trigger | One line |
|---|---|---|
| [双层解释法 / Two-layer explanation](./skills/learning/two-layer-explain/SKILL.md) | 这个概念给我讲透 | Explained twice, novice then expert, so you get past feeling like you understood |
| [反向拆解 / Reverse teardown](./skills/learning/reverse-teardown/SKILL.md) | 拆解一下这个东西好在哪 | Take a great example apart and find which choices made the difference |
| [横纵分析法 / Horizontal-vertical](./skills/learning/horizontal-vertical-analysis/SKILL.md) | 深度研究一下这家公司 | Vertical for how it got here, horizontal for how it differs from rivals |
| [事实核查 / Fact check](./skills/learning/fact-check/SKILL.md) | 这个说法是真的吗 | Split a claim into fact, inference, and value judgement, then verify each |
| [寓言故事 / Parable](./skills/learning/parable/SKILL.md) | 用寓言给我讲讲这个概念 | Never names the concept. Tells you a story instead, and you work it out yourself |
| [teach](./skills/learning/matt-teach/SKILL.md) · Matt | `/matt-teach` | Turns this directory into your private classroom, one small win per lesson, lessons and reference sheets kept |

### 3. Solve

| | Trigger | One line |
|---|---|---|
| [专家会诊 / Expert panel](./skills/solving/expert-panel/SKILL.md) | 找几个互补的专家会诊 | Three genuinely complementary views, then make them challenge each other |
| [第一性原理 / First principles](./skills/solving/first-principles/SKILL.md) | 用第一性原理重新想一遍 | Stop patching, strip it to bedrock facts and rebuild |
| [跨领域借解 / Cross-domain](./skills/solving/cross-domain-borrow/SKILL.md) | 别的行业怎么解决这个 | Another field may have solved your problem a decade ago |
| [idea-king](./skills/solving/carl-idea-king/SKILL.md) · Carl | 点子王，拆一下这个方案 | Assume the plan will die, then go find out how |
| [diagnosing-bugs](./skills/solving/matt-diagnosing-bugs/SKILL.md) · Matt | 帮我排查这个 bug | Get a reliably failing red light before any theory, and fix with a regression test |

### 4. Decide

| | Trigger | One line |
|---|---|---|
| [双向钢人论证 / Steelman both sides](./skills/deciding/steelman-both-sides/SKILL.md) | 两边都论证到最强再让我选 | When both options look right, argue each at its strongest |
| [最小实验 / Minimum experiment](./skills/deciding/minimum-experiment/SKILL.md) | 设计个七天能跑完的实验 | Stop simulating it in your head. Run it for seven days and let reality hand you the data |

### 5. Do

| | Trigger | One line |
|---|---|---|
| [leader](./skills/doing/kaz-leader/SKILL.md) · Khazix | 帮我给 agent 写个目标 | Turn a one-line idea into a brief an agent can run all night on |
| [neat-freak](./skills/doing/kaz-neat-freak/SKILL.md) · Khazix | 收尾，把文档和记忆对齐 | Reconcile docs, rule files, and agent memory with what the code actually does |

### 6. Know yourself

Two long interviews, half an hour and up. They never interrupt you on their own.

| | Trigger | One line |
|---|---|---|
| [挖掘隐藏天赋 / Hidden talent](./skills/self-knowledge/hidden-talent/SKILL.md) | `/hidden-talent` | Looking back, assembling unrelated experiences into a talent manual |
| [人生设计术 / Life design](./skills/self-knowledge/life-design/SKILL.md) | `/life-design` | Looking forward, three different five-year versions all worth taking seriously |

The old man himself lives at [skills/laoyeye](./skills/laoyeye/SKILL.md). Type `/laoyeye` to call him. His whole job is routing your situation to one of the twenty-one.

## Why verbatim

The usual way to skill-ify a prompt is to break it into agent-style steps with branches and checklists. That is deliberately not done here.

These are finished work. Their effect comes from the specific wording, the pacing of the follow-up questions, and the order of the output. Compress "ask one question at a time, do not hand me the whole questionnaire up front" into "ask step by step" and the model dumps all six at once, which voids the prompt entirely.

Two guards, both exit 1:

```bash
python3 scripts/sync.py verify     # the 14 prompts against sources/prompts.md, character by character
python3 scripts/vendor.py verify   # the 7 vendored skills against vendor/ and vendor.lock.json
```

The teachers' originals sit in [vendor/](./vendor/), pinned to specific commits. Generating into `skills/` does exactly one thing: rename, so the names do not collide with the upstream repos. Every patch applied is declared in `scripts/vendor.py`. To check upstream for changes, run `python3 scripts/vendor.py pull`.

## License

MIT for this repo's own code and docs. Vendored skills keep their original licenses, preserved as-is under [vendor/](./vendor/) along with each LICENSE file. The prompts remain their authors' own. This repo packages and verifies, and claims no rights over the content.
