import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-gray-900 text-white px-6 py-4 shadow">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        <h1 className="text-2xl font-bold">KnowVault</h1>
        <div className="space-x-4">
          <Link to="/" className="hover:text-gray-300">Upload</Link>
          <Link to="/search" className="hover:text-gray-300">Search</Link>
        </div>
      </div>
    </nav>
  );
}
