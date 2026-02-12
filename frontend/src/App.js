import { useState } from "react";

const API_BASE_URL = (process.env.REACT_APP_API_URL || "http://127.0.0.1:8000").replace(/\/+$/, "");

function App() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");

  const askQuestion = async () => {
    if (!question) return;
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API_BASE_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      if (!res.ok) {
        const message = await res.text();
        throw new Error(message || `Request failed with status ${res.status}`);
      }

      const data = await res.json();
      setChatHistory((prev) => [...prev, { q: question, a: data.answer }]);
      setQuestion("");
    } catch (err) {
      setError(err.message || "Failed to ask question.");
    } finally {
      setLoading(false);
    }
  };

  const uploadFile = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    setError("");
    try {
      const res = await fetch(`${API_BASE_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const message = await res.text();
        throw new Error(message || `Upload failed with status ${res.status}`);
      }
    } catch (err) {
      setError(err.message || "File upload failed.");
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial", display: "flex", height: "100vh" }}>
      <div style={{ flex: 1, paddingRight: "20px" }}>
        <h1>Enterprise AI Knowledge Assistant</h1>

        <div style={{ marginBottom: "20px" }}>
          <h3>Upload Document</h3>
          <input type="file" onChange={(e) => setFile(e.target.files[0])} />
          <button onClick={uploadFile}>Upload</button>
        </div>

        <div style={{ height: "60vh", overflowY: "auto", border: "1px solid #ccc", padding: "10px" }}>
          {chatHistory.map((item, i) => (
            <div key={i} style={{ marginBottom: "10px" }}>
              <strong>You:</strong> {item.q}
              <br />
              <strong>AI:</strong> {item.a}
            </div>
          ))}
        </div>

        <textarea
          rows="3"
          style={{ width: "100%", padding: "10px", marginTop: "10px" }}
          placeholder="Ask a question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        {error && <p style={{ color: "red", marginTop: "8px" }}>{error}</p>}
        <button onClick={askQuestion} style={{ marginTop: "10px", padding: "10px" }} disabled={loading}>
          {loading ? "Thinking..." : "Ask"}
        </button>
      </div>
    </div>
  );
}

export default App;
