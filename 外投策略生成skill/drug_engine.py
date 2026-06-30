#!/usr/bin/env python3
"""
药品社媒投放策略分析引擎 v2.1
新结构: 一、基础档案(含不良反应/社媒热点/竞品对比)
        二、发展阶段分析(5阶段框架指导投放重点)
        三、利益点拆解(融合用户画像+植入建议)
        四、投放策略框架(达人矩阵+传播逻辑+投放节奏+预算)
        五、总结
"""
import json, os, shutil, subprocess, tempfile
from datetime import datetime

TEMP_DIR = tempfile.mkdtemp(prefix="drug_report_")


def esc(val):
    """HTML安全转义"""
    v = (val or "")
    v = v.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    return v.replace("\n", "<br>")


def hx(val):
    return esc(val)


# ============================================================
# MARKDOWN 生成
# ============================================================
def generate_report(data: dict) -> str:
    d = data
    lines = []

    lines.append(f"# 🎯 {d.get('drug_name','')} - 社媒投放策略报告")
    lines.append(f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("> 投放策略仅供参考\n")

    # ===================== 一、药品基础档案 =====================
    lines.append("## 一、药品基础档案\n")

    info_items = [
        ("药品名称", "trade_name"), ("通用名", "generic_name"),
        ("生产厂家", "manufacturer"), ("药品类别", "drug_category"),
        ("适应症", "indication"),
        ("作用机制（通俗版）", "mechanism_simple"),
        ("作用机制（专业版）", "mechanism_detail"),
        ("疗程/用法", "dosage"), ("价格参考", "price_info"),
        ("渠道", "channels"), ("上市状态", "market_status"),
    ]
    for label, key in info_items:
        val = d.get(key, "")
        if val:
            lines.append(f"- **{label}**：{val}")

    # 1.2 不良反应
    ar = d.get("adverse_reactions", "")
    if ar:
        lines.append(f"\n- **不良反应/副作用**：{ar}")

    # 社媒合规提醒
    ctips = d.get("compliance_tips", [])
    if ctips:
        lines.append(f"\n**社媒传播合规提醒：**\n")
        for t in ctips:
            lines.append(f"- ❌ \"{t.get('trap','')}\" → ✅ {t.get('suggest','')}")

    # 1.3 社媒热点
    hotspots = d.get("social_hotspots", [])
    if hotspots:
        lines.append(f"\n**当前社媒热点：**\n")
        for h in hotspots:
            platform = h.get("platform", "")
            topic = h.get("topic", "") or h.get("content", "")
            note = h.get("note", "")
            if topic:
                lines.append(f"- **{platform}**：{topic}{' - ' + note if note else ''}")

    # 1.4 竞品对比
    competitors = d.get("competitors", [])
    if competitors:
        lines.append(f"\n**竞品格局 → 核心优势：**\n")
        lines.append("| 药物 | 厂家 | 价格 | 特点 |")
        lines.append("|------|------|------|------|")
        for c in competitors:
            cname = c.get("name", "") or c.get("brand", "")
            maker = c.get("maker", "")
            price = c.get("price", "")
            cnote = c.get("note", "") or c.get("advantage", "")
            lines.append(f"| {cname} | {maker} | {price} | {cnote} |")
        lines.append("")
        diff = d.get("competitor_advantage", "") or d.get("differentiation_key", "")
        if diff:
            lines.append(f"> **本品核心优势**：{diff}")

    lines.append("\n---\n")

    # ===================== 二、发展階分析 =====================
    lines.append("## 二、药品发展阶段分析\n")
    lines.append(f"**判断依据**：{d.get('stage_analysis','')}\n")
    lines.append(f"**当前阶段**：{d.get('development_stage','')}\n")
    lines.append(f"**投放重点**：{d.get('stage_focus','')}\n")

    lines.append("\n---\n")

    # ===================== 三、产品利益点（融合画像） =====================
    lines.append("## 三、产品利益点拆解 & 社媒语言转化\n")
    benefits = d.get("benefits", [])
    if benefits:
        for i, b in enumerate(benefits, 1):
            bname = b.get("name", "") or b.get("point", "")
            baudience = b.get("audience", "")
            bportrait = b.get("user_portrait", "")
            bcopy = b.get("social_copy", "")
            bplacement = b.get("placement_tip", "")
            bformat = b.get("format_suggestions", "")
            bplatforms = b.get("platforms", "")
            bevidence = b.get("evidence", "")
            bimpli = b.get("implication", "")
            bvalue = b.get("user_value", "")

            lines.append(f"### {i}️⃣ {bname}")
            # 新字段模式 (point/evidence/implication/user_value)
            if bevidence or bimpli or bvalue:
                if bevidence:
                    lines.append(f"- **证据**：{bevidence}")
                if bimpli:
                    lines.append(f"- **意义**：{bimpli}")
                if bvalue:
                    lines.append(f"- **用户语言**：{bvalue}")
            # 旧字段模式 (audience/social_copy/placement_tip等)
            else:
                lines.append(f"- **目标人群**：{baudience}")
                lines.append(f"- **用户画像**：{bportrait}")
                lines.append(f"- **社媒语言**：\"{bcopy}\"")
                lines.append(f"- **植入建议**：{bplacement}")
                lines.append(f"- **建议内容形式**：{bformat}")
                lines.append(f"- **推荐平台**：{bplatforms}")
            lines.append("")

    lines.append("---\n")

    # ===================== 四、投放策略框架 =====================
    lines.append("## 四、投放策略框架\n")

    # 4.1 治疗场景分析
    lines.append("### 4.1 产品/适应症治疗场景分析\n")
    lines.append(d.get("scenario_analysis", ""))
    lines.append("")
    lines.append(f"- **严肃医疗特征**：{d.get('serious_features','')}")
    lines.append(f"- **消费医疗特征**：{d.get('consumer_features','')}")
    lines.append(f"- **结论**：{d.get('scenario_conclusion','')}")
    lines.append("")

    # 用户决策路径
    if d.get("user_behavior"):
        lines.append(f"**搜索行为路径**：{d.get('user_behavior','')}")
    if d.get("decision_path"):
        lines.append(f"**决策链路**：{d.get('decision_path','')}")
    lines.append("")

    # 4.2 达人矩阵
    lines.append("### 4.2 达人矩阵投放占比\n")
    km = d.get("kol_matrix", {})
    # types_map 提到外面，4.3 也要用
    types_map = {
        "official_media": "官媒/品牌号",
        "doctor_kol": "医生/专家KOL",
        "non_medical_koc": "非医KOC/KOL",
        "patient_kol": "患者KOL/真实用户",
    }
    if km:
        lines.append("| 达人类型 | 占比 | 角色定位 |")
        lines.append("|---------|------|---------|")
        for key, label in types_map.items():
            t = km.get(key, {})
            if t.get("pct"):
                lines.append(f"| **{label}** | {t['pct']} | {t.get('strategy','')} |")
        lines.append("")

    # 4.3 每种达人策略 + 脚本示意 + 传播逻辑
    lines.append("### 4.3 达人投放策略 & 脚本示意\n")
    # 传播逻辑整体先展示
    if d.get("propagation_logic"):
        lines.append(f"> **核心传播逻辑**：{d['propagation_logic']}\n")

    for key, label in types_map.items():
        t = km.get(key, {})
        if t.get("pct"):
            lines.append(f"**{label}（{t['pct']}）**")
            lines.append("")
            lines.append(f"- 投放策略：{t.get('strategy','')}")
            if t.get("example_script"):
                lines.append(f"- 脚本示意：{t.get('example_script','')}")
            lines.append("")

    # 4.4 投放节奏
    lines.append("### 4.4 投放节奏\n")
    budget = d.get("budget", "")
    budget_duration = d.get("budget_duration", "")
    if budget or budget_duration:
        lines.append(f"> **总预算**：{budget or '—'}　|　**投放周期**：{budget_duration or '—'}\n")
    tactics = d.get("phase_tactics", [])
    if tactics:
        lines.append("| 阶段 | 周期 | 核心任务 | 内容方向 | 预算占比 |")
        lines.append("|------|------|---------|---------|---------|")
        for t in tactics:
            lines.append(f"| **{t.get('phase','')}** | {t.get('duration','')} | {t.get('core_task','')} | {t.get('content_direction','')} | {t.get('budget_pct','')} |")
        lines.append("")
        lines.append("> 线上处方闭环贯穿全周期，转化收割期适合重点用体验分享类内容做持续投放。")
    else:
        lines.append("（用户未提供预算，未生成详细节奏；如需请联系确认预算后补充）\n")

    # 4.5 预算细化（有预算时）
    if d.get("budget_detail"):
        lines.append("### 4.5 传播节奏细化（有预算）\n")
        lines.append(d.get("budget_detail", ""))
        lines.append("")

    # 平台推荐
    platforms = d.get("platforms", [])
    if platforms:
        lines.append("**平台推荐：**\n")
        for p in platforms:
            lines.append(f"- **{p.get('name','')}** {p.get('stars','')} - {p.get('reason','')}")
        lines.append("")

    # 内容方向
    cmap = d.get("content_mapping", [])
    if cmap:
        lines.append("**内容方向 & 利益点匹配：**\n")
        lines.append("| 内容方向 | 对应利益点 | 适合平台 | 合规风险 |")
        lines.append("|---------|-----------|---------|---------|")
        for cm in cmap:
            plat = cm.get("platforms", "") or cm.get("platform", "")
            lines.append(f"| {cm.get('direction','')} | {cm.get('benefits','')} | {plat} | {cm.get('risk','')} |")
        lines.append("")

    # 合规
    compliance = d.get("compliance", [])
    if compliance:
        lines.append("**合规注意事项：**\n")
        for cl in compliance:
            lines.append(f"- ❌ \"{cl.get('avoid','')}\" → ✅ \"{cl.get('suggest','')}\"")
        lines.append("")

    lines.append("---\n")

    # ===================== 五、总结 =====================
    lines.append("## 五、总结\n")
    lines.append(d.get("summary", "") or d.get("unique_opportunities", ""))
    lines.append("")
    lines.append("---")
    lines.append("*投放策略仅供参考*")

    return "\n".join(lines)


# ============================================================
# HTML 生成
# ============================================================
def generate_html(data: dict) -> str:
    d = data
    name = d.get("drug_name", "")
    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    # 基础信息
    info_rows = ""
    for label, key in [
        ("药品名称", "trade_name"), ("通用名", "generic_name"),
        ("生产厂家", "manufacturer"), ("药品类别", "drug_category"),
        ("适应症", "indication"),
        ("作用机制（通俗版）", "mechanism_simple"),
        ("作用机制（专业版）", "mechanism_detail"),
        ("疗程/用法", "dosage"), ("价格参考", "price_info"),
        ("渠道", "channels"), ("上市状态", "market_status"),
    ]:
        val = d.get(key, "")
        if val:
            info_rows += f'<tr><td class="label">{hx(label)}</td><td>{hx(val)}</td></tr>'

    # 不良反应
    ar = d.get("adverse_reactions", "")
    if ar:
        info_rows += f'<tr><td class="label">不良反应</td><td>{hx(ar)}</td></tr>'

    # 社媒合规提醒
    ctips = d.get("compliance_tips", [])
    if ctips:
        tips_html = "".join(
            f'<div style="margin:4px 0;font-size:13px;">❌ "{hx(t.get("trap",""))}" → ✅ <span style="color:#27ae60;">{hx(t.get("suggest",""))}</span></div>'
            for t in ctips
        )
        info_rows += f'<tr><td class="label">社媒传播合规提醒</td><td>{tips_html}</td></tr>'

    # 社媒热点
    hotspots = d.get("social_hotspots", [])
    if hotspots:
        hs_html = "".join(
            f'<div style="margin:4px 0;font-size:13px;">📍 <strong>{hx(h.get("platform",""))}</strong>：{hx(h.get("topic","") or h.get("content",""))}{(" - " + hx(h.get("note",""))) if h.get("note") else ""}</div>'
            for h in hotspots
        )
        info_rows += f'<tr><td class="label">当前社媒热点</td><td>{hs_html}</td></tr>'

    # 竞品
    competitors = d.get("competitors", [])
    if competitors:
        comp_rows_v2 = ""
        for c in competitors:
            cname = c.get("name", "") or c.get("brand", "")
            cnote = c.get("note", "") or c.get("advantage", "")
            comp_rows_v2 += f'<tr><td>{hx(cname)}</td><td>{hx(c.get("maker",""))}</td><td>{hx(c.get("price",""))}</td><td>{hx(cnote)}</td></tr>'
        diff = d.get("competitor_advantage", "") or d.get("differentiation_key", "")
        diff_html = f'<div style="margin-top:12px;padding:12px 16px;background:#e8f4fd;border-radius:10px;font-size:14px;"><strong>本品核心优势：</strong>{hx(diff)}</div>' if diff else ""
        comp_section = f'''
        <h3 style="font-size:16px;margin:20px 0 12px;">竞品格局 → 核心优势</h3>
        <table class="info-table"><tr><th>药物</th><th>厂家</th><th>价格</th><th>特点</th></tr>{comp_rows_v2}</table>
        {diff_html}
        '''
    else:
        comp_section = ""

    # 利益点
    benefits = d.get("benefits", [])
    benefits_html = ""
    for i, b in enumerate(benefits, 1):
        bname = b.get("name", "") or b.get("point", "")
        bevidence = b.get("evidence", "")
        bimpli = b.get("implication", "")
        bvalue = b.get("user_value", "")
        baudience = b.get("audience", "")
        bportrait = b.get("user_portrait", "")
        bcopy = b.get("social_copy", "")
        bplacement = b.get("placement_tip", "")
        bformat = b.get("format_suggestions", "")
        bplatforms = b.get("platforms_benefit", "") or b.get("platforms", "")
        
        # 新结构 (evidence/implication/user_value)
        if bevidence or bimpli or bvalue:
            details = ""
            if bevidence:
                details += f'<div class="benefit-row"><span class="bl">📊 证据</span><span class="bv">{hx(bevidence)}</span></div>'
            if bimpli:
                details += f'<div class="benefit-row"><span class="bl">💡 意义</span><span class="bv">{hx(bimpli)}</span></div>'
            if bvalue:
                details += f'<div class="benefit-row"><span class="bl">🗣️ 用户语言</span><span class="bv">{hx(bvalue)}</span></div>'
            benefit_body = f'<div class="benefit-title">{hx(bname)}</div>{details}'
        else:
            benefit_body = f'''
            <div class="benefit-title">{hx(bname)}</div>
            <div class="benefit-row"><span class="bl">目标人群</span><span class="bv">{hx(baudience)}</span></div>
            <div class="benefit-row"><span class="bl">用户画像</span><span class="bv">{hx(bportrait)}</span></div>
            <div class="benefit-row"><span class="bl">社媒语言</span><span class="bv quote">"{hx(bcopy)}"</span></div>
            <div class="benefit-row"><span class="bl">植入建议</span><span class="bv">{hx(bplacement)}</span></div>
            <div class="benefit-row"><span class="bl">建议内容形式</span><span class="bv">{hx(bformat)}</span></div>
            <div class="benefit-row"><span class="bl">推荐平台</span><span class="bv">{hx(bplatforms)}</span></div>
            '''
        
        benefits_html += f'''
        <div class="benefit-card">
            <div class="benefit-num">{i}️⃣</div>
            <div class="benefit-body">
                {benefit_body}
            </div>
        </div>
        '''

    # 达人矩阵
    km = d.get("kol_matrix", {})
    types_map = {"official_media": "官媒/品牌号", "doctor_kol": "医生/专家KOL", "non_medical_koc": "非医KOC/KOL", "patient_kol": "患者KOL/真实用户"}
    km_rows = ""
    km_detail = ""
    for key, label in types_map.items():
        t = km.get(key, {})
        if t.get("pct"):
            km_rows += f'<tr><td><strong>{hx(label)}</strong></td><td>{hx(t["pct"])}</td><td>{hx(t.get("strategy",""))}</td></tr>'
            script = hx(t.get("example_script", ""))
            if script:
                km_detail += f'<div class="kol-detail"><strong>{hx(label)}（{hx(t["pct"])}）</strong><div class="km-strategy">{hx(t.get("strategy",""))}</div><div class="km-script">📝 {script}</div></div>'

    # 投放节奏
    tactics = d.get("phase_tactics", [])
    budget = d.get("budget", "")
    budget_duration = d.get("budget_duration", "")
    budget_banner = ""
    if budget or budget_duration:
        budget_banner = (
            f'<div style="margin-bottom:12px;padding:12px 16px;background:#eef7ee;border-radius:10px;font-size:14px;">'
            f'<strong>总预算：</strong>{hx(budget or "—")}　|　<strong>投放周期：</strong>{hx(budget_duration or "—")}</div>'
        )
    tactics_rows = ""
    for t in tactics:
        tactics_rows += f'<tr><td><strong>{hx(t.get("phase",""))}</strong></td><td>{hx(t.get("duration",""))}</td><td>{hx(t.get("core_task",""))}</td><td>{hx(t.get("content_direction",""))}</td><td>{hx(t.get("budget_pct",""))}</td></tr>'

    # 平台
    platforms = d.get("platforms", [])
    plat_html = ""
    for p in platforms:
        pname = hx(p.get("name", ""))
        ppct = hx(p.get("pct", "") or p.get("stars", ""))
        preason = hx(p.get("reason", ""))
        head = f'{pname}{(" · " + ppct) if ppct else ""}'
        body = f'<div style="font-size:12px;color:#666;margin-top:3px;">{preason}</div>' if preason else ""
        plat_html += f'<div class="pill" style="display:block;margin:6px 0;">{head}{body}</div>'

    # 内容映射
    cmap = d.get("content_mapping", [])
    cmap_rows = ""
    for cm in cmap:
            plat = cm.get("platforms", "") or cm.get("platform", "")
            cmap_rows += f'<tr><td>{hx(cm.get("direction",""))}</td><td>{hx(cm.get("benefits",""))}</td><td>{hx(plat)}</td><td><span class="risk-{cm.get("risk","低")}">{hx(cm.get("risk","低"))}</span></td></tr>'

    # 合规
    compliance = d.get("compliance", [])
    comp_rows2 = ""
    for cl in compliance:
        comp_rows2 += f'<tr><td class="avoid">{hx(cl.get("avoid",""))}</td><td class="suggest">{hx(cl.get("suggest",""))}</td></tr>'

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{hx(name)} - 社媒投放策略报告</title>
<style>
@page {{ margin: 1.2cm; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:'WenQuanYi Micro Hei','PingFang SC','Noto Sans SC','Microsoft YaHei',sans-serif; color:#1a1a2e; background:#f8f9fc; line-height:1.7; }}
.container {{ max-width:960px; margin:0 auto; padding:20px; }}
.header {{ background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460); color:#fff; border-radius:16px; padding:36px 40px; margin-bottom:24px; }}
.header h1 {{ font-size:26px; margin-bottom:6px; }}
.header .sub {{ color:rgba(255,255,255,.65); font-size:13px; }}
.section {{ background:#fff; border-radius:14px; padding:24px 28px; margin-bottom:18px; box-shadow:0 2px 8px rgba(0,0,0,.06); page-break-inside:avoid; }}
.section h2 {{ font-size:19px; margin-bottom:14px; padding-bottom:8px; border-bottom:3px solid #e94560; color:#0f3460; display:flex; align-items:center; gap:8px; }}
table {{ width:100%; border-collapse:collapse; font-size:14px; }}
table th,table td {{ padding:9px 12px; text-align:left; border-bottom:1px solid #eee; vertical-align:top; }}
table th {{ background:#f2f4f8; font-weight:600; color:#444; font-size:13px; }}
table tr:last-child td {{ border-bottom:none; }}
table tr {{ page-break-inside:avoid; }}
.info-table td.label {{ width:130px; font-weight:600; color:#0f3460; white-space:nowrap; }}
.quote {{ color:#e94560; font-style:italic; }}
.pill {{ display:inline-block; background:#e8f0fe; color:#0f3460; padding:5px 14px; border-radius:20px; margin:3px 5px 3px 0; font-size:13px; }}
.risk-低 {{ color:#27ae60; font-weight:600; }}
.risk-中 {{ color:#e67e22; font-weight:600; }}
.risk-高 {{ color:#e74c3c; font-weight:600; }}
.avoid {{ color:#e74c3c; }}
.suggest {{ color:#27ae60; }}
.stage-card {{ background:linear-gradient(135deg,#667eea,#764ba2); color:#fff; border-radius:10px; padding:16px 18px; page-break-inside:avoid; }}
.stage-card2 {{ background:linear-gradient(135deg,#f093fb,#f5576c); }}
.stage-card3 {{ background:linear-gradient(135deg,#4facfe,#00f2fe); }}
.stage-card4 {{ background:linear-gradient(135deg,#11998e,#38ef7d); }}
.benefit-card {{ display:flex; gap:14px; padding:16px 0; border-bottom:1px solid #f0f0f0; }}
.benefit-card:last-child {{ border-bottom:none; }}
.benefit-num {{ font-size:22px; width:40px; text-align:center; flex-shrink:0; }}
.benefit-body {{ flex:1; }}
.benefit-title {{ font-size:16px; font-weight:700; color:#0f3460; margin-bottom:8px; }}
.benefit-row {{ display:flex; margin:3px 0; font-size:13px; }}
.benefit-row .bl {{ width:80px; flex-shrink:0; color:#888; }}
.benefit-row .bv {{ flex:1; color:#444; }}
.kol-detail {{ padding:14px 0; border-bottom:1px solid #f0f0f0; }}
.kol-detail:last-child {{ border-bottom:none; }}
.km-strategy {{ margin:6px 0; font-size:14px; color:#555; }}
.km-script {{ padding:10px 14px; background:#f9f9fb; border-radius:8px; font-size:13px; color:#666; margin-top:6px; }}
.footer {{ text-align:center; color:#999; font-size:12px; padding:20px; }}
@media print {{
    body {{ background:#fff; }}
    .section {{ box-shadow:none; border:1px solid #eee; }}
    .header {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
    .stage-card,.stage-card2,.stage-card3,.stage-card4 {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
}}
</style>
</head>
<body>
<div class="container">

<div class="header">
    <h1>🎯 {hx(name)} - 社媒投放策略情报</h1>
    <div class="sub">生成时间：{hx(now)}</div>
</div>

<!-- 一、基础档案 -->
<div class="section">
    <h2>一、药品基础档案</h2>
    <table class="info-table">{info_rows}</table>
    {comp_section}
</div>

<!-- 二、发展阶段 -->
<div class="section">
    <h2>二、药品发展阶段分析</h2>
    <div style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:14px;">
        <div class="stage-card" style="flex:1;min-width:180px;"><div style="font-size:13px;opacity:.9;">当前阶段</div><div style="font-size:20px;font-weight:700;margin-top:4px;">{hx(d.get('development_stage',''))}</div></div>
        <div class="stage-card stage-card4" style="flex:2;min-width:240px;"><div style="font-size:13px;opacity:.9;">投放重点</div><div style="font-size:16px;font-weight:600;margin-top:4px;">{hx(d.get('stage_focus',''))}</div></div>
    </div>
    <p style="line-height:1.8;color:#555;font-size:14px;"><strong>判断依据：</strong>{hx(d.get('stage_analysis',''))}</p>
</div>

<!-- 三、利益点 -->
<div class="section">
    <h2>三、产品利益点拆解 &amp; 社媒语言转化</h2>
    {benefits_html}
</div>

<!-- 四、投放策略 -->
<div class="section">
    <h2>四、投放策略框架</h2>

    <h3 style="font-size:16px;margin-bottom:10px;">4.1 治疗场景分析</h3>
    <p style="line-height:1.8;color:#555;font-size:14px;">{hx(d.get('scenario_analysis',''))}</p>
    <table style="margin-top:10px;">
        <tr><td style="width:130px;font-weight:600;color:#0f3460;">严肃医疗特征</td><td>{hx(d.get('serious_features',''))}</td></tr>
        <tr><td style="font-weight:600;color:#0f3460;">消费医疗特征</td><td>{hx(d.get('consumer_features',''))}</td></tr>
    </table>
    <div style="margin:12px 0;padding:12px 16px;background:#fef3e2;border-radius:10px;font-weight:600;color:#e67e22;">{hx(d.get('scenario_conclusion',''))}</div>

    <h3 style="font-size:16px;margin:18px 0 10px;">4.2 达人矩阵投放占比</h3>
    <table><tr><th>达人类型</th><th>占比</th><th>角色定位</th></tr>{km_rows}</table>

    <h3 style="font-size:16px;margin:18px 0 10px;">4.3 达人投放策略 &amp; 脚本示意</h3>
    {f'<div style="padding:12px 16px;background:#e8f4fd;border-radius:10px;margin-bottom:14px;font-size:14px;"><strong>核心传播逻辑：</strong>{hx(d.get("propagation_logic",""))}</div>' if d.get('propagation_logic') else ''}
    {km_detail}

    <h3 style="font-size:16px;margin:18px 0 10px;">4.4 投放节奏</h3>
    {budget_banner}
    {"<table><tr><th>阶段</th><th>周期</th><th>核心任务</th><th>内容方向</th><th>预算占比</th></tr>" + tactics_rows + "</table><p style='margin-top:8px;font-size:13px;color:#888;'>线上处方闭环贯穿全周期，转化收割期适合重点用体验分享类内容做持续投放。</p>" if tactics_rows else '<p style="color:#888;font-size:13px;">用户未提供预算，未生成详细节奏；如需请联系确认预算后补充。</p>'}

    {f"""
    <h3 style="font-size:16px;margin:18px 0 10px;">4.5 传播节奏细化</h3>
    <p style="line-height:1.8;font-size:14px;">""" + hx(d.get("budget_detail","")) + """</p>
    """ if d.get("budget_detail") else ''}

    <h3 style="font-size:16px;margin:18px 0 10px;">平台推荐</h3>
    <div class="platform-strip">{plat_html}</div>

    {f'<h3 style="font-size:16px;margin:18px 0 10px;">内容方向 & 利益点匹配</h3><table><tr><th>内容方向</th><th>对应利益点</th><th>适合平台</th><th>合规风险</th></tr>{cmap_rows}</table>' if cmap_rows else ''}

    {f'<h3 style="font-size:16px;margin:18px 0 10px;">合规注意事项</h3><table><tr><th style="width:45%">❌ 避免</th><th>✅ 建议</th></tr>{comp_rows2}</table>' if comp_rows2 else ''}
</div>

<!-- 五、总结 -->
<div class="section">
    <h2>五、总结</h2>
    <p style="line-height:1.8;color:#444;">{hx(d.get("summary","") or d.get("unique_opportunities",""))}</p>
</div>

<div class="footer">
    <p>投放策略仅供参考 · {hx(now)}</p>
</div>

</div>
</body>
</html>'''
    return html


# ============================================================
# PDF 渲染（跨平台兜底：wkhtmltopdf → Chrome → Edge）
# ============================================================
_CHROME_CANDIDATES = [
    "chrome", "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]
_EDGE_CANDIDATES = [
    "msedge", "microsoft-edge", "microsoft-edge-stable",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def _find_executable(candidates):
    """从候选名/绝对路径列表中返回第一个可用的可执行文件路径，找不到返回 None。"""
    for c in candidates:
        is_abs = os.path.sep in c or (len(c) > 1 and c[1] == ":")
        if is_abs:
            if os.path.exists(c):
                return c
        else:
            found = shutil.which(c)
            if found:
                return found
    return None


def _ok(pdf_path):
    return os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0


def _render_pdf(html_path: str, pdf_path: str) -> str:
    """把 HTML 渲染为 PDF。按序探测 wkhtmltopdf → Chrome → Edge，任一成功即返回 pdf_path。
    全部失败时抛 RuntimeError（HTML 文件仍保留可用）。"""
    errors = []

    # 1) wkhtmltopdf（若已安装，质量最佳）
    wk = _find_executable(["wkhtmltopdf"])
    if wk:
        try:
            subprocess.run(
                [wk, "--enable-local-file-access", "--encoding", "utf-8",
                 "--dpi", "300", "--image-dpi", "300", "--image-quality", "94",
                 "--disable-smart-shrinking", "--page-size", "A4",
                 "--margin-top", "14", "--margin-bottom", "14",
                 "--margin-left", "12", "--margin-right", "12",
                 html_path, pdf_path],
                capture_output=True, timeout=60, check=True
            )
            if _ok(pdf_path):
                return pdf_path
        except Exception as e:
            errors.append(f"wkhtmltopdf: {e}")

    # 2) Chrome / 3) Edge —— 二者共用 Chromium headless 的 --print-to-pdf
    for label, cands in (("chrome", _CHROME_CANDIDATES), ("edge", _EDGE_CANDIDATES)):
        exe = _find_executable(cands)
        if not exe:
            continue
        try:
            subprocess.run(
                [exe, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                 f"--print-to-pdf={pdf_path}", os.path.abspath(html_path)],
                capture_output=True, timeout=90, check=True
            )
            if _ok(pdf_path):
                return pdf_path
        except Exception as e:
            errors.append(f"{label}: {e}")

    detail = " | ".join(errors) if errors else "未找到任何 PDF 渲染器（wkhtmltopdf/Chrome/Edge）"
    raise RuntimeError(f"PDF 渲染失败：{detail}。HTML 文件仍可用：{html_path}")


# ============================================================
# 文件操作
# ============================================================
def _sanitize_name(name: str) -> str:
    return name.replace(" ", "_").replace("（","_").replace("）","_").replace("(","_").replace(")","_")

def save_report(drug_name: str, markdown: str) -> str:
    safe = _sanitize_name(drug_name)
    path = os.path.join(TEMP_DIR, f"{safe}_投放策略报告.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(markdown)
    return path


def save_html(drug_name: str, html: str) -> str:
    safe = _sanitize_name(drug_name)
    path = os.path.join(TEMP_DIR, f"{safe}_投放策略报告.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def html_to_pdf(html_path: str) -> str:
    pdf_path = html_path.rsplit(".", 1)[0] + ".pdf"
    return _render_pdf(html_path, pdf_path)


def save_report_rich(data: dict) -> dict:
    """生成报告并保存到临时目录，返回各格式文件路径"""
    md = generate_report(data)
    html = generate_html(data)
    name = data.get("drug_name", "")
    md_path = save_report(name, md)
    html_path = save_html(name, html)
    pdf_path = html_to_pdf(html_path)
    return {"markdown": md_path, "html": html_path, "pdf": pdf_path}


def generate_and_upload_pdf(data: dict) -> str:
    """生成报告 → 转 PDF → 放到临时目录并返回 PDF 路径（调用方负责上传）。"""
    md = generate_report(data)
    html = generate_html(data)
    name = data.get("drug_name", "")

    safe = _sanitize_name(name)
    md_path = os.path.join(TEMP_DIR, f"{safe}_投放策略报告.md")
    html_path = os.path.join(TEMP_DIR, f"{safe}_投放策略报告.html")
    pdf_path = os.path.join(TEMP_DIR, f"{safe}_投放策略报告.pdf")

    os.makedirs(TEMP_DIR, exist_ok=True)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    _render_pdf(html_path, pdf_path)

    return pdf_path


def cleanup_temp():
    """清除临时目录中的所有文件"""
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR, exist_ok=True)


if __name__ == "__main__":
    print("药品投放策略分析引擎 v2.1 (无本地存储)")
    print(f"临时目录: {TEMP_DIR}")
    print("报告通过 generate_and_upload_pdf() 生成后由调用方上传云存储分发")
