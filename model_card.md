# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder is designed to suggest 3–5 songs from a small catalog based on a user's preferred genre, mood, energy level, and valence. It is built for classroom exploration and demonstration purposes — not for production use with real listeners. The system assumes the user knows their own preferences and can express them as a simple dictionary of values.

**Non-intended use:** This model should not be deployed to real users on a streaming platform. It lacks listening history, skip data, collaborative signals, and any content understanding beyond basic numerical attributes.

---

## 3. How the Model Works

The recommender reads a list of songs from a spreadsheet. Each song has attributes like genre (pop, rock, lofi), mood (happy, chill, intense), and a set of numbers describing how energetic, danceable, positive, and acoustic it sounds.

When a user tells the system their preferences, the system goes through every song in the catalog and gives it a point score:

- **+2.0 points** if the song's genre matches the user's preferred genre — the biggest reward, because genre is the clearest signal of musical taste.
- **+1.0 point** if the song's mood matches the user's preferred mood.
- **Up to 1.0 points** based on how close the song's energy level is to the user's target — a song with energy 0.80 scores almost perfectly for a user who wants 0.82.
- **Up to 0.5 points** based on how close the song's valence (musical positivity) is to the user's target.

After every song is scored, the system sorts the list from highest to lowest and returns the top results along with a plain-language explanation of which attributes contributed points.

---

## 4. Data

- **Catalog size:** 18 songs
- **Features per song:** genre, mood, energy (0–1), tempo\_bpm, valence (0–1), danceability (0–1), acousticness (0–1)
- **Genres represented:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, folk, edm
- **Moods represented:** happy, chill, intense, relaxed, moody, focused, nostalgic
- **Data source:** Hand-crafted starter set (10 songs) expanded with 8 additional songs generated for genre/mood diversity
- **Missing from data:** lyrics, language, cultural origin, listener demographics, play counts, release year context

The dataset reflects a Western, English-language taste bias — genres like K-pop, Afrobeats, or classical are entirely absent.

---

## 5. Strengths

- **Transparent:** Every recommendation includes an exact breakdown of which rules fired and how many points each contributed. A user can always see *why* a song was suggested.
- **Deterministic:** Given the same user profile and catalog, the system always returns the same results — no randomness or black-box behavior.
- **Works well for clear, narrow preferences:** A user who strongly prefers pop+happy gets coherent, intuitive results at the top of the list.
- **Energy as a tiebreaker:** When two songs match genre and mood, the energy similarity score acts as a meaningful differentiator.

---

## 6. Limitations and Bias

- **Genre dominance creates a filter bubble.** Because a genre match is worth +2.0 — twice the weight of a mood match — the system will almost always surface genre-matching songs first, even if their mood, energy, and valence are far from ideal. A "relaxed pop" song will beat a "happy jazz" song for a happy-pop user, even if the jazz track feels more right.
- **Catalog imbalance amplifies the bubble.** Pop and lofi each have 3+ songs; folk, EDM, and synthwave have only 1–2. Users whose taste sits in underrepresented genres get fewer meaningful choices.
- **No artist diversity enforcement.** The same artist (e.g., Voltline) can occupy the top 2 slots if their songs best match the profile. Real systems add diversity constraints to avoid this.
- **Binary genre matching.** "Indie pop" and "pop" are treated as entirely different genres even though they share characteristics. A more nuanced system would use genre similarity scores.
- **No temporal awareness.** The system recommends the same songs in every session regardless of how recently they were played.

---

## 7. Evaluation

Three distinct user profiles were tested:

| Profile | Target | Top Result | Surprise? |
|---|---|---|---|
| High-Energy Pop | genre=pop, mood=happy, energy=0.85 | Sunrise City (4.46) | No — intuitive match |
| Chill Lofi | genre=lofi, mood=chill, energy=0.38 | Library Rain (4.46) | No — clear winner |
| Deep Intense Rock | genre=rock, mood=intense, energy=0.90 | Storm Runner (4.47) | Mild — same artist in top 2 |

**What surprised me:** The Chill Lofi profile produced two songs with nearly identical scores (4.46 vs 4.45). This shows that with a small catalog, tiny differences in energy distance can be the only differentiator. If the catalog were larger, this sensitivity would matter more.

**Logic experiment:** Doubling the energy weight and halving the genre weight changed whether a mood-only match or an energy-close genre match won. This confirmed the system is sensitive to weight choices and that no single weighting is universally "correct."

---

## 8. Future Work

1. **Add a diversity penalty** — if an artist already appears in the top results, reduce the score of their other songs so a wider range of artists surfaces.
2. **Genre similarity scoring** — instead of a binary genre match, use a similarity table (e.g., "indie pop" is 70% similar to "pop") to reduce harsh mismatches.
3. **Collaborative filtering layer** — collect implicit signals (play count, skips, repeat listens) and blend them with content scores so the system learns from behavior over time.

---

## 9. Personal Reflection

Building VibeFinder made the inner workings of recommendation systems feel much less mysterious. What looks like "magic" on Spotify is, at its core, a loop that scores every candidate against a set of rules and picks the winners — the same loop I wrote in `score_song`. The biggest surprise was how much the **weight choices** matter: doubling the energy weight changed which songs appeared, even though no preferences changed. This made me realize that every weighting decision is a design choice that reflects the developer's assumptions about what users care about — and those assumptions can easily be wrong.

Using AI tools helped me draft the initial structure quickly, but I had to verify every piece of logic myself. The AI suggested reasonable starting weights, but testing with real profiles was the only way to see whether the results actually "felt right." Human judgment — asking "does this recommendation make sense to a person?" — was essential at every evaluation step and can't be replaced by the algorithm itself.

If I extended this project, I would add a diversity constraint and experiment with blending content scores with simple popularity data to see whether real-world appeal improves the recommendations beyond pure attribute matching.
