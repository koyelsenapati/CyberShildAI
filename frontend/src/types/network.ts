export type NetworkProtocol = "TCP" | "UDP" | "ICMP";
export type NetworkPacketStatus = "NORMAL" | "SUSPICIOUS" | "BLOCKED";

export interface NetworkPacket {
  id: string;
  timestamp: string;
  source_ip: string;
  destination_ip: string;
  protocol: NetworkProtocol;
  port: number;
  size: number;
  status: NetworkPacketStatus;
}

export interface NetworkStatistics {
  packets_per_second: number;
  active_connections: number;
  bandwidth: number;
  protocols: Record<NetworkProtocol, number>;
}
