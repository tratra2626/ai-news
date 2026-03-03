import asyncio
import json
import os
from playwright.async_api import async_playwright

# Mock LLM function - replace with actual API call (OpenAI, Gemini, etc.)
async def analyze_with_llm(text):
    print(f"\n[Agent Brain] Analyzing content length: {len(text)}...")
    # Example: "Summarize the sentiment of these comments regarding Doubao Input Method"
    return "Analysis Result: Users seem to like the voice input feature but complain about some lag."

async def run_agent():
    if not os.path.exists("xhs_cookies.json"):
        print("Error: 'xhs_cookies.json' not found. Please run get_cookies.py first.")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False) # Headless=False to see it working
        
        # Load cookies
        with open("xhs_cookies.json", "r") as f:
            cookies = json.load(f)
            
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        await context.add_cookies(cookies)
        page = await context.new_page()
        
        # 1. Search
        keyword = "豆包输入法"
        print(f"Agent: Searching for '{keyword}'...")
        # Search with "Latest" sort if possible, but XHS web URL params for sort are tricky.
        # usually &sort=time_desc or similar, but let's stick to default for now as "Latest" tab might need clicking.
        await page.goto(f"https://www.xiaohongshu.com/search_result?keyword={keyword}&source=web_explore_feed")
        
        try:
            # Wait for results
            await page.wait_for_selector("section.note-item", timeout=10000)
            
            # Click "Latest" (最新) tab if it exists
            # Selectors might vary, try to find text "最新"
            try:
                latest_tab = page.locator("div.filter-box div.filter-item:has-text('最新')")
                if await latest_tab.count() > 0:
                    print("Agent: Clicking 'Latest' tab...")
                    await latest_tab.click()
                    await page.wait_for_timeout(2000) # Wait for reload
            except Exception as e:
                print(f"Agent: Could not click 'Latest' tab: {e}")

            collected_data = []
            target_count = 50
            
            while len(collected_data) < target_count:
                # Get all current items
                items = page.locator("section.note-item")
                count = await items.count()
                print(f"Agent: Found {count} notes on screen...")
                
                # Iterate through items
                # We need to keep track of processed indices or IDs to avoid duplicates if we re-query
                # But XHS infinite scroll adds to the bottom. 
                # Be careful: DOM elements might be recycled or become stale.
                # Safer strategy: Get all links, then visit them? 
                # Visiting links navigates away, losing search state.
                # Opening in new tab is better, or Modal.
                
                # Let's try opening in Modal (click item), scrape, close modal.
                
                for i in range(len(collected_data), count):
                    if len(collected_data) >= target_count:
                        break
                        
                    item = items.nth(i)
                    try:
                        title_el = item.locator(".title span")
                        if not await title_el.count():
                            continue
                        title = await title_el.inner_text()
                        print(f"[{len(collected_data)+1}/{target_count}] Processing: {title}")
                        
                        # Click to open modal
                        await item.click()
                        
                        # Wait for modal content
                        try:
                            # Wait for note container or close button
                            await page.wait_for_selector(".note-detail-mask", timeout=5000)
                            
                            # Extract Content
                            desc_el = page.locator("#detail-desc")
                            content = await desc_el.inner_text() if await desc_el.count() else ""
                            
                            # Extract Date (to confirm it's recent)
                            # Scope to note detail container to avoid finding dates in the background list
                            try:
                                # Try to find date within the modal container
                                # Usually under .note-content or .note-scroller
                                date_el = page.locator(".note-detail-mask .date").first
                                if await date_el.count():
                                    date = await date_el.inner_text()
                                else:
                                    date = ""
                            except:
                                date = ""
                            
                            # Extract Comments
                            # Scroll comments section
                            # Note: On web modal, comments are usually in .note-scroller or similar container
                            # Try multiple strategies to find comments
                            comments_text = []
                            try:
                                # Strategy 1: Find any comment content in the modal
                                # Scope to modal
                                modal = page.locator(".note-detail-mask")
                                if await modal.count():
                                    # Scroll the modal content to trigger lazy load
                                    # Try scrolling .note-scroller or just the window/modal
                                    # The scroller is often the div with class "note-scroller" or similar
                                    scroller = modal.locator(".note-scroller")
                                    if await scroller.count():
                                        await scroller.evaluate("el => el.scrollTop += 2000")
                                    else:
                                        # Try scrolling the modal itself or generic scroll
                                        await page.mouse.wheel(0, 2000)
                                    
                                    await page.wait_for_timeout(2000) # Wait for comments to load
                                    
                                    # Select comments within modal
                                    comments = modal.locator(".comment-item .content")
                                    c_count = await comments.count()
                                    if c_count == 0:
                                        # Try broader selector
                                        comments = modal.locator(".comment-content")
                                        c_count = await comments.count()
                                    
                                    print(f"    - Found {c_count} comments.")
                                    for c_i in range(min(10, c_count)): # Top 10 comments
                                        text = await comments.nth(c_i).inner_text()
                                        if text:
                                            comments_text.append(text)
                            except Exception as e:
                                print(f"    - Error extracting comments: {e}")
                            
                            collected_data.append({
                                "title": title,
                                "date": date,
                                "content": content,
                                "comments": comments_text
                            })
                            
                            # Close Modal
                            close_btn = page.locator(".close-mask") # Generic close mask
                            if await close_btn.count():
                                await close_btn.click()
                            else:
                                # Try clicking outside or Escape
                                await page.keyboard.press("Escape")
                                
                            await page.wait_for_timeout(1000) # Wait for animation
                            
                        except Exception as e:
                            print(f"Error processing note: {e}")
                            # Try to recover: Press Escape
                            await page.keyboard.press("Escape")
                            await page.wait_for_timeout(1000)

                    except Exception as e:
                        print(f"Error clicking note: {e}")

                # Scroll down to load more
                if len(collected_data) < target_count:
                    print("Agent: Scrolling down...")
                    await page.evaluate("window.scrollBy(0, 1000)")
                    await page.wait_for_timeout(2000) # Wait for load
                    
                    # Check if we reached bottom or no new items
                    new_count = await page.locator("section.note-item").count()
                    if new_count == count:
                        print("Agent: No new items found after scroll.")
                        # Try scrolling more
                        await page.evaluate("window.scrollBy(0, 2000)")
                        await page.wait_for_timeout(3000)
                        if await page.locator("section.note-item").count() == count:
                            print("Agent: End of results reached.")
                            break

            # Save data
            print(f"Agent: Collected {len(collected_data)} items.")
            with open("xhs_reviews.json", "w", encoding="utf-8") as f:
                json.dump(collected_data, f, ensure_ascii=False, indent=2)
            print("Agent: Data saved to xhs_reviews.json")
            
        except Exception as e:
            print(f"Agent Error: {e}")
            await page.screenshot(path="error.png")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_agent())
