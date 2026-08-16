"use client";

import { ChangeEvent, useState } from "react";
import { useRouter } from "next/navigation";
import {
  Camera,
  CheckCircle2,
  ImagePlus,
  Loader2,
  MapPin,
  ShieldCheck,
  Sparkles,
  Upload,
} from "lucide-react";

import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { useAuth } from "@/providers/AuthProvider";
import {
  scanHeritageImage,
  type HeritageScannerResponse,
} from "@/services/ai";

export default function ScannerPage() {
  const router = useRouter();
  const { isAuthenticated, isLoading: authLoading } = useAuth();

  const [preview, setPreview] = useState("");
  const [result, setResult] = useState<HeritageScannerResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  if (!authLoading && !isAuthenticated) {
    router.replace("/login");
    return null;
  }

  async function handleFile(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    if (!["image/jpeg", "image/png", "image/webp"].includes(file.type)) {
      setError("Please upload a JPEG, PNG, or WEBP image.");
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setError("Image must be smaller than 10 MB.");
      return;
    }

    setError("");
    setResult(null);
    setPreview(URL.createObjectURL(file));
    setLoading(true);

    try {
      const response = await scanHeritageImage(file);
      setResult(response);
    } catch {
      setError(
        "HeritageAI could not analyze this image. Please try another image.",
      );
    } finally {
      setLoading(false);
    }
  }

  const scanner = result?.result;

  return (
    <>
      <Navbar />

      <main className="mx-auto min-h-[calc(100vh-100px)] max-w-6xl px-4 py-10 sm:px-6 lg:px-8">
        <section className="mx-auto max-w-3xl text-center">
          <div className="heritage-gold-glow mx-auto flex h-14 w-14 items-center justify-center rounded-2xl border border-[var(--glass-border-strong)] bg-[var(--glass-bg-strong)]">
            <Camera className="h-6 w-6 text-[var(--heritage-gold-light)]" />
          </div>

          <p className="mt-6 text-xs font-semibold uppercase tracking-[0.24em] text-[var(--heritage-gold)]">
            Heritage Scanner
          </p>

          <h1 className="mt-3 text-4xl font-semibold tracking-tight text-[var(--heritage-ivory)] sm:text-5xl">
            Point to the past.
          </h1>

          <p className="mx-auto mt-5 max-w-2xl text-base leading-7 text-[var(--heritage-muted)]">
            Upload a heritage image and let HeritageAI analyze its visual
            evidence, identity, context and confidence.
          </p>
        </section>

        <section className="mt-10 grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
          <div className="heritage-glass-strong rounded-[28px] p-5 sm:p-7">
            <label
              htmlFor="heritage-image"
              className="group flex min-h-[420px] cursor-pointer flex-col items-center justify-center overflow-hidden rounded-2xl border border-dashed border-[var(--glass-border-strong)] bg-black/20 p-6 text-center transition-all hover:border-[var(--heritage-gold)]/50"
            >
              {preview ? (
                <img
                  src={preview}
                  alt="Selected heritage image"
                  className="h-full max-h-[360px] w-full rounded-xl object-contain"
                />
              ) : (
                <>
                  <ImagePlus className="h-10 w-10 text-[var(--heritage-gold)]" />
                  <p className="mt-5 text-sm font-semibold text-[var(--heritage-ivory)]">
                    Upload a heritage image
                  </p>
                  <p className="mt-2 text-xs leading-6 text-[var(--heritage-muted)]">
                    JPEG, PNG or WEBP · Maximum 10 MB
                  </p>
                  <span className="mt-6 inline-flex items-center gap-2 rounded-xl border border-[var(--glass-border)] px-4 py-2.5 text-sm text-[var(--heritage-ivory)]">
                    <Upload className="h-4 w-4" />
                    Choose image
                  </span>
                </>
              )}

              <input
                id="heritage-image"
                type="file"
                accept="image/jpeg,image/png,image/webp"
                className="sr-only"
                onChange={handleFile}
              />
            </label>

            {loading && (
              <div className="mt-4 flex items-center justify-center gap-2 rounded-xl border border-[var(--glass-border)] bg-white/5 p-3 text-sm text-[var(--heritage-muted)]">
                <Loader2 className="h-4 w-4 animate-spin text-[var(--heritage-gold)]" />
                Analyzing visual evidence...
              </div>
            )}

            {error && (
              <div className="mt-4 rounded-xl border border-red-400/20 bg-red-400/5 p-4 text-sm text-red-200">
                {error}
              </div>
            )}
          </div>

          <div className="heritage-glass-strong rounded-[28px] p-5 sm:p-7">
            {!scanner ? (
              <div className="flex min-h-[420px] flex-col items-center justify-center text-center">
                <Sparkles className="h-8 w-8 text-[var(--heritage-gold)]" />
                <h2 className="mt-5 text-xl font-semibold text-[var(--heritage-ivory)]">
                  Your analysis will appear here
                </h2>
                <p className="mt-3 max-w-md text-sm leading-7 text-[var(--heritage-muted)]">
                  HeritageAI will clearly separate identification, visual
                  evidence, confidence and grounding instead of presenting
                  uncertain guesses as facts.
                </p>
              </div>
            ) : (
              <div>
                <div className="flex flex-wrap items-start justify-between gap-4">
                  <div>
                    <p className="text-xs uppercase tracking-[0.2em] text-[var(--heritage-gold)]">
                      Analysis
                    </p>

                    <h2 className="mt-2 text-2xl font-semibold text-[var(--heritage-ivory)]">
                      {scanner.identified_name ?? "Identification uncertain"}
                    </h2>
                  </div>

                  <span className="inline-flex items-center gap-1.5 rounded-full border border-[var(--glass-border)] bg-white/5 px-3 py-1.5 text-xs text-[var(--heritage-muted)]">
                    <ShieldCheck className="h-3.5 w-3.5 text-[var(--heritage-gold)]" />
                    {scanner.grounding_status.replace("_", " ")}
                  </span>
                </div>

                <div className="mt-6 grid gap-3 sm:grid-cols-2">
                  <div className="rounded-2xl border border-[var(--glass-border)] p-4">
                    <p className="text-xs text-[var(--heritage-muted)]">
                      Identification
                    </p>
                    <p className="mt-2 text-sm font-medium text-[var(--heritage-ivory)]">
                      {scanner.identification_status.replace("_", " ")}
                    </p>
                  </div>

                  <div className="rounded-2xl border border-[var(--glass-border)] p-4">
                    <p className="text-xs text-[var(--heritage-muted)]">
                      Confidence
                    </p>
                    <p className="mt-2 text-sm font-medium text-[var(--heritage-ivory)]">
                      {scanner.confidence_level} ·{" "}
                      {Math.round(scanner.confidence * 100)}%
                    </p>
                  </div>

                  {scanner.category && (
                    <div className="rounded-2xl border border-[var(--glass-border)] p-4">
                      <p className="text-xs text-[var(--heritage-muted)]">
                        Category
                      </p>
                      <p className="mt-2 text-sm text-[var(--heritage-ivory)]">
                        {scanner.category}
                      </p>
                    </div>
                  )}

                  {scanner.location && (
                    <div className="rounded-2xl border border-[var(--glass-border)] p-4">
                      <p className="flex items-center gap-1 text-xs text-[var(--heritage-muted)]">
                        <MapPin className="h-3.5 w-3.5" />
                        Location
                      </p>
                      <p className="mt-2 text-sm text-[var(--heritage-ivory)]">
                        {scanner.location}
                      </p>
                    </div>
                  )}
                </div>

                {scanner.description && (
                  <div className="mt-6">
                    <h3 className="text-sm font-semibold text-[var(--heritage-ivory)]">
                      Description
                    </h3>
                    <p className="mt-2 text-sm leading-7 text-[var(--heritage-muted)]">
                      {scanner.description}
                    </p>
                  </div>
                )}

                {scanner.visual_evidence.length > 0 && (
                  <div className="mt-6">
                    <h3 className="flex items-center gap-2 text-sm font-semibold text-[var(--heritage-ivory)]">
                      <CheckCircle2 className="h-4 w-4 text-[var(--heritage-gold)]" />
                      Visual evidence
                    </h3>

                    <ul className="mt-3 space-y-2">
                      {scanner.visual_evidence.map((item) => (
                        <li
                          key={item}
                          className="rounded-xl border border-[var(--glass-border)] bg-white/[0.025] p-3 text-sm leading-6 text-[var(--heritage-muted)]"
                        >
                          {item}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {scanner.alternative_matches.length > 0 && (
                  <div className="mt-6">
                    <h3 className="text-sm font-semibold text-[var(--heritage-ivory)]">
                      Alternative matches
                    </h3>

                    <div className="mt-3 flex flex-wrap gap-2">
                      {scanner.alternative_matches.map((match) => (
                        <span
                          key={match}
                          className="rounded-full border border-[var(--glass-border)] px-3 py-1.5 text-xs text-[var(--heritage-muted)]"
                        >
                          {match}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </section>
      </main>

      <Footer />
    </>
  );
}
