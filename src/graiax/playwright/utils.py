from pathlib import Path
from re import Pattern
from typing import Literal

from loguru import logger
from playwright._impl._api_structures import (
    Geolocation,
    HttpCredentials,
    ProxySettings,
    StorageState,
    ViewportSize,
)
from typing_extensions import TypedDict


def log(level: str, rich_text: str) -> None:
    getattr(logger.opt(colors=True), level)(
        rich_text.replace("[", "<").replace("]", ">"),
        alt=rich_text,
    )


class Progress:
    def __init__(self, name: str) -> None:
        self.last_updated: float = 0
        self.progress: float = 0.0
        self.name = name

    def update(self, *, target: float):
        import time

        if self.progress >= 100:
            return
        if (
            time.time() - self.last_updated >= 1
            or (target - self.progress >= 10 and time.time() - self.last_updated >= 0.1)
            or target == 100
        ):
            self.progress = target
            log(
                "info",
                f"[cyan]{self.name}[/] [green]{'-' * int(self.progress / 5):<20}[/] [magenta]{int(self.progress)}%[/]",
            )
            self.last_updated = time.time()


brower_config_list = [
    "executable_path",
    "channel",
    "args",
    "ignore_default_args",
    "handle_sigint",
    "handle_sigterm",
    "handle_sighup",
    "timeout",
    "env",
    "headless",
    "devtools",
    "proxy",
    "downloads_path",
    "slow_mo",
    "traces_dir",
    "chromium_sandbox",
    "firefox_user_prefs",
]

browser_context_config_list = [
    "viewport",
    "screen",
    "no_viewport",
    "ignore_https_errors",
    "java_script_enabled",
    "bypass_csp",
    "user_agent",
    "locale",
    "timezone_id",
    "geolocation",
    "permissions",
    "extra_http_headers",
    "offline",
    "http_credentials",
    "device_scale_factor",
    "is_mobile",
    "has_touch",
    "color_scheme",
    "reduced_motion",
    "forced_colors",
    "accept_downloads",
    "default_browser_type",
    "proxy",
    "record_har_path",
    "record_har_omit_content",
    "record_video_dir",
    "record_video_size",
    "storage_state",
    "base_url",
    "strict_selectors",
    "service_workers",
    "record_har_url_filter",
    "record_har_mode",
    "record_har_content",
]


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
