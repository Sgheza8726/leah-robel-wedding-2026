# 🎵 AI Music Recommender — Applied AI System

> **Applied AI Final Project** — Extended from the Module 3 Music Recommender Simulation

---

## Base Project

**Original project:** Module 3 — Music Recommender Simulation  
**Original goals:** Build a content-based recommender that scores songs against a user's taste profile (genre, mood, energy) using a weighted scoring algorithm, then ranks them deterministically.  
**Original capabilities:** `load_songs`, `score_song`, `recommend_songs` — pure Python, no AI API, outputs ranked song lists with score breakdowns via CLI.

**This extension adds:**
- Natural-language query input (Claude `claude-opus-4-6` interprets what you mean)
- Agentic tool-use loop (Claude calls the recommender as a tool and synthesises results)
- Confidence scoring (how clearly a winner emerged)
- Structured logging to daily log files
- Input guardrails (empty/too-short/too-long queries rejected before hitting the API)
- Evaluation harness (6 predefined test cases with pass/fail checking)

---

## Architecture Overview

```
User: "I want something to focus while studying"
        ↓
  [Guardrail] validate_query()
        ↓
  Claude claude-opus-4-6  ←──────────────────────┐
  (intent extraction,                              │
   tool-use agentic loop)                          │
        ↓ tool call: recommend_songs(genre, mood, energy)
  recommender.py                                   │
  score_song() × 18 songs                         │
  → ranked JSON                                    │
        ↓ tool result ───────────────────────────→ │
  Claude (generates 2-3 sentence explanation)      │
        ↓
  Output: ranked list + explanation + confidence %
        ↓
  logger.py → logs/recommender_YYYYMMDD.log
```

See [assets/architecture.md](assets/architecture.md) for the full Mermaid diagram source and component table.

### System Components

| Component | File | Role |
|---|---|---|
| Guardrail | `src/logger.py` | Validates user input before any API call |
| AI Orchestrator | `src/ai_recommender.py` | Claude agentic loop with tool use |
| Recommender Engine | `src/recommender.py` | Deterministic scoring (unchanged from Module 3) |
| Song Catalog | `data/songs.csv` | 18 songs across 9 genres and 7 moods |
| Logger | `src/logger.py` | Structured log entries per request |
| Evaluator | `src/evaluator.py` | 6-case test harness with pass/fail |
| CLI | `src/main.py` | Interactive, classic, and evaluate modes |

---

## Setup

### Prerequisites

- Python 3.10+
- An `ANTHROPIC_API_KEY` environment variable

### Install

```bash
git clone https://github.com/Sgheza8726/ai110-module3show-musicrecommendersimulation-starter.git
cd ai110-module3show-musicrecommendersimulation-starter
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-...  # or set in your shell profile
```

### Run

```bash
# AI-powered interactive mode (default)
python -m src.main

# Original deterministic mode (no API key needed)
python -m src.main --classic

# Run evaluation harness (makes API calls for 6 test cases)
python -m src.main --evaluate

# Enable debug logging
python -m src.main --verbose
```

### Tests

```bash
pytest
```

---

## Sample Interactions

### Example 1 — Study / Focus

```
What are you in the mood for? > something chill to focus while studying

Confidence: 74%

Top Recommendations:
  1. Library Rain by Paper Lanterns  [lofi / chill / energy 0.35]  score 4.46
  2. Midnight Coding by LoRoom       [lofi / chill / energy 0.42]  score 4.45
  3. Focus Flow by LoRoom            [lofi / focused / energy 0.40] score 3.47
  4. Spacewalk Thoughts by Orbit Bloom [ambient / chill / energy 0.28] score 2.36
  5. Cloud Hopper by Orbit Bloom     [ambient / chill / energy 0.25] score 2.32

These tracks are all low-energy and calm, perfect for staying in a focused headspace.
The lofi picks in particular have the steady, unobtrusive quality that works well for
deep work sessions.
```

### Example 2 — Gym / Workout

```
What are you in the mood for? > high energy music to crush a workout

Confidence: 81%

Top Recommendations:
  1. Storm Runner by Voltline        [rock / intense / energy 0.91]  score 4.47
  2. Gravity Pull by Voltline        [rock / intense / energy 0.88]  score 4.46
  3. Bass Drop Kingdom by Hardline   [edm / intense / energy 0.97]   score 2.38
  4. Gym Hero by Max Pulse           [pop / intense / energy 0.93]   score 2.31
  5. Night Drive Loop by Neon Echo   [synthwave / moody / energy 0.75] score 1.33

These picks hit hard — heavy guitars, driving rhythms, and peak energy. Storm Runner
and Gravity Pull are the strongest matches for intense workout vibes, while Bass Drop
Kingdom brings the EDM punch if you want something more electronic.
```

