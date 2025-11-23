# This module contains simple validation helpers
# used to check incoming user queries and internal data.

from typing import Any


def validate_query(query: str) -> bool:
    # This function validates that the user query is non-empty and not just whitespace.
    return isinstance(query, str) and query.strip() != ""


def is_non_empty_list(value: Any) -> bool:
    # This function checks if a given value is a non-empty list.
    return isinstance(value, list) and len(value) > 0
