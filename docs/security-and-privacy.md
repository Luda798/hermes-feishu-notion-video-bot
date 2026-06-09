# 安全与隐私

## Public Repo Rules

Never commit:

- Notion API tokens;
- Feishu App Secret;
- model provider API keys;
- cookies;
- user local absolute paths;
- private Notion database IDs;
- chat IDs/user IDs;
- raw private transcripts or payloads.

## Beginner-Friendly Token Setup

This template allows users to paste a Notion API token into their own Feishu Bot for simplicity. Mitigations:

1. Use a dedicated Notion Integration.
2. Connect only the target database to the Integration.
3. Do not connect unrelated private pages.
4. Bot should store token and then redact it in replies.
5. If the token is exposed publicly, rotate it in Notion.

Never ask users to paste Feishu App Secret or model provider keys into normal Bot chat unless they explicitly understand the risk.

## Tool Output Hygiene

- Do not print full API responses by default.
- Do not print full Notion page content unless user asks.
- Do not print tokens/cookies/headers.
- Store large artifacts locally and summarize.

## Custom API Base Warning

Scripts should send Notion tokens only to `https://api.notion.com` by default. Custom API bases should require explicit opt-in.
