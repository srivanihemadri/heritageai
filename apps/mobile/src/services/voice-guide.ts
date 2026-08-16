import apiClient from "@/lib/api-client";

export type VoiceGuideSource = {
  rank: number;
  chunk_id: string;
  document_id: string;
  title: string;
  similarity_score: number;
  provenance_level: string;
  is_verified: boolean;
};

export type VoiceGuideResponse = {
  success: boolean;
  transcript: string;
  language: string | null;
  confidence: number | null;
  answer: string;
  grounded: boolean;
  sources: VoiceGuideSource[];
  audio_url: string | null;
  audio_mime_type: string | null;
  audio_sample_rate: number | null;
  tts_available: boolean;
  tts_fallback_reason: string | null;
};

export async function processVoiceGuide(
  uri: string,
): Promise<VoiceGuideResponse> {
  console.log(
    "[VOICE GUIDE TRACE] preparing audio upload:",
    uri,
  );

  const response = await fetch(uri);

  if (!response.ok) {
    throw new Error(
      "Unable to read the recorded audio.",
    );
  }

  const audioBlob = await response.blob();

  console.log(
    "[VOICE GUIDE TRACE] audio blob:",
    JSON.stringify({
      type: audioBlob.type,
      size: audioBlob.size,
    }),
  );

  if (!audioBlob.size) {
    throw new Error(
      "The recorded audio is empty.",
    );
  }

  const mimeType =
    audioBlob.type || "audio/webm";

  const extension = mimeType.includes("wav")
    ? "wav"
    : mimeType.includes("mp4") ||
        mimeType.includes("m4a")
      ? "m4a"
      : "webm";

  const formData = new FormData();

  formData.append(
    "file",
    audioBlob,
    `heritage-voice.${extension}`,
  );

  console.log(
    "[VOICE GUIDE TRACE] sending audio to /ai/voice-guide",
  );

  const responseData =
    await apiClient.post<VoiceGuideResponse>(
      "/ai/voice-guide",
      formData,
      {
        timeout: 180000,
      },
    );

  console.log(
    "[VOICE GUIDE TRACE] voice guide received:",
    JSON.stringify({
      success: responseData.data.success,
      grounded: responseData.data.grounded,
      sourceCount: responseData.data.sources.length,
      audioMimeType:
        responseData.data.audio_mime_type,
      audioSampleRate:
        responseData.data.audio_sample_rate,
    }),
  );

  return responseData.data;
}
