import pathlib
import typing
from typing import AsyncContextManager, Literal

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
    viewport: typing.Optional[ViewportSize]
    screen: typing.Optional[ViewportSize]
    no_viewport: typing.Optional[bool]
    ignore_https_errors: typing.Optional[bool]
    java_script_enabled: typing.Optional[bool]
    bypass_csp: typing.Optional[bool]
    user_agent: typing.Optional[str]
    locale: typing.Optional[str]
    timezone_id: typing.Optional[str]
    geolocation: typing.Optional[Geolocation]
    permissions: typing.Optional[typing.List[str]]
    extra_http_headers: typing.Optional[typing.Dict[str, str]]
    offline: typing.Optional[bool]
    http_credentials: typing.Optional[HttpCredentials]
    device_scale_factor: typing.Optional[float]
    is_mobile: typing.Optional[bool]
    has_touch: typing.Optional[bool]
    color_scheme: typing.Optional[Literal["dark", "light", "no-preference"]]
    forced_colors: typing.Optional[Literal["active", "none"]]
    reduced_motion: typing.Optional[Literal["no-preference", "reduce"]]
    accept_downloads: typing.Optional[bool]
    default_browser_type: typing.Optional[str]
    proxy: typing.Optional[ProxySettings]
    record_har_path: typing.Optional[typing.Union[str, pathlib.Path]]
    record_har_omit_content: typing.Optional[bool]
    record_video_dir: typing.Optional[typing.Union[str, pathlib.Path]]
    record_video_size: typing.Optional[ViewportSize]
    storage_state: typing.Optional[typing.Union[StorageState, str, pathlib.Path]]
    base_url: typing.Optional[str]
    strict_selectors: typing.Optional[bool]
    service_workers: typing.Optional[Literal["allow", "block"]]
    record_har_url_filter: typing.Optional[typing.Union[str, typing.Pattern[str]]]
    record_har_mode: typing.Optional[Literal["full", "minimal"]]
    record_har_content: typing.Optional[Literal["attach", "embed", "omit"]]


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
