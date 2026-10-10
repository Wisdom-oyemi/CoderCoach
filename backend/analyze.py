
import json
from pathlib import Path

from llm import ask_llm

# ---------------------------------------------------------------------------
# While False -> the real pipeline runs. While True -> analyze() returns
# MOCK_RESPONSE so the frontend can be built before this file is finished.
# Flip to False once step 5 works.
# ---------------------------------------------------------------------------
USE_MOCK = True

PATTERNS_FILE = Path(__file__).parent / "patterns.json"

MOCK_RESPONSE = {
    "pattern": "Sliding Window",
    "confidence": "high",
    "why": "The problem asks for the best contiguous subarray.",
    "hints": [
        "What's the brute-force approach, and what does it recompute?",
        "Could you reuse work between overlapping subarrays?",
        "This is a Sliding Window problem.",
        "Keep two pointers; grow right, shrink left when the condition breaks.",
    ],
    "practice": [
        "Longest Substring Without Repeating Characters",
        "Max Sum Subarray of Size K",
    ],
}


def load_patterns(path: Path = PATTERNS_FILE) -> list[dict]:
    """Read patterns.json and return it as a list of dicts."""
    


def build_prompt(problem: str, patterns: list[dict]) -> str:
    """Build the single prompt string we send to Gemini."""
    # TODO: build a string that contains, in this order:
    #   1. The role: "You are a coding tutor who teaches students to RECOGNIZE
    #      problem-solving patterns. You never give the full solution."
    #   2. The allowed patterns. For each one include its name and its "tell"
    #      (NOT the hints, to keep the prompt short). Tell the model it MUST
    #      choose exactly one name from this list and may not invent new ones.
    #   3. The student's problem, clearly separated (e.g. between ---).
    #   4. The output format: "Reply with JSON only, no markdown, no commentary"
    #      plus the keys: pattern, confidence, why. (We do NOT ask the model for
    #      hints or practice; those come from patterns.json so they stay curated.)
    #   5. Optional: a rule for when nothing fits, e.g. choose the closest
    #      pattern and set confidence to "low".
    # Tip: a ''' triple-quoted f-string is easiest. Build the pattern list with
    # a loop or join() first.


def parse_llm_reply(text: str) -> dict:
    """Turn the model's raw text reply into a dict."""
    # TODO:
    #   - strip whitespace
    #   - models often wrap JSON in ```json ... ``` fences even when told not to.
    #     If the text starts with ``` remove the opening fence line and the closing ```
    #   - json.loads the cleaned text and return it


def validate_result(result: dict, patterns: list[dict]) -> dict:
    """Check the model's answer, then fill in hints and practice from patterns.json."""
    # TODO:
    #   - make sure "pattern" and "why" are in result
    #   - find the entry in `patterns` whose "name" equals result["pattern"]
    #     (compare case-insensitively, strip spaces). If none matches, raise
    #     ValueError. (Stretch: fall back to the closest match instead.)
    #   - if "confidence" isn't one of high/medium/low, set it to "low"
    #   - build and return the final contract dict:
    #       pattern    <- the official name from patterns.json
    #       confidence <- from the model (cleaned)
    #       why        <- from the model
    #       hints      <- entry["hints"]       (curated, NOT from the model)
    #       practice   <- entry["practice"]    (curated, NOT from the model)


def analyze(problem: str) -> dict:
    """Main entry point called by main.py. Returns the contract dict."""
    if USE_MOCK:
        return MOCK_RESPONSE

    # TODO:
    #   1. patterns = load_patterns()
    #   2. prompt   = build_prompt(problem, patterns)
    #   3. reply    = ask_llm(prompt)
    #   4. parsed   = parse_llm_reply(reply)
    #   5. return validate_result(parsed, patterns)


if __name__ == "__main__":
    test_problems = [
        "Given an array of integers and a number k, find the maximum sum of any "
        "contiguous subarray of size k.",
    ]
    for p in test_problems:
        print("PROBLEM:", p)
        print(json.dumps(analyze(p), indent=2))
        print("-" * 60)
