#!/usr/bin/env python
import argparse
import re

from datetime import date

from sys import stderr
import shutil

from pathlib import Path

STARTS_WITH_TIMESTAMP = re.compile(r"(\d\d\d\d\-\d\d\-\d\d)_")


def with_current_date(filename: str, today: date = date.today()) -> str:
    nowstamp = today.strftime(r"%Y-%m-%d")
    m = re.match(STARTS_WITH_TIMESTAMP, filename)
    if not m:
        return f"{nowstamp}_{filename}"

    rest_of_filename = filename[m.span()[1] :]
    then = date.fromisoformat(m.group(1))
    if then == today:
        raise ValueError(f"{filename} already begins with today's date!")

    return f"{nowstamp}_{rest_of_filename}"


def copy_dated(inpath: Path, today: date = date.today()) -> None:
    if not inpath.exists():
        raise FileNotFoundError(f"{inpath} doesn't exist")

    dest = inpath.parent / with_current_date(inpath.name, today)
    if inpath.is_file():
        stderr.write(f"copy2({inpath}, {dest})")
        shutil.copy2(inpath, dest)
    elif inpath.is_dir():
        stderr.write(f"copytree({inpath}, {dest})")
        shutil.copytree(inpath, dest)
    else:
        raise ValueError(f"{inpath} is neither a file nor a directory")


def main():
    parser = argparse.ArgumentParser(
        description="Create a new copy of a file or directory with today's date as a prefix"
    )
    parser.add_argument("inpath", help="Input file/directory to dated")
    parsed = parser.parse_args()
    inpath = Path(parsed.inpath)
    return copy_dated(inpath)
