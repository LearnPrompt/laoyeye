[中文](./README.md) · **English**

# thinking-prompts

12 thinking prompts, packaged as skills with the original wording untouched. Say what you are stuck on, and the agent reaches for the right one.

## Install

```bash
npx skills@latest add LearnPrompt/thinking-prompts
```

That is the whole setup. For a single prompt:

```bash
npx skills@latest add LearnPrompt/thinking-prompts --skill=fact-check
```

If you do not know which one fits, type `/which-prompt` in a session, describe your situation, and it routes you and fires the right skill for you.

No skill support in your agent? These 12 never needed an install anyway. Open [sources/prompts.md](./sources/prompts.md), copy the one you want, paste it into any AI.

The prompts themselves are in Chinese, which is how the author wrote them and how they are kept here. Most models answer in whatever language you write back in.

## The 12

Replace the 【…】 placeholders with your own details. Bring your raw material along, context is cheap.

### 1. Ask a sharper question

| Prompt | One line |
|---|---|
| [苏格拉底式提问 / Socratic inquiry](./skills/asking/socratic-inquiry/SKILL.md) | No advice yet, one question at a time, until the question worth answering surfaces |

### 2. Learn

| Prompt | One line |
|---|---|
| [双层解释法 / Two-layer explanation](./skills/learning/two-layer-explain/SKILL.md) | Explained twice, novice then expert, so you get past feeling like you understood |
| [反向拆解 / Reverse teardown](./skills/learning/reverse-teardown/SKILL.md) | Take a great example apart and find which choices made the difference |
| [横纵分析法 / Horizontal-vertical analysis](./skills/learning/horizontal-vertical-analysis/SKILL.md) | Vertical axis for how it got here, horizontal axis for how it differs from rivals |
| [事实核查 / Fact check](./skills/learning/fact-check/SKILL.md) | Split a claim into fact, inference, and value judgement, then verify each |

### 3. Solve

| Prompt | One line |
|---|---|
| [专家会诊 / Expert panel](./skills/solving/expert-panel/SKILL.md) | Three genuinely complementary views, then make them challenge each other |
| [第一性原理 / First principles](./skills/solving/first-principles/SKILL.md) | Stop patching, strip it back to bedrock facts and rebuild |
| [跨领域借解 / Cross-domain borrowing](./skills/solving/cross-domain-borrow/SKILL.md) | Another field may have solved your problem a decade ago |

### 4. Decide

| Prompt | One line |
|---|---|
| [双向钢人论证 / Steelman both sides](./skills/deciding/steelman-both-sides/SKILL.md) | When both options look right, argue each at its strongest |
| [用最小实验替代空想 / Minimum experiment](./skills/deciding/minimum-experiment/SKILL.md) | Some decisions stop getting clearer by thinking. Go test one |

### 5. Know yourself

Two long interviews, half an hour and up. User-invoked only, so they never interrupt you on their own.

| Prompt | One line |
|---|---|
| [挖掘隐藏天赋 / Hidden talent](./skills/self-knowledge/hidden-talent/SKILL.md) | Looking back, assembling unrelated experiences into a talent manual |
| [人生设计术 / Life design](./skills/self-knowledge/life-design/SKILL.md) | Looking forward, three different five-year versions all worth taking seriously |

Plus one router: [which-prompt](./skills/which-prompt/SKILL.md), which answers which one to use.

## Why verbatim

This repo does exactly one thing: **put the prompts in front of the agent unchanged.**

The usual way to skill-ify a prompt is to break it into agent-style steps with branches and checklists. That is deliberately not done here. These 12 are finished work, and their effect comes from the specific wording, the pacing of the follow-up questions, and the order of the output. Rewrite them and you have a different thing.

So:

- One copy of each prompt lives in [sources/prompts.md](./sources/prompts.md).
- The block inside each `SKILL.md` is written by `scripts/sync.py build`, never by hand.
- `scripts/sync.py verify` compares all 12 character by character and exits 1 on any drift.

```bash
python3 scripts/sync.py verify
```

## Credits

All 12 prompts and the method behind them come from **数字生命卡兹克 (Khazix)**, published on 2026-08-21 in [《都Agent时代了，我还是想分享给你这12个我最常用的Prompt。》](https://mp.weixin.qq.com/s/NAdhdFrUq9-BKelqzqpwBQ). Four of them (horizontal-vertical analysis, hidden talent, life design, steelman both sides) have their own dedicated articles, linked from that piece.

The repo layout, the user-invoked versus model-invoked split, and the router skill follow [mattpocock/skills](https://github.com/mattpocock/skills), specifically `ask-matt` and `grill-me`.

This repo packages and verifies. It claims no rights over the prompt text.

## License

MIT for the repo's code and docs. The prompt text remains the author's.
