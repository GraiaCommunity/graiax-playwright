from __future__ import annotations

import pathlib
import typing
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any, AsyncGenerator, Literal

from launart import ExportInterface
from playwright._impl._api_structures import (
    Geolocation,
    HttpCredentials,
    ProxySettings,
    StorageState,
    ViewportSize,
)
from playwright.async_api import Browser, BrowserContext, Page
from typing_extensions import TypedDict, Unpack

from graiax.playwright.pager import ContextualPage, Parameters, RegularPage

if TYPE_CHECKING:
    from .service import PlaywrightService


class PlaywrightBrowserImpl(ExportInterface["PlaywrightService"]):
    service: PlaywrightService
    browser: Browser

    def __init__(self, service: PlaywrightService, browser: Browser):
        self.service = service
        self.browser = browser

    @asynccontextmanager
    async def page(
        self,
        *,
        context: bool = False,
        **kwargs: Unpack[Parameters],
    ) -> AsyncGenerator[Page, None]:
        async with (ContextualPage if context else RegularPage)(self.browser, **kwargs) as page:
            yield page

    if not TYPE_CHECKING:

        def __getattr__(self, name: str) -> Any:
            return self.browser.__getattribute__(name)


class PlaywrightBrowserStub(PlaywrightBrowserImpl, Browser):
    service: PlaywrightService
    browser: Browser

    @asynccontextmanager
    async def page(
        self,
        *,
        context: bool = False,
        viewport: typing.Optional[ViewportSize] = None,
        screen: typing.Optional[ViewportSize] = None,
        no_viewport: typing.Optional[bool] = None,
        ignore_https_errors: typing.Optional[bool] = None,
        java_script_enabled: typing.Optional[bool] = None,
        bypass_csp: typing.Optional[bool] = None,
        user_agent: typing.Optional[str] = None,
        locale: typing.Optional[str] = None,
        timezone_id: typing.Optional[str] = None,
        geolocation: typing.Optional[Geolocation] = None,
        permissions: typing.Optional[typing.List[str]] = None,
        extra_http_headers: typing.Optional[typing.Dict[str, str]] = None,
        offline: typing.Optional[bool] = None,
        http_credentials: typing.Optional[HttpCredentials] = None,
        device_scale_factor: typing.Optional[float] = None,
        is_mobile: typing.Optional[bool] = None,
        has_touch: typing.Optional[bool] = None,
        color_scheme: typing.Optional[Literal["dark", "light", "no-preference"]] = None,
        forced_colors: typing.Optional[Literal["active", "none"]] = None,
        reduced_motion: typing.Optional[Literal["no-preference", "reduce"]] = None,
        accept_downloads: typing.Optional[bool] = None,
        default_browser_type: typing.Optional[str] = None,
        proxy: typing.Optional[ProxySettings] = None,
        record_har_path: typing.Optional[typing.Union[str, pathlib.Path]] = None,
        record_har_omit_content: typing.Optional[bool] = None,
        record_video_dir: typing.Optional[typing.Union[str, pathlib.Path]] = None,
        record_video_size: typing.Optional[ViewportSize] = None,
        storage_state: typing.Optional[typing.Union[StorageState, str, pathlib.Path]] = None,
        base_url: typing.Optional[str] = None,
        strict_selectors: typing.Optional[bool] = None,
        service_workers: typing.Optional[Literal["allow", "block"]] = None,
        record_har_url_filter: typing.Optional[typing.Union[str, typing.Pattern[str]]] = None,
        record_har_mode: typing.Optional[Literal["full", "minimal"]] = None,
        record_har_content: typing.Optional[Literal["attach", "embed", "omit"]] = None,
    ) -> AsyncGenerator[Page, None]:
        """获得一个浏览器页面

        Args:
            context: bool, 是否使用

        Usage:
            ```python
            from graiax.playwright import PlaywrightBrowser

            browser = launart.get_interface(PlaywrightBrowser)
            async with browser.get_page(context=True, viewport={'width': 800, 'height': 10}, device_scale_factor=1.5) as page:
                await page.set_content('Hello World!')
                img = await page.screenshot(type='jpeg', quality=80, full_page=True, scale='device')
            ```
        """
        ...


if TYPE_CHECKING:
    PlaywrightBrowser = PlaywrightBrowserStub
else:
    PlaywrightBrowser = PlaywrightBrowserImpl
