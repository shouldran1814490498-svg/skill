#!/usr/bin/env python3
"""
药品投放策略报告 JSON 数据加载器
用法：
  # 本地 Windows：用 python（python3 在本机是空存根）
  python drug_json_runner.py rpt_p1.json [rpt_p2.json ...]
  # joyclaw / Linux：用 python3
  python3 drug_json_runner.py /tmp/rpt_p1.json [/tmp/rpt_p2.json ...]

把数据拆成多个小 JSON 文件（用 write 工具写，无heredoc风险），
或者把所有数据放一个 JSON 文件里，传给此脚本。
此脚本会依次加载所有 JSON 文件、合并字典、生成 PDF。
PDF 渲染由引擎自动兜底：wkhtmltopdf → Chrome → Edge，输出落在系统临时目录。

数据字段定义见 SKILL.md 的"数据字段对照"表。

拆文件最佳实践（避免 write 超长单文件）：
  part1: 基础信息（drug_name ~ adverse_reactions）
  part2: 合规/社媒/竞品/阶段/预算
  part3: 利益点/画像/用户行为
  part4: 达人矩阵/平台/内容/节奏/合规/总结

每个JSON文件只需包含部分字段，加载器会自动merge。
"""

import json, os, sys, tempfile

# Windows 控制台默认 GBK，打印 ✓/emoji 会崩；强制 stdout/stderr 走 UTF-8
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 引入引擎
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drug_engine import generate_report, generate_html, cleanup_temp
from drug_engine import _sanitize_name, _render_pdf


def load_json(path):
    """加载单个JSON文件，返回dict"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    if len(sys.argv) < 2:
        print("用法: python3 drug_json_runner.py <json_file1> [json_file2 ...]")
        sys.exit(1)

    # 合并所有JSON
    data = {}
    for path in sys.argv[1:]:
        if not os.path.exists(path):
            print(f"⚠️ 文件不存在，跳过: {path}")
            continue
        part = load_json(path)
        data.update(part)
        print(f"  ✓ {path} → 加载 {len(part)} 个字段")

    required = ["drug_name", "trade_name", "generic_name", "manufacturer",
                 "drug_category", "indication", "mechanism_simple"]
    missing = [k for k in required if k not in data]
    if missing:
        print(f"⚠️ 缺少必填字段: {', '.join(missing)}")
        print(f"  仍将继续生成，但报告可能不完整")

    print(f"\n📊 数据加载完成，共 {len(data)} 个字段")
    print(f"💊 药品: {data.get('drug_name', '未知')}")
    print(f"📈 阶段: {data.get('development_stage', '未指定')}")
    print(f"💰 预算: {data.get('budget', '未指定')} / {data.get('budget_duration', '未指定')}")
    print()

    # 生成报告
    cleanup_temp()
    md = generate_report(data)
    html = generate_html(data)

    name = data.get("drug_name", "报告")
    safe = _sanitize_name(name)
    tmp_dir = os.path.join(tempfile.gettempdir(), "drug_report_" + safe[:30])
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
        print(f"✅ PDF: {pdf_path}")
    except Exception as e:
        print(f"⚠️ PDF生成失败: {e}")
        print(f"   HTML文件仍可用: {html_path}")

    print(f"   MD: {md_path}")


if __name__ == "__main__":
    main()