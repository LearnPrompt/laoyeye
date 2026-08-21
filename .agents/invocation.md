# 模型可唤起 vs 只有用户能唤起

`skills/` 下每个 `SKILL.md` 都是一个 Skill。区分它们的只有一个轴：**谁能唤起它**。

- **只有用户能唤起**：只有人亲口叫它才出现。frontmatter 里 `disable-model-invocation: true`（Claude Code），`agents/openai.yaml` 里 `policy.allow_implicit_invocation: false`（Codex）。这时 `description` 是**写给人看的**，一句话说清它是干嘛的就行，不要堆触发词。
- **模型可唤起**（默认）：模型和用户都能唤起。省掉上面两处。这时 `description` 是**写给模型看的**，触发词要堆足，中文口语说法尽量列全，这样用户随口一说就能命中。

两个 harness 必须同步。一个 Skill 在两边要么都是用户唤起，要么都不是。

## 这个仓库怎么分

大部分提示语是模型可唤起的。用户说「这个说法是真的吗」，`fact-check` 就该自己出来，不需要用户记得有这么个 Skill。

三条例外：

- **`which-prompt`**：路由。让模型自己唤起路由，等于多绕一层，用户直接敲就行。
- **`hidden-talent`**、**`life-design`**：半小时以上的多轮深度追问。作者原话是有些 Prompt 会一直拷打他导致很烦。这种东西自动蹦出来是骚扰，必须用户亲口叫。

判断标准：**这条提示语会不会在用户没准备好的时候把他拖进一场长对话**。会，就设成用户唤起。

## 互相调用

一个 Skill 要用另一个 Skill，写成明确的指令：用 Skill 工具唤起 `<名字>`。不要写成 `../别的目录/FILE.md` 的跨目录引用，也不要只丢一个 `/名字` 让模型猜。

只有模型可唤起的 Skill 能被这样调用。用户唤起的 Skill 谁也调不动，包括别的 Skill。`which-prompt` 是用户唤起的，所以它能唤起那 10 条模型可唤起的提示语，但它唤不动 `hidden-talent` 和 `life-design`，只能告诉用户去敲 `/hidden-talent`。
