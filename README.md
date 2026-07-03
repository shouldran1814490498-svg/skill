# 药品社媒外投全流程技能合集

一站式药品社交媒体投放技能包，涵盖策略生成、达人筛选、达人排期、内容生成&审核、比价核验全链路，支持单独使用或流水线自动编排。

## 技能清单

| 技能 | 触发命令 | 功能 |
|------|----------|------|
| 策略生成 | `/strategy {药品名}` | 输入药品名，输出完整社媒投放策略报告 |
| 达人筛选 | `/kol-screen {参数}` | 根据策略和预算自动筛选达人、生成看板 |
| 达人排期 | `/schedule {达人列表} {投放周期}` | 为筛选后的达人自动分配发布日期 |
| 内容生成&审核 | `/xhs {达人表} {策略报告}` | 为每位达人生成个性化笔记并合规审核 |
| 比价核验 | `/quote-audit {PO单} {基准库}` | 对比供应商报价与基准价格，输出风险报告 |
| 全流程编排 | `/pipeline full {参数}` | 一键串联以上技能，自动传递数据 |

## 数据流

```
策略生成 ──→ 达人筛选 ──→ 达人排期 ──→ 内容生成&审核
                │
                └──→ 比价核验（可选）
```

## 安装方式

本技能包通过手动下载安装到 Claude Code 的 `.claude/commands/` 目录。

### 方式一：一键脚本安装（推荐）

打开 Claude Code，直接说：

> 帮我从 https://github.com/shouldran1814490498-svg/skill 下载所有 skill 到本地

Claude Code 会自动 clone 仓库并将文件放到正确位置。

### 方式二：手动安装

1. 克隆仓库到任意位置：
   ```
   git clone https://github.com/shouldran1814490498-svg/skill.git
   ```

2. 将以下文件复制到你的 `~/.claude/commands/` 目录（Windows 为 `%USERPROFILE%\.claude\commands\`）：

   | 源文件 | 目标文件名 |
   |--------|-----------|
   | `外投策略生成skill/SKILL.md` | `strategy.md` |
   | `外投达人筛选skill/医生达人筛选看板_Skill.md` | `kol-screen.md` |
   | `外投排期skill/SKILL.md` | `schedule.md` |
   | `外投小红书内容生成&审核skill/SKILL.md` | `xhs.md` |
   | `外投比价skill/SKILL.md` | `quote-audit.md` |
   | `pipeline/pipeline.md` | `pipeline.md` |

3. 将 `外投策略生成skill/scripts/` 目录下的所有文件复制到 `~/.claude/commands/scripts/`

### 方式三：自动更新（安装后持续同步）

安装时可以让 Claude Code 配置自动同步 hook，这样 GitHub 仓库有更新时本地会自动拉取最新版本：

> 帮我配置 skill 自动同步，仓库地址是 https://github.com/shouldran1814490498-svg/skill

配置后每次使用 Claude Code 时会自动检查更新（每小时最多一次）。

## 验证安装

安装完成后，在 Claude Code 中输入以下命令验证：

```
/strategy
/kol-screen
/schedule
/xhs
/quote-audit
/pipeline
```

如果能看到对应的 skill 说明，即安装成功。

## 目录结构

```
├── README.md                          ← 本文件
├── 安装与使用指南.md                    ← 详细使用教程
├── .claude-plugin/
│   └── plugin.json
├── 外投策略生成skill/
│   ├── SKILL.md
│   ├── README.md
│   └── scripts/                       ← 策略报告生成引擎
├── 外投达人筛选skill/
│   └── 医生达人筛选看板_Skill.md
├── 外投排期skill/
│   └── SKILL.md
├── 外投小红书内容生成&审核skill/
│   ├── SKILL.md
│   └── README.md
├── 外投比价skill/
│   ├── SKILL.md
│   └── README.md
└── pipeline/
    └── pipeline.md                    ← 全流程编排定义
```

## 作者

[@shouldran1814490498-svg](https://github.com/shouldran1814490498-svg)
