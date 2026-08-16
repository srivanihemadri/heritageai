import { create } from "zustand";

import {
  clearAccessToken,
  getAccessToken,
} from "@/storage/auth-storage";
import {
  getCurrentUser,
  login as loginRequest,
  logout as logoutRequest,
} from "@/services/auth";
import type {
  LoginRequest,
  UserResponse,
} from "@/types/auth";

type AuthStatus =
  | "loading"
  | "authenticated"
  | "unauthenticated";

interface AuthState {
  status: AuthStatus;
  user: UserResponse | null;
  initialize: () => Promise<void>;
  login: (credentials: LoginRequest) => Promise<void>;
  logout: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  status: "loading",
  user: null,

  initialize: async () => {
    try {
      const token = await getAccessToken();

      if (!token) {
        set({
          status: "unauthenticated",
          user: null,
        });
        return;
      }

      const user = await getCurrentUser();

      set({
        status: "authenticated",
        user,
      });
    } catch {
      await clearAccessToken();

      set({
        status: "unauthenticated",
        user: null,
      });
    }
  },

  login: async (credentials) => {
    await loginRequest(credentials);

    const user = await getCurrentUser();

    set({
      status: "authenticated",
      user,
    });
  },

  logout: async () => {
    await logoutRequest();

    set({
      status: "unauthenticated",
      user: null,
    });
  },
}));
