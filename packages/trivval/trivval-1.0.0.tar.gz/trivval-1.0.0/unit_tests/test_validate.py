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
"""Simple tests for the validation routine."""

import json

from unittest import mock

from typing import Any, Dict, List, Optional, Tuple  # noqa: H301

try:
    import pytest  # type: ignore
except ImportError:
    from . import fake_pytest as pytest

import trivval

from . import data as tdata


def do_test(
    value: Dict[str, Any], schema: Dict[str, Any], backwards: bool = False
) -> None:
    """Run the tests for a specific value against a schema."""

    def test_extra_succeed() -> None:
        trivval.validate_dict(value, schema, 0)

    def test_extra_fail() -> None:
        with pytest.raises(trivval.ValidationError) as err:
            trivval.validate_dict(value, schema, 0)
        assert err.value.path[-1] != "a,more"
        assert err.value.err.startswith("extra")

    test_extra = test_extra_fail if backwards else test_extra_succeed

    trivval.validate_dict(value, schema, trivval.FLAG_ALLOW_EXTRA)
    test_extra()

    if "node" in value:
        add_to = value["node"]
        add_path = ["node"]
    else:
        add_key = next(iter(value["nodes"].keys()))
        add_to = value["nodes"][add_key]
        add_path = ["nodes", add_key]
    assert "more" not in add_to and "a" not in add_to
    add_to.update({"a": "lot", "more": "stuff"})
    trivval.validate_dict(value, schema, trivval.FLAG_ALLOW_EXTRA)
    with pytest.raises(trivval.ValidationError) as err:
        trivval.validate_dict(value, schema, 0)
    if not backwards:
        assert err.value.path == add_path + ["a,more"]
        assert err.value.err.startswith("extra")

    del add_to["a"]
    del add_to["more"]
    trivval.validate_dict(value, schema, trivval.FLAG_ALLOW_EXTRA)
    test_extra()

    missing = add_to.pop("hostname")

    with pytest.raises(trivval.ValidationError) as err:
        trivval.validate_dict(value, schema, trivval.FLAG_ALLOW_EXTRA)
    assert err.value.path == add_path + ["hostname"]
    assert err.value.err.startswith("missing")

    with pytest.raises(trivval.ValidationError) as err:
        trivval.validate_dict(value, schema, 0)
    if not backwards:
        assert err.value.path == add_path + ["hostname"]
        assert err.value.err.startswith("missing")

    add_to["hostname"] = missing
    trivval.validate_dict(value, schema, trivval.FLAG_ALLOW_EXTRA)
    test_extra()


def test_exact() -> None:
    """Test against the same version."""
    for version in sorted(tdata.VALUES.keys()):
        schema = tdata.SCHEMA[version]
        for value in tdata.VALUES[version]:
            do_test(value, schema)


def test_backwards() -> None:
    """Test against an earlier version."""
    for current_version in sorted(tdata.VALUES.keys()):
        for earlier_version in sorted(
            ver
            for ver in tdata.SCHEMA
            if ver[0] == current_version[0] and ver[1] < current_version[1]
        ):
            schema = tdata.SCHEMA[earlier_version]
            for value in tdata.VALUES[current_version]:
                do_test(value, schema, backwards=True)


def test_breaking() -> None:
    """Make sure validation fails after a breaking change."""
    for current_version in sorted(tdata.VALUES.keys()):
        for other_version in sorted(
            ver for ver in tdata.SCHEMA if ver[0] != current_version[0]
        ):
            schema = tdata.SCHEMA[other_version]
            for value in tdata.VALUES[current_version]:
                with pytest.raises(trivval.ValidationError):
                    trivval.validate_dict(value, schema, 0)


def test_schema() -> None:
    """Make sure validation succeeds with all schemas."""
    called: List[Optional[Tuple[Dict[str, Any], trivval.SchemaType, int]]] = [
        None
    ]

    def mock_validate_dict(
        value: Dict[str, Any], schema: trivval.SchemaType, flags: int
    ) -> None:
        called.append((value, schema, flags))

    for version, values in tdata.VALUES.items():
        v_format = {"version": {"major": version[0], "minor": version[1]}}
        for value in values:
            augmented = dict(value)
            assert "format" not in augmented
            augmented["format"] = v_format

            trivval.validate(augmented, tdata.SCHEMA, 0)

            assert augmented["format"] is v_format
            del augmented["format"]
            assert augmented == value

            augmented["format"] = v_format
            called = [None]

            with mock.patch("trivval.validate_dict", new=mock_validate_dict):
                trivval.validate(augmented, tdata.SCHEMA, 0)

            assert called[1] is not None
            assert called[1][0] == augmented
            called.pop(1)
            assert called == [
                None,
                (value, tdata.SCHEMA[version], 0),
            ]


def test_exact_json() -> None:
    """Test against the same version after a round trip through JSON."""
    for version in sorted(tdata.VALUES.keys()):
        schema = tdata.SCHEMA[version]
        for value in tdata.VALUES[version]:
            do_test(json.loads(json.dumps(value)), schema)
