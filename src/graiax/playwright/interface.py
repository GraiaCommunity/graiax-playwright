from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Any, AsyncGenerator, Literal, Pattern

from playwright._impl._api_structures import (
    Geolocation,
    HttpCredentials,
    ProxySettings,
    StorageState,
    ViewportSize,
)
from playwright.async_api import Browser, BrowserContext, Page
from typing_extensions import TypedDict, Unpack

if TYPE_CHECKING:
    from .service import PlaywrightService


class Parameters(TypedDict, total=False):
    viewport: ViewportSize | None
    screen: ViewportSize | None
    no_viewport: bool | None
    ignore_https_errors: bool | None
    java_script_enabled: bool | None
    bypass_csp: bool | None
    user_agent: str | None
    locale: str | None
    timezone_id: str | None
    geolocation: Geolocation | None
    permissions: list[str] | None
    extra_http_headers: dict[str, str] | None
    offline: bool | None
    http_credentials: HttpCredentials | None
    device_scale_factor: float | None
    is_mobile: bool | None
    has_touch: bool | None
    color_scheme: Literal["dark", "light", "no-preference"] | None
    forced_colors: Literal["active", "none"] | None
    reduced_motion: Literal["no-preference", "reduce"] | None
    accept_downloads: bool | None
    default_browser_type: str | None
    proxy: ProxySettings | None
    record_har_path: str | Path | None
    record_har_omit_content: bool | None
    record_video_dir: str | Path | None
    record_video_size: ViewportSize | None
    storage_state: StorageState | str | Path | None
    base_url: str | None
    strict_selectors: bool | None
    service_workers: Literal["allow", "block"] | None
    record_har_url_filter: str | Pattern[str] | None
    record_har_mode: Literal["full", "minimal"] | None
    record_har_content: Literal["attach", "embed", "omit"] | None


class PlaywrightBrowserImpl:
    service: PlaywrightService
    browser: Browser

    def __init__(self, *, service: PlaywrightService, browser: Browser):
        self.service = service
        self.browser = browser

    @asynccontextmanager
    async def page(
        self,
        *,
        new_context: bool = False,
        **kwargs: Unpack[Parameters],
    ) -> AsyncGenerator[Page, None]:
        if new_context:
            page = await (await self.browser.new_context(**kwargs)).new_page()
        else:
            page = await self.browser.new_page(**kwargs)
        yield page
        await page.close()

    if not TYPE_CHECKING:

        def __getattr__(self, name: str) -> Any:
            return self.browser.__getattribute__(name)


class PlaywrightBrowserStub(PlaywrightBrowserImpl, Browser):
    @asynccontextmanager
    async def page(
        self,
        *,
        new_context: bool = False,
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
    ) -> AsyncGenerator[Page, None]:
        """获得一个新的浏览器页面（Page）

        Args:
            new_context (bool): 是否使用一个新的 Browser Context，详见 <https://playwright.dev/python/docs/browser-contexts>。
                若想使用全局通用的 Browser Context，请使用 `PlaywrightContext` 接口

        Usage:
            ```python
            from graiax.playwright import PlaywrightBrowser

            browser = launart.get_interface(PlaywrightBrowser)
            async with browser.page(new_context=True, viewport={"width": 800, "height": 10}, device_scale_factor=1.5) as page:
                await page.set_content("Hello World!")
                img = await page.screenshot(type="jpeg", quality=80, full_page=True, scale='device')
            ```
        """
        ...


class PlaywrightContextImpl:
    service: PlaywrightService
    context: BrowserContext

    def __init__(self, *, service: PlaywrightService, context: BrowserContext):
        self.service = service
        self.context = context

    @asynccontextmanager
    async def page(self) -> AsyncGenerator[Page, None]:
        page = await self.context.new_page()
        yield page
        await page.close()

    if not TYPE_CHECKING:

        def __getattr__(self, name: str) -> Any:
            return self.context.__getattribute__(name)


class PlaywrightContextStub(PlaywrightContextImpl, BrowserContext):
    @asynccontextmanager
    async def page(self) -> AsyncGenerator[Page, None]:
        """获得全局浏览器上下文（Browser Context）

        若使用持久性上下文（Persistent Context）则获得的是持久上下文。
        若没有使用持久性上下文，则获得的是一个全局通用的（会跟随整个生命周期的）上下文

        Usage:
            ```python
            from graiax.playwright import laywrightContext

            context = launart.get_interface(laywrightContext)
            async with context.page() as page:
                await page.set_content("Hello World!")
                img = await page.screenshot(type="jpeg", quality=80, full_page=True, scale='device')
            ```
        """
        ...


if TYPE_CHECKING:
    PlaywrightBrowser = PlaywrightBrowserStub
    PlaywrightContext = PlaywrightContextStub
else:
    PlaywrightBrowser = PlaywrightBrowserImpl
    PlaywrightContext = PlaywrightContextImpl
