import json

SELECTED_FILE = 'selected_news.json'

def main():
    with open(SELECTED_FILE, 'r', encoding='utf-8') as f:
        news_items = json.load(f)
    
    new_items = []
    removed_count = 0
    
    for item in news_items:
        # Check if title contains raw scraping artifacts
        if '\n.\nAIbase' in item['title'] or item['title'].strip().startswith(('1 小时前', '2 小时前', '3 小时前', '4 小时前', '5 小时前')):
            print(f"Removing: {item['title'][:30]}...")
            removed_count += 1
        else:
            new_items.append(item)
            
    with open(SELECTED_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_items, f, ensure_ascii=False, indent=2)
        
    print(f"Removed {removed_count} items. Remaining: {len(new_items)}")

if __name__ == "__main__":
    main()
