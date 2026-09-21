import {
  Bot,
  Send,
  ShieldCheck,
} from "lucide-react";

import DashboardLayout from "../layouts/DashboardLayout";
import PageHeader from "../components/common/PageHeader";

export default function AIChat() {
  return (
    <DashboardLayout>
      <div className="mx-auto max-w-5xl space-y-6">
        <PageHeader
          eyebrow="AI SECURITY"
          title="AI Security Assistant"
          description="Analyze security events, logs, vulnerabilities, and CVEs with AI-assisted security analysis."
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
                Security analysis engine ready
              </p>
            </div>
          </div>

          <div className="flex min-h-[450px] items-center justify-center p-6">
            <div className="max-w-md text-center">
              <ShieldCheck className="mx-auto h-10 w-10 text-[#00F0FF]/40" />

              <h2 className="mt-4 text-sm font-semibold text-white">
                Ask a Security Question
              </h2>

              <p className="mt-2 text-xs leading-6 text-gray-500">
                Analyze logs, explain CVEs, understand vulnerabilities,
                or request defensive remediation guidance.
              </p>
            </div>
          </div>

          <div className="border-t border-white/10 p-4">
            <div className="flex gap-3">
              <textarea
                rows={2}
                placeholder="Ask CyberShield AI about a security event..."
                className="flex-1 resize-none rounded-lg border border-white/10 bg-[#0B0F17] px-4 py-3 text-sm text-white outline-none placeholder:text-gray-700 focus:border-[#00F0FF]/40"
              />

              <button
                className="self-end rounded-lg bg-[#00F0FF] p-3 text-[#0B0F17]"
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
