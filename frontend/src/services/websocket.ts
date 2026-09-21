import type { NetworkPacket, NetworkStatistics } from "../types/network";
import { useAuthStore } from "../store/authStore";

const WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL ||
  `${window.location.protocol === "https:" ? "wss" : "ws"}://${window.location.host}`;

export interface NetworkWebSocketData {
  timestamp: string;
  statistics: NetworkStatistics;
  packets: NetworkPacket[];
}

export function createNetworkWebSocket(
  onMessage: (data: NetworkWebSocketData) => void,
  onOpen?: () => void,
  onClose?: () => void,
  onError?: () => void,
) {
  const token = useAuthStore.getState().token;
  if (!token) {
    throw new Error("An authenticated session is required for network telemetry.");
  }

  const socket = new WebSocket(
    `${WS_BASE_URL}/ws/network?token=${encodeURIComponent(token)}`,
  );
  socket.onopen = () => onOpen?.();
  socket.onmessage = (event) => {
    try {
      onMessage(JSON.parse(event.data) as NetworkWebSocketData);
    } catch (error) {
      console.error("Invalid Network WebSocket message:", error);
    }
  };
  socket.onerror = () => onError?.();
  socket.onclose = () => onClose?.();
  return socket;
}
