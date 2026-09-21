export type IndicatorType =
  | "IP"
  | "DOMAIN"
  | "HASH";

export type ThreatSeverity =
  | "CLEAN"
  | "LOW"
  | "MEDIUM"
  | "HIGH"
  | "CRITICAL";

export interface ThreatIndicator {
  id: string;
  indicator: string;
  type: IndicatorType;
  severity: ThreatSeverity;
  reputation_score: number;
  malicious: boolean;
  confidence: number;
  country?: string;
  provider?: string;
  first_seen?: string;
  last_seen?: string;
  tags: string[];
  description: string;
}

export interface ThreatLookupResponse {
  indicator: ThreatIndicator;
}
