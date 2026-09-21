export type RiskLevel =
  | "Critical"
  | "High"
  | "Medium"
  | "Low"
  | "Safe";

export type SecurityHeaderStatus =
  | "PASS"
  | "WARN"
  | "FAIL";

export interface SecurityHeaderFinding {
  name: string;
  status: SecurityHeaderStatus;
  recommendation: string;
}

export interface WebSecurityResult {
  security_score: number;
  risk_level: RiskLevel;
  phishing_detected: boolean;
  ssl_valid: boolean;
  ssl_issuer: string | null;
  ssl_expiry: string | null;
  dns_records: string[];
  whois_registrar: string | null;
  headers: SecurityHeaderFinding[];
  recommendations: string[];
}
