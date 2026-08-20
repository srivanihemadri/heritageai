import apiClient from "@/lib/api-client";

export type VoiceTranscriptionResponse = {
  success: boolean;
  transcript: string;
  language: string | null;
  confidence: number | null;
};

type BackendVoiceResponse = {
  success: boolean;
  result: {
    transcript: string;
    language: string | null;
    confidence: number | null;
  };
};

export async function transcribeVoice(
  uri: string,
): Promise<VoiceTranscriptionResponse> {
  console.log(
    "[CHAT VOICE TRACE] preparing audio upload:",
    uri,
  );

  const formData = new FormData();

  formData.append(
    "file",
    {
      uri,
      name: "heritage-chat-voice.m4a",
      type: "audio/mp4",
    } as any,
  );

  console.log(
    "[CHAT VOICE TRACE] multipart file prepared",
  );

  console.log(
    "[CHAT VOICE TRACE] sending audio to /ai/voice",
  );

  const response =
    await apiClient.post<BackendVoiceResponse>(
      "/ai/voice",
      formData,
      {
        timeout: 180000,
      },
    );

  console.log(
    "[CHAT VOICE TRACE] transcription HTTP status:",
    response.status,
  );

  console.log(
    "[CHAT VOICE TRACE] backend response:",
    JSON.stringify(response.data),
  );

  const result = response.data.result;

  if (!result?.transcript) {
    throw new Error(
      "Voice transcription response did not contain a transcript.",
    );
  }

  const transcription: VoiceTranscriptionResponse = {
    success: response.data.success,
    transcript: result.transcript,
    language: result.language,
    confidence: result.confidence,
  };

  console.log(
    "[CHAT VOICE TRACE] transcription received:",
    JSON.stringify(transcription),
  );

  return transcription;
}
