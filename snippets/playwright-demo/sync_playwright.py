# import time
from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import (Browser, BrowserContext,
                                            BrowserType, Page, Request,
                                            Response)


def get_title_httpStatus(page: Page):
    response: Response | None = page.goto(
        'http://localhost:3000/',
        wait_until='domcontentloaded',
        timeout=60000,  # wait 60 seconds
    )
    if response is None:
        return -1, None, None
    else:
        return response.status, page.url, page.title()


def reauestLoaded(req: Request):
    print(req.headers)
    print(req.url)


def main():
    with sync_playwright() as contextManager:
        browser: Browser = contextManager.chromium.launch(
            channel='chrome',
            headless=False,
            timeout=30000,  # wait 60 seconds for the browser instant to start.
            slow_mo=250,  # slowdown playwright operations by 0.25 second.
        )
        page = browser.new_page()
        page.expect_event('load', lambda x: print(x))
        responses = [get_title_httpStatus(page) for _ in range(5)]
        print(responses)
        page.close()


if __name__ == '__main__':
    main()
