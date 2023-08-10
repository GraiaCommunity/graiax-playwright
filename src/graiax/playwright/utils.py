from loguru import logger


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
