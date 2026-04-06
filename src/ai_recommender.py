"""
Claude-powered music recommendation via tool use (agentic workflow).

Pipeline:
  User natural-language query
      → Claude (interprets intent, calls tools)
      → recommend_songs() / get_song_details() tool execution
      → Claude (synthesises natural-language explanation)
      → Result dict with recommendations, explanation, confidence, usage
"""
import json
import logging
import anthropic
from typing import Optional

from src.recommender import load_songs, recommend_songs

logger = logging.getLogger(__name__)

_client: Optional[anthropic.Anthropic] = None
_songs_cache: Optional[list] = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client


def _get_songs() -> list:
    global _songs_cache
    if _songs_cache is None:
        _songs_cache = load_songs("data/songs.csv")
    return _songs_cache


# ── Tool definitions ──────────────────────────────────────────────────────────

TOOLS = [
    {
        "name": "recommend_songs",
        "description": (
            "Score and rank songs from the catalog based on structured taste preferences. "
            "Call this once you have inferred the user's genre, mood, and energy."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "genre": {
                    "type": "string",
                    "description": (
                        "Preferred genre. One of: pop, rock, lofi, jazz, ambient, "
                        "edm, folk, synthwave, indie pop"
                    ),
                },
                "mood": {
                    "type": "string",
                    "description": (
                        "Preferred mood. One of: happy, chill, intense, relaxed, "
                        "moody, focused, nostalgic"
                    ),
                },
                "energy": {
                    "type": "number",
                    "description": "Target energy 0.0 (very calm) to 1.0 (very intense).",
                },
                "valence": {
                    "type": "number",
                    "description": "Musical positivity 0.0 (dark) to 1.0 (bright). Optional.",
                },
                "k": {
                    "type": "integer",
                    "description": "Number of results to return (default 5).",
                },
            },
            "required": ["genre", "mood", "energy"],
        },
    },
    {
        "name": "get_song_details",
        "description": "Retrieve full attribute data for a song by its exact title.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Exact song title."}
            },
            "required": ["title"],
        },
    },
]

SYSTEM_PROMPT = """You are a music recommendation assistant with access to a song catalog.

Your job:
1. Interpret the user's natural-language music request.
2. Map it to structured preferences (genre, mood, energy 0-1, optionally valence 0-1).
3. Call the recommend_songs tool with those preferences.
4. After receiving results, write a concise 2-3 sentence explanation of why these songs fit the request.

Available genres: pop, rock, lofi, jazz, ambient, edm, folk, synthwave, indie pop
Available moods:  happy, chill, intense, relaxed, moody, focused, nostalgic

Keep your final explanation brief and friendly. Do not repeat the raw scores."""


# ── Tool execution ────────────────────────────────────────────────────────────

def _execute_tool(tool_name: str, tool_input: dict) -> str:
    """Dispatch a tool call and return a JSON string result."""
    songs = _get_songs()

    if tool_name == "recommend_songs":
        user_prefs = {
            "genre": tool_input.get("genre", ""),
            "mood": tool_input.get("mood", ""),
            "energy": float(tool_input.get("energy", 0.5)),
        }
        if "valence" in tool_input:
            user_prefs["valence"] = float(tool_input["valence"])
        k = int(tool_input.get("k", 5))
        results = recommend_songs(user_prefs, songs, k=k)
        payload = [
            {
                "title": s["title"],
                "artist": s["artist"],
                "genre": s["genre"],
                "mood": s["mood"],
                "energy": s["energy"],
                "score": score,
                "why": explanation,
            }
            for s, score, explanation in results
        ]
        return json.dumps(payload)

    if tool_name == "get_song_details":
        title = tool_input.get("title", "")
        song = next(
            (s for s in songs if s["title"].lower() == title.lower()), None
        )
        return json.dumps(song) if song else json.dumps({"error": f"Song '{title}' not found."})

    return json.dumps({"error": f"Unknown tool: {tool_name}"})


# ── Confidence scoring ────────────────────────────────────────────────────────

def _compute_confidence(recommendations: list) -> float:
    """
    Confidence 0-1 based on top score magnitude and gap to second place.
    Higher gap = clearer winner = higher confidence.
    """
    if not recommendations:
        return 0.0
    if len(recommendations) == 1:
        return round(min(1.0, recommendations[0]["score"] / 4.5), 2)
    top = recommendations[0]["score"]
    second = recommendations[1]["score"]
    magnitude = min(1.0, top / 4.5) * 0.7
    gap = min(1.0, (top - second) / 2.0) * 0.3
    return round(magnitude + gap, 2)


# ── Main entry point ──────────────────────────────────────────────────────────

def get_ai_recommendations(user_query: str) -> dict:
    """
    Run the full agentic recommendation pipeline for a natural-language query.

    Returns a dict:
        query           – original query string
        recommendations – list of {title, artist, genre, mood, energy, score, why}
        explanation     – Claude's natural-language summary
        confidence      – float 0-1
        tool_calls      – list of {tool, input} for observability
        usage           – {input_tokens, output_tokens}
    """
    logger.info("Query received: %r", user_query)
    client = _get_client()
    messages = [{"role": "user", "content": user_query}]
    recommendations: list = []
    tool_calls: list = []
    final_text = ""
    last_usage = {"input_tokens": 0, "output_tokens": 0}

    # Agentic loop – runs until Claude stops calling tools
    for _turn in range(10):  # hard cap as guardrail
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2048,
            thinking={"type": "adaptive"},
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        last_usage = {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        }
        logger.debug("Turn %d stop_reason=%s usage=%s", _turn, response.stop_reason, last_usage)

        # Collect final text from this turn
        for block in response.content:
            if block.type == "text":
                final_text = block.text

        if response.stop_reason == "end_turn":
            break

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                logger.info("Tool call: %s(%s)", block.name, json.dumps(block.input))
                result_str = _execute_tool(block.name, block.input)
                tool_calls.append({"tool": block.name, "input": block.input})
                if block.name == "recommend_songs":
                    try:
                        recommendations = json.loads(result_str)
                    except json.JSONDecodeError:
                        pass
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result_str,
                    }
                )
            messages.append({"role": "user", "content": tool_results})
        else:
            # Unexpected stop reason – bail out
            logger.warning("Unexpected stop_reason: %s", response.stop_reason)
            break

    confidence = _compute_confidence(recommendations)
    logger.info(
        "Done: %d recommendations, confidence=%.2f", len(recommendations), confidence
    )

    return {
        "query": user_query,
        "recommendations": recommendations,
        "explanation": final_text,
        "confidence": confidence,
        "tool_calls": tool_calls,
        "usage": last_usage,
    }
