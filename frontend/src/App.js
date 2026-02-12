import { useState } from "react";
import "./App.css";

const API_BASE_URL = (process.env.REACT_APP_API_URL || "http://127.0.0.1:8000").replace(/\/+$/, "");

function App() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");

  const askQuestion = async () => {
    if (!question) return;
    setLoading(true);
    setError("");
    setStatus("");
    const currentQuestion = question.trim();
    if (!currentQuestion) {
      setLoading(false);
      return;
    }

    setChatHistory((prev) => [...prev, { q: currentQuestion, a: "", pending: true }]);

    try {
      const res = await fetch(`${API_BASE_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: currentQuestion }),
      });

      if (!res.ok) {
        const message = await res.text();
        throw new Error(message || `Request failed with status ${res.status}`);
      }

      const data = await res.json();
      setChatHistory((prev) =>
        prev.map((item, idx) =>
          idx === prev.length - 1 ? { q: currentQuestion, a: data.answer, pending: false } : item
        )
      );
      setQuestion("");
    } catch (err) {
      setChatHistory((prev) =>
        prev.map((item, idx) =>
          idx === prev.length - 1 ? { ...item, a: "Failed to get response.", pending: false } : item
        )
      );
      setError(err.message || "Failed to ask question.");
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0] || null;
    setFile(selectedFile);
    setError("");
    if (selectedFile) {
      const sizeKb = Math.max(1, Math.round(selectedFile.size / 1024));
      setStatus(`Selected: ${selectedFile.name} (${sizeKb} KB)`);
    } else {
      setStatus("");
    }
  };

  const uploadFile = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    setError("");
    setStatus("Uploading file...");
    setUploading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const message = await res.text();
        throw new Error(message || `Upload failed with status ${res.status}`);
      }

      const data = await res.json();
      setStatus(data.message || "Upload completed.");
    } catch (err) {
      setError(err.message || "File upload failed.");
      setStatus("");
    } finally {
      setUploading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      if (!loading) {
        askQuestion();
      }
    }
  };

  return (
    <div className="app-shell">
      <div className="orb orb-one" />
      <div className="orb orb-two" />
      <main className="app-frame">
        <header className="app-header">
          <div>
            <p className="kicker">Enterprise Assistant</p>
            <h1>Knowledge Copilot</h1>
          </div>
          <span className="api-tag">{API_BASE_URL}</span>
        </header>

        <section className="upload-panel">
          <label className="upload-label">Document Ingestion</label>
          <div className="upload-row">
            <input type="file" className="file-input" onChange={handleFileChange} />
            <button className="btn btn-secondary" onClick={uploadFile} disabled={!file || uploading}>
              {uploading ? "Uploading..." : "Upload & Index"}
            </button>
          </div>
          {status && <p className="status">{status}</p>}
          {error && <p className="error">{error}</p>}
        </section>

        <div className="chat-window">
          {chatHistory.length === 0 && (
            <div className="empty-state">
              <h2>Ask anything about your enterprise docs</h2>
              <p>Upload a file, then ask policy, engineering, or operational questions.</p>
            </div>
          )}

          {chatHistory.map((item, i) => (
            <article key={i} className="chat-card">
              <div className="question">
                <span>You</span>
                <p>{item.q}</p>
              </div>
              <div className="answer">
                <span>Assistant</span>
                {item.pending ? (
                  <p className="typing">Generating detailed answer...</p>
                ) : (
                  <p>{item.a}</p>
                )}
              </div>
            </article>
          ))}
        </div>

        <div className="composer">
          <textarea
            rows="3"
            className="composer-input"
            placeholder="Ask a question... Press Enter to send"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <button className="btn btn-primary" onClick={askQuestion} disabled={loading || !question.trim()}>
            {loading ? "Thinking..." : "Ask"}
          </button>
        </div>
      </main>
    </div>
  );
}

export default App;
