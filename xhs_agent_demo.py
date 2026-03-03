import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # Launch browser
        # user_agent is important to avoid immediate block
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        page = await context.new_page()
        
        print("Navigating to Xiaohongshu...")
        try:
            await page.goto("https://www.xiaohongshu.com/explore", timeout=30000)
            await page.wait_for_load_state("networkidle")
            print(f"Page title: {await page.title()}")
            
            # Screenshot for debugging
            await page.screenshot(path="xhs_home.png")
            print("Screenshot saved to xhs_home.png")
            
            # Try to find search box
            # Note: XHS classes are often random strings.
            # Usually input[type="text"] or similar
            search_input = page.locator("input.search-input")
            if not await search_input.count():
                search_input = page.locator("input#search-input") # try ID
            if not await search_input.count():
                search_input = page.locator("input[type='text']") # generic
            
            if await search_input.count() > 0:
                print("Search input found. Typing '豆包输入法'...")
                # await search_input.first.fill("豆包输入法")
                # await search_input.first.press("Enter")
                
                # Direct navigation to search result
                print("Navigating directly to search results...")
                await page.goto("https://www.xiaohongshu.com/search_result?keyword=%E8%B1%86%E5%8C%85%E8%BE%93%E5%85%A5%E6%B3%95&source=web_explore_feed", timeout=30000)
                await page.wait_for_load_state("networkidle")
                print(f"Current URL: {page.url}")

                # Wait for results
                print("Waiting for results...")
                # Usually results are in feeds
                try:
                    await page.wait_for_selector("section.note-item", timeout=10000)
                    
                    # Get some titles
                    items = page.locator("section.note-item")
                    count = await items.count()
                    print(f"Found {count} items.")
                    
                    for i in range(min(5, count)):
                        item = items.nth(i)
                        title_el = item.locator(".title span")
                        if await title_el.count():
                            title = await title_el.inner_text()
                            print(f"Result {i+1}: {title}")
                            
                            # Get link
                            link_el = item.locator("a.cover")
                            if await link_el.count():
                                href = await link_el.get_attribute("href")
                                print(f"  Link: https://www.xiaohongshu.com{href}")
                                
                except Exception as e:
                    print(f"Could not find results: {e}")
                    await page.screenshot(path="xhs_search_fail.png")
            else:
                print("Search input NOT found.")
                
        except Exception as e:
            print(f"Error: {e}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
