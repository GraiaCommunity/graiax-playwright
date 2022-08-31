# -*- coding: utf-8 -*-

import subprocess

from loguru import logger
from playwright._impl._driver import compute_driver_executable, get_driver_env


def install_playwright():
    """自动安装、更新 Chromium"""

    logger.info("正在检查 Chromium 更新")
    env = get_driver_env()
    env["PLAYWRIGHT_DOWNLOAD_HOST"] = "https://playwright.sk415.workers.dev"
    driver_executable = compute_driver_executable()
    completed_process = subprocess.run([str(driver_executable), "install", "chromium"], env=env)
    if completed_process.returncode != 0:
        logger.info("Chromium 更新失败，尝试从原始仓库下载，速度较慢")
        del env["PLAYWRIGHT_DOWNLOAD_HOST"]
        subprocess.run([str(driver_executable), "install", "chromium"], env=env)
