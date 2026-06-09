# Retry and State Machine

## States

```text
待处理
提取中
已整理
待复核
失败
```

## State Meaning

- `待处理`: captured but extraction not started.
- `提取中`: extraction or writing is currently in progress.
- `已整理`: enough evidence exists and Notion write is verified.
- `待复核`: saved but content evidence is partial/blocked.
- `失败`: terminal failure or unsupported/invalid input.

## Retry Rules

Retryable:

- transient network timeout;
- HTTP 429/5xx;
- TLS EOF;
- temporary browser load failure;
- ASR model download timeout if another local/cached model exists.

Not retryable with same strategy:

- login required;
- risk-control/captcha page;
- deleted/invalid link;
- unsupported platform;
- media URL expired and cannot be rediscovered;
- Notion permission denied until user fixes sharing.

## Recommended Attempts

- Network fetch: 2-3 short retries.
- Media download: 1 retry after rediscovering URL.
- ASR: 1 retry with smaller/local model if available.
- Notion write: 1 retry for transient network/TLS; no retry for validation/permission errors.

## Interruption Handling

If a run is interrupted:

1. Re-read Notion row.
2. Check local cache manifest/artifacts.
3. Determine last phase.
4. Resume from latest stable artifact.
5. Do not label as `失败` unless extraction actually failed.

## Failure Types

Use a `失败类型` field when available, otherwise write these into `处理日志`:

- `登录限制`
- `风控反爬`
- `链接失效`
- `媒体不可下载`
- `ASR失败`
- `内容证据不足`
- `Notion权限错误`
- `Notion字段缺失`
- `不支持平台`
