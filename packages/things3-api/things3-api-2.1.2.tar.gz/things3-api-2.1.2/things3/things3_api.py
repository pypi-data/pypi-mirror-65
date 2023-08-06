#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simple read-only Things 3 Web Serivce."""

from __future__ import print_function

__author__ = "Alexander Willner"
__copyright__ = "Copyright 2020 Alexander Willner"
__credits__ = ["Alexander Willner"]
__license__ = "Apache License 2.0"
__version__ = "2.1.2"
__maintainer__ = "Alexander Willner"
__email__ = "alex@willner.ws"
__status__ = "Development"

import sys
from os import getcwd
import json
from flask import Flask
from flask import Response
from things3.things3 import Things3

PORT = 8088
APP = Flask(__name__)
PATH = getcwd() + '/resources/'
THINGS3 = Things3()


@APP.route('/<url>')
def on_get(url):
    """Handles other GET requests"""
    filename = PATH + url
    content_type = 'application/json'
    if filename.endswith('css'):
        content_type = 'text/css'
    if filename.endswith('html'):
        content_type = 'text/html'
    if filename.endswith('js'):
        content_type = 'text/javascript'
    if filename.endswith('png'):
        content_type = 'image/png'
    if filename.endswith('jpg'):
        content_type = 'image/jpeg'
    if filename.endswith('ico'):
        content_type = 'image/x-ico'
    with open(filename, 'rb') as source:
        data = source.read()
    return Response(response=data, content_type=content_type)


@APP.route('/api/<command>')
def api(command):
    """Return database as JSON strings."""
    if command in THINGS3.functions:
        func = THINGS3.functions[command]
        data = json.dumps(THINGS3.convert_tasks_to_model(func(THINGS3)))
        return Response(response=data, content_type='application/json')

    data = json.dumps(THINGS3.convert_tasks_to_model(
        THINGS3.get_not_implemented()))
    return Response(response=data, content_type='application/json',
                    status=404)


def main():
    """"Main function."""
    print("Starting up...")
    try:
        APP.run(port=PORT)
    except KeyboardInterrupt:
        print("Shutting down...")
        sys.exit(0)


if __name__ == "__main__":
    main()
