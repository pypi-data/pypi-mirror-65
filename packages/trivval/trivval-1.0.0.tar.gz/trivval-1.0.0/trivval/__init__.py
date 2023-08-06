# Copyright (c) 2020  Peter Pentchev <roam@ringlet.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
"""Trivial validation - when the full power of the JSON Schema is not needed.

This library provides a simplistic way to validate a dictionary against
something resembling a schema - a dictionary describing the desired data
structure by example.

The main entry point is the validate() function, but the various
validate_*() functions may be invoked directly with appropriate
arguments.

The schema used for validation is a dictionary (the top-level object must
be a dictionary). For the present, the keys may only be strings.
A special case of a dictionary with a single key "*" means any value for
a key will be accepted. Otherwise, all keys with names not starting with
a "?" character are mandatory, and any keys with names starting with
a "?" character are optional.

The dictionary values may be any of:
- a Python type signifying that the value must be an instance thereof
- a single-element list signifying that the value must be a list with
  all the elements validated by the same rules as a dictionary value
  (i.e. one of a Python type, a single-element list, a set, or
  a dictionary)
- a set signifying that the value must be exactly equal to one of
  the set elements, i.e. an enumeration of the allowed values
- a dictionary with the same semantics as described above

For example, the following schema:

    {
        "name": str,
        "id": int,
        "address": [str],
        "preferences": {
            "meal": set(("breakfast", "lunch", "brunch")),
            "colors": [{
                "name": str,
                "intensity": set(["dark", "light"])
            }]
        },
        "possessions": {
            "*": int
        }
    }

...may be used to validate the following dictionary:

    {
        "name": "A. N. Nymous",
        "id": 13,
        "address": [
            "42 Nowhere Circle",
            "Notown-at-all",
            "Unnamed territory"
        ],
        "preferences": {
            "meal": "brunch",
            "colors": [
                {"name": "blue", "intensity": "light"},
                {"name": "green", "intensity": "dark"}
            ]
        },
        "possessions": {
            "pencil": 4,
            "paper": 0
        }
    }
"""

from typing import Any, Dict, List, Tuple  # noqa: H301

VERSION = "1.0.0"

FEATURES_STRING = "trivval=" + VERSION

FLAG_ALLOW_EXTRA = 0x0001

SCHEMA_FORMAT = {"format": {"version": {"major": int, "minor": int}}}

SchemaType = Dict[Tuple[int, int], Dict[str, Any]]


class ValidationError(Exception):
    """Signal an error that occurred during the validation."""

    def __init__(self, path: List[str], err: str) -> None:
        self.path = path
        self.err = err
        suffix = "" if not self.path else ": " + "/".join(path)
        super(ValidationError, self).__init__(err + suffix)


def validate_single(key: str, item: Any, schema: Any, flags: int) -> None:
    """Validate a single dictionary value."""
    if isinstance(schema, type):
        if not isinstance(item, schema):
            raise ValidationError(
                [key],
                f"not a {schema.__name__}, {type(item).__name__} instead",
            )
    elif isinstance(schema, list):
        validate_list(key, item, schema, flags)
    elif isinstance(schema, set):
        if item not in schema:
            raise ValidationError([key], "not among the allowed values")
    else:
        assert isinstance(schema, dict)
        try:
            validate_dict(item, schema, flags)
        except ValidationError as err:
            raise ValidationError([key] + err.path, err.err)


def validate_list(
    key: str, value: List[Any], schema: List[Any], flags: int
) -> None:
    """Validate a list against a single-element schema."""
    if not isinstance(value, list):
        raise ValidationError(
            [key], f"not a list, {type(value).__name__} instead".__name__
        )

    assert len(schema) == 1
    for index, item in enumerate(value):
        validate_single(
            f"{key}[{index}]", item, schema[0], flags,
        )


def validate_dict(value: Any, schema: Dict[str, Any], flags: int) -> None:
    """Validate a dictionary against a schema."""
    if not isinstance(value, dict):
        raise ValidationError(
            [], f"not a dictionary, {type(value).__name__} instead"
        )

    if len(schema.keys()) == 1 and "*" in schema:
        valtype = schema["*"]
        for key in value.keys():
            validate_single(key, value[key], valtype, flags)
        return

    extra = set(value.keys())
    for key, valtype in schema.items():
        if key.startswith("?"):
            required = False
            key = key[1:]
        else:
            required = True

        if key not in value:
            if required:
                raise ValidationError([key], "missing")
            continue
        extra.remove(key)

        validate_single(key, value[key], valtype, flags)

    if extra and not flags & FLAG_ALLOW_EXTRA:
        raise ValidationError([",".join(sorted(extra))], "extra keys")


def validate(
    value: Dict[str, Any], schemas: SchemaType, flags: int = 0
) -> None:
    """Validate a dictionary against the appropriate schema."""
    try:
        validate_dict(value, SCHEMA_FORMAT, FLAG_ALLOW_EXTRA)
    except ValidationError:
        raise
    except Exception:
        raise ValidationError(
            ["format", "version"],
            "could not parse the version of the data format",
        )
    version = (
        value["format"]["version"]["major"],
        value["format"]["version"]["minor"],
    )
    stripped = {key: val for key, val in value.items() if key != "format"}

    same_major = sorted(
        ver
        for ver in schemas.keys()
        if ver[0] == version[0] and ver[1] <= version[1]
    )
    if not same_major:
        raise ValidationError(
            ["format", "version"], "unsupported format version"
        )

    validate_dict(stripped, schemas[same_major[-1]], flags)
