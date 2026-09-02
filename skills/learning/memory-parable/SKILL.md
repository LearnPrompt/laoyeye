---
name: memory-parable
description: 记忆寓言提示语原文。用户想用故事记住一个抽象或陌生的概念，或者只是无聊想让 AI 讲个有意思的东西时使用。触发词包括 记忆寓言、用故事帮我记、讲个寓言、别让我背概念、研究生水平的概念、无聊的时候讲个故事、Amanda Askell 那个提示词。产出一则不点破概念的寓言，再解释概念和寓言里每个隐喻的对应关系。
---

# 记忆寓言法

跟第 13 段寓言故事同一个思路，但这是更短、留原样英文的版本：陈乔维Justin 在一次采访里听 Anthropic 的 Amanda Askell 提到这个方法后原样整理出来的，没有卡兹克那份加的防套路清单和检验题。

适合无聊的时候不想刷手机、想顺手学一个陌生领域的概念又怕学完就忘时使用。领域现填，什么专业都能套。

## 怎么用

下面代码块里的提示语是原文，逐字使用。

- 用户要你执行：直接按提示语里的角色和流程走。它说先别给建议就先别给，说一次只问一个问题就一次只问一个，说按顺序输出就按那个顺序输出。
- 用户要原文（说「给我提示语」「我要复制」「原文发我」）：把整段原样打出来，一个字不改。

禁止改写、精简、扩写、翻译、重排、加小标题，禁止把它替换成你自己的流程，也禁止把多轮追问压缩成一次性问卷。用户手上有原始材料（文档、截图、链接、聊天记录）就一并读进来，上下文多不是问题。

## 领域怎么填

原文最后一行 `Domain: [your field]` 里的 `[your field]` 要换成用户想学的领域，比如经济学、心理学、计算机、哲学。用户没说清楚就先问，别自己替他挑。

```markdown
Choose one concept from the domain I give you at the end. Make it roughly graduate-school level.

Write a parable that teaches the concept indirectly. Do not name the concept at the beginning.

Let the reader understand what the story was really about only near the final turn.

After the parable, explain the concept clearly, then map each important metaphor in the story back to the idea.

Domain: [your field]
```

---

提示语原文来自陈乔维Justin（抖音），出处见仓库 README 的致谢。改动这段原文要走 `scripts/sync.py`，手改会被 verify 拦下。
