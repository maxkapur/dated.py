#!/usr/bin/env python
import argparse
import re

from datetime import date as Date

import enum
from sys import stderr
import shutil

from typing import NamedTuple

from pathlib import Path


class FilenameStyle(enum.Enum):
    BARE = enum.auto()
    WITH_DATESTAMP = enum.auto()
    WITH_DATESTAMP_AND_LETTER = enum.auto()


class FilenameParts(NamedTuple):
    style: FilenameStyle
    date: Date | None
    letter: str | None
    basename: str

    @classmethod
    def from_filename(cls, filename: str):
        if m := re.match(r"(\d\d\d\d\-\d\d\-\d\d)_([a-z])_(.*$)", filename):
            return cls(
                FilenameStyle.WITH_DATESTAMP_AND_LETTER,
                Date.fromisoformat(m.group(1)),
                m.group(2),
                m.group(3),
            )
        elif m := re.match(r"(\d\d\d\d\-\d\d\-\d\d)_(.*$)", filename):
            return cls(
                FilenameStyle.WITH_DATESTAMP,
                Date.fromisoformat(m.group(1)),
                None,
                m.group(2),
            )
        else:
            return cls(
                FilenameStyle.BARE,
                None,
                None,
                filename,
            )


def new_filenames(filename: str, today: Date = Date.today()) -> tuple[str, str]:
    old_filename_style, old_date, old_letter = FilenameStyle.from_filename(filename)
    nowstamp = today.strftime(r"%Y-%m-%d")
    if old_filename_style == FilenameStyle.BARE:
        # We don't know the previous date, so just give the old file today's
        # date and an "a" prefix
        return f"{nowstamp}_a_{filename}", f"{nowstamp}_b_{filename}"

    assert old_date is not None
    thenstamp = old_date.strftime(r"%Y-%m-%d")

    if old_filename_style == FilenameStyle.WITH_DATESTAMP:
        assert old_date is not None
        if old_date == today:
            assert thenstamp == nowstamp
            return f"{thenstamp}_a_"

    m = re.match(STARTS_WITH_TIMESTAMP, filename)
    if not m:
        return f"{nowstamp}_{filename}"

    rest_of_filename = filename[m.span()[1] :]
    then = date.fromisoformat(m.group(1))
    if then == today:
        raise ValueError(f"{filename} already begins with today's date!")

    return f"{nowstamp}_{rest_of_filename}"


def copy_dated(inpath: Path, today: Date = Date.today()) -> None:
    if not inpath.exists():
        raise FileNotFoundError(f"{inpath} doesn't exist")

    dest = inpath.parent / with_current_date(inpath.name, today)
    if inpath.is_file():
        stderr.write(f"copy2({inpath}, {dest})\n")
        shutil.copy2(inpath, dest)
    elif inpath.is_dir():
        stderr.write(f"copytree({inpath}, {dest})\n")
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
