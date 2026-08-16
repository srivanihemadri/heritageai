import React from "react";

export interface SectionProps extends React.HTMLAttributes<HTMLElement> {
  as?: "section" | "div" | "article";
}

export function Section({
  as = "section",
  className = "",
  children,
  ...props
}: SectionProps) {
  const Tag = as;

  return (
    <Tag className={`heritage-section ${className}`} {...props}>
      {children}
    </Tag>
  );
}
