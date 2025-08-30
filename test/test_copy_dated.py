from pathlib import Path
import dated
import pytest
from datetime import date

NOW = date.fromisoformat("2025-01-01")


@pytest.mark.parametrize(
    "filename,expected",
    [
        # With date
        ("1999-01-01_whatever.txt", "2025-01-01_whatever.txt"),
        ("2025-12-31_this_is_fine.jpg", "2025-01-01_this_is_fine.jpg"),
        ("0001-01-01_this_too.html", "2025-01-01_this_too.html"),
        # Without date
        ("whatever.txt", "2025-01-01_whatever.txt"),
        ("25_this_is_fine.jpg", "2025-01-01_25_this_is_fine.jpg"),
        ("this_too.html", "2025-01-01_this_too.html"),
    ],
)
def test_infile_file(filename: str, expected: str, tmp_path: Path):
    infile = tmp_path / filename
    infile.touch()
    dated.copy_dated(infile, NOW)
    assert (tmp_path / expected).is_file(), list(tmp_path.glob("**/*"))


@pytest.mark.parametrize(
    "filename,expected",
    [
        # With date
        ("1999-01-01_whatever", "2025-01-01_whatever"),
        ("2025-12-31_this_is_fine", "2025-01-01_this_is_fine"),
        ("0001-01-01_this_too", "2025-01-01_this_too"),
        # Without date
        ("whatever", "2025-01-01_whatever"),
        ("25_this_is_fine", "2025-01-01_25_this_is_fine"),
        ("this_too", "2025-01-01_this_too"),
    ],
)
def test_infile_dir(filename: str, expected: str, tmp_path: Path):
    infile = tmp_path / filename
    infile.mkdir(parents=True)
    (infile / "a.txt").touch()
    (infile / "b.txt").touch()

    dated.copy_dated(infile, NOW)
    assert (tmp_path / expected).is_dir(), list(tmp_path.glob("**/*"))
    assert (tmp_path / expected / "a.txt").is_file(), list(tmp_path.glob("**/*"))
    assert (tmp_path / expected / "b.txt").is_file(), list(tmp_path.glob("**/*"))
