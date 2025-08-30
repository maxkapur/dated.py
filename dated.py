#!/usr/bin/env python
import argparse
import re

from datetime import date

from sys import stderr
import shutil

STARTS_WITH_TIMESTAMP = re.compile(r"(\d\d\d\d\-\d\d\-\d\d)_")


def with_current_date(filename: str, now: date = date.today()) -> str:
    nowstamp = now.strftime(r"%Y-%m-%d")
    m = re.match(STARTS_WITH_TIMESTAMP, filename)
    if not m:
        return f"{nowstamp}_{filename}"

    rest_of_filename = filename[m.span()[1] :]
    then = date.fromisoformat(m.group(1))
    if then == now:
        raise ValueError(f"{filename} already begins with today's date!")

    return f"{nowstamp}_{rest_of_filename}"
