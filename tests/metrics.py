# This module defines basic evaluation metrics used in the test harness.
# It measures keyword coverage and response length as simple quality proxies.

from typing import List


def keyword_coverage(response: str, expected_keywords: List[str]) -> float:
    # This function computes the fraction of expected keywords
    # that appear (case-insensitive) in the response text.
    if not expected_keywords:
        return 1.0
    response_lower = response.lower()
    hits = 0
    for kw in expected_keywords:
        if kw.lower() in response_lower:
            hits += 1
    return round(hits / len(expected_keywords), 2)


def response_length_tokens(response: str) -> int:
    # This function returns the number of whitespace-separated tokens in the response.
    return len(response.split())
