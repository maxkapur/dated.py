import uuid
from datetime import date as Date
from pathlib import Path

import pytest

import dated

NOW = Date.fromisoformat("2025-01-01")


@pytest.mark.parametrize(
    "filename,old_dest,new_dest",
    [
        # Bare filename
        ("some_file.txt", "2025-01-01_a_some_file.txt", "2025-01-01_b_some_file.txt"),
        ("fear.jpg", "2025-01-01_a_fear.jpg", "2025-01-01_b_fear.jpg"),
        ("fine.png", "2025-01-01_a_fine.png", "2025-01-01_b_fine.png"),
        # Filename with date only
        ## original date != today: no letter
        ("1999-01-02_file.docx", "1999-01-02_file.docx", "2025-01-01_file.docx"),
        ("2999-01-02_future.py", "2999-01-02_future.py", "2025-01-01_future.py"),
        ## original date == today: add a letter (and don't trip up on "a")
        ("2025-01-01_a.jpg", "2025-01-01_a_a.jpg", "2025-01-01_b_a.jpg"),
        # Filename with date and letter
        ## original date != today: no letter
        ("1999-01-02_c_file.docx", "1999-01-02_c_file.docx", "2025-01-01_file.docx"),
        ("2999-01-02_b_future.py", "2999-01-02_b_future.py", "2025-01-01_future.py"),
        ## original date == today: advance to next letter
        ("2025-01-01_a_img.jpg", "2025-01-01_a_img.jpg", "2025-01-01_b_img.jpg"),
    ],
)
def test_make_dated__file(filename: str, old_dest: str, new_dest: str, tmp_path: Path):
    # Put infile in a subdirectory to ensure correct handling
    infile = tmp_path / str(uuid.uuid4()) / filename
    infile.parent.mkdir(parents=True, exist_ok=True)
    infile.touch()

    dated.make_dated(infile, NOW)

    expected = [infile.parent / old_dest, infile.parent / new_dest]
    expected.sort()
    found = sorted(infile.parent.glob("**/*"))
    assert expected == found


@pytest.mark.parametrize(
    "filename,old_dest,new_dest",
    [
        # Bare filename
        ("some_file", "2025-01-01_a_some_file", "2025-01-01_b_some_file"),
        ("fear", "2025-01-01_a_fear", "2025-01-01_b_fear"),
        ("fine", "2025-01-01_a_fine", "2025-01-01_b_fine"),
        # Filename with date only
        ## original date != today: no letter
        ("1999-01-02_file", "1999-01-02_file", "2025-01-01_file"),
        ("2999-01-02_future", "2999-01-02_future", "2025-01-01_future"),
        ## original date == today: add a letter (and don't trip up on "a")
        ("2025-01-01_a", "2025-01-01_a_a", "2025-01-01_b_a"),
        # Filename with date and letter
        ## original date != today: no letter
        ("1999-01-02_c_file", "1999-01-02_c_file", "2025-01-01_file"),
        ("2999-01-02_b_future", "2999-01-02_b_future", "2025-01-01_future"),
        ## original date == today: advance to next letter
        ("2025-01-01_a_img", "2025-01-01_a_img", "2025-01-01_b_img"),
    ],
)
def test_make_dated__dir(filename: str, old_dest: str, new_dest: str, tmp_path: Path):
    # Put infile in a subdirectory to ensure correct handling
    infile = tmp_path / str(uuid.uuid4()) / filename

    infile.mkdir(parents=True)
    (infile / "a.txt").touch()
    (infile / "b.txt").touch()

    dated.make_dated(infile, NOW)

    expected = [
        infile.parent / old_dest,
        infile.parent / old_dest / "a.txt",
        infile.parent / old_dest / "b.txt",
        infile.parent / new_dest,
        infile.parent / new_dest / "a.txt",
        infile.parent / new_dest / "b.txt",
    ]
    expected.sort()
    found = sorted(infile.parent.glob("**/*"))
    assert expected == found
