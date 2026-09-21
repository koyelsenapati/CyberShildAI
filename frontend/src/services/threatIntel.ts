import api from "./api";

import type {
  IndicatorType,
  ThreatLookupResponse,
} from "../types/threatIntel";

export async function lookupThreatIndicator(
  indicator: string,
  type: IndicatorType,
): Promise<ThreatLookupResponse> {
  const response = await api.post(
    "/threat-intel/lookup",
    {
      indicator,
      type,
    },
  );

  return response.data;
}
