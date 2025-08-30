import dated
import re
import pytest


@pytest.mark.parametrize(
    "s",
    [
        "1999-01-01_whatever.txt",
        "2025-99-99_this_is_fine.jpg",
        "0000-00-00_this_too.html",
    ],
)
def test_regex_match(s: str):
    assert re.match(dated.STARTS_WITH_TIMESTAMP, s)


@pytest.mark.parametrize(
    "s",
    [
        "1999-01-01close_but_no.cigar",
        " 2002-01-99_.tiffwhy_not.jpg",
    ],
)
def test_regex_nomatch(s: str):
    assert not re.match(dated.STARTS_WITH_TIMESTAMP, s)
