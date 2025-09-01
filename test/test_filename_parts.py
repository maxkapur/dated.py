from datetime import date as Date

import pytest

import dated


@pytest.mark.parametrize(
    "filename",
    [
        "basic_case.txt",
        "just_fine.html",
        "little_ 0weird _but.ok",
    ],
)
def test_from_filename__bare(filename: str):
    style_parsed, date_parsed, letter_parsed, basename_parsed = (
        dated.FilenameParts.from_filename(filename)
    )
    assert style_parsed == dated.FilenameStyle.BARE
    assert date_parsed is None
    assert letter_parsed is None
    assert basename_parsed == filename


@pytest.mark.parametrize(
    "filename,date_expected,basename_expected",
    [
        ("2025-01-01_basic_case.txt", Date(2025, 1, 1), "basic_case.txt"),
        ("1999-12-31_just_fine.html", Date(1999, 12, 31), "just_fine.html"),
        ("0001-03-03_little_weird_but.ok", Date(1, 3, 3), "little_weird_but.ok"),
    ],
)
def test_from_filename__with_datestamp(
    filename: str, date_expected: Date, basename_expected: str
):
    style_parsed, date_parsed, letter_parsed, basename_parsed = (
        dated.FilenameParts.from_filename(filename)
    )
    assert style_parsed == dated.FilenameStyle.WITH_DATESTAMP
    assert date_parsed == date_expected
    assert letter_parsed is None
    assert basename_parsed == basename_expected


@pytest.mark.parametrize(
    "filename,date_expected,letter_expected,basename_expected",
    [
        ("2025-01-01_z_basic_case.txt", Date(2025, 1, 1), "z", "basic_case.txt"),
        ("1999-12-31_d_just_fine.html", Date(1999, 12, 31), "d", "just_fine.html"),
        ("0001-03-03_a_little_weird_but.ok", Date(1, 3, 3), "a", "little_weird_but.ok"),
    ],
)
def test_from_filename__with_datestamp_and_letter(
    filename: str, date_expected: Date, letter_expected: str, basename_expected: str
):
    style_parsed, date_parsed, letter_parsed, basename_parsed = (
        dated.FilenameParts.from_filename(filename)
    )
    assert style_parsed == dated.FilenameStyle.WITH_DATESTAMP_AND_LETTER
    assert date_parsed == date_expected
    assert letter_parsed == letter_expected
    assert basename_parsed == basename_expected
