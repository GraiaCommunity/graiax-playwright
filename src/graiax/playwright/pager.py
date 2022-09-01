from pathlib import Path
from typing import AsyncContextManager, Dict, List, Literal, Optional, Pattern, Union

from playwright._impl._api_structures import (
    Geolocation,
    HttpCredentials,
    ProxySettings,
    StorageState,
    ViewportSize,
)
from playwright.async_api import Browser, BrowserContext, Page
from typing_extensions import TypedDict, Unpack


class Parameters(TypedDict, total=False):
    viewport: Optional[ViewportSize]
    screen: Optional[ViewportSize]
    no_viewport: Optional[bool]
    ignore_https_errors: Optional[bool]
    java_script_enabled: Optional[bool]
    bypass_csp: Optional[bool]
    user_agent: Optional[str]
    locale: Optional[str]
    timezone_id: Optional[str]
    geolocation: Optional[Geolocation]
    permissions: Optional[List[str]]
    extra_http_headers: Optional[Dict[str, str]]
    offline: Optional[bool]
    http_credentials: Optional[HttpCredentials]
    device_scale_factor: Optional[float]
    is_mobile: Optional[bool]
    has_touch: Optional[bool]
    color_scheme: Optional[Literal["dark", "light", "no-preference"]]
    forced_colors: Optional[Literal["active", "none"]]
    reduced_motion: Optional[Literal["no-preference", "reduce"]]
    accept_downloads: Optional[bool]
    default_browser_type: Optional[str]
    proxy: Optional[ProxySettings]
    record_har_path: Optional[Union[str, Path]]
    record_har_omit_content: Optional[bool]
    record_video_dir: Optional[Union[str, Path]]
    record_video_size: Optional[ViewportSize]
    storage_state: Optional[Union[StorageState, str, Path]]
    base_url: Optional[str]
    strict_selectors: Optional[bool]
    service_workers: Optional[Literal["allow", "block"]]
    record_har_url_filter: Optional[Union[str, Pattern[str]]]
    record_har_mode: Optional[Literal["full", "minimal"]]
    record_har_content: Optional[Literal["attach", "embed", "omit"]]


class RegularPage(AsyncContextManager[Page]):
    browser: Browser
    page: Page

    def __init__(self, browser: Browser, **kwargs: Unpack[Parameters]):
        self.browser = browser
        self.kwargs = kwargs

    async def __aenter__(self) -> Page:
        self.page = await self.browser.new_page(**self.kwargs)
        return self.page

    async def __aexit__(self, *args) -> None:
        await self.page.close()
        return None


class ContextualPage(AsyncContextManager[Page]):
    browser: Browser
    context: BrowserContext
    page: Page

    def __init__(self, browser: Browser, **kwargs: Unpack[Parameters]):
        self.browser = browser
        self.kwargs = kwargs

    async def __aenter__(self) -> Page:
        self.context = await self.browser.new_context(**self.kwargs)
        self.page = await self.context.new_page()
        return self.page

    async def __aexit__(self, *args) -> None:
        await self.page.close()
        await self.context.close()
        return None
