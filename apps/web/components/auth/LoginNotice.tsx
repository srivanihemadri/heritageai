"use client";

import { useSearchParams } from "next/navigation";

export default function LoginNotice() {
  const searchParams = useSearchParams();

  if (searchParams.get("reason") !== "download-app") {
    return null;
  }

  return (
    <div
      role="status"
      className="mx-auto mb-6 w-full max-w-md rounded-2xl border border-[rgba(212,175,90,0.25)] bg-[rgba(212,175,90,0.06)] px-5 py-4 text-center"
    >
      <p className="text-sm font-semibold text-[var(--heritage-gold-light)]">
        Sign in to access the HeritageAI mobile app.
      </p>

      <p className="mt-1 text-xs leading-5 text-[var(--heritage-muted)]">
        Sign in first, then you can choose Android or iOS.
      </p>
    </div>
  );
}
