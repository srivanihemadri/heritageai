const FALLBACK_API_URL = "https://heritageai-api.onrender.com/api/v1";

export const env = {
  apiUrl:
    process.env.EXPO_PUBLIC_API_URL?.replace(/\/+$/, "") ??
    FALLBACK_API_URL,

  googleWebClientId:
    process.env.EXPO_PUBLIC_GOOGLE_WEB_CLIENT_ID ?? "",

  googleAndroidClientId:
    process.env.EXPO_PUBLIC_GOOGLE_ANDROID_CLIENT_ID ?? "",

  googleIosClientId:
    process.env.EXPO_PUBLIC_GOOGLE_IOS_CLIENT_ID ?? "",
} as const;

