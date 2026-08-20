import axios from "axios";
import { GoogleSignin } from "@react-native-google-signin/google-signin";

import apiClient from "@/lib/api-client";
import { env } from "@/config/env";
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

async function configureGoogleSignIn(): Promise<void> {
  await GoogleSignin.configure({
    webClientId: env.googleWebClientId,
    offlineAccess: false,
  });
}

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

  await setAccessToken(response.data.access_token);

  return response.data;
}

export async function loginWithGoogle(
  idToken: string,
): Promise<TokenResponse> {
  const normalizedToken = idToken.trim();

  if (!normalizedToken) {
    throw new Error("Google ID token is required.");
  }

  console.log(
    "[AUTH TRACE] Google login: sending ID token",
  );

  const response = await axios.post<TokenResponse>(
    `${apiClient.defaults.baseURL}/auth/google`,
    {
      id_token: normalizedToken,
    },
    {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      timeout: 15000,
    },
  );

  console.log(
    "[AUTH TRACE] Google login: HTTP success",
    response.status,
  );

  await setAccessToken(response.data.access_token);

  console.log(
    "[AUTH TRACE] Google login: token storage success",
  );

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
  console.log(
    "[AUTH TRACE] logout: configuring Google Sign-In",
  );

  try {
    await configureGoogleSignIn();

    console.log(
      "[AUTH TRACE] logout: Google Sign-In configured",
    );

    await GoogleSignin.signOut();

    console.log(
      "[AUTH TRACE] logout: Google sign-out success",
    );
  } catch (error) {
    console.error(
      "[AUTH TRACE] logout: Google sign-out failed",
      error,
    );
  } finally {
    await clearAccessToken();

    console.log(
      "[AUTH TRACE] logout: HeritageAI access token cleared",
    );
  }
}
