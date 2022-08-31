# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Optional

from playwright.async_api import Browser, Playwright, async_playwright


class PlaywrightBrowser(ABC):
    browser: Optional[Browser] = None
    playwright: Optional[Playwright] = None

    def __init__(self):
        ...

    def get(self) -> Browser:
        if self.browser is not None:
            return self.browser
        raise RuntimeError("The browser has not been initialized!")

    async def close(self):
        if self.browser is not None:
            await self.browser.close()
        if self.playwright is not None:
            await self.playwright.stop()

    @abstractmethod
    async def init(self, **config):
        ...


class WebkitBrowser(PlaywrightBrowser):
    """Webkit 浏览器"""

    async def init(self, **config):
        """初始化 Playwright

        Args:
            **config: 要传给 playwright.webkit.launch 的参数
        """
        if self.playwright is not None or self.browser is not None:
            raise RuntimeError("Webkit browser has been initialized!")
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.webkit.launch(**config)


class ChromiumBrowser(PlaywrightBrowser):
    """Chromium 浏览器"""

    async def init(self, **config):
        """初始化 Playwright

        Args:
            **config: 要传给 playwright.chromium.launch 的参数
        """
        if self.playwright is not None or self.browser is not None:
            raise RuntimeError("Chromium browser has been initialized!")
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(**config)


class FirefoxBrowser(PlaywrightBrowser):
    """Firefox 浏览器"""

    async def init(self, **config):
        """初始化 Playwright

        Args:
            **config: 要传给 playwright.firefox.launch 的参数
        """
        if self.playwright is not None or self.browser is not None:
            raise RuntimeError("Firefox browser has been initialized!")
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.firefox.launch(**config)
