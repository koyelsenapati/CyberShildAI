import { useCallback, useEffect, useRef, useState } from "react";
import { createNetworkWebSocket } from "../services/websocket";
import type { NetworkPacket, NetworkStatistics } from "../types/network";

const INITIAL_STATISTICS: NetworkStatistics = {
  packets_per_second: 0,
  active_connections: 0,
  bandwidth: 0,
  protocols: { TCP: 0, UDP: 0, ICMP: 0 },
};

export function useNetworkWebSocket() {
  const socketRef = useRef<WebSocket | null>(null);
  const [connected, setConnected] = useState(false);
  const [packets, setPackets] = useState<NetworkPacket[]>([]);
  const [statistics, setStatistics] = useState<NetworkStatistics>(INITIAL_STATISTICS);

  const handleMessage = useCallback((data: unknown) => {
    if (!data || typeof data !== "object") return;
    const message = data as Partial<{ statistics: NetworkStatistics; packets: NetworkPacket[] }>;
    if (message.statistics) setStatistics(message.statistics);
    if (Array.isArray(message.packets)) setPackets(message.packets);
  }, []);

  const start = useCallback(() => {
    if (socketRef.current?.readyState === WebSocket.OPEN ||
      socketRef.current?.readyState === WebSocket.CONNECTING) return;
    try {
      socketRef.current = createNetworkWebSocket(
        handleMessage,
        () => setConnected(true),
        () => setConnected(false),
        () => setConnected(false),
      );
    } catch (error) {
      console.error("Network WebSocket connection failed:", error);
      setConnected(false);
      socketRef.current = null;
    }
  }, [handleMessage]);

  const stop = useCallback(() => {
    socketRef.current?.close();
    socketRef.current = null;
    setConnected(false);
  }, []);

  useEffect(() => () => socketRef.current?.close(), []);
  return { connected, packets, statistics, start, stop, clearPackets: () => setPackets([]) };
}
