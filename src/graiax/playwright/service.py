from collections.abc import AsyncGenerator
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from pathlib import Path
from re import Pattern
from typing import Any, Literal, overload
from warnings import warn

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
from playwright.async_api import Page, Playwright, async_playwright
from typing_extensions import ParamSpec, Unpack

from .i18n import N_
from .installer import install_playwright
from .utils import Parameters, brower_config_list, browser_context_config_list, log

P = ParamSpec("P")


class PlaywrightServiceStub:
    _browser: Browser | None = None
    _context: BrowserContext
    use_persistent_context: bool = False  # 指示目前是否以持久性上下文模式启动


class PlaywrightPageInterface(PlaywrightServiceStub):
    @overload
    def page(
        self,
        *,
        use_global_context: Literal[True] = True,
        without_new_context: Literal[True] = True,
    ) -> AbstractAsyncContextManager[Page]:
        """
        获得一个新的浏览器页面（playwright.async_api.Page），并使用全局上下文。

        Args:
            use_global_context (Literal[True]): 是否使用全局上下文，该选项默认为 True。
                当你传入新上下文或新页面的参数时，该选项将会被忽略，将不使用全局上下文。
                当你使用持久化上下文模式启动 Playwright 时，则只能使用全局上下文，也无法传入更多额外参数。
            without_new_context (Literal[True]): 是否开一个新的上下文。
                当你使用全局上下文时，该选项无意义且必须为 True。

        Returns:
            AbstractAsyncContextManager[Page]: 这是一个异步生成器，请参照文档使用。

        Usage:
            ```python
            from graiax.playwright import PlaywrightService

            pw_service = manager.get_component(PlaywrightService)
            async with pw_service.page() as page:
                await page.set_content("Hello World!")
                img = await page.screenshot(type="jpeg", quality=80, full_page=True, scale='device')
            ```
        """
        ...

    @overload
    def page(
        self,
        *,
        use_global_context: bool = True,
        without_new_context: bool = True,
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
        forced_colors: Literal["active", "none"] | None = None,
        reduced_motion: Literal["no-preference", "reduce"] | None = None,
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
    ) -> AbstractAsyncContextManager[Page]:
        """
        获得一个新的浏览器页面（playwright.async_api.Page），并传入新上下文或新页面的参数。

        Args:
            use_global_context (bool): 是否使用全局上下文，该选项默认为 True。
                当你传入新上下文或新页面的参数时，该选项将会被忽略，将不使用全局上下文。
                当你使用持久化上下文模式启动 Playwright 时，则只能使用全局上下文，也无法传入更多额外参数。
            without_new_context (bool, optional): 是否开一个新的上下文。默认为 True。
                即使你不使用全局上下文而是开一个新的上下文，仍然会受到 Playwright 启动参数的影响。
            **kwargs: 更多参数，用法及释义请参阅：
                - 当 `without_new_context` 为 `True` 时： <https://playwright.dev/python/docs/api/class-browser#browser-new-page>
                - 当 `without_new_context` 为 `False` 时： <https://playwright.dev/python/docs/api/class-browser#browser-new-context>

        Returns:
            AbstractAsyncContextManager[Page]: 这是一个异步生成器，请参照文档使用。

        Usage:
            ```python
            from graiax.playwright import PlaywrightService

            pw_service = manager.get_component(PlaywrightService)
            async with pw_service.page(
                viewport={"width": 300, "height": 100},
            ) as page:
                await page.set_content("Hello World!")
                img = await page.screenshot(type="jpeg", quality=80, full_page=True, scale='device')
            ```
        """
        ...

    @asynccontextmanager
    async def page(
        self,
        *,
        use_global_context: bool = True,
        without_new_context: bool = True,
        **kwargs: Unpack[Parameters],
    ) -> AsyncGenerator[Page, None]:
        """
        获得一个新的浏览器页面（playwright.async_api.Page）。

        Args:
            use_global_context (Literal[True]): 是否使用全局上下文，该选项默认为 True。
                当你传入新上下文或新页面的参数时，该选项将会被忽略，将不使用全局上下文。
                当你使用持久化上下文模式启动 Playwright 时，则只能使用全局上下文，也无法传入更多额外参数。
            without_new_context (Literal[True]): 是否开一个新的上下文。
                当你使用全局上下文时，该选项无意义且必须为 True。
                即使你不使用全局上下文而是开一个新的上下文，仍然会受到 Playwright 启动参数的影响。
            **kwargs: 更多参数，用法及释义请参阅：
                - 当 `without_new_context` 为 `True` 时： <https://playwright.dev/python/docs/api/class-browser#browser-new-page>
                - 当 `without_new_context` 为 `False` 时： <https://playwright.dev/python/docs/api/class-browser#browser-new-context>

        Returns:
            AsyncGenerator[Page, None]: 这是一个异步生成器，请参照文档使用。

        Usage:
            ```python
            from graiax.playwright import PlaywrightService

            pw_service = manager.get_component(PlaywrightService)
            async with pw_service.page(...) as page:
                await page.set_content("Hello World!")
                img = await page.screenshot(type="jpeg", quality=80, full_page=True, scale='device')
            ```
        """
        if self._context is None:
            raise RuntimeError(N_("Playwright has not been started yet, you cannot use the this method at this time"))
        if self.use_persistent_context and not use_global_context:
            raise RuntimeError(
                N_("Playwright service is launched by using a persistent context. So you must use global context.")
            )
        if self.use_persistent_context:
            if kwargs:
                warn(N_("`Prsistent Context` cannot accept additional parameters. Ignore it."))
            page = await self._context.new_page()
            try:
                yield page
            finally:
                await page.close()
                return

        if use_global_context and not kwargs:
            page = await self._context.new_page()
            try:
                yield page
            finally:
                await page.close()
                return

        if self._browser is None:
            raise RuntimeError(N_("Playwright has not been started yet, you cannot use the this method at this time"))
        context = None
        if without_new_context:
            page = await self._browser.new_page(**kwargs)
        else:
            context = await self._browser.new_context(**kwargs)
            page = await context.new_page()
        try:
            yield page
        finally:
            await page.close()
            if context is not None:
                await context.close()
            return


