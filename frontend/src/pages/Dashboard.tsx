import { useEffect, useState } from "react";
import {
  Activity,
  AlertTriangle,
  ArrowUpRight,
  Bug,
  CheckCircle2,
  Shield,
  ShieldAlert,
  Wifi,
} from "lucide-react";

import DashboardLayout from "../layouts/DashboardLayout";
import PageHeader from "../components/common/PageHeader";
import {
  getDashboardStatistics,
  type DashboardStatistics,
} from "../services/dashboard";

function MetricCard({
  title,
  value,
  subtitle,
  icon: Icon,
  danger = false,
}: {
  title: string;
  value: string | number;
  subtitle: string;
  icon: typeof Shield;
  danger?: boolean;
}) {
  return (
    <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-5 transition hover:border-[#00F0FF]/20">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs text-gray-500">{title}</p>

          <p
            className={`mt-3 font-mono text-3xl font-bold ${
              danger ? "text-[#EF4444]" : "text-white"
            }`}
          >
            {value}
          </p>

          <p className="mt-2 text-[10px] text-gray-600">
            {subtitle}
          </p>
        </div>

        <div className="rounded-lg bg-[#00F0FF]/10 p-3">
          <Icon className="h-5 w-5 text-[#00F0FF]" />
        </div>
      </div>
    </div>
  );
}

export default function Dashboard() {
  const [stats, setStats] =
    useState<DashboardStatistics | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  useEffect(() => {
    let mounted = true;

    async function loadDashboard() {
      try {
        setLoading(true);
        setError("");

        const data =
          await getDashboardStatistics();

        if (mounted) {
          setStats(data);
        }
      } catch {
        if (mounted) {
          setError(
            "Unable to connect to the CyberShield backend.",
          );
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    }

    loadDashboard();

    return () => {
      mounted = false;
    };
  }, []);

  return (
    <DashboardLayout>
      <div className="mx-auto max-w-[1600px] space-y-6">
        <PageHeader
          eyebrow="SECURITY OPERATIONS CENTER"
          title="Security Dashboard"
          description="Real-time security visibility, threat monitoring, and vulnerability intelligence."
        />

        {loading && (
          <div className="rounded-xl border border-white/10 bg-[#1F2937]/40 p-10 text-center">
            <Activity className="mx-auto h-7 w-7 animate-pulse text-[#00F0FF]" />

            <p className="mt-4 text-xs text-gray-500">
              Loading security telemetry...
            </p>
          </div>
        )}

        {!loading && error && (
          <div className="rounded-xl border border-[#EF4444]/20 bg-[#EF4444]/5 p-5">
            <div className="flex items-center gap-3">
              <ShieldAlert className="h-5 w-5 text-[#EF4444]" />

              <div>
                <p className="text-sm font-semibold text-white">
                  Backend Connection Failed
                </p>

                <p className="mt-1 text-xs text-gray-500">
                  {error}
                </p>
              </div>
            </div>
          </div>
        )}

        {!loading && stats && (
          <>
            {/* Security Overview */}

            <section>
              <div className="mb-4 flex items-center justify-between">
                <div>
                  <p className="text-[10px] uppercase tracking-widest text-[#00F0FF]">
                    Overview
                  </p>

                  <h2 className="mt-1 text-sm font-semibold text-white">
                    Security Telemetry
                  </h2>
                </div>

                <div className="flex items-center gap-2 text-[10px] text-[#10B981]">
                  <span className="h-1.5 w-1.5 rounded-full bg-[#10B981]" />
                  SYSTEM ONLINE
                </div>
              </div>

              <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
                <MetricCard
                  title="Security Score"
                  value={`${stats.security_score}/100`}
                  subtitle="Overall security posture"
                  icon={Shield}
                />

                <MetricCard
                  title="Active Threats"
                  value={stats.threat_count}
                  subtitle="Detected security threats"
                  icon={ShieldAlert}
                  danger={stats.threat_count > 0}
                />

                <MetricCard
                  title="Security Alerts"
                  value={stats.alert_count}
                  subtitle="Requires analyst attention"
                  icon={AlertTriangle}
                  danger={stats.alert_count > 0}
                />

                <MetricCard
                  title="Vulnerabilities"
                  value={stats.vulnerability_count}
                  subtitle="Known security findings"
                  icon={Bug}
                  danger={stats.vulnerability_count > 0}
                />
              </div>
            </section>

            {/* Network Activity */}

            <section className="grid gap-6 lg:grid-cols-3">
              <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-5 lg:col-span-2">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-[10px] uppercase tracking-widest text-gray-600">
                      Network Monitoring
                    </p>

                    <h2 className="mt-1 text-sm font-semibold text-white">
                      Network Activity
                    </h2>
                  </div>

                  <Wifi className="h-5 w-5 text-[#00F0FF]" />
                </div>

                <div className="mt-8 grid gap-6 sm:grid-cols-2">
                  <div>
                    <p className="text-xs text-gray-500">
                      Packets / Second
                    </p>

                    <p className="mt-2 font-mono text-3xl font-bold text-white">
                      {stats.packets_per_second}
                    </p>

                    <div className="mt-4 h-1 overflow-hidden rounded-full bg-white/5">
                      <div
                        className="h-full rounded-full bg-[#00F0FF]"
                        style={{
                          width: `${Math.min(
                            stats.packets_per_second / 10,
                            100,
                          )}%`,
                        }}
                      />
                    </div>
                  </div>

                  <div>
                    <p className="text-xs text-gray-500">
                      Active Connections
                    </p>

                    <p className="mt-2 font-mono text-3xl font-bold text-white">
                      {stats.active_connections}
                    </p>

                    <p className="mt-3 text-[10px] text-gray-600">
                      Current monitored connections
                    </p>
                  </div>
                </div>
              </div>

              {/* Security Score */}

              <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-5">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-[10px] uppercase tracking-widest text-gray-600">
                      Security Posture
                    </p>

                    <h2 className="mt-1 text-sm font-semibold text-white">
                      Security Score
                    </h2>
                  </div>

                  <CheckCircle2 className="h-5 w-5 text-[#10B981]" />
                </div>

                <div className="mt-8 flex items-end gap-2">
                  <span className="font-mono text-5xl font-bold text-white">
                    {stats.security_score}
                  </span>

                  <span className="mb-2 text-xs text-gray-600">
                    /100
                  </span>
                </div>

                <div className="mt-5 h-2 overflow-hidden rounded-full bg-white/5">
                  <div
                    className="h-full rounded-full bg-[#10B981]"
                    style={{
                      width: `${Math.min(
                        Math.max(stats.security_score, 0),
                        100,
                      )}%`,
                    }}
                  />
                </div>

                <p className="mt-3 text-[10px] text-gray-600">
                  Overall defensive security posture.
                </p>
              </div>
            </section>

            {/* Vulnerability Overview */}

            <section className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-5">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-[10px] uppercase tracking-widest text-gray-600">
                    Vulnerability Management
                  </p>

                  <h2 className="mt-1 text-sm font-semibold text-white">
                    Vulnerability Overview
                  </h2>
                </div>

                <ArrowUpRight className="h-5 w-5 text-gray-600" />
              </div>

              <div className="mt-6 grid gap-4 sm:grid-cols-3">
                <div className="rounded-lg border border-[#EF4444]/10 bg-[#EF4444]/5 p-4">
                  <p className="text-[10px] uppercase text-gray-500">
                    Critical
                  </p>

                  <p className="mt-2 font-mono text-2xl font-bold text-[#EF4444]">
                    {stats.critical_vulnerabilities}
                  </p>
                </div>

                <div className="rounded-lg border border-[#F59E0B]/10 bg-[#F59E0B]/5 p-4">
                  <p className="text-[10px] uppercase text-gray-500">
                    Total Findings
                  </p>

                  <p className="mt-2 font-mono text-2xl font-bold text-[#F59E0B]">
                    {stats.vulnerability_count}
                  </p>
                </div>

                <div className="rounded-lg border border-[#10B981]/10 bg-[#10B981]/5 p-4">
                  <p className="text-[10px] uppercase text-gray-500">
                    Monitoring
                  </p>

                  <p className="mt-2 font-mono text-2xl font-bold text-[#10B981]">
                    ACTIVE
                  </p>
                </div>
              </div>
            </section>
          </>
        )}
      </div>
    </DashboardLayout>
  );
}
