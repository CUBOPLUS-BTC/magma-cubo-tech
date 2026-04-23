"""
Internationalization (i18n) module for Magma Bitcoin app.
Provides translation, locale detection, and locale-aware number/date formatting.

Uses threading.local to store per-request locale so route handlers
can simply call ``t("key")`` without passing locale explicitly.
"""

import threading

from .translator import Translator, LocaleManager
from .formatter import NumberFormatter, DateFormatter, MessageFormatter

__all__ = [
    "Translator",
    "LocaleManager",
    "NumberFormatter",
    "DateFormatter",
    "MessageFormatter",
    "t",
    "set_request_locale",
    "get_request_locale",
    "set_default_locale",
    "get_translator",
]

# Module-level singleton translator
_translator = Translator(default_locale="en")

# Thread-local storage for per-request locale
_local = threading.local()


def set_request_locale(code: str) -> None:
    """Set the locale for the current request/thread."""
    _local.locale = code


def get_request_locale() -> str:
    """Get the locale for the current request/thread (default 'en')."""
    return getattr(_local, "locale", "en")


def t(key: str, locale: str = None, **kwargs) -> str:
    """Shorthand global translate function.

    If ``locale`` is not provided, uses the per-request locale
    set via ``set_request_locale()``.
    """
    if locale is None:
        locale = get_request_locale()
    return _translator.translate(key, locale=locale, **kwargs)


def set_default_locale(code: str) -> None:
    """Set the module-level default locale."""
    _translator.set_locale(code)


def get_translator() -> Translator:
    """Return the module-level Translator singleton."""
    return _translator
