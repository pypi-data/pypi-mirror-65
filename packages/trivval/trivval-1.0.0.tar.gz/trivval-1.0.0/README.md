# Trivial validation - when the full power of the JSON Schema is not needed

This library provides a simplistic way to validate a dictionary against
something resembling a schema - a dictionary describing the desired data
structure by example.

The main entry point is the `validate()` function, but the various
`validate_*()` functions may be invoked directly with appropriate
arguments.

The schema used for validation is a dictionary (the top-level object must
be a dictionary). For the present, the keys may only be strings.
A special case of a dictionary with a single key `*` means any value for
a key will be accepted. Otherwise, all keys with names not starting with
a `?` character are mandatory, and any keys with names starting with
a `?` character are optional.

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
