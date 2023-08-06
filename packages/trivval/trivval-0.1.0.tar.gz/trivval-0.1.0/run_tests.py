#!/usr/bin/python
"""Simulate pytest -s -vv: discover and run some tests."""

from __future__ import print_function

import argparse
import importlib
import sys
import traceback

# Make sure we really import the correct module
# (we do not want to end up with the old "pathlib" backport to Python 2.x)
#
if sys.version_info[0] < 3:
    import pathlib2 as pathlib  # pylint: disable=import-error
else:
    import pathlib  # pylint: disable=import-error


def main():
    # type: () -> None
    """Discover tests, run them."""
    parser = argparse.ArgumentParser(
        prog="run_tests", description="Try to Python unit tests"
    )
    parser.add_argument(
        "testdir",
        nargs="?",
        type=str,
        default="unit_tests",
        help="Path to the unit tests directory",
    )
    args = parser.parse_args()

    testdir = pathlib.Path(args.testdir)
    if not testdir.parts or testdir.parts[0] in ("/", ".."):
        sys.exit("Only a subdirectory supported for the present")

    print("Looking for tests in {testdir}".format(testdir=testdir))
    collected = {}
    for fname in (path.with_suffix("") for path in testdir.rglob("test_*.py")):
        mod = importlib.import_module(".".join(fname.parts))
        for test in (name for name in dir(mod) if name.startswith("test_")):
            key = "{fname}::{test}".format(fname=fname, test=test)
            collected[key] = getattr(mod, test)

    print("Collected {count} items\n".format(count=len(collected)))
    failed = []
    for name in sorted(collected):
        print("{name}... ".format(name=name), end="")
        try:
            collected[name]()
            print("ok")
        except Exception:  # pylint: disable=broad-except
            print("FAILED")
            failed.append(sys.exc_info())

    if failed:
        print(repr(failed))
        for item in failed:
            print("\n")
            traceback.print_exception(*item)
            print("\n")
        sys.exit(1)
    print("Fine!")


if __name__ == "__main__":
    main()
