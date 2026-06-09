# 平台提取细节

## General Rules

- Create a Notion checkpoint before fragile extraction.
- Save raw HTML/JSON/transcripts to local cache files.
- Use the strongest available content evidence.
- If only metadata exists, mark `待复核`.

## Douyin

Supported forms:

- `https://v.douyin.com/.../`
- `https://www.douyin.com/video/<aweme_id>`
- `https://www.douyin.com/note/<id>`
- `https://www.iesdouyin.com/share/video/<aweme_id>/`

Extraction sequence:

1. Resolve short links with mobile/browser-like UA.
2. Extract `aweme_id` or note ID.
3. Fetch share page or canonical page.
4. Parse `window._ROUTER_DATA` when present.
5. If browser is available, inspect:
   - `document.body.innerText`
   - meta tags
   - `performance.getEntriesByType('resource')`
6. Look for:
   - title/description
   - author
   - publish time
   - statistics
   - chapter points
   - visible text/captions
   - signed audio/video URLs
7. Download public media only when accessible.
8. Run ASR if possible.
9. If download/ASR fails, write available evidence and mark limitations.

Common failure types:

- `风控反爬`
- `登录限制`
- `链接失效`
- `媒体不可下载`
- `ASR失败`

## Xiaohongshu

Supported forms:

- `https://xhslink.com/...`
- `https://www.xiaohongshu.com/discovery/item/<note_id>`
- `https://www.xiaohongshu.com/explore/<note_id>`

Extraction sequence:

1. Resolve short link.
2. Extract note ID.
3. Fetch public SSR HTML.
4. Parse initial state for:
   - type
   - title
   - desc
   - author
   - tags
   - publish/update time
   - interaction info
   - video streams
5. For text/image notes, use visible/source note text as evidence.
6. For video notes, download public stream and ASR when feasible.
7. Risk/login pages should become `待复核`, not hallucinated summaries.

## WeChat Official Account

Supported form:

- `https://mp.weixin.qq.com/s/...`

Extraction sequence:

1. Fetch HTML with mobile WeChat/browser-like UA.
2. Extract metadata from inline variables and meta tags:
   - `msg_title`
   - `nickname`
   - `publish_time`
   - `msg_desc`
3. Extract article body around `js_content`.
4. Strip UI/footer artifacts.
5. Preserve paragraph/list structure.
6. Store original article text in Notion body.

Failure handling:

- Deleted/private/restricted article → checkpoint + `待复核` or `失败` depending on whether metadata exists.
