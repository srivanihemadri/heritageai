import axios from "axios";

import apiClient from "@/lib/api-client";
import {
  clearAccessToken,
  setAccessToken,
} from "@/storage/auth-storage";
import type {
  APIResponse,
  LoginRequest,
  TokenResponse,
  UserResponse,
} from "@/types/auth";

export async function login(
  data: LoginRequest,
): Promise<TokenResponse> {
  const formData = new URLSearchParams();

  formData.append("username", data.email);
  formData.append("password", data.password);

  console.log("[AUTH TRACE] login: sending request");

  const response = await axios.post<TokenResponse>(
    `${apiClient.defaults.baseURL}/auth/login`,
    formData.toString(),
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      timeout: 15000,
    },
  );

  console.log(
    "[AUTH TRACE] login: HTTP success",
    response.status,
  );

  console.log(
    "[AUTH TRACE] login: storing access token",
  );

  try {
    await setAccessToken(response.data.access_token);
    console.log(
      "[AUTH TRACE] login: token storage success",
    );
  } catch (error) {
    console.error(
      "[AUTH TRACE] login: token storage FAILED",
      error,
    );
    throw error;
  }

  return response.data;
}

export async function getCurrentUser(): Promise<UserResponse> {
  console.log(
    "[AUTH TRACE] getCurrentUser: sending request",
  );

  try {
    const response = await apiClient.get<APIResponse<UserResponse>>(
      "/auth/me",
    );

    console.log(
      "[AUTH TRACE] getCurrentUser: HTTP success",
      response.status,
    );

    return response.data.data;
  } catch (error) {
    console.error(
      "[AUTH TRACE] getCurrentUser: FAILED",
      error,
    );
    throw error;
  }
}

export async function logout(): Promise<void> {
  await clearAccessToken();
}
