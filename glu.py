#!/usr/bin/env python

import argparse
import os
import subprocess
import sys

from functools import reduce
from typing import List, Callable


def walk(filter: Callable[[List[str], List[str]], bool]):
    """
    Walk the directory tree
    """
    for dirname, subdirs, files in os.walk('.'):
        if filter(subdirs, files):
            yield dirname

def execute(dir: str, options: object):
    """
    Execute the command in the subdirectory
    """
    cwd = dir
    if options.subdir:
        cwd = os.path.join(cwd, options.subdir)

    subprocess.run(options.command, cwd=cwd)


def include_filter(options: object) -> Callable:
    def filter(subdirs: List[str], files: List[str]) -> bool:
        return options.include_dir in subdirs
    return filter


def src_filter(options: object) -> Callable:
    def filter(subdirs: List[str], files: List[str]) -> bool:
        return options.subdir in subdirs

    return filter


def filter_chain(*args):
    return filter


def make_filter(options):
    filters = [include_filter(options)]

    if options.subdir:
        filters.append(src_filter(options))

    # Applies all the directory filters
    def filter(subdirs: List[str], files: List[str]) -> bool:
        return reduce(lambda a, b: a and b(subdirs, files), filters, True)
    return filter


def get_options():
    """
    Returns the options passed from the arguments
    """

    parser = argparse.ArgumentParser(description="Run a command on multiple sub-directories.")
    parser.add_argument("command",
                        type=str,
                        nargs=argparse.REMAINDER,
                        help='The command to run.  Careful:  Environment variables are evaluated in this directory!')
    parser.add_argument("--include_dir",
                        default=".git",
                        help="Identifies the sub-directory to run the command in.")
    parser.add_argument("--subdir",
                        type=str,
                        help="Run the command in the named subdirectory.")

    return parser.parse_args()


if __name__ == "__main__":

    options = get_options()
    print(options)
    for dir in walk(make_filter(options)):
        print(f"=================================\n{dir}")

        execute(dir, options)