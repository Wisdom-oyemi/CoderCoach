"""Tiny API layer: exposes analyze() to the frontend.
Run from the backend/ folder:  uvicorn main:app --reload --port 8000
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from analyze import analyze

app = FastAPI(title="CoderCoach API")

# Lets the Vite dev server (port 5173) call this API from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProblemRequest(BaseModel):
    problem: str


@app.post("/api/analyze")
def analyze_route(body: ProblemRequest):
    try:
        return analyze(body.problem)
    except ValueError as e:  # bad input or unusable model reply
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:  # keys failed, network down, etc.
        raise HTTPException(status_code=500, detail="Couldn't analyze that. Try again.")
