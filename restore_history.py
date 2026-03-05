import json
import os

SELECTED_FILE = 'selected_news.json'
BACKUP_FILE = 'selected_news_backup.json'

def main():
    if not os.path.exists(BACKUP_FILE):
        print("No backup file found.")
        return

    try:
        with open(SELECTED_FILE, 'r', encoding='utf-8') as f:
            current_news = json.load(f)
    except:
        current_news = []
    
    with open(BACKUP_FILE, 'r', encoding='utf-8') as f:
        backup_news = json.load(f)
    
    current_links = {item['link'] for item in current_news}
    added_count = 0
    
    for item in backup_news:
        if item['link'] not in current_links:
            current_news.append(item)
            added_count += 1
    
    # Sort by date desc
    current_news.sort(key=lambda x: x['date'], reverse=True)
    
    with open(SELECTED_FILE, 'w', encoding='utf-8') as f:
        json.dump(current_news, f, ensure_ascii=False, indent=2)
        
    print(f"Restored {added_count} items from backup.")

if __name__ == "__main__":
    main()
