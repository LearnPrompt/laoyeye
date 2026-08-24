**中文** · [English](./README.en.md)

# 戒指老爷爷 · laoyeye

小说里的主角都会有一个随身戒指的老爷爷，必要的时候帮他出谋划策。那我们在用 AI 的时候，为什么就不能拥有自己的老爷爷呢。

所以我把今年用到的辅助思考类型的提示语都熔炼起来，做成了这个每个人都可以拥有的戒指老爷爷。

一共 21 件，分六个场景。你不用记住它们，说出你卡在哪就行，老爷爷点人。

## 安装

```bash
npx skills@latest add LearnPrompt/laoyeye
```

装完就能用。想只装其中一件（注意 `--skill` 后面是空格不是等号，写成 `--skill=fact-check` 不会报错，会把 20 件全装上）：

```bash
npx skills@latest add LearnPrompt/laoyeye --skill fact-check
```

不知道用哪件，在会话里敲 `/laoyeye`，说说你卡在哪，老爷爷指路并直接把对应的那件唤起来。

你的 Agent 不支持 Skill 也没关系。那 14 条提示语本来就不需要装任何东西，打开 [sources/prompts.md](./sources/prompts.md)，复制哪条用哪条，粘进任何一个 AI 都能跑。

## 为什么会有它

起因是一个很小的烦恼。

我知道有这些 prompt，也试过用插件快速导入，试过存进备忘录方便搜索。但这些方式都太重了。真到要用的时候，你得先记起来自己存过，再翻出来，再复制粘贴。

