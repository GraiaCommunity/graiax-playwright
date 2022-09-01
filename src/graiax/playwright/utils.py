import asyncio
import re
import time
from typing import Optional

from loguru import logger
from playwright._impl._driver import compute_driver_executable, get_driver_env


async def install_playwright(download_host: Optional[str] = None):
    select = re.compile("(\\d+)%")
    downloaded = re.compile("(?P<file>.*) downloaded to (?P<path>.*)")
    last_progress_time = 0

    command = [str(compute_driver_executable()), "install", "chromium"]
    env = get_driver_env()
    if download_host:
        env["PLAYWRIGHT_DOWNLOAD_HOST"] = download_host
    shell = await asyncio.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE, env=env)
    
    if shell.stdout is not None:
        first_line = (await shell.stdout.readline()).decode("UTF-8")

        if not first_line:
            await shell.wait()
            # logger.info("Playwright 已经下载了哦")
            return
        elif "Downloading" not in first_line:
            logger.warning("Playwright 下载停止")
            logger.error(f"下载程序回报意外的内容:\n{first_line}")
            shell.kill()
            return

        while line := (await shell.stdout.readline()).decode("UTF-8"):
            percent = select.findall(line)
            if percent and (time.time() - last_progress_time > 1 or percent[0] == "100"):
                logger.info(f"Downloading {percent[0]}%")
                last_progress_time = time.time()
            elif "downloaded" in line and (p := downloaded.match(line)) is not None:
                p = p.groupdict()
                logger.info(f"{p['file']} 下载成功，下载位置：{p['path']}")
            elif "Downloading" in line:
                logger.info(f"Downloading {line[12:-1]}")
            elif line == "Failed to install browsers\n":
                message = await shell.stdout.read()
                logger.warning("Download Failed:\n" + message.decode("UTF-8"))

    if shell.returncode:
        logger.warning("Playwright 下载失败，请尝试重新运行，或按照官方教程手动下载")
        logger.warning("Playwright 文档地址: https://playwright.dev/python/docs/intro")
        logger.warning("使用命令 poetry run playwright install 或 pdm run playwright install 可手动下载 Playwright")
    else:
        logger.success("Playwright 下载成功")
