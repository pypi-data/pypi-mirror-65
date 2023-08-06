#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""KanbanView (app) for Things 3."""

from __future__ import print_function

# pylint: disable=duplicate-code
__author__ = "Luc Beaulieu and Alexander Willner"
__copyright__ = "Copyright 2018 Luc Beaulieu / 2020 Alexander Willner"
__credits__ = ["Luc Beaulieu", "Alexander Willner"]
__license__ = "Apache License 2.0"
__version__ = "2.1.2"
__maintainer__ = "Alexander Willner"
__email__ = "alex@willner.ws"
__status__ = "Development"

import sys
from os import system
from threading import Thread
import webview  # type: ignore
import objc  # type: ignore # pylint: disable=unused-import # noqa F401
import pkg_resources.py2_warn  # type: ignore # pylint: disable=unused-import # noqa F401
import things3.things3_api as things3_api


def open_api():
    """Delay opening the browser."""
    things3_api.APP.run(port=things3_api.PORT)


FILE = "kanban.html"
THREAD = Thread(target=open_api)


def main():
    """Run the app."""
    # kill possible zombie processes; can't use psutil in py2app context
    system('lsof -nti:' + str(things3_api.PORT) +
           ' | xargs kill -9')

    webview.create_window(
        title='KanbanView for Things 3',
        url=f'http://localhost:{things3_api.PORT}/{FILE}',
        width=1024,
        min_size=(1024, 600),
        frameless=True)

    try:
        THREAD.start()
        webview.start()
    except KeyboardInterrupt:
        print("Shutting down...")
        THREAD.join()
        sys.exit(0)


if __name__ == "__main__":
    main()
