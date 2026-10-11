import json
from pathlib import Path
from dotenv import load_dotenv
from llm import ask_llm

# ---------------------------------------------------------------------------
# While False -> the real pipeline runs. While True -> analyze() returns
# MOCK_RESPONSE so the frontend can be built before this file is finished.
# Flip to False once step 5 works.
# ---------------------------------------------------------------------------
USE_MOCK = False

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
    with path.open("r", encoding="utf-8") as file:
        patterns = json.load(file)

    return patterns


def build_prompt(problem: str, patterns: list[dict]) -> str:
    """Build the single prompt string we send to Gemini."""
    
    allowed_patterns = []
    for entry in patterns:
        allowed_patterns.append(
            f'- {entry["pattern"]}: {entry["why"]}'
        )

    pattern_list = "\n".join(allowed_patterns)

    prompt = f"""
    You are a coding tutor who teaches students to RECOGNIZE
    problem-solving patterns. You never give the full solution.

    Choose exactly ONE pattern from the approved list below.
    Do not invent or rename patterns.

    APPROVED PATTERNS:
    {pattern_list}

    STUDENT'S PROBLEM:
    ---
    {problem}
    ---

    If no pattern fits perfectly, choose the closest one and set
    confidence to "low".

    Reply with JSON only, no markdown, no commentary.
    Use exactly these keys:
    - pattern
    - confidence
    - why

    confidence must be "high", "medium", or "low".
    Do not include hints or practice problems.
    """

    return prompt


def parse_llm_reply(text: str) -> dict:
       text = text.strip()
       if text.startswith("```"):
           lines = text.splitlines()[1:]          # drop the opening ``` / ```json line
           if lines and lines[-1].strip() == "```":
               lines = lines[:-1]                 # drop the closing fence
           text = "\n".join(lines).strip()
       try:
           return json.loads(text)
       except json.JSONDecodeError:
           raise ValueError(f"Model reply was not valid JSON: {text[:200]}")
                          
        
    

def validate_result(result: dict, patterns: list[dict]) -> dict:
    """Check the model's answer, then fill in hints and practice from patterns.json."""
    if "pattern" not in result or "why" not in result:
        raise ValueError("The AI response is missing required fields.")

    selected_pattern = str(result["pattern"]).strip().casefold()

    matched_entry = None

    for entry in patterns:
        if entry["pattern"].strip().casefold() == selected_pattern:
            matched_entry = entry
            break

    if matched_entry is None:
        raise ValueError(
            f"Unknown pattern returned by AI: {result['pattern']}"
        )

    confidence = str(result.get("confidence", "low")).strip().lower()

    if confidence not in {"high", "medium", "low"}:
        confidence = "low"

    why = result["why"]

    if not isinstance(why, str) or not why.strip():
        raise ValueError("The AI response has an invalid explanation.")

    final_result = {
        "pattern": matched_entry["pattern"],
        "confidence": confidence,
        "why": why.strip(),
        "hints": matched_entry["hints"],
        "practice": matched_entry["practice"],
    }

    return final_result


def analyze(problem: str) -> dict:
    """Main entry point called by main.py. Returns the contract dict."""
    if USE_MOCK:
        return MOCK_RESPONSE
    if not problem.strip(): raise ValueError("Please enter a problem.")

    patterns = load_patterns()
    prompt = build_prompt(problem, patterns)
    for attempt in range(2):
       try:
           reply = ask_llm(prompt)
           return validate_result(parse_llm_reply(reply), patterns)
       except ValueError:
           if attempt == 1:
               raise


if __name__ == "__main__":
    test_problems = [
        "Given an array of integers and a number k, find the maximum sum of any "
        "contiguous subarray of size k.",
    ]
    for p in test_problems:
        print("PROBLEM:", p)
        print(json.dumps(analyze(p), indent=2))
        print("-" * 60)