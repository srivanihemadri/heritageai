const ACCESS_TOKEN_KEY = "heritageai_access_token";

let fallbackToken: string | null = null;

export async function getAccessToken(): Promise<string | null> {
  if (
    typeof globalThis !== "undefined" &&
    "localStorage" in globalThis
  ) {
    const storage = globalThis.localStorage;

    return storage.getItem(ACCESS_TOKEN_KEY);
  }

  return fallbackToken;
}

export async function setAccessToken(
  token: string,
): Promise<void> {
  if (
    typeof globalThis !== "undefined" &&
    "localStorage" in globalThis
  ) {
    globalThis.localStorage.setItem(
      ACCESS_TOKEN_KEY,
      token,
    );
    return;
  }

  fallbackToken = token;
}

export async function clearAccessToken(): Promise<void> {
  if (
    typeof globalThis !== "undefined" &&
    "localStorage" in globalThis
  ) {
    globalThis.localStorage.removeItem(
      ACCESS_TOKEN_KEY,
    );
    return;
  }

  fallbackToken = null;
}
