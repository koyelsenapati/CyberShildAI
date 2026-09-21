import { useState } from "react";

import {
  Globe2,
  Hash,
  MapPin,
  Radar,
  Search,
  ShieldAlert,
  ShieldCheck,
} from "lucide-react";

import DashboardLayout from "../layouts/DashboardLayout";
import PageHeader from "../components/common/PageHeader";

import { lookupThreatIndicator } from "../services/threatIntel";

import type {
  IndicatorType,
  ThreatIndicator,
} from "../types/threatIntel";

function SeverityBadge({
  severity,
}: {
  severity: ThreatIndicator["severity"];
}) {
  const styles: Record<
    ThreatIndicator["severity"],
    string
  > = {
    CLEAN:
      "border-[#10B981]/20 bg-[#10B981]/5 text-[#10B981]",
    LOW:
      "border-[#10B981]/20 bg-[#10B981]/5 text-[#10B981]",
    MEDIUM:
      "border-[#F59E0B]/20 bg-[#F59E0B]/5 text-[#F59E0B]",
    HIGH:
      "border-[#EF4444]/20 bg-[#EF4444]/5 text-[#EF4444]",
    CRITICAL:
      "border-[#EF4444]/30 bg-[#EF4444]/10 text-[#EF4444]",
  };

  return (
    <span
      className={`rounded border px-2 py-1 text-[9px] font-semibold ${styles[severity]}`}
    >
      {severity}
    </span>
  );
}

function IndicatorIcon({
  type,
}: {
  type: IndicatorType;
}) {
  if (type === "IP") {
    return <Radar className="h-5 w-5" />;
  }

  if (type === "HASH") {
    return <Hash className="h-5 w-5" />;
  }

  return <Globe2 className="h-5 w-5" />;
}

