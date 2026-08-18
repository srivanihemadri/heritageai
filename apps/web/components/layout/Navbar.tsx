"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Menu, X } from "lucide-react";
import { usePathname } from "next/navigation";
import Logo from "../ui/logo/Logo";
import { useAuth } from "@/providers/AuthProvider";

const navigation = [
  { label: "Home", href: "/" },
  { label: "Explorer", href: "/explorer" },
  { label: "About", href: "/about" },
];

export default function Navbar() {
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);
  const { user, isAuthenticated, logout } = useAuth();

  useEffect(() => {
    setIsOpen(false);
  }, [pathname]);

  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setIsOpen(false);
      }
    };

    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [isOpen]);

  if (pathname === "/login") {
    return null;
  }

  const isActive = (href: string) => {
    if (href === "/") {
      return pathname === "/";
    }

    return pathname === href || pathname.startsWith(`${href}/`);
  };

  return (
    <header className="sticky top-0 z-50 w-full px-3 pt-3 sm:px-5 sm:pt-5">
      <nav
        className="heritage-nav-glass mx-auto flex max-w-7xl items-center justify-between rounded-[var(--radius-glass)] px-3 py-2.5 sm:px-4"
        aria-label="Primary navigation"
      >
        <Logo />

        <div className="hidden items-center gap-1 md:flex">
          {navigation.map((item) => {
            const active = isActive(item.href);

            return (
              <Link
                key={item.href}
                href={item.href}
                aria-current={active ? "page" : undefined}
                className={`relative rounded-xl px-4 py-2.5 text-sm font-medium transition-all duration-200 ${
                  active
                    ? "bg-[rgba(212,175,90,0.10)] text-[var(--heritage-gold-light)]"
                    : "text-[var(--heritage-muted)] hover:bg-white/[0.04] hover:text-[var(--heritage-ivory)]"
                }`}
              >
                {item.label}

                {active && (
                  <span className="absolute inset-x-4 -bottom-px h-px bg-gradient-to-r from-transparent via-[var(--heritage-gold)] to-transparent" />
                )}
              </Link>
            );
          })}

          {isAuthenticated && user && (
            <Link
              href="/#download-app"
              className="relative rounded-xl px-4 py-2.5 text-sm font-medium text-[var(--heritage-muted)] transition-all duration-200 hover:bg-white/[0.04] hover:text-[var(--heritage-ivory)]"
            >
              Download App
            </Link>
          )}
        </div>

        <div className="hidden items-center gap-2 md:flex">
          {isAuthenticated && user ? (
            <div className="relative flex items-center gap-2">
              <Link
                href="/profile"
                className="flex min-h-10 items-center gap-2 rounded-xl border border-[var(--glass-border)] bg-white/[0.03] px-3 py-2 text-sm font-medium text-[var(--heritage-ivory)] transition-all hover:bg-white/[0.06]"
              >
                {user.profile_image_url ? (
                  <img
                    src={user.profile_image_url}
                    alt={`${user.full_name || "HeritageAI"} profile`}
                    className="h-7 w-7 rounded-full object-cover"
                  />
                ) : (
                  <span className="flex h-7 w-7 items-center justify-center rounded-full bg-[rgba(212,175,90,0.12)] text-xs font-semibold text-[var(--heritage-gold-light)]">
                    {user.full_name?.charAt(0)?.toUpperCase() || "U"}
                  </span>
                )}
                <span className="max-w-32 truncate">
                  {user.full_name || "Profile"}
                </span>
              </Link>

              <button
                type="button"
                onClick={logout}
                className="heritage-button heritage-button-glass min-h-10 px-4 text-sm"
              >
                Leave
              </button>
            </div>
          ) : (
            <Link
              href="/login"
              className="heritage-button heritage-button-gold heritage-gold-glow min-h-10 px-5 text-sm"
            >
              Get In
            </Link>
          )}
        </div>

        <button
          type="button"
          aria-label={isOpen ? "Close navigation menu" : "Open navigation menu"}
          aria-expanded={isOpen}
          onClick={() => setIsOpen((open) => !open)}
          className="flex h-10 w-10 items-center justify-center rounded-xl border border-[var(--glass-border)] bg-white/[0.02] text-[var(--heritage-ivory)] transition-all hover:border-[var(--glass-border-hover)] hover:bg-white/[0.05] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--heritage-gold)] md:hidden"
        >
          {isOpen ? (
            <X size={20} strokeWidth={1.8} />
          ) : (
            <Menu size={20} strokeWidth={1.8} />
          )}
        </button>
      </nav>

      {isOpen && (
        <div className="heritage-glass mx-auto mt-2 max-w-7xl overflow-hidden rounded-[var(--radius-glass)] md:hidden">
          <div className="p-2">
            {navigation.map((item) => {
              const active = isActive(item.href);

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center justify-between rounded-xl px-4 py-3.5 text-sm font-medium transition-all ${
                    active
                      ? "bg-[rgba(212,175,90,0.10)] text-[var(--heritage-gold-light)]"
                      : "text-[var(--heritage-muted)] hover:bg-white/[0.04] hover:text-[var(--heritage-ivory)]"
                  }`}
                >
                  <span>{item.label}</span>

                  {active && (
                    <span className="h-1.5 w-1.5 rounded-full bg-[var(--heritage-gold)] shadow-[0_0_12px_rgba(212,175,90,0.55)]" />
                  )}
                </Link>
              );
            })}

            {isAuthenticated && user && (
              <Link
                href="/#download-app"
                onClick={() => setIsOpen(false)}
                className="flex items-center justify-between rounded-xl px-4 py-3.5 text-sm font-medium text-[var(--heritage-muted)] transition-all hover:bg-white/[0.04] hover:text-[var(--heritage-ivory)]"
              >
                <span>Download App</span>
              </Link>
            )}
          </div>

          <div className="border-t border-[var(--glass-border)] p-3">
            {isAuthenticated && user ? (
              <div className="space-y-2">
                <Link
                  href="/profile"
                  onClick={() => setIsOpen(false)}
                  className="flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium text-[var(--heritage-ivory)] transition-all hover:bg-white/[0.04]"
                >
                  {user.profile_image_url ? (
                    <img
                      src={user.profile_image_url}
                      alt={`${user.full_name || "HeritageAI"} profile`}
                      className="h-8 w-8 rounded-full object-cover"
                    />
                  ) : (
                    <span className="flex h-8 w-8 items-center justify-center rounded-full bg-[rgba(212,175,90,0.12)] text-xs font-semibold text-[var(--heritage-gold-light)]">
                      {user.full_name?.charAt(0)?.toUpperCase() || "U"}
                    </span>
                  )}
                  <span className="truncate">
                    {user.full_name || "Profile"}
                  </span>
                </Link>

                <button
                  type="button"
                  onClick={() => {
                    setIsOpen(false);
                    logout();
                  }}
                  className="heritage-button heritage-button-glass min-h-11 w-full text-sm"
                >
                  Leave
                </button>
              </div>
            ) : (
              <Link
                href="/login"
                className="heritage-button heritage-button-gold min-h-11 w-full text-sm"
              >
                Get In
              </Link>
            )}
          </div>
        </div>
      )}
    </header>
  );
}
