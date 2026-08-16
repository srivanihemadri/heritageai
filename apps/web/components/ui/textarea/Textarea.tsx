import React from "react";

export interface TextareaProps
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {}

export const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className = "", ...props }, ref) => {
    return (
      <textarea
        ref={ref}
        className={`heritage-input min-h-28 resize-y ${className}`}
        {...props}
      />
    );
  },
);

Textarea.displayName = "Textarea";
