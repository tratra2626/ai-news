import json
import os
import datetime
import time
import re
import asyncio
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright

# --- Constants ---
CANDIDATES_FILE = 'aibase_candidates.json'
SELECTED_FILE = 'selected_news.json'
TODAY = datetime.date.today()
LIMIT_DATE = TODAY - datetime.timedelta(days=2)

def clear_files():
    print("Cleaning up old files...")
    if os.path.exists(CANDIDATES_FILE):
        os.remove(CANDIDATES_FILE)
    
    # Backup selected_news.json
    if os.path.exists(SELECTED_FILE):
        with open(SELECTED_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        with open('selected_news_backup.json', 'w', encoding='utf-8') as f:
            f.write(content)
        # Clear it
        with open(SELECTED_FILE, 'w', encoding='utf-8') as f:
            f.write('[]')
    print("Files cleared.")

# --- AIBase Fetcher ---
def parse_aibase_date(raw_text):
    # Simplified version of the logic in fetch_aibase_news.py
    # Returns date object or None
    lines = raw_text.split('\n')
    first_line = lines[0].strip()
    
    if '小时前' in first_line or '分钟前' in first_line or '刚刚' in first_line:
        return TODAY
    elif '天前' in first_line:
        try:
            days = int(re.search(r'(\d+)\s*天前', first_line).group(1))
            return TODAY - datetime.timedelta(days=days)
        except:
            return None
    elif re.match(r'\d{4}-\d{2}-\d{2}', first_line):
        try:
            return datetime.date.fromisoformat(re.match(r'\d{4}-\d{2}-\d{2}', first_line).group(0))
        except:
            return None
    elif re.match(r'\d{1,2}-\d{1,2}', first_line):
        try:
            m = re.match(r'(\d{1,2})-(\d{1,2})', first_line)
            return datetime.date(TODAY.year, int(m.group(1)), int(m.group(2)))
        except:
            return None
    return None

def fetch_aibase():
    print("Fetching AIBase (Recent 3 days)...")
    items = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://www.aibase.com/zh/news')
        
        # Scroll a bit, but not too much
        for _ in range(8):
            page.keyboard.press("End")
            time.sleep(1)
            
        candidates = page.evaluate("""() => {
            const items = [];
            const links = document.querySelectorAll('a');
            links.forEach(a => {
                const text = a.innerText.trim();
                const href = a.href;
                if (text.length > 20 && href.includes('/news/')) {
                    items.push({ title: text, link: href, source: 'AIBase' });
                }
            });
            return items;
        }""")
        
        seen = set()
        for c in candidates:
            if c['link'] in seen: continue
            seen.add(c['link'])
            
            d = parse_aibase_date(c['title'])
            if d and d >= LIMIT_DATE:
                c['date'] = d.isoformat()
                # Clean title for display (remove date lines)
                # But keep original logic which stores full text in title for now, 
                # as the admin UI might expect it. 
                # Actually, let's keep it consistent with previous scripts.
                c['status'] = 'pending'
                c['summary'] = ''
                c['takeaway'] = ''
                items.append(c)
        
        browser.close()
    print(f"Found {len(items)} recent AIBase items.")
    return items

# --- WeChat/GeekPark Fetcher ---
async def fetch_wechat():
    print("Fetching GeekPark/APPSO (Top 5 each)...")
    targets = [
        {"name": "APPSO", "url": "https://www.ifanr.com/app", "selector": "h3 a, h2 a"}, 
        {"name": "GeekPark", "url": "https://www.geekpark.net/", "selector": "h3 a, .article-item a"}
    ]
    
    items = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        for t in targets:
            try:
                await page.goto(t['url'])
                await page.wait_for_load_state('domcontentloaded')
                
                elements = await page.locator(t['selector']).all()
                count = 0
                for el in elements:
                    if count >= 5: break
                    
                    text = await el.inner_text()
                    href = await el.get_attribute('href')
                    
                    if not text or len(text) < 5: continue
                    
                    if href and not href.startswith('http'):
                        if 'ifanr' in t['url']: href = 'https://www.ifanr.com' + href
                        elif 'geekpark' in t['url']: href = 'https://www.geekpark.net' + href
                    
                    # Keywords check
                    keywords = ["OpenAI", "GPT", "Sora", "Anthropic", "Claude", "Google", "Gemini", "DeepSeek", "腾讯", "阿里", "AI", "模型"]
                    if any(k.lower() in text.lower() for k in keywords):
                        items.append({
                            "title": text.strip(),
                            "link": href,
                            "source": t['name'],
                            "date": TODAY.isoformat(), # Assume today for top items
                            "status": "pending",
                            "summary": "",
                            "takeaway": ""
                        })
                        count += 1
            except Exception as e:
                print(f"Error fetching {t['name']}: {e}")
        
        await browser.close()
    print(f"Found {len(items)} WeChat/GeekPark items.")
    return items

def main():
    clear_files()
    
    # 1. AIBase
    aibase_items = fetch_aibase()
    
    # 2. WeChat (Async)
    wechat_items = asyncio.run(fetch_wechat())
    
    # Merge
    all_items = aibase_items + wechat_items
    
    # Save
    with open(CANDIDATES_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)
    
    print(f"Total {len(all_items)} fresh items saved to {CANDIDATES_FILE}")

if __name__ == "__main__":
    main()
