"use client";

import { motion, useReducedMotion } from "framer-motion";
import {
  ArrowUpRight,
  BookOpen,
  Globe2,
  Landmark,
  Sparkles,
} from "lucide-react";

const EASE = [0.22, 1, 0.36, 1] as const;

const stats = [
  {
    value: "100+",
    label: "Heritage stories",
    description: "Places and cultural narratives ready to be explored.",
    icon: Landmark,
  },
  {
    value: "AI",
    label: "Heritage intelligence",
    description: "Visual and conversational AI experiences in one platform.",
    icon: Sparkles,
  },
  {
    value: "24/7",
    label: "Knowledge access",
    description: "Explore heritage knowledge whenever curiosity begins.",
    icon: BookOpen,
  },
  {
    value: "∞",
    label: "Stories to discover",
    description: "Every heritage place can open a deeper journey.",
    icon: Globe2,
  },
];

export default function Stats() {
  const reduceMotion = useReducedMotion();

  return (
    <section className="relative overflow-hidden py-24 sm:py-32">
      <div className="pointer-events-none absolute left-0 top-1/3 h-72 w-72 rounded-full bg-[rgba(212,175,90,0.04)] blur-[110px]" />

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
          className="grid gap-6 lg:grid-cols-[1fr_auto] lg:items-end"
        >
          <div className="max-w-2xl">
            <div className="heritage-badge w-fit">
              <Sparkles
                className="h-3.5 w-3.5 text-[var(--heritage-gold-light)]"
                aria-hidden="true"
              />
              HeritageAI impact
            </div>

            <h2 className="mt-5 text-balance text-3xl font-semibold tracking-[-0.045em] text-[var(--heritage-ivory)] sm:text-4xl lg:text-5xl">
              Technology should make
              <span className="heritage-gold-gradient"> heritage closer.</span>
            </h2>

            <p className="mt-5 max-w-xl text-sm leading-7 text-[var(--heritage-muted)] sm:text-base">
              HeritageAI brings cultural discovery and intelligent
              interpretation together so more people can connect with the
              stories behind extraordinary places.
            </p>
          </div>

          <div className="hidden items-center gap-2 text-xs text-[var(--heritage-muted)] lg:flex">
            <span className="h-1.5 w-1.5 rounded-full bg-[var(--heritage-gold)]" />
            Built for discovery
          </div>
        </motion.div>

        {/* ---------------------------------------------------------------- */}
        {/* Main impact composition */}
        {/* ---------------------------------------------------------------- */}

        <div className="mt-12 grid gap-4 lg:grid-cols-[0.72fr_1.28fr]">
          {/* Editorial statement */}

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
              amount: 0.15,
            }}
            transition={{
              duration: reduceMotion ? 0 : 0.7,
              ease: EASE,
            }}
            className="heritage-glass-strong flex min-h-[390px] flex-col justify-between rounded-[30px] p-6 sm:p-8 lg:p-9"
          >
            <div>
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-[var(--glass-border)] bg-[rgba(212,175,90,0.07)]">
                <Globe2
                  className="h-5 w-5 text-[var(--heritage-gold-light)]"
                  aria-hidden="true"
                />
              </div>

              <p className="mt-7 text-[10px] font-semibold uppercase tracking-[0.2em] text-[var(--heritage-gold-light)]">
                A larger mission
              </p>

              <p className="mt-4 text-2xl font-semibold leading-tight tracking-[-0.035em] text-[var(--heritage-ivory)] sm:text-3xl">
                Preserve the past by making it easier to understand.
              </p>

              <p className="mt-5 text-sm leading-7 text-[var(--heritage-muted)]">
                The value of heritage grows when knowledge can be discovered,
                understood and shared across generations.
              </p>
            </div>

            <div className="mt-8 flex items-center gap-3 border-t border-[var(--glass-border)] pt-5">
              <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-[rgba(212,175,90,0.08)]">
                <ArrowUpRight
                  className="h-4 w-4 text-[var(--heritage-gold-light)]"
                  aria-hidden="true"
                />
              </span>

              <p className="text-xs leading-5 text-[var(--heritage-muted)]">
                Discover
                <span className="mx-1.5 text-[var(--heritage-gold)]">·</span>
                Understand
                <span className="mx-1.5 text-[var(--heritage-gold)]">·</span>
                Preserve
              </p>
            </div>
          </motion.div>

          {/* Metrics */}

          <div className="grid gap-4 sm:grid-cols-2">
            {stats.map((stat, index) => {
              const Icon = stat.icon;

              return (
                <motion.article
                  key={stat.label}
                  initial={{
                    opacity: 0,
                    y: reduceMotion ? 0 : 22,
                  }}
                  whileInView={{
                    opacity: 1,
                    y: 0,
                  }}
                  viewport={{
                    once: true,
                    amount: 0.12,
                  }}
                  transition={{
                    duration: reduceMotion ? 0 : 0.55,
                    delay: reduceMotion ? 0 : index * 0.06,
                    ease: EASE,
                  }}
                  whileHover={
                    reduceMotion
                      ? undefined
                      : {
                          y: -4,
                        }
                  }
                  className="heritage-glass group rounded-[26px] p-6 transition-colors duration-300 hover:border-[var(--glass-border-strong)] sm:p-7"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-[var(--glass-border)] bg-[rgba(212,175,90,0.06)]">
                      <Icon
                        className="h-4 w-4 text-[var(--heritage-gold-light)]"
                        aria-hidden="true"
                      />
                    </div>

                    <span className="text-[10px] font-medium uppercase tracking-[0.16em] text-[var(--heritage-bronze)]">
                      0{index + 1}
                    </span>
                  </div>

                  <p className="mt-8 text-4xl font-semibold tracking-[-0.05em] text-[var(--heritage-ivory)] sm:text-5xl">
                    {stat.value}
                  </p>

                  <h3 className="mt-3 text-sm font-semibold text-[var(--heritage-ivory)]">
                    {stat.label}
                  </h3>

                  <p className="mt-2 text-sm leading-6 text-[var(--heritage-muted)]">
                    {stat.description}
                  </p>
                </motion.article>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
}
