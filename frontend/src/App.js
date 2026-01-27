import { useState } from "react";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const [file, setFile] = useState(null);

  const askQuestion = async () => {
    if (!question) return;
    setLoading(true);
    const res = await fetch("http://127.0.0.1:8000/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    });
    const data = await res.json();
    setAnswer(data.answer);
    setChatHistory([...chatHistory, { q: question, a: data.answer }]);
    setQuestion("");
    setLoading(false);
  };

  const uploadFile = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData,
    });
    alert("File uploaded");
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
        <button onClick={askQuestion} style={{ marginTop: "10px", padding: "10px" }} disabled={loading}>
          {loading ? "Thinking..." : "Ask"}
        </button>
      </div>
    </div>
  );
}

export default App;
