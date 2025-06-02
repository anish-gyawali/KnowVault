import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import FileUpload from "./components/FileUpload";
import ChatBox from "./components/ChatBox";

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50 text-gray-900 flex flex-col">
        <Navbar />
        <main className="flex-1 py-10 px-4">
          <Routes>
            <Route path="/" element={<FileUpload />} />
            <Route path="/search" element={<ChatBox />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}
