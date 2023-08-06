#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module documentation goes here."""

import unittest
from things3 import things3_api


class Things3APICase(unittest.TestCase):
    """Class documentation goes here."""

    things3_api = things3_api.Things3API(database='tests/Things.sqlite3')

    def test_today(self):
        """Test Today."""

        result = self.things3_api.api("today").response
        self.assertEqual(1, len(result))

    def test_get_file(self):
        """Test get file."""

        result = self.things3_api.on_get(
            "/kanban.html").response[0].decode("utf-8")
        self.assertIn("footer", result)


if __name__ == '__main__':
    unittest.main()
