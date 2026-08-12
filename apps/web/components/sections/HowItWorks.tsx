"use client";

import { motion } from "framer-motion";
import { Compass, ScanSearch, ShieldCheck, Sparkles } from "lucide-react";

const steps = [
  {
    number: "01",
    title: "Discover",
    description:
      "Explore monuments, historical landmarks and cultural heritage from around the world.",
    icon: Compass,
  },
  {
    number: "02",
    title: "Analyze",
    description:
      "Use AI to study heritage imagery, inscriptions and visible structural conditions.",
    icon: ScanSearch,
  },
  {
    number: "03",
    title: "Preserve",
    description:
      "Transform analysis into restoration, documentation and preservation insights.",
    icon: ShieldCheck,
  },
  {
    number: "04",
    title: "Understand",
    description:
      "Experience heritage through intelligent explanations designed for people and researchers.",
    icon: Sparkles,
  },
];

export default function HowItWorks() {
  return (
    <section
      id="how-it-works"
      className="relative mx-auto w-full max-w-7xl px-6 py-24 md:px-8 md:py-32"
    >
      <div className="mx-auto max-w-3xl text-center">
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--heritage-gold-light)]">
          The HeritageAI Experience
        </p>

        <h2 className="mt-4 text-3xl font-semibold tracking-tight text-[var(--heritage-ivory)] md:text-5xl">
          From discovery to preservation.
        </h2>

        <p className="mt-5 text-sm leading-7 text-[var(--heritage-muted)] md:text-base">
          HeritageAI connects exploration, artificial intelligence and
          preservation into one continuous heritage experience.
        </p>
      </div>

      <div className="relative mt-16 grid gap-5 md:grid-cols-2 lg:grid-cols-4">
        <div
          aria-hidden="true"
          className="pointer-events-none absolute left-[12%] right-[12%] top-16 hidden h-px bg-gradient-to-r from-transparent via-[var(--glass-border-strong)] to-transparent lg:block"
        />

        {steps.map((step, index) => {
          const Icon = step.icon;

          return (
            <motion.article
              key={step.number}
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.25 }}
              transition={{ duration: 0.55, delay: index * 0.08 }}
              whileHover={{ y: -6 }}
              className="heritage-glass relative rounded-[var(--radius-card)] p-6 transition-all duration-300 hover:border-[var(--glass-border-strong)]"
            >
              <div className="relative z-10 flex items-center justify-between">
                <span className="text-xs font-semibold tracking-[0.2em] text-[var(--heritage-gold)]">
                  {step.number}
                </span>

                <div className="flex h-11 w-11 items-center justify-center rounded-full border border-[var(--glass-border)] bg-[var(--heritage-charcoal)]">
                  <Icon className="h-5 w-5 text-[var(--heritage-gold-light)]" />
                </div>
              </div>

              <h3 className="mt-8 text-xl font-semibold text-[var(--heritage-ivory)]">
                {step.title}
              </h3>

              <p className="mt-3 text-sm leading-7 text-[var(--heritage-muted)]">
                {step.description}
              </p>
            </motion.article>
          );
        })}
      </div>
    </section>
  );
}