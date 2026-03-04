import json

SELECTED_FILE = 'selected_news.json'

def main():
    with open(SELECTED_FILE, 'r', encoding='utf-8') as f:
        news_items = json.load(f)
    
    # Update the item with link https://www.aibase.com/zh/news/25908
    target_link = "https://www.aibase.com/zh/news/25908"
    
    found = False
    for item in news_items:
        if item['link'] == target_link:
            item['title'] = "不仅是性价比之王！MiniMax 2.5 霸榜全球调用量：月收入破 1.5 亿美元"
            item['summary'] = "2026年3月3日，OpenRouter数据显示，国产大模型MiniMax M2.5、Kimi K2.5和GLM-5包揽全球调用量前三。其中，MiniMax M2.5仅发布一周，调用量即突破3.07万亿Tokens，月收入（ARR）飙升至1.5亿美元。其凭借10B的极致小参数和针对Agent优化的低成本策略，精准切中开发者痛点，成为“性价比之王”。此外，DeepSeek V4即将发布，MiniMax M3也将在上半年推出，国产大模型竞争进入白热化阶段。"
            item['takeaway'] = "中国大模型厂商通过极致的工程化和性价比策略，在全球开发者社区实现了“弯道超车”。MiniMax M2.5的成功证明了小参数、高效率模型在Agent场景下的巨大商业价值，预示着AI应用落地正从单纯追求模型能力转向追求实际产出比。"
            item['category'] = "emerging"
            print(f"Updated item: {target_link}")
            found = True
            break
    
    if not found:
        print(f"Item not found: {target_link}")
            
    with open(SELECTED_FILE, 'w', encoding='utf-8') as f:
        json.dump(news_items, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
