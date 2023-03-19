from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Pattern, Type, Union, overload

from launart import Service
from playwright._impl._api_structures import (
    Geolocation,
    HttpCredentials,
    ProxySettings,
    ViewportSize,
)
from playwright.async_api import Browser, BrowserContext
from playwright.async_api import Error as PWError
from playwright.async_api import Playwright, async_playwright
from typing_extensions import ParamSpec

from .i18n import N_
from .installer import install_playwright
from .interface import (
    PlaywrightBrowser,
    PlaywrightBrowserImpl,
    PlaywrightContext,
    PlaywrightContextImpl,
)
from .utils import log

P = ParamSpec("P")


class PlaywrightService(Service):
    """用于 launart 的浏览器服务

    Args:
        browser_type (Literal["chromium", "firefox", "webkit"]): 你要使用的浏览器，默认为 Chromium
        auto_download_browser (bool): 是否在启动时自动下载 Playwright 所使用的浏览器或检查其更新，若你需要使用
            本地计算机上已有的 Chromium 浏览器，则可以设置为 False
        playwright_download_host (Optional[str]): 如需自动下载浏览器或检查更新，此处可以指定下载/检查更新的地址
        install_with_deps (bool):是否在下载安装 Playwright 所使用的浏览器时一同安装缺失的系统依赖，可能需要访问 sudo 或管理员权限
        **kwargs: 参见 <https://playwright.dev/python/docs/api/class-browsertype#browser-type-launch>
    """

    id = "web.render/playwright"
    supported_interface_types = {PlaywrightBrowser, PlaywrightContext}
    playwright: Playwright
    browser: Union[Browser, None]
    context: BrowserContext
    launch_config: Dict[str, Any]
    auto_download_browser: bool
    playwright_download_host: Optional[str]

    @overload
    def __init__(
        self,
        browser_type: Literal["chromium", "firefox", "webkit"] = "chromium",
        auto_download_browser: bool = True,
        playwright_download_host: Optional[str] = None,
        install_with_deps: bool = False,
        *,
        user_data_dir: None = None,
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

    @overload
    def __init__(
        self,
        browser_type: Literal["chromium", "firefox", "webkit"] = "chromium",
        auto_download_browser: bool = True,
        playwright_download_host: Optional[str] = None,
        install_with_deps: bool = False,
        *,
        user_data_dir: Union[str, Path],
        channel: Optional[str] = None,
        executable_path: Optional[Union[str, Path]] = None,
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
        viewport: Optional[ViewportSize] = None,
        screen: Optional[ViewportSize] = None,
        no_viewport: Optional[bool] = None,
        ignore_https_errors: Optional[bool] = None,
        java_script_enabled: Optional[bool] = None,
        bypass_csp: Optional[bool] = None,
        user_agent: Optional[str] = None,
        locale: Optional[str] = None,
        timezone_id: Optional[str] = None,
        geolocation: Optional[Geolocation] = None,
        permissions: Optional[List[str]] = None,
        extra_http_headers: Optional[Dict[str, str]] = None,
        offline: Optional[bool] = None,
        http_credentials: Optional[HttpCredentials] = None,
        device_scale_factor: Optional[float] = None,
        is_mobile: Optional[bool] = None,
        has_touch: Optional[bool] = None,
        color_scheme: Optional[Literal["dark", "light", "no-preference"]] = None,
        reduced_motion: Optional[Literal["no-preference", "reduce"]] = None,
        forced_colors: Optional[Literal["active", "none"]] = None,
        accept_downloads: Optional[bool] = None,
        traces_dir: Optional[Union[str, Path]] = None,
        chromium_sandbox: Optional[bool] = None,
        record_har_path: Optional[Union[str, Path]] = None,
        record_har_omit_content: Optional[bool] = None,
        record_video_dir: Optional[Union[str, Path]] = None,
        record_video_size: Optional[ViewportSize] = None,
        base_url: Optional[str] = None,
        strict_selectors: Optional[bool] = None,
        service_workers: Optional[Literal["allow", "block"]] = None,
        record_har_url_filter: Optional[Union[str, Pattern[str]]] = None,
        record_har_mode: Optional[Literal["full", "minimal"]] = None,
        record_har_content: Optional[Literal["attach", "embed", "omit"]] = None,
    ):
        ...

    def __init__(
        self,
        browser_type: Literal["chromium", "firefox", "webkit"] = "chromium",
        auto_download_browser: bool = True,
        playwright_download_host: Optional[str] = None,
        install_with_deps: bool = False,
        **kwargs,
    ) -> None:
        self.browser_type: Literal["chromium", "firefox", "webkit"] = browser_type
        self.launch_config = kwargs
        self.auto_download_browser = auto_download_browser
        self.playwright_download_host = playwright_download_host
        self.install_with_deps = install_with_deps
        self.browser = None
        super().__init__()

    def get_interface(self, typ: Union[Type[PlaywrightBrowser], Type[PlaywrightContext]]):
        if typ is PlaywrightBrowser:
            if self.browser:
                return PlaywrightBrowserImpl(self, self.browser)
            raise RuntimeError(
                N_("Playwright service is launched by using a persistent context. Fetching browser is not supported.")
            )
        elif typ is PlaywrightContext:
            return PlaywrightContextImpl(self, self.context)

    @property
    def required(self):
        return set()

    @property
    def stages(self):
        return {"preparing", "cleanup"}

    async def launch(self, _):
        if self.auto_download_browser:
            await install_playwright(
                self.playwright_download_host,
                self.browser_type,
                self.install_with_deps,
            )

        playwright_mgr = async_playwright()

        async with self.stage("preparing"):
            self.playwright = await playwright_mgr.__aenter__()
            browser_type = {
                "chromium": self.playwright.chromium,
                "firefox": self.playwright.firefox,
                "webkit": self.playwright.webkit,
            }[self.browser_type]
            try:
                if "user_data_dir" not in self.launch_config:
                    self.browser = await browser_type.launch(**self.launch_config)
                    self.context = await self.browser.new_context()
                else:
                    self.context = await browser_type.launch_persistent_context(**self.launch_config)
            except PWError:
                log(
                    "error",
                    N_(
                        "Unable to launch Playwright for {browser_type}, "
                        "please check the log output for the reason of failure. "
                        "It is possible that some system dependencies are missing. "
                        "You can set [magenta]`install_with_deps`[/] to [magenta]`True`[/] "
                        "to install dependencies when download browser."
                    ).format(browser_type=self.browser_type),
                )
                raise
            else:
                log("success", N_("Playwright for {browser_type} is started.").format(browser_type=self.browser_type))

        async with self.stage("cleanup"):
            # await self.context.close()  # 这里会卡住
            await playwright_mgr.__aexit__()
