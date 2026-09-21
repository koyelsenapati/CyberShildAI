import { useState } from "react";
import type { FormEvent } from "react";
import { Eye, EyeOff, LockKeyhole, ShieldCheck, UserRound } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { loginUser } from "../services/auth";
import { useAuthStore } from "../store/authStore";

export default function Login() {
  const navigate = useNavigate();
  const login = useAuthStore((state) => state.login);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");

    if (!email || !password) {
      setError("Email and password are required.");
      return;
    }

    setLoading(true);
    try {
      const response = await loginUser({ email, password });
      login(response.user, response.access_token);
      navigate("/dashboard", { replace: true });
    } catch (loginError) {
      const detail = typeof loginError === "object" && loginError !== null &&
        "response" in loginError
        ? (loginError.response as { data?: { detail?: string } }).data?.detail
        : undefined;
      setError(detail ?? "Authentication failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center bg-[#0B0F17] px-4 text-white">
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute left-1/2 top-1/2 h-96 w-96 -translate-x-1/2 -translate-y-1/2 rounded-full bg-[#00F0FF]/5 blur-3xl" />
      </div>
      <div className="relative w-full max-w-md">
        <div className="mb-8 text-center">
          <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl border border-[#00F0FF]/20 bg-[#00F0FF]/10">
            <ShieldCheck className="h-7 w-7 text-[#00F0FF]" />
          </div>
          <h1 className="text-2xl font-bold">CyberShield <span className="text-[#00F0FF]">AI</span></h1>
          <p className="mt-2 text-sm text-gray-500">Advanced Defensive Cybersecurity Platform</p>
        </div>
        <div className="rounded-2xl border border-white/10 bg-[#111827]/90 p-6 shadow-2xl backdrop-blur md:p-8">
          <div className="mb-6">
            <h2 className="text-lg font-semibold">Secure Sign In</h2>
            <p className="mt-1 text-xs text-gray-500">Authenticate to access the Security Operations Center.</p>
          </div>
          {error && <div className="mb-5 rounded-lg border border-[#EF4444]/20 bg-[#EF4444]/10 px-4 py-3 text-xs text-[#EF4444]">{error}</div>}
          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label htmlFor="email" className="mb-2 block text-xs font-medium text-gray-400">Email Address</label>
              <div className="relative">
                <UserRound className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-600" />
                <input id="email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="Enter your email address" autoComplete="email" className="w-full rounded-lg border border-white/10 bg-[#0B0F17] py-3 pl-10 pr-4 text-sm text-white outline-none transition placeholder:text-gray-700 focus:border-[#00F0FF]/50" />
              </div>
            </div>
            <div>
              <label htmlFor="password" className="mb-2 block text-xs font-medium text-gray-400">Password</label>
              <div className="relative">
                <LockKeyhole className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-600" />
                <input id="password" type={showPassword ? "text" : "password"} value={password} onChange={(event) => setPassword(event.target.value)} placeholder="Enter your password" autoComplete="current-password" className="w-full rounded-lg border border-white/10 bg-[#0B0F17] py-3 pl-10 pr-11 text-sm text-white outline-none transition placeholder:text-gray-700 focus:border-[#00F0FF]/50" />
                <button type="button" onClick={() => setShowPassword((current) => !current)} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-600 hover:text-gray-300" aria-label={showPassword ? "Hide password" : "Show password"}>
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>
            <button type="submit" disabled={loading} className="flex w-full items-center justify-center rounded-lg bg-[#00F0FF] px-4 py-3 text-sm font-semibold text-[#0B0F17] transition hover:bg-[#00F0FF]/90 disabled:cursor-not-allowed disabled:opacity-50">
              {loading ? "Authenticating..." : "Sign In"}
            </button>
          </form>
          <div className="mt-6 flex items-center justify-center gap-2 text-[10px] text-gray-600"><LockKeyhole className="h-3 w-3" />Secure authentication channel</div>
        </div>
      </div>
    </main>
  );
}
