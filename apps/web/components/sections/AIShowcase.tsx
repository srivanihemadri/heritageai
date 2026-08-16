"use client";

import Link from "next/link";
import { motion, useReducedMotion } from "framer-motion";
import {
  ArrowRight,
  Bot,
  Camera,
  CheckCircle2,
  FileSearch,
  ImagePlus,
  MessageCircle,
  ScanSearch,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

const EASE = [0.22, 1, 0.36, 1] as const;

const guideSteps = [
  "Your question",
  "Verified evidence",
  "Grounded answer",
];

const scannerSteps = [
  "Upload a photo",
  "AI analyzes it",
  "Understand the result",
];

export default function AIShowcase() {
  const reduceMotion = useReducedMotion();

  return (
    <section
      id="ai"
      className="relative overflow-hidden py-24 sm:py-32"
    >
      <div className="pointer-events-none absolute left-1/2 top-1/4 h-[420px] w-[420px] -translate-x-1/2 rounded-full bg-[rgba(212,175,90,0.045)] blur-[130px]" />

      <div className="heritage-container relative">
        {/* ---------------------------------------------------------------- */}
        {/* Heading */}
        {/* ---------------------------------------------------------------- */}

        <motion.div
          initial={{
            opacity: 0,
            y: reduceMotion ? 0 : 20,
          }}
          whileInView={{
            opacity: 1,
            y: 0,
          }}
          viewport={{
            once: true,
            amount: 0.2,
          }}
          transition={{
            duration: reduceMotion ? 0 : 0.7,
            ease: EASE,
          }}
          className="mx-auto max-w-3xl text-center"
        >
          <div className="heritage-badge mx-auto w-fit">
            <Sparkles
              className="h-3.5 w-3.5 text-[var(--heritage-gold-light)]"
              aria-hidden="true"
            />
            Heritage intelligence
          </div>

          <h2 className="mt-5 text-balance text-3xl font-semibold tracking-[-0.045em] text-[var(--heritage-ivory)] sm:text-4xl lg:text-5xl">
            AI that helps you
            <span className="heritage-gold-gradient"> understand heritage.</span>
          </h2>

          <p className="mx-auto mt-5 max-w-2xl text-sm leading-7 text-[var(--heritage-muted)] sm:text-base">
            Ask questions about heritage or use a photograph to explore what
            you are seeing. HeritageAI brings conversational knowledge and
            visual intelligence into one experience.
          </p>
        </motion.div>

        {/* ---------------------------------------------------------------- */}
        {/* AI Guide */}
        {/* ---------------------------------------------------------------- */}

        <motion.article
          initial={{
            opacity: 0,
            y: reduceMotion ? 0 : 28,
          }}
          whileInView={{
            opacity: 1,
            y: 0,
          }}
          viewport={{
            once: true,
            amount: 0.15,
          }}
          transition={{
            duration: reduceMotion ? 0 : 0.75,
            ease: EASE,
          }}
          className="heritage-glass-strong mt-12 overflow-hidden rounded-[30px] p-2 sm:p-3"
        >
          <div className="grid overflow-hidden rounded-[25px] border border-white/[0.06] lg:grid-cols-[0.9fr_1.1fr]">
            <div className="relative flex min-h-[430px] flex-col justify-between overflow-hidden bg-[rgba(212,175,90,0.035)] p-6 sm:p-8 lg:p-10">
              <div className="pointer-events-none absolute right-[-100px] top-[-100px] h-64 w-64 rounded-full border border-[var(--glass-border)] opacity-40" />

              <div>
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl border border-[var(--glass-border-strong)] bg-[rgba(212,175,90,0.08)]">
                  <Bot
                    className="h-5 w-5 text-[var(--heritage-gold-light)]"
                    aria-hidden="true"
                  />
                </div>

                <p className="mt-7 text-[10px] font-semibold uppercase tracking-[0.2em] text-[var(--heritage-gold-light)]">
                  AI Heritage Guide
                </p>

                <h3 className="mt-3 max-w-md text-2xl font-semibold tracking-[-0.035em] text-[var(--heritage-ivory)] sm:text-3xl">
                  Ask about the story behind a place.
                </h3>

                <p className="mt-4 max-w-md text-sm leading-7 text-[var(--heritage-muted)]">
                  Ask natural-language questions and let HeritageAI use
                  available heritage evidence to construct a grounded answer.
                </p>
              </div>

              <div className="mt-8 flex flex-wrap gap-2">
                {guideSteps.map((step, index) => (
                  <div
                    key={step}
                    className="flex items-center gap-2 rounded-xl border border-[var(--glass-border)] bg-white/[0.025] px-3 py-2"
                  >
                    <span className="text-[10px] font-semibold text-[var(--heritage-gold)]">
                      0{index + 1}
                    </span>
                    <span className="text-xs text-[var(--heritage-muted)]">
                      {step}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div className="flex items-center p-5 sm:p-8 lg:p-10">
              <div className="heritage-glass w-full rounded-[24px] p-5 sm:p-6">
                <div className="flex items-center gap-3 border-b border-[var(--glass-border)] pb-4">
                  <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[rgba(212,175,90,0.09)]">
                    <MessageCircle
                      className="h-4 w-4 text-[var(--heritage-gold-light)]"
                      aria-hidden="true"
                    />
                  </div>

                  <div>
                    <p className="text-xs font-semibold text-[var(--heritage-ivory)]">
                      HeritageAI Guide
                    </p>
                    <p className="text-[10px] text-[var(--heritage-muted)]">
                      Grounded heritage knowledge
                    </p>
                  </div>

                  <span className="ml-auto flex items-center gap-1.5 text-[10px] text-[var(--heritage-gold-light)]">
                    <span className="h-1.5 w-1.5 rounded-full bg-[var(--heritage-gold)]" />
                    Ready
                  </span>
                </div>

                <div className="mt-5 rounded-2xl border border-[var(--glass-border)] bg-white/[0.02] p-4">
                  <p className="text-[10px] font-semibold uppercase tracking-[0.14em] text-[var(--heritage-bronze)]">
                    Question
                  </p>

                  <p className="mt-2 text-sm leading-6 text-[var(--heritage-ivory)]">
                    Why is this temple architecturally significant?
                  </p>
                </div>

                <div className="ml-5 mt-3 rounded-2xl border border-[var(--glass-border)] bg-[rgba(212,175,90,0.045)] p-4 sm:ml-10">
                  <div className="flex items-center gap-2">
                    <ShieldCheck
                      className="h-3.5 w-3.5 text-[var(--heritage-gold-light)]"
                      aria-hidden="true"
                    />

                    <span className="text-[10px] font-semibold uppercase tracking-[0.13em] text-[var(--heritage-gold-light)]">
                      Grounded response
                    </span>
                  </div>

                  <p className="mt-3 text-sm leading-6 text-[var(--heritage-muted)]">
                    Answers are designed to stay within the available
                    HeritageAI evidence rather than presenting unsupported
                    historical claims as facts.
                  </p>

                  <div className="mt-4 flex flex-wrap gap-2">
                    <span className="rounded-lg border border-[var(--glass-border)] px-2.5 py-1 text-[9px] text-[var(--heritage-muted)]">
                      Evidence
                    </span>
                    <span className="rounded-lg border border-[var(--glass-border)] px-2.5 py-1 text-[9px] text-[var(--heritage-muted)]">
                      Sources
                    </span>
                    <span className="rounded-lg border border-[var(--glass-border)] px-2.5 py-1 text-[9px] text-[var(--heritage-muted)]">
                      Grounded
                    </span>
                  </div>
                </div>

                <Link
                  href="/chat"
                  className="heritage-button heritage-button-gold group mt-5 w-full"
                >
                  Ask HeritageAI
                  <ArrowRight
                    className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-1"
                    aria-hidden="true"
                  />
                </Link>
              </div>
            </div>
          </div>
        </motion.article>

        {/* ---------------------------------------------------------------- */}
        {/* Scanner */}
        {/* ---------------------------------------------------------------- */}

        <motion.article
          initial={{
            opacity: 0,
            y: reduceMotion ? 0 : 28,
          }}
          whileInView={{
            opacity: 1,
            y: 0,
          }}
          viewport={{
            once: true,
            amount: 0.15,
          }}
          transition={{
            duration: reduceMotion ? 0 : 0.75,
            delay: reduceMotion ? 0 : 0.08,
            ease: EASE,
          }}
          className="heritage-glass-strong mt-4 overflow-hidden rounded-[30px] p-2 sm:p-3"
        >
          <div className="grid overflow-hidden rounded-[25px] border border-white/[0.06] lg:grid-cols-[1.1fr_0.9fr]">
            <div className="relative order-2 flex items-center p-5 sm:p-8 lg:order-1 lg:p-10">
              <div className="w-full">
                <div className="relative mx-auto max-w-lg overflow-hidden rounded-[26px] border border-[var(--glass-border)] bg-[var(--heritage-charcoal)] p-2">
                  <div className="relative aspect-[4/3] overflow-hidden rounded-[20px] bg-[rgba(11,9,7,0.8)]">
                    <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_40%,rgba(212,175,90,0.10),transparent_45%)]" />

                    <div className="absolute inset-6 rounded-[18px] border border-[var(--glass-border)]" />

                    <div className="absolute left-1/2 top-1/2 flex -translate-x-1/2 -translate-y-1/2 flex-col items-center">
                      <div className="flex h-16 w-16 items-center justify-center rounded-[22px] border border-[var(--glass-border-strong)] bg-[rgba(212,175,90,0.08)] shadow-[0_0_40px_rgba(212,175,90,0.10)]">
                        <ScanSearch
                          className="h-7 w-7 text-[var(--heritage-gold-light)]"
                          aria-hidden="true"
                        />
                      </div>

                      <p className="mt-4 text-xs font-semibold text-[var(--heritage-ivory)]">
                        Heritage Scanner
                      </p>

                      <p className="mt-1 text-[10px] text-[var(--heritage-muted)]">
                        Visual heritage intelligence
                      </p>
                    </div>

                    <div className="absolute left-8 top-8 h-5 w-5 border-l border-t border-[var(--heritage-gold)]" />
                    <div className="absolute right-8 top-8 h-5 w-5 border-r border-t border-[var(--heritage-gold)]" />
                    <div className="absolute bottom-8 left-8 h-5 w-5 border-b border-l border-[var(--heritage-gold)]" />
                    <div className="absolute bottom-8 right-8 h-5 w-5 border-b border-r border-[var(--heritage-gold)]" />
                  </div>
                </div>
              </div>
            </div>

            <div className="order-1 flex flex-col justify-center p-6 sm:p-8 lg:order-2 lg:p-10">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl border border-[var(--glass-border-strong)] bg-[rgba(212,175,90,0.08)]">
                <Camera
                  className="h-5 w-5 text-[var(--heritage-gold-light)]"
                  aria-hidden="true"
                />
              </div>

              <p className="mt-7 text-[10px] font-semibold uppercase tracking-[0.2em] text-[var(--heritage-gold-light)]">
                Heritage Scanner
              </p>

              <h3 className="mt-3 text-2xl font-semibold tracking-[-0.035em] text-[var(--heritage-ivory)] sm:text-3xl">
                Let a photograph become a doorway into history.
              </h3>

              <p className="mt-4 text-sm leading-7 text-[var(--heritage-muted)]">
                Upload an image of a heritage place and HeritageAI can analyze
                the visual evidence, return structured identification
                information and communicate uncertainty when the evidence is
                insufficient.
              </p>

              <div className="mt-7 space-y-3">
                {scannerSteps.map((step, index) => (
                  <div
                    key={step}
                    className="flex items-center gap-3 rounded-xl border border-[var(--glass-border)] bg-white/[0.02] px-4 py-3"
                  >
                    <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-[rgba(212,175,90,0.08)] text-[10px] font-semibold text-[var(--heritage-gold)]">
                      0{index + 1}
                    </span>

                    <span className="text-xs text-[var(--heritage-muted)]">
                      {step}
                    </span>

                    {index < 2 && (
                      <CheckCircle2
                        className="ml-auto h-3.5 w-3.5 text-[var(--heritage-gold)]"
                        aria-hidden="true"
                      />
                    )}
                  </div>
                ))}
              </div>

              <Link
                href="/scanner"
                className="heritage-button heritage-button-glass group mt-7 w-full sm:w-fit"
              >
                Try Heritage Scanner
                <ArrowRight
                  className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-1"
                  aria-hidden="true"
                />
              </Link>
            </div>
          </div>
        </motion.article>

        {/* ---------------------------------------------------------------- */}
        {/* Trust statement */}
        {/* ---------------------------------------------------------------- */}

        <motion.div
          initial={{
            opacity: 0,
            y: reduceMotion ? 0 : 14,
          }}
          whileInView={{
            opacity: 1,
            y: 0,
          }}
          viewport={{
            once: true,
            amount: 0.2,
          }}
          transition={{
            duration: reduceMotion ? 0 : 0.6,
            ease: EASE,
          }}
          className="mt-5 grid gap-3 sm:grid-cols-3"
        >
          <div className="heritage-glass rounded-2xl p-4">
            <FileSearch
              className="h-4 w-4 text-[var(--heritage-gold-light)]"
              aria-hidden="true"
            />
            <p className="mt-3 text-xs font-semibold text-[var(--heritage-ivory)]">
              Evidence-aware
            </p>
            <p className="mt-1 text-xs leading-5 text-[var(--heritage-muted)]">
              AI experiences are designed around available evidence.
            </p>
          </div>

          <div className="heritage-glass rounded-2xl p-4">
            <ShieldCheck
              className="h-4 w-4 text-[var(--heritage-gold-light)]"
              aria-hidden="true"
            />
            <p className="mt-3 text-xs font-semibold text-[var(--heritage-ivory)]">
              Uncertainty matters
            </p>
            <p className="mt-1 text-xs leading-5 text-[var(--heritage-muted)]">
              Insufficient evidence should remain insufficient.
            </p>
          </div>

          <div className="heritage-glass rounded-2xl p-4">
            <ImagePlus
              className="h-4 w-4 text-[var(--heritage-gold-light)]"
              aria-hidden="true"
            />
            <p className="mt-3 text-xs font-semibold text-[var(--heritage-ivory)]">
              Multimodal
            </p>
            <p className="mt-1 text-xs leading-5 text-[var(--heritage-muted)]">
              Explore heritage through both questions and images.
            </p>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
