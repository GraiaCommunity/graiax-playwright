import asyncio
import re
from typing import Optional

from playwright._impl._driver import compute_driver_executable, get_driver_env

from .i18n import N_, WINDOWS
from .utils import Progress, log

download_complete = re.compile("(?P<file>.*) downloaded to (?P<path>.*)")
percent_pat = re.compile("(\\d+)%")


async def install_playwright(
    download_host: Optional[str] = None,
    browser_type: str = "chromium",
    install_with_deps: bool = False,
):
    env = get_driver_env()
    if download_host:
        env["PLAYWRIGHT_DOWNLOAD_HOST"] = download_host

    if install_with_deps:
        command = [str(compute_driver_executable()), "install", "--with-deps", browser_type]
        if WINDOWS:
            log(
                "info",
                N_(
                    "Start download Playwright for {browser_type} with dependencies, "
                    "may require administrator privileges from you."
                ).format(browser_type=browser_type),
            )
        else:
            log(
                "info",
                N_(
                    "Start download Playwright for {browser_type} with dependencies, may require you to access sudo."
                ).format(browser_type=browser_type),
            )
    else:
        command = [str(compute_driver_executable()), "install", browser_type]
        log("info", N_("Start download Playwright for {browser_type}.").format(browser_type=browser_type))

    shell = await asyncio.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE, env=env)
    returncode = None

    assert shell.stdout

    progress: Optional[Progress] = None

    while line := (await shell.stdout.readline()).decode("UTF-8"):
        if "Downloading" in line:
            progress = Progress(line[12:-1])
        if percent := percent_pat.findall(line):
            progress_target = float(percent[0])
            if progress:
                progress.update(target=progress_target)
        elif p := download_complete.match(line):
            p = p.groupdict()
            log(
                "success", N_("Downloaded [cyan]{file}[/] to [magenta]{path}[/]").format(file=p["file"], path=p["path"])
            )
        elif line == "Failed to install browsers\n":
            message = await shell.stdout.read()
            log("error", N_("Download Failed:\n") + message.decode("UTF-8"))
            returncode = 1

    if returncode or shell.returncode:
        log("error", N_("Failed to download Playwright for {browser_type}.").format(browser_type=browser_type))
        log("error", N_("Please see: [magenta]https://playwright.dev/python/docs/intro[/]"))
        log(
            "error",
            N_(
                "Run [magenta]poetry run playwright install[/] or "
                "[magenta]pdm run playwright install[/] to install Playwright manually."
            ),
        )
    else:
        log("success", N_("Playwright for {browser_type} is installed.").format(browser_type=browser_type))
