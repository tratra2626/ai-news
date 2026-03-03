from bs4 import BeautifulSoup
import re

def parse_html_to_markdown(html_path, output_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Define columns
    columns = {
        'overseas': {'title': '🌍 海外重点 (Overseas)', 'items': []},
        'domestic': {'title': '🇨🇳 国内重点 (Domestic)', 'items': []},
        'emerging': {'title': '🚀 新兴/其他 (Emerging)', 'items': []}
    }

    # Helper to clean text
    def clean_text(text):
        if not text:
            return ""
        return re.sub(r'\s+', ' ', text).strip()

    # Find the matrix grid
    matrix_grid = soup.find('div', class_='matrix-grid')
    if not matrix_grid:
        print("Error: matrix-grid not found")
        return

    # Find the week row
    week_row = matrix_grid.find('div', class_='week-row')
    if not week_row:
        print("Error: week-row not found")
        return

    # The structure in week-row is: Time Label, Overseas Cell, Domestic Cell, Emerging Cell
    # We skip the time label
    news_cells = week_row.find_all('div', class_='news-cell')
    
    if len(news_cells) >= 1:
        columns['overseas']['cell'] = news_cells[0]
    if len(news_cells) >= 2:
        columns['domestic']['cell'] = news_cells[1]
    if len(news_cells) >= 3:
        columns['emerging']['cell'] = news_cells[2]

    # Extract items for each column
    for key, col_data in columns.items():
        if 'cell' not in col_data:
            continue
            
        cell = col_data['cell']
        news_items = cell.find_all('div', class_='news-item')
        
        for item in news_items:
            # Extract data
            title_div = item.find('div', class_='news-title')
            link = title_div.find('a') if title_div else None
            tag_span = title_div.find('span') if title_div else None
            
            title = clean_text(link.get_text()) if link else "No Title"
            url = link['href'] if link else "#"
            tag = clean_text(tag_span.get_text()) if tag_span else ""
            
            date_badge = item.find('span', class_='date-badge')
            date = clean_text(date_badge.get_text()) if date_badge else ""
            
            desc_div = item.find('div', class_='news-desc')
            desc = clean_text(desc_div.get_text()) if desc_div else ""
            
            details_content = item.find('div', class_='details-content')
            takeaway = ""
            if details_content:
                takeaway_box = details_content.find('div', class_='takeaway-box')
                if takeaway_box:
                    # Remove the title span from takeaway text if present
                    takeaway_title = takeaway_box.find('span', class_='takeaway-title')
                    if takeaway_title:
                        takeaway_title.decompose()
                    takeaway = clean_text(takeaway_box.get_text())

            col_data['items'].append({
                'title': title,
                'url': url,
                'tag': tag,
                'date': date,
                'desc': desc,
                'takeaway': takeaway
            })

    # Generate Markdown
    md_lines = []
    md_lines.append("# AI 重点新闻周报 (2026.01.29 - 2026.02.05)")
    md_lines.append("")
    md_lines.append("## 📅 本周动态概览")
    md_lines.append("")

    # Create Summary Table
    # We need to transpose the lists to fill the table rows
    # But wait, the user asked for a "horizontal 3-row table" which I interpreted as 3 columns.
    # In a markdown table, we write row by row.
    # Max items in a column?
    max_items = max(len(columns['overseas']['items']), len(columns['domestic']['items']), len(columns['emerging']['items']))
    
    md_lines.append(f"| {columns['overseas']['title']} | {columns['domestic']['title']} | {columns['emerging']['title']} |")
    md_lines.append("| :--- | :--- | :--- |")

    for i in range(max_items):
        row_cells = []
        for key in ['overseas', 'domestic', 'emerging']:
            items = columns[key]['items']
            if i < len(items):
                item = items[i]
                # Format: **Title**<br>Desc<br>[Link]
                # Note: Markdown tables don't support newlines well. We use <br>.
                cell_content = f"**{item['title']}**<br><span style='color:gray;font-size:0.9em'>{item['desc']}</span><br>🔗 [Link]({item['url']})"
                row_cells.append(cell_content)
            else:
                row_cells.append("")
        md_lines.append(f"| {row_cells[0]} | {row_cells[1]} | {row_cells[2]} |")

    md_lines.append("")
    md_lines.append("## 📝 详细内容与洞察 (Takeaway)")
    md_lines.append("")

    for key in ['overseas', 'domestic', 'emerging']:
        col = columns[key]
        if not col['items']:
            continue
            
        md_lines.append(f"### {col['title']}")
        for idx, item in enumerate(col['items'], 1):
            md_lines.append(f"#### {idx}. [{item['title']}]({item['url']})")
            if item['tag']:
                md_lines.append(f"- **标签**: `{item['tag']}`")
            md_lines.append(f"- **日期**: {item['date']}")
            md_lines.append(f"- **摘要**: {item['desc']}")
            if item['takeaway']:
                md_lines.append(f"- **💡 Takeaway**: {item['takeaway']}")
            md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    print(f"Markdown file generated at: {output_path}")

if __name__ == "__main__":
    parse_html_to_markdown(
        r"c:\Users\Admin\Downloads\ai_dashboard.html",
        r"c:\Users\Admin\Downloads\ai_news_feishu.md"
    )
