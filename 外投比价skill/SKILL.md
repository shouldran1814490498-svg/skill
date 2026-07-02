---
name: external-quote-audit
description: Audit external creator/media-buying supplier PO quotes and settlement prices against the regularly updated JOYspace 蒲公英平台报价库 online sheet, or a user-provided offline export when online access is unavailable. Use when the user asks to核验/比价/审核 外投报价, 供应商PO报价, 达人/博主报价, 结算单价, 蒲公英报价库, JOYspace在线文档, CPM/CPE, or to judge whether a supplier quote is reasonable from Excel/CSV/online-sheet quote data.
---

# External Quote Audit

## Overview

Use this skill to audit whether an external supplier's creator quote is reasonable by comparing supplier PO quotes or settlement prices against the user's regularly updated quote database.

The primary benchmark is the JOYspace online sheet:

`https://joyspace.jd.com/sheets/zLYydbGAzSAEUNscQaL3?themeColor=maxdeep&env=timline&lang=zh_CN`

Prefer querying the JOYspace online document for the latest data. Use an uploaded Excel export only when online access is unavailable, the user requests a historical/offline version, or the user explicitly supplies an export for this audit.

Before auditing the database, read `references/database-schema.md`.

## Inputs

Accept any combination of:

- Supplier PO quotation sheet: creator name/ID/link, content format, quote amount, quote date or campaign month, supplier name.
- Supplier settlement sheet: creator name/ID/link, settlement unit price, quantity, settlement date/month, optional CPM/CPE/views/interactions.
- Benchmark source: JOYspace online quote sheet first; latest exported `蒲公英平台报价库.xlsx` only as fallback.
- Optional custom benchmark/rate-card sheet. If present, prefer it over derived assumptions.

If online access to JOYspace fails because of network, login, or permission limits, state the issue and ask for one fallback: latest Excel export, copied table rows, screenshots, or access/permission. Do not claim to have checked the latest database unless the online document was actually accessed.

## Workflow

1. Determine benchmark source: JOYspace online sheet first; offline export only as fallback or when explicitly requested.
2. Record benchmark source, query/read time, and whether the data is latest online data or an offline snapshot.
3. Load PO/settlement files and benchmark data. List sheets, row counts, and columns.
4. Standardize columns into: `creator_name`, `creator_id`, `profile_url`, `platform`, `content_format`, `fan_count`, `quote_price`, `settlement_price`, `quote_month`, `supplier`, `avg_views`, `avg_reads`, `avg_interactions`, `cpm`, `cpe`.
5. Normalize numbers: money is RMB; parse `w`/`万` suffixes only when the cell value contains the suffix; for fields named `粉丝数/w`, keep the numeric value as 万粉 for display and multiply by 10,000 only when computing fan tiers; treat `-`, `/`, `暂无`, blanks, and non-numeric values as missing.
6. Match each supplier row to the benchmark.
7. Calculate comparisons and risk flags.
8. Return a Markdown report with auditable details and follow-up actions.

## Matching Rules

Use deterministic matching and disclose the matched basis.

Priority:

1. Exact `creator_id` / `小红书id` match.
2. Exact normalized `profile_url` match. Ignore URL query parameters where possible.
3. Exact creator name match after trimming whitespace and normalizing full-/half-width punctuation.
4. Fuzzy creator name match only if there is a single high-confidence candidate. If multiple candidates exist, mark `⚠️ 需人工确认匹配`.

For Xiaohongshu 蒲公英 rows, prefer sheet `达人list`. For non-Xiaohongshu or missing 蒲公英 data, use other reference sheets as comparable market references, but label them as `外部参考价` rather than `蒲公英平台价`.

For every matched row, preserve the data source: `JOYspace在线文档`, `离线导出Excel`, `截图/复制表格`, or other user-supplied source. Include the query/read time in the final report.

## Price Selection

Choose benchmark price by content format:

- `图文`: compare against `图文笔记一口价`.
- `视频`: compare against `视频笔记一口价`.
- Unknown format with only one available benchmark price: use that price and disclose the assumption.
- Unknown format with both 图文/视频 prices: report both and mark `⚠️ 需确认内容形式`; do not give final approval.

For fields such as `5月执行价格`, `价格`, or `参考价（需二核）`, treat them as market reference prices. Do not call them 蒲公英 prices unless they come from `达人list` price columns.

## Risk Rules

### Supplier quote vs benchmark

Calculate `quote_ratio = supplier_quote / benchmark_price`.

- `🔴 倒挂`: quote ratio > 100%; supplier quote is above benchmark.
- `✅ 合理`: 80% <= quote ratio <= 100%.
- `⚠️ 低价需核实`: 50% <= quote ratio < 80%; verify deliverables, account quality, and pricing basis.
- `🔴 严重低报/口径异常`: quote ratio < 50%; verify account/platform/content-format matching.
- `⚠️ 无可比数据`: no reliable benchmark match or benchmark price is missing.

### Settlement vs PO

If both settlement and PO are provided:

- Match by creator ID/name/link plus batch/campaign month when available.
- `🔴 结算超PO`: settlement unit price > approved PO price.
- `✅ 一致`: equal or within user-specified tolerance. If no tolerance is given, use exact equality after rounding to 2 decimals.
- `⚠️ 结算低于PO`: settlement unit price < PO price; explain discount, cancellation, or changed deliverable.
- `⚠️ 缺失PO记录`: settlement row has no corresponding PO.

### CPM / CPE

Use uploaded CPM/CPE if provided. If missing, calculate when possible:

- `CPM = price / avg_views * 1000`
- `CPE = price / avg_interactions`

For Xiaohongshu:

- 图文: prefer `预估CPM图文` and `预估阅读单价图文`.
- 视频: prefer `预估CPM视频` and `预估阅读单价视频`.

For external reference sheets, derive a comparison only from same/similar platform, content format, fan tier, and category when enough samples exist. Label this as `同类样本估算`, not exact platform quote.

## Output

Return a Markdown report.

Start with:

- 场景类型
- 使用文件
- 报价库来源: `JOYspace在线文档` / `离线导出Excel` / other
- 报价库查询或读取时间
- 使用数据库 sheet
- 核验总数
- 精确匹配数
- 需人工确认匹配数
- 无可比数据数
- 综合风险等级: `🔴 高风险`, `⚠️ 中风险`, or `✅ 低风险`

Then provide a detail table:

| 达人/账号 | 平台 | 内容形式 | 匹配依据 | 基准来源 | 供应商报价/结算价 | 基准价格 | 报价比值 | CPM | CPE | 风险 | 说明 |
|---|---|---|---|---|---:|---:|---:|---:|---:|---|---|

End with:

- All `🔴` and `⚠️` issues.
- Evidence for each issue.
- Suggested procurement action: approve / negotiate / reject / supplement data / manual match confirmation.
- Key assumptions, especially online access failure, offline snapshot use, missing content format, or derived CPM/CPE.

## Guardrails

- Never invent benchmark data, prices, or industry ranges.
- Prefer the JOYspace online document for latest quote data. If using an offline export, explicitly state that it may not be the latest version.
- Do not pretend the latest JOYspace data was queried if online access failed or was not attempted.
- Do not mix Xiaohongshu 蒲公英 price and Douyin/external reference price without labeling the source.
- Do not approve when content format is unknown and both 图文/视频 benchmarks exist.
- Do not merge same-name accounts across platforms unless ID/link confirms the same account.
- Preserve source sheet, source field, match basis, and query/read time so the user can audit the result.
