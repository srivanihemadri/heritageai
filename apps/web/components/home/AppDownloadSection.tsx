"use client";

import { Download, Smartphone, Sparkles } from "lucide-react";

import { useEffect, useState } from "react";
import { useAuth } from "@/providers/AuthProvider";

const ANDROID_DOWNLOAD_URL =
  "https://github.com/srivanihemadri/heritageai/releases/download/v1.0.0/HeritageAI.apk";

export default function AppDownloadSection() {
  const { isAuthenticated, isLoading } = useAuth();
  const [platform, setPlatform] = useState<"android" | "ios" | null>(null);

  useEffect(() => {
    if (isLoading || !isAuthenticated) {
      return;
    }

    if (window.location.hash === "#download-app") {
      requestAnimationFrame(() => {
        document.getElementById("download-app")?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      });
    }
  }, [isAuthenticated, isLoading]);

  if (isLoading || !isAuthenticated) {
    return null;
  }

  return (
    <section className="relative overflow-hidden py-14 sm:py-16">
      <div className="heritage-container">
        <div className="heritage-glass-strong mx-auto mb-8 max-w-5xl rounded-[26px] p-5 sm:p-6">
          <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-sm font-semibold text-[var(--heritage-ivory)]">
                Still curious?
              </p>

              <p className="mt-1 max-w-2xl text-xs leading-5 text-[var(--heritage-muted)] sm:text-sm">
                Discover more heritage and take the HeritageAI experience with
                you wherever you go.
              </p>
            </div>

            <a
              href="#download-app"
              className="heritage-button heritage-button-gold heritage-gold-glow min-h-11 shrink-0 px-5"
            >
              Download App
              <span aria-hidden="true">→</span>
            </a>
          </div>
        </div>

        <div
          id="download-app"
          className="heritage-glass-strong relative scroll-mt-24 overflow-hidden rounded-[32px] border border-[var(--glass-border-strong)]"
        >
          <div className="pointer-events-none absolute -right-24 -top-24 h-72 w-72 rounded-full bg-[rgba(212,175,90,0.08)] blur-[100px]" />
          <div className="pointer-events-none absolute -bottom-24 -left-24 h-72 w-72 rounded-full bg-[rgba(155,117,48,0.06)] blur-[100px]" />

          <div className="relative z-10 grid gap-0 lg:grid-cols-[1.05fr_0.95fr]">
            <div className="p-7 sm:p-10 lg:p-12">
              <div className="heritage-badge w-fit">
                <Sparkles
                  className="h-3.5 w-3.5 text-[var(--heritage-gold-light)]"
                  aria-hidden="true"
                />
                HeritageAI Mobile
              </div>

              <p className="mt-6 text-xs font-semibold uppercase tracking-[0.24em] text-[var(--heritage-gold-light)]">
                Continue the journey
              </p>

              <h2 className="mt-4 max-w-xl text-3xl font-semibold tracking-[-0.04em] text-[var(--heritage-ivory)] sm:text-4xl lg:text-5xl">
                Take HeritageAI with you.
              </h2>

              <p className="mt-5 max-w-xl text-sm leading-7 text-[var(--heritage-muted)] sm:text-base">
                Explore heritage places on the web, then continue your
                discovery in the HeritageAI mobile app with dedicated AI
                experiences built for the field.
              </p>

              <div className="mt-8 grid gap-3 sm:grid-cols-2">
                <div className="rounded-2xl border border-[var(--glass-border)] bg-white/[0.02] p-4">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[var(--heritage-gold-light)]">
                    Explore
                  </p>
                  <p className="mt-2 text-sm leading-6 text-[var(--heritage-muted)]">
                    Keep discovering heritage places wherever you go.
                  </p>
                </div>

                <div className="rounded-2xl border border-[var(--glass-border)] bg-white/[0.02] p-4">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[var(--heritage-gold-light)]">
                    Mobile
                  </p>
                  <p className="mt-2 text-sm leading-6 text-[var(--heritage-muted)]">
                    Access the dedicated HeritageAI mobile experience.
                  </p>
                </div>
              </div>
            </div>

            <div className="flex items-center border-t border-[var(--glass-border)] bg-white/[0.02] p-7 sm:p-10 lg:border-l lg:border-t-0 lg:p-12">
              <div className="w-full">
                <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl border border-[var(--glass-border)] bg-[rgba(212,175,90,0.08)]">
                  <Smartphone
                    className="h-7 w-7 text-[var(--heritage-gold-light)]"
                    aria-hidden="true"
                  />
                </div>

                <h3 className="mt-6 text-center text-2xl font-semibold text-[var(--heritage-ivory)]">
                  Download the app
                </h3>

                <p className="mx-auto mt-3 max-w-sm text-center text-sm leading-6 text-[var(--heritage-muted)]">
                  Choose your platform to continue.
                </p>

                <div className="mt-7 grid grid-cols-2 gap-3">
                  <button
                    type="button"
                    onClick={() => setPlatform("android")}
                    className={`min-h-12 rounded-xl border px-4 text-sm font-semibold transition-all ${
                      platform === "android"
                        ? "border-[var(--heritage-gold)] bg-[rgba(212,175,90,0.12)] text-[var(--heritage-gold-light)]"
                        : "border-[var(--glass-border)] bg-white/[0.02] text-[var(--heritage-muted)] hover:bg-white/[0.05] hover:text-[var(--heritage-ivory)]"
                    }`}
                  >
                    Android
                  </button>

                  <button
                    type="button"
                    onClick={() => setPlatform("ios")}
                    className={`min-h-12 rounded-xl border px-4 text-sm font-semibold transition-all ${
                      platform === "ios"
                        ? "border-[var(--heritage-gold)] bg-[rgba(212,175,90,0.12)] text-[var(--heritage-gold-light)]"
                        : "border-[var(--glass-border)] bg-white/[0.02] text-[var(--heritage-muted)] hover:bg-white/[0.05] hover:text-[var(--heritage-ivory)]"
                    }`}
                  >
                    iOS
                  </button>
                </div>

                {platform === "android" && (
                  <>
                    <a
                      href={ANDROID_DOWNLOAD_URL}
                      download
                      className="heritage-button heritage-button-gold mt-4 flex min-h-12 w-full items-center justify-center gap-2 px-6"
                    >
                      <Download className="h-4 w-4" aria-hidden="true" />
                      Download Android APK
                    </a>

                    <p className="mt-3 text-center text-[10px] uppercase tracking-[0.16em] text-[var(--heritage-bronze)]">
                      HeritageAI Android • Version 1.0.0
                    </p>
                  </>
                )}

                {platform === "ios" && (
                  <>
                    <button
                      type="button"
                      disabled
                      className="heritage-button heritage-button-gold mt-4 min-h-12 w-full cursor-not-allowed px-6 opacity-70"
                    >
                      <Download className="h-4 w-4" aria-hidden="true" />
                      Coming Soon to the App Store
                    </button>

                    <p className="mt-3 text-center text-[10px] uppercase tracking-[0.16em] text-[var(--heritage-bronze)]">
                      iOS version is currently under development
                    </p>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
