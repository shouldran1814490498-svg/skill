# 药品社媒投放策略分析（drug-marketing-strategy）

一个 Claude Code 技能：输入药品名（+可选品牌/厂家），输出一份完整的社媒投放策略报告——产品利益点拆解、治疗场景、用户画像、竞品格局分析。

## 📦 安装

在 Claude Code 里依次执行：

```
/plugin marketplace add Alvinxie323716/drug-marketing-strategy
/plugin install drug-marketing-strategy@alvinxie-skills
```

装完重启 Claude Code（或执行 `/reload-plugins`）即可使用。

## 🔄 开启自动更新（重要，只需开一次）

第三方市场默认**关闭**自动更新，需手动开启一次，之后作者每次发布新版你就自动收到：

1. 输入 `/plugin` 打开菜单
2. 进入 **Marketplaces** 标签
3. 选中 `alvinxie-skills`
4. 选择 **Enable auto-update**

开启后，每次启动 Claude Code 会自动拉取最新版，并提示 `/reload-plugins` 应用。

### 手动更新（没开自动更新时用）

```
/plugin marketplace update alvinxie-skills
/reload-plugins
```

## 💡 用法

安装后，直接对 Claude 说：

- 「分析 XX 药的投放策略」
- 「帮我出 XX 的投放报告」
- 「做 XX 的利益点拆解 / 用户画像分析」

即可触发，输出完整投放策略报告（PDF + 概览摘要）。

## 🖥️ 其它运行环境

- **Joyclaw 平台**：通过 Joyclaw 自己的技能市场上架分发，更新方式为重新安装最新版（不读取 `.claude-plugin/` 清单）。
- **纯手动**：直接 `git clone` 本仓库到 skills 目录，更新即 `git pull`。
