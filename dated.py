#!/usr/bin/env python
import argparse
import re

from datetime import date as Date

import enum
from sys import stderr
import shutil

from typing import NamedTuple

from pathlib import Path

from string import ascii_lowercase as ASCII_LOWERCASE


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
    parts = FilenameParts.from_filename(filename)
    nowstamp = today.strftime(r"%Y-%m-%d")
    if parts.style == FilenameStyle.BARE:
        # We don't know the previous date, so just give the old file today's
        # date and add letter prefixes
        return f"{nowstamp}_a_{filename}", f"{nowstamp}_b_{filename}"

    assert parts.date is not None
    thenstamp = parts.date.strftime(r"%Y-%m-%d")

    if parts.style == FilenameStyle.WITH_DATESTAMP:
        if parts.date == today:
            assert thenstamp == nowstamp
            return f"{thenstamp}_a_{parts.basename}", f"{thenstamp}_b_{parts.basename}"
        else:
            return f"{thenstamp}_{parts.basename}", f"{nowstamp}_{parts.basename}"

    if parts.style == FilenameStyle.WITH_DATESTAMP_AND_LETTER:
        assert parts.letter is not None
        if parts.date == today:
            assert thenstamp == nowstamp
            new_letter = chr(ord(parts.letter) + 1)
            assert new_letter in ASCII_LOWERCASE  # TODO: helpful error
            return filename, f"{thenstamp}_{new_letter}_{parts.basename}"
        else:
            return filename, f"{nowstamp}_{parts.basename}"

    raise ValueError(f"Unknown filename style {parts.style}")


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
