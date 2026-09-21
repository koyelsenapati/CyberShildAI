export type RiskLevel =
  | "LOW"
  | "MEDIUM"
  | "HIGH"
  | "CRITICAL";

export type Severity =
  | "CRITICAL"
  | "HIGH"
  | "MEDIUM"
  | "LOW"
  | "INFO";

export interface SecurityScore {
  score: number;
  risk_level: RiskLevel;
}

export interface DashboardAlert {
  id: number;
  title: string;
  severity: Severity;
  source: string;
  timestamp: string;
  status: "OPEN" | "INVESTIGATING" | "RESOLVED";
}

export interface NetworkActivityPoint {
  time: string;
  packets: number;
  connections: number;
  suspicious: number;
}

export interface VulnerabilitySummary {
  critical: number;
  high: number;
  medium: number;
  low: number;
  resolved: number;
}

export interface ThreatSummary {
  critical: number;
  high: number;
  medium: number;
  low: number;
}

export interface RecentScan {
  id: number;
  target: string;
  scan_type: string;
  status: "COMPLETED" | "RUNNING" | "FAILED" | "QUEUED";
  severity: Severity;
  created_at: string;
}

export interface DashboardStatistics {
  security_score: SecurityScore;
  active_alerts: number;
  critical_alerts: number;
  active_connections: number;
  suspicious_connections: number;
  vulnerabilities: VulnerabilitySummary;
  threats: ThreatSummary;
  network_activity: NetworkActivityPoint[];
  recent_scans: RecentScan[];
}
