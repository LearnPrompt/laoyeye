[中文](./README.md) · **English**

# ring-elder 戒指老爷爷

Chinese web novels have a stock setup: the hero picks up a ring, and inside it lives the remnant soul of an ancient master. He does not fight the hero's battles. He hands over what he knows, a piece at a time. 戒指老爷爷, the old man in the ring.

This repo is that ring. What lives inside is **the people who taught me prompting**.

Khazix (数字生命卡兹克) taught me how to ask, how to learn, and how to decide, and all 12 of his prompts are here verbatim. Matt Pocock taught me what being properly interrogated feels like, and what it takes to actually learn a subject rather than follow it once. Plus my own idea-king, for tearing a plan apart once it looks finished.

One rule: **whoever taught it owns it, and not one character changes.** The originals are kept here byte for byte, two guards enforce it, and the only thing I write is the few lines beside them.

## Install

```bash
npx skills@latest add LearnPrompt/ring-elder
```

That is the whole setup. For a single skill:

```bash
npx skills@latest add LearnPrompt/ring-elder --skill=fact-check
```

If you do not know which one fits, type `/ring-elder` in a session, say what you are stuck on, and it routes you and fires the right skill for you.

No skill support in your agent? Khazix's 12 never needed an install anyway. Open [sources/prompts.md](./sources/prompts.md), copy the one you want, paste it into any AI. Those 12 are in Chinese, which is how he wrote them and how they are kept here. Most models answer in whatever language you write back in.

## The teachers

| Teacher | What they taught | Kept here | License |
|---|---|---|---|
| [数字生命卡兹克 / Khazix](https://github.com/KKKKhazix/khazix-skills) | Asking, learning, deciding, knowing yourself | 12 prompts + leader + neat-freak | article / MIT |
| [Matt Pocock](https://github.com/mattpocock/skills) | Being interrogated until every branch is settled, and actually learning a subject | grilling + grill-me + teach | MIT |
| Carl (me) | Tearing a finished-looking plan apart | idea-king | MIT |

The 12 come from Khazix's 2026-08-21 piece [《都Agent时代了，我还是想分享给你这12个我最常用的Prompt。》](https://mp.weixin.qq.com/s/NAdhdFrUq9-BKelqzqpwBQ). The repo layout, the user-invoked versus model-invoked split, and the shape of the ring-elder router all follow Matt's [ask-matt](https://github.com/mattpocock/skills/tree/main/skills/engineering/ask-matt) and grill-me.

## Contents

Replace the 【…】 placeholders with your own details. Bring your raw material along, context is cheap.

### 1. Ask a sharper question

| | One line |
|---|---|
| [苏格拉底式提问 / Socratic inquiry](./skills/asking/socratic-inquiry/SKILL.md) | No advice yet, one question at a time, six at most |
| [grilling](./skills/asking/matt-grilling/SKILL.md) · Matt | This one does not stop. Every branch of the design tree, until the frontier is empty |
| [grill-me](./skills/asking/matt-grill-me/SKILL.md) · Matt | The user-invoked way into the one above |

### 2. Learn

| | One line |
|---|---|
| [双层解释法 / Two-layer explanation](./skills/learning/two-layer-explain/SKILL.md) | Explained twice, novice then expert |
| [反向拆解 / Reverse teardown](./skills/learning/reverse-teardown/SKILL.md) | Take a great example apart and find which choices made the difference |
| [横纵分析法 / Horizontal-vertical analysis](./skills/learning/horizontal-vertical-analysis/SKILL.md) | Vertical for how it got here, horizontal for how it differs from rivals |
| [事实核查 / Fact check](./skills/learning/fact-check/SKILL.md) | Split a claim into fact, inference, and value judgement, then verify each |
| [teach](./skills/learning/matt-teach/SKILL.md) · Matt | The four above are one-shot. This one runs across sessions and leaves lessons and reference sheets behind |

### 3. Solve

| | One line |
|---|---|
| [专家会诊 / Expert panel](./skills/solving/expert-panel/SKILL.md) | Three complementary views, then make them challenge each other |
| [第一性原理 / First principles](./skills/solving/first-principles/SKILL.md) | Stop patching, strip it to bedrock facts and rebuild |
| [跨领域借解 / Cross-domain borrowing](./skills/solving/cross-domain-borrow/SKILL.md) | Another field may have solved your problem a decade ago |
| [idea-king](./skills/solving/carl-idea-king/SKILL.md) · Carl | First-principles decomposition plus adversarial review |

### 4. Decide

| | One line |
|---|---|
| [双向钢人论证 / Steelman both sides](./skills/deciding/steelman-both-sides/SKILL.md) | When both options look right, argue each at its strongest |
| [用最小实验替代空想 / Minimum experiment](./skills/deciding/minimum-experiment/SKILL.md) | Some decisions stop getting clearer by thinking. Go test one |

### 5. Do

Once it is clear, hand the work out, then clean up after it.

| | One line |
|---|---|
| [leader](./skills/doing/kaz-leader/SKILL.md) · Khazix | Turn a one-line idea into a brief an agent can run all night on |
| [neat-freak](./skills/doing/kaz-neat-freak/SKILL.md) · Khazix | Reconcile docs, rule files, and agent memory with what the code actually does |

### 6. Know yourself

Two long interviews, half an hour and up. User-invoked only, so they never interrupt you on their own.

| | One line |
|---|---|
| [挖掘隐藏天赋 / Hidden talent](./skills/self-knowledge/hidden-talent/SKILL.md) | Looking back, assembling unrelated experiences into a talent manual |
| [人生设计术 / Life design](./skills/self-knowledge/life-design/SKILL.md) | Looking forward, three different five-year versions all worth taking seriously |

The elder himself lives at [skills/ring-elder](./skills/ring-elder/SKILL.md), and his whole job is routing your situation to one of the above.

## Why verbatim

The usual way to skill-ify a prompt is to break it into agent-style steps with branches and checklists. That is deliberately not done here.

These are finished work. Their effect comes from the specific wording, the pacing of the follow-up questions, and the order of the output. Compress "ask one question at a time, do not hand me the whole questionnaire up front" into "ask step by step" and the model dumps all six at once, which voids the prompt entirely.

Two guards, both exit 1:

```bash
python3 scripts/sync.py verify     # the 12 prompts against sources/prompts.md, character by character
python3 scripts/vendor.py verify   # vendored skills against vendor/ and vendor.lock.json
```

The teachers' originals sit in [vendor/](./vendor/), pinned to specific commits. Generating into `skills/` does exactly one thing: rename, so the names do not collide with the upstream repos. Every patch applied is declared in `PATCHES` in `scripts/vendor.py`.

To check upstream for changes, run `python3 scripts/vendor.py pull`.

## License

MIT for this repo's own code and docs. Vendored skills keep their original licenses, preserved as-is under [vendor/](./vendor/) along with each LICENSE file. The 12 prompts remain their author's. This repo packages and verifies, and claims no rights over the content.
