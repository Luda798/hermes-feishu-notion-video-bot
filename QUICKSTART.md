# 快速开始

本页是最短路径。如果你是第一次配置 Hermes 飞书 Bot，建议同时看 `README.md` 和 `docs/` 下的详细教程。

## 目标

搭建一个飞书 Bot：你发抖音、小红书、微信公众号链接，它自动整理并保存到 Notion。

## Step 1：安装 Hermes 并配置飞书 Bot

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
hermes setup
hermes gateway setup
```

在 gateway setup 中选择 Feishu/Lark，并按提示填写飞书应用信息。

## Step 2：准备 Notion

1. 新建 Notion 数据库，例如 `我的知识库`；
2. 创建 Notion API 内部连接（Internal connection）：Notion 左侧边栏 `Settings` → `Connections` → 底部 `Develop your own connections` → `+ New connection`；
   - 直达链接：<https://www.notion.so/profile/integrations/internal>
   - 如果页面空白，先登录 Notion 网页版，并确认你是目标工作区的 Workspace owner；
3. 复制 Internal connection token（也就是 API Token）；
4. 把数据库连接给 Integration：数据库右上角 `...` → `Connect to`。

## Step 3：给飞书 Bot 发初始化消息

```text
notion api：你的_Notion_API_Key
notion 数据库名称：我的知识库

参考这个 GitHub 仓库中的内容完成安装和初始化：
https://github.com/Luda798/hermes-feishu-notion-video-bot

请安装仓库里的 Skill，并初始化我的 Notion 数据库。初始化完成后，请告诉我是否需要重启。
```

## Step 4：重启并测试

如果 Bot 提醒需要重启：

```text
/restart
```

然后发送一个链接：

```text
https://v.douyin.com/xxxx/
```

Bot 应该会：

1. 创建/更新 Notion 记录；
2. 提取内容；
3. 整理摘要、关键观点、行动建议；
4. 写入 Notion；
5. 返回 Notion 页面链接。
