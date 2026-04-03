# Reflection: Profile Comparisons

## High-Energy Pop vs. Chill Lofi

These two profiles are near-opposites. The pop profile targets high energy (0.85), happy mood, and pop genre. The lofi profile targets low energy (0.38), chill mood, and lofi genre. The top-scoring songs for each are completely different — *Sunrise City* leads pop, *Library Rain* leads lofi — which makes sense because both genre and mood are worth the most points and they don't overlap at all between these profiles.

What's interesting is that both profiles produced a top score of ~4.46. This tells us the scoring ceiling is similar regardless of preference, because both profiles had songs that matched genre + mood + close energy. The system is internally consistent across different taste types.

## High-Energy Pop vs. Deep Intense Rock

Both profiles target high energy (0.85 vs 0.90) and a punchy mood, but differ in genre. The pop profile recommends lighter tracks with high valence (Sunrise City, Summer Static). The rock profile recommends heavier tracks with lower valence (Storm Runner, Gravity Pull). Even though the energy levels are similar, the genre and valence differences produce completely different vibes at the top of the list — this shows the system is capturing more than just raw intensity.

One issue: the rock catalog only has 2 songs, so Voltline (the only rock artist) occupies both top slots. The system works correctly, but the small catalog limits diversity for niche genres.

## Chill Lofi vs. Deep Intense Rock

This is the most dramatic contrast. The lofi profile rewards slow, quiet, acoustic-leaning tracks. The rock profile rewards fast, loud, electric tracks. The top recommendations share zero songs. This confirms the scoring logic creates meaningful separation between radically different taste profiles — the system isn't just returning the same popular songs to everyone.

The key takeaway: the recommender's quality depends heavily on the diversity of the catalog. A user with an underrepresented taste (e.g., jazz or folk) will get fewer strong matches simply because fewer songs exist for those genres, not because the algorithm is worse for them.
