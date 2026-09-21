export interface FileIntegrityScan {
  id?: number;
  file_path: string;
  file_hash: string;
  algorithm: string;
  status: string;
  result?: string | null;
  created_at?: string | null;
}

export interface FileIntegrityResponse {
  message: string;
  scan: FileIntegrityScan;
}
