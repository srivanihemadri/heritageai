"use client";

import Link from "next/link";
import { motion, useReducedMotion } from "framer-motion";
import {
  ArrowRight,
  Camera,
  Compass,
  Map,
  MessageCircle,
  Sparkles,
} from "lucide-react";

const EASE = [0.22, 1, 0.36, 1] as const;

const steps = [
  {
    number: "01",
    title: "Discover",
    description:
      "Start with a place, monument, landmark or cultural story and explore what makes it meaningful.",
    icon: Compass,
    accent: "Explore heritage",
  },
  {
    number: "02",
    title: "Identify",
    description:
      "Use visual intelligence to understand heritage architecture and recognize what you are seeing.",
    icon: Camera,
    accent: "Visual intelligence",
  },
  {
    number: "03",
    title: "Understand",
    description:
      "Ask questions and explore historical context, architecture and cultural significance.",
    icon: MessageCircle,
    accent: "Grounded knowledge",
  },
  {
    number: "04",
    title: "Explore",
    description:
      "Follow the story deeper through related places, locations and connected heritage experiences.",
    icon: Map,
    accent: "Go deeper",
  },
];

export default function HowItWorks() {
  const reduceMotion = useReducedMotion();

  return (
    <section
      id="how-it-works"
      className="relative overflow-hidden py-24 sm:py-32"
    >
      <div className="pointer-events-none absolute left-1/2 top-20 h-72 w-72 -translate-x-1/2 rounded-full bg-[rgba(212,175,90,0.045)] blur-[100px]" />

      <div className="heritage-container relative">
        {/* ------------------------------------------------------------------ */}
        {/* Heading */}
        {/* ------------------------------------------------------------------ */}

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
            amount: 0.25,
          }}
          transition={{
            duration: reduceMotion ? 0 : 0.65,
            ease: EASE,
          }}
          className="mx-auto max-w-2xl text-center"
        >
          <div className="heritage-badge mx-auto w-fit">
            <Sparkles
              className="h-3.5 w-3.5 text-[var(--heritage-gold-light)]"
              aria-hidden="true"
            />
            How HeritageAI works
          </div>

          <h2 className="mt-5 text-balance text-3xl font-semibold tracking-[-0.045em] text-[var(--heritage-ivory)] sm:text-4xl lg:text-5xl">
            From seeing a place to
            <span className="heritage-gold-gradient"> understanding it.</span>
          </h2>

          <p className="mx-auto mt-5 max-w-xl text-sm leading-7 text-[var(--heritage-muted)] sm:text-base">
            HeritageAI connects discovery, visual understanding and historical
            knowledge into one continuous heritage experience.
          </p>
        </motion.div>

        {/* ------------------------------------------------------------------ */}
        {/* Desktop progression */}
        {/* ------------------------------------------------------------------ */}

        <div className="relative mt-14 hidden lg:block">
          <div
            className="pointer-events-none absolute left-[12.5%] right-[12.5%] top-16 h-px bg-gradient-to-r from-transparent via-[var(--glass-border-strong)] to-transparent"
            aria-hidden="true"
          />

          <div className="grid grid-cols-4 gap-4">
            {steps.map((step, index) => {
              const Icon = step.icon;

              return (
                <motion.article
                  key={step.number}
                  initial={{
                    opacity: 0,
                    y: reduceMotion ? 0 : 24,
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
                    duration: reduceMotion ? 0 : 0.55,
                    delay: reduceMotion ? 0 : index * 0.08,
                    ease: EASE,
                  }}
                  whileHover={
                    reduceMotion
                      ? undefined
                      : {
                          y: -5,
                        }
                  }
                  className="relative"
                >
                  <div className="relative z-10 mx-auto flex h-14 w-14 items-center justify-center rounded-2xl border border-[var(--glass-border-strong)] bg-[var(--heritage-charcoal)] shadow-[0_0_28px_rgba(212,175,90,0.08)]">
                    <Icon
                      className="h-5 w-5 text-[var(--heritage-gold-light)]"
                      aria-hidden="true"
                    />
                  </div>

                  <div className="heritage-glass mt-7 min-h-[270px] rounded-[24px] p-6">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-semibold tracking-[0.16em] text-[var(--heritage-gold)]">
                        {step.number}
                      </span>

                      <span className="text-[10px] font-medium uppercase tracking-[0.14em] text-[var(--heritage-bronze)]">
                        {step.accent}
                      </span>
                    </div>

                    <h3 className="mt-6 text-xl font-semibold tracking-[-0.025em] text-[var(--heritage-ivory)]">
                      {step.title}
                    </h3>

                    <p className="mt-3 text-sm leading-6 text-[var(--heritage-muted)]">
                      {step.description}
                    </p>
                  </div>
                </motion.article>
              );
            })}
          </div>
        </div>

        {/* ------------------------------------------------------------------ */}
        {/* Mobile / tablet progression */}
        {/* ------------------------------------------------------------------ */}

        <div className="mt-12 lg:hidden">
          <div className="relative">
            <div
              className="pointer-events-none absolute bottom-8 left-[22px] top-8 w-px bg-gradient-to-b from-[var(--glass-border-strong)] via-[var(--glass-border)] to-transparent"
              aria-hidden="true"
            />

            <div className="space-y-4">
              {steps.map((step, index) => {
                const Icon = step.icon;

                return (
                  <motion.article
                    key={step.number}
                    initial={{
                      opacity: 0,
                      x: reduceMotion ? 0 : -14,
                    }}
                    whileInView={{
                      opacity: 1,
                      x: 0,
                    }}
                    viewport={{
                      once: true,
                      amount: 0.12,
                    }}
                    transition={{
                      duration: reduceMotion ? 0 : 0.5,
                      delay: reduceMotion ? 0 : index * 0.06,
                      ease: EASE,
                    }}
                    className="relative flex gap-4"
                  >
                    <div className="relative z-10 flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-[var(--glass-border-strong)] bg-[var(--heritage-charcoal)]">
                      <Icon
                        className="h-4 w-4 text-[var(--heritage-gold-light)]"
                        aria-hidden="true"
                      />
                    </div>

                    <div className="heritage-glass flex-1 rounded-[22px] p-5">
                      <div className="flex items-center justify-between gap-3">
                        <span className="text-xs font-semibold tracking-[0.16em] text-[var(--heritage-gold)]">
                          {step.number}
                        </span>

                        <span className="text-[9px] font-medium uppercase tracking-[0.12em] text-[var(--heritage-bronze)]">
                          {step.accent}
                        </span>
                      </div>

                      <h3 className="mt-3 text-lg font-semibold text-[var(--heritage-ivory)]">
                        {step.title}
                      </h3>

                      <p className="mt-2 text-sm leading-6 text-[var(--heritage-muted)]">
                        {step.description}
                      </p>
                    </div>
                  </motion.article>
                );
              })}
            </div>
          </div>
        </div>

        {/* ------------------------------------------------------------------ */}
        {/* CTA */}
        {/* ------------------------------------------------------------------ */}

        <motion.div
          initial={{
            opacity: 0,
            y: reduceMotion ? 0 : 16,
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
            delay: reduceMotion ? 0 : 0.1,
            ease: EASE,
          }}
          className="mt-10 flex justify-center"
        >
          <Link
            href="/explorer"
            className="heritage-button heritage-button-glass group min-h-11 px-5"
          >
            Start exploring
            <ArrowRight
              className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-1"
              aria-hidden="true"
            />
          </Link>
        </motion.div>
      </div>
    </section>
  );
}
