import { useState } from "react";
import type { FormEvent } from "react";
import "./App.css";

type CoachResult = {
  pattern: string;
  confidence: string;
  why: string;
  hints: string[];
  practice: string[];
};

const demoResult: CoachResult = {
  pattern: "Sliding Window",
  confidence: "high",
  why: "The problem asks for the best contiguous subarray, so overlapping ranges can reuse their previous work.",
  hints: [
    "What does the brute-force approach recompute for each new range?",
    "Can you keep a running total as the range moves across the array?",
    "This is a Sliding Window problem.",
    "Grow the right side of the window and remove values from the left when it is too large.",
  ],
  practice: [
    "Longest Substring Without Repeating Characters",
    "Minimum Size Subarray Sum",
  ],
};

function getName(): string {
  const savedName = window.localStorage.getItem("codercoach-name");
  if (savedName) return savedName;

  let enteredName: string | null = null;
  try {
    enteredName = window.prompt("What should CoderCoach call you?");
  } catch {
    // Some embedded browsers disable prompt dialogs; use the demo name there.
  }
  const name = enteredName?.trim() || "Coder";
  window.localStorage.setItem("codercoach-name", name);
  return name;
}

function isCoachResult(value: unknown): value is CoachResult {
  if (!value || typeof value !== "object") return false;
  const result = value as Record<string, unknown>;
  return (
    typeof result.pattern === "string" &&
    typeof result.confidence === "string" &&
    typeof result.why === "string" &&
    Array.isArray(result.hints) &&
    result.hints.every((hint) => typeof hint === "string") &&
    Array.isArray(result.practice) &&
    result.practice.every((item) => typeof item === "string")
  );
}

async function askCoach(problem: string): Promise<CoachResult> {
  const backendUrl = import.meta.env.VITE_BACKEND_URL?.trim();
  if (!backendUrl) {
    await new Promise((resolve) => window.setTimeout(resolve, 450));
    return demoResult;
  }

  const response = await fetch(`${backendUrl.replace(/\/$/, "")}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ problem }),
  });

  if (!response.ok) {
    throw new Error(`Coach request failed (${response.status}).`);
  }

  const data: unknown = await response.json();
  if (!isCoachResult(data)) {
    throw new Error("The coach returned an unexpected response.");
  }
  return data;
}

export default function App() {
  const [name] = useState(getName);
  const [problem, setProblem] = useState("");
  const [result, setResult] = useState<CoachResult | null>(null);
  const [visibleHints, setVisibleHints] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmedProblem = problem.trim();
    if (!trimmedProblem || loading) return;

    setLoading(true);
    setError("");
    setResult(null);
    setVisibleHints(1);

    try {
      setResult(await askCoach(trimmedProblem));
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "The coach could not answer right now.",
      );
    } finally {
      setLoading(false);
    }
  }

  const hints = result?.hints ?? [];
  const hasMoreHints = visibleHints < hints.length;
  const patternRevealed = visibleHints >= 3;
  const practiceRevealed = hints.length > 0 && visibleHints >= hints.length;

  return (
    <div className="app">
      <header className="topbar">
        <div className="icons" aria-label="Quick actions">
          <button className="icon-btn" type="button" aria-label="Profile">
            <span aria-hidden="true">●</span>
          </button>
          <button className="icon-btn" type="button" aria-label="Tips">
            <span aria-hidden="true">✦</span>
          </button>
        </div>
        <p className="eyebrow">Your pattern practice partner</p>
        <h1>CoderCoach</h1>
      </header>

      <main className="main">
        {!result && !loading && !error && (
          <h2 className="welcome">Welcome, {name}!</h2>
        )}

        {loading && <p className="status">Thinking...</p>}

        {error && (
          <div className="error-state" role="alert">
            <p>{error}</p>
            <button className="hint-btn" type="button" onClick={() => setError("")}>
              Try again
            </button>
          </div>
        )}

        {result && (
          <section className="response-card" aria-live="polite">
            <div className="card-heading">
              <div>
                <p className="card-label">Pattern coach</p>
                {patternRevealed && <h2>{result.pattern}</h2>}
              </div>
              <span className="confidence">{result.confidence} confidence</span>
            </div>
            <p className="why">{result.why}</p>

            <div className="hint-ladder">
              {hints.slice(0, visibleHints).map((hint, index) => (
                <p className="hint" key={`${hint}-${index}`}>
                  <span>{index + 1}</span>
                  {hint}
                </p>
              ))}
            </div>

            {hasMoreHints && (
              <button
                className="hint-btn"
                type="button"
                onClick={() => setVisibleHints((current) => current + 1)}
              >
                Reveal next hint
              </button>
            )}

            {practiceRevealed && (
              <div className="practice">
                <p className="card-label">Try next</p>
                <ul>
                  {result.practice.map((item) => <li key={item}>{item}</li>)}
                </ul>
              </div>
            )}
          </section>
        )}
      </main>

      <form className="composer" onSubmit={handleSubmit}>
        <label htmlFor="problem">Prompt your problem...</label>
        <div className="composer-row">
          <input
            id="problem"
            value={problem}
            onChange={(event) => setProblem(event.target.value)}
            placeholder="e.g. Find the longest substring..."
            autoComplete="off"
          />
          <button type="submit" disabled={loading || !problem.trim()}>
            {loading ? "Thinking..." : "Ask"}
          </button>
        </div>
      </form>
    </div>
  );
}
