@echo off
chcp 65001
echo ==========================================
echo      🤖 AI 新闻采编助手 - 一键启动
echo ==========================================
echo.

cd /d "%~dp0"

echo [1/3] 正在抓取 AIBase 新闻...
python fetch_aibase_news.py

echo [2/3] 正在抓取 公众号(APPSO/极客公园) 新闻...
python fetch_wechat_news.py

echo.
echo [3/3] 正在启动采编后台...
echo.
echo 👉 请在浏览器访问: http://localhost:8080/admin
echo.
echo (完成后请勿关闭此窗口，直到你完成新闻发布)
echo.

python admin_server.py

pause