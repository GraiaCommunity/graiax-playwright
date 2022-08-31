# -*- coding: utf-8 -*-

from typing import Any, Optional

from launart import Service

from .browser import ChromiumBrowser, PlaywrightBrowser
from .provider import BrowserProvider

# from .util import install_playwright


class BrowserService(Service):
    """用于 launart 的浏览器服务

    Args:
        browser: BrowserProvider, 你要使用的浏览器，默认为 Chromium
        **config, 启动浏览器所用的配置，即要传给 playwright.chromium.launch 的参数
    """

    id = "web.render/playwright"
    supported_interface_types = {BrowserProvider}
    browser: PlaywrightBrowser
    config: dict[str, Any]

    def __init__(self, browser: Optional[PlaywrightBrowser] = None, **config) -> None:
        self.browser = browser or ChromiumBrowser()
        self.config = config
        super().__init__()

    def get_interface(self, interface_type):
        if issubclass(interface_type, BrowserProvider):
            return BrowserProvider(self.browser)
        raise ValueError(f"unsupported interface type {interface_type}")

    @property
    def required(self):
        return set()

    @property
    def stages(self):
        return {"preparing", "cleanup"}

    async def launch(self, _):
        # install_playwright()  # TODO
        async with self.stage("preparing"):
            await self.browser.init(**self.config)
            self.config = {}
        async with self.stage("cleanup"):
            await self.browser.close()
