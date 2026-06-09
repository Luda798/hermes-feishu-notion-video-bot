# Bot 初始化说明

本文是给 Hermes Bot 看的初始化操作说明。

## 输入信息

用户会在飞书里提供：

```text
notion api：...
notion 数据库名称：...
仓库链接：...
```

## 初始化目标

让当前 Hermes 飞书 Bot 具备以下能力：

- 收到抖音链接后整理并保存 Notion；
- 收到小红书链接后整理并保存 Notion；
- 收到微信公众号文章后整理并保存 Notion；
- 无法完整提取时保存检查点并标记 `待复核`。

## 初始化步骤

### 1. 读取仓库资料

读取：

- `README.md`
- `skills/feishu-video-to-notion/SKILL.md`
- `docs/notion-database-schema.md`
- `docs/supported-platforms.md`
- `docs/troubleshooting.md`

### 2. 安装 Skill

优先使用 Hermes Skill 安装命令：

```bash
hermes skills install <SKILL_RAW_URL>
```

如果无法直接安装，则在本地 Hermes skills 目录创建：

```text
~/.hermes/skills/productivity/feishu-video-to-notion/SKILL.md
```

内容使用仓库中的 `skills/feishu-video-to-notion/SKILL.md`。

安装后可能需要新会话或 gateway 重启才能稳定生效。

### 3. 保存 Notion API

将用户提供的 Notion Token 保存为：

```text
NOTION_API_KEY=...
```

推荐写入 Hermes 环境文件：

```bash
hermes config env-path
```

注意：回复用户时不要展示完整 Token。

### 4. 搜索 Notion 数据库

使用 Notion Search API 搜索用户提供的数据库名称。

如果找不到，提醒用户检查：

1. 数据库名称是否正确；
2. 数据库是否 Connect 给了 Integration；
3. Notion API Key 是否正确；
4. Integration 是否有权限访问该 workspace。

### 5. 检查/初始化字段

读取数据库/数据源 schema，检查推荐字段是否存在。

如果字段缺失：

- 优先尝试用 Notion API 自动补齐字段；
- 如果失败，告诉用户手动新增字段名和字段类型。

字段清单见 `docs/notion-database-schema.md`。

### 6. 写入测试记录

创建一条测试记录：

```text
标题：Hermes 初始化测试
平台：Hermes
内容类型：测试
处理状态：已整理
摘要：如果你能看到这条记录，说明 Hermes 已经可以写入 Notion。
```

### 7. 验证

重新读取测试页面，确认：

- 页面存在；
- 标题正确；
- 处理状态正确；
- 页面 URL 可用。

### 8. 用户通知

初始化成功后回复：

```text
初始化完成。你的飞书 Bot 已经可以处理抖音、小红书、微信公众号链接并保存到 Notion。
如果后续链接没有自动触发，请发送 /restart 后再测试。
```

如果失败，回复具体失败点和修复步骤。
