"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { useAuth } from "@/providers/AuthProvider";

export default function ProfilePage() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading, logout } = useAuth();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.replace("/login");
    }
  }, [isLoading, isAuthenticated, router]);

  if (isLoading || !user) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[var(--heritage-black)]">
        <p className="text-sm text-[var(--heritage-muted)]">
          Loading profile...
        </p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-[var(--heritage-black)] px-4 py-24 sm:px-6">
      <section className="mx-auto w-full max-w-2xl rounded-3xl border border-[var(--glass-border)] bg-white/[0.03] p-8 backdrop-blur-xl">
        <div className="flex flex-col items-center text-center">
          <div className="flex h-20 w-20 items-center justify-center rounded-full bg-[rgba(212,175,90,0.12)] text-2xl font-semibold text-[var(--heritage-gold-light)]">
            {user.full_name?.charAt(0)?.toUpperCase() || "U"}
          </div>

          <p className="mt-5 text-xs font-semibold uppercase tracking-[0.3em] text-[var(--heritage-gold)]">
            HERITAGEAI PROFILE
          </p>

          <h1 className="mt-3 text-3xl font-semibold text-[var(--heritage-ivory)]">
            {user.full_name}
          </h1>

          <p className="mt-2 text-sm text-[var(--heritage-muted)]">
            {user.email}
          </p>
        </div>

        <div className="mt-8 grid gap-3 sm:grid-cols-2">
          <div className="rounded-2xl border border-[var(--glass-border)] bg-white/[0.02] p-5">
            <p className="text-xs uppercase tracking-[0.18em] text-[var(--heritage-muted)]">
              Role
            </p>
            <p className="mt-2 text-sm font-medium text-[var(--heritage-ivory)]">
              {user.role}
            </p>
          </div>

          <div className="rounded-2xl border border-[var(--glass-border)] bg-white/[0.02] p-5">
            <p className="text-xs uppercase tracking-[0.18em] text-[var(--heritage-muted)]">
              Account
            </p>
            <p className="mt-2 text-sm font-medium text-[var(--heritage-gold-light)]">
              {user.is_active ? "Active" : "Inactive"}
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={() => {
            logout();
            router.replace("/");
          }}
          className="mt-8 w-full rounded-2xl border border-[var(--glass-border)] bg-white/[0.04] px-5 py-3 text-sm font-semibold text-[var(--heritage-ivory)] transition hover:bg-white/[0.08]"
        >
          Logout
        </button>
      </section>
    </main>
  );
}
