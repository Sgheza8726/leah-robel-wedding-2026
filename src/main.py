"""
AI Music Recommender — Command-line interface.

Usage:
  python -m src.main                → interactive AI-powered mode (default)
  python -m src.main --classic      → original profile-based mode
  python -m src.main --evaluate     → run the evaluation harness
  python -m src.main --verbose      → enable DEBUG logging
"""
import argparse
import logging

from src.recommender import load_songs, recommend_songs
from src.logger import setup_logging, validate_query, log_recommendation_event


# ── Classic mode (original Phase 3 implementation) ───────────────────────────

def run_classic_mode() -> None:
    """Run the original deterministic profile-based recommender."""
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    profiles = {
        "High-Energy Pop":    {"genre": "pop",  "mood": "happy",   "energy": 0.85, "valence": 0.85},
        "Chill Lofi":         {"genre": "lofi", "mood": "chill",   "energy": 0.38, "valence": 0.58},
        "Deep Intense Rock":  {"genre": "rock", "mood": "intense", "energy": 0.90, "valence": 0.45},
    }

    for name, prefs in profiles.items():
        recs = recommend_songs(prefs, songs, k=5)
        print(f"{'='*50}\nProfile: {name}\n{'='*50}")
        for i, (song, score, explanation) in enumerate(recs, 1):
            print(f"{i}. {song['title']} by {song['artist']}")
            print(f"   Score: {score:.2f}")
            print(f"   Why:   {explanation}")
        print()


# ── AI interactive mode ───────────────────────────────────────────────────────

def run_interactive_mode(logger: logging.Logger) -> None:
    """Natural-language mode powered by Claude API with tool use."""
    from src.ai_recommender import get_ai_recommendations

    print("\n🎵  AI Music Recommender  (powered by Claude)")
    print("Describe the music you want in plain English.")
    print("Type 'quit' to exit.\n")

    while True:
        try:
            query = input("What are you in the mood for? > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if query.lower() in ("quit", "exit", "q", ""):
            print("Goodbye!")
            break

        is_valid, error_msg = validate_query(query)
        if not is_valid:
            print(f"[Guardrail] {error_msg}\n")
            continue

        print("\nFinding recommendations...\n")
        try:
            result = get_ai_recommendations(query)
            log_recommendation_event(query, result, logger)

            recs = result["recommendations"]
            print(f"Confidence: {result['confidence']:.0%}\n")
            print("Top Recommendations:")
            for i, rec in enumerate(recs, 1):
                print(
                    f"  {i}. {rec['title']} by {rec['artist']}"
                    f"  [{rec['genre']} / {rec['mood']} / energy {rec['energy']}]"
                    f"  score {rec['score']:.2f}"
                )
            print(f"\n{result['explanation']}\n")

        except Exception as exc:
            logger.error("Error processing query: %s", exc)
            print(f"[Error] Could not process request: {exc}\n")


# ── Evaluation mode ───────────────────────────────────────────────────────────

def run_evaluate_mode() -> None:
    """Run predefined test cases and print a pass/fail summary."""
    from src.evaluator import run_evaluation
    summary = run_evaluation()
    print(f"Pass rate: {summary['pass_rate']:.0%}")
    print(f"Average confidence: {summary['avg_confidence']:.2f}")


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="AI Music Recommender Simulation")
    parser.add_argument("--classic",  action="store_true", help="Run original profile-based mode")
    parser.add_argument("--evaluate", action="store_true", help="Run evaluation harness")
    parser.add_argument("--verbose",  action="store_true", help="Enable DEBUG logging")
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    app_logger = setup_logging(log_level)

    if args.classic:
        run_classic_mode()
    elif args.evaluate:
        run_evaluate_mode()
    else:
        run_interactive_mode(app_logger)


if __name__ == "__main__":
    main()
