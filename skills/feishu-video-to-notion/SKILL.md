---
name: feishu-video-to-notion
description: Use when a user sends Douyin, Xiaohongshu, or WeChat Official Account links in Feishu and wants Hermes to checkpoint, extract evidence, summarize, and save the result into the user's Notion knowledge database.
version: 1.1.0
author: Hermes Community Template
license: MIT
metadata:
  hermes:
    tags: [feishu, notion, douyin, xiaohongshu, wechat, video, article, knowledge-base]
    related_skills: []
---

# Feishu Video/Article Link → Notion

## Overview

This public skill turns a Feishu Hermes Bot into a personal knowledge-base assistant.
When the user sends a supported link, Hermes should:

1. create or update a Notion checkpoint first;
2. extract the strongest available content evidence;
3. generate a structured knowledge card only when evidence is sufficient;
4. save properties and page body to Notion;
5. verify the write before reporting completion.

First version supported sources:

- Douyin public video/note links;
- Xiaohongshu public video/note links;
- WeChat Official Account public article links.

This skill intentionally does **not** require Coze/扣子 and does not cover YouTube/Bilibili in v1.

## Required References

Before operating, read the repository references if available:

- `references/notion-workflow.md` — Notion schema, checkpointing, duplicate checks, payload limits.
- `references/platform-extraction-playbook.md` — Douyin/Xiaohongshu/WeChat extraction paths.
- `references/retry-state-machine.md` — statuses, retry rules, recoverable interruptions.
- `references/asr-and-evidence.md` — ASR fallback, evidence grades, reliability language.
- `references/security-and-privacy.md` — token handling and public-repo hygiene.

If these files are not available in the current skill installation, use the same rules embedded below.

## When to Use

Use this skill when the user message contains one or more URLs matching:

- `v.douyin.com`
- `douyin.com/video/`
- `douyin.com/note/`
- `iesdouyin.com/share/`
- `xhslink.com`
- `xiaohongshu.com/discovery/item/`
- `xiaohongshu.com/explore/`
- `mp.weixin.qq.com/s/`

Do not use this skill for unrelated Notion operations or unsupported/private/login-only content unless the user explicitly asks for best-effort capture.

## User Configuration

The user provides:

- Notion API token, saved as `NOTION_API_KEY`.
- Target Notion database name.

The target Notion database must be connected to the user's Notion Integration:

```text
Notion database → ... → Connect to → choose Integration
```

Never print the full Notion token back to the user. If the token arrives in chat, store it, then refer to it only as redacted, e.g. `ntn_...abcd`.

## Supported Database Schema

Recommended properties:

| Property | Type | Purpose |
|---|---|---|
| `标题` | Title | Page title |
| `原始链接` | URL | User-provided link |
| `标准化链接` | URL | Resolved canonical URL |
| `平台` | Select | 抖音 / 小红书 / 微信公众号 / 其他 |
| `内容类型` | Select | 视频 / 图文 / 文章 / 未知 / 测试 |
| `处理状态` | Select | 待处理 / 提取中 / 已整理 / 待复核 / 失败 |
| `作者或来源` | Rich text | Creator/account/source |
| `摘要` | Rich text | Concise summary |
| `关键观点` | Rich text | Key points |
| `可行动结论` | Rich text | Actionable takeaways |
| `标签` | Multi-select | Tags |
| `主题` | Multi-select | Topics |
| `收集时间` | Date | Capture time |
| `重试次数` | Number | Retry count |
| `置信度` | Number | 0-1 confidence score |
| `处理日志` | Rich text | Short processing log |

Recommended advanced properties when possible:

| Property | Type | Purpose |
|---|---|---|
| `平台内容ID` | Rich text | aweme_id / xhs note_id / article key |
| `去重键` | Rich text | platform + content ID or canonical URL |
| `证据等级` | Select | high / medium / low / none |
| `证据来源` | Multi-select | ASR / 公众号正文 / 页面可见文本 / 平台章节 / 元数据 |
| `失败类型` | Select | 登录限制 / 风控反爬 / 链接失效 / 媒体不可下载 / ASR失败 / Notion写入失败 / 不支持平台 |
| `最后错误` | Rich text | Most recent concise error |
| `最后处理时间` | Date | Last attempt time |

