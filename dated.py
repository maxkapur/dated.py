#!/usr/bin/env python
"""Apply my filename convention to a given file or directory.

1. If the input file has a date, make a copy with today's date.
2. If the input file has today's date, insert `_a` and `_b` suffixes, or advance
   an existing letter suffix.
3. If the input file has no date, insert today's date and apply case 2.
"""

import argparse
import re
import shutil
from datetime import date as Date
from pathlib import Path
from string import ascii_lowercase as ASCII_LOWERCASE
from sys import stderr, stdout
from typing import NamedTuple


class FilenameParts(NamedTuple):
    """Parts of a conventional filename."""

    date: Date | None
    """The date embedded in the filename, if present."""

    letter: str | None
    """The version letter embedded in the filename, if present."""

    basename: str
    """The "rest" of the filename (without date or version letter)."""

    @classmethod
    def from_filename(cls, filename: str) -> "FilenameParts":
        """Construct a `FilenameParts` tuple from `filename`.

        Use regex to determine the filename structure and extract parts.
        """

        if m := re.match(r"(\d\d\d\d\-\d\d\-\d\d)_([a-z])_(.*$)", filename):
            # Filename with date and version letter
            return cls(Date.fromisoformat(m.group(1)), m.group(2), m.group(3))
        elif m := re.match(r"(\d\d\d\d\-\d\d\-\d\d)_(.*$)", filename):
            # Filename with date only
            return cls(Date.fromisoformat(m.group(1)), None, m.group(2))
        else:
            # Bare filename
            return cls(None, None, filename)


def new_filenames(filename: str, today: Date = Date.today()) -> tuple[str, str]:
    """Construct new conventional filenames for the given input.

    Return `old_dest_name` (to which the original file should be moved) and
    `new_dest_name` (to which the original should be copied) as a tuple.
    """
    todaystamp = today.strftime(r"%Y-%m-%d")

    match FilenameParts.from_filename(filename):
        case FilenameParts(date=None, letter=None, basename=basename):
            # Bare filename. We don't know the previous date, so just give the
            # old file today's date and add letter prefixes
            assert basename == filename
            return f"{todaystamp}_a_{filename}", f"{todaystamp}_b_{filename}"
        case FilenameParts(date=date, basename=basename) if date != today:
            # Date given but it isn't today: Original filename prevails
            # regardless of whether there was a letter
            return filename, f"{todaystamp}_{basename}"
        case FilenameParts(date=date, letter=None, basename=basename):
            # Date is today and no version letter: Create one (this is actually
            # the same as the first case)
            assert date == today
            return f"{todaystamp}_a_{basename}", f"{todaystamp}_b_{basename}"
        case FilenameParts(date=date, letter=letter, basename=basename):
            # Date is today and already have a version letter: Advance it
            assert date == today
            assert isinstance(letter, str)
            next_letter = chr(ord(letter) + 1)
            if next_letter not in ASCII_LOWERCASE:
                raise ValueError(f"No letter after {letter}")
            return filename, f"{todaystamp}_{next_letter}_{basename}"
        case parts:
            raise ValueError(f"Unable to parse {parts}")


def make_dated(inpath: Path, today: Date = Date.today()) -> list[str]:
    """Copy and rename `inpath` as necessary to apply the filename convention.

    Log what happened to `stderr`.
    """
    if not inpath.exists():
        raise FileNotFoundError(f"{inpath} doesn't exist")

    old_dest_name, new_dest_name = new_filenames(inpath.name, today)
    old_dest = inpath.parent / old_dest_name
    new_dest = inpath.parent / new_dest_name
    assert old_dest != new_dest
    assert not new_dest.exists()

    operations: list[str] = []
    if old_dest != inpath:
        # Move the original file if required, e.g. because we are adding a
        # datestamp or letter
        assert not old_dest.exists()
        op = f"move({inpath}, {old_dest})"
        operations.append(op)
        stderr.write(f"{op}\n")
        shutil.move(inpath, old_dest)

    if old_dest.is_file():
        op = f"copy2({inpath}, {new_dest})"
        operations.append(op)
        stderr.write(f"{op}\n")
        shutil.copy2(old_dest, new_dest)
    elif old_dest.is_dir():
        op = f"copytree({inpath}, {new_dest})"
        operations.append(op)
        stderr.write(f"{op}\n")
        shutil.copytree(old_dest, new_dest)
    else:
        raise ValueError(f"{inpath} is neither a file nor a directory")
    stdout.write(str(new_dest))

    return operations


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a new copy of a file or directory with today's date as a prefix"
    )
    parser.add_argument("inpath", help="Input file/directory to dated")
    parsed = parser.parse_args()
    inpath = Path(parsed.inpath)
    make_dated(inpath)


if __name__ == "__main__":
    main()
