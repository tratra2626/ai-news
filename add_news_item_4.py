import json

SELECTED_FILE = 'selected_news.json'

def main():
    try:
        with open(SELECTED_FILE, 'r', encoding='utf-8') as f:
            news_items = json.load(f)
    except:
        news_items = []
    
    target_link = "https://mp.weixin.qq.com/s/p4HFkQLKmIEbBWdNLdBcBA"
    
    # Check if exists
    exists = False
    for item in news_items:
        if item['link'] == target_link:
            exists = True
            break
    
    if not exists:
        new_item = {
            "title": "刚刚，GPT-5.3 新模型撞车 Gemini，OpenClaw：谢谢你们",
            "link": target_link,
            "source": "WeChat",
            "date": "2026-03-04",
            "status": "selected",
            "summary": "OpenAI 发布 GPT-5.3 Instant，主打自然对话和低幻觉率；Google 同时推出 Gemini 3.1 Flash-Lite，强调极致速度和性价比，输入价格仅为 $0.25/百万 tokens。两款轻量级模型均试图打破“小模型即智障”的刻板印象，在特定场景下展现出强大的实用性。",
            "takeaway": "轻量级模型正在从单纯的“降本”转向“提质”。Gemini 3.1 Flash-Lite 的 $0.25/$1.50 定价策略极具攻击性，配合“思考等级”调节，将对实时交互应用（如NPC、UI生成）产生巨大吸引力。GPT-5.3 则通过“去AI腔”优化了用户体验，更适合内容创作。",
            "category": "overseas"
        }
        # Insert at top for new news
        news_items.insert(0, new_item)
        print(f"Added item: {target_link}")
        
        with open(SELECTED_FILE, 'w', encoding='utf-8') as f:
            json.dump(news_items, f, ensure_ascii=False, indent=2)
    else:
        print("Item already exists.")

if __name__ == "__main__":
    main()