For beginner databases, keep required fields minimal. If advanced fields are missing, log equivalent information into `处理日志` instead of failing.

## Core State Machine

Use these primary states:

```text
待处理 → 提取中 → 已整理
待处理 → 提取中 → 待复核
待处理 → 提取中 → 失败
提取中 interrupted/stale → 待复核 or resume from checkpoint
```

Rules:

- `已整理`: enough evidence exists to produce a grounded knowledge card.
- `待复核`: record is saved, but extraction evidence is partial or blocked.
- `失败`: terminal failure after retry policy or invalid/unsupported link.
- Do not call an interrupted checkpoint a true failure until you audit Notion status and local artifacts.

## Mandatory Workflow

### 1. Extract and classify links

- Extract all URLs from the message.
- Handle each URL as an independent task.
- Classify platform and content type.
- Resolve short links where possible.

### 2. Compute duplicate key

Prefer duplicate checks in this order:

1. platform content ID (`aweme_id`, Xiaohongshu note ID, WeChat article key);
2. exact `标准化链接`;
3. exact `原始链接`.

If a duplicate exists, update that page rather than creating another page, unless the user asks for a new note.

### 3. Write Notion checkpoint before fragile work

Before browser rendering, media download, ASR, or long extraction:

- create/update Notion page;
- set `处理状态 = 提取中`;
- write original URL, canonical URL if available, platform, capture time, retry count, and processing log;
- store platform content ID and duplicate key when available.

This guarantees the user never loses a link when extraction is interrupted.

### 4. Persist large artifacts outside model context

Store raw HTML, metadata JSON, resource lists, transcript files, screenshots/OCR text, and Notion payload JSON in local cache files. Keep the conversation context compact: path + summary only.

Use a stable per-item cache directory such as:

```text
~/.hermes/cache/video_ingestion/<platform>_<content_id_or_hash>/
```

Do not keep expensive artifacts only in `/tmp`.

### 5. Extract strongest available evidence

Evidence priority:

1. official/native article text or captions;
2. browser-rendered public text;
3. public SSR metadata with chapter/description text;
4. downloadable media + ASR;
5. OCR/visible subtitle snippets;
6. title/author/cover/stats only.

If only item 6 is available, do not generate a confident full summary; mark `待复核`.

### 6. Generate knowledge card

Use the evidence to generate:

- 一句话结论;
- 摘要;
- 核心观点;
- 可行动结论;
- 关键原话 / 高亮 if present;
- source/evidence section;
- reliability caveat.

### 7. Write final Notion page body

Use this order:

```text
整理版
一句话结论
摘要
核心观点
可行动结论
关键原话 / 高亮
原文 / 转写文本 / 可用证据
元数据
来源链接
处理说明与可靠性
```

Keep raw/source material near the bottom, but always include it or explicitly state why it is unavailable.

### 8. Verify before completion

Re-read Notion page/properties/children and verify:

- page exists and URL is available;
- `原始链接` exists;
- status is `已整理` or `待复核`/`失败` with reason;
- page body contains the standard sections;
- evidence and reliability are stated;
- the bot did not claim full transcript without evidence.

Only then tell the user the task is complete.

## Platform Playbooks

### Douyin

For `v.douyin.com`, `douyin.com/video`, `douyin.com/note`, and `iesdouyin.com/share`:

1. Resolve short links with mobile/browser-like User-Agent.
2. Extract `aweme_id` or note ID from URL.
3. Fetch `https://www.iesdouyin.com/share/video/<aweme_id>/` or the canonical page when accessible.
4. Parse SSR data such as `window._ROUTER_DATA` when present.
5. Use browser-rendered `document.body.innerText` and performance resource URLs if browser tools are available.
6. Look for chapter points, descriptions, visible captions, audio/video resources.
7. If public media is downloadable, run ASR and review transcript before writing.
8. If media is blocked, use available public metadata/chapter/visible text and mark evidence limitations.

