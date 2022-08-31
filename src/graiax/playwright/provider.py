# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Dict, List, Literal, Optional, Pattern, Union

from launart import ExportInterface
from playwright._impl._api_structures import (
    Geolocation,
    HttpCredentials,
    ProxySettings,
    StorageState,
    ViewportSize,
)

from .browser import PlaywrightBrowser
from .get_page import GetContextPage, GetPage


class BrowserProvider(ExportInterface):
    """获取 Playwright 的 Browser 实例的接口"""

    browser: PlaywrightBrowser

    def __init__(self, browser):
        self.browser = browser
        super().__init__()

    def get_page(
        self,
        context: bool = False,  # 是否使用 Browser Context，详见：https://playwright.dev/python/docs/browser-contexts
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
    ):
        """获得一个浏览器页面

        Args:
            context: bool, 是否使用

        Usage:
            ```python
            from graiax.playwright import BrowserProvider

            browser = launart.get_interface(BrowserProvider)
            async with browser.get_page(context=True, viewport={'width': 800, 'height': 10}, device_scale_factor=1.5) as page:
                await page.set_content('Hello World!')
                img = await page.screenshot(type='jpeg', quality=80, full_page=True, scale='device')
            ```
        """
        if context:
            return GetContextPage(
                browser=self.browser.get(),
                viewport=viewport,
                screen=screen,
                no_viewport=no_viewport,
                ignore_https_errors=ignore_https_errors,
                java_script_enabled=java_script_enabled,
                bypass_csp=bypass_csp,
                user_agent=user_agent,
                locale=locale,
                timezone_id=timezone_id,
                geolocation=geolocation,
                permissions=permissions,
                extra_http_headers=extra_http_headers,
                offline=offline,
                http_credentials=http_credentials,
                device_scale_factor=device_scale_factor,
                is_mobile=is_mobile,
                has_touch=has_touch,
                color_scheme=color_scheme,
                reduced_motion=reduced_motion,
                forced_colors=forced_colors,
                accept_downloads=accept_downloads,
                default_browser_type=default_browser_type,
                proxy=proxy,
                record_har_path=record_har_path,
                record_har_omit_content=record_har_omit_content,
                record_video_dir=record_video_dir,
                record_video_size=record_video_size,
                storage_state=storage_state,
                base_url=base_url,
                strict_selectors=strict_selectors,
                service_workers=service_workers,
                record_har_url_filter=record_har_url_filter,
                record_har_mode=record_har_mode,
                record_har_content=record_har_content,
            )
        else:
            return GetPage(
                browser=self.browser.get(),
                viewport=viewport,
                screen=screen,
                no_viewport=no_viewport,
                ignore_https_errors=ignore_https_errors,
                java_script_enabled=java_script_enabled,
                bypass_csp=bypass_csp,
                user_agent=user_agent,
                locale=locale,
                timezone_id=timezone_id,
                geolocation=geolocation,
                permissions=permissions,
                extra_http_headers=extra_http_headers,
                offline=offline,
                http_credentials=http_credentials,
                device_scale_factor=device_scale_factor,
                is_mobile=is_mobile,
                has_touch=has_touch,
                color_scheme=color_scheme,
                reduced_motion=reduced_motion,
                forced_colors=forced_colors,
                accept_downloads=accept_downloads,
                default_browser_type=default_browser_type,
                proxy=proxy,
                record_har_path=record_har_path,
                record_har_omit_content=record_har_omit_content,
                record_video_dir=record_video_dir,
                record_video_size=record_video_size,
                storage_state=storage_state,
                base_url=base_url,
                strict_selectors=strict_selectors,
                service_workers=service_workers,
                record_har_url_filter=record_har_url_filter,
                record_har_mode=record_har_mode,
                record_har_content=record_har_content,
            )
