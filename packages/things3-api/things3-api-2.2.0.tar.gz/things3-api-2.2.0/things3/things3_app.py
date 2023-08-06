#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""KanbanView (app) for Things 3."""

from __future__ import print_function

# pylint: disable=duplicate-code
__author__ = "Alexander Willner"
__copyright__ = "Copyright 2020 Alexander Willner"
__credits__ = ["Luc Beaulieu", "Alexander Willner"]
__license__ = "Apache License 2.0"
__version__ = "2.2.0"
__maintainer__ = "Alexander Willner"
__email__ = "alex@willner.ws"
__status__ = "Development"

import sys
from os import system
from multiprocessing import Process
import webview  # type: ignore
import objc  # type: ignore # pylint: disable=unused-import # noqa F401
import pkg_resources.py2_warn  # type: ignore # pylint: disable=unused-import # noqa F401
import things3.things3_api as things3_api


class Things3App():
    """App wrapper for simple read-only API for Things 3."""

    database = None
    FILE = "kanban.html"

    def open_api(self):
        """Delay opening the browser."""
        print(f"Using database 2: {self.database}")
        things3_api.Things3API(database=self.database).main()

    def __init__(self, database=None):
        self.database = database

    def main(self):
        """Run the app."""
        # kill possible zombie processes; can't use psutil in py2app context
        system('lsof -nti:' + str(things3_api.Things3API.PORT) +
               ' | xargs kill -9')

        print(f"Using database 1: {self.database}")

        webview.create_window(
            title='KanbanView for Things 3',
            url=f'http://localhost:{things3_api.Things3API.PORT}/{self.FILE}',
            width=1024,
            min_size=(1024, 600),
            frameless=True)

        thread = Process(target=self.open_api)
        try:
            thread.start()
            webview.start()  # blocking
            thread.terminate()
            thread.join()
        except KeyboardInterrupt:
            print("Shutting down...")
            thread.terminate()
            thread.join()
            sys.exit(0)


if __name__ == "__main__":
    Things3App().main()
