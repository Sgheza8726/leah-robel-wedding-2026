# 🎧 Model Card — AI Music Recommender

## 1. Model Name

**VibeFinder 2.0** (extended from VibeFinder 1.0, Module 3)

---

## 2. Intended Use

VibeFinder 2.0 suggests 3–5 songs from a small catalog based on a user's natural-language description of what they want to hear. It is designed for classroom demonstration of how LLMs can be integrated into existing algorithmic systems — not for deployment to real streaming users.

**Intended:**
- Classroom exploration of AI-integrated recommendation pipelines
- Demonstrating agentic tool use and NL-to-structured-data extraction

**Not intended:**
- Production music streaming (catalog too small, no personalization history)
- Medical, legal, or safety-critical applications
- Replacing human music curation

---

## 3. How the Model Works

VibeFinder 2.0 has two layers working together:

**Layer 1 — AI Understanding (Claude):** When a user types something like "I want something intense for the gym," Claude reads that sentence and translates it into a set of numbers and labels: a genre (rock), a mood (intense), and an energy level (0.9). This is the same kind of thing a human music librarian would do — they hear what you want and mentally filter the collection.

**Layer 2 — Algorithmic Scoring (Python):** The scoring engine goes through every song in the catalog and gives it a point score: +2 for matching genre, +1 for matching mood, and fractional points based on how close the song's energy is to your target. Songs are then sorted and the top results are returned.

Claude then reads those results and writes a 2-3 sentence explanation in plain language.

---

## 4. Data

- **Catalog:** 18 songs across 9 genres (pop, rock, lofi, jazz, ambient, edm, folk, synthwave, indie pop) and 7 moods
- **Features per song:** genre, mood, energy (0–1), tempo\_bpm, valence (0–1), danceability (0–1), acousticness (0–1)
- **Data source:** Hand-crafted, no real song metadata or audio features
- **Representation gaps:** No classical, hip-hop, R&B, K-pop, Afrobeats, or non-English genres; no release year or cultural context
- **Whose taste?** The catalog reflects Western popular music categories with a bias toward genres common in lo-fi study playlists and gym playlists

---

## 5. Strengths

- **Transparent:** Every recommendation includes an exact breakdown of which scoring rules fired and how many points each contributed — there is no black box.
- **Separation of concerns:** Claude handles ambiguous language; the Python engine handles deterministic math. If Claude extracts the wrong genre, the scoring result is still predictable and auditable.
- **Confidence signal:** The confidence score gives users a quick indicator of how clear the result was — a 90% confidence means one song clearly dominated; 60% means several songs were close.
- **Robust to phrasing variations:** Claude can map "something to crush a workout" and "high energy gym music" to the same structured preferences, where a keyword-matching system would fail.

---

## 6. Limitations and Bias

- **Genre dominance creates filter bubbles.** Genre matching is worth +2.0 — twice the mood weight. If Claude maps a query to the wrong genre, the top results will feel completely wrong even if mood and energy are right. The user has no way to correct this in the current interface.
- **Catalog imbalance.** Pop and lofi each have 3+ songs; folk, EDM, and synthwave have 1–2 each. Users with niche tastes get fewer meaningful choices not because the algorithm fails, but because the data is thin.
- **Binary genre labels.** "Indie pop" and "pop" are separate strings. A query for "indie" might match one and not the other, even though they share sonic characteristics.
- **Claude can hallucinate preferences.** For very ambiguous queries (e.g., "something nostalgic"), Claude may confidently pick a genre that doesn't match what the user had in mind. There is no feedback loop to correct this.
- **No diversity enforcement.** The same artist (e.g., Voltline) can appear twice in the top 5. Real systems add diversity constraints.

---

## 7. Evaluation

Six test cases were run with the evaluation harness (`python -m src.main --evaluate`):

| ID | Query | Expected | Status |
|---|---|---|---|
| TC01 | "upbeat happy pop for a road trip" | pop/happy/energy≥0.6 | PASS |
| TC02 | "chill lofi to study to" | lofi/chill/energy≤0.55 | PASS |
| TC03 | "heavy intense rock for working out" | rock/intense/energy≥0.75 | PASS |
| TC04 | "relaxing jazz for a coffee shop" | jazz/relaxed/energy≤0.50 | PASS |
| TC05 | "dark moody electronic for night drives" | moody/energy≥0.50 | PASS |
| TC06 | "nostalgic folk songs, warm and acoustic" | folk/nostalgic/energy≤0.55 | PASS |

**What surprised me:** TC05 (dark moody electronic) passed even though neither "ambient" nor "synthwave" was explicitly expected — Claude correctly mapped "electronic" to "synthwave" or "ambient" without being told those were options. The model's world knowledge about genre labels helped where a keyword system would have failed.

**What struggled:** TC06 sometimes produces borderline confidence because only 2 folk songs exist. When the genre matches but energy expectations are tight, the result is technically correct but feels thin.

---

## 8. Future Work

1. **Expand and diversify the catalog** — At minimum 5 songs per genre to give the scoring engine meaningful variety. Ideally integrate with a real music API (Spotify, MusicBrainz) for real audio features.
2. **Add a diversity penalty** — Prevent the same artist from appearing more than once in the top 5 results.
3. **Session memory** — Track which songs were played or skipped and adjust future recommendations (collaborative signal).
4. **Feedback loop** — After recommendations, ask "Did this feel right?" and use the answer to weight Claude's genre/mood mappings in future sessions.

---

## 9. Personal Reflection

### AI Collaboration

**Helpful instance:** When designing the tool use architecture, Claude suggested separating the intent-extraction step (NL → structured preferences) from the scoring step (preferences → ranked songs) rather than having Claude score songs directly in prose. This was the right call — it keeps the scoring auditable and the AI layer replaceable. I kept that design.

**Flawed instance:** When I asked Claude to suggest confidence scoring logic, it proposed using the LLM's own token-probability outputs as a confidence signal. This sounded plausible but was wrong for this use case — token probabilities reflect Claude's uncertainty about language, not about whether the *recommender algorithm* found a good match. I replaced it with a score-gap heuristic based on the recommender's own output.

### What I Learned

Building this system clarified something I found confusing before: the difference between *what an LLM does well* and *what deterministic code does well*. Claude is good at understanding what "a road trip vibe" means and translating it into structured data. Python is good at applying consistent math to 18 songs and returning the same answer every time. The power came from connecting the two — not from replacing one with the other.

The hardest part was the confidence scoring. A confidence score implies the system knows how certain it is, but the system is actually two separate components with different failure modes. Claude might be very confident about genre but completely wrong, and the Python engine might return a low-confidence spread because the catalog is sparse, not because the genre was wrong. I settled for a heuristic that measures the *ranking spread*, which at least captures whether the recommendation was unambiguous — even if it can't diagnose *why*.

Real music recommenders on Spotify or YouTube combine hundreds of signals — collaborative filtering, audio fingerprinting, recency, social graph — in ways that make even their creators uncertain about why specific songs surface. Building this simple version made me more skeptical of any recommendation system that claims to "understand" what you want. The system doesn't understand anything; it matches patterns in the way it was told to match them.
