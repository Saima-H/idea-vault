"use client";

import { useState, useEffect } from "react";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export default function TestRLS() {
  const [user, setUser] = useState<any>(null);
  const [scripts, setScripts] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      // 1. Check who is logged in
      const { data: { user } } = await supabase.auth.getUser();
      setUser(user);

      if (!user) {
        setError("You are not logged in. Please go to the login page first.");
        return;
      }

      // 2. Fetch directly from the database (Bypassing FastAPI entirely!)
      // The Supabase client automatically attaches the user's JWT to this request.
      const { data, error } = await supabase.from("answer_scripts").select("*");
      
      if (error) {
        setError(error.message);
      } else {
        setScripts(data || []);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="p-8 bg-gray-900 text-white min-h-screen">
      <h1 className="text-2xl font-bold mb-4">RLS Direct Database Test</h1>
      
      <div className="mb-4 p-4 bg-gray-800 rounded">
        <p><strong>Logged in as:</strong> {user?.email || "Not logged in"}</p>
      </div>

      {error && <p className="text-red-500 mb-4">{error}</p>}

      <h2 className="text-xl font-bold mb-2">Answer Scripts returned from DB: {scripts.length}</h2>
      
      <div className="space-y-2">
        {scripts.map((script) => (
          <div key={script.id} className="p-3 bg-gray-800 rounded border border-gray-700">
            <p>Script ID: {script.id}</p>
            <p>Student ID: {script.student_id}</p>
            <p>Status: {script.status}</p>
          </div>
        ))}
      </div>
    </div>
  );
}