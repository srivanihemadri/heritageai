export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface UserResponse {
  profile_image_url: string | null;
  id: string;
  full_name: string;
  email: string;
  role: string;
  is_active: boolean;
}

export interface APIResponse<T> {
  success: boolean;
  data: T;
  message: string;
}
