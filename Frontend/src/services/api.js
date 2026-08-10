const API_URL = "http://127.0.0.1:8000";

export async function sendMessage(message) {
  const response = await fetch(`${API_URL}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      session_id: "test-session",
      message: message,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to send message");
  }

  const data = await response.json();

  return data.response;
}

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