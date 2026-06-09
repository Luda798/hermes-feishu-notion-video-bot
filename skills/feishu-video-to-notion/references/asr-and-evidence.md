# ASR and Evidence Reference

## Evidence Grades

### High

Use `已整理` when one of these exists:

- complete WeChat article body;
- full visible note text;
- official/native captions;
- full ASR transcript reviewed for obvious errors.

### Medium

Usually `已整理` with caveat or `待复核` depending on richness:

- detailed platform chapter points;
- visible subtitle snippets;
- rich public description;
- partial transcript.

### Low

Use `待复核`:

- title only;
- author/source only;
- cover/statistics only;
- generic metadata without content substance.

### None

Use `失败` or `待复核`:

- link inaccessible;
- deleted content;
- unsupported private content.

## ASR Workflow

1. Prefer official/native captions first.
2. If no captions, use downloadable public media.
3. Prefer local ASR for privacy when available.
4. Use language/domain prompt when helpful.
5. Review output for:
   - Simplified/Traditional consistency;
   - obvious homophones;
   - repeated loops;
   - broken timestamps;
   - product/person/platform names.
6. Label as `ASR转写，非官方字幕`.
7. Add caveat in reliability section.

## When ASR Fails

- Keep checkpoint.
- Save metadata and visible text.
- Set `待复核` if no enough evidence.
- Record `ASR失败` or `媒体不可下载`.
- Ask user for a fresh link, screenshot, or manual transcript if needed.

## Reliability Language

Examples:

```text
内容来源：公众号公开正文，可靠性较高。
```

```text
内容来源：公开视频音频 ASR 转写，非官方字幕，可能存在同音词或专有名词误差。
```

```text
内容来源：公开页面标题、描述和章节要点，未取得完整视频原文，建议人工复核。
```
