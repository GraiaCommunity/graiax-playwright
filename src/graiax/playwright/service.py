from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, Union

from launart import Service
from playwright._impl._api_structures import ProxySettings
from playwright.async_api import Browser, Playwright, async_playwright
from typing_extensions import ParamSpec

from .installer import install_playwright
from .interface import PlaywrightBrowser, PlaywrightBrowserImpl

P = ParamSpec("P")


class PlaywrightService(Service):
    """用于 launart 的浏览器服务

    Args:
        browser_type(Literal["chromium", "firefox", "webkit"]): 你要使用的浏览器，默认为 Chromium
        **kwargs: 参见 <https://playwright.dev/python/docs/api/class-browsertype#browser-type-launch>
    """

    id = "web.render/playwright"
    supported_interface_types = {PlaywrightBrowser}
    playwright: Playwright
    browser: Browser
    browser_type: str
    launch_config: Dict[str, Any]
    playwright_download_host: Optional[str]

    if TYPE_CHECKING:

        def __init__(
            self,
            browser_type: Literal["chromium", "firefox", "webkit"] = "chromium",
            playwright_download_host: Optional[str] = None,
            *,
            executable_path: Optional[Union[str, Path]] = None,
            channel: Optional[str] = None,
            args: Optional[List[str]] = None,
            ignore_default_args: Optional[Union[bool, List[str]]] = None,
            handle_sigint: Optional[bool] = None,
            handle_sigterm: Optional[bool] = None,
            handle_sighup: Optional[bool] = None,
            timeout: Optional[float] = None,
            env: Optional[Dict[str, Union[str, float, bool]]] = None,
            headless: Optional[bool] = None,
            devtools: Optional[bool] = None,
            proxy: Optional[ProxySettings] = None,
            downloads_path: Optional[Union[str, Path]] = None,
            slow_mo: Optional[float] = None,
            traces_dir: Optional[Union[str, Path]] = None,
            chromium_sandbox: Optional[bool] = None,
            firefox_user_prefs: Optional[Dict[str, Union[str, float, bool]]] = None,
        ):
            ...

    else:

        def __init__(
            self,
            browser_type: Literal["chromium", "firefox", "webkit"],
            playwright_download_host: Optional[str] = None,
            **kwargs,
        ) -> None:
            self.browser_type: Literal["chromium", "firefox", "webkit"] = browser_type
            self.launch_config = kwargs
            self.playwright_download_host = playwright_download_host
            super().__init__()

    def get_interface(self, _):
        return PlaywrightBrowserImpl(self, self.browser)

    @property
    def required(self):
        return set()

    @property
    def stages(self):
        return {"preparing", "cleanup"}

    async def launch(self, _):
        await install_playwright(self.playwright_download_host, self.browser_type)
        playwright_mgr = async_playwright()

        async with self.stage("preparing"):
            self.playwright = await playwright_mgr.__aenter__()
            browser_type = {
                "chromium": self.playwright.chromium,
                "firefox": self.playwright.firefox,
                "webkit": self.playwright.webkit,
            }[self.browser_type]
            self.browser = await browser_type.launch(**self.launch_config)

        async with self.stage("cleanup"):
            await playwright_mgr.__aexit__()
