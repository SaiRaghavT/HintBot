const API_URL = "http://127.0.0.1:8000";


// =========================
// CHAT
// =========================

export async function sendMessage({
  sessionId,
  problemId,
  message,
  code,
  executionOutput,
  executionError
}) {

  const response = await fetch(`${API_URL}/api/chat`, {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      session_id: sessionId,
      problem_id: problemId,
      message: message,
      code: code,
      execution_output: executionOutput,
      execution_error: executionError,
    }),
  })

  if (!response.ok) {

    const errorData = await response.json()

    console.error("CHAT API ERROR:", errorData)

    throw new Error("Failed to send message")
  }

  return await response.json()
}


// =========================
// RUN CODE
// =========================

export async function runCode(code) {

  const response = await fetch(`${API_URL}/api/run`, {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      language: "python",
      code: code,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to run code");
  }

  return await response.json();
}


// =========================
// CURRENT PROBLEM
// =========================

export async function getCurrentProblem() {

  const response = await fetch(
    `${API_URL}/api/problems/current`
  );

  if (!response.ok) {
    throw new Error("Failed to load problem");
  }

  return await response.json();
}