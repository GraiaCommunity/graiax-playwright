<div align="center">

# GraiaX Playwright

*适用于 Graia Project 的 Playwright 管理器*

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![License](https://img.shields.io/github/license/GraiaCommunity/graiax-playwright)](https://github.com/GraiaCommunity/graiax-playwright/blob/master/LICENSE)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
[![PyPI](https://img.shields.io/pypi/v/graiax-playwright)](https://img.shields.io/pypi/v/graiax-playwright)

</div>

Graiax Playwright 使用 [launart](https://github.com/GraiaProject/launart) 作为启动管理器，
适用于 [Ariadne](https://github.com/GraiaProject/Ariadne) 及 [Avilla](https://github.com/GraiaProject/Avilla)。

以 Ariadne 为例，通过 GraiaX Playwright 你可以轻松地在 Ariadne 启动的时候同时启动一个
Playwright，并在其退出的时候自动关闭 Playwright。

> 需要注意的是，Playwright 将会在运行期间保持后台常驻，  
> 但由于并未开启任何页面，其内存占用量不是非常大（但也是可观的）。

## 安装

`pdm add graiax-playwright` 或 `poetry add graiax-playwright`。

> 我们强烈建议使用包管理器或虚拟环境

## 开始使用

以下示例以 Ariadne 为例。

### 机器人入口文件

```python
from graia.ariadne.app import Ariadne
from graiax.playwright import PlaywrightService

app = Ariadne(...)
app.launch_manager.add_service(PlaywrightService("chromium")) # 默认值为 chromium
app.launch_manager.add_service(PlaywrightService(user_data_dir="./browser_data"))  # 与上一行二选一，使用 Persistent Context
...

Ariadne.launch_blocking()
```

### 配合 Graia Saya 使用

```python
from graia.ariadne.app import Ariadne
from graia.ariadne.util.saya import listen
from graiax.playwright import PlaywrightBrowser

# 此处代码为没有使用 Persistent Context 的示例
# 若使用 Persistent Context 请使用 `context = app.launch_manager.get_interface(PlaywrightContext)`
# 该方法获得的对象与 playwright.async_api.BrowserContext 兼容


@listen(...)
async def function(app: Ariadne):
    browser = app.launch_manager.get_interface(PlaywrightBrowser)
    # 此处的 browser 之用法与 playwright.async_api.Browser 无异，但要注意的是下方代码的返回值为 False。
    # `isinstance(browser, playwright.async_api.Browser)`
    async with browser.page(  # 此 API 启用了自动上下文管理
        viewport={"width": 800, "height": 10},
        device_scale_factor=1.5,
    ) as page:
        await page.set_content("Hello World!")
        img = await page.screenshot(type="jpeg", quality=80, full_page=True, scale="device")
    ...
```

## 许可证

本项目使用 [`MIT`](./LICENSE) 许可证进行许可。
