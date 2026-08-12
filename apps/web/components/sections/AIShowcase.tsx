"use client";

import { motion } from "framer-motion";
import {
  Camera,
  Languages,
  ScanLine,
  Sparkles,
} from "lucide-react";

const capabilities = [
  {
    title: "AI Restoration",
    description:
      "Enhance damaged historical photographs and artifacts while preserving their visual character.",
    icon: Sparkles,
  },
  {
    title: "Damage Detection",
    description:
      "Analyze heritage imagery for visible cracks, erosion, vegetation and other preservation concerns.",
    icon: ScanLine,
  },
  {
    title: "Artifact Understanding",
    description:
      "Use visual intelligence to identify and interpret important characteristics of historical objects.",
    icon: Camera,
  },
  {
    title: "Inscription Translation",
    description:
      "Make historical inscriptions more accessible by connecting visual text with understandable context.",
    icon: Languages,
  },
];

export default function AIShowcase() {
  return (
    <section
      id="ai"
      className="relative mx-auto w-full max-w-7xl px-6 py-24 md:px-8 md:py-32"
    >
      <div className="mx-auto max-w-3xl text-center">
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--heritage-gold-light)]">
          Intelligence For Preservation
        </p>

        <h2 className="mt-4 text-3xl font-semibold tracking-tight text-[var(--heritage-ivory)] md:text-5xl">
          AI that helps heritage live longer.
        </h2>

        <p className="mt-5 text-sm leading-7 text-[var(--heritage-muted)] md:text-base">
          HeritageAI combines visual intelligence, restoration and historical
          understanding to make cultural preservation more accessible.
        </p>
      </div>

      <div className="mt-16 grid gap-5 md:grid-cols-2">
        {capabilities.map((capability, index) => {
          const Icon = capability.icon;

          return (
            <motion.article
              key={capability.title}
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.2 }}
              transition={{ duration: 0.55, delay: index * 0.08 }}
              whileHover={{ y: -6 }}
              className="heritage-glass group rounded-[var(--radius-card)] p-6 md:p-7"
            >
              <div className="flex items-start justify-between gap-5">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl border border-[var(--glass-border)] bg-[var(--heritage-charcoal)]">
                  <Icon className="h-5 w-5 text-[var(--heritage-gold-light)]" />
                </div>

                <span className="text-xs font-semibold tracking-[0.2em] text-[var(--heritage-bronze)]">
                  AI
                </span>
              </div>

              <h3 className="mt-7 text-xl font-semibold text-[var(--heritage-ivory)]">
                {capability.title}
              </h3>

              <p className="mt-3 max-w-xl text-sm leading-7 text-[var(--heritage-muted)]">
                {capability.description}
              </p>

              <div className="mt-6 h-px w-full bg-gradient-to-r from-[var(--glass-border-strong)] via-[var(--glass-border)] to-transparent" />
            </motion.article>
          );
        })}
      </div>
    </section>
  );
}