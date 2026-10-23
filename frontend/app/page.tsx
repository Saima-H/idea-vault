"use client";

import { useState } from "react";
import { createClient } from "@supabase/supabase-js";
import { useRouter } from "next/navigation";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // 1. Talk to Supabase Auth
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    // 2. Handle the result
    if (error) {
      alert(error.message); // Show error if wrong password
    } else {
      // 3. THE REDIRECT: Send them to the dashboard
      router.push("/dashboard"); 
    }
  };

  return (
    <main className="min-h-screen bg-gray-900 flex items-center justify-center p-8">
      <form onSubmit={handleLogin} className="bg-gray-800 p-8 rounded-lg shadow-lg w-full max-w-md">
        <h1 className="text-3xl font-bold text-blue-400 mb-6 text-center">Login to Idea Vault</h1>
        
        <div className="mb-4">
          <label className="block text-gray-400 mb-2">Email</label>
          <input
            type="email"
            className="w-full bg-gray-700 text-white p-3 rounded focus:outline-none"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="mb-6">
          <label className="block text-gray-400 mb-2">Password</label>
          <input
            type="password"
            className="w-full bg-gray-700 text-white p-3 rounded focus:outline-none"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded">
          Login
        </button>
      </form>
    </main>
  );
}