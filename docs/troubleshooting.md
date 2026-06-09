# 常见问题排查

## 1. 飞书 Bot 没反应

检查：

```bash
hermes gateway status
hermes doctor
```

尝试重启：

```bash
hermes gateway restart
```

或在飞书里发送：

```text
/restart
```

## 2. 找不到 Notion 数据库

常见原因：

1. 数据库名称写错；
2. 数据库没有 Connect 给 Integration；
3. Notion API Key 填错；
4. Integration 不在同一个 workspace；
5. 用户创建的是普通页面，不是数据库。

修复：

```text
打开数据库页面 → 右上角 ... → Connect to → 选择 Integration
```

然后重新发送初始化 Prompt。

## 3. Notion 字段缺失

Bot 会提示缺哪些字段。按 `docs/notion-database-schema.md` 添加即可。

常见字段类型：

```text
原始链接：URL
平台：Select
处理状态：Select
摘要：Rich text
标签：Multi-select
收集时间：Date
重试次数：Number
置信度：Number
```

## 4. 抖音/小红书无法完整整理

这是正常情况。短视频平台可能存在：

- 反爬；
- 登录限制；
- IP 风控；
- 链接过期；
- 视频已删除；
- 音频/视频无法下载。

正确结果应该是：

```text
已保存到 Notion，但状态为 待复核。
```

而不是编造总结。

## 5. 为什么需要重启？

Hermes 安装新 Skill 后，当前会话可能不会立刻加载。重启 gateway 或开始新会话后更稳定。

飞书里可以发送：

```text
/restart
```

## 6. API Key 发给 Bot 安全吗？

Notion API Token 拥有你授权给 Integration 的页面/数据库权限。建议只把你希望 Bot 操作的数据库 Connect 给这个 Integration，不要授权整个工作区的敏感页面。

## 7. 公众号文章没有作者或发布时间

部分公众号页面不会稳定暴露所有元数据。Bot 应该保存能提取到的信息，并在处理说明里标记缺失字段。

## 8. 如何判断成功？

成功结果应该包含：

- 飞书里 Bot 回复 Notion 页面链接；
- Notion 数据库里有新记录；
- `处理状态` 是 `已整理` 或合理的 `待复核`；
- 页面正文里有整理版、来源链接、处理说明与可靠性。
