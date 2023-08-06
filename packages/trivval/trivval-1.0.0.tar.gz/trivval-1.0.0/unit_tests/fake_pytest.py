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
"""Simulate pytest.raises() in a very naive way."""

import contextlib
import re
import sys

from types import TracebackType
from typing import Iterator, Optional, Tuple, Type, Union  # noqa: H301


ExceptionTuple = Union[
    Tuple[Type[BaseException], BaseException, TracebackType],
    Tuple[None, None, None],
]


class ExceptionInfo:
    """Simulate the exception info returned by pytest.raises()."""

    type: Optional[Type[BaseException]]
    typename: Optional[str]
    value: Optional[BaseException]
    tb: Optional[TracebackType]  # pylint: disable=invalid-name

    def __init__(self, einfo: Optional[ExceptionTuple] = None) -> None:
        self.type = None
        self.typename = None
        self.value = None
        self.tb = None  # pylint: disable=invalid-name

        if einfo is None:
            einfo = sys.exc_info()
        self.init_from(einfo)

    def init_from(self, einfo: ExceptionTuple) -> None:
        """Initialize the current object's members.

        This is needed because the exception is caught much later than
        the object is returned by raises().
        """
        self.type, self.value, self.tb = einfo  # pylint: disable=invalid-name
        self.typename = self.type.__name__ if self.type is not None else None
        # We do not simulate the traceback member

    def errisinstance(self, exc: Type[Exception]) -> bool:
        """Check whether the exception is an instance of that class."""
        return isinstance(self.value, exc)

    def match(self, regexp: str) -> None:
        """Check whether the exception message matches that pattern."""
        assert re.match(regexp, str(self.value))

    def __repr__(self) -> str:
        return (
            f"ExceptionInfo(type={repr(self.type)}, "
            f"value={repr(self.value)}, "
            f"tb={repr(self.tb)})"
        )

    def __str__(self) -> str:
        return repr(self)


@contextlib.contextmanager
def raises(etype: Type[Exception]) -> Iterator[ExceptionInfo]:
    """Make sure that the specified exception will be raised."""
    einfo = ExceptionInfo()
    caught = False
    try:
        yield einfo
    except etype:
        einfo.init_from(sys.exc_info())
        caught = True
    finally:
        if not caught:
            raise Exception(f"{etype} not thrown")