Never claim full subtitle/transcript extraction if only title, metadata, or chapter summary was available.

### Xiaohongshu

For `xhslink.com`, `/discovery/item/<note_id>`, and `/explore/<note_id>`:

1. Resolve short links, including redirect URLs embedded in OAuth-style redirects when present.
2. Extract note ID and note type: video, image note, or text/image note.
3. Fetch public SSR HTML when accessible.
4. Parse public initial state for title, desc, author, tags, publish time, interaction info, and stream URLs.
5. If video stream is publicly downloadable, download and run ASR.
6. If it is a text/image note and the body is visible, treat visible note text as source evidence.
7. If risk/login page appears, checkpoint and mark `待复核` with failure type `风控反爬` or `登录限制`.

### WeChat Official Account

For `mp.weixin.qq.com/s/...`:

1. Fetch public HTML with mobile WeChat/browser-like headers.
2. Extract metadata from inline variables and meta tags: title, nickname, publish time, description.
3. Extract article body around `js_content`.
4. Strip WeChat UI/footer artifacts while preserving paragraph breaks.
5. Store full original text in Notion page body under `原文`.
6. Generate a high-confidence article knowledge card when body text is available.

WeChat article extraction is usually more stable than short-video extraction because article text is often present in HTML.

## ASR Rules

ASR is optional but valuable. Use it when:

- no official/native transcript exists;
- public media is downloadable;
- local or configured ASR is available.

Rules:

- Prefer local ASR when available for privacy.
- Use domain/language prompts when helpful.
- Review ASR for obvious homophones, script consistency, duplicated segments, and broken names.
- Label transcript as `ASR转写，非官方字幕` unless it is official.
- If ASR fails, fall back to metadata/visible text and mark evidence limitations.

## Failure and Retry Policy

- Retry transient network/HTTP/TLS/timeouts a small number of times.
- Do not retry the exact same blocked strategy indefinitely.
- Treat login/risk-control/media-unavailable as extraction limitations, not Notion failures.
- Set `待复核` when a human can provide a fresh link, screenshot, or manual context.
- Set `失败` only for invalid links, unsupported platforms, repeated terminal errors, or unrecoverable Notion failures.

## Notion API Rules

- Use `NOTION_API_KEY` from env/config.
- Do not print the full token.
- Use `parent.database_id` when creating pages.
- Use data source query endpoints for querying in newer Notion API versions when available.
- Split long rich text blocks under Notion's 2,000-character limit.
- Batch children under Notion request limits.
- Print compact summaries, not full API responses.

## User-Facing Replies

Success:

```text
已完成整理并保存到 Notion。

标题：...
平台：...
处理状态：已整理
证据来源：ASR转写 / 公众号正文 / 页面可见文本 / 平台章节
Notion 页面：...
```

Partial extraction:

```text
已保存到 Notion，但需要复核。

原因：未能取得完整视频原文，只取得公开元数据/页面描述。
处理状态：待复核
Notion 页面：...
```

Unsupported/private:

```text
我已创建 Notion 检查点，但该链接当前无法公开访问或需要登录，暂时不能完整整理。
处理状态：待复核
```

## Common Pitfalls

1. Database not shared with Integration → tell user to Connect database to Integration.
2. Missing fields → initialize fields or ask user to add exact names/types.
3. Metadata-only summary → do not overclaim; mark `待复核`.
4. Long payloads → split blocks and use file-backed payloads.
5. Anti-bot pages → checkpoint first, then mark limitation.
6. Multiple links → one link, one task, one Notion row.
7. Interrupted run → audit checkpoint/cache before declaring failure.
8. Secrets in chat/logs → redact tokens in responses.

## Verification Checklist

- [ ] Supported platform identified.
- [ ] Duplicate check performed.
- [ ] Notion checkpoint created before fragile extraction.
- [ ] Evidence grade assigned.
- [ ] Final status reflects evidence quality.
- [ ] Page body follows standard template.
- [ ] Source/evidence/reliability section exists.
- [ ] Notion page was re-read and verified.
- [ ] No private token/secret was printed.
