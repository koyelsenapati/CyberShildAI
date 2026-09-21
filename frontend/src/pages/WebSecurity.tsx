import { useState } from "react";

import {
  AlertTriangle,
  CheckCircle2,
  Globe,
  Lock,
  Radar,
  Search,
  ShieldAlert,
  ShieldCheck,
  XCircle,
} from "lucide-react";

import DashboardLayout from "../layouts/DashboardLayout";
import PageHeader from "../components/common/PageHeader";

import { scanWebsite } from "../services/webSecurity";

import type {
  SecurityHeaderFinding,
  WebSecurityResult,
} from "../types/webSecurity";

function HeaderStatus({
  status,
}: {
  status: SecurityHeaderFinding["status"];
}) {
  switch (status) {
    case "PASS":
      return (
        <span className="flex items-center gap-1 text-[10px] font-semibold text-[#10B981]">
          <CheckCircle2 className="h-3.5 w-3.5" />
          PASS
        </span>
      );

    case "WARN":
      return (
        <span className="flex items-center gap-1 text-[10px] font-semibold text-[#F59E0B]">
          <AlertTriangle className="h-3.5 w-3.5" />
          WARN
        </span>
      );

    default:
      return (
        <span className="flex items-center gap-1 text-[10px] font-semibold text-[#EF4444]">
          <XCircle className="h-3.5 w-3.5" />
          FAIL
        </span>
      );
  }
}

function getRiskValue(
  riskLevel: WebSecurityResult["risk_level"],
): string {
  if (riskLevel === null || riskLevel === undefined) {
    return "";
  }

  return String(riskLevel).toUpperCase();
}

function getRiskColor(
  riskLevel: WebSecurityResult["risk_level"],
): string {
  const value = getRiskValue(riskLevel);

  if (
    value.includes("CRITICAL") ||
    value.includes("HIGH")
  ) {
    return "text-[#EF4444]";
  }

  if (value.includes("MEDIUM")) {
    return "text-[#F59E0B]";
  }

  return "text-[#10B981]";
}

function RiskIcon({
  riskLevel,
}: {
  riskLevel: WebSecurityResult["risk_level"];
}) {
  const value = getRiskValue(riskLevel);

  if (
    value.includes("CRITICAL") ||
    value.includes("HIGH")
  ) {
    return (
      <ShieldAlert className="h-5 w-5 text-[#EF4444]" />
    );
  }

  return (
    <ShieldCheck className="h-5 w-5 text-[#10B981]" />
  );
}

