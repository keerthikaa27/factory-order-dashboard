import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import apiClient from "../api/client";

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("admin@test.com");
  const [password, setPassword] = useState("123456");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const response = await apiClient.post("/auth/login", { email, password });
localStorage.setItem("access_token", response.data.access_token);
navigate("/"); 

    } catch (err: any) {
      console.error(err);
      setError(err?.response?.data?.detail || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#f6efe6]">
      <div className="card w-full max-w-md">
        <h1 className="heading text-2xl mb-1 text-center">
          Factory Access Portal
        </h1>
        <p className="text-xs text-center text-slate-500 mb-6">
          Sign in to view order analytics and dashboards
        </p>

        {error && (
          <div className="mb-4 text-xs text-red-700 bg-red-50 border border-red-200 px-3 py-2 rounded-lg">
            {error}
          </div>
        )}
        

        <form onSubmit={handleSubmit} className="space-y-4 text-sm">
          <div>
            <label className="block text-xs mb-1">Email</label>
            <input
              type="email"
              className="input w-full"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
            />
          </div>

          <div>
            <label className="block text-xs mb-1">Password</label>
            <input
              type="password"
              className="input w-full"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>
          <p className="text-sm text-center mt-4">
  Internal tool – accounts are created by the administrator.{" "}
  <a href="/register" className="text-brown-700 font-semibold hover:underline">
  </a>
</p>


          <button
            type="submit"
            disabled={loading}
            className="btn-primary w-full justify-center flex"
          >
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
