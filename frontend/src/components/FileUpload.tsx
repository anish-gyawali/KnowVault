import { useState } from "react";
import { uploadFile } from "../api";

export default function FileUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!file) return;
    setLoading(true);
    setStatus("");
    try {
      await uploadFile(file);
      setStatus("Upload successful!");
    } catch {
      setStatus("Upload failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white shadow p-6 rounded w-full max-w-2xl mx-auto">
      <h2 className="text-xl font-semibold mb-4">Upload Document</h2>
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
        <input
          type="file"
          accept=".txt,.pdf"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="flex-1 border border-gray-300 rounded px-3 py-2"
        />
        <button
          onClick={handleSubmit}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
          disabled={loading}
        >
          {loading ? "Uploading..." : "Upload"}
        </button>
      </div>
      {status && <p className="mt-2 text-sm text-gray-600">{status}</p>}
    </div>
  );
}
