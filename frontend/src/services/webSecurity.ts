import api from "./api";

import type {
  WebSecurityResult,
} from "../types/webSecurity";

export async function scanWebsite(
  url: string,
): Promise<WebSecurityResult> {
  const response = await api.post(
    "/web-scan/",
    {
      url,
    },
  );

  return response.data;
}
