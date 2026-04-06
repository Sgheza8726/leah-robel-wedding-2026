"""
Evaluation harness for the AI Music Recommender.

Runs predefined test cases, checks genre/mood/energy expectations,
and reports pass/fail counts with average confidence scores.
"""
import logging
from typing import List, Optional

from src.ai_recommender import get_ai_recommendations

logger = logging.getLogger(__name__)

# ── Test suite ────────────────────────────────────────────────────────────────

TEST_CASES = [
    {
        "id": "TC01",
        "description": "Happy pop road trip",
        "query": "I want upbeat happy pop songs for a road trip",
        "expected_genre": "pop",
        "expected_mood": "happy",
        "min_energy": 0.60,
    },
    {
        "id": "TC02",
        "description": "Lofi study music",
        "query": "Something chill to study to, like lofi beats",
        "expected_genre": "lofi",
        "expected_mood": "chill",
        "max_energy": 0.55,
    },
    {
        "id": "TC03",
        "description": "Intense rock workout",
        "query": "Heavy intense rock music for working out hard",
        "expected_genre": "rock",
        "expected_mood": "intense",
        "min_energy": 0.75,
    },
    {
        "id": "TC04",
        "description": "Relaxing jazz café",
        "query": "Relaxing jazz for a coffee shop afternoon",
        "expected_genre": "jazz",
        "expected_mood": "relaxed",
        "max_energy": 0.50,
    },
    {
        "id": "TC05",
        "description": "Dark moody electronic",
        "query": "Dark moody electronic music for late night drives",
        "expected_mood": "moody",
        "min_energy": 0.50,
    },
    {
        "id": "TC06",
        "description": "Nostalgic acoustic folk",
        "query": "Nostalgic folk songs that feel warm and acoustic",
        "expected_genre": "folk",
        "expected_mood": "nostalgic",
        "max_energy": 0.55,
    },
]


# ── Evaluation logic ──────────────────────────────────────────────────────────

def _check_result(result: dict, tc: dict) -> dict:
    """Return {passed: bool, checks: list[str]} for one test case."""
    recs = result.get("recommendations", [])
    checks: List[str] = []
    passed = True

    if not recs:
        return {"passed": False, "checks": ["✗ No recommendations returned"]}

    top = recs[0]

    if "expected_genre" in tc:
        found = any(r["genre"].lower() == tc["expected_genre"].lower() for r in recs[:3])
        checks.append(
            f"{'✓' if found else '✗'} Genre '{tc['expected_genre']}' in top 3"
        )
        if not found:
            passed = False

    if "expected_mood" in tc:
        found = any(r["mood"].lower() == tc["expected_mood"].lower() for r in recs[:3])
        checks.append(
            f"{'✓' if found else '✗'} Mood '{tc['expected_mood']}' in top 3"
        )
        if not found:
            passed = False

    if "min_energy" in tc:
        e = float(top["energy"])
        ok = e >= tc["min_energy"]
        checks.append(f"{'✓' if ok else '✗'} Top energy {e:.2f} >= {tc['min_energy']}")
        if not ok:
            passed = False

    if "max_energy" in tc:
        e = float(top["energy"])
        ok = e <= tc["max_energy"]
        checks.append(f"{'✓' if ok else '✗'} Top energy {e:.2f} <= {tc['max_energy']}")
        if not ok:
            passed = False

    conf = result.get("confidence", 0.0)
    checks.append(f"  Confidence: {conf:.2f}")

    return {"passed": passed, "checks": checks}


# ── Public runner ─────────────────────────────────────────────────────────────

def run_evaluation(test_cases: Optional[List[dict]] = None) -> dict:
    """
    Run the evaluation harness and print a summary.

    Returns:
        passed        – number of tests that passed
        total         – total tests run
        pass_rate     – fraction passed
        avg_confidence – mean confidence across all results
        details       – list of per-test result dicts
    """
    cases = test_cases or TEST_CASES
    details = []
    passed_count = 0
    total_confidence = 0.0

    print("\n" + "=" * 60)
    print("  AI MUSIC RECOMMENDER — EVALUATION HARNESS")
    print("=" * 60)

    for tc in cases:
        print(f"\n[{tc['id']}] {tc['description']}")
        print(f"  Query: \"{tc['query']}\"")

        try:
            result = get_ai_recommendations(tc["query"])
            eval_out = _check_result(result, tc)

            status = "PASS" if eval_out["passed"] else "FAIL"
            if eval_out["passed"]:
                passed_count += 1
            total_confidence += result.get("confidence", 0.0)

            print(f"  Status: {status}")
            for line in eval_out["checks"]:
                print(f"    {line}")

            recs = result.get("recommendations", [])
            if recs:
                t = recs[0]
                print(
                    f"  Top: {t['title']} by {t['artist']}  "
                    f"(score {t['score']:.2f})"
                )

            details.append({"test_case": tc, "result": result, "evaluation": eval_out})

        except Exception as exc:
            logger.exception("Error running test case %s", tc["id"])
            print(f"  ERROR: {exc}")
            details.append(
                {
                    "test_case": tc,
                    "result": None,
                    "evaluation": {"passed": False, "checks": [f"Exception: {exc}"]},
                }
            )

    avg_confidence = total_confidence / len(cases) if cases else 0.0

    print(f"\n{'=' * 60}")
    print(f"  SUMMARY: {passed_count}/{len(cases)} tests passed")
    print(f"  Average confidence: {avg_confidence:.2f}")
    print("=" * 60 + "\n")

    return {
        "passed": passed_count,
        "total": len(cases),
        "pass_rate": passed_count / len(cases) if cases else 0.0,
        "avg_confidence": avg_confidence,
        "details": details,
    }
