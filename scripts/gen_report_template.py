#!/usr/bin/env python3
"""
药品投放策略报告生成脚本模板
用法：把 data 字典按需要填充，然后：python3 this_script.py
"""

import json, os, sys, tempfile

# Windows 控制台默认 GBK，打印中文/emoji 会崩；强制 UTF-8
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ---------- 引入引擎 ----------
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drug_engine import generate_report, generate_html, cleanup_temp
from drug_engine import _sanitize_name, _render_pdf

# ---------- 请填充此数据字典 ----------
data = {
    "drug_name": "药品名（商品名+通用名）",
    "trade_name": "商品名",
    "generic_name": "通用名（英文）",
    "manufacturer": "厂家",
    "drug_category": "处方药/OTC",
    "indication": "适应症",
    "mechanism_simple": "通俗机制描述，50字以内",
    "mechanism_detail": "专业机制描述",
    "dosage": "用法用量",
    "price_info": "价格参考",
    "channels": "渠道",
    "market_status": "已上市/未上市",
    "adverse_reactions": "不良反应",
    "compliance_tips": [
        {"trap": "社媒禁区用词", "suggest": "安全替代表达"}
    ],
    "social_hotspots": [
        {"platform": "平台名", "content": "相关热点"}
    ],
    "competitors": [
        {"brand": "竞品名", "maker": "厂家", "price": "价格", "advantage": "特点"}
    ],
    "competitor_advantage": "本品核心优势",
    "development_stage": "导入期/成长期/成熟期/维护期",
    "stage_analysis": "阶段判断依据",
    "stage_focus": "当前阶段投放重点",
    "budget": "预算（可选）",
    "budget_duration": "投放周期（可选）",
    "benefits": [
        {
            "point": "利益点名称",
            "evidence": "数据或事实证据",
            "implication": "对用户的意义",
            "user_value": "用用户的语言表达"
        }
    ],
    "scenario_analysis": "治疗场景分析",
    "serious_features": "严肃医疗特征",
    "consumer_features": "消费医疗特征",
    "scenario_conclusion": "消费属性结论",
    "user_behavior": "用户搜索行为路径",
    "decision_path": "决策链路",
    "kol_matrix": {
        "official_media": {"pct": "占比", "strategy": "策略", "example_script": "脚本示例"},
        "doctor_kol": {"pct": "占比", "strategy": "策略", "example_script": "脚本示例"},
        "non_medical_koc": {"pct": "占比", "strategy": "策略", "example_script": "脚本示例"},
        "patient_kol": {"pct": "占比", "strategy": "策略", "example_script": "脚本示例"}
    },
    "propagation_logic": "传播策略概述",
    "platforms": [
        {"name": "平台名", "pct": "占比", "reason": "理由"}
    ],
    "content_mapping": [
        {"direction": "内容方向", "benefits": "对应利益点编号", "platform": "平台", "risk": "低/中/高"}
    ],
    "compliance": [
        {"avoid": "不能说", "suggest": "可以说"}
    ],
    "summary": "报告总结"
}

# ============================================================
# 以下代码无需修改
# ============================================================
def main():
    cleanup_temp()
    
    md = generate_report(data)
    html = generate_html(data)
    
    name = data.get("drug_name", "报告")
    safe = _sanitize_name(name)

    # 写文件到临时目录（跨平台）
    tmp_dir = os.path.join(tempfile.gettempdir(), "drug_report_" + safe[:20])
    os.makedirs(tmp_dir, exist_ok=True)

    html_path = os.path.join(tmp_dir, safe + "_投放策略报告.html")
    pdf_path = os.path.join(tmp_dir, safe + "_投放策略报告.pdf")
    md_path = os.path.join(tmp_dir, safe + "_投放策略报告.md")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)

    try:
        _render_pdf(html_path, pdf_path)
        print(f"PDF: {pdf_path}")
    except Exception as e:
        print(f"PDF生成失败: {e}")
        print(f"HTML文件仍可用: {html_path}")
    print(f"MD: {md_path}")

if __name__ == "__main__":
    main()