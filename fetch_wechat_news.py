import asyncio
from playwright.async_api import async_playwright
import json
import os
import datetime

# 配置目标公众号/网站及其关键词
TARGETS = [
    {"name": "APPSO", "url": "https://www.ifanr.com/app", "selector": "h3 a, h2 a"}, 
    {"name": "GeekPark", "url": "https://www.geekpark.net/", "selector": "h3 a, .article-item a"},
    {"name": "Founder Park", "url": "https://www.geekpark.net/founder-park", "selector": "h3 a"} 
]

KEYWORDS = ["OpenAI", "GPT", "Sora", "Anthropic", "Claude", "Grok", "xAI", 
            "Perplexity", "腾讯", "元宝", "混元", "阿里", "通义", "千问", 
            "DeepSeek", "豆包", "字节", "Apple", "苹果", "AI"]

OUTPUT_FILE = 'aibase_candidates.json'

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        results = []
        
        for target in TARGETS:
            print(f"正在访问 {target['name']}...")
            try:
                await page.goto(target['url'], timeout=30000)
                await page.wait_for_load_state("domcontentloaded")
                
                # 简单滚动
                for _ in range(20):
                    await page.evaluate("window.scrollBy(0, 1000)")
                    await page.wait_for_timeout(500)
                
                # 抓取链接
                elements = await page.locator(target['selector']).all()
                print(f"  找到 {len(elements)} 个潜在文章...")
                
                for el in elements:
                    try:
                        title = await el.inner_text()
                        href = await el.get_attribute("href")
                        
                        if not title or len(title) < 5: continue
                        
                        # 完整链接处理
                        if href and not href.startswith("http"):
                            # 简单处理相对路径，不同网站可能不同
                            if "ifanr" in target['url']:
                                href = "https://www.ifanr.com" + href if href.startswith("/") else href
                            elif "geekpark" in target['url']:
                                href = "https://www.geekpark.net" + href if href.startswith("/") else href
                        
                        # 关键词过滤
                        matched_kw = None
                        for kw in KEYWORDS:
                            if kw.lower() in title.lower():
                                matched_kw = kw
                                break
                        
                        if matched_kw:
                            results.append({
                                "source": target['name'],
                                "title": title.strip(),
                                "url": href,
                                "keyword": matched_kw
                            })
                    except:
                        continue
                        
            except Exception as e:
                print(f"  访问 {target['name']} 失败: {e}")
        
        await browser.close()

        # Merge into aibase_candidates.json
        print(f"\nMerging {len(results)} items into {OUTPUT_FILE}...")
        
        existing_items = []
        if os.path.exists(OUTPUT_FILE):
            try:
                with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                    existing_items = json.load(f)
            except Exception as e:
                print(f"Error reading existing file: {e}")
        
        existing_links = {item.get('link', '') for item in existing_items}
        added_count = 0
        
        today_str = datetime.date.today().isoformat()
        
        for item in results:
            if item['url'] not in existing_links:
                new_entry = {
                    "title": item['title'],
                    "link": item['url'],
                    "source": item['source'],
                    "date": today_str,
                    "status": "pending",
                    "summary": "",
                    "takeaway": ""
                }
                existing_items.append(new_entry)
                existing_links.add(item['url'])
                added_count += 1
                
        # Save back
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(existing_items, f, ensure_ascii=False, indent=2)
            
        print(f"Saved. Added {added_count} new items from WeChat sources.")


if __name__ == "__main__":
    asyncio.run(run())
