#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module documentation goes here."""

import unittest
import io
import sys
import things3.things3_cli as things3_cli
from things3.things3 import Things3


class Things3CLICase(unittest.TestCase):
    """Class documentation goes here."""

    things3 = Things3(database='tests/Things.sqlite3')

    def test_today(self):
        """Test Today."""
        args = things3_cli.get_parser().parse_args(['today'])
        new_out = io.StringIO()
        old_out = sys.stdout
        try:
            sys.stdout = new_out
            things3_cli.main(args, self.things3)
        finally:
            sys.stdout = old_out
        self.assertIn("Today Todo", new_out.getvalue())


if __name__ == '__main__':
    unittest.main()
