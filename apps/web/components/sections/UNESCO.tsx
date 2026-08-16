"use client";

import Link from "next/link";
import { motion, useReducedMotion } from "framer-motion";
import {
  ArrowRight,
  Landmark,
  MapPin,
  Sparkles,
  Globe2,
} from "lucide-react";

const EASE = [0.22, 1, 0.36, 1] as const;

const heritageSites = [
  {
    title: "Brihadeeswarar Temple",
    location: "Thanjavur, Tamil Nadu",
    category: "Temple Architecture",
    image: "/heritage/brihadeeswarar-temple.jpg",
    description:
      "A monumental expression of Chola architecture and craftsmanship.",
  },
];

export default function UNESCO() {
  const reduceMotion = useReducedMotion();

  return (
    <section
      id="heritage"
      className="relative overflow-hidden py-24 sm:py-32"
    >
      <div className="pointer-events-none absolute right-0 top-1/4 h-80 w-80 rounded-full bg-[rgba(212,175,90,0.045)] blur-[110px]" />

      <div className="heritage-container relative">
        {/* ---------------------------------------------------------------- */}
        {/* Editorial heading */}
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
              <Globe2
                className="h-3.5 w-3.5 text-[var(--heritage-gold-light)]"
                aria-hidden="true"
              />
              World heritage
            </div>

            <h2 className="mt-5 text-balance text-3xl font-semibold tracking-[-0.045em] text-[var(--heritage-ivory)] sm:text-4xl lg:text-5xl">
              Places worth
              <span className="heritage-gold-gradient"> remembering.</span>
            </h2>

            <p className="mt-5 max-w-xl text-sm leading-7 text-[var(--heritage-muted)] sm:text-base">
              Discover places where architecture, memory, culture and history
              come together—and understand the stories that make them matter.
            </p>
          </div>

          <Link
            href="/explorer"
            className="heritage-button heritage-button-glass group w-fit"
          >
            View explorer
            <ArrowRight
              className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-1"
              aria-hidden="true"
            />
          </Link>
        </motion.div>

        {/* ---------------------------------------------------------------- */}
        {/* Featured editorial composition */}
        {/* ---------------------------------------------------------------- */}

        <div className="mt-12 grid gap-4 lg:grid-cols-[1.35fr_0.65fr]">
          <motion.article
            initial={{
              opacity: 0,
              y: reduceMotion ? 0 : 26,
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
            className="group relative min-h-[520px] overflow-hidden rounded-[30px] border border-[var(--glass-border)] bg-[var(--heritage-charcoal)] sm:min-h-[620px]"
          >
            <div
              className="absolute inset-0 bg-cover bg-center transition-transform duration-1000 ease-out group-hover:scale-[1.035]"
              style={{
                backgroundImage:
                  "url('/heritage/brihadeeswarar-temple.jpg')",
              }}
            />

            <div className="absolute inset-0 bg-gradient-to-t from-[rgba(11,9,7,0.96)] via-[rgba(11,9,7,0.28)] to-[rgba(11,9,7,0.08)]" />

            <div className="absolute inset-x-5 bottom-5 sm:inset-x-8 sm:bottom-8">
              <div className="flex flex-wrap gap-2">
                <span className="heritage-badge border-white/[0.12] bg-[rgba(11,9,7,0.52)] backdrop-blur-xl">
                  UNESCO World Heritage
                </span>

                <span className="heritage-badge border-white/[0.12] bg-[rgba(11,9,7,0.52)] backdrop-blur-xl">
                  Living Heritage
                </span>
              </div>

              <h3 className="mt-5 max-w-2xl text-2xl font-semibold tracking-[-0.035em] text-[var(--heritage-ivory)] sm:text-4xl">
                Brihadeeswarar Temple
              </h3>

              <div className="mt-3 flex items-center gap-2 text-sm text-[rgba(247,241,230,0.72)]">
                <MapPin
                  className="h-3.5 w-3.5 text-[var(--heritage-gold-light)]"
                  aria-hidden="true"
                />
                Thanjavur, Tamil Nadu
              </div>

              <p className="mt-4 max-w-xl text-sm leading-6 text-[rgba(247,241,230,0.66)]">
                Explore one of the defining monuments of Chola architecture
                and discover the history, craftsmanship and cultural context
                behind the monument.
              </p>

              <Link
                href="/explorer"
                className="heritage-button heritage-button-gold group mt-6 w-fit"
              >
                Explore this heritage
                <ArrowRight
                  className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-1"
                  aria-hidden="true"
                />
              </Link>
            </div>
          </motion.article>

          {/* -------------------------------------------------------------- */}
          {/* Context panel */}
          {/* -------------------------------------------------------------- */}

          <motion.aside
            initial={{
              opacity: 0,
              x: reduceMotion ? 0 : 20,
            }}
            whileInView={{
              opacity: 1,
              x: 0,
            }}
            viewport={{
              once: true,
              amount: 0.15,
            }}
            transition={{
              duration: reduceMotion ? 0 : 0.7,
              delay: reduceMotion ? 0 : 0.08,
              ease: EASE,
            }}
            className="heritage-glass-strong flex flex-col justify-between rounded-[30px] p-6 sm:p-8"
          >
            <div>
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-[var(--glass-border)] bg-[rgba(212,175,90,0.07)]">
                <Landmark
                  className="h-5 w-5 text-[var(--heritage-gold-light)]"
                  aria-hidden="true"
                />
              </div>

              <p className="mt-7 text-[10px] font-semibold uppercase tracking-[0.2em] text-[var(--heritage-gold-light)]">
                Why heritage matters
              </p>

              <h3 className="mt-3 text-2xl font-semibold tracking-[-0.035em] text-[var(--heritage-ivory)]">
                History becomes meaningful when we understand its context.
              </h3>

              <p className="mt-5 text-sm leading-7 text-[var(--heritage-muted)]">
                A monument is more than its walls. Architecture, people,
                geography, traditions and historical events create the story
                around it.
              </p>
            </div>

            <div className="mt-10 border-t border-[var(--glass-border)] pt-6">
              <div className="flex items-center gap-3">
                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[rgba(212,175,90,0.08)]">
                  <Sparkles
                    className="h-4 w-4 text-[var(--heritage-gold-light)]"
                    aria-hidden="true"
                  />
                </div>

                <div>
                  <p className="text-xs font-semibold text-[var(--heritage-ivory)]">
                    HeritageAI approach
                  </p>

                  <p className="mt-0.5 text-xs text-[var(--heritage-muted)]">
                    Discover with context, not just images.
                  </p>
                </div>
              </div>
            </div>
          </motion.aside>
        </div>

        {/* ---------------------------------------------------------------- */}
        {/* Site cards */}
        {/* ---------------------------------------------------------------- */}

        <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {heritageSites.map((site, index) => (
            <motion.article
              key={site.title}
              initial={{
                opacity: 0,
                y: reduceMotion ? 0 : 18,
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
              className="heritage-glass overflow-hidden rounded-[24px] p-2"
            >
              <div className="relative aspect-[16/10] overflow-hidden rounded-[18px]">
                <div
                  className="absolute inset-0 bg-cover bg-center transition-transform duration-700 hover:scale-[1.04]"
                  style={{
                    backgroundImage: `url('${site.image}')`,
                  }}
                />

                <div className="absolute inset-0 bg-gradient-to-t from-[rgba(11,9,7,0.82)] to-transparent" />

                <span className="absolute bottom-3 left-3 heritage-badge border-white/[0.1] bg-[rgba(11,9,7,0.48)] backdrop-blur-xl">
                  {site.category}
                </span>
              </div>

              <div className="p-4">
                <h3 className="font-semibold text-[var(--heritage-ivory)]">
                  {site.title}
                </h3>

                <div className="mt-2 flex items-center gap-1.5 text-xs text-[var(--heritage-muted)]">
                  <MapPin
                    className="h-3 w-3 text-[var(--heritage-gold)]"
                    aria-hidden="true"
                  />
                  {site.location}
                </div>

                <p className="mt-3 text-sm leading-6 text-[var(--heritage-muted)]">
                  {site.description}
                </p>
              </div>
            </motion.article>
          ))}
        </div>
      </div>
    </section>
  );
}
