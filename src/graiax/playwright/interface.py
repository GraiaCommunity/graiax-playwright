from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncGenerator,
    Dict,
    List,
    Literal,
    Optional,
    Pattern,
    Union,
)

from launart import ExportInterface
from playwright._impl._api_structures import (
    Geolocation,
    HttpCredentials,
    ProxySettings,
    StorageState,
    ViewportSize,
)
from playwright.async_api import Browser, Page
from typing_extensions import Unpack

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
        forced_colors: Optional[Literal["active", "none"]] = None,
        reduced_motion: Optional[Literal["no-preference", "reduce"]] = None,
        accept_downloads: Optional[bool] = None,
        default_browser_type: Optional[str] = None,
        proxy: Optional[ProxySettings] = None,
        record_har_path: Optional[Union[str, Path]] = None,
        record_har_omit_content: Optional[bool] = None,
        record_video_dir: Optional[Union[str, Path]] = None,
        record_video_size: Optional[ViewportSize] = None,
        storage_state: Optional[Union[StorageState, str, Path]] = None,
        base_url: Optional[str] = None,
        strict_selectors: Optional[bool] = None,
        service_workers: Optional[Literal["allow", "block"]] = None,
        record_har_url_filter: Optional[Union[str, Pattern[str]]] = None,
        record_har_mode: Optional[Literal["full", "minimal"]] = None,
        record_har_content: Optional[Literal["attach", "embed", "omit"]] = None,
    ) -> AsyncGenerator[Page, None]:
        """获得一个浏览器页面

        Args:
            context: bool, 是否使用 Browser Context，详见 <https://playwright.dev/python/docs/browser-contexts#browser-context>

        Usage:
            ```python
            from graiax.playwright import PlaywrightBrowser

            browser = launart.get_interface(PlaywrightBrowser)
            async with browser.page(context=True, viewport={"width": 800, "height": 10}, device_scale_factor=1.5) as page:
                await page.set_content("Hello World!")
                img = await page.screenshot(type="jpeg", quality=80, full_page=True, scale='device')
            ```
        """
        ...


if TYPE_CHECKING:
    PlaywrightBrowser = PlaywrightBrowserStub
else:
    PlaywrightBrowser = PlaywrightBrowserImpl
