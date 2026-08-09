import apiClient from "@/lib/api-client";
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

  const response = await apiClient.post<TokenResponse>(
    "/api/v1/auth/login",
    formData,
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    },
  );

  return response.data;
}

export async function getCurrentUser(): Promise<UserResponse> {
  const response = await apiClient.get<APIResponse<UserResponse>>(
    "/api/v1/auth/me",
  );

  return response.data.data;
}