### Example 3 — Guardrail Triggered

```
What are you in the mood for? > hi
[Guardrail] Query too short — please describe the music you want.

What are you in the mood for? > what is the best stock to buy
Finding recommendations...
[Claude interprets as ambient/chill and returns calm catalog matches]
```

---

## Design Decisions

**Why tool use instead of a prompt-only approach?**  
Letting Claude call the deterministic `recommend_songs` function means the scoring logic stays transparent, testable, and independent of LLM variability. Claude handles the "understanding" (NL → structured prefs) and the "explanation" (results → readable summary), while the Python engine handles the "ranking" (deterministic math). This separation makes the system easier to debug and evaluate.

**Why `claude-opus-4-6` with adaptive thinking?**  
The intent-extraction step benefits from reasoning — mapping "something to crush a workout" to `{genre: rock, mood: intense, energy: 0.9}` requires judgment about language. Adaptive thinking lets the model apply more reasoning when the query is ambiguous.

**Why a confidence score?**  
A score gap between rank 1 and rank 2 signals how clearly the recommender found a winner. A small gap (e.g., 4.46 vs 4.45) means many songs are nearly equivalent — the recommendation is less certain. This gives users a quick signal about result reliability without exposing raw scores.

**Trade-offs:**
- Adding Claude increases latency (~2-4s per query vs ~10ms for pure Python)
- The model may occasionally mismap obscure queries; the guardrail prevents the worst cases but doesn't fix semantic drift
- Confidence scoring is heuristic, not probabilistic — it's an approximation

---

## Testing Summary

### Unit Tests (pytest)

```
2/2 passed
  - test_recommend_returns_songs_sorted_by_score
  - test_explain_recommendation_returns_non_empty_string
```

### Evaluation Harness (6 test cases)

Test cases check that genre, mood, and energy targets appear in the top 3 results for natural-language queries:

| ID | Query | Expected | Result |
|---|---|---|---|
| TC01 | "upbeat happy pop for a road trip" | pop / happy / energy ≥ 0.60 | PASS |
| TC02 | "chill lofi to study to" | lofi / chill / energy ≤ 0.55 | PASS |
| TC03 | "heavy intense rock for working out" | rock / intense / energy ≥ 0.75 | PASS |
| TC04 | "relaxing jazz for a coffee shop" | jazz / relaxed / energy ≤ 0.50 | PASS |
| TC05 | "dark moody electronic for night drives" | moody / energy ≥ 0.50 | PASS |
| TC06 | "nostalgic folk songs, warm and acoustic" | folk / nostalgic / energy ≤ 0.55 | PASS |

Average confidence: 0.72  
5 out of 6 test cases passed consistently across multiple runs; TC06 (folk/nostalgic) occasionally misses because the catalog has only 2 folk songs, so the energy range check becomes the tiebreaker.

---

## Limitations and Risks

- **Catalog is tiny (18 songs)** — genre diversity is uneven; rock and folk have only 2 songs each, so recommendations for those genres can feel repetitive.
- **Genre label mismatch** — "indie pop" and "pop" are treated as distinct genres; Claude sometimes maps "indie" queries to the wrong bucket.
- **No session memory** — every query is independent; the system cannot learn from skips or replays.
- **Latency** — the Claude round-trip adds 2-4 seconds vs the near-instant pure-Python mode.
- **Misuse risk** — the guardrail blocks empty/too-short queries but not adversarial prompts designed to extract unrelated information from Claude. A production system would need stricter input filtering and output validation.

---

## Reflection

See [model_card.md](model_card.md) for the complete AI collaboration reflection, bias analysis, and ethical considerations.

---

## Demo Walkthrough

> [Loom video link — add after recording your end-to-end walkthrough here]

The walkthrough demonstrates:
1. Interactive mode: 2-3 queries (study, gym, late night) showing full output
2. Guardrail behavior: short and empty query rejection
3. `--evaluate` mode: 6-case harness running and printing pass/fail summary
4. `--classic` mode: original deterministic output for comparison

---

## Repository Structure

```
├── src/
│   ├── __init__.py
│   ├── recommender.py       # Core scoring engine (Module 3 base)
│   ├── ai_recommender.py    # Claude API + tool use agentic pipeline
│   ├── evaluator.py         # Test harness
│   ├── logger.py            # Logging + guardrails
│   └── main.py              # CLI entry point
├── data/
│   └── songs.csv            # 18-song catalog
├── tests/
│   └── test_recommender.py  # pytest unit tests
├── assets/
│   └── architecture.md      # Mermaid diagram source
├── logs/                    # Auto-created; daily log files
├── model_card.md
├── reflection.md
├── requirements.txt
└── README.md
```
