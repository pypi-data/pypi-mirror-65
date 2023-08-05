# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""Module for reading from list files"""

from typing import List


def read_list(listpath: str) -> List[str]:
    """Reads the given list file and returns its contents"""
    with open(listpath, mode="r") as list_file:
        return [line.strip() for line in list_file.read().splitlines()]
