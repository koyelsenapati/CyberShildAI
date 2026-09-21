import {
  Lock,
  Settings as SettingsIcon,
  ShieldCheck,
} from "lucide-react";

import DashboardLayout from "../layouts/DashboardLayout";
import PageHeader from "../components/common/PageHeader";

export default function Settings() {
  return (
    <DashboardLayout>
      <div className="mx-auto max-w-5xl space-y-6">
        <PageHeader
          eyebrow="SYSTEM CONFIGURATION"
          title="Settings"
          description="Manage account security, application preferences, and security controls."
        />

        <div className="space-y-4">
          {[
            {
              icon: ShieldCheck,
              title: "Security Preferences",
              description:
                "Configure security monitoring and alert preferences.",
            },
            {
              icon: Lock,
              title: "Authentication & Access",
              description:
                "Manage authentication methods, sessions, and access controls.",
            },
            {
              icon: SettingsIcon,
              title: "Application Settings",
              description:
                "Configure dashboard and system preferences.",
            },
          ].map((item) => {
            const Icon = item.icon;

            return (
              <div
                key={item.title}
                className="flex items-center gap-4 rounded-xl border border-white/10 bg-[#1F2937]/60 p-5 transition hover:border-[#00F0FF]/20"
              >
                <div className="rounded-lg bg-[#00F0FF]/10 p-3">
                  <Icon className="h-5 w-5 text-[#00F0FF]" />
                </div>

                <div>
                  <h2 className="text-sm font-semibold text-white">
                    {item.title}
                  </h2>

                  <p className="mt-1 text-xs text-gray-500">
                    {item.description}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </DashboardLayout>
  );
}
