---
name: creator-publish-scheduler
description: Automatically schedule publication dates for already-filtered creators/KOLs based on a project period and a creator list CSV/XLSX. Use when the user asks to为达人排期/外投达人排期/确定帖子发布日期/生成达人发布日历, especially when the list contains 最近月份 and 科室 fields and outputs should include a CSV with 发布日期, a JOYspace-ready table, and an HTML scheduling rationale report.
---

# Creator Publish Scheduler

## Overview

Create balanced creator posting schedules from a project period and a creator list. Use the creator list's `最近月份` and `科室` fields, then intelligently adjust publication density around ecommerce nodes, weekends/holidays, and medically relevant disease/health awareness days.

## Required inputs

Ask for missing required inputs before producing final files:

- Project period with start and end dates. If the user says “今日”, resolve it using the current local date and state the resolved date.
- Creator list as CSV/XLSX. Expected standard columns include `达人昵称`, `ID`, `主页链接`, `科室`, `粉丝(w)`, `层级`, and `最近月份`; only `达人昵称`, `科室`, and `最近月份` are essential for scheduling.

Optional but useful inputs:

- Product/brand/campaign name for output filenames and report title.
- Platform, desired total cadence, daily maximum, blackout dates, or must-hit dates.
- Whether the schedule should favor weekday release, weekend release, promotion bursts, or medical education rhythm.

## Workflow

1. Inspect the creator list schema and row count. Preserve all original columns and row order unless the user asks to sort.
2. Parse and normalize the project period. Every assigned `发布日期` must be within the period.
3. Interpret `最近月份` as the creator's latest posting/cooperation month. Use it to avoid clustering recently active creators too tightly and to spread creators with the same recent-month bucket across the whole period.
4. Research and assemble scheduling nodes for the project period:
   - Ecommerce nodes: 618, 双11, 双12, 年货节, 开学季, 大促预热/爆发/返场 windows when relevant.
   - Calendar nodes: weekends and official public holidays/adjusted workdays for the campaign year.
   - Medical/health days: only boost dates when the creator `科室` has a strong relationship to that disease/health day.
5. Apply the detailed rules in `references/scheduling-policy.md`.
6. Generate three deliverables:
   - CSV: original table plus exactly one new column named `发布日期`, formatted as `YYYY-MM-DD`.
   - JOYspace table: upload/create at `https://joyspace.jd.com/h/receive` when the environment has browser/network/auth access. If not possible, create a JOYspace-ready CSV/XLSX and clearly say it is ready for manual upload.
   - HTML report: readable report explaining the scheduling logic, nodes used, disease-day matching decisions, distribution summary, and any assumptions.
7. Use encoding-safe generation for Chinese files. On Windows/PowerShell, do not pass long Chinese HTML/Python source through inline shell command text because the console code page may replace characters with `?`. Prefer one of:
   - create/edit a UTF-8 `.py` script with `apply_patch`, then execute it;
   - use Python string values loaded from UTF-8 files;
   - use Unicode escape sequences only when writing short inline snippets is unavoidable.
8. Validate before handing off:
   - Row count unchanged.
   - Every row has one valid `发布日期`.
   - Dates are inside the project period.
   - The CSV keeps the original columns and adds `发布日期`.
   - Report explains why node boosts were or were not used.
   - HTML source includes `<meta charset="utf-8">`.
   - The generated HTML contains no suspicious replacement text such as repeated `????`, especially in headings, table headers, and rationale paragraphs.

## Output conventions

Use stable Chinese filenames when possible:

- `<项目名或产品名>_达人排期.csv`
- `<项目名或产品名>_达人排期_joyspace.csv` or `.xlsx` when direct JOYspace upload is unavailable
- `<项目名或产品名>_达人排期报告.html`

If no product/campaign name is provided, derive a concise name from the source filename.

## Research and citation requirements

Node and disease-day information can change by year. When the runtime supports internet access, verify current-year official holidays and health/disease-day dates using reliable sources, then include source URLs and query date in the HTML report. If browsing is unavailable, use well-known fixed dates only when confident, mark them as “未联网复核”, and avoid aggressive boosts based on uncertain nodes.

## Encoding guardrail

When generating Chinese CSV/HTML on Windows:

- Write CSV with `encoding="utf-8-sig"` so Excel opens Chinese correctly.
- Write HTML with `encoding="utf-8"` and `<meta charset="utf-8">`.
- Avoid inline PowerShell commands containing substantial Chinese text. If a report or script contains Chinese prose, save it as a UTF-8 file first and run/read that file.
- After writing the HTML, reopen it as UTF-8 and inspect the first lines plus all headings. If `?` appears in place of Chinese text, regenerate before handing off.
