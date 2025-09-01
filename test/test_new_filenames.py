import dated
import pytest
from datetime import date

NOW = date.fromisoformat("2025-01-01")


@pytest.mark.parametrize(
    "filename,old_dest,new_dest",
    [
        ("some_file.txt", "2025-01-01_a_some_file.txt", "2025-01-01_b_some_file.txt"),
        ("fear.jpg", "2025-01-01_a_fear.jpg", "2025-01-01_b_fear.jpg"),
        ("fine.png", "2025-01-01_a_fine.png", "2025-01-01_b_fine.png"),
    ],
)
def test_new_filenames__bare(filename: str, old_dest: str, new_dest: str):
    assert (old_dest, new_dest) == dated.new_filenames(filename, NOW)


@pytest.mark.parametrize(
    "filename,old_dest,new_dest",
    [
        # original date != today: no letter
        ("1999-01-02_file.docx", "1999-01-02_file.docx", "2025-01-01_file.docx"),
        ("2999-01-02_future.py", "2999-01-02_future.py", "2025-01-01_future.py"),
        # original date == today: add a letter (and don't trip up on "a")
        ("2025-01-01_a.jpg", "2025-01-01_a_a.jpg", "2025-01-01_b_a.jpg"),
    ],
)
def test_new_filenames__with_date(filename: str, old_dest: str, new_dest: str):
    assert (old_dest, new_dest) == dated.new_filenames(filename, NOW)


@pytest.mark.parametrize(
    "filename,old_dest,new_dest",
    [
        # original date != today: no letter
        ("1999-01-02_c_file.docx", "1999-01-02_c_file.docx", "2025-01-01_file.docx"),
        ("2999-01-02_b_future.py", "2999-01-02_b_future.py", "2025-01-01_future.py"),
        # original date == today: advance to next letter
        ("2025-01-01_a_img.jpg", "2025-01-01_a_img.jpg", "2025-01-01_b_img.jpg"),
    ],
)
def test_new_filenames__with_date_and_letter(
    filename: str, old_dest: str, new_dest: str
):
    assert (old_dest, new_dest) == dated.new_filenames(filename, NOW)
