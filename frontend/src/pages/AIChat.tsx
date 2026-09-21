import { useState } from "react";
import { Bot, Send, ShieldCheck, User } from "lucide-react";

import DashboardLayout from "../layouts/DashboardLayout";
import PageHeader from "../components/common/PageHeader";
import { sendAIMessage } from "../services/aiAssistant";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function AIChat() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSend() {
    const value = message.trim();

    if (!value || loading) {
      return;
    }

    setError("");
    setMessage("");

    const userMessage: Message = {
      role: "user",
      content: value,
    };

    setMessages((current) => [...current, userMessage]);
    setLoading(true);

    try {
      const response = await sendAIMessage(value);

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: response.answer,
        },
      ]);
    } catch (err: any) {
      const detail =
        err?.response?.data?.detail ||
        "Unable to reach the AI backend.";

      setError(detail);
    } finally {
      setLoading(false);
    }
  }

  return (
    <DashboardLayout>
      <div className="mx-auto max-w-5xl space-y-6">
        <PageHeader
          eyebrow="AI SECURITY"
          title="AI Security Assistant"
          description="Analyze security events, logs, vulnerabilities, CVEs, and defensive remediation with the configured AI backend."
        />

        <div className="overflow-hidden rounded-xl border border-white/10 bg-[#1F2937]/60">
          <div className="flex items-center gap-3 border-b border-white/10 p-4">
            <div className="rounded-lg bg-[#00F0FF]/10 p-2">
              <Bot className="h-5 w-5 text-[#00F0FF]" />
            </div>

            <div>
              <p className="text-sm font-semibold text-white">
                CyberShield AI
              </p>

              <p className="text-[10px] text-[#10B981]">
                Real backend AI analysis
              </p>
            </div>
          </div>

          <div className="min-h-[450px] space-y-4 p-6">
            {messages.length === 0 && (
              <div className="flex min-h-[330px] items-center justify-center">
                <div className="max-w-md text-center">
                  <ShieldCheck className="mx-auto h-10 w-10 text-[#00F0FF]/40" />

                  <h2 className="mt-4 text-sm font-semibold text-white">
                    Ask a Security Question
                  </h2>

                  <p className="mt-2 text-xs leading-6 text-gray-500">
                    Ask about logs, CVEs, vulnerabilities, incidents,
                    detection logic, or defensive remediation.
                  </p>
                </div>
              </div>
            )}

            {messages.map((item, index) => (
              <div
                key={`${item.role}-${index}`}
                className={`flex gap-3 ${
                  item.role === "user"
                    ? "justify-end"
                    : "justify-start"
                }`}
              >
                {item.role === "assistant" && (
                  <div className="rounded-lg bg-[#00F0FF]/10 p-2">
                    <Bot className="h-4 w-4 text-[#00F0FF]" />
                  </div>
                )}

                <div
                  className={`max-w-[80%] rounded-lg px-4 py-3 text-xs leading-6 ${
                    item.role === "user"
                      ? "bg-[#00F0FF]/10 text-white"
                      : "bg-[#0B0F17] text-gray-300"
                  }`}
                >
                  {item.content}
                </div>

                {item.role === "user" && (
                  <div className="rounded-lg bg-white/5 p-2">
                    <User className="h-4 w-4 text-gray-400" />
                  </div>
                )}
              </div>
            ))}

            {loading && (
              <div className="flex items-center gap-3 text-xs text-gray-500">
                <Bot className="h-4 w-4 text-[#00F0FF]" />
                AI is analyzing...
              </div>
            )}

            {error && (
              <div className="rounded-lg border border-[#EF4444]/20 bg-[#EF4444]/5 px-4 py-3 text-xs text-[#EF4444]">
                {error}
              </div>
            )}
          </div>

          <div className="border-t border-white/10 p-4">
            <div className="flex gap-3">
              <textarea
                rows={2}
                value={message}
                onChange={(event) =>
                  setMessage(event.target.value)
                }
                onKeyDown={(event) => {
                  if (
                    event.key === "Enter" &&
                    !event.shiftKey
                  ) {
                    event.preventDefault();
                    void handleSend();
                  }
                }}
                disabled={loading}
                placeholder="Ask CyberShield AI about a security event..."
                className="flex-1 resize-none rounded-lg border border-white/10 bg-[#0B0F17] px-4 py-3 text-sm text-white outline-none placeholder:text-gray-700 focus:border-[#00F0FF]/40 disabled:opacity-50"
              />

              <button
                onClick={() => void handleSend()}
                disabled={loading || !message.trim()}
                className="self-end rounded-lg bg-[#00F0FF] p-3 text-[#0B0F17] disabled:cursor-not-allowed disabled:opacity-40"
                aria-label="Send message"
              >
                <Send className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
