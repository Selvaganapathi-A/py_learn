# from playwright.sync_api import sync_playwright
# BRAVE_USER_DATA = "C:\\Users/Tesla/AppData/Local/BraveSoftware/Brave-Browser/User Data/"  # Windows
# # For Linux: "/home/youruser/.config/BraveSoftware/Brave-Browser/"
# BRAVE_PATH = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
# with sync_playwright() as p:
#     browser = p.chromium.launch_persistent_context(BRAVE_USER_DATA, executable_path=BRAVE_PATH, headless=False)
#     page = browser.new_page()
#     page.goto("https://example.com")
#     print(f"Logged-in URL: {page.url}")
#     print(f"Page Title: {page.title()}")
#     browser.close()
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        # Channel can be "chrome", "msedge", "chrome-beta", "msedge-beta" or "msedge-dev".
        browser = await p.chromium.launch(channel='chrome', headless=True)
        # context = await browser.new_context()
        context = await browser.new_context(
            storage_state='session.json'
        )  # Load session
        page = await browser.new_page()
        response = await page.goto(
            'http://localhost:3000/',
            timeout=30_000,
            wait_until='commit',
        )
        print(type(page))
        print(type(context))
        print(type(browser))
        print(type(response))
        # print(help(response))
        title = await page.title()
        if response is not None:
            print(f'{response.status}')
        print(f'{title!r}')
        print(page.url)
        await page.close()
        # await asyncio.sleep(5)
        # break
        # input("Press Any key to Continue")
        # Step 3: Wait for Login to Complete
        await page.wait_for_load_state('networkidle')
        # Step 4: Save Cookies & Storage State
        await context.storage_state(path='session.json')
        await browser.close()


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
