from typing import Optional

from playwright.async_api import async_playwright
from playwright.async_api._generated import (Browser, BrowserContext, Page,
                                             Response)


async def get_basic_data(browser: Browser):
    HTTP_STATUS: int = -1
    RESPONSE_URL: Optional[str] = None
    RESPONSE_TITLE: Optional[str] = None
    #
    page: Page = await browser.new_page()
    webpage: Optional[Response] = await page.goto(
        'http://localhost:3000/',
        wait_until='domcontentloaded',
        timeout=60000,
    )
    if webpage is not None:
        HTTP_STATUS = webpage.status
        RESPONSE_TITLE = await page.title()
        RESPONSE_URL = page.url
    return HTTP_STATUS, RESPONSE_URL, RESPONSE_TITLE


async def main():
    async with async_playwright() as contextManager:
        browser: Browser = await contextManager.chromium.launch(
            channel='chrome',
            headless=True,
            timeout=60000,  # wait 60 seconds for the browser instant to start.
            slow_mo=250,  # slowdown playwright operations by 0.25 second.
        )
        context: BrowserContext = await browser.new_context(
            reduced_motion='reduce',
        )
        page: Page = await context.new_page()
        result = await asyncio.gather(
            *(get_basic_data(browser) for _ in range(10)),
        )
        print(result)
        await page.close()


if __name__ == '__main__':
    import asyncio

    asyncio.run(main=main())
