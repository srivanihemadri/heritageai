import React from "react";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "gold" | "muted";
}

export function Badge({
  variant = "default",
  className = "",
  children,
  ...props
}: BadgeProps) {
  const variantClass = {
    default:
      "bg-[rgba(212,175,90,0.09)] text-[var(--heritage-gold-light)]",
    gold:
      "bg-[rgba(212,175,90,0.16)] text-[var(--heritage-gold-light)]",
    muted:
      "bg-white/[0.04] text-[var(--heritage-muted)]",
  }[variant];

  return (
    <span
      className={`heritage-badge ${variantClass} ${className}`}
      {...props}
    >
      {children}
    </span>
  );
}
