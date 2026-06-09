# Notion Workflow Reference

## Goal

Every link should become a recoverable Notion task before expensive extraction starts.

## Initialization

1. Store user's token as `NOTION_API_KEY`.
2. Search for the target database by name.
3. Confirm the database is shared with the Integration.
4. Read schema.
5. Create or request missing properties.
6. Create and verify a test row.

## Duplicate Detection

Use an OR-style strategy:

1. `去重键` equals `<platform>:<content_id>` when available.
2. `平台内容ID` equals extracted ID.
3. `标准化链接` equals canonical URL.
4. `原始链接` equals user URL.

Update existing rows unless the user asks for a separate copy.

## Checkpoint Properties

Minimum checkpoint:

- `标题`: temporary title or URL
- `原始链接`
- `标准化链接` if known
- `平台`
- `内容类型`
- `处理状态 = 提取中`
- `收集时间`
- `重试次数`
- `处理日志`

Recommended extra properties:

- `平台内容ID`
- `去重键`
- `证据等级`
- `证据来源`
- `失败类型`
- `最后错误`
- `最后处理时间`

## Final Write

Update properties and append page body in this order:

1. `整理版`
2. `一句话结论`
3. `摘要`
4. `核心观点`
5. `可行动结论`
6. `关键原话 / 高亮`
7. `原文 / 转写文本 / 可用证据`
8. `元数据`
9. `来源链接`
10. `处理说明与可靠性`

## Payload Limits

- Notion rich text content should be under 2,000 characters per text object.
- Split long source text/transcripts into paragraphs.
- Append children in batches below Notion limits.
- Store large raw API responses and payloads in files; print only compact summaries.

## Verification

After writing, re-read the page and check:

- page URL exists;
- title exists;
- source link exists;
- status is correct;
- summary or review reason exists;
- required headings exist;
- reliability section exists.
