import axios from "axios";

import { env } from "@/config/env";
import { getAccessToken } from "@/storage/auth-storage";

// eslint-disable-next-line import/no-named-as-default-member
const apiClient = axios.create({
  baseURL: env.apiUrl,
  headers: {
    Accept: "application/json",
  },
  timeout: 15000,
});

apiClient.interceptors.request.use(async (config) => {
  const token = await getAccessToken();

  console.log(
    "[API TRACE] request:",
    config.method?.toUpperCase(),
    config.url,
  );

  console.log(
    "[API TRACE] access token:",
    token ? `PRESENT (${token.length} chars)` : "MISSING",
  );

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;

    console.log(
      "[API TRACE] Authorization header: ATTACHED",
    );
  } else {
    console.log(
      "[API TRACE] Authorization header: NOT ATTACHED",
    );
  }

  return config;
});

export default apiClient;