后来我在用 Matt Pocock 那套 skill，里面内置了一堆，我一开始不知道该拿哪个，于是干脆去问他的 [ask-matt](https://github.com/mattpocock/skills/tree/main/skills/engineering/ask-matt)：我现在这个情况该用哪个。

那一下我意识到这才是对的形态。一个场景里可以有好几种应对方式，而你不需要记住它们，只需要说出你的处境。这比在外面复制各种内容好，比写进 Agent 的文档里好，也比装插件快。

戒指老爷爷就是这么来的，指路那部分是照着 ask-matt 学的。

## 老师们

戒指里住着的不是我一个人的东西。谁教的就是谁的，原文一个字不改。

| 老师 | 教的是 | 收录了 | 许可 |
|---|---|---|---|
| [数字生命卡兹克](https://github.com/KKKKhazix/khazix-skills) | 怎么问、怎么学、怎么决策、怎么认识自己 | 13 条提示语原文，加领导、洁癖 | 原文 / MIT |
| [Matt Pocock](https://github.com/mattpocock/skills) | 怎么被拷问到把每个分支都想清楚，怎么把一门东西真学下来，怎么修一个难缠的 bug | 拷问、拷问我、教、诊断 | MIT |
| [卡尔（我自己）](https://github.com/LearnPrompt/partner-skill) | 方案成型之后找人拆台 | 点子王 | MIT |

另有一条乔哈里视窗，流传于网络没有署名，原作者如认领欢迎提 issue。

那 13 条提示语出自卡兹克的[这篇](https://mp.weixin.qq.com/s/NAdhdFrUq9-BKelqzqpwBQ)和[这篇](https://mp.weixin.qq.com/s/L1ISA0FvxY_7OR994RttWw)。寓言故事那条的原始思路来自 Anthropic 的 [Amanda Askell](https://askell.io/)，卡兹克在她基础上加了防套路黑名单和两道检验题。仓库结构、user-invoked 与 model-invoked 的分法、老爷爷这个路由的形状，学的是 Matt 的 [ask-matt](https://github.com/mattpocock/skills/tree/main/skills/engineering/ask-matt) 和 grill-me。

## 二十一件

【】里的内容换成你自己的信息。手上有原始材料就一起丢上去，这年头不怕上下文多。

触发语那一列是你直接说出口的话。带斜杠的那几件不会自己出现，只有你亲口敲才启动。

### 一、问清问题

| | 触发语 | 一句话 |
|---|---|---|
| [苏格拉底式提问](./skills/asking/socratic-inquiry/SKILL.md) | 我不知道我到底想问什么 | 先别急着要答案，让它把你真正该问的那个问题问出来，最多六问就收 |
| [拷问](./skills/asking/matt-grilling/SKILL.md) · Matt | 把这个方案盘到底 | 把方案画成决策树，每个分支都问到底，走空为止 |
| [拷问我](./skills/asking/matt-grill-me/SKILL.md) · Matt | `/matt-grill-me` | 同一场拷问，改成只有你亲口喊才开始 |
| [乔哈里视窗](./skills/asking/johari-window/SKILL.md) | 别猜我的需求，先搞清楚再答 | 先分清这件事你知我知谁不知，再决定怎么答 |

### 二、学习

| | 触发语 | 一句话 |
|---|---|---|
| [双层解释法](./skills/learning/two-layer-explain/SKILL.md) | 这个概念给我讲透 | 小白版和专业版各讲一遍，别停在好像懂了 |
| [反向拆解](./skills/learning/reverse-teardown/SKILL.md) | 拆解一下这个东西好在哪 | 看到一个牛逼的成品，把它为什么牛逼拆出来 |
| [横纵分析法](./skills/learning/horizontal-vertical-analysis/SKILL.md) | 深度研究一下这家公司 | 纵轴看它怎么走到今天，横轴看它跟对手差在哪 |
| [事实核查](./skills/learning/fact-check/SKILL.md) | 这个说法是真的吗 | 把事实、推论、价值判断拆开，一条条验 |
| [寓言故事](./skills/learning/parable/SKILL.md) | 用寓言给我讲讲这个概念 | 不直接讲这个概念，给你讲个故事，读完你自己悟到 |
| [教](./skills/learning/matt-teach/SKILL.md) · Matt | `/matt-teach` | 把当前目录变成你的私人课堂，一节课一个小胜利，课件和速查表都留着 |

### 三、解决问题

| | 触发语 | 一句话 |
|---|---|---|
| [专家会诊](./skills/solving/expert-panel/SKILL.md) | 找几个互补的专家会诊 | 组一个真正互补的专家团，然后让他们互相质疑 |
| [第一性原理](./skills/solving/first-principles/SKILL.md) | 用第一性原理重新想一遍 | 别再打补丁了，拆回最底层重新推 |
| [跨领域借解](./skills/solving/cross-domain-borrow/SKILL.md) | 别的行业怎么解决这个 | 你这个问题，别的行业可能十几年前就解决了 |
| [点子王](./skills/solving/carl-idea-king/SKILL.md) · 卡尔 | 点子王，拆一下这个方案 | 假设方案会死，然后去找它是怎么死的 |
| [诊断](./skills/solving/matt-diagnosing-bugs/SKILL.md) · Matt | 帮我排查这个 bug | 先拿到一个能稳定复现的红灯，再谈任何理论，修完带回归测试 |

### 四、决策

| | 触发语 | 一句话 |
|---|---|---|
| [双向钢人论证](./skills/deciding/steelman-both-sides/SKILL.md) | 两边都论证到最强再让我选 | 两个选项都有道理的时候，把两边都论证到最强 |
| [最小实验](./skills/deciding/minimum-experiment/SKILL.md) | 设计个七天能跑完的实验 | 别再推演了，花七天真跑一次，让现实给你数据 |

### 五、动手

| | 触发语 | 一句话 |
|---|---|---|
| [领导](./skills/doing/kaz-leader/SKILL.md) · 卡兹克 | 帮我给 agent 写个目标 | 把一句话的想法拆成 agent 能独立跑一整夜的任务书 |
| [洁癖](./skills/doing/kaz-neat-freak/SKILL.md) · 卡兹克 | 收尾，把文档和记忆对齐 | 干完活跑一下，让文档、规则文件、agent 记忆跟代码的真实状态对上 |

### 六、认识你自己

这两件是长对话，动辄半小时以上，只有你亲口叫才出现，不会自己蹦出来烦你。

| | 触发语 | 一句话 |
|---|---|---|
| [挖掘隐藏天赋](./skills/self-knowledge/hidden-talent/SKILL.md) | `/hidden-talent` | 往过去看，从那些看起来毫无关系的经历里拼出一份天赋说明书 |
| [人生设计术](./skills/self-knowledge/life-design/SKILL.md) | `/life-design` | 往未来看，给你三个完全不同、同样值得认真考虑的五年版本 |

老爷爷本人在 [skills/laoyeye](./skills/laoyeye/SKILL.md)，敲 `/laoyeye` 叫他。他的活就是把你的处境路由到上面某一件。

## 为什么是原文

Skill 化的常见做法是把提示语拆成 Agent 风格的流程步骤、加上分支和检查清单。这里刻意不这么干。

这些都是成品，效果来自具体措辞、追问节奏和输出顺序。把「每次只问一个问题，不要提前给我一整套问卷」压成「请逐步提问」，模型立刻会把六个问题一次倒出来，整条提示语当场作废。所以重写一遍就是另一个东西了。

守卫有两道，都会退出 1：

```bash
python3 scripts/sync.py verify     # 14 条提示语 vs sources/prompts.md，逐字
python3 scripts/vendor.py verify   # 7 个收录的 skill vs vendor/ 与 vendor.lock.json，逐字
```

老师们的原文躺在 [vendor/](./vendor/)，钉在具体 commit 上。生成到 `skills/` 时只做一件事：改名字，避开跟上游仓库的重名。改了哪几处写在 `scripts/vendor.py` 的 patches 里，一目了然。想跟上游同步就跑 `python3 scripts/vendor.py pull`。

## License

仓库自己的代码与文档 MIT。收录的 skill 各自沿用原许可，原样保存在 [vendor/](./vendor/) 下，含各自的 LICENSE。提示语原文的著作权属各自原作者，本仓库只做封装和校验，不主张任何权利。
