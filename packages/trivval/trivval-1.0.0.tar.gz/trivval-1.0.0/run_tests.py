#!/usr/bin/python3
"""Simulate pytest -s -vv: discover and run some tests."""

from __future__ import print_function

import argparse
import importlib
import pathlib
import sys
import traceback


def main() -> None:
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

    print(f"Looking for tests in {testdir}")
    collected = {}
    for fname in (path.with_suffix("") for path in testdir.rglob("test_*.py")):
        mod = importlib.import_module(".".join(fname.parts))
        for test in (name for name in dir(mod) if name.startswith("test_")):
            key = f"{fname}::{test}"
            collected[key] = getattr(mod, test)

    print(f"Collected {len(collected)} items\n")
    failed = []
    for name in sorted(collected):
        print(f"{name}... ", end="")
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
