# 🎵 Music Recommender Simulation

## Project Summary

This project simulates a content-based music recommendation system. It reads a catalog of songs from a CSV file and scores each one against a user's taste profile (preferred genre, mood, energy level, and valence). Songs are ranked by score and the top results are returned with plain-language explanations of why each track was chosen. The system is designed to be transparent — every recommendation includes a breakdown of exactly which attributes matched and how many points each contributed.

---

## How The System Works

Real-world platforms like Spotify use a mix of **collaborative filtering** (learning from what similar users liked) and **content-based filtering** (matching songs by their audio features). This simulation focuses purely on content-based filtering because it is simpler to inspect and reason about.

### Features each `Song` uses

- `genre` — musical category (pop, rock, lofi, jazz, etc.)
- `mood` — emotional feel (happy, chill, intense, moody, etc.)
- `energy` — intensity on a 0.0–1.0 scale
- `tempo_bpm` — beats per minute (loaded but not currently scored)
- `valence` — musical positivity on a 0.0–1.0 scale
- `danceability` — rhythmic suitability on a 0.0–1.0 scale
- `acousticness` — how acoustic the track feels on a 0.0–1.0 scale

### What `UserProfile` stores

- `favorite_genre` — the genre the user prefers
- `favorite_mood` — the mood the user prefers
- `target_energy` — the energy level the user aims for
- `likes_acoustic` — whether the user prefers acoustic tracks

### Algorithm Recipe (scoring logic)

For each song in the catalog the recommender awards:

| Rule | Points |
|---|---|
| Genre matches user preference | +2.0 |
| Mood matches user preference | +1.0 |
| Energy similarity (1.0 − |song\_energy − target|) | 0.0–1.0 |
| Valence similarity (optional, ×0.5 weight) | 0.0–0.5 |

Songs are then sorted highest-to-lowest and the top K are returned with a reason string listing exactly which rules fired.

### Data flow

```
Input (User Prefs)
      ↓
  For each song in catalog:
      score_song(user_prefs, song)  →  (score, reasons)
      ↓
  Sort all songs by score (descending)
      ↓
Output: Top K recommendations with explanations
```

### Potential biases expected before testing

- Genre matching carries the most weight (+2.0), so the system will strongly favor songs in the user's preferred genre even when other attributes conflict.
- The catalog has 18 songs — small diversity means some genres (pop, lofi) have more representatives and will naturally appear more in recommendations.

---

## Getting Started

### Setup

1. Create a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python -m src.main
   ```

### Running Tests

```bash
pytest
```

---

## Experiments You Tried

### Profile: High-Energy Pop

Top results: *Sunrise City*, *Summer Static*, *Gym Hero*. Both genre+mood matches scored ~4.4, while mood-only matches dropped to ~2.4. The gap shows that genre weight dominates.

### Profile: Chill Lofi

Top results: *Library Rain*, *Midnight Coding*, *Focus Flow*. The two mood+genre matches were nearly tied (4.46 vs 4.45) because their energy values are both very close to the target (0.38). This confirms the energy similarity term can act as a useful tiebreaker.

### Profile: Deep Intense Rock

Top results: *Storm Runner*, *Gravity Pull* (both Voltline). Having only two rock songs in the catalog means the same artist dominates the top 2 every time — a clear diversity limitation.

### Weight Experiment

When the energy similarity weight was doubled (×2.0) and genre weight halved (+1.0), the rankings for the "High-Energy Pop" profile shifted so that *Gym Hero* (energy 0.93, no mood match) beat out *Rooftop Lights* (energy 0.76, mood match). This confirmed the scoring is sensitive to weight choices.

---

## Limitations and Risks

- The catalog has only 18 songs, so recommendations for niche genres (folk, EDM) have very little to choose from.
- Genre match is worth twice as much as mood match, which can cause a "wrong vibe" song in the right genre to outrank a "perfect vibe" song in a slightly different genre.
- There is no diversity enforcement — the same artist can appear multiple times in the top 5.
- The system has no memory of past listens, so it will recommend the same songs every session.
- Lyrics, language, cultural context, and listener history are completely ignored.

---

## Reflection

See [model_card.md](model_card.md) for the full model card and personal reflection.

---

## Terminal Output Screenshots

### High-Energy Pop Profile
```
Profile: High-Energy Pop
1. Sunrise City by Neon Echo       Score: 4.46
   Why: genre match (pop, +2.0); mood match (happy, +1.0); energy similarity (0.97); valence similarity (0.49)
2. Summer Static by Coastal Drift  Score: 4.42
   Why: genre match (pop, +2.0); mood match (happy, +1.0); energy similarity (0.94); valence similarity (0.48)
3. Gym Hero by Max Pulse           Score: 3.38
   Why: genre match (pop, +2.0); energy similarity (0.92); valence similarity (0.46)
```

### Chill Lofi Profile
```
Profile: Chill Lofi
1. Library Rain by Paper Lanterns  Score: 4.46
   Why: genre match (lofi, +2.0); mood match (chill, +1.0); energy similarity (0.97); valence similarity (0.49)
2. Midnight Coding by LoRoom       Score: 4.45
   Why: genre match (lofi, +2.0); mood match (chill, +1.0); energy similarity (0.96); valence similarity (0.49)
3. Focus Flow by LoRoom            Score: 3.47
   Why: genre match (lofi, +2.0); energy similarity (0.98); valence similarity (0.49)
```

### Deep Intense Rock Profile
```
Profile: Deep Intense Rock
1. Storm Runner by Voltline        Score: 4.47
   Why: genre match (rock, +2.0); mood match (intense, +1.0); energy similarity (0.99); valence similarity (0.48)
2. Gravity Pull by Voltline        Score: 4.46
   Why: genre match (rock, +2.0); mood match (intense, +1.0); energy similarity (0.98); valence similarity (0.48)
3. Bass Drop Kingdom by Hardline   Score: 2.38
   Why: mood match (intense, +1.0); energy similarity (0.93); valence similarity (0.45)
```