export default function ThreatIntel() {
  const [indicator, setIndicator] = useState("");

  const [type, setType] =
    useState<IndicatorType>("IP");

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const [result, setResult] =
    useState<ThreatIndicator | null>(null);

  async function handleLookup() {
    const value = indicator.trim();

    if (!value) {
      setError("Enter an IP, domain, or file hash.");
      return;
    }

    setError("");
    setLoading(true);
    setResult(null);

    try {
      const response =
        await lookupThreatIndicator(value, type);

      setResult(response.indicator);
    } catch (error) {
      console.error(
        "Threat intelligence lookup failed:",
        error,
      );

      setError(
        "Unable to retrieve threat intelligence from the backend.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <DashboardLayout>
      <div className="mx-auto max-w-[1600px] space-y-6">
        <PageHeader
          eyebrow="THREAT INTELLIGENCE"
          title="Threat Intelligence"
          description="Investigate IP addresses, domains, file hashes, indicators of compromise, and threat reputation."
        />

        {/* Lookup */}
        <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-5">
          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-[#00F0FF]/10 p-2">
              <Radar className="h-5 w-5 text-[#00F0FF]" />
            </div>

            <div>
              <h2 className="text-sm font-semibold text-white">
                Indicator Investigation
              </h2>

              <p className="mt-1 text-xs text-gray-500">
                Search threat intelligence for a security indicator.
              </p>
            </div>
          </div>

          <div className="mt-5 grid gap-3 md:grid-cols-[160px_1fr_auto]">
            <select
              value={type}
              onChange={(event) => {
                setType(
                  event.target.value as IndicatorType,
                );
                setResult(null);
                setError("");
              }}
              disabled={loading}
              className="rounded-lg border border-white/10 bg-[#0B0F17] px-4 py-3 text-sm text-white outline-none focus:border-[#00F0FF]/40 disabled:opacity-50"
            >
              <option value="IP">
                IP Address
              </option>

              <option value="DOMAIN">
                Domain
              </option>

              <option value="HASH">
                File Hash
              </option>
            </select>

            <input
              value={indicator}
              onChange={(event) =>
                setIndicator(event.target.value)
              }
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                  handleLookup();
                }
              }}
              disabled={loading}
              placeholder={
                type === "IP"
                  ? "Enter IP address"
                  : type === "DOMAIN"
                    ? "Enter domain"
                    : "Enter SHA256 hash"
              }
              className="rounded-lg border border-white/10 bg-[#0B0F17] px-4 py-3 font-mono text-sm text-white outline-none placeholder:text-gray-700 focus:border-[#00F0FF]/40 disabled:opacity-50"
            />

            <button
              onClick={handleLookup}
              disabled={loading}
              className="flex items-center justify-center gap-2 rounded-lg bg-[#00F0FF] px-6 py-3 text-xs font-semibold text-[#0B0F17] transition hover:bg-[#00D9E8] disabled:cursor-not-allowed disabled:opacity-50"
            >
              <Search className="h-4 w-4" />

              {loading
                ? "Investigating..."
                : "Investigate"}
            </button>
          </div>

          {error && (
            <div className="mt-4 rounded-lg border border-[#EF4444]/20 bg-[#EF4444]/5 px-4 py-3">
              <p className="text-xs text-[#EF4444]">
                {error}
              </p>
            </div>
          )}
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex min-h-[300px] items-center justify-center rounded-xl border border-white/10 bg-[#1F2937]/40">
            <div className="text-center">
              <Radar className="mx-auto h-10 w-10 animate-pulse text-[#00F0FF]" />

              <p className="mt-4 text-sm font-semibold text-white">
                Investigating indicator...
              </p>

              <p className="mt-2 text-xs text-gray-500">
                Waiting for threat intelligence data from the backend.
              </p>
            </div>
          </div>
        )}

        {/* Result */}
        {result && !loading && (
          <>
            {/* Overview */}
            <div className="grid gap-4 lg:grid-cols-4">
              <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-5 lg:col-span-2">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex gap-3">
                    <div className="rounded-lg bg-[#00F0FF]/10 p-3 text-[#00F0FF]">
                      <IndicatorIcon
                        type={result.type}
                      />
                    </div>

                    <div>
                      <p className="text-[10px] uppercase tracking-wider text-gray-600">
                        {result.type} Indicator
                      </p>

                      <p className="mt-1 break-all font-mono text-sm text-white">
                        {result.indicator}
                      </p>
                    </div>
                  </div>

                  <SeverityBadge
                    severity={result.severity}
                  />
                </div>

                <p className="mt-5 text-xs leading-6 text-gray-400">
                  {result.description ||
                    "No additional description was provided by the threat intelligence provider."}
                </p>
              </div>

              {/* Reputation */}
              <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-5">
                <ShieldAlert
                  className={`h-5 w-5 ${
                    result.malicious
                      ? "text-[#EF4444]"
                      : "text-[#10B981]"
                  }`}
                />

                <p className="mt-4 text-xs text-gray-500">
                  Reputation
                </p>

                <p
                  className={`mt-1 text-xl font-bold ${
                    result.malicious
                      ? "text-[#EF4444]"
                      : "text-[#10B981]"
                  }`}
                >
                  {result.malicious
                    ? "MALICIOUS"
                    : "CLEAN"}
                </p>
              </div>

              {/* Confidence */}
              <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-5">
                <ShieldCheck className="h-5 w-5 text-[#00F0FF]" />

                <p className="mt-4 text-xs text-gray-500">
                  Confidence
                </p>

                <p className="mt-1 font-mono text-xl font-bold text-white">
                  {result.confidence}%
                </p>
              </div>
            </div>

            {/* Reputation Details */}
            <div className="grid gap-6 lg:grid-cols-3">
              <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-5">
                <p className="text-xs text-gray-500">
                  Reputation Score
                </p>

                <div className="mt-4 flex items-end gap-2">
                  <span className="font-mono text-4xl font-bold text-white">
                    {result.reputation_score}
                  </span>

                  <span className="mb-1 text-xs text-gray-600">
                    /100
                  </span>
                </div>

                <div className="mt-4 h-2 overflow-hidden rounded-full bg-white/5">
                  <div
                    className="h-full rounded-full bg-[#F59E0B]"
                    style={{
                      width: `${Math.min(
                        Math.max(
                          result.reputation_score,
                          0,
                        ),
                        100,
                      )}%`,
                    }}
                  />
                </div>

                <p className="mt-3 text-[10px] text-gray-600">
                  Reputation score returned by the intelligence provider.
                </p>
              </div>

              {/* Location */}
              <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-5">
                <div className="flex items-center gap-3">
                  <MapPin className="h-5 w-5 text-[#00F0FF]" />

                  <h2 className="text-sm font-semibold text-white">
                    Location
                  </h2>
                </div>

                <p className="mt-5 text-sm text-gray-400">
                  {result.country || "Not provided"}
                </p>
              </div>

              {/* Provider */}
              <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-5">
                <p className="text-xs text-gray-500">
                  Intelligence Provider
                </p>

                <p className="mt-3 text-sm text-gray-400">
                  {result.provider || "Not provided"}
                </p>
              </div>
            </div>

            {/* Metadata */}
            <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-5">
              <h2 className="text-sm font-semibold text-white">
                Indicator Metadata
              </h2>

              <div className="mt-5 grid gap-5 md:grid-cols-3">
                <div>
                  <p className="text-[10px] uppercase tracking-wider text-gray-600">
                    First Seen
                  </p>

                  <p className="mt-2 font-mono text-xs text-gray-400">
                    {result.first_seen || "Not provided"}
                  </p>
                </div>

                <div>
                  <p className="text-[10px] uppercase tracking-wider text-gray-600">
                    Last Seen
                  </p>

                  <p className="mt-2 font-mono text-xs text-gray-400">
                    {result.last_seen
                      ? new Date(
                          result.last_seen,
                        ).toLocaleString()
                      : "Not provided"}
                  </p>
                </div>

                <div>
                  <p className="text-[10px] uppercase tracking-wider text-gray-600">
                    Tags
                  </p>

                  {result.tags?.length ? (
                    <div className="mt-2 flex flex-wrap gap-2">
                      {result.tags.map((tag) => (
                        <span
                          key={tag}
                          className="rounded border border-white/10 bg-white/[0.02] px-2 py-1 font-mono text-[9px] text-gray-500"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <p className="mt-2 text-xs text-gray-600">
                      No tags provided
                    </p>
                  )}
                </div>
              </div>
            </div>
          </>
        )}

        {/* Empty State */}
        {!result && !loading && !error && (
          <div className="flex min-h-[400px] items-center justify-center rounded-xl border border-white/10 bg-[#1F2937]/40">
            <div className="max-w-md px-6 text-center">
              <Radar className="mx-auto h-10 w-10 text-[#00F0FF]/30" />

              <h2 className="mt-4 text-sm font-semibold text-white">
                Threat Investigation Center
              </h2>

              <p className="mt-2 text-xs leading-6 text-gray-500">
                Enter an IP address, domain, or file hash to investigate its reputation and threat intelligence.
              </p>
            </div>
          </div>
        )}

        {/* Backend Error State */}
        {!result && !loading && error && (
          <div className="flex min-h-[300px] items-center justify-center rounded-xl border border-[#EF4444]/20 bg-[#EF4444]/5">
            <div className="max-w-md px-6 text-center">
              <ShieldAlert className="mx-auto h-10 w-10 text-[#EF4444]/60" />

              <h2 className="mt-4 text-sm font-semibold text-white">
                Threat Intelligence Unavailable
              </h2>

              <p className="mt-2 text-xs leading-6 text-gray-500">
                The backend did not return threat intelligence data for this request.
              </p>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
