import axios from "axios";

const api = axios.create({
  baseURL: "/api/v1",
  headers: { "Content-Type": "application/json" },
});

/**
 * POST /api/v1/analyze — Send pitch text + style for Director analysis.
 */
export async function analyzePitch(pitchText, selectedStyle) {
  const { data } = await api.post("/analyze", {
    pitch_text: pitchText,
    selected_style: selectedStyle,
  });
  return data;
}

/**
 * POST /api/v1/generate — Start storyboard generation, return SSE EventSource.
 *
 * We use fetch + ReadableStream because axios doesn't support SSE natively.
 */
export function startGeneration(payload, onEvent) {
  const controller = new AbortController();

  (async () => {
    try {
      const response = await fetch("/api/v1/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        signal: controller.signal,
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        onEvent({
          type: "error",
          message: err.detail || `Server error ${response.status}`,
        });
        return;
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop(); // keep incomplete line

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            try {
              const event = JSON.parse(line.slice(6));
              onEvent(event);
            } catch {
              // skip malformed JSON
            }
          }
        }
      }
    } catch (err) {
      if (err.name !== "AbortError") {
        onEvent({ type: "error", message: err.message });
      }
    }
  })();

  return controller; // caller can abort via controller.abort()
}

/**
 * GET /api/v1/styles — Fetch available art styles.
 */
export async function fetchStyles() {
  const { data } = await api.get("/styles");
  return data;
}

export default api;
