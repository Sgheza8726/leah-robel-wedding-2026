"""
Logging setup and input guardrails for the AI Music Recommender.
"""
import logging
from pathlib import Path
from datetime import datetime

LOG_DIR = Path("logs")


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure file + console logging and return root logger."""
    LOG_DIR.mkdir(exist_ok=True)
    log_file = LOG_DIR / f"recommender_{datetime.now().strftime('%Y%m%d')}.log"

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger("music_recommender")


def validate_query(query: str) -> tuple:
    """
    Guardrail: reject empty, too-short, or too-long queries.
    Returns (is_valid: bool, error_message: str).
    """
    if not query or not query.strip():
        return False, "Query cannot be empty."
    if len(query.strip()) < 3:
        return False, "Query too short — please describe the music you want."
    if len(query) > 500:
        return False, "Query too long — please keep it under 500 characters."
    return True, ""


def log_recommendation_event(query: str, result: dict, logger: logging.Logger) -> None:
    """Log key metrics for a single recommendation request."""
    recs = result.get("recommendations", [])
    usage = result.get("usage", {})
    logger.info(
        "Recommendation | "
        "query_len=%d | num_results=%d | confidence=%.2f | "
        "top_song=%s | tokens_in=%d | tokens_out=%d",
        len(query),
        len(recs),
        result.get("confidence", 0.0),
        recs[0]["title"] if recs else "none",
        usage.get("input_tokens", 0),
        usage.get("output_tokens", 0),
    )
