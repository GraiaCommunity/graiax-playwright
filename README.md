<div align="center">

# GraiaX Playwright

_适用于 Graia Project 的 Playwright 管理器_

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![License](https://img.shields.io/github/license/GraiaCommunity/graiax-playwright)](https://github.com/GraiaCommunity/graiax-playwright/blob/master/LICENSE)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
[![PyPI](https://img.shields.io/pypi/v/graiax-playwright)](https://img.shields.io/pypi/v/graiax-playwright)

</div>

Graiax Playwright 使用 [launart](https://github.com/GraiaProject/launart) 作为启动管理器，
适用于 [Ariadne](https://github.com/GraiaProject/Ariadne) 及 [Avilla](https://github.com/GraiaProject/Avilla)。

通过 GraiaX Playwright 你可以轻松地在 Ariadne / Avilla 启动的时候同时启动一个
Playwright，并在其退出的时候自动关闭 Playwright。

> 需要注意的是，Playwright 将会在运行期间保持后台常驻，  
> 但由于并未开启任何页面，其内存占用量不是非常大（但也是可观的）。

## 安装

`pdm add graiax-playwright` 或 `poetry add graiax-playwright`。

> 我们强烈建议使用包管理器或虚拟环境

## 开始使用

以下教程以配合 Launart 使用为例。

### 机器人入口文件

```python
from creart import create
from launart import Launart
from graia.ariadne.app import Ariadne
from graiax.playwright import PlaywrightService

launart = create(Launart)
launart.add_component(PlaywrightService("chromium")) # 默认值为 chromium
launart.add_component(PlaywrightService("chromium"， user_data_dir="./browser_data"))  # 与上一行二选一，该方式使用 Persistent Context
...

launart.launch_blocking()
```

### 配合 Graia Saya 使用

```python
from creart import create
from launart import Launart
from graia.ariadne.util.saya import listen
from graiax.playwright import PlaywrightService


@listen(...)
async def function(app: Ariadne):
    launart = create(Launart)
    pw_service = launart.get_component(PlaywrightService)

    async with pw_service.page(  # 此 API 启用了自动上下文管理
        viewport={"width": 800, "height": 10},
        device_scale_factor=1.5,
    ) as page:
        await page.set_content("Hello World!")
        img = await page.screenshot(type="jpeg", quality=80, full_page=True, scale="device")
    ...
```

### 高级用法之一

上面配合 Saya 使用的例子展示了创建一个页面的例子，但该页面默认与其他页面互相**隔离**（例如 cookie
等），假如我们需要一个与其他页面**隔离**的新页面，那么我们可以使用
`page(use_global_context=False)` 在创建页面时使用一个新的上下文，如下所示：

> [!NOTE]  
> 该种用法中的新上下文，仍受到 Playwright 启动参数的影响
>
> 如果你传入了例如 `viewport` 之类的只有新创建上下文或者新页面才支持的参数时，则会忽略
> `use_global_context` 参数。此时若 `without_new_context`
> 为 `True`（默认行为），则将会直接使用浏览器实例创建新页面。
> 反之则会先创建新上下文再用新的上下文创建新页面，但是结束时新的页面和上下文都会被关闭。
>
> 更多信息详见：<https://playwright.dev/python/docs/browser-contexts>

```python
@listen(...)
async def function(app: Ariadne):
    launart = create(Launart)
    pw_service = launart.get_component(PlaywrightService)
    async with pw_service.page(use_global_context=False) as page:  # 此 API 启用了自动上下文管理
        await page.set_content("Hello World!")
        img = await page.screenshot(type="jpeg", quality=80, full_page=True, scale="device")
    ...
```

### 高级用法之二

上面配合 Saya 使用的例子展示了为**单个页面**设置 viewport 的功能，自 GraiaX Playwright `v0.3.1`
版本起，可以在创建 PlaywrightService 时为全局的 Browser Context 指定 viewport，然后在截图时使用全局
Browser Context 截图，如下所示：

**机器人入口文件：**

```python
launart.add_service(PlaywrightService("chromium"))
```

**Saya 模块中：**

```python
from graiax.playwright import PlaywrightService


@listen(...)
async def function(app: Ariadne):
    launart = create(Launart)
    pw_service = manager.get_component(PlaywrightService)
    async with pw_service.context(...) as context:  # 此 API 启用了自动上下文管理
        page = context.new_page()
        try:
            await page.set_content("Hello World!")
            img = await page.screenshot(type="jpeg", quality=80, full_page=True, scale='device')
        finally:
            page.stop()
    ...
```

### 高级用法之三

通过依赖注入来获取 `PlaywrightService`，前面的代码中获取 `PlaywrightService` 都需要通过 Launart
的 `get_component()` 方法，你也可以通过自定义一个 BCC 的 `Dispatcher` 来实现依赖注入。

编写一个 `Dispatcher`：

```python
from graia.broadcast.entities.dispatcher import BaseDispatcher
from graia.broadcast.interfaces.dispatcher import DispatcherInterface

class CustomDispatcher(BaseDispatcher):
    @classmethod
    async def catch(cls, interface: DispatcherInterface):
        with contextlib.suppress(TypeError):
            if generic_isinstance(interface.event, Service):
                manager = Launart.current()
                return manager.get_component(interface.annotation)
```

在启动 Launart 之前获取一个 BCC 实例并对其应用这个 `Dispatcher`：

```python
from creart import it
from graia.broadcast import Broadcast

bcc = it(Broadcast)
bcc.finale_dispatchers.append(RedbotDispatcher)

...

launart.launch_blocking() # 或者是 avilla.launch()
```

之后用起来就很简单了，你可以对比一下有什么不同：

```python
from graiax.playwright import PlaywrightService

@listen(...)
async def function(app: Ariadne, pw_service: PlaywrightService):
    async with pw_service.page(...) as page:
        ...
```

## 许可证

本项目使用 [`MIT`](./LICENSE) 许可证进行许可。
