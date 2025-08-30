import dated
import re
import pytest
from datetime import date

NOW = date.fromisoformat("2025-01-01")


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("1999-01-01_whatever.txt", "2025-01-01_whatever.txt"),
        ("2025-12-31_this_is_fine.jpg", "2025-01-01_this_is_fine.jpg"),
        ("0001-01-01_this_too.html", "2025-01-01_this_too.html"),
    ],
)
def test_filename_with_date__ok(filename: str, expected: str):
    assert expected == dated.with_current_date(filename, NOW)


@pytest.mark.parametrize(
    "filename",
    [
        "2025-01-01_whatever.txt",
        "2025-01-01_mistake.docx",
    ],
)
def test_filename_with_date__same_date_error(filename: str):
    with pytest.raises(ValueError, match=".*already begins with"):
        dated.with_current_date(filename, NOW)


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("whatever.txt", "2025-01-01_whatever.txt"),
        ("25_this_is_fine.jpg", "2025-01-01_25_this_is_fine.jpg"),
        ("this_too.html", "2025-01-01_this_too.html"),
    ],
)
def test_filename_without_date(filename: str, expected: str):
    assert expected == dated.with_current_date(filename, NOW)
