"use client";

import React, { useEffect } from "react";

export interface ModalProps {
  open: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  size?: "sm" | "md" | "lg";
}

export function Modal({
  open,
  onClose,
  title,
  children,
  size = "md",
}: ModalProps) {
  useEffect(() => {
    if (!open) return;

    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };

    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.body.style.overflow = previousOverflow;
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [open, onClose]);

  if (!open) return null;

  const sizes = {
    sm: "max-w-md",
    md: "max-w-xl",
    lg: "max-w-3xl",
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto p-4 sm:p-6"
      role="dialog"
      aria-modal="true"
      aria-label={title}
    >
      <button
        type="button"
        aria-label="Close modal"
        className="fixed inset-0 bg-black/65 backdrop-blur-md"
        onClick={onClose}
      />

      <div
        className={`heritage-glass-strong relative z-10 w-full ${sizes[size]} overflow-hidden rounded-[var(--radius-glass)]`}
      >
        <div className="flex items-center justify-between border-b border-[var(--glass-border)] px-5 py-4 sm:px-6">
          {title ? (
            <h2 className="text-lg font-semibold text-[var(--heritage-ivory)]">
              {title}
            </h2>
          ) : (
            <span />
          )}

          <button
            type="button"
            onClick={onClose}
            aria-label="Close modal"
            className="rounded-full px-2 py-1 text-xl leading-none text-[var(--heritage-muted)] transition hover:bg-white/5 hover:text-[var(--heritage-ivory)]"
          >
            ×
          </button>
        </div>

        <div className="p-5 sm:p-6">
          {children}
        </div>
      </div>
    </div>
  );
}
