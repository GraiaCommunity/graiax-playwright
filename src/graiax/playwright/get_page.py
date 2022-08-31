# -*- coding: utf-8 -*-

from typing import Any

from playwright.async_api import Browser


class GetContextPage:
    """获得一个使用了 Browser Context 的页面

    详见：https://playwright.dev/python/docs/browser-contexts

    Args:
        browser: playwright.async_api.Browser, 浏览器实例
        **config, Browser Context 的配置
    """

    browser: Browser
    config: dict[str, Any]

    def __init__(self, browser: Browser, **config):
        self.browser = browser
        self.config = config

    async def __aenter__(self):
        self.context = await self.browser.new_context(**self.config)
        self.page = await self.context.new_page()
        return self.page

    async def __aexit__(self, type, value, trace):
        await self.page.close()
        await self.context.close()


class GetPage:
    """获得一个页面

    Args:
        browser: playwright.async_api.Browser, 浏览器实例
        **config, Browser Context 的配置
    """

    browser: Browser
    config: dict[str, Any]

    def __init__(self, browser: Browser, **config):
        self.browser = browser
        self.config = config

    async def __aenter__(self):
        self.page = await self.browser.new_page(**self.config)
        return self.page

    async def __aexit__(self, type, value, trace):
        await self.page.close()
