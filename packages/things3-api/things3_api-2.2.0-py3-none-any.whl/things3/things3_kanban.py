#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""KanbanView (static) for Things 3."""

from __future__ import print_function

__author__ = "Alexander Willner"
__copyright__ = "Copyright 2020 Alexander Willner"
__credits__ = ["Luc Beaulieu", "Alexander Willner"]
__license__ = "Apache License 2.0"
__version__ = "2.2.0"
__maintainer__ = "Alexander Willner"
__email__ = "alex@willner.ws"
__status__ = "Development"

import codecs
from os import getcwd
from things3.things3 import Things3

# Basic variables
FILE_HTML = getcwd() + '/kanban-static.html'
THINGS3 = Things3()
TARGET = codecs.open(FILE_HTML, 'w', 'utf-8')


def write_html_column(cssclass, file, header, rows):
    """Create a column in the output."""

    file.write("<div class='column'><div class=''>" +
               "<h2 class='" + cssclass + "'>" + header +
               "<span class='size'>" + str(len(rows)) +
               "</span></h2>")

    for row in rows:
        task_uuid = str(row[THINGS3.I_UUID]) \
            if row[THINGS3.I_UUID] is not None else ''
        task_title = str(row[THINGS3.I_TITLE]) \
            if row[THINGS3.I_TITLE] is not None else ''
        context_title = str(row[THINGS3.I_CONTEXT]) \
            if row[THINGS3.I_CONTEXT] is not None else ''
        context_uuid = str(row[THINGS3.I_CONTEXT_UUID]) \
            if row[THINGS3.I_CONTEXT_UUID] is not None else ''
        deadline = str(row[THINGS3.I_DUE]) \
            if row[THINGS3.I_DUE] is not None else ''

        task_link = '<a href="things:///show?id=' + task_uuid + '">' + \
            task_title + '</a>' if task_uuid != '' else task_title
        context_link = '<a href="things:///show?id=' + context_uuid + '">' + \
            context_title + '</a>' if context_uuid != '' else context_title
        css_class = 'hasProject' if context_title != '' else 'hasNoProject'
        css_class = 'hasDeadline' if deadline != '' else css_class

        file.write('<div class="box">' + task_link +
                   '<div class="deadline">' + deadline + '</div>' +
                   '<div class="area ' + css_class + '">' + context_link +
                   '</div>' +
                   '</div>')
    file.write("</div></div>")


def write_html_header(file):
    """Write HTML header."""

    message = """
        <!DOCTYPE html>
        <html>
        <head>
          <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
          <link rel="stylesheet" href="./resources/kanban.css">
          <title>KanbanView for Things 3</title>
        </head>

        <body>
          <header>
            <a href="https://kanbanview.app" title="visit product page">
              <img class="logo bright" src="./resources/logo.png"
                alt="logo for bright theme">
              <img class="logo dark" src="./resources/logo-dark.png"
                alt="logo for dark theme" style="display: none;">
            </a>
          </header>
          <article class='some-page-wrapper'>
            <div class='row'>
        """
    file.write(message)


def write_html_footer(file):
    """Write HTML footer."""

    message = """
            </div>
          </article>
        <footer class="footer"><br />
        Copyright &copy;2020 Alexander Willner
        </footer></body></html>"""
    file.write(message)


def write_html_columns(file):
    """Write HTML columns."""

    write_html_column("color1", file, "Backlog", THINGS3.get_someday())
    write_html_column("color5", file, "Upcoming", THINGS3.get_upcoming())
    write_html_column("color3", file, "Waiting", THINGS3.get_waiting())
    write_html_column("color4", file, "Inbox", THINGS3.get_inbox())
    write_html_column("color2", file, "MIT", THINGS3.get_mit())
    write_html_column("color6", file, "Today", THINGS3.get_today())
    write_html_column("color7", file, "Next", THINGS3.get_anytime())


def main(output):
    """Convert Things 3 database to Kanban HTML view."""

    with output as file:
        write_html_header(file)
        write_html_columns(file)
        write_html_footer(file)


if __name__ == "__main__":
    main(TARGET)
