@echo off
chcp 65001
echo ==========================================
echo      🚀 AI 新闻发布助手 - 一键上线
echo ==========================================
echo.

cd /d "%~dp0"

echo [1/2] 正在生成网页...
python update_site.py

echo.
echo [2/2] 正在推送到 GitHub...
python publish.py

echo.
echo ✅ 发布完成！
echo 🌍 访问地址: https://tratra2626.github.io/ai-news/
echo.
pause
