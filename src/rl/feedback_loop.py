# This module implements a very simple feedback loop,
# which evaluates the quality of a generated response and analysis.

from typing import Dict
from utils.logger import log_info


def evaluate_response_quality(analysis: Dict[str, object], response: str) -> float:
    # This function computes a simple quality score based on:
    # - number of claims found
    # - length of response (not too short)
    claims = analysis.get("claims", [])
    num_claims = len(claims) if isinstance(claims, list) else 0
    response_length = len(response.split())

    score = 0.0
    if num_claims > 0:
        score += 0.5
    if response_length > 50:
        score += 0.3
    if response_length > 100:
        score += 0.2

    return round(min(score, 1.0), 2)


def should_retry(quality_score: float, threshold: float = 0.6) -> bool:
    # This function decides if the system should retry based on the quality score.
    retry = quality_score < threshold
    log_info(
        f"FeedbackLoop: quality_score={quality_score}, "
        f"threshold={threshold}, should_retry={retry}"
    )
    return retry
