import api from "./api";
import type { NetworkPacket, NetworkStatistics } from "../types/network";

export type { NetworkPacket, NetworkStatistics } from "../types/network";

export interface NetworkSnapshot {
  statistics: NetworkStatistics;
  packets: NetworkPacket[];
}

export async function getNetworkSnapshot(): Promise<NetworkSnapshot> {
  const response = await api.get("/network/statistics");
  return response.data;
}
