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
"""Validate the format of the Markdown documentation files."""

import dataclasses
import pathlib
import re

from typing import Any, Dict, List, Iterator, Optional, Union  # noqa: H301

import mistune  # type: ignore

from packaging import version as pversion

import trivval


@dataclasses.dataclass(frozen=True)
class MDHeadingParams:
    """A Markdown heading's parameters."""

    level: int


@dataclasses.dataclass(frozen=True)
class MDHeading:
    """A Markdown heading."""

    type: str
    text: str
    params: MDHeadingParams


@dataclasses.dataclass(frozen=True)
class MDListItemParams:
    """A Markdown list item's parameters."""

    depth: int


@dataclasses.dataclass(frozen=True)
class MDListItem:
    """A Markdown list item."""

    type: str
    children: List["MDObject"]
    params: MDListItemParams


@dataclasses.dataclass(frozen=True)
class MDListParams:
    """A Markdown list's parameters."""

    ordered: bool
    depth: int
    start: Any


@dataclasses.dataclass(frozen=True)
class MDList:
    """A Markdown list."""

    type: str
    children: List[MDListItem]
    params: MDListParams


@dataclasses.dataclass(frozen=True)
class MDBlockText:
    """A Markdown text string."""

    type: str
    text: str


MDObject = Union[MDBlockText, MDHeading, MDList]

RE_HEADING = re.compile(
    r""" ^
        (?P<version> \d+ \. \d+ \. \d+ ) \s+
        [(]
        (?:
            (?P<date> \d{4} - \d{2} - \d{2} )
            |
            (?P<not_yet> not [ ] yet )
        )
        [)]
    $ """,
    re.X,
)


def parse_object(obj: Dict[str, Any]) -> MDObject:
    """Parse an object returned by mistune into a dataclass."""

    def parse_block_text(obj: Dict[str, Any]) -> MDObject:
        """Parse a block of text."""
        assert obj["type"] == "block_text"
        return MDBlockText(type=str(obj["type"]), text=str(obj["text"]))

    def parse_heading(obj: Dict[str, Any]) -> MDObject:
        """Parse a heading."""
        assert obj["type"] == "heading"
        assert len(obj["params"]) == 1
        return MDHeading(
            type=str(obj["type"]),
            text=str(obj["text"]),
            params=MDHeadingParams(level=int(obj["params"][0])),
        )

    def parse_list_item(obj: Dict[str, Any]) -> MDListItem:
        """Parse a list item."""
        assert obj["type"] == "list_item"
        assert len(obj["params"]) == 1
        return MDListItem(
            type=str(obj["type"]),
            children=[parse_object(item) for item in obj["children"]],
            params=MDListItemParams(depth=int(obj["params"][0])),
        )

    def parse_list(obj: Dict[str, Any]) -> MDObject:
        """Parse a list."""
        assert obj["type"] == "list"
        assert len(obj["params"]) == 3
        return MDList(
            type=str(obj["type"]),
            children=[parse_list_item(item) for item in obj["children"]],
            params=MDListParams(
                ordered=bool(obj["params"][0]),
                depth=int(obj["params"][1]),
                start=obj["params"][2],
            ),
        )

    handlers = {
        "block_text": parse_block_text,
        "heading": parse_heading,
        "list": parse_list,
    }

    return handlers[obj["type"]](obj)


def test_changelog() -> None:
    """Test the format of the CHANGES.md file."""
    text = pathlib.Path("CHANGES.md").read_text(encoding="UTF-8")
    parser = mistune.BlockParser()
    state: Dict[str, Any] = {}
    raw: List[Dict[str, Any]] = parser.parse(text, state)
    res = [parse_object(item) for item in raw]

    def validate_list(items: MDList) -> None:
        """Recursively validate a list."""
        for listitem in items.children:
            assert isinstance(listitem, MDListItem)
            for item in listitem.children:
                if isinstance(item, MDBlockText):
                    continue

                assert isinstance(item, MDList)
                validate_list(item)

    def validate_entries(lst: Iterator[MDObject]) -> None:
        """Validate the changelog entries."""
        last_version: Optional[str] = None
        while True:
            try:
                heading = next(lst)
            except StopIteration:
                assert last_version is not None
                return
            assert isinstance(heading, MDHeading) and heading.params.level == 2

            data = RE_HEADING.match(heading.text)
            assert data, heading.text
            version = data.group("version")
            if last_version is None:
                assert version == trivval.VERSION
            else:
                assert pversion.Version(version) < pversion.Version(
                    last_version
                )
                assert data.group("date")
            last_version = version

            items = next(lst)
            assert isinstance(items, MDList)
            validate_list(items)

    assert isinstance(res[0], MDHeading) and res[0].params.level == 1
    validate_entries(iter(res[1:]))


def test_readme() -> None:
    """Just test that README.md may be parsed."""
    text = pathlib.Path("README.md").read_text(encoding="UTF-8")
    parser = mistune.BlockParser()
    parser.parse(text, {})
