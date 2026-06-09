# Hermes 飞书 Notion 视频知识库 Bot

这是一个面向小白用户的公开模板仓库，用来搭建一个运行在 **飞书/Lark** 里的 Hermes Bot：

> 你在飞书里给 Bot 发抖音、小红书或微信公众号链接，Bot 会自动整理内容，并保存到你的 Notion 知识库。

第一版目标是 **简单、可跑通、可复核**，暂不追求覆盖所有平台，也不依赖 Coze/扣子。

## 支持范围

✅ 抖音公开视频/图文：`v.douyin.com`、`douyin.com/video/...`、`iesdouyin.com/share/...`  
✅ 小红书公开视频/图文：`xhslink.com`、`xiaohongshu.com/discovery/item/...`、`xiaohongshu.com/explore/...`  
✅ 微信公众号公开文章：`mp.weixin.qq.com/s/...`  
✅ 自动写入 Notion 数据库  
✅ 自动生成摘要、关键观点、可行动结论  
✅ 提取不到完整内容时标记为 `待复核`，不编造总结

暂不支持：YouTube、B站、私密/登录内容、托管云服务、Coze/扣子强依赖。

## 用户只需要四步

### 1. 安装 Hermes，配置飞书 Bot

先安装 Hermes Agent，并完成飞书 Bot/Gateway 配置。

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
hermes setup
hermes gateway setup
```

详细教程见：[docs/setup-feishu-hermes.md](docs/setup-feishu-hermes.md)

### 2. 建立 Notion 空白数据库，新建 Notion API

在 Notion 中：

1. 新建一个空白数据库，例如：`我的知识库`；
2. 到 <https://www.notion.so/my-integrations> 创建 Integration；
3. 复制 Notion API Token；
4. 把数据库右上角 `...` → `Connect to` → 连接给你的 Integration。

详细教程见：[docs/setup-notion.md](docs/setup-notion.md)

### 3. 给飞书 Bot 发两句话

把下面内容发给你自己的飞书 Bot：

```text
notion api：你的_Notion_API_Key
notion 数据库名称：你的_Notion_数据库名称

参考这个 GitHub 仓库中的内容完成安装和初始化：
https://github.com/你的用户名/hermes-feishu-notion-video-bot

请安装仓库里的 Skill，并初始化我的 Notion 数据库。初始化完成后，请告诉我是否需要重启。
```

完整初始化 Prompt 见：[prompts/bootstrap-prompt.md](prompts/bootstrap-prompt.md)

### 4. 重启，然后发一个视频链接测试

如果 Bot 提示需要重启，请在飞书里发送：

```text
/restart
```

然后测试：

```text
请帮我整理这个链接并保存到 Notion：
https://v.douyin.com/xxxx/
```

或：

```text
https://mp.weixin.qq.com/s/xxxx
```

## 仓库内容

```text
.
├── README.md
├── QUICKSTART.md
├── LICENSE
├── skills/
│   └── feishu-video-to-notion/
│       └── SKILL.md
├── prompts/
│   └── bootstrap-prompt.md
├── docs/
│   ├── bot-initialization.md
│   ├── notion-database-schema.md
│   ├── platform-extraction-details.md
│   ├── retry-and-state-machine.md
│   ├── asr.md
│   ├── security-and-privacy.md
│   ├── setup-feishu-hermes.md
│   ├── setup-notion.md
│   ├── supported-platforms.md
│   └── troubleshooting.md
└── scripts/
    ├── notion_apply_payload.py
    └── verify_notion_connection.py
```

## 进阶说明

- 平台提取细节：[docs/platform-extraction-details.md](docs/platform-extraction-details.md)
- 重试与状态机：[docs/retry-and-state-machine.md](docs/retry-and-state-machine.md)
- ASR 与证据等级：[docs/asr.md](docs/asr.md)
- 安全与隐私：[docs/security-and-privacy.md](docs/security-and-privacy.md)

## 重要原则

- 每个链接独立处理。
- 先写 Notion 检查点，再做长时间提取。
- 有实际内容证据才生成完整整理。
- 如果只有标题/元数据，标记为 `待复核`。
- 写入 Notion 后必须验证页面存在，再回复用户“完成”。
- Notion API Token 只拥有你授权给 Integration 的页面/数据库权限；请只连接你愿意让 Bot 操作的数据库。

## 推荐 Notion 字段

见：[docs/notion-database-schema.md](docs/notion-database-schema.md)

## 常见问题

见：[docs/troubleshooting.md](docs/troubleshooting.md)
