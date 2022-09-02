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
