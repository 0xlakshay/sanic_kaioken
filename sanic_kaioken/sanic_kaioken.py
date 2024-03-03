import logging
import os

from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install as enable_rich_traceback
from sanic_ext import Extension

from .logo import _GOKU_KAIOKEN


class SanicKaioken(Extension):
    name = "kaioken"

    def startup(self, bootstrap):
        if not self.app.debug:
            return

        console = Console()
        console.print(_GOKU_KAIOKEN, style="bold red")
        enable_rich_traceback()

        self._patch_logging()

    def _patch_logging(self):
        self._patch_exc_logging()
        self._patch_access_logging()
        self._patch_root_logging()

    def _patch_exc_logging(self):
        _show_locals = bool(os.environ.get("KAIOKEN"))

        error_logger = logging.getLogger("sanic.error")
        error_logger.handlers.clear()
        rich_handler = RichHandler(
            show_path=False,
            show_level=False,
            show_time=True,
            omit_repeated_times=False,
            rich_tracebacks=True,
            tracebacks_theme="one-dark",
            tracebacks_show_locals=_show_locals,
            locals_max_length=2,
        )
        formatter = logging.Formatter("%(message)s", datefmt="%Y/%m/%d %H:%M:%S")
        rich_handler.setFormatter(formatter)
        error_logger.addHandler(rich_handler)

    def _patch_access_logging(self):
        error_logger = logging.getLogger("sanic.access")
        error_logger.handlers.clear()
        rich_handler = RichHandler(
            rich_tracebacks=True,
            show_path=False,
            show_time=True,
            show_level=True,
            omit_repeated_times=False,
        )
        formatter = logging.Formatter("%(request)s %(message)s %(status)d %(byte)d")
        rich_handler.setFormatter(formatter)
        error_logger.addHandler(rich_handler)

    def _patch_root_logging(self):
        server_logger = logging.getLogger("sanic.server")
        server_logger.handlers.clear()
        rich_handler = RichHandler(
            rich_tracebacks=True,
            show_path=False,
            show_time=True,
            omit_repeated_times=False,
            markup=True,
        )
        server_logger.addHandler(rich_handler)

        root_logger = logging.getLogger("sanic.root")
        root_logger.handlers.clear()
        rich_handler = RichHandler(
            rich_tracebacks=True,
            show_path=False,
            show_time=True,
            omit_repeated_times=False,
            markup=True,
        )
        root_logger.addHandler(rich_handler)

    def label(self):
        if not self.app.debug:
            return "Disabled in Production"
