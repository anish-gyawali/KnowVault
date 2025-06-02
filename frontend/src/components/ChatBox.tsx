import { useState } from "react";
import { searchQuery } from "../api";

export default function ChatBox() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<
    { user: string; response: string; score: number }[]
  >([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!query) return;
    setLoading(true);
    try {
      const res = await searchQuery(query);
      if (res.matches.length === 0) {
        setMessages([
          ...messages,
          { user: query, response: "No results found.", score: 0 },
        ]);
      } else {
        const newMessages = res.matches.map((m: any) => ({
          user: query,
          response: m.chunk,
          score: m.score,
        }));
        setMessages([...messages, ...newMessages]);
      }
    } catch {
      setMessages([
        ...messages,
        { user: query, response: "Error searching. Try again.", score: 0 },
      ]);
    } finally {
      setLoading(false);
      setQuery("");
    }
  };

  return (
    <div className="bg-white shadow p-6 rounded w-full max-w-2xl mx-auto">
      <h2 className="text-xl font-semibold mb-4">Search Documents</h2>
      <div className="space-y-4 max-h-96 overflow-y-auto border p-4 rounded">
        {messages.length === 0 && (
          <p className="text-gray-500 text-center">No results yet.</p>
        )}
        {messages.map((m, i) => (
          <div key={i} className="border-b pb-2">
            <p className="font-semibold text-blue-700">You: {m.user}</p>
            <p className="ml-4 text-gray-700 whitespace-pre-line">{m.response}</p>
            {m.score > 0 && (
              <span className="ml-4 inline-block bg-green-100 text-green-700 text-xs px-2 py-1 rounded">
                Score: {m.score.toFixed(2)}
              </span>
            )}
          </div>
        ))}
      </div>
      <div className="mt-4 flex gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question..."
          className="flex-1 border px-3 py-2 rounded"
          disabled={loading}
        />
        <button
          onClick={handleSend}
          className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50"
          disabled={loading}
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </div>
    </div>
  );
}
