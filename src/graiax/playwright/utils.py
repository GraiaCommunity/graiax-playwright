import re
import asyncio
import time

from loguru import logger
from playwright._impl._driver import compute_driver_executable, get_driver_env

async def install_playwright(download_host: str = None):   
    select = re.compile(r"(\d+)%")
    downloaded = re.compile(r"(?P<file>.*) downloaded to (?P<path>.*)")
    last_progress_time = 0

    command = [str(compute_driver_executable()), "install", "chromium"]
    env = get_driver_env()
    if download_host:
        env["PLAYWRIGHT_DOWNLOAD_HOST"] = download_host
    shell = await asyncio.create_subprocess_exec(*command,
                                                 stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.STDOUT,
                                                 env=env)
    
    first_line = (await shell.stdout.readline()).decode('UTF-8')

    if not first_line:
        await shell.wait()
        logger.info("已经下载了哦")
        return
    elif not "Downloading" in first_line:
        logger.warning(f"wtf:\n{first_line}")
        return
    
    while line := (await shell.stdout.readline()).decode('UTF-8'):
        percent = select.findall(line)
        if percent and (time.time() - last_progress_time > 1 or percent[0] == "100"):
            logger.info(f"Downloading {percent[0]}%")
            last_progress_time = time.time()
        elif 'downloaded' in line:
            p = downloaded.match(line).groupdict()
            logger.info(f"{p['file']} 下载成功，下载位置：{p['path']}")
        elif 'Downloading' in line:
            logger.info(f"Downloading {line[12:-1]}")
        elif line == "Failed to install browsers\n":
            message = await shell.stdout.read()
            logger.warning("Download Failed:\n" + message.decode("UTF-8"))

    if shell.returncode:
        logger.warning("下载失败，请重新启动，或者其他")
    else:
        logger.success("下载成功")