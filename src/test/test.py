import asyncio
from os import remove

from creart import create
from launart import Launart, Service

from graiax.playwright import PlaywrightBrowser, PlaywrightContext, PlaywrightService


class Test(Service):
    id = "test"

    @property
    def required(self):
        return {"web.render/graiax.playwright"}

    @property
    def stages(self):
        return {"blocking"}

    async def launch(self, manager: Launart):
        async with self.stage("blocking"):
            browser = manager.get_interface(PlaywrightBrowser)
            async with browser.page(viewport={"width": 300, "height": 100}) as page:
                await page.set_content("Hello World!")
                await page.screenshot(
                    full_page=True,
                    type="jpeg",
                    path="graiax-playwright_test1.jpg",
                )
            browser = manager.get_interface(PlaywrightBrowser)
            async with browser.page(new_context=True) as page:
                await page.set_content("Hello World!")
                await page.screenshot(
                    full_page=True,
                    type="jpeg",
                    path="graiax-playwright_test2.jpg",
                )
            context = manager.get_interface(PlaywrightContext)
            async with context.page() as page:
                await page.set_content("Hello World!")
                await page.screenshot(
                    full_page=True,
                    type="jpeg",
                    path="graiax-playwright_test3.jpg",
                )
            await asyncio.sleep(10)
            remove("graiax-playwright_test1.jpg")
            remove("graiax-playwright_test2.jpg")
            remove("graiax-playwright_test3.jpg")


launart = create(Launart)

launart.add_component(PlaywrightService("chromium", viewport={"width": 800, "height": 10}, device_scale_factor=1.5))
launart.add_component(Test())

launart.launch_blocking()
