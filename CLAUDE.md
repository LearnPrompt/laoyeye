# 在这个仓库里干活

这个仓库装的是**老师们的原文**。它的价值全在一个字没动，所以下面第一条是铁律，不是建议。

两类内容，两道守卫，规矩一样：

| | 原文放哪 | 生成到哪 | 守卫 |
|---|---|---|---|
| 卡兹克 12 条提示语 | `sources/prompts.md` | 各 `SKILL.md` 里的 markdown 代码块 | `python3 scripts/sync.py verify` |
| 收录的 6 个 skill | `vendor/`（钉在 commit 上） | `skills/<bucket>/<name>/` 整个目录 | `python3 scripts/vendor.py verify` |

## 铁律：都不许手改

- **提示语**：要改先改 `sources/prompts.md`，再 `python3 scripts/sync.py build`。顺序、编号、标点、换行、`【】` 占位符全都算字。作者写的是全角冒号就是全角冒号，不要顺手改成英文标点。
- **收录的 skill**：`skills/` 下那六个目录整个是生成物，连 `references/` 和 `scripts/` 一起。要动只能动 `vendor/`，而 `vendor/` 只能靠 `python3 scripts/vendor.py pull` 从上游同步，不能手编。
- 想加自己的说明，写在代码块**外面**、或者写在 README 里。原文里只有原文。
- 每次提交前两道都跑。细节见 [.agents/verbatim.md](./.agents/verbatim.md)。

## 目录

```
sources/prompts.md              卡兹克 12 条原文，唯一真理
vendor/                         老师们的 pristine 副本，钉在 commit 上
vendor/vendor.lock.json         每个文件的 sha256、上游仓库和 commit
scripts/sync.py                 12 条提示语的 build / verify
scripts/vendor.py               收录 skill 的 build / verify / pull
skills/<bucket>/<name>/         生成物，全部
skills/junshi/SKILL.md          军师路由，手写
```

六个 bucket：`asking`、`learning`、`solving`、`deciding`、`doing`、`self-knowledge`。前五个对应卡兹克文章的场景，`doing` 是为收录进来的 leader 和 neat-freak 开的，它们不是提示语，是会真的动文件的 skill。

## 命名：前缀只为解决重名

上游已经用某个名字发布过的 skill，收进来时加来源前缀（`matt-`、`kaz-`、`carl-`），这样用户同时装了上游和军师也不会撞车。没在别处以 skill 形式发布过的，保持原名——卡兹克那 12 条提示语只在文章里出现过，所以 `fact-check` 就叫 `fact-check`。

改名是 `scripts/vendor.py` 里 `VENDORED` 的 patches 声明的唯一一类改动。grill-me 正文里那句 `Call the Skill tool with "grilling"` 也跟着改成 `matt-grilling`，否则改完名它就指向一个不存在的 skill。这条也在 patches 里，一目了然。

## 加东西

**加一条提示语**：追加进 `sources/prompts.md` → 在 `scripts/sync.py` 的 `CATALOG` 里加一条（顺序必须跟文件里的块一一对应）→ build → verify。

**收录一个 skill**：把上游文件按原路径放进 `vendor/<repo>/` → 更新 `vendor/vendor.lock.json`（repo、commit、每个文件的 sha256）→ 在 `scripts/vendor.py` 的 `VENDORED` 里加一条 → build → verify。上游许可必须允许再分发，并把上游的 LICENSE 一起放进 `vendor/<repo>/`。

两种都要顺手更新：`README.md`、`README.en.md`、`.claude-plugin/plugin.json` 的 `skills` 数组，以及 [军师](./skills/junshi/SKILL.md)。**路由漏了一条，就是一个会撒谎的路由。**

## 唤起方式

每条 `SKILL.md` 只有两种身份，见 [.agents/invocation.md](./.agents/invocation.md)：

- **模型可唤起**（默认）：`description` 里写足触发词，Agent 自己就能拿出来用。
- **只有用户能唤起**：加 `disable-model-invocation: true`，同时在 `agents/openai.yaml` 里加 `policy.allow_implicit_invocation: false`。

目前五条是用户唤起：`junshi`、`matt-grill-me`、`matt-teach`、`hidden-talent`、`life-design`。收录来的沿用上游的身份，不动。本仓库原生那 12 条的身份写在 `CATALOG` 的 `model_invoked` 布尔值上，别绕过 `sync.py` 直接改 frontmatter。

收录来的 skill 里，只有 mattpocock 那三条上游带 `agents/openai.yaml`。khazix 的和点子王没有，这里也不替它们造一个——造了就不是原样收录了。

## 文风

中文，大白话，能直接念出来。不用破折号。不写「不是 A 而是 B」这类句式。列表能少就少。
