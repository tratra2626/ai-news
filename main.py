import json
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import collections
import os

app = FastAPI()

# Data Model
class Review(BaseModel):
    title: str
    date: str
    content: str
    comments: list[str]
    keywords: list[str] = []
    sentiment: str = "neutral"

# Load Data
DATA_FILE = "xhs_reviews.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Negative keywords configuration
NEGATIVE_KEYWORDS = [
    "卡", "慢", "卡顿", "延迟", "不准", "难用", "垃圾", 
    "闪退", "bug", "BUG", "智障", "蠢", "卸载", 
    "广告", "不好用", "失望", "太差", "无语", "避雷",
    "没有皮肤", "词库少", "不能自定义"
]

@app.get("/api/stats")
async def get_stats():
    data = load_data()
    total = len(data)
    negative_count = 0
    keyword_counts = collections.Counter()
    
    processed_data = []
    
    for item in data:
        text = item['title'] + "\n" + item['content'] + "\n" + "\n".join(item['comments'])
        found_keywords = [k for k in NEGATIVE_KEYWORDS if k in text]
        
        if found_keywords:
            negative_count += 1
            for k in found_keywords:
                keyword_counts[k] += 1
        
        item['keywords'] = found_keywords
        item['is_negative'] = len(found_keywords) > 0
        processed_data.append(item)
        
    top_keywords = [{"name": k, "value": v} for k, v in keyword_counts.most_common(10)]
    
    return {
        "total_reviews": total,
        "negative_reviews": negative_count,
        "negative_rate": round(negative_count / total * 100, 1) if total > 0 else 0,
        "top_keywords": top_keywords,
        "recent_reviews": processed_data
    }

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("dashboard.html", "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
