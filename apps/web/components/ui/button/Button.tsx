import React from "react";

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "glass" | "gold" | "ghost";
  size?: "sm" | "md" | "lg";
  loading?: boolean;
}

const sizeClasses = {
  sm: "min-h-9 px-3 text-sm",
  md: "min-h-11 px-4 text-sm",
  lg: "min-h-12 px-6 text-base",
};

const variantClasses = {
  glass: "heritage-button-glass",
  gold: "heritage-button-gold",
  ghost:
    "border border-transparent bg-transparent text-[var(--heritage-muted)] hover:border-[var(--glass-border)] hover:text-[var(--heritage-ivory)]",
};

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className = "",
      variant = "glass",
      size = "md",
      loading = false,
      disabled,
      children,
      ...props
    },
    ref,
  ) => {
    return (
      <button
        ref={ref}
        disabled={disabled || loading}
        className={`heritage-button ${sizeClasses[size]} ${variantClasses[variant]} ${className}`}
        {...props}
      >
        {loading ? (
          <span
            aria-hidden="true"
            className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent"
          />
        ) : null}

        {children}
      </button>
    );
  },
);

Button.displayName = "Button";
