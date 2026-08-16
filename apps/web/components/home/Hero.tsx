"use client";

import { motion, useReducedMotion } from "framer-motion";
import Link from "next/link";
import { ArrowRight, Sparkles } from "lucide-react";
import HeroBackground from "./HeroBackground";
import HeroBadge from "./HeroBadge";
import HeroStats from "./HeroStats";

const HERO_EASE = [0.22, 1, 0.36, 1] as const;

export default function Hero() {
  const reduceMotion = useReducedMotion();

  const fadeUp = {
    hidden: {
      opacity: 0,
      y: reduceMotion ? 0 : 24,
    },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: reduceMotion ? 0 : 0.7,
        ease: HERO_EASE,
      },
    },
  };

  return (
    <section className="relative isolate min-h-[calc(100svh-5rem)] overflow-hidden">
      <HeroBackground />

      <div className="heritage-container relative flex min-h-[calc(100svh-5rem)] items-center py-20 sm:py-24 lg:py-28">
        <div className="grid w-full items-center gap-14 lg:grid-cols-[1.08fr_0.92fr] lg:gap-16">
          <motion.div
            initial="hidden"
            animate="visible"
            variants={fadeUp}
            className="max-w-3xl"
          >
            <HeroBadge />

            <h1 className="mt-7 max-w-4xl text-balance text-[clamp(3.25rem,8vw,7rem)] font-semibold leading-[0.91] tracking-[-0.065em] text-[var(--heritage-ivory)]">
              Discover the
              <span className="block heritage-gold-gradient">
                stories behind history.
              </span>
            </h1>

            <p className="mt-7 max-w-2xl text-base leading-7 text-[var(--heritage-muted)] sm:text-lg sm:leading-8">
              Explore the world&apos;s cultural heritage with AI-powered
              discovery, visual understanding and historically grounded
              knowledge.
            </p>

            <div className="mt-9 flex flex-col gap-3 sm:flex-row">
              <Link
                href="/explorer"
                className="heritage-button heritage-button-gold heritage-gold-glow group min-h-12 px-6"
              >
                Explore Heritage
                <ArrowRight
                  className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-1"
                  aria-hidden="true"
                />
              </Link>

              <Link
                href="/chat"
                className="heritage-button heritage-button-glass group min-h-12 px-6"
              >
                <Sparkles
                  className="h-4 w-4 text-[var(--heritage-gold)]"
                  aria-hidden="true"
                />
                Ask HeritageAI
              </Link>
            </div>

            <div className="mt-10">
              <HeroStats />
            </div>
          </motion.div>

          <motion.div
            initial={{
              opacity: 0,
              y: reduceMotion ? 0 : 30,
              scale: reduceMotion ? 1 : 0.98,
            }}
            animate={{
              opacity: 1,
              y: 0,
              scale: 1,
            }}
            transition={{
              duration: reduceMotion ? 0 : 0.9,
              delay: reduceMotion ? 0 : 0.15,
              ease: HERO_EASE,
            }}
            className="relative mx-auto w-full max-w-xl lg:ml-auto"
          >
            <div className="relative aspect-[0.86] overflow-hidden rounded-[32px] border border-[var(--glass-border-strong)] bg-[rgba(30,25,19,0.48)] p-2 shadow-[0_30px_100px_rgba(0,0,0,0.45)] backdrop-blur-2xl">
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_15%,rgba(240,207,122,0.18),transparent_42%)]" />

              <div className="relative h-full overflow-hidden rounded-[26px] border border-white/[0.08] bg-[var(--heritage-charcoal)]">
                <div
                  className="absolute inset-0 bg-cover bg-center"
                  style={{
                    backgroundImage:
                      "url('/heritage/brihadeeswarar-temple.jpg')",
                  }}
                />

                <div className="absolute inset-0 bg-gradient-to-t from-[rgba(11,9,7,0.96)] via-[rgba(11,9,7,0.20)] to-transparent" />

                <div className="absolute inset-x-5 bottom-5 sm:inset-x-7 sm:bottom-7">
                  <div className="heritage-glass-strong rounded-2xl p-5 sm:p-6">
                    <div className="flex items-center justify-between gap-4">
                      <div>
                        <p className="text-[10px] font-semibold uppercase tracking-[0.2em] text-[var(--heritage-gold-light)]">
                          Featured Heritage
                        </p>

                        <h2 className="mt-2 text-xl font-semibold tracking-tight text-[var(--heritage-ivory)] sm:text-2xl">
                          Brihadeeswarar Temple
                        </h2>

                        <p className="mt-1 text-sm text-[var(--heritage-muted)]">
                          Thanjavur, Tamil Nadu
                        </p>
                      </div>

                      <div className="hidden h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-[var(--glass-border)] bg-[rgba(212,175,90,0.08)] sm:flex">
                        <Sparkles
                          className="h-4 w-4 text-[var(--heritage-gold-light)]"
                          aria-hidden="true"
                        />
                      </div>
                    </div>

                    <div className="mt-5 flex flex-wrap gap-2">
                      <span className="heritage-badge">
                        Chola Architecture
                      </span>
                      <span className="heritage-badge">
                        UNESCO World Heritage
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {!reduceMotion && (
              <>
                <div className="pointer-events-none absolute -right-5 top-12 h-24 w-24 rounded-full bg-[rgba(212,175,90,0.10)] blur-3xl" />
                <div className="pointer-events-none absolute -bottom-8 -left-8 h-32 w-32 rounded-full bg-[rgba(155,117,48,0.08)] blur-3xl" />
              </>
            )}
          </motion.div>
        </div>
      </div>
    </section>
  );
}
