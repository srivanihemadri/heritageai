"use client";

import { useState } from "react";

interface UserAvatarProps {
  src?: string | null;
  name?: string | null;
  size?: "sm" | "md";
}

export default function UserAvatar({
  src,
  name,
  size = "sm",
}: UserAvatarProps) {
  const [failed, setFailed] = useState(false);

  const initial = name?.trim()?.charAt(0)?.toUpperCase() || "U";

  const sizeClass =
    size === "md" ? "h-8 w-8 text-sm" : "h-7 w-7 text-xs";

  if (!src || failed) {
    return (
      <span
        className={`flex ${sizeClass} shrink-0 items-center justify-center rounded-full bg-[rgba(212,175,90,0.12)] font-semibold text-[var(--heritage-gold-light)]`}
      >
        {initial}
      </span>
    );
  }

  return (
    <img
      src={src}
      alt={`${name || "HeritageAI"} profile`}
      className={`${sizeClass} shrink-0 rounded-full object-cover`}
      onError={() => setFailed(true)}
    />
  );
}
