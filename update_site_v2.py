import json
import datetime
import shutil
from bs4 import BeautifulSoup

SELECTED_FILE = 'selected_news.json'
HTML_FILE = 'ai_dashboard.html'

def get_week_range(date_str):
    # Custom logic for 02.27 - 03.03 (and later, as per user request to group recent news)
    if date_str >= '2026-02-27':
        return "02.27 - 03.03"

    try:
        dt = datetime.date.fromisoformat(date_str)
    except ValueError:
        return "Unknown Date"
    start = dt - datetime.timedelta(days=dt.weekday())
    end = start + datetime.timedelta(days=6)
    return f"{start.strftime('%m.%d')} - {end.strftime('%m.%d')}"

def get_company_tag(title, summary):
    text = (title + " " + summary).lower()
    if 'openai' in text or 'chatgpt' in text or 'gpt' in text: return 'openai'
    if 'anthropic' in text or 'claude' in text: return 'anthropic'
    if 'google' in text or 'gemini' in text: return 'google'
    if 'alibaba' in text or 'qwen' in text or '通义' in text: return 'alibaba'
    if 'tencent' in text or 'hunyuan' in text: return 'tencent'
    return 'other'

def create_news_item(soup, item):
    company = get_company_tag(item['title'], item.get('summary', ''))
    news_item = soup.new_tag('div', attrs={'class': 'news-item', 'data-company': company})
    
    # Date badge (optional, inside item)
    date_badge = soup.new_tag('span', attrs={'class': 'date-badge'})
    date_badge.string = item['date'].replace('-', '.')
    news_item.append(date_badge)

    # Title
    title_div = soup.new_tag('div', attrs={'class': 'news-title'})
    
    # Tag (optional)
    # tag = soup.new_tag('span', attrs={'class': 'tag-tech'})
    # tag.string = "资讯"
    # title_div.append(tag)
    # title_div.append(" ") # space

    link = soup.new_tag('a', href=item['link'], target='_blank')
    link.string = item['title']
    title_div.append(link)
    
    news_item.append(title_div)
    
    # Summary
    if item.get('summary'):
        desc = soup.new_tag('div', attrs={'class': 'news-desc'})
        desc.string = item['summary']
        news_item.append(desc)
    
    # Takeaway
    if item.get('takeaway'):
        details = soup.new_tag('details', attrs={'class': 'details-container'})
        summary = soup.new_tag('summary', attrs={'class': 'details-summary'})
        summary.string = "深度解读 / Takeaway"
        details.append(summary)
        
        content = soup.new_tag('div', attrs={'class': 'details-content'})
        
        # Takeaway box
        box = soup.new_tag('div', attrs={'class': 'takeaway-box'})
        box_title = soup.new_tag('span', attrs={'class': 'takeaway-title'})
        box_title.string = "Takeaway"
        box.append(box_title)
        box.append(" " + item['takeaway'])
        
        content.append(box)
        details.append(content)
        news_item.append(details)
        
    return news_item

def update_html():
    with open(SELECTED_FILE, 'r', encoding='utf-8') as f:
        news_items = json.load(f)
    
    # Group by week
    weeks = {}
    for item in news_items:
        w = get_week_range(item['date'])
        if w not in weeks:
            weeks[w] = []
        weeks[w].append(item)
    
    sorted_weeks = sorted(weeks.keys(), reverse=True)
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    # Find container
    # The container should be the .matrix-grid inside .timeline-container
    container = soup.find('div', class_='matrix-grid')
    if not container:
        # Fallback
        tl_container = soup.find('div', class_='timeline-container')
        if tl_container:
            container = tl_container.find('div', class_='matrix-grid')
    
    if not container:
        print("Could not find matrix-grid.")
        return

    # IMPORTANT: We should NOT clear the headers!
    # The headers are div.col-header (and one empty div for time col).
    # We should only remove existing week-rows.
    
    # Find all week-rows and remove them
    for row in container.find_all('div', class_='week-row'):
        row.decompose()
        
    # Now append new week rows
    for week in sorted_weeks:
        items = weeks[week]
        
        row = soup.new_tag('div', attrs={'class': 'week-row'})
        
        # 1. Time Label
        time_label = soup.new_tag('div', attrs={'class': 'time-label'})
        date_span = soup.new_tag('span', attrs={'class': 'time-date'})
        date_span.string = week
        time_label.append(date_span)
        row.append(time_label)
        
        # 2. Cells
        # Overseas (2fr) -> add news-grid-2col
        cell_overseas = soup.new_tag('div', attrs={'class': 'news-cell news-grid-2col'})
        cell_domestic = soup.new_tag('div', attrs={'class': 'news-cell'})
        cell_emerging = soup.new_tag('div', attrs={'class': 'news-cell'})
        
        for item in items:
            cat = item.get('category', 'overseas').lower()
            n_item = create_news_item(soup, item)
            
            if 'domestic' in cat:
                cell_domestic.append(n_item)
            elif 'emerging' in cat:
                cell_emerging.append(n_item)
            else:
                cell_overseas.append(n_item) # Default to overseas
        
        row.append(cell_overseas)
        row.append(cell_domestic)
        row.append(cell_emerging)
        
        container.append(row)
        
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    # Create index.html copy for GitHub Pages
    shutil.copy(HTML_FILE, 'index.html')
    print("HTML updated and index.html created successfully.")

if __name__ == "__main__":
    update_html()
