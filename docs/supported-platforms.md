# 支持平台与能力边界

## 第一版支持

### 抖音

支持链接示例：

```text
https://v.douyin.com/xxxx/
https://www.douyin.com/video/123456
https://www.iesdouyin.com/share/video/123456/
```

能力：

- 解析短链；
- 提取公开视频元数据；
- 尝试读取页面可见文本/章节；
- 尝试获取可下载公开视频/音频并 ASR；
- 保存到 Notion。

限制：

- 反爬、登录、地区、IP 风控可能导致提取失败；
- 无法取得视频原文时，只能保存元数据并标记 `待复核`；
- 不保证每条视频都能完整转写。

### 小红书

支持链接示例：

```text
https://xhslink.com/...
https://www.xiaohongshu.com/discovery/item/...
https://www.xiaohongshu.com/explore/...
```

能力：

- 解析短链；
- 尝试提取 SSR 公开元数据；
- 尝试提取图文正文；
- 尝试下载公开视频并 ASR；
- 保存到 Notion。

限制：

- 小红书可能出现 IP 风险、登录、页面风控；
- 风控时会创建 Notion 检查点并标记 `待复核`。

### 微信公众号

支持链接示例：

```text
https://mp.weixin.qq.com/s/xxxx
```

能力：

- 抓取公开文章 HTML；
- 提取标题、作者、摘要、正文；
- 生成文章知识卡片；
- 保存原文和整理版到 Notion。

限制：

- 已删除、需登录、被限制访问的文章无法完整提取；
- 部分文章可能缺少发布时间或作者字段。

## 暂不支持

- YouTube
- B站
- 快手
- 视频号
- TikTok
- Instagram
- 私密内容
- 需要登录后才能访问的内容
- 100% 保证视频完整转写

## 处理原则

如果无法获取足够内容证据，Bot 应该：

1. 保存原始链接；
2. 保存可用元数据；
3. 设置 `处理状态 = 待复核`；
4. 在 `处理日志` 中说明原因；
5. 不编造完整总结。
