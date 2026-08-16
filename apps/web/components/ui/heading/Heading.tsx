import React from "react";

export interface HeadingProps
  extends React.HTMLAttributes<HTMLHeadingElement> {
  level?: 1 | 2 | 3 | 4 | 5 | 6;
  gradient?: boolean;
}

export function Heading({
  level = 2,
  gradient = false,
  className = "",
  children,
  ...props
}: HeadingProps) {
  const Tag = `h${level}` as keyof React.JSX.IntrinsicElements;

  const sizes = {
    1: "text-4xl sm:text-5xl lg:text-6xl",
    2: "text-3xl sm:text-4xl lg:text-5xl",
    3: "text-2xl sm:text-3xl",
    4: "text-xl sm:text-2xl",
    5: "text-lg",
    6: "text-base",
  };

  return React.createElement(
    Tag,
    {
      className: `${sizes[level]} font-semibold tracking-tight ${
        gradient ? "heritage-gold-gradient" : "text-[var(--heritage-ivory)]"
      } ${className}`,
      ...props,
    },
    children,
  );
}