export default function WebSecurity() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] =
    useState<WebSecurityResult | null>(null);

  async function handleScan() {
    const trimmedUrl = url.trim();

    if (!trimmedUrl) {
      setError("Please enter a website URL.");
      setResult(null);
      return;
    }

    let validUrl: URL;

    try {
      validUrl = new URL(trimmedUrl);
    } catch {
      setError(
        "Please enter a valid HTTP or HTTPS website URL.",
      );
      setResult(null);
      return;
    }

    if (
      validUrl.protocol !== "http:" &&
      validUrl.protocol !== "https:"
    ) {
      setError(
        "Only HTTP and HTTPS URLs are supported.",
      );
      setResult(null);
      return;
    }

    if (!validUrl.hostname) {
      setError(
        "The URL must contain a valid domain or hostname.",
      );
      setResult(null);
      return;
    }

    setError("");
    setLoading(true);
    setResult(null);

    try {
      const response = await scanWebsite(
        validUrl.toString(),
      );

      if (!response) {
        throw new Error(
          "Empty response received from backend.",
        );
      }

      setResult(response);
    } catch (scanError) {
      console.error(
        "Website security scan failed:",
        scanError,
      );

      if (
        scanError instanceof Error &&
        scanError.message
      ) {
        setError(scanError.message);
      } else {
        setError(
          "Unable to retrieve website security data from the backend.",
        );
      }

      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <DashboardLayout>
      <div className="mx-auto max-w-[1600px] space-y-6">

        <PageHeader
          eyebrow="WEB SECURITY"
          title="Web Security Scanner"
          description="Analyze websites for phishing indicators, security headers, SSL configuration, DNS information, and security weaknesses."
        />

        <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-5">

          <div className="flex items-center gap-3">

            <div className="rounded-lg bg-[#00F0FF]/10 p-2">
              <Globe className="h-5 w-5 text-[#00F0FF]" />
            </div>

            <div>
              <h2 className="text-sm font-semibold text-white">
                Website Security Analysis
              </h2>

              <p className="mt-1 text-xs text-gray-500">
                Enter a public website URL to begin analysis.
              </p>
            </div>

          </div>

          <div className="mt-5 flex flex-col gap-3 md:flex-row">

            <div className="relative flex-1">

              <Globe
                className="
                  absolute
                  left-4
                  top-1/2
                  h-4
                  w-4
                  -translate-y-1/2
                  text-gray-700
                "
              />

              <input
                type="url"
                value={url}
                onChange={(event) =>
                  setUrl(event.target.value)
                }
                onKeyDown={(event) => {
                  if (
                    event.key === "Enter" &&
                    !loading
                  ) {
                    handleScan();
                  }
                }}
                placeholder="https://your-domain.com"
                disabled={loading}
                className="
                  w-full
                  rounded-lg
                  border
                  border-white/10
                  bg-[#0B0F17]
                  py-3
                  pl-11
                  pr-4
                  font-mono
                  text-sm
                  text-white
                  outline-none
                  placeholder:text-gray-700
                  focus:border-[#00F0FF]/40
                  disabled:cursor-not-allowed
                  disabled:opacity-50
                "
              />

            </div>

            <button
              type="button"
              onClick={handleScan}
              disabled={loading}
              className="
                flex
                items-center
                justify-center
                gap-2
                rounded-lg
                bg-[#00F0FF]
                px-6
                py-3
                text-xs
                font-semibold
                text-[#0B0F17]
                transition
                hover:bg-[#00D9E8]
                disabled:cursor-not-allowed
                disabled:opacity-50
              "
            >

              {loading ? (
                <>
                  <Radar className="h-4 w-4 animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Search className="h-4 w-4" />
                  Analyze Website
                </>
              )}

            </button>

          </div>

          {error && (
            <div className="mt-4 rounded-lg border border-[#EF4444]/20 bg-[#EF4444]/5 px-4 py-3">

              <div className="flex items-center gap-2">

                <AlertTriangle className="h-4 w-4 shrink-0 text-[#EF4444]" />

                <p className="text-xs text-[#EF4444]">
                  {error}
                </p>

              </div>

            </div>
          )}

        </div>

        {loading && (
          <div className="rounded-xl border border-[#00F0FF]/20 bg-[#00F0FF]/5 p-6">

            <div className="flex items-center gap-4">

              <Radar className="h-6 w-6 animate-spin text-[#00F0FF]" />

              <div>

                <p className="text-sm font-semibold text-white">
                  Analyzing website security...
                </p>

                <p className="mt-1 text-xs text-gray-500">
                  Checking phishing indicators, SSL,
                  security headers, DNS and website
                  configuration.
                </p>

              </div>

            </div>

            <div className="mt-5 h-1.5 overflow-hidden rounded-full bg-white/5">
              <div className="h-full w-2/3 animate-pulse rounded-full bg-[#00F0FF]" />
            </div>

          </div>
        )}

        {result && !loading && (
          <>

            <div className="grid gap-4 lg:grid-cols-4">

              <div className="rounded-xl border border-[#00F0FF]/20 bg-[#00F0FF]/5 p-6">

                <p className="text-xs uppercase tracking-wider text-gray-500">
                  Security Score
                </p>

                <div className="mt-3 flex items-end gap-2">

                  <span className="font-mono text-5xl font-bold text-white">
                    {result.security_score ?? 0}
                  </span>

                  <span className="mb-2 text-sm text-gray-600">
                    /100
                  </span>

                </div>

                <div className="mt-4 h-2 overflow-hidden rounded-full bg-white/5">

                  <div
                    className="h-full rounded-full bg-[#00F0FF] transition-all"
                    style={{
                      width: `${Math.max(
                        0,
                        Math.min(
                          100,
                          Number(
                            result.security_score ?? 0,
                          ),
                        ),
                      )}%`,
                    }}
                  />

                </div>

              </div>

              <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-6">

                <RiskIcon
                  riskLevel={result.risk_level}
                />

                <p className="mt-4 text-xs text-gray-500">
                  Risk Level
                </p>

                <p
                  className={`mt-1 text-xl font-bold ${getRiskColor(
                    result.risk_level,
                  )}`}
                >
                  {result.risk_level
                    ? String(result.risk_level)
                    : "Unknown"}
                </p>

              </div>

              <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-6">

                {result.phishing_detected ? (
                  <ShieldAlert className="h-5 w-5 text-[#EF4444]" />
                ) : (
                  <CheckCircle2 className="h-5 w-5 text-[#10B981]" />
                )}

                <p className="mt-4 text-xs text-gray-500">
                  Phishing Detection
                </p>

                <p
                  className={`mt-1 text-xl font-bold ${
                    result.phishing_detected
                      ? "text-[#EF4444]"
                      : "text-[#10B981]"
                  }`}
                >
                  {result.phishing_detected
                    ? "DETECTED"
                    : "CLEAR"}
                </p>

              </div>

              <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-6">

                <Lock
                  className={`h-5 w-5 ${
                    result.ssl_valid
                      ? "text-[#10B981]"
                      : "text-[#EF4444]"
                  }`}
                />

                <p className="mt-4 text-xs text-gray-500">
                  SSL Certificate
                </p>

                <p
                  className={`mt-1 text-xl font-bold ${
                    result.ssl_valid
                      ? "text-[#10B981]"
                      : "text-[#EF4444]"
                  }`}
                >
                  {result.ssl_valid
                    ? "VALID"
                    : "INVALID"}
                </p>

              </div>

            </div>

            <div className="grid gap-6 lg:grid-cols-3">

              <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-5">

                <div className="flex items-center gap-3">

                  <Lock className="h-5 w-5 text-[#10B981]" />

                  <h2 className="text-sm font-semibold text-white">
                    SSL Certificate
                  </h2>

                </div>

                <div className="mt-5 space-y-3 text-xs">

                  <div className="flex justify-between gap-4">

                    <span className="text-gray-600">
                      Status
                    </span>

                    <span
                      className={
                        result.ssl_valid
                          ? "text-[#10B981]"
                          : "text-[#EF4444]"
                      }
                    >
                      {result.ssl_valid
                        ? "Valid"
                        : "Invalid"}
                    </span>

                  </div>

                  <div className="flex justify-between gap-4">

                    <span className="text-gray-600">
                      Issuer
                    </span>

                    <span className="text-right text-gray-400">
                      {result.ssl_issuer || "N/A"}
                    </span>

                  </div>

                  <div className="flex justify-between gap-4">

                    <span className="text-gray-600">
                      Expiry
                    </span>

                    <span className="font-mono text-gray-400">
                      {result.ssl_expiry || "N/A"}
                    </span>

                  </div>

                </div>

              </div>

              <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-5">

                <div className="flex items-center gap-3">

                  <Globe className="h-5 w-5 text-[#00F0FF]" />

                  <h2 className="text-sm font-semibold text-white">
                    DNS Records
                  </h2>

                </div>

                <div className="mt-5 space-y-2">

                  {result.dns_records &&
                  result.dns_records.length > 0 ? (
                    result.dns_records.map(
                      (record, index) => (
                        <div
                          key={`${record}-${index}`}
                          className="
                            rounded-lg
                            border
                            border-white/5
                            bg-[#0B0F17]
                            px-3
                            py-2
                            font-mono
                            text-[10px]
                            text-gray-500
                          "
                        >
                          {record}
                        </div>
                      ),
                    )
                  ) : (
                    <p className="text-xs text-gray-600">
                      No DNS records returned.
                    </p>
                  )}

                </div>

              </div>

              <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-5">

                <div className="flex items-center gap-3">

                  <Search className="h-5 w-5 text-[#F59E0B]" />

                  <h2 className="text-sm font-semibold text-white">
                    WHOIS
                  </h2>

                </div>

                <div className="mt-5">

                  <p className="text-[10px] uppercase tracking-wider text-gray-600">
                    Registrar
                  </p>

                  <p className="mt-2 text-sm text-gray-400">
                    {result.whois_registrar ||
                      "Information unavailable"}
                  </p>

                </div>

              </div>

            </div>

            <div className="overflow-hidden rounded-xl border border-white/10 bg-[#1F2937]/60">

              <div className="border-b border-white/10 px-5 py-4">

                <h2 className="text-sm font-semibold text-white">
                  Security Headers
                </h2>

                <p className="mt-1 text-[10px] text-gray-500">
                  HTTP security header analysis.
                </p>

              </div>

              <div className="divide-y divide-white/5">

                {result.headers &&
                result.headers.length > 0 ? (
                  result.headers.map(
                    (header) => (
                      <div
                        key={header.name}
                        className="
                          flex
                          flex-col
                          gap-3
                          px-5
                          py-4
                          md:flex-row
                          md:items-center
                          md:justify-between
                        "
                      >

                        <div>

                          <p className="font-mono text-xs text-gray-300">
                            {header.name}
                          </p>

                          <p className="mt-1 text-[10px] text-gray-600">
                            {header.recommendation ||
                              "No recommendation provided."}
                          </p>

                        </div>

                        <HeaderStatus
                          status={header.status}
                        />

                      </div>
                    ),
                  )
                ) : (
                  <div className="px-5 py-6 text-xs text-gray-600">
                    No security header data returned.
                  </div>
                )}

              </div>

            </div>

            <div className="rounded-xl border border-[#00F0FF]/10 bg-[#00F0FF]/5 p-5">

              <div className="flex items-center gap-3">

                <ShieldCheck className="h-5 w-5 text-[#00F0FF]" />

                <h2 className="text-sm font-semibold text-white">
                  Security Recommendations
                </h2>

              </div>

              <div className="mt-4 space-y-3">

                {result.recommendations &&
                result.recommendations.length > 0 ? (
                  result.recommendations.map(
                    (recommendation, index) => (
                      <div
                        key={`${recommendation}-${index}`}
                        className="flex gap-3"
                      >

                        <span className="font-mono text-xs text-[#00F0FF]">
                          {String(
                            index + 1,
                          ).padStart(2, "0")}
                        </span>

                        <p className="text-xs leading-5 text-gray-400">
                          {recommendation}
                        </p>

                      </div>
                    ),
                  )
                ) : (
                  <p className="text-xs text-gray-600">
                    No recommendations returned by the backend.
                  </p>
                )}

              </div>

            </div>

          </>
        )}

        {!result && !loading && !error && (
          <div className="flex min-h-[400px] items-center justify-center rounded-xl border border-white/10 bg-[#1F2937]/40">

            <div className="max-w-md px-6 text-center">

              <Globe className="mx-auto h-10 w-10 text-[#00F0FF]/30" />

              <h2 className="mt-4 text-sm font-semibold text-white">
                Website Security Scanner
              </h2>

              <p className="mt-2 text-xs leading-6 text-gray-500">
                Enter a public website URL to analyze
                its SSL certificate, DNS records,
                security headers, phishing indicators,
                and overall security posture.
              </p>

            </div>

          </div>
        )}

      </div>
    </DashboardLayout>
  );
}
