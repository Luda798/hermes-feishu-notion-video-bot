# 配置 Notion

## 1. 新建数据库

在 Notion 中新建一个空白数据库，例如：

```text
我的知识库
```

可以暂时只保留标题字段，后面让 Bot 自动检查和补齐字段。

## 2. 创建 Notion Integration

打开：

<https://www.notion.so/my-integrations>

点击创建 Integration，名称可以叫：

```text
Hermes知识库助手
```

复制 API Token，通常以 `ntn_` 或 `secret_` 开头。

## 3. 把数据库连接给 Integration

打开你的 Notion 数据库页面：

```text
右上角 ... → Connect to → 选择你的 Integration
```

如果没有这一步，Hermes Bot 通常会搜索不到数据库。

## 4. 把 API 和数据库名发给 Bot

```text
notion api：你的_Notion_API_Key
notion 数据库名称：我的知识库

参考 https://github.com/你的用户名/hermes-feishu-notion-video-bot 中的内容，安装 Skill，并初始化我的 Notion 数据库。
```

## 5. 权限提醒

Notion Integration 只能操作你明确 Connect 给它的页面或数据库。为了降低误操作范围，建议只把目标知识库数据库连接给这个 Integration。
