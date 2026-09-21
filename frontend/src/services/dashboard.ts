import { api } from "./api";

export interface DashboardStatistics {
  security_score: number;
  threat_count: number;
  alert_count: number;
  vulnerability_count: number;
  critical_vulnerabilities: number;
  active_connections: number;
  packets_per_second: number;
  total_scans?: number;
}

export async function getDashboardStatistics(): Promise<DashboardStatistics> {
  const response = await api.get("/dashboard/statistics");

  return response.data;
}
