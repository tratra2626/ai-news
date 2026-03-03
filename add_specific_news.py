import json
import datetime

# --- Constants ---
SELECTED_FILE = 'selected_news.json'

def main():
    with open(SELECTED_FILE, 'r', encoding='utf-8') as f:
        existing_news = json.load(f)
    
    # Check if they already exist to avoid duplicates
    existing_links = {item['link'] for item in existing_news}

    new_items = []

    # 1. Cursor News
    link_cursor = "https://www.aibase.com/zh/news/25870"
    if link_cursor not in existing_links:
        cursor_news = {
            "title": "吸金力惊人！AI 编程助手 Cursor 年化营收突破 20 亿美元，三个月内翻倍增长",
            "link": link_cursor,
            "source": "AIBase",
            "date": "2026-03-03",
            "status": "selected",
            "summary": "AI编程助手Cursor年化营收（ARR）突破20亿美元，三个月内实现翻倍。成立仅四年的Cursor成功转型企业级市场，目前约60%的收入来自大型企业客户。尽管面临Claude Code等低价竞争对手的挑战，Cursor凭借在高端市场的深耕和2.3亿美元融资，依然保持行业领先地位。",
            "takeaway": "AI编程工具市场正在从个人开发者向企业级市场转移，企业客户的高黏性和付费意愿是增长的关键。Cursor的成功证明了垂直领域AI工具的巨大商业潜力。",
            "category": "emerging"
        }
        new_items.append(cursor_news)
    
    # 2. MiniMax News
    link_minimax = "https://www.aibase.com/zh/news/25888"
    if link_minimax not in existing_links:
        minimax_news = {
            "title": "MiniMax公布上市后首份财报 全年收入7903.8万美元",
            "link": link_minimax,
            "source": "AIBase",
            "date": "2026-03-03",
            "status": "selected",
            "summary": "MiniMax（上海稀宇科技）发布上市后首份年度财报，全年收入7904万美元，同比增长158.9%，其中海外收入占比超70%。尽管年内亏损达18.72亿美元（主要因金融负债公允价值重估），但经调整净亏损仅小幅扩大，且销售费用大幅下降。公司正从“大模型”向“AI平台”转型，其M2.5模型在性价比和编程能力上表现优异。",
            "takeaway": "MiniMax展现了中国AI公司独特的全球化路径，通过高性价比模型和C端应用（Talkie）在海外市场取得突破。虽然账面亏损巨大，但经营效率的提升和清晰的平台化战略为其长期发展奠定了基础。",
            "category": "emerging"
        }
        new_items.append(minimax_news)

    # 3. Claude Code Voice Mode
    link_claude = "https://www.aibase.com/zh/news/25877"
    if link_claude not in existing_links:
        claude_news = {
            "title": "Claude Code 迎来重磅更新：官方语音模式上线，按住空格键即可对话编程",
            "link": link_claude,
            "source": "AIBase",
            "date": "2026-03-03",
            "status": "selected",
            "summary": "Anthropic旗下AI编程工具Claude Code推出语音模式（Voice Mode），允许开发者通过自然语音输入指令。用户只需输入`/voice`即可开启，按住空格键说话，语音内容会实时转录为文本。该功能目前正向约5%的用户逐步推送，支持混合输入，特别适合快速描述复杂逻辑或重构代码。",
            "takeaway": "编程工具的交互方式正在发生变革，从纯文本向多模态进化。语音输入的加入降低了使用门槛，使开发者能更专注于逻辑思考，进一步提升了人机协作的效率。",
            "category": "overseas"
        }
        new_items.append(claude_news)

    # Add news items
    if new_items:
        existing_news.extend(new_items)
        # Save
        with open(SELECTED_FILE, 'w', encoding='utf-8') as f:
            json.dump(existing_news, f, ensure_ascii=False, indent=2)
        print(f"Added {len(new_items)} news items.")
    else:
        print("No new items added (duplicates found).")

if __name__ == "__main__":
    main()
