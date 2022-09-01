import pathlib
import typing
from typing import TYPE_CHECKING, Any, Dict, Literal

from launart import Service
from playwright._impl._api_structures import ProxySettings
from playwright.async_api import Browser, Playwright, async_playwright
from typing_extensions import ParamSpec, TypedDict

from graiax.playwright.interface import PlaywrightBrowser, PlaywrightBrowserImpl
from .utils import install_playwright

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

    if TYPE_CHECKING:

        def __init__(
            self,
            browser_type: Literal["chromium", "firefox", "webkit"] = "chromium",
            *,
            executable_path: typing.Optional[typing.Union[str, pathlib.Path]] = None,
            channel: typing.Optional[str] = None,
            args: typing.Optional[typing.List[str]] = None,
            ignore_default_args: typing.Optional[typing.Union[bool, typing.List[str]]] = None,
            handle_sigint: typing.Optional[bool] = None,
            handle_sigterm: typing.Optional[bool] = None,
            handle_sighup: typing.Optional[bool] = None,
            timeout: typing.Optional[float] = None,
            env: typing.Optional[typing.Dict[str, typing.Union[str, float, bool]]] = None,
            headless: typing.Optional[bool] = None,
            devtools: typing.Optional[bool] = None,
            proxy: typing.Optional[ProxySettings] = None,
            downloads_path: typing.Optional[typing.Union[str, pathlib.Path]] = None,
            slow_mo: typing.Optional[float] = None,
            traces_dir: typing.Optional[typing.Union[str, pathlib.Path]] = None,
            chromium_sandbox: typing.Optional[bool] = None,
            firefox_user_prefs: typing.Optional[typing.Dict[str, typing.Union[str, float, bool]]] = None,
        ):
            ...

    else:

        def __init__(
            self,
            browser_type: Literal["chromium", "firefox", "webkit"],
            **kwargs,
        ) -> None:
            self.browser_type: Literal["chromium", "firefox", "webkit"] = browser_type
            self.launch_config = kwargs
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
        await install_playwright()
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
