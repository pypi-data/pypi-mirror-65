#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simple read-only Thing 3 CLI."""

from __future__ import print_function

__author__ = "Alexander Willner"
__copyright__ = "2020 Alexander Willner"
__credits__ = ["Alexander Willner"]
__license__ = "Apache License 2.0"
__version__ = "2.1.1"
__maintainer__ = "Alexander Willner"
__email__ = "alex@willner.ws"
__status__ = "Development"

import sys
import argparse
import json
import csv
import webbrowser
from things3.things3 import Things3


class Things3CLI():
    """Simple read-only Thing 3 CLI."""

    print_json = False
    print_csv = False
    things3 = None

    def __init__(self, args, things):
        self.print_json = args.json
        self.print_csv = args.csv
        self.things3 = things

    def print_tasks(self, tasks):
        """Print a task."""
        if self.print_json:
            print(json.dumps(self.things3.convert_tasks_to_model(tasks)))
        elif self.print_csv:
            fieldnames = ['uuid', 'title', 'context', 'context_uuid', 'due',
                          'created', 'modified', 'started', 'stopped']
            writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.things3.convert_tasks_to_model(tasks))
        else:
            for task in tasks:
                title = task[self.things3.I_TITLE]
                context = task[self.things3.I_CONTEXT]
                print(' - ', title, ' (', context, ')')

    @classmethod
    def print_unimplemented(cls):
        """Show warning that method is not yet implemented."""
        print("not implemented yet (see things.sh for a more complete CLI)")


def get_parser():
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description='Simple read-only Thing 3 CLI.')

    subparsers = parser.add_subparsers(help='',
                                       metavar="command",
                                       required=True,
                                       dest="command")
    subparsers.add_parser('inbox',
                          help='Shows all inbox tasks')
    subparsers.add_parser('today',
                          help='Shows all todays tasks')
    subparsers.add_parser('upcoming',
                          help='Shows all upcoming tasks')
    subparsers.add_parser('next',
                          help='Shows all next tasks')
    subparsers.add_parser('someday',
                          help='Shows all someday tasks')
    subparsers.add_parser('completed',
                          help='Shows all completed tasks')
    subparsers.add_parser('cancelled',
                          help='Shows all cancelled tasks')
    subparsers.add_parser('trashed',
                          help='Shows all trashed tasks')
    subparsers.add_parser('feedback',
                          help='Give feedback')
    subparsers.add_parser('all',
                          help='Shows all tasks')
    subparsers.add_parser('csv',
                          help='Exports all tasks as CSV')
    subparsers.add_parser('due',
                          help='Shows all tasks with due dates')
    subparsers.add_parser('headings',
                          help='Shows all headings')
    subparsers.add_parser('hours',
                          help='Shows how many hours have been planned today')
    subparsers.add_parser('ical',
                          help='Shows all tasks ordered by due date as iCal')
    subparsers.add_parser('logbook',
                          help='Shows all tasks completed today')
    subparsers.add_parser('mostClosed',
                          help='Shows days on which most tasks were closed')
    subparsers.add_parser('mostCancelled',
                          help='Shows days on which most tasks were cancelled')
    subparsers.add_parser('mostTrashed',
                          help='Shows days on which most tasks were trashed')
    subparsers.add_parser('mostCreated',
                          help='Shows days on which most tasks were created')
    subparsers.add_parser('mostTasks',
                          help='Shows projects that have most tasks')
    subparsers.add_parser('mostCharacters',
                          help='Shows tasks that have most characters')
    subparsers.add_parser('nextish',
                          help='Shows all nextish tasks')
    subparsers.add_parser('old',
                          help='Shows all old tasks')
    subparsers.add_parser('projects',
                          help='Shows all projects')
    subparsers.add_parser('repeating',
                          help='Shows all repeating tasks')
    subparsers.add_parser('schedule',
                          help='Schedules an event using a template')
    subparsers.add_parser('search',
                          help='Searches for a specific task')
    subparsers.add_parser('stat',
                          help='Provides a number of statistics')
    subparsers.add_parser('statcsv',
                          help='Exports some statistics as CSV')
    subparsers.add_parser('subtasks',
                          help='Shows all subtasks')
    subparsers.add_parser('tag',
                          help='Shows all tasks with the waiting for tag')
    subparsers.add_parser('tags',
                          help='Shows all tags ordered by their usage')
    subparsers.add_parser('waiting',
                          help='Shows all tasks with the waiting for tag')

    parser.add_argument("-j", "--json",
                        action="store_true", default=False,
                        help="output as JSON", dest="json")

    parser.add_argument("-c", "--csv",
                        action="store_true", default=False,
                        help="output as CSV", dest="csv")

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    return parser


def main(args=None, things3=Things3()):
    """ Main entry point of the app """

    if args is None:
        main(get_parser().parse_args())
    else:
        things_cli = Things3CLI(args, things3)
        command = args.command

        if command in things3.functions:
            func = things3.functions[command]
            things_cli.print_tasks(func(things3))
        elif command == "csv":
            print("Deprecated: use --csv instead")
        elif command == "feedback":
            webbrowser.open(
                'https://github.com/AlexanderWillner/KanbanView/issues')
        else:
            Things3CLI.print_unimplemented()


if __name__ == "__main__":
    main(get_parser().parse_args())
