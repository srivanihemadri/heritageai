import React from "react";

export interface ContainerProps
  extends React.HTMLAttributes<HTMLDivElement> {
  size?: "default" | "wide" | "narrow";
}

export function Container({
  size = "default",
  className = "",
  children,
  ...props
}: ContainerProps) {
  const widths = {
    narrow: "max-w-4xl",
    default: "max-w-7xl",
    wide: "max-w-[1440px]",
  };

  return (
    <div
      className={`mx-auto w-[calc(100%-2rem)] sm:w-[calc(100%-3rem)] lg:w-[calc(100%-4rem)] ${widths[size]} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
