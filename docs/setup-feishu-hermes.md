# 安装 Hermes 并配置飞书 Bot

本页给出面向小白的概览步骤。不同系统和 Hermes 版本的细节可能略有差异，请以 Hermes 官方文档为准。

## 1. 安装 Hermes

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

安装后运行：

```bash
hermes setup
```

按提示配置模型供应商和 API Key。

## 2. 配置飞书应用

在飞书开放平台创建应用：

1. 进入飞书开放平台；
2. 创建企业自建应用；
3. 开启机器人能力；
4. 记录 App ID 和 App Secret；
5. 配置事件订阅和回调地址；
6. 给应用添加需要的消息权限；
7. 发布或启用应用。

## 3. 配置 Hermes Gateway

运行：

```bash
hermes gateway setup
```

选择 Feishu/Lark，根据提示填写 App ID、App Secret 等信息。

## 4. 启动 Gateway

前台测试：

```bash
hermes gateway run
```

后台服务：

```bash
hermes gateway install
hermes gateway start
```

## 5. 测试 Bot

在飞书里给 Bot 发：

```text
你好
```

如果 Bot 能回复，说明飞书连接成功。

## 6. 密钥提醒

飞书 App Secret、模型 API Key、Notion API Token 都不要提交到公开 GitHub 仓库。飞书 App Secret 和模型供应商 Key 不建议通过普通聊天发给 Bot；请在 Hermes 配置流程或本地环境文件中填写。

## 7. 常用命令

```bash
hermes gateway status
hermes gateway restart
hermes doctor
hermes config
hermes tools list
```

在飞书里也可以尝试：

```text
/status
/restart
```
