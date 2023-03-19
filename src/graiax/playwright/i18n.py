import contextlib
import gettext
import locale
import os
import sys
from pathlib import Path
from typing import Optional

WINDOWS = sys.platform.startswith("win") or os.name == "nt"


def _get_win_locale() -> Optional[str]:
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        lcid = kernel32.GetUserDefaultUILanguage()
        return locale.windows_locale.get(lcid)
    except ImportError:
        import winreg

        with contextlib.suppress(Exception):
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\International") as key:
                if lcid := winreg.QueryValueEx(key, "Locale")[0]:
                    return locale.windows_locale.get(int(lcid, 16))


def get_locale() -> Optional[str]:
    if WINDOWS:
        return _get_win_locale()

    return locale.getlocale(locale.LC_MESSAGES)[0]


t = gettext.translation(
    "graiax-playwright",
    localedir=Path(__file__).parent / "locale",
    languages=[lang] if (lang := get_locale()) else None,
    fallback=True,
)
N_ = t.gettext
