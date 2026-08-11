from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        # wait_until="domcontentloaded" tells Playwright not to wait for heavy images/iframes
        self.page.goto(url, wait_until="domcontentloaded", timeout=60000)