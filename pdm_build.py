from babel.messages.frontend import CommandLineInterface


def pdm_build_update_files(context, files):
    CommandLineInterface().run(["pybabel", "compile", "-D", "graiax-playwright", "-d", "src/graiax/playwright/locale/"])
