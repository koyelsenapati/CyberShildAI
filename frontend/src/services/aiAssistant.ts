import api from "./api";

export interface AIChatResponse {
  answer: string;
  provider: string;
  model: string;
}

export async function sendAIMessage(
  message: string,
): Promise<AIChatResponse> {
  const response = await api.post<AIChatResponse>(
    "/ai-assistant/chat",
    { message },
  );

  return response.data;
}