class PlaywrightContextInterface(PlaywrightServiceStub):
    @overload
    def context(self, *, use_global_context: Literal[True] = True) -> AbstractAsyncContextManager[BrowserContext]:
        """
        获得一个新的浏览器上下文（playwright.async_api.BrowserContext）。

        Args:
            use_global_context (Literal[True]): 是否使用全局上下文，该选项默认为 True。
                当你使用持久化上下文模式启动 Playwright 时，则只能使用全局上下文，也无法传入更多额外参数。

        Returns:
            AbstractAsyncContextManager[BrowserContext]: 这是一个异步生成器，请参照文档使用。

        Usage:
            ```python
            from graiax.playwright import PlaywrightService

            pw_service = manager.get_component(PlaywrightService)
            async with pw_service.context() as context:
                page = context.new_page()
                try:
                    await page.set_content("Hello World!")
                    img = await page.screenshot(type="jpeg", quality=80, full_page=True, scale='device')
                finally:
                    page.stop()
            ```
        """
        ...

    @overload
    def context(
        self,
        *,
        use_global_context: Literal[False] = False,
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
        forced_colors: Literal["active", "none"] | None = None,
        reduced_motion: Literal["no-preference", "reduce"] | None = None,
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
    ) -> AbstractAsyncContextManager[BrowserContext]:
        """
        获得一个新的浏览器上下文（playwright.async_api.BrowserContext）。

        Args:
            use_global_context (Literal[False]): 是否使用全局上下文，该选项默认为 True。
                当你传入新上下文的参数时，该选项将会被忽略，将不使用全局上下文。
                当你使用持久化上下文模式启动 Playwright 时，则只能使用全局上下文，也无法传入更多额外参数。
            **kwargs: 更多参数，用法及释义请参阅 <https://playwright.dev/python/docs/api/class-browser#browser-new-context>

        Returns:
            AbstractAsyncContextManager[BrowserContext]: 这是一个异步生成器，请参照文档使用。

        Usage:
            ```python
            from graiax.playwright import PlaywrightService

            pw_service = manager.get_component(PlaywrightService)
            async with pw_service.context(
                viewport={"width": 300, "height": 100},
            ) as context:
                page = context.new_page()
                try:
                    await page.set_content("Hello World!")
                    img = await page.screenshot(type="jpeg", quality=80, full_page=True, scale='device')
                finally:
                    page.stop()
            ```
        """
        ...

    @asynccontextmanager
    async def context(
        self,
        *,
        use_global_context: bool = True,
        **kwargs: Unpack[Parameters],
    ) -> AsyncGenerator[BrowserContext, None]:
        """
        获得一个新的浏览器上下文（playwright.async_api.BrowserContext）。

        Args:
            use_global_context (Literal[False]): 是否使用全局上下文，该选项默认为 True。
                当你传入新上下文的参数时，该选项将会被忽略，将不使用全局上下文。
                当你使用持久化上下文模式启动 Playwright 时，则只能使用全局上下文，也无法传入更多额外参数。
            **kwargs: 更多参数，用法及释义请参阅 <https://playwright.dev/python/docs/api/class-browser#browser-new-context>

        Returns:
            AsyncGenerator[BrowserContext, None]: 这是一个异步生成器，请参照文档使用。

        Usage:
            ```python
            from graiax.playwright import PlaywrightService

            pw_service = manager.get_component(PlaywrightService)
            async with pw_service.context(...) as context:
                page = context.new_page()
                try:
                    await page.set_content("Hello World!")
                    img = await page.screenshot(type="jpeg", quality=80, full_page=True, scale='device')
                finally:
                    page.stop()
            ```
        """
        if self._context is None:
            raise RuntimeError(N_("Playwright has not been started yet, you cannot use the this method at this time"))
        if self.use_persistent_context and not use_global_context:
            raise RuntimeError(
                N_("Playwright service is launched by using a persistent context. So you must use global context.")
            )
        if self.use_persistent_context:
            if kwargs:
                warn(N_("`Prsistent Context` cannot accept additional parameters. Ignore it."))
            yield self._context
            return

        if self._browser is None:
            raise RuntimeError(N_("Playwright has not been started yet, you cannot use the this method at this time"))

        if use_global_context and not kwargs:
            yield self._context
            return

        context = await self._browser.new_context(**kwargs)
        try:
            yield context
        finally:
            await context.close()
            return


