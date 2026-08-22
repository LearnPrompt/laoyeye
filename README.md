**中文** · [English](./README.en.md)

# 戒指老爷爷 · laoyeye

萧炎捡到一枚戒指，里面住着药老。药老不替他打架，他把一身本事一点点传过去。

这个仓库就是这么回事。戒指里住着**我的提示语老师们**。

教我怎么问、怎么学、怎么决策的是卡兹克，他那 12 条提示语原文全在里面。教我什么叫真正被拷问到底、怎么把一门东西真学下来的是 Matt Pocock。加上我自己那条点子王，方案成型之后找它拆台。

一条规矩：**谁教的就是谁的，一个字不改**。老师们的原文在这里逐字保存，两道校验守着，我只写他们旁边那几行说明。

## 安装

```bash
npx skills@latest add LearnPrompt/laoyeye
```

装完就能用。想只装其中一条：

```bash
npx skills@latest add LearnPrompt/laoyeye --skill=fact-check
```

不知道用哪条，在会话里敲 `/laoyeye`，说说你卡在哪，老爷爷指路并直接把对应的那条唤起来。

你的 Agent 不支持 Skill 也没关系。卡兹克那 12 条本来就不需要装任何东西，打开 [sources/prompts.md](./sources/prompts.md)，复制哪条用哪条，粘进任何一个 AI 都能跑。

## 老师们

| 老师 | 教的是 | 收录了 | 许可 |
|---|---|---|---|
| [数字生命卡兹克](https://github.com/KKKKhazix/khazix-skills) | 怎么问、怎么学、怎么决策、怎么认识自己 | 12 条提示语原文 + 领导 + 洁癖 | 文章原文 / MIT |
| [Matt Pocock](https://github.com/mattpocock/skills) | 怎么被拷问到把每个分支都想清楚，怎么把一门东西真学下来 | grilling + grill-me + teach | MIT |
| 卡尔（我自己） | 方案成型之后找人拆台 | 点子王 idea-king | MIT |

卡兹克那 12 条来自他 2026 年 8 月 21 日的文章[《都Agent时代了，我还是想分享给你这12个我最常用的Prompt。》](https://mp.weixin.qq.com/s/NAdhdFrUq9-BKelqzqpwBQ)。仓库结构、user-invoked 与 model-invoked 的分法、老爷爷这个路由的形状，学的是 Matt 的 [ask-matt](https://github.com/mattpocock/skills/tree/main/skills/engineering/ask-matt) 和 grill-me。

## 目录

把【】里的内容换成你自己的信息。手上有原始材料就一起丢上去，这年头不怕上下文多。

### 一、问清问题

| | 一句话 |
|---|---|
| [苏格拉底式提问](./skills/asking/socratic-inquiry/SKILL.md) | 先别急着要答案，让它把你真正该问的那个问题问出来，最多六问就收 |
| [拷问 grilling](./skills/asking/matt-grilling/SKILL.md) · Matt | 这条不收。决策树每个分支都问到底，走空为止 |
| [拷问我 grill-me](./skills/asking/matt-grill-me/SKILL.md) · Matt | 上面那条的用户唤起版，敲了才出现 |

### 二、学习

| | 一句话 |
|---|---|
| [双层解释法](./skills/learning/two-layer-explain/SKILL.md) | 小白版和专业版各讲一遍，别停在好像懂了 |
| [反向拆解](./skills/learning/reverse-teardown/SKILL.md) | 看到一个牛逼的成品，把它为什么牛逼拆出来 |
| [横纵分析法](./skills/learning/horizontal-vertical-analysis/SKILL.md) | 纵轴看它怎么走到今天，横轴看它跟对手差在哪 |
| [事实核查](./skills/learning/fact-check/SKILL.md) | 把事实、推论、价值判断拆开，一条条验 |
| [教 teach](./skills/learning/matt-teach/SKILL.md) · Matt | 上面四条都是单次的。这条跨会话把一门东西真学下来，留下课件和速查表 |

### 三、解决问题

| | 一句话 |
|---|---|
| [专家会诊](./skills/solving/expert-panel/SKILL.md) | 组一个真正互补的专家团，然后让他们互相质疑 |
| [第一性原理](./skills/solving/first-principles/SKILL.md) | 别再打补丁了，拆回最底层重新推一遍 |
| [跨领域借解](./skills/solving/cross-domain-borrow/SKILL.md) | 你这个问题，别的行业可能十几年前就解决了 |
| [点子王 idea-king](./skills/solving/carl-idea-king/SKILL.md) · 卡尔 | 第一性原理拆解加对抗式审查，专治方案自我感觉良好 |

### 四、决策

| | 一句话 |
|---|---|
| [双向钢人论证](./skills/deciding/steelman-both-sides/SKILL.md) | 两个选项都有道理的时候，把两边都论证到最强 |
| [用最小实验替代空想](./skills/deciding/minimum-experiment/SKILL.md) | 有些决定，再想也不会更清楚了，去试 |

### 五、动手

想清楚之后，把活派出去，再把摊子收干净。

| | 一句话 |
|---|---|
| [领导 leader](./skills/doing/kaz-leader/SKILL.md) · 卡兹克 | 把一句话的想法拆成 agent 能独立跑一整夜的任务书 |
| [洁癖 neat-freak](./skills/doing/kaz-neat-freak/SKILL.md) · 卡兹克 | 干完活跑一下，把文档、规则文件、agent 记忆跟代码真实状态对齐 |

### 六、认识你自己

这两条是长对话，动辄半小时以上，只有你亲口叫才出现，不会自己蹦出来烦你。

| | 一句话 |
|---|---|
| [挖掘隐藏天赋](./skills/self-knowledge/hidden-talent/SKILL.md) | 往过去看，从那些看起来毫无关系的经历里拼出一份天赋说明书 |
| [人生设计术](./skills/self-knowledge/life-design/SKILL.md) | 往未来看，给你三个完全不同、同样值得认真考虑的五年版本 |

老爷爷本人在 [skills/laoyeye](./skills/laoyeye/SKILL.md)，他的活就是把你的处境路由到上面某一条。

## 为什么是原文

Skill 化的常见做法是把提示语拆成 Agent 风格的流程步骤、加上分支和检查清单。这里刻意不这么干。

这些都是成品，效果来自具体措辞、追问节奏和输出顺序。「每次只问一个问题，不要提前给我一整套问卷」压成「请逐步提问」，模型立刻会把六个问题一次倒出来，整条提示语当场作废。所以重写一遍就是另一个东西了。

守卫有两道，都会退出 1：

```bash
python3 scripts/sync.py verify     # 12 条提示语 vs sources/prompts.md，逐字
python3 scripts/vendor.py verify   # 收录的 skill vs vendor/ 与 vendor.lock.json，逐字
```

老师们的原文躺在 [vendor/](./vendor/)，钉在具体 commit 上。生成到 `skills/` 时只做一件事：改名字，避开跟上游仓库的重名。改了哪几处写在 `scripts/vendor.py` 的 `PATCHES` 里，一目了然。

想跟上游同步就跑 `python3 scripts/vendor.py pull`。

## License

仓库自己的代码与文档 MIT。收录的 skill 各自沿用原许可，原样保存在 [vendor/](./vendor/) 下，含各自的 LICENSE。卡兹克那 12 条提示语的著作权属原作者，本仓库只做封装和校验，不主张任何权利。
