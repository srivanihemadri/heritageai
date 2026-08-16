import React from "react";

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "glass" | "strong" | "solid";
  interactive?: boolean;
}

export function Card({
  variant = "glass",
  interactive = false,
  className = "",
  children,
  ...props
}: CardProps) {
  const variantClass = {
    glass: "heritage-glass",
    strong: "heritage-glass-strong",
    solid: "heritage-glass-solid",
  }[variant];

  return (
    <div
      className={`${variantClass} rounded-[var(--radius-card)] ${
        interactive ? "cursor-pointer hover:-translate-y-1" : ""
      } ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({
  className = "",
  children,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={`p-5 sm:p-6 ${className}`} {...props}>
      {children}
    </div>
  );
}

export function CardContent({
  className = "",
  children,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={`px-5 pb-5 sm:px-6 sm:pb-6 ${className}`} {...props}>
      {children}
    </div>
  );
}

export function CardFooter({
  className = "",
  children,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={`border-t border-[var(--glass-border)] px-5 py-4 sm:px-6 ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
