import asyncio
from playwright.async_api import async_playwright
import json

async def run():
    async with async_playwright() as p:
        # Launch non-headless to let user login
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        print("Opening Xiaohongshu... Please log in manually within 60 seconds.")
        await page.goto("https://www.xiaohongshu.com")
        
        # Wait for user to login (adjust time as needed)
        try:
            # You might want to wait for a specific element that appears only after login
            # For now, we just wait a fixed time or until user closes? 
            # Better: wait for a known post-login element, e.g., avatar
            await page.wait_for_selector(".user-avatar", timeout=60000)
            print("Login detected!")
        except:
            print("Timeout or login not detected. Saving cookies anyway...")

        # Save cookies
        cookies = await context.cookies()
        with open("xhs_cookies.json", "w") as f:
            json.dump(cookies, f)
        print("Cookies saved to xhs_cookies.json")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
