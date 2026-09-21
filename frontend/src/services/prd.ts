import api from "./api";

export interface PasswordAnalyzeRequest {
  password: string;
}

export interface PasswordAnalyzeResponse {
  score: number;
  strength: string;
  entropy: number;
  common_password: boolean;
  brute_force_seconds: number;
  suggestions: string[];
}

export async function analyzePassword(
  payload: PasswordAnalyzeRequest,
): Promise<PasswordAnalyzeResponse> {
  const response = await api.post("/password/analyze", payload);
  return response.data;
}

export async function analyzeMalwareHash(
  file: File,
) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post(
    "/malware-hash/analyze",
    formData,
    { headers: { "Content-Type": "multipart/form-data" } },
  );

  return response.data;
}

export interface IncidentCreateRequest {
  title: string;
  severity?: "Low" | "Medium" | "High" | "Critical";
  description?: string | null;
}

export async function getIncidents() {
  const response = await api.get("/incidents/");
  return response.data;
}

export async function createIncident(
  payload: IncidentCreateRequest,
) {
  const response = await api.post("/incidents/", payload);
  return response.data;
}

export async function getIncident(id: number) {
  const response = await api.get(`/incidents/${id}`);
  return response.data;
}

export async function updateIncident(
  id: number,
  payload: {
    status?: "Open" | "Investigating" | "Resolved" | "Closed";
    analyst_notes?: string | null;
    resolution?: string | null;
    severity?: "Low" | "Medium" | "High" | "Critical";
  },
) {
  const response = await api.patch(`/incidents/${id}`, payload);
  return response.data;
}

export async function analyzeEmailPhishing(
  file: File,
) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post(
    "/email-phishing/analyze",
    formData,
    { headers: { "Content-Type": "multipart/form-data" } },
  );

  return response.data;
}
