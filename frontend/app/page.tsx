"use client"; // This tells Next.js this file runs in the browser

import { useState, useEffect } from "react";

// 1. Define the TypeScript interface (What an Idea looks like)
interface Idea {
  id: number;
  content: string;
  url: string | null;
}

export default function Home() {
  // 2. Set up State (Variables that update the screen)
  const [ideas, setIdeas] = useState<Idea[]>([]); // Array of ideas
  const [content, setContent] = useState("");     // The text input
  const [url, setUrl] = useState("");             // The URL input
  const [isLoading, setIsLoading] = useState(false);

  // 3. Fetch ideas from FastAPI
  const fetchIdeas = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/ideas");
      const data = await response.json();
      setIdeas(data);
    } catch (error) {
      console.error("Failed to fetch ideas:", error);
    }
  };

  // Run fetchIdeas once when the page loads
  useEffect(() => {
    fetchIdeas();
  }, []);

  // 4. Handle the form submission (Add a new idea)
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); // Stop page refresh
    if (!content) return; // Don't submit empty ideas

    setIsLoading(true);

    try {
      // Send data to FastAPI
      await fetch("http://127.0.0.1:8000/ideas", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ content, url: url || null }),
      });

      // Clear the form
      setContent("");
      setUrl("");
      
      // Refresh the list
      await fetchIdeas();
    } catch (error) {
      console.error("Failed to add idea:", error);
    } finally {
      setIsLoading(false);
    }
  };

  // 5. The UI (HTML + Tailwind CSS)
  return (
    <main className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-4xl font-bold text-blue-400 mb-8">💡 Idea Vault</h1>

        {/* ADD IDEA FORM */}
        <form onSubmit={handleSubmit} className="bg-gray-800 p-6 rounded-lg shadow-lg mb-8">
          <h2 className="text-xl font-semibold mb-4">Add a New Idea</h2>
          
          <div className="mb-4">
            <label className="block text-sm text-gray-400 mb-1">Idea Content</label>
            <textarea
              className="w-full bg-gray-700 text-white p-3 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
              placeholder="What's on your mind?"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              required
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm text-gray-400 mb-1">URL (Optional)</label>
            <input
              type="url"
              className="w-full bg-gray-700 text-white p-3 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="https://example.com"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded transition duration-200"
          >
            {isLoading ? "Saving..." : "Save Idea"}
          </button>
        </form>

        {/* IDEAS LIST */}
        <div>
          <h2 className="text-2xl font-semibold mb-4">Your Ideas ({ideas.length})</h2>
          
          {ideas.length === 0 ? (
            <p className="text-gray-400">No ideas yet. Add one above!</p>
          ) : (
            <div className="space-y-4">
              {ideas.map((idea) => (
                <div key={idea.id} className="bg-gray-800 p-5 rounded-lg border border-gray-700">
                  <p className="text-lg mb-2">{idea.content}</p>
                  
                  {idea.url && (
                    <a 
                      href={idea.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-blue-400 hover:underline text-sm break-all"
                    >
                      {idea.url}
                    </a>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </main>
  );
}