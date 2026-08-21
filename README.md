**中文** · [English](./README.en.md)

# 军师 · junshi

你出想法，它出打法。

装个军师。你把卡住的事跟它说，它先问你几句，再指一条该用的提示语并直接开跑。

里面是 12 条辅助思考的提示语，原文一个字没改。问清问题、学习、解决问题、决策、认识你自己，五个场景各管一摊。

## 安装

```bash
npx skills@latest add LearnPrompt/junshi
```

装完就能用。想只装其中一条：

```bash
npx skills@latest add LearnPrompt/junshi --skill=fact-check
```

不知道用哪条，在会话里敲 `/junshi`，说说你卡在哪，它指路并直接把对应的那条唤起来。

你的 Agent 不支持 Skill 也没关系。这 12 条本来就不需要装任何东西，打开 [sources/prompts.md](./sources/prompts.md)，复制哪条用哪条，粘进任何一个 AI 都能跑。

## 12 条

把【】里的内容换成你自己的信息。手上有原始材料就一起丢上去，这年头不怕上下文多。

### 一、问清问题

| 提示语 | 一句话 |
|---|---|
| [苏格拉底式提问](./skills/asking/socratic-inquiry/SKILL.md) | 先别急着要答案，让它把你真正该问的那个问题问出来 |

### 二、学习

| 提示语 | 一句话 |
|---|---|
| [双层解释法](./skills/learning/two-layer-explain/SKILL.md) | 小白版和专业版各讲一遍，别停在好像懂了 |
| [反向拆解](./skills/learning/reverse-teardown/SKILL.md) | 看到一个牛逼的成品，把它为什么牛逼拆出来 |
| [横纵分析法](./skills/learning/horizontal-vertical-analysis/SKILL.md) | 纵轴看它怎么走到今天，横轴看它跟对手差在哪 |
| [事实核查](./skills/learning/fact-check/SKILL.md) | 把事实、推论、价值判断拆开，一条条验 |

### 三、解决问题

| 提示语 | 一句话 |
|---|---|
| [专家会诊](./skills/solving/expert-panel/SKILL.md) | 组一个真正互补的专家团，然后让他们互相质疑 |
| [第一性原理](./skills/solving/first-principles/SKILL.md) | 别再打补丁了，拆回最底层重新推一遍 |
| [跨领域借解](./skills/solving/cross-domain-borrow/SKILL.md) | 你这个问题，别的行业可能十几年前就解决了 |

### 四、决策

| 提示语 | 一句话 |
|---|---|
| [双向钢人论证](./skills/deciding/steelman-both-sides/SKILL.md) | 两个选项都有道理的时候，把两边都论证到最强 |
| [用最小实验替代空想](./skills/deciding/minimum-experiment/SKILL.md) | 有些决定，再想也不会更清楚了，去试 |

### 五、认识你自己

这两条是长对话，动辄半小时以上，只有你亲口叫才出现，不会自己蹦出来烦你。

| 提示语 | 一句话 |
|---|---|
| [挖掘隐藏天赋](./skills/self-knowledge/hidden-talent/SKILL.md) | 往过去看，从那些看起来毫无关系的经历里拼出一份天赋说明书 |
| [人生设计术](./skills/self-knowledge/life-design/SKILL.md) | 往未来看，给你三个完全不同、同样值得认真考虑的五年版本 |

军师本人在 [skills/junshi](./skills/junshi/SKILL.md)，它的活就是把你的处境路由到上面某一条。

## 为什么是原文

这个仓库只做一件事：**把提示语原封不动地送到 Agent 面前**。

Skill 化的常见做法是把提示语拆成 Agent 风格的流程步骤、加上分支和检查清单。这里刻意不这么干。这 12 条是作者反复打磨过的成品，它们的效果来自具体措辞、追问节奏和输出顺序，重写一遍就是另一个东西了。

所以：

- 提示语只有一份，在 [sources/prompts.md](./sources/prompts.md)。
- 各个 `SKILL.md` 里的提示语由 `scripts/sync.py build` 灌进去，不许手改。
- `scripts/sync.py verify` 逐字比对全部 12 条，差一个字就退出 1。改完提示语必须跑一遍。

```bash
python3 scripts/sync.py verify
```

## 致谢

12 条提示语的原文和方法论全部来自 **数字生命卡兹克**，出处是他 2026 年 8 月 21 日的文章[《都Agent时代了，我还是想分享给你这12个我最常用的Prompt。》](https://mp.weixin.qq.com/s/NAdhdFrUq9-BKelqzqpwBQ)。其中横纵分析法、隐藏天赋、人生设计术、双向钢人论证他各写过一篇独立文章，都在原文里有链接。

仓库结构、user-invoked 与 model-invoked 的分法、路由 Skill 的形态，参考了 [mattpocock/skills](https://github.com/mattpocock/skills) 的 `ask-matt` 与 `grill-me`。

本仓库只做封装和校验，不主张对提示语内容的任何权利。

## License

仓库代码与文档 MIT。提示语原文著作权属原作者。
