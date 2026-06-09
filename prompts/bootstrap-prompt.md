# 初始化 Prompt

把下面这段发给你自己的飞书 Hermes Bot。请替换其中的 `你的_Notion_API_Key` 和 `你的_Notion_数据库名称`。

```text
notion api：你的_Notion_API_Key
notion 数据库名称：你的_Notion_数据库名称

请参考这个 GitHub 仓库中的内容完成安装和初始化：
https://github.com/你的用户名/hermes-feishu-notion-video-bot

请你按以下步骤执行：

1. 读取仓库 README、prompts/bootstrap-prompt.md、docs/bot-initialization.md、docs/notion-database-schema.md、docs/platform-extraction-details.md、docs/retry-and-state-machine.md、docs/asr.md、docs/security-and-privacy.md，以及 skills/feishu-video-to-notion/SKILL.md。

2. 安装或创建仓库中的 Skill：feishu-video-to-notion。
   如果可以通过 hermes skills install 安装，请使用仓库 Raw URL 安装。
   如果不能直接安装，请根据 SKILL.md 内容在本地创建同名 Skill。

3. 将我提供的 Notion API 保存到 Hermes 可读取的环境配置中，变量名为 NOTION_API_KEY。后续回复不要展示完整 API Key。

4. 使用 Notion API 搜索我提供的 Notion 数据库名称。
   如果找不到数据库，请提醒我检查：
   - 数据库名称是否正确；
   - 数据库是否已经 Connect 到 Notion Integration；
   - Notion API 是否正确。

5. 读取数据库字段结构，并检查是否包含以下字段：
   - 标题，Title
   - 原始链接，URL
   - 标准化链接，URL
   - 平台，Select
   - 内容类型，Select
   - 处理状态，Select
   - 作者或来源，Rich text
   - 摘要，Rich text
   - 关键观点，Rich text
   - 可行动结论，Rich text
   - 标签，Multi-select
   - 主题，Multi-select
   - 收集时间，Date
   - 重试次数，Number
   - 置信度，Number
   - 处理日志，Rich text

6. 如果字段缺失，请优先尝试自动补齐数据库字段；如果无法自动补齐，请清楚告诉我需要手动添加哪些字段和字段类型。

7. 字段可用后，请创建一条测试记录：
   标题：Hermes 初始化测试
   平台：Hermes
   内容类型：测试
   处理状态：已整理
   摘要：如果你能看到这条记录，说明 Hermes 已经可以写入 Notion。

8. 写入后，请重新读取 Notion 页面验证是否成功。验证成功后，告诉我初始化完成，并告诉我是否需要发送 /restart 或重启 Hermes gateway。

9. 初始化完成后，请说明：以后我在飞书里发送抖音、小红书、微信公众号链接时，你会自动识别链接、创建 Notion 检查点、提取内容、整理摘要、保存原文/证据、写入 Notion，并返回页面链接。

重要规则：
- 如果无法取得视频原文或足够内容证据，不要编造总结，请标记为“待复核”。
- 每个链接独立处理。
- 写入 Notion 后必须验证页面存在再告诉我完成。
```

## 更短版本

如果你已经在视频里解释过细节，可以只发：

```text
notion api：你的_Notion_API_Key
notion 数据库名称：你的_Notion_数据库名称

参考 https://github.com/你的用户名/hermes-feishu-notion-video-bot 中的内容，安装 Skill，并初始化我的 Notion 数据库。初始化完成后告诉我是否需要重启。
```
