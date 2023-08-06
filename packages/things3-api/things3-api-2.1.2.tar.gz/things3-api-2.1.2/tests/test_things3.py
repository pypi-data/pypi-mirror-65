#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module documentation goes here."""

import unittest
from things3.things3 import Things3


class Things3Case(unittest.TestCase):
    """Class documentation goes here."""

    things3 = Things3(database='tests/Things.sqlite3')

    def test_today(self):
        """Test Today."""
        tasks = self.things3.get_today()
        self.assertEqual(1, len(tasks), "foo")

    def test_inbox(self):
        """Test Inbox."""
        tasks = self.things3.get_inbox()
        self.assertEqual(1, len(tasks))

    def test_next(self):
        """Test Next."""
        tasks = self.things3.get_anytime()
        self.assertEqual(4, len(tasks))

    def test_backlog(self):
        """Test Backlog."""
        tasks = self.things3.get_someday()
        self.assertEqual(1, len(tasks))

    def test_upcoming(self):
        """Test Upcoming."""
        tasks = self.things3.get_upcoming()
        self.assertEqual(3, len(tasks))

    def test_waiting(self):
        """Test Waiting."""
        tasks = self.things3.get_waiting()
        self.assertEqual(1, len(tasks))

    def test_mit(self):
        """Test MIT."""
        tasks = self.things3.get_mit()
        self.assertEqual(0, len(tasks))

    def test_completed(self):
        """Test completed tasks."""
        tasks = self.things3.get_completed()
        self.assertEqual(1, len(tasks))

    def test_cancelled(self):
        """Test cancelled tasks."""
        tasks = self.things3.get_cancelled()
        self.assertEqual(1, len(tasks))

    def test_trashed(self):
        """Test trashed tasks."""
        tasks = self.things3.get_trashed()
        self.assertEqual(3, len(tasks))

    def test_all(self):
        """Test all tasks."""
        tasks = self.things3.get_all()
        self.assertEqual(13, len(tasks))

    def test_due(self):
        """Test due tasks."""
        tasks = self.things3.get_due()
        self.assertEqual(1, len(tasks))

    def test_anonymize(self):
        """Test anonymized tasks."""
        tasks = self.things3.get_today()
        self.assertIn("Today Todo", tasks.pop())
        self.things3.anonymize = True
        tasks = self.things3.get_today()
        self.assertNotIn("Today Todo", tasks.pop())


if __name__ == '__main__':
    unittest.main()
