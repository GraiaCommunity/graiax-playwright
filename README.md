# (WIP) GraiaX Playwright

适用于 Graia Project 的 Playwright 管理器

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

...

Ariadne.launch_blocking()
```

### 配合 Graia Saya 使用

```python
from graia.ariadne.app import Ariadne
from graia.ariadne.util.saya import listen
from graiax.playwright import PlaywrightBrowser


@listen(...)
async def function(app: Ariadne):
    browser = app.launch_manager.get_interface(PlaywrightBrowser)
    # 此处的 Browser 与 playwright.async_api.Browser 无异.
    async with browser.page( # 此为启用了自动上下文管理的 API.
        context=True, # 新建 Browser Context, 默认为 False.
        viewport={"width": 800, "height": 10},
        device_scale_factor=1.5,
    ) as page:
        await page.set_content("Hello World!")
        img = await page.screenshot(type="jpeg", quality=80, full_page=True, scale="device")
    ...
```
