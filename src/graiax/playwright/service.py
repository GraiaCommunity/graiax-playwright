from __future__ import annotations

from pathlib import Path
from typing import Any, Literal, Pattern, overload

from launart import Service
from playwright._impl._api_structures import (
    Geolocation,
    HttpCredentials,
    ProxySettings,
    StorageState,
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
from .utils import brower_config_list, browser_context_config_list, log

P = ParamSpec("P")


class PlaywrightService(Service):
    """用于 launart 的浏览器服务

    Args:
        browser_type (Literal["chromium", "firefox", "webkit"]): 你要使用的浏览器。默认为 Chromium
        auto_download_browser (bool): 是否在启动时自动下载 Playwright 所使用的浏览器或检查其更新。若你需要使用
            本地计算机上已有的 Chromium 浏览器，则可以设置为 False
        playwright_download_host (Optional[str]): 如需自动下载浏览器或检查更新，此处可以指定下载/检查更新的地址
        install_with_deps (bool): 是否在下载安装 Playwright 所使用的浏览器时一同安装缺失的系统依赖，可能需要访问
            sudo 或管理员权限
        user_data_dir: (str | Path | None): 用户数据储存目录。传入该参数且不为 None 时，使用持久性上下文模式启动 Playwright，
            此时将不可通过 `PlaywrightBrowser` 接口获取浏览器实例
        **kwargs: 详见 <https://playwright.dev/python/docs/api/class-browsertype#browser-type-launch>
    """

    id = "web.render/graiax.playwright"
    supported_interface_types = {PlaywrightBrowser, PlaywrightContext}
    playwright: Playwright
    browser: Browser | None = None
    context: BrowserContext
    auto_download_browser: bool
    playwright_download_host: str | None
    use_persistent_context: bool = False  # 指示目前是否以持久性上下文模式启动

    launch_config: dict[str, Any] = {}  # 持久性上下文模式时储存的是持久性上下文的启动参数
    global_context_config: dict[str, Any] = {}  # 仅供非持久性上下文模式时储存全局上下文配置

    @overload
    def __init__(
        self,
        browser_type: Literal["chromium", "firefox", "webkit"] = "chromium",
        *,
        auto_download_browser: bool = True,
        playwright_download_host: str | None = None,
        install_with_deps: bool = False,
        user_data_dir: None = None,
        executable_path: str | Path | None = None,
        channel: str | None = None,
        args: list[str] | None = None,
        ignore_default_args: bool | list[str] | None = None,
        handle_sigint: bool | None = None,
        handle_sigterm: bool | None = None,
        handle_sighup: bool | None = None,
        timeout: float | None = None,
        env: dict[str, str | float | bool] | None = None,
        headless: bool | None = None,
        devtools: bool | None = None,
        downloads_path: str | Path | None = None,
        slow_mo: float | None = None,
        traces_dir: str | Path | None = None,
        chromium_sandbox: bool | None = None,
        firefox_user_prefs: dict[str, str | float | bool] | None = None,
        viewport: ViewportSize | None = None,
        screen: ViewportSize | None = None,
        no_viewport: bool | None = None,
        ignore_https_errors: bool | None = None,
        java_script_enabled: bool | None = None,
        bypass_csp: bool | None = None,
        user_agent: str | None = None,
        locale: str | None = None,
        timezone_id: str | None = None,
        geolocation: Geolocation | None = None,
        permissions: list[str] | None = None,
        extra_http_headers: dict[str, str] | None = None,
        offline: bool | None = None,
        http_credentials: HttpCredentials | None = None,
        device_scale_factor: float | None = None,
        is_mobile: bool | None = None,
        has_touch: bool | None = None,
        color_scheme: Literal["dark", "light", "no-preference", "null"] | None = None,
        reduced_motion: Literal["no-preference", "null", "reduce"] | None = None,
        forced_colors: Literal["active", "none", "null"] | None = None,
        accept_downloads: bool | None = None,
        default_browser_type: str | None = None,
        proxy: ProxySettings | None = None,
        record_har_path: str | Path | None = None,
        record_har_omit_content: bool | None = None,
        record_video_dir: str | Path | None = None,
        record_video_size: ViewportSize | None = None,
        storage_state: StorageState | str | Path | None = None,
        base_url: str | None = None,
        strict_selectors: bool | None = None,
        service_workers: Literal["allow", "block"] | None = None,
        record_har_url_filter: str | Pattern[str] | None = None,
        record_har_mode: Literal["full", "minimal"] | None = None,
        record_har_content: Literal["attach", "embed", "omit"] | None = None,
    ):
        ...

    @overload
    def __init__(
        self,
        browser_type: Literal["chromium", "firefox", "webkit"] = "chromium",
        *,
        auto_download_browser: bool = True,
        playwright_download_host: str | None = None,
        install_with_deps: bool = False,
        user_data_dir: str | Path,
        channel: str | None = None,
        executable_path: str | Path | None = None,
        args: list[str] | None = None,
        ignore_default_args: bool | list[str] | None = None,
        handle_sigint: bool | None = None,
        handle_sigterm: bool | None = None,
        handle_sighup: bool | None = None,
        timeout: float | None = None,
        env: dict[str, str | float | bool] | None = None,
        headless: bool | None = None,
        devtools: bool | None = None,
        proxy: ProxySettings | None = None,
        downloads_path: str | Path | None = None,
        slow_mo: float | None = None,
        viewport: ViewportSize | None = None,
        screen: ViewportSize | None = None,
        no_viewport: bool | None = None,
        ignore_https_errors: bool | None = None,
        java_script_enabled: bool | None = None,
        bypass_csp: bool | None = None,
        user_agent: str | None = None,
        locale: str | None = None,
        timezone_id: str | None = None,
        geolocation: Geolocation | None = None,
        permissions: list[str] | None = None,
        extra_http_headers: dict[str, str] | None = None,
        offline: bool | None = None,
        http_credentials: HttpCredentials | None = None,
        device_scale_factor: float | None = None,
        is_mobile: bool | None = None,
        has_touch: bool | None = None,
        color_scheme: Literal["dark", "light", "no-preference"] | None = None,
        reduced_motion: Literal["no-preference", "reduce"] | None = None,
        forced_colors: Literal["active", "none"] | None = None,
        accept_downloads: bool | None = None,
        traces_dir: str | Path | None = None,
        chromium_sandbox: bool | None = None,
        record_har_path: str | Path | None = None,
        record_har_omit_content: bool | None = None,
        record_video_dir: str | Path | None = None,
        record_video_size: ViewportSize | None = None,
        base_url: str | None = None,
        strict_selectors: bool | None = None,
        service_workers: Literal["allow", "block"] | None = None,
        record_har_url_filter: str | Pattern[str] | None = None,
        record_har_mode: Literal["full", "minimal"] | None = None,
        record_har_content: Literal["attach", "embed", "omit"] | None = None,
    ):
        ...

    def __init__(
        self,
        browser_type: Literal["chromium", "firefox", "webkit"] = "chromium",
        *,
        auto_download_browser: bool = True,
        playwright_download_host: str | None = None,
        install_with_deps: bool = False,
        **kwargs,
    ) -> None:
        self.browser_type: Literal["chromium", "firefox", "webkit"] = browser_type
        self.auto_download_browser = auto_download_browser
        self.playwright_download_host = playwright_download_host
        self.install_with_deps = install_with_deps

        if "user_data_dir" in kwargs and kwargs["user_data_dir"] is not None:
            self.use_persistent_context = True

        if self.use_persistent_context:
            self.launch_config = kwargs
        else:
            for k, v in kwargs.items():
                if k in brower_config_list:
                    self.launch_config[k] = v
                if k in browser_context_config_list:
                    self.global_context_config[k] = v

        super().__init__()

    def get_interface(self, typ: type[PlaywrightBrowser] | type[PlaywrightContext]):
        if typ is PlaywrightBrowser:
            if self.browser:
                return PlaywrightBrowserImpl(service=self, browser=self.browser)
            raise RuntimeError(
                N_("Playwright service is launched by using a persistent context. Fetching browser is not supported.")
            )
        elif typ is PlaywrightContext:
            return PlaywrightContextImpl(service=self, context=self.context)

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
                if self.use_persistent_context:
                    log("info", N_("Playwright is currently starting in persistent context mode."))
                    self.context = await browser_type.launch_persistent_context(**self.launch_config)
                else:
                    self.browser = await browser_type.launch(**self.launch_config)
                    self.context = await self.browser.new_context(**self.global_context_config)
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
