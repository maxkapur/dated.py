import dated
import pytest
from datetime import date


@pytest.mark.parametrize(
    "filename",
    [
        "basic_case.txt",
        "just_fine.html",
        "little_ 0weird _but.ok",
    ],
)
def test_from_filename__bare(filename: str):
    style_parsed, date_parsed, letter_parsed = dated.FilenameStyle.from_filename(
        filename
    )
    assert style_parsed == dated.FilenameStyle.BARE
    assert date_parsed is None
    assert letter_parsed is None


@pytest.mark.parametrize(
    "filename,date_expected",
    [
        ("2025-01-01_basic_case.txt", date(2025, 1, 1)),
        ("1999-12-31_just_fine.html", date(1999, 12, 31)),
        ("0001-03-03_little_weird_but.ok", date(1, 3, 3)),
    ],
)
def test_from_filename__with_datestamp(filename: str, date_expected: date):
    style_parsed, date_parsed, letter_parsed = dated.FilenameStyle.from_filename(
        filename
    )
    assert style_parsed == dated.FilenameStyle.WITH_DATESTAMP
    assert date_parsed == date_expected
    assert letter_parsed is None


@pytest.mark.parametrize(
    "filename,date_expected,letter_expected",
    [
        ("2025-01-01_z_basic_case.txt", date(2025, 1, 1), "z"),
        ("1999-12-31_d_just_fine.html", date(1999, 12, 31), "d"),
        ("0001-03-03_a_little_weird_but.ok", date(1, 3, 3), "a"),
    ],
)
def test_from_filename__with_datestamp_and_letter(
    filename: str, date_expected: date, letter_expected: str
):
    style_parsed, date_parsed, letter_parsed = dated.FilenameStyle.from_filename(
        filename
    )
    assert style_parsed == dated.FilenameStyle.WITH_DATESTAMP_AND_LETTER
    assert date_parsed == date_expected
    assert letter_parsed == letter_expected
