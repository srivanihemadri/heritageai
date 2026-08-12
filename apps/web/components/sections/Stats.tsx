"use client";

import { motion } from "framer-motion";
import {
  Globe2,
  Layers3,
  ScanSearch,
  Languages,
} from "lucide-react";

const impactItems = [
  {
    value: "Global",
    label: "Heritage Discovery",
    description:
      "Explore cultural landmarks and historical places through a unified digital experience.",
    icon: Globe2,
  },
  {
    value: "Multi-layer",
    label: "Heritage Intelligence",
    description:
      "Connect visual analysis, historical context and preservation information in one workflow.",
    icon: Layers3,
  },
  {
    value: "AI-assisted",
    label: "Visual Analysis",
    description:
      "Analyze heritage imagery for restoration and visible preservation concerns.",
    icon: ScanSearch,
  },
  {
    value: "Accessible",
    label: "Historical Knowledge",
    description:
      "Make inscriptions, architecture and cultural context easier to understand.",
    icon: Languages,
  },
];

export default function Stats() {
  return (
    <section
      id="impact"
      className="relative mx-auto w-full max-w-7xl px-6 py-24 md:px-8 md:py-32"
    >
      <div className="heritage-glass overflow-hidden rounded-[28px] p-6 md:p-10">
        <div className="grid gap-10 lg:grid-cols-[0.8fr_1.2fr] lg:items-center">
          <motion.div
            initial={{ opacity: 0, x: -24 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, amount: 0.25 }}
            transition={{ duration: 0.7 }}
          >
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--heritage-gold-light)]">
              Heritage Impact
            </p>

            <h2 className="mt-4 text-3xl font-semibold tracking-tight text-[var(--heritage-ivory)] md:text-5xl">
              Technology with preservation at its core.
            </h2>

            <p className="mt-5 max-w-xl text-sm leading-7 text-[var(--heritage-muted)] md:text-base">
              HeritageAI is designed to bring exploration, artificial
              intelligence and cultural preservation together without losing
              the human story behind every place.
            </p>
          </motion.div>

          <div className="grid gap-3 sm:grid-cols-2">
            {impactItems.map((item, index) => {
              const Icon = item.icon;

              return (
                <motion.article
                  key={item.label}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, amount: 0.2 }}
                  transition={{
                    duration: 0.5,
                    delay: index * 0.08,
                  }}
                  className="rounded-2xl border border-[var(--glass-border)] bg-[var(--heritage-charcoal)]/55 p-5"
                >
                  <div className="flex items-center justify-between gap-4">
                    <Icon className="h-5 w-5 text-[var(--heritage-gold)]" />

                    <span className="text-sm font-semibold text-[var(--heritage-gold-light)]">
                      {item.value}
                    </span>
                  </div>

                  <h3 className="mt-5 text-base font-semibold text-[var(--heritage-ivory)]">
                    {item.label}
                  </h3>

                  <p className="mt-2 text-sm leading-6 text-[var(--heritage-muted)]">
                    {item.description}
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