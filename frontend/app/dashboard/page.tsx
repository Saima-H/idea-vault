"use client";

import { useState, useEffect } from "react";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

interface Idea {
  id: number;
  content: string;
  url: string | null;
  tags: string | null;
}

export default function Dashboard() {
  const [ideas, setIdeas] = useState<Idea[]>([]);
  const [content, setContent] = useState("");
  const [url, setUrl] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [userEmail, setUserEmail] = useState<string | null>(null);

  // 1. Check who is logged in
  useEffect(() => {
    const getUser = async () => {
      const { data: { user } } = await supabase.auth.getUser();
      if (user && user.email) {
        setUserEmail(user.email);
      } else {
        window.location.href = "/"; // Kick them out if not logged in
      }
    };
    getUser();
  }, []);

  // 2. Fetch ideas for this specific user
  const fetchIdeas = async () => {
    if (!userEmail) return;
    
    const { data: { session } } = await supabase.auth.getSession();
    const token = session?.access_token;

    try {
      const response = await fetch(`http://127.0.0.1:8000/ideas`, {
        headers: {
          "Authorization": `Bearer ${token}`,
        }
      });
      const data = await response.json();
      setIdeas(data);
    } catch (error) {
      console.error("Failed to fetch ideas:", error);
    }
  };

  useEffect(() => {
    if (userEmail) fetchIdeas();
  }, [userEmail]);

  // 3. Add a new idea
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!content || !userEmail) return;

    const { data: { session } } = await supabase.auth.getSession();
    const token = session?.access_token;

    setIsLoading(true);
    try {
      await fetch("http://127.0.0.1:8000/ideas", {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ user_id: userEmail, content, url: url || null }),
      });
      
      setContent("");
      setUrl("");
      await fetchIdeas();
    } catch (error) {
      console.error("Failed to add idea:", error);
    } finally {
      setIsLoading(false);
    }
  };

  // 4. Log Out Function
  const handleLogout = async () => {
    await supabase.auth.signOut();
    window.location.href = "/";
  };

  if (!userEmail) return <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">Loading...</div>;

  return (
    <main className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-3xl mx-auto">
        
        {/* HEADER WITH LOGOUT BUTTON */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold text-blue-400">💡 Idea Vault</h1>
          <div className="flex items-center gap-4">
            <span className="text-gray-400 text-sm">Logged in as: {userEmail}</span>
            <button 
              onClick={handleLogout} 
              className="bg-red-600 hover:bg-red-700 text-white px-4 py-1 rounded text-sm transition"
            >
              Log Out
            </button>
          </div>
        </div>

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
                    <a href={idea.url} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline text-sm break-all block mb-3">
                      {idea.url}
                    </a>
                  )}

                  {idea.tags && (
                    <div className="flex flex-wrap gap-2 mt-3">
                      {idea.tags.split(", ").map((tag, index) => (
                        <span key={index} className="bg-blue-900 text-blue-200 text-xs px-2 py-1 rounded-full border border-blue-700">
                          #{tag}
                        </span>
                      ))}
                    </div>
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