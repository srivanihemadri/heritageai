import apiClient from "@/lib/api-client";

export type GroundedAnswerSource = {
  rank: number;
  chunk_id: string;
  document_id: string;
  title: string;
  similarity_score: number;
  provenance_level: string;
  is_verified: boolean;
};

export type GroundedAnswerResponse = {
  query: string;
  answer: string;
  sources: GroundedAnswerSource[];
  grounded: boolean;
};

export type GroundedAnswerRequest = {
  question: string;
  top_k?: number;
};

export async function askHeritageAI(
  question: string,
  top_k = 5,
): Promise<GroundedAnswerResponse> {
  const normalizedQuestion = question.trim();

  if (!normalizedQuestion) {
    throw new Error("Question cannot be empty.");
  }

  console.log(
    "[AI CHAT TRACE] sending question:",
    normalizedQuestion,
  );

  const response =
    await apiClient.post<GroundedAnswerResponse>(
      "/ai/answer",
      {
        question: normalizedQuestion,
        top_k,
      },
    );

  console.log(
    "[AI CHAT TRACE] response received:",
    response.status,
  );

  return response.data;
}
