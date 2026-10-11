# CoderCoach

**Learn to recognize the pattern, not memorize the answer.**

CoderCoach is a problem-solving coach for students. Paste a coding problem and it identifies which problem-solving pattern fits (Sliding Window, Two Pointers, Hash Map, and more), then reveals hints one at a time, from vague to specific, so you work out the solution yourself. It finishes with practice problems that use the same pattern.

Built at HackRU (Education track).

## How it works

1. The student pastes a problem into the chat box.
2. The backend sends the problem to Google Gemini, which must choose **one** pattern from a curated list.
3. The hints and practice problems come from our own hand-written `patterns.json`, not from the model, so the teaching content stays accurate and consistent.
4. The frontend shows the result as a hint ladder the student reveals step by step.

```
React frontend  --POST /api/analyze-->  FastAPI  -->  analyze.py  -->  Gemini
                                                          |
                                                    patterns.json
                                              (curated hints + practice)
```

## Tech stack

- **Frontend:** React + TypeScript (Vite)
- **Backend:** Python, FastAPI
- **AI:** Google Gemini API
- **Content:** `backend/patterns.json`

## Project structure

```
backend/
  main.py          API route (/api/analyze)
  analyze.py       prompt building, reply parsing, validation
  llm.py           thin Gemini wrapper
  patterns.json    pattern library: hints and practice problems
  test_keys.py     checks that API keys work
  .env.example     template for your API key
frontend/CoderCoach/
  src/             React app
```

## Running it locally

**Prerequisites:** Python 3.11+, Node.js 18+, and a Gemini API key from [Google AI Studio](https://aistudio.google.com/).

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
cp .env.example .env           # then paste your key into .env
python test_keys.py            # optional: confirms your key works
uvicorn main:app --reload --port 8000
```

`.env` format:

```
GEMINI_API_KEYS=your_key_here
# optional: GEMINI_MODEL=...
```

### Frontend

```bash
cd frontend/CoderCoach
npm install
npm run dev
```

Open the URL Vite prints (usually http://localhost:5173). The backend must be running on port 8000.

## Adding or editing patterns

Everything the student sees as hints comes from `backend/patterns.json`. Each entry has a pattern name, an example, four hints ordered vague to specific, and practice problems. Add an entry and it's available immediately, with no code changes.

## Limitations and next steps

- Covers six patterns today; BFS/DFS, Greedy, and Backtracking are next.
- Progress tracking across sessions is not built yet.
- Pattern detection depends on the model, so unusual problems may come back with low confidence.

## Team

- Wisdom 
- Abhigya 
- Yogishi 
