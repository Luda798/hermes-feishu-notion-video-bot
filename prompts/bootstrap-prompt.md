# 初始化 Prompt

这个文件给用户复制到自己的 **飞书 Hermes Bot** 中使用。目标是让用户尽量只发“两句话”，Bot 就能根据本仓库完成 Skill 安装、Notion 连接、数据库初始化和测试写入。

> 使用前提：用户已经完成 Hermes 安装、飞书 Bot 配置、Notion Integration 创建，并把目标 Notion 数据库 Connect 给该 Integration。

---

## 版本 A：小白两句话版（推荐放在视频里）

把下面内容发给你自己的飞书 Bot。只需要替换 Notion API 和数据库名称。

```text
notion api：你的_Notion_API_Key
notion 数据库名称：你的_Notion_数据库名称

参考这个 GitHub 仓库完成安装和初始化：
https://github.com/Luda798/hermes-feishu-notion-video-bot

请你自动完成以下事情：安装仓库里的 feishu-video-to-notion Skill，保存我的 Notion API，搜索并初始化我的 Notion 数据库，创建一条测试记录并验证写入。初始化完成后告诉我是否需要发送 /restart。以后我发送抖音、小红书、微信公众号链接时，请自动整理并保存到 Notion；如果无法取得足够内容证据，不要编造总结，标记为“待复核”。
```

适合视频教学，因为用户只需要改两处：

```text
你的_Notion_API_Key
你的_Notion_数据库名称
```

---

## 版本 B：详细稳定版（如果两句话版执行不完整，用这一版）

```text
notion api：你的_Notion_API_Key
notion 数据库名称：你的_Notion_数据库名称

请参考这个 GitHub 仓库完成初始化：
https://github.com/Luda798/hermes-feishu-notion-video-bot

你需要按下面步骤执行，不要只回复教程：

1. 读取仓库中的这些文件：
   - README.md
   - QUICKSTART.md
   - prompts/bootstrap-prompt.md
   - docs/bot-initialization.md
   - docs/notion-database-schema.md
   - docs/platform-extraction-details.md
   - docs/retry-and-state-machine.md
   - docs/asr.md
   - docs/security-and-privacy.md
   - skills/feishu-video-to-notion/SKILL.md

2. 安装 Skill：feishu-video-to-notion。
   优先使用这个 Raw URL 安装：
   https://raw.githubusercontent.com/Luda798/hermes-feishu-notion-video-bot/main/skills/feishu-video-to-notion/SKILL.md
   如果不能直接安装，请根据仓库里的 SKILL.md 在本地 Hermes skills 目录创建同名 Skill。

3. 保存 Notion API：
   - 将我提供的 Notion API 保存为 NOTION_API_KEY；
   - 后续回复中不要展示完整 API；
   - 只需要告诉我“已保存 Notion API”。

4. 连接 Notion 数据库：
   - 使用 Notion API 搜索我提供的数据库名称；
   - 如果找不到数据库，提醒我检查数据库名称、Integration 是否 Connect、API 是否正确；
   - 找到后读取数据库字段结构。

5. 初始化数据库字段。
   请检查并尽量自动补齐这些字段：
   - 标题：Title
   - 原始链接：URL
   - 标准化链接：URL
   - 平台：Select
   - 内容类型：Select
   - 处理状态：Select
   - 作者或来源：Rich text
   - 摘要：Rich text
   - 关键观点：Rich text
   - 可行动结论：Rich text
   - 标签：Multi-select
   - 主题：Multi-select
   - 收集时间：Date
   - 重试次数：Number
   - 置信度：Number
   - 处理日志：Rich text
   可选高级字段：平台内容ID、去重键、证据等级、证据来源、失败类型、最后错误、最后处理时间。

   如果当前工具或 Notion API 权限不支持自动补齐字段，请不要卡住，请直接列出我需要手动添加的字段名和字段类型。

6. 创建测试记录并验证：
   - 标题：Hermes 初始化测试
   - 平台：Hermes
   - 内容类型：测试
   - 处理状态：已整理
   - 摘要：如果你能看到这条记录，说明 Hermes 已经可以写入 Notion。
   写入后请重新读取该页面，确认标题、状态、URL 存在。

7. 初始化完成后，请告诉我：
   - Skill 是否已安装；
   - Notion API 是否已保存；
   - 数据库是否找到；
   - 字段是否完整；
   - 测试记录是否写入并验证成功；
   - 是否需要发送 /restart。

8. 初始化后的长期规则：
   - 当我发送抖音、小红书、微信公众号链接时，每个链接独立处理；
   - 先创建 Notion 检查点，再做提取；
   - 有实际内容证据才生成完整总结；
   - 如果只有标题、封面、作者、互动数据等低证据内容，标记为“待复核”；
   - 写入 Notion 后必须重新读取验证，再告诉我完成。
```

---

## 版本 C：初始化失败后的继续处理 Prompt

如果 Bot 中途失败、字段缺失、Notion 数据库没找到，修复后发送：

```text
请继续刚才的 Hermes Notion 初始化任务。

我已经按你的提示修复了问题。请重新检查：
1. Notion API 是否可用；
2. 数据库是否能找到；
3. 数据库字段是否完整；
4. 测试记录是否能创建并验证；
5. feishu-video-to-notion Skill 是否已安装。

如果还有问题，请只告诉我具体缺什么、怎么修。
```

---

## 版本 D：测试链接 Prompt

初始化完成并重启后，发送：

```text
请用 feishu-video-to-notion Skill 处理这个链接，并保存到我的 Notion 知识库：
这里粘贴一个抖音/小红书/微信公众号链接

要求：先写 Notion 检查点，再提取内容；如果证据不足，请标记为“待复核”，不要编造总结；写入后请验证 Notion 页面并把页面链接发给我。
```
