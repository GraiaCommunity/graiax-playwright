from babel.messages.frontend import CommandLineInterface


def build(src: str, dst: str):
    CommandLineInterface().run(["pybabel", "compile", "-D", "graiax-playwright", "-d", "src/graiax/playwright/locale/"])


if __name__ == "__main__":
    build("", "")
