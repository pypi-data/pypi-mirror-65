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
"""Data samples for the validation library tests."""


SCHEMA_1_0 = {
    "node": {
        "hostname": str,
        "flavor": set(("desktop", "laptop", "server")),
        "services": {
            "launcher": {"timestamp": int},
            "server": {"timestamp": int, "instances": int},
        },
    },
    "users": {"*": {"first_name": str, "last_name": str, "id": int}},
    "tags": [str],
}

SCHEMA_1_1 = {
    "node": {
        "hostname": str,
        "flavor": set(("desktop", "laptop", "server")),
        "services": {
            "launcher": {"timestamp": int},
            "server": {"timestamp": int, "instances": int},
        },
    },
    "users": {
        "*": {"first_name": str, "last_name": str, "id": int, "?nickname": str}
    },
    "tags": [str],
}

SCHEMA_2_0 = {
    "nodes": {
        "*": {
            "hostname": str,
            "flavor": set(("laptop", "server")),
            "services": {
                "launcher": {"timestamp": int},
                "server": {"timestamp": int, "instances": int},
            },
        },
    },
    "users": {
        "*": {
            "first_name": str,
            "last_name": str,
            "id": int,
            "?nickname": str,
        }
    },
    "tags": [str],
}

SCHEMA = {
    (1, 0): SCHEMA_1_0,
    (1, 1): SCHEMA_1_1,
    (2, 0): SCHEMA_2_0,
}

VALUES_1_0 = [
    {
        "node": {
            "hostname": "straylight",
            "flavor": "laptop",
            "services": {
                "launcher": {"timestamp": 1000},
                "server": {"timestamp": 1001, "instances": 4},
            },
        },
        "users": {
            "jrl": {
                "first_name": "J. Random",
                "last_name": "Lucretius",
                "id": 42,
            },
            "centre": {"first_name": "Aza", "last_name": "Thoth", "id": 616},
        },
        "tags": ["foo", "bar"],
    },
    {
        "node": {
            "hostname": "feylight",
            "flavor": "desktop",
            "services": {
                "launcher": {"timestamp": 3000},
                "server": {"timestamp": 3005, "instances": 4},
            },
        },
        "users": {
            "guest": {
                "first_name": "Mister",
                "last_name": "Apollinax",
                "id": 201,
            },
        },
        "tags": [],
    },
]

VALUES_1_1 = [
    {
        "node": {
            "hostname": "straylight",
            "flavor": "server",
            "services": {
                "launcher": {"timestamp": 1000},
                "server": {"timestamp": 1001, "instances": 4},
            },
        },
        "users": {
            "jrl": {
                "first_name": "J. Random",
                "last_name": "Lucretius",
                "id": 42,
                "nickname": "jay",
            },
            "centre": {"first_name": "Aza", "last_name": "Thoth", "id": 616},
        },
        "tags": ["foo", "bar"],
    },
    {
        "node": {
            "hostname": "feylight",
            "flavor": "desktop",
            "services": {
                "launcher": {"timestamp": 3000},
                "server": {"timestamp": 3005, "instances": 4},
            },
        },
        "users": {
            "guest": {
                "first_name": "Mister",
                "last_name": "Apollinax",
                "id": 201,
                "nickname": "paul",
            },
        },
        "tags": [],
    },
]

VALUES_2_0 = [
    {
        "nodes": {
            "laptop": {
                "hostname": "straylight",
                "flavor": "laptop",
                "services": {
                    "launcher": {"timestamp": 1000},
                    "server": {"timestamp": 1001, "instances": 4},
                },
            },
        },
        "users": {
            "jrl": {
                "first_name": "J. Random",
                "last_name": "Lucretius",
                "id": 42,
                "nickname": "jay",
            },
            "centre": {"first_name": "Aza", "last_name": "Thoth", "id": 616},
        },
        "tags": ["foo", "bar"],
    },
    {
        "nodes": {
            "local": {
                "hostname": "feylight",
                "flavor": "server",
                "services": {
                    "launcher": {"timestamp": 3000},
                    "server": {"timestamp": 3005, "instances": 4},
                },
            },
        },
        "users": {
            "guest": {
                "first_name": "Mister",
                "last_name": "Apollinax",
                "id": 201,
                "nickname": "paul",
            },
        },
        "tags": [],
    },
]

VALUES = {
    (1, 0): VALUES_1_0,
    (1, 1): VALUES_1_1,
    (2, 0): VALUES_2_0,
}
