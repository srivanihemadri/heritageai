"use client";

import Link from "next/link";
import { motion, useReducedMotion } from "framer-motion";
import {
  ArrowRight,
  CalendarDays,
  MapPin,
  Sparkles,
  Landmark,
} from "lucide-react";

const EASE = [0.22, 1, 0.36, 1] as const;

export default function LivingHeritage() {
  const reduceMotion = useReducedMotion();

  return (
    <section
      id="heritage"
      className="relative overflow-hidden py-24 sm:py-32"
    >
      <div className="heritage-container">
        <motion.div
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
            amount: 0.2,
          }}
          transition={{
            duration: reduceMotion ? 0 : 0.7,
            ease: EASE,
          }}
          className="mb-10 max-w-2xl"
        >
          <div className="heritage-badge w-fit">
            <Landmark
              className="h-3.5 w-3.5 text-[var(--heritage-gold-light)]"
              aria-hidden="true"
            />
            Featured heritage
          </div>

          <h2 className="mt-5 text-balance text-3xl font-semibold tracking-[-0.04em] text-[var(--heritage-ivory)] sm:text-4xl lg:text-5xl">
            One place.
            <span className="heritage-gold-gradient"> Thousands of stories.</span>
          </h2>

          <p className="mt-5 max-w-xl text-sm leading-7 text-[var(--heritage-muted)] sm:text-base">
            Go beyond a photograph. Explore the architecture, history,
            cultural significance and context behind extraordinary heritage
            places.
          </p>
        </motion.div>

        <motion.div
          initial={{
            opacity: 0,
            y: reduceMotion ? 0 : 30,
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
            duration: reduceMotion ? 0 : 0.8,
            ease: EASE,
          }}
          className="heritage-glass-strong overflow-hidden rounded-[32px] p-2 sm:p-3"
        >
          <div className="grid overflow-hidden rounded-[26px] border border-white/[0.07] bg-[rgba(11,9,7,0.42)] lg:grid-cols-[1.05fr_0.95fr]">
            {/* ---------------------------------------------------------------- */}
            {/* Visual */}
            {/* ---------------------------------------------------------------- */}

            <div className="group relative min-h-[420px] overflow-hidden sm:min-h-[520px] lg:min-h-[620px]">
              <div
                className="absolute inset-0 bg-cover bg-center transition-transform duration-700 ease-out group-hover:scale-[1.035]"
                style={{
                  backgroundImage:
                    "url('/heritage/brihadeeswarar-temple.jpg')",
                }}
              />

              <div className="absolute inset-0 bg-gradient-to-t from-[rgba(11,9,7,0.92)] via-[rgba(11,9,7,0.15)] to-[rgba(11,9,7,0.08)]" />

              <div className="absolute inset-x-5 bottom-5 sm:inset-x-7 sm:bottom-7">
                <div className="flex flex-wrap gap-2">
                  <span className="heritage-badge border-white/[0.12] bg-[rgba(11,9,7,0.55)] backdrop-blur-xl">
                    UNESCO World Heritage
                  </span>

                  <span className="heritage-badge border-white/[0.12] bg-[rgba(11,9,7,0.55)] backdrop-blur-xl">
                    Chola Architecture
                  </span>
                </div>
              </div>
            </div>

            {/* ---------------------------------------------------------------- */}
            {/* Information */}
            {/* ---------------------------------------------------------------- */}

            <div className="flex flex-col justify-between p-6 sm:p-8 lg:p-10">
              <div>
                <div className="flex items-start justify-between gap-5">
                  <div>
                    <p className="text-[10px] font-semibold uppercase tracking-[0.22em] text-[var(--heritage-gold-light)]">
                      Brihadeeswarar Temple
                    </p>

                    <h3 className="mt-3 text-2xl font-semibold tracking-[-0.035em] text-[var(--heritage-ivory)] sm:text-3xl">
                      The Great Living Chola Temple
                    </h3>
                  </div>

                  <div className="hidden h-11 w-11 shrink-0 items-center justify-center rounded-2xl border border-[var(--glass-border)] bg-[rgba(212,175,90,0.07)] sm:flex">
                    <Sparkles
                      className="h-4 w-4 text-[var(--heritage-gold-light)]"
                      aria-hidden="true"
                    />
                  </div>
                </div>

                <div className="mt-7 grid gap-3 sm:grid-cols-2">
                  <div className="rounded-2xl border border-[var(--glass-border)] bg-white/[0.02] p-4">
                    <div className="flex items-center gap-2 text-xs font-medium text-[var(--heritage-muted)]">
                      <MapPin
                        className="h-3.5 w-3.5 text-[var(--heritage-gold)]"
                        aria-hidden="true"
                      />
                      Location
                    </div>

                    <p className="mt-2 text-sm font-medium text-[var(--heritage-ivory)]">
                      Thanjavur, Tamil Nadu
                    </p>
                  </div>

                  <div className="rounded-2xl border border-[var(--glass-border)] bg-white/[0.02] p-4">
                    <div className="flex items-center gap-2 text-xs font-medium text-[var(--heritage-muted)]">
                      <CalendarDays
                        className="h-3.5 w-3.5 text-[var(--heritage-gold)]"
                        aria-hidden="true"
                      />
                      Heritage period
                    </div>

                    <p className="mt-2 text-sm font-medium text-[var(--heritage-ivory)]">
                      Chola period
                    </p>
                  </div>
                </div>

                <div className="mt-7">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[var(--heritage-gold-light)]">
                    Why it matters
                  </p>

                  <p className="mt-3 text-sm leading-7 text-[var(--heritage-muted)]">
                    The temple represents the architectural ambition,
                    craftsmanship and cultural legacy associated with the
                    Chola era. HeritageAI helps transform a visit from simply
                    seeing a monument into understanding the story around it.
                  </p>
                </div>

                <div className="heritage-glass mt-7 rounded-2xl p-5">
                  <div className="flex items-center gap-2">
                    <span className="flex h-8 w-8 items-center justify-center rounded-xl bg-[rgba(212,175,90,0.10)]">
                      <Sparkles
                        className="h-3.5 w-3.5 text-[var(--heritage-gold-light)]"
                        aria-hidden="true"
                      />
                    </span>

                    <p className="text-xs font-semibold uppercase tracking-[0.16em] text-[var(--heritage-gold-light)]">
                      HeritageAI insight
                    </p>
                  </div>

                  <p className="mt-4 text-sm leading-7 text-[var(--heritage-muted)]">
                    Ask HeritageAI about the architecture, historical period,
                    cultural significance or visual details of a heritage
                    place and explore the available evidence behind the
                    answer.
                  </p>
                </div>
              </div>

              <div className="mt-8 border-t border-[var(--glass-border)] pt-6">
                <Link
                  href="/explorer"
                  className="heritage-button heritage-button-gold group w-full min-h-12 px-5 sm:w-fit"
                >
                  Explore Heritage Sites
                  <ArrowRight
                    className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-1"
                    aria-hidden="true"
                  />
                </Link>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
