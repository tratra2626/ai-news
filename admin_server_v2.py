import http.server
import socketserver
import json
import urllib.parse
import os

PORT = 8080
CANDIDATES_FILE = 'aibase_candidates.json'
SELECTED_FILE = 'selected_news.json'

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path_only = self.path.split('?')[0]
        
        if path_only == '/admin':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # Load candidates
            candidates = []
            if os.path.exists(CANDIDATES_FILE):
                with open(CANDIDATES_FILE, 'r', encoding='utf-8') as f:
                    candidates = json.load(f)
            
            # Load selected to mark duplicates
            selected_links = set()
            if os.path.exists(SELECTED_FILE):
                with open(SELECTED_FILE, 'r', encoding='utf-8') as f:
                    selected = json.load(f)
                    for item in selected:
                        selected_links.add(item['link'])

            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>News Selector</title>
                <style>
                    body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                    .item { border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px; }
                    .item.selected { background-color: #e0f7fa; }
                    .title { font-weight: bold; }
                    .meta { color: #666; font-size: 0.9em; }
                    button { padding: 10px 20px; font-size: 1.2em; background: #007bff; color: white; border: none; cursor: pointer; }
                </style>
            </head>
            <body>
                <h1>Select News</h1>
                <form action="/save" method="post">
            """
            
            for i, item in enumerate(candidates):
                is_selected = item['link'] in selected_links
                checked = 'checked disabled' if is_selected else ''
                cls = 'item selected' if is_selected else 'item'
                status_text = ' (Already Selected)' if is_selected else ''
                
                html += f"""
                <div class="{cls}">
                    <label>
                        <input type="checkbox" name="index" value="{i}" {checked}>
                        <span class="title">{item['title']}</span>
                        <span class="meta">[{item['source']}] {item['date']}{status_text}</span>
                    </label>
                    <div><a href="{item['link']}" target="_blank">View Original</a></div>
                </div>
                """
            
            html += """
                    <div style="position: sticky; bottom: 20px; background: white; padding: 10px; border-top: 1px solid #ddd;">
                        <button type="submit">Save Selection</button>
                    </div>
                </form>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
            return

        super().do_GET()

    def do_POST(self):
        if self.path == '/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = urllib.parse.parse_qs(post_data)
            
            selected_indices = params.get('index', [])
            
            # Load candidates
            with open(CANDIDATES_FILE, 'r', encoding='utf-8') as f:
                candidates = json.load(f)
            
            # Load existing selected
            existing_news = []
            if os.path.exists(SELECTED_FILE):
                with open(SELECTED_FILE, 'r', encoding='utf-8') as f:
                    existing_news = json.load(f)
            
            existing_links = {item['link'] for item in existing_news}
            
            count = 0
            for idx in selected_indices:
                item = candidates[int(idx)]
                if item['link'] not in existing_links:
                    # Prepare item format
                    new_item = {
                        "title": item['title'],
                        "link": item['link'],
                        "source": item['source'],
                        "date": item['date'],
                        "status": "selected",
                        "summary": item.get('summary', ''),
                        "takeaway": "",
                        "category": "overseas" # Default, user can edit later or auto-detect
                    }
                    existing_news.append(new_item)
                    count += 1
            
            # Save
            with open(SELECTED_FILE, 'w', encoding='utf-8') as f:
                json.dump(existing_news, f, ensure_ascii=False, indent=2)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"Saved {count} new items. <a href='/admin'>Back</a>".encode('utf-8'))
            return

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}/admin")
    httpd.serve_forever()
