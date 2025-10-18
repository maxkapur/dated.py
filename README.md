# dated.py

Apply my [obnoxious](https://maxkapur.com/2024/04/26/iso-dates-filenames.html)
datestamping conventions to create a working copy of a file or directory.

1. If the input file already has a datestamp, the new copy has the datestamp
   updated to today:

   ```shell
   $ touch 2025-01-01_already_dated.txt
   $ dated 2025-01-01_already_dated.txt
   copy2(2025-01-01_already_dated.txt, 2025-08-31_already_dated.txt)
   2025-08-31_already_dated.txt
   $ ls
   2025-01-01_already_dated.txt  2025-08-31_already_dated.txt
   ```

2. If the input file's datestamp is already today, then insert suffixes `_a`
   (original) and `_b` (copy) after the date:

   ```shell
   $ touch (date -Idate)_already_dated_today.txt
   $ dated (date -Idate)_already_dated_today.txt
   move(2025-09-01_already_dated_today.txt, 2025-09-01_a_already_dated_today.txt)
   copy2(2025-09-01_already_dated_today.txt, 2025-09-01_b_already_dated_today.txt)
   2025-09-01_b_already_dated_today.txt
   $ ls
   2025-09-01_a_already_dated_today.txt  2025-09-01_b_already_dated_today.txt
   ```

3. If the input file doesn't have a datestamp, assume it was created today and
   apply case 2:

   ```shell
   $ touch undated.txt
   $ dated undated.txt
   move(undated.txt, 2025-09-01_a_undated.txt)
   copy2(undated.txt, 2025-09-01_b_undated.txt)
   2025-09-01_b_undated.txt
   $ ls
   2025-09-01_a_undated.txt  2025-09-01_b_undated.txt
   ```

The logging output (e.g. `move(undated.txt, 2025-09-01_a_undated.txt)`) is
written to `stderr` and can be suppressed by redirection:

```shell
dated undated.txt 2>/dev/null
```

The new filename (e.g. `2025-09-01_b_already_dated_today.txt`) is written to
`stdout` so you can do stuff like this:

```shell
micro $(dated notes.txt)
```

## Installation

```shell
pipx install 'git+https://github.com/maxkapur/dated.py'
```

## Usage

```shell
dated path/to/some_file.docx  # Date is prepended to "some_file.docx"
dated path/to/some_directory  # Date is prepended to "some_directory"
```

## Development

```shell
python -m venv venv
source ./venv/bin/activate  # Or appropriate command for your shell
pip install --upgrade pip
pip install --editable .[dev]
```
