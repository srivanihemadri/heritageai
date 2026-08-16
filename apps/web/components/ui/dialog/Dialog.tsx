"use client";

import React, { useEffect } from "react";

export interface DialogProps {
  open: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
}

export function Dialog({
  open,
  onClose,
  title,
  children,
}: DialogProps) {
  useEffect(() => {
    if (!open) return;

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };

    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
      aria-label={title}
    >
      <button
        type="button"
        aria-label="Close dialog"
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
      />

      <div className="heritage-glass-strong relative z-10 w-full max-w-lg overflow-hidden rounded-[var(--radius-glass)]">
        {title ? (
          <div className="border-b border-[var(--glass-border)] px-6 py-5">
            <h2 className="text-lg font-semibold text-[var(--heritage-ivory)]">
              {title}
            </h2>
          </div>
        ) : null}

        <div className="p-6">
          {children}
        </div>
      </div>
    </div>
  );
}
