"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import {
  getCurrentUser,
  googleLogin as googleLoginRequest,
  login as loginRequest,
} from "@/services/auth";

import type {
  LoginRequest,
  UserResponse,
} from "@/types/auth";

interface AuthContextValue {
  user: UserResponse | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (data: LoginRequest) => Promise<UserResponse>;
  loginWithGoogle: (idToken: string) => Promise<UserResponse>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(
  undefined,
);

const ACCESS_TOKEN_KEY = "heritageai_access_token";

export function AuthProvider({
  children,
}: {
  children: ReactNode;
}) {
  const [user, setUser] = useState<UserResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const logout = useCallback(() => {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    setUser(null);
  }, []);

  const login = useCallback(async (data: LoginRequest) => {
    const token = await loginRequest(data);

    localStorage.setItem(
      ACCESS_TOKEN_KEY,
      token.access_token,
    );

    const currentUser = await getCurrentUser();

    setUser(currentUser);

    return currentUser;
  }, []);

  const loginWithGoogle = useCallback(
    async (idToken: string) => {
      const token = await googleLoginRequest(idToken);

      localStorage.setItem(
        ACCESS_TOKEN_KEY,
        token.access_token,
      );

      const currentUser = await getCurrentUser();

      setUser(currentUser);

      return currentUser;
    },
    [],
  );

  useEffect(() => {
    const restoreSession = async () => {
      const token = localStorage.getItem(
        ACCESS_TOKEN_KEY,
      );

      if (!token) {
        setIsLoading(false);
        return;
      }

      try {
        const currentUser = await getCurrentUser();
        setUser(currentUser);
      } catch {
        localStorage.removeItem(ACCESS_TOKEN_KEY);
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    void restoreSession();
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      isAuthenticated: Boolean(user),
      isLoading,
      login,
      loginWithGoogle,
      logout,
    }),
    [user, isLoading, login, loginWithGoogle, logout],
  );

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error(
      "useAuth must be used inside AuthProvider",
    );
  }

  return context;
}
