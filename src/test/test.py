import asyncio
from os import remove

from graiax.playwright import PlaywrightBrowser, PlaywrightContext, PlaywrightService
from launart import Launart, Launchable


class Test(Launchable):
    id = "test"

    @property
    def required(self):
        return {PlaywrightBrowser, PlaywrightContext}

    @property
    def stages(self):
        return {"blocking"}

    async def launch(self, manager: Launart):
        async with self.stage("blocking"):
            browser = manager.get_interface(PlaywrightBrowser)
                await page.set_content("Hello World!")
                await page.screenshot(
                    full_page=True,
                    type="jpeg",
                    path="graiax-playwright_test.jpg",
                )
            await asyncio.sleep(10)
            remove("graiax-playwright_test.jpg")
            context = manager.get_interface(PlaywrightContext)
            async with context.page() as page:
                await page.set_content("Hello World!")
                await page.screenshot(
                    full_page=True,
                    type="jpeg",
                    path="graiax-playwright_test.jpg",
                )
            await asyncio.sleep(10)
            remove("graiax-playwright_test.jpg")


loop = asyncio.new_event_loop()
launart = Launart()

launart.add_service(PlaywrightService("chromium"))
launart.add_launchable(Test())

launart.launch_blocking()

launart.status.exiting = True
if launart.task_group is not None:
    launart.task_group.stop = True
    task = launart.task_group.blocking_task
    if task and not task.done():
        task.cancel()
