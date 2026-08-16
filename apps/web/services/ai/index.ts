import apiClient from "@/lib/api-client";

export interface GroundedAnswerSource {
  rank: number;
  chunk_id: string;
  document_id: string;
  title: string;
  similarity_score: number;
  provenance_level: string;
  is_verified: boolean;
}

export interface GroundedAnswerResponse {
  query: string;
  answer: string;
  sources: GroundedAnswerSource[];
  grounded: boolean;
}

export interface HeritageScannerResult {
  identified_name: string | null;
  identification_status:
    | "IDENTIFIED"
    | "POSSIBLE_MATCH"
    | "INSUFFICIENT_EVIDENCE"
    | "NOT_HERITAGE"
    | "AMBIGUOUS";
  evidence_quality: "STRONG" | "MODERATE" | "WEAK" | "NONE";
  category: string | null;
  location: string | null;
  country: string | null;
  confidence: number;
  confidence_level: "LOW" | "MEDIUM" | "HIGH";
  description: string | null;
  architectural_style: string | null;
  historical_period: string | null;
  historical_significance: string | null;
  visual_evidence: string[];
  alternative_matches: string[];
  grounding_status: "GROUNDED" | "PARTIALLY_GROUNDED" | "UNVERIFIED";
}

export interface HeritageScannerResponse {
  success: boolean;
  scan_id: string;
  result: HeritageScannerResult;
}

export async function askHeritageAI(
  question: string,
  top_k = 5,
): Promise<GroundedAnswerResponse> {
  const response = await apiClient.post<GroundedAnswerResponse>(
    "/ai/answer",
    {
      question,
      top_k,
    },
  );

  return response.data;
}

export async function scanHeritageImage(
  file: File,
): Promise<HeritageScannerResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await apiClient.post<HeritageScannerResponse>(
    "/ai/scan",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    },
  );

  return response.data;
}
