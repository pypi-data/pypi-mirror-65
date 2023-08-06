#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module documentation goes here."""

import unittest
import io
import sys
import things3.things3_cli as things3_cli


class Things3CLICase(unittest.TestCase):
    """Class documentation goes here."""

    things3_cli = things3_cli.Things3CLI(database='tests/Things.sqlite3')

    def test_today(self):
        """Test Today."""
        args = self.things3_cli.get_parser().parse_args(['today'])
        new_out = io.StringIO()
        old_out = sys.stdout
        try:
            sys.stdout = new_out
            self.things3_cli.main(args)
        finally:
            sys.stdout = old_out
        self.assertIn("Today Todo", new_out.getvalue())


if __name__ == '__main__':
    unittest.main()
