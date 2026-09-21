import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  ArrowDown,
  Globe,
  Network,
  Radio,
  ShieldAlert,
  Wifi,
} from "lucide-react";

import DashboardLayout from "../layouts/DashboardLayout";
import PageHeader from "../components/common/PageHeader";

import type {
  NetworkPacket,
  NetworkStatistics,
} from "../services/network";

import {
  createNetworkWebSocket,
  type NetworkWebSocketData,
} from "../services/websocket";

function StatusBadge({
  status,
}: {
  status: NetworkPacket["status"];
}) {
  const styles: Record<NetworkPacket["status"], string> = {
    NORMAL:
      "border-[#10B981]/20 bg-[#10B981]/5 text-[#10B981]",
    SUSPICIOUS:
      "border-[#F59E0B]/20 bg-[#F59E0B]/5 text-[#F59E0B]",
    BLOCKED:
      "border-[#EF4444]/20 bg-[#EF4444]/5 text-[#EF4444]",
  };

  return (
    <span
      className={`rounded border px-2 py-1 text-[9px] font-semibold ${styles[status]}`}
    >
      {status}
    </span>
  );
}

export default function NetworkAnalyzer() {
  const [statistics, setStatistics] =
    useState<NetworkStatistics | null>(null);

  const [packets, setPackets] =
    useState<NetworkPacket[]>([]);

  const [live, setLive] = useState(true);
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!live) {
      setConnected(false);
      return;
    }

    let socket: WebSocket | null = null;
    let reconnectTimer: ReturnType<typeof setTimeout> | null = null;
    let mounted = true;

    const connect = () => {
      if (!mounted || !live) {
        return;
      }

      setLoading(true);
      setError("");

      socket = createNetworkWebSocket(
        (data: NetworkWebSocketData) => {
          if (!mounted) {
            return;
          }

          setStatistics(data.statistics);
          setPackets(data.packets ?? []);
          setLoading(false);
          setConnected(true);
          setError("");
        },

        () => {
          if (!mounted) {
            return;
          }

          setConnected(true);
          setLoading(false);
          setError("");
        },

        () => {
          if (!mounted) {
            return;
          }

          setConnected(false);

          reconnectTimer = setTimeout(() => {
            connect();
          }, 3000);
        },

        () => {
          if (!mounted) {
            return;
          }

          setConnected(false);
          setError(
            "Network telemetry connection error.",
          );
        },
      );
    };

    connect();

    return () => {
      mounted = false;

      if (reconnectTimer) {
        clearTimeout(reconnectTimer);
      }

      socket?.close();
    };
  }, [live]);

  const protocolEntries = useMemo(() => {
    if (!statistics?.protocols) {
      return [];
    }

    return Object.entries(statistics.protocols);
  }, [statistics]);

  const suspiciousPackets = useMemo(
    () =>
      packets.filter(
        (packet) =>
          packet.status === "SUSPICIOUS",
      ).length,
    [packets],
  );

  return (
    <DashboardLayout>
      <div className="mx-auto max-w-[1600px] space-y-6">

        <PageHeader
          eyebrow="NETWORK OPERATIONS"
          title="Network Analyzer"
          description="Monitor live network traffic, connections, protocols, and suspicious packet activity."
        />

        {error && (
          <div className="rounded-lg border border-[#EF4444]/20 bg-[#EF4444]/5 px-4 py-3 text-xs text-[#EF4444]">
            {error}
          </div>
        )}

        <div className="flex items-center justify-between rounded-xl border border-white/10 bg-[#1F2937]/60 px-5 py-4">
          <div className="flex items-center gap-3">
            <div
              className={`h-2 w-2 rounded-full ${
                connected
                  ? "animate-pulse bg-[#10B981]"
                  : "bg-gray-600"
              }`}
            />

            <div>
              <p className="text-xs font-semibold text-white">
                Network Monitoring
              </p>

              <p className="mt-1 text-[10px] text-gray-600">
                {connected
                  ? "Live backend telemetry connected"
                  : live
                    ? "Connecting to backend telemetry..."
                    : "Monitoring paused"}
              </p>
            </div>
          </div>

          <button
            onClick={() =>
              setLive((value) => !value)
            }
            className="rounded-lg border border-white/10 px-4 py-2 text-[10px] font-semibold text-gray-400 transition hover:border-[#00F0FF]/30 hover:text-[#00F0FF]"
          >
            {live
              ? "Pause Monitoring"
              : "Resume Monitoring"}
          </button>
        </div>

        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">

          <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-5">
            <Activity className="h-5 w-5 text-[#00F0FF]" />

            <p className="mt-4 text-xs text-gray-500">
              Packets / Second
            </p>

            <p className="mt-2 font-mono text-3xl font-bold text-white">
              {loading
                ? "--"
                : statistics?.packets_per_second ?? "--"}
            </p>

            <div className="mt-4 flex items-center gap-2 text-[10px] text-[#10B981]">
              <ArrowDown className="h-3 w-3 rotate-180" />
              Live Backend
            </div>
          </div>

          <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-5">
            <Wifi className="h-5 w-5 text-[#00F0FF]" />

            <p className="mt-4 text-xs text-gray-500">
              Active Connections
            </p>

            <p className="mt-2 font-mono text-3xl font-bold text-white">
              {loading
                ? "--"
                : statistics?.active_connections ?? "--"}
            </p>

            <div className="mt-4 text-[10px] text-gray-600">
              Current sessions
            </div>
          </div>

          <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-5">
            <ArrowDown className="h-5 w-5 text-[#00F0FF]" />

            <p className="mt-4 text-xs text-gray-500">
              Bandwidth
            </p>

            <p className="mt-2 font-mono text-3xl font-bold text-white">
              {loading
                ? "--"
                : statistics?.bandwidth ?? "--"}
            </p>

            <div className="mt-4 text-[10px] text-gray-600">
              Mbps
            </div>
          </div>

          <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-5">
            <ShieldAlert className="h-5 w-5 text-[#F59E0B]" />

            <p className="mt-4 text-xs text-gray-500">
              Suspicious Activity
            </p>

            <p className="mt-2 font-mono text-3xl font-bold text-[#F59E0B]">
              {loading
                ? "--"
                : suspiciousPackets}
            </p>

            <div className="mt-4 text-[10px] text-gray-600">
              Live backend packets
            </div>
          </div>

        </div>

        <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-5">

          <div className="flex items-center justify-between">
            <div>
              <p className="text-[10px] uppercase tracking-widest text-gray-600">
                Live Backend Telemetry
              </p>

              <h2 className="mt-1 text-sm font-semibold text-white">
                Network Traffic
              </h2>
            </div>

            <Radio
              className={`h-5 w-5 ${
                connected
                  ? "animate-pulse text-[#10B981]"
                  : "text-gray-600"
              }`}
            />
          </div>

          <div className="mt-6 flex h-48 items-center justify-center">

            {loading ? (
              <p className="text-xs text-gray-600">
                Connecting to network telemetry...
              </p>
            ) : !statistics ? (
              <p className="text-xs text-gray-600">
                No network telemetry available.
              </p>
            ) : (
              <div className="text-center">
                <Activity className="mx-auto h-8 w-8 text-[#00F0FF]" />

                <p className="mt-3 text-xs text-gray-500">
                  Current packet rate
                </p>

                <p className="mt-1 font-mono text-2xl font-bold text-white">
                  {statistics.packets_per_second}
                </p>

                <p className="mt-1 text-[10px] text-gray-600">
                  packets / second
                </p>
              </div>
            )}

          </div>
        </div>

        <div className="grid gap-6 lg:grid-cols-3">

          <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-5">

            <div className="flex items-center gap-3">
              <Globe className="h-5 w-5 text-[#00F0FF]" />

              <h2 className="text-sm font-semibold text-white">
                Protocol Statistics
              </h2>
            </div>

            <div className="mt-5 space-y-4">

              {protocolEntries.length === 0 ? (
                <p className="text-xs text-gray-600">
                  No protocol data available from backend.
                </p>
              ) : (
                protocolEntries.map(
                  ([protocol, percentage]) => (
                    <div key={protocol}>

                      <div className="flex justify-between text-[10px]">
                        <span className="font-mono text-gray-400">
                          {protocol}
                        </span>

                        <span className="text-gray-600">
                          {percentage}%
                        </span>
                      </div>

                      <div className="mt-2 h-1.5 rounded-full bg-white/5">
                        <div
                          className="h-full rounded-full bg-[#00F0FF]"
                          style={{
                            width: `${percentage}%`,
                          }}
                        />
                      </div>

                    </div>
                  ),
                )
              )}

            </div>
          </div>

          <div className="rounded-xl border border-white/10 bg-[#1F2937]/60 p-5 lg:col-span-2">

            <div className="flex items-center gap-3">
              <Network className="h-5 w-5 text-[#00F0FF]" />

              <div>
                <h2 className="text-sm font-semibold text-white">
                  Connection Monitor
                </h2>

                <p className="mt-1 text-[10px] text-gray-600">
                  Live protocol information reported by backend telemetry.
                </p>
              </div>
            </div>

            <div className="mt-6">

              {protocolEntries.length === 0 ? (
                <div className="rounded-lg bg-[#0B0F17] p-8 text-center">
                  <p className="text-xs text-gray-600">
                    No protocol telemetry available.
                  </p>
                </div>
              ) : (
                <div className="grid grid-cols-2 gap-3 md:grid-cols-4">

                  {protocolEntries.map(
                    ([protocol, percentage]) => (
                      <div
                        key={protocol}
                        className="rounded-lg bg-[#0B0F17] p-4"
                      >
                        <p className="text-[9px] uppercase text-gray-600">
                          {protocol}
                        </p>

                        <p className="mt-2 font-mono text-xl text-white">
                          {percentage}%
                        </p>
                      </div>
                    ),
                  )}

                </div>
              )}

            </div>
          </div>

        </div>

        <div className="overflow-hidden rounded-xl border border-white/10 bg-[#1F2937]/60">

          <div className="border-b border-white/10 px-5 py-4">

            <div className="flex items-center justify-between">

              <div>
                <p className="text-[10px] uppercase tracking-widest text-gray-600">
                  Packet Inspection
                </p>

                <h2 className="mt-1 text-sm font-semibold text-white">
                  Network Packets
                </h2>
              </div>

              <span className="font-mono text-[10px] text-gray-600">
                {packets.length} packets
              </span>

            </div>
          </div>

          <div className="overflow-x-auto">

            <table className="w-full min-w-[900px] text-left">

              <thead>
                <tr className="border-b border-white/5 text-[9px] uppercase tracking-wider text-gray-600">
                  <th className="px-5 py-3">Time</th>
                  <th className="px-5 py-3">Source</th>
                  <th className="px-5 py-3">Destination</th>
                  <th className="px-5 py-3">Protocol</th>
                  <th className="px-5 py-3">Port</th>
                  <th className="px-5 py-3">Size</th>
                  <th className="px-5 py-3">Status</th>
                </tr>
              </thead>

              <tbody className="divide-y divide-white/5">

                {packets.length === 0 ? (
                  <tr>
                    <td
                      colSpan={7}
                      className="px-5 py-10 text-center text-xs text-gray-600"
                    >
                      {loading
                        ? "Loading network packets..."
                        : "No network packets available from backend."}
                    </td>
                  </tr>
                ) : (
                  packets.map((packet, index) => (
                    <tr
                      key={
                        packet.id ??
                        `${packet.timestamp}-${index}`
                      }
                      className="transition hover:bg-white/[0.02]"
                    >

                      <td className="px-5 py-3 font-mono text-[10px] text-gray-600">
                        {packet.timestamp}
                      </td>

                      <td className="px-5 py-3 font-mono text-[10px] text-gray-400">
                        {packet.source_ip}
                      </td>

                      <td className="px-5 py-3 font-mono text-[10px] text-gray-400">
                        {packet.destination_ip}
                      </td>

                      <td className="px-5 py-3 font-mono text-[10px] text-[#00F0FF]">
                        {packet.protocol}
                      </td>

                      <td className="px-5 py-3 font-mono text-[10px] text-gray-500">
                        {packet.port}
                      </td>

                      <td className="px-5 py-3 font-mono text-[10px] text-gray-500">
                        {packet.size} B
                      </td>

                      <td className="px-5 py-3">
                        <StatusBadge
                          status={packet.status}
                        />
                      </td>

                    </tr>
                  ))
                )}

              </tbody>
            </table>

          </div>
        </div>

      </div>
    </DashboardLayout>
  );
}
