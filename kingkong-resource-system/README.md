# 药师金刚资源位管理系统

这是一个运行在 Cloudflare Workers 上的全栈系统，使用 Vinext/Next.js 构建，并通过 Cloudflare D1 保存共享的提报、排期、询价指标和操作记录。

## 本地开发

```bash
pnpm install
pnpm dev
```

## Cloudflare 部署

1. 登录 Cloudflare：`pnpm exec wrangler login`
2. 创建 D1 数据库：`pnpm exec wrangler d1 create jd-health-kingkong-resource-db`
3. 将返回的 `database_id` 写入 `wrangler.jsonc`
4. 执行迁移：`pnpm run cf:migrate`
5. 部署：`pnpm run deploy`

`drizzle/0002_migrate_sites_data.sql` 包含从原站点迁移的初始数据。