class PlaywrightService(Service, PlaywrightPageInterface, PlaywrightContextInterface):
    """用于 launart 的浏览器服务

    Args:
        browser_type (Literal["chromium", "firefox", "webkit"]): 你要使用的浏览器。默认为 Chromium
        auto_download_browser (bool): 是否在启动时自动下载 Playwright 所使用的浏览器或检查其更新。若你需要使用
            本地计算机上已有的 Chromium 浏览器，则可以设置为 False
        playwright_download_host (Optional[str]): 如需自动下载浏览器或检查更新，此处可以指定下载/检查更新的地址
        install_with_deps (bool): 是否在下载安装 Playwright 所使用的浏览器时一同安装缺失的系统依赖，可能需要访问
            sudo 或管理员权限
        user_data_dir: (str | Path | None): 用户数据储存目录。传入该参数且不为 None 时，使用持久性上下文模式启动
            Playwright，此时将不可通过 `PlaywrightBrowser` 接口获取浏览器实例
        **kwargs: 详见 <https://playwright.dev/python/docs/api/class-browsertype#browser-type-launch>
    """

    id = "web.render/graiax.playwright"
    playwright: Playwright
    auto_download_browser: bool
    playwright_download_host: str | None

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
                    self._context = await browser_type.launch_persistent_context(**self.launch_config)
                else:
                    self._browser = await browser_type.launch(**self.launch_config)
                    self._context = await self._browser.new_context(**self.global_context_config)
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
