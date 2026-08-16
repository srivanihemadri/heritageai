const FALLBACK_API_URL = "http://127.0.0.1:8000/api/v1";

export const env = {
  apiUrl:
    process.env.EXPO_PUBLIC_API_URL?.replace(/\/+$/, "") ??
    FALLBACK_API_URL,
} as const;
