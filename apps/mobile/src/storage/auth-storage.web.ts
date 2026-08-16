const ACCESS_TOKEN_KEY = "heritageai_access_token";

function getStorage(): Storage | null {
  if (typeof window === "undefined") {
    return null;
  }

  return window.localStorage;
}

export async function getAccessToken(): Promise<string | null> {
  return getStorage()?.getItem(ACCESS_TOKEN_KEY) ?? null;
}

export async function setAccessToken(
  token: string,
): Promise<void> {
  getStorage()?.setItem(
    ACCESS_TOKEN_KEY,
    token,
  );
}

export async function clearAccessToken(): Promise<void> {
  getStorage()?.removeItem(
    ACCESS_TOKEN_KEY,
  );
}
