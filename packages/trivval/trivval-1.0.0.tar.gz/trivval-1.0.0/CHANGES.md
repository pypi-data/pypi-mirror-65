# Changelog for trivval, the trivial data structure validation library

## 1.0.0 (2020-04-14)

- Only support Python 3.6 or later:
  - drop the Python 2.x unit tests and mypy check
  - unconditionally import typing and pathlib
  - drop the "equivalent types" support only needed for
    the Python 2.x `unicode`/`str` weirdness
  - no longer inherit from `object`
  - use f-strings for errors and diagnostic messages
  - use Python 3.x's `unittest.mock` and drop `fake_mock`
- Use the `mistune` library to validate the Markdown files.

## 0.1.0 (2020-04-14)

- First public release.
