# 在这个仓库里干活

这个仓库只装 12 条提示语。它的价值全在**原文一个字没动**，所以下面第一条是铁律，不是建议。

## 铁律：提示语不许手改

- 唯一真理是 [sources/prompts.md](./sources/prompts.md) 里的 12 个 ```` ``` markdown ```` 代码块。
- 各个 `SKILL.md` 里的提示语代码块是**生成物**。要改先改 `sources/prompts.md`，再 `python3 scripts/sync.py build`。
- 每次提交前跑 `python3 scripts/sync.py verify`。它逐字比对 12 条，差一个字符就退出 1。
- 顺序、编号、标点、换行、`【】` 占位符，全都算字。作者写的是全角冒号就是全角冒号，不要顺手改成英文标点。
- 想加一句自己的补充说明，写在代码块**外面**。代码块里只有原文。

细节见 [.agents/verbatim.md](./.agents/verbatim.md)。

## 目录

```
sources/prompts.md              12 条原文，唯一真理
scripts/sync.py                 build / verify
skills/<bucket>/<name>/SKILL.md 生成物
skills/junshi/SKILL.md    路由，手写
```

五个 bucket 对应文章里的五个场景：`asking`、`learning`、`solving`、`deciding`、`self-knowledge`。

## 加一条提示语

1. 把原文追加进 `sources/prompts.md`，位置按它属于哪个场景。
2. 在 `scripts/sync.py` 的 `CATALOG` 里加一条，顺序必须和 `sources/prompts.md` 里的块顺序一一对应。
3. 跑 `build`，再跑 `verify`。
4. 更新 `README.md`、`README.en.md`、`.claude-plugin/plugin.json` 的 `skills` 数组。
5. 更新 [军师 junshi](./skills/junshi/SKILL.md)。**路由漏了一条，就是一个会撒谎的路由。**

## 唤起方式

每条 `SKILL.md` 只有两种身份，见 [.agents/invocation.md](./.agents/invocation.md)：

- **模型可唤起**（默认）：`description` 里写足触发词，Agent 自己就能拿出来用。
- **只有用户能唤起**：加 `disable-model-invocation: true`，同时在 `agents/openai.yaml` 里加 `policy.allow_implicit_invocation: false`。两处必须同时改，一个 Skill 在两个 harness 里要么都是用户唤起，要么都不是。

目前只有三条是用户唤起：`junshi`、`hidden-talent`、`life-design`。后两条是半小时以上的深度追问，自动蹦出来只会烦人。这个判断标准写在 `CATALOG` 里那个 `model_invoked` 布尔值上，别绕过 `sync.py` 直接改 frontmatter。

## 文风

中文，大白话，能直接念出来。不用破折号。不写「不是 A 而是 B」这类句式。列表能少就少。
