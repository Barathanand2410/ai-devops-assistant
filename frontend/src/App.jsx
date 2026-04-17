import { useState, useEffect } from "react";
import axios from "axios";
import logo from "./assets/logo.png";

function App() {
const API = "https://devops-backend-139813555989.asia-south1.run.app";
  const [loading, setLoading] = useState(false);
  const [explainLoading, setExplainLoading] = useState(false);
  const [fixLoading, setFixLoading] = useState(false);

  const [query, setQuery] = useState("");
  const [errorInput, setErrorInput] = useState("");
  const [history, setHistory] = useState([]);
  const [messages, setMessages] = useState([]);

  const [tool, setTool] = useState("github");
  const [activeTab, setActiveTab] = useState("explain");

  const [explanation, setExplanation] = useState("");
  const [fixResult, setFixResult] = useState("");

  const latestScript =
    messages.filter((msg) => msg.type === "bot").slice(-1)[0]?.text || "";

  const handleNewChat = () => {
    setMessages([]);
    setQuery("");
    setErrorInput("");
    setExplanation("");
    setFixResult("");
    setActiveTab("explain");
  };

  const handleGenerate = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setMessages((prev) => [
      ...prev,
      { type: "user", text: query },
      { type: "bot", text: "Generating..." }
    ]);

    try {
      const res = await axios.post(`${API}/ai/devops-query`, {
        query,
        tool
      });

      setMessages((prev) => {
        const updated = [...prev];
        updated.pop();
        return [...updated, { type: "bot", text: res.data.generated_script }];
      });

      setHistory((prev) => [
        {
          id: res.data.id,
          query,
          response: res.data.generated_script
        },
        ...prev
      ]);

      setQuery("");
      setExplanation("");
      setFixResult("");
    } catch (err) {
      console.error(err);
      setMessages((prev) => {
        const updated = [...prev];
        updated.pop();
        return [...updated, { type: "bot", text: "Generation failed ❌" }];
      });
    }

    setLoading(false);
  };

  const handleExplain = async () => {
    if (!latestScript.trim()) return;

    setExplainLoading(true);
    setActiveTab("explain");
    setExplanation("Explaining...");

    try {
      const res = await axios.post(`${API}/ai/explain`, {
        script: latestScript
      });
      setExplanation(res.data.explanation);
    } catch (err) {
      console.error(err);
      setExplanation("Explain failed ❌");
    }

    setExplainLoading(false);
  };

  const handleFixError = async () => {
    if (!errorInput.trim()) {
      alert("Please enter pipeline error");
      return;
    }

    setFixLoading(true);
    setActiveTab("fix");
    setFixResult("Fixing error...");

    try {
      const res = await axios.post(`${API}/ai/fix-error`, {
        error: errorInput
      });
      setFixResult(res.data.solution);
    } catch (err) {
      console.error(err);
      setFixResult("Fix failed ❌");
    }

    setFixLoading(false);
  };

  const fetchHistory = async () => {
    try {
      const res = await axios.get(`${API}/ai/history`);
      const sorted = res.data.sort((a, b) => b.id - a.id);
      setHistory(sorted);
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`${API}/ai/query/${id}`);
      setHistory((prev) => prev.filter((item) => item.id !== id));
    } catch (err) {
      console.error(err);
    }
  };

  const handleDownload = (id) => {
    window.open(`${API}/ai/download/${id}`, "_blank");
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div className="flex h-screen font-sans bg-gray-50">
      {/* SIDEBAR */}
      <div
        className="w-1/4 text-white flex flex-col"
        style={{
          background: "linear-gradient(180deg, #1973b8, #4ea749)"
        }}
      >
        <div className="bg-white py-3 flex justify-center items-center shadow">
          <img
            src={logo}
            alt="Company Logo"
            className="h-12 object-contain"
          />
        </div>

        <div className="p-4 flex flex-col gap-3 border-b border-white/20">
          <button
            onClick={handleNewChat}
            className="w-full py-2 px-3 rounded-lg bg-white text-[#1973b8] font-semibold shadow hover:bg-gray-100 transition"
          >
            + New Chat
          </button>
        </div>

        <div className="p-4 overflow-y-auto flex-1">
          <h2 className="text-lg font-semibold mb-3">History</h2>

          {history.map((item) => (
            <div
              key={item.id}
              className="p-2 mb-2 rounded-md bg-white/10 hover:bg-white/20 transition"
            >
              <p
                className="cursor-pointer text-xs leading-5 line-clamp-2"
                onClick={() =>
                  setMessages([{ type: "bot", text: item.response }])
                }
              >
                {item.query}
              </p>

              <div className="flex gap-3 mt-1 text-[11px]">
                <button
                  onClick={() => handleDelete(item.id)}
                  className="text-red-200 hover:text-red-400"
                >
                  Delete
                </button>

                <button
                  onClick={() => handleDownload(item.id)}
                  className="text-green-200 hover:text-green-400"
                >
                  Download
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* MAIN */}
      <div className="flex-1 p-6 flex flex-col overflow-hidden">
        <div
          className="text-3xl font-bold mb-4 text-white p-4 rounded-lg shadow"
          style={{
            background: "linear-gradient(90deg, #1973b8, #4ea749)"
          }}
        >
          AI DevOps Assistant
        </div>

        <div
          className="p-1 rounded mb-4 w-60 shadow"
          style={{
            background: "linear-gradient(90deg, #1973b8, #4ea749)"
          }}
        >
          <select
            value={tool}
            onChange={(e) => setTool(e.target.value)}
            className="w-full p-2 rounded text-black bg-white outline-none"
          >
            <option value="github">GitHub Actions</option>
            <option value="jenkins">Jenkins</option>
            <option value="gitlab">GitLab CI</option>
          </select>
        </div>

        <div className="flex gap-4 flex-1 overflow-hidden">
          {/* LEFT */}
          <div className="w-1/2 bg-white rounded-lg shadow-inner p-4 overflow-y-auto">
            <h2 className="text-lg font-semibold mb-3 text-gray-700">
              Generated Script
            </h2>

            {messages.length === 0 && (
              <p className="text-gray-400">Start asking something...</p>
            )}

            {messages.map((msg, index) => (
              <div
                key={index}
                className={`mb-3 ${
                  msg.type === "user" ? "text-right" : "text-left"
                }`}
              >
                <div
                  className="inline-block p-3 rounded-xl max-w-[80%] shadow"
                  style={
                    msg.type === "user"
                      ? { background: "#1973b8", color: "white" }
                      : { background: "#1a1a1a", color: "#4ea749" }
                  }
                >
                  <pre className="whitespace-pre-wrap text-sm">{msg.text}</pre>
                </div>
              </div>
            ))}
          </div>

          {/* RIGHT */}
          <div className="w-1/2 flex flex-col bg-white rounded-lg shadow-inner overflow-hidden">
            <div className="flex border-b bg-gray-100">
              <button
                onClick={() => setActiveTab("explain")}
                className={`px-4 py-3 font-medium ${
                  activeTab === "explain"
                    ? "border-b-2 border-blue-600 text-blue-600 bg-white"
                    : "text-gray-600"
                }`}
              >
                Explain
              </button>
              <button
                onClick={() => setActiveTab("fix")}
                className={`px-4 py-3 font-medium ${
                  activeTab === "fix"
                    ? "border-b-2 border-green-600 text-green-600 bg-white"
                    : "text-gray-600"
                }`}
              >
                Fix Error
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-4">
              {activeTab === "explain" && (
                <div className="h-full flex flex-col">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-lg font-semibold text-gray-700">
                      Explanation
                    </h3>
                    <button
                      onClick={handleExplain}
                      className="px-4 py-2 rounded-lg text-white shadow"
                      style={{ background: "#1973b8" }}
                    >
                      {explainLoading ? "Explaining..." : "Explain"}
                    </button>
                  </div>

                  <div className="flex-1 bg-yellow-50 border border-yellow-200 rounded-lg p-4 overflow-y-auto">
                    <p className="whitespace-pre-wrap text-sm text-gray-800">
                      {explanation || "Click Explain to view script explanation."}
                    </p>
                  </div>
                </div>
              )}

              {activeTab === "fix" && (
                <div className="h-full flex flex-col">
                  <h3 className="text-lg font-semibold text-gray-700 mb-3">
                    Fix Pipeline Error
                  </h3>

                  <textarea
                    className="w-full p-3 border rounded-lg shadow-sm mb-3"
                    rows="4"
                    placeholder="Paste pipeline error here..."
                    value={errorInput}
                    onChange={(e) => setErrorInput(e.target.value)}
                  />

                  <div className="mb-3">
                    <button
                      onClick={handleFixError}
                      className="px-4 py-2 rounded-lg text-white shadow"
                      style={{ background: "#4ea749" }}
                    >
                      {fixLoading ? "Fixing..." : "Fix Error"}
                    </button>
                  </div>

                  <div className="flex-1 bg-red-50 border border-red-200 rounded-lg p-4 overflow-y-auto">
                    <p className="whitespace-pre-wrap text-sm text-gray-800">
                      {fixResult || "Enter an error and click Fix Error."}
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="mt-4">
          <textarea
            className="w-full p-3 border rounded-lg mb-3 shadow-sm"
            rows="3"
            placeholder="Ask: Create CI/CD pipeline for Node.js with Docker"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />

          <button
            onClick={handleGenerate}
            className="px-5 py-2 rounded-lg text-white shadow"
            style={{
              background: "linear-gradient(90deg, #1973b8, #4ea749)"
            }}
          >
            {loading ? "Generating..." : "Generate"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;