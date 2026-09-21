import type {
  FileIntegrityResponse,
} from "../types/fileIntegrity";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "/api/v1";

export async function scanFileIntegrity(
  filePath: string,
): Promise<FileIntegrityResponse> {
  const token = localStorage.getItem("token");

  const params = new URLSearchParams({
    file_path: filePath,
  });

  const response = await fetch(
    `${API_BASE_URL}/file-integrity/?${params.toString()}`,
    {
      method: "POST",
      headers: {
        ...(token
          ? {
              Authorization: `Bearer ${token}`,
            }
          : {}),
      },
    },
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data?.detail ||
        "File integrity scan failed.",
    );
  }

  return data;
}
