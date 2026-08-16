import React from "react";

export interface SpinnerProps {
  size?: "sm" | "md" | "lg";
  label?: string;
}

export function Spinner({
  size = "md",
  label = "Loading",
}: SpinnerProps) {
  const sizes = {
    sm: "h-4 w-4 border-2",
    md: "h-6 w-6 border-2",
    lg: "h-10 w-10 border-[3px]",
  };

  return (
    <span
      role="status"
      aria-label={label}
      className={`inline-block animate-spin rounded-full border-[var(--heritage-gold)] border-t-transparent ${sizes[size]}`}
    />
  );
}
