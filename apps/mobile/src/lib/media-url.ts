import { env } from "@/config/env";

export function resolveMediaUrl(url: string): string {
  try {
    const parsed = new URL(url);
    const configured = new URL(env.apiUrl);

    if (
      parsed.hostname === "localhost" ||
      parsed.hostname === "127.0.0.1"
    ) {
      parsed.protocol = configured.protocol;
      parsed.hostname = configured.hostname;
      parsed.port = configured.port;
    }

    return parsed.toString();
  } catch {
    if (url.startsWith("/")) {
      return `${env.apiUrl.replace(/\/api\/v1$/, "")}${url}`;
    }

    return url;
  }
}
