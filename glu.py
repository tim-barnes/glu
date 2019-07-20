#!/usr/bin/env python

import argparse
import fnmatch
import glob
import os
import subprocess
import sys

from typing import List, Callable


def walk(rootdir, filter: Callable[[str, List[str], List[str]], bool]):
    """
    Walk the directory tree
    """
    for dirname, subdirs, files in os.walk(rootdir):
        if filter(dirname, subdirs, files):
            yield dirname


def execute(dir: str, options: object):
    """
    Execute the command in the subdirectory
    """
    cwd = dir
    if options.subdir:
        cwd = os.path.join(cwd, options.subdir)

    subprocess.run(options.command, cwd=cwd)


def dir_filter(directory: str) -> Callable:
    def filter(dirname: str, subdirs: List[str], files: List[str]) -> bool:
        return directory in subdirs

    return filter


def glob_filter(pattern: str) -> Callable:
    def filter(dirname: str, subdirs: List[str], files: List[str]) -> bool:
        curdir = os.curdir
        os.chdir(dirname)
        matches = glob.glob(pattern)
        os.chdir(curdir)
        return len(matches)

    return filter


def make_filter(options):
    filters = [dir_filter(options.repo_match)]

    if options.subdir:
        filters.append(dir_filter(options.subdir))

    if options.glob:
        filters.append(glob_filter(options.glob))

    # Applies all the directory filters
    def filter(dirname: str, subdirs: List[str], files: List[str]) -> bool:
        pass_dir = True
        l = len(filters)
        i = 0
        while pass_dir and i < l:
            pass_dir = pass_dir and filters[i](dirname, subdirs, files)
            i = i + 1
        return pass_dir

    return filter


def get_options():
    """
    Returns the options passed from the arguments
    """

    parser = argparse.ArgumentParser(
        description="Run a command on multiple repositories."
    )
    parser.add_argument(
        "command",
        type=str,
        nargs=argparse.REMAINDER,
        help="The command to run.  Careful:  Environment variables are evaluated in this directory!",
    )
    parser.add_argument(
        "--repo_match",
        default=".git",
        help="Identifies a sub-directory containing a repo.",
    )
    parser.add_argument(
        "--subdir",
        type=str,
        help="Run the command in the named subdirectory of the repo.",
    )
    parser.add_argument(
        "--glob",
        type=str,
        help="Only run the command repos with files/directories matching the pattern.  Supports globbing.",
    )

    return parser.parse_args()


if __name__ == "__main__":

    options = get_options()
    print(options)
    for dir in walk(os.path.abspath(os.curdir), make_filter(options)):
        print(f"=================================\n{dir}\n")

        execute(dir, options)
