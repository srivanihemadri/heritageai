"use client";

import { motion } from "framer-motion";
import {
  Landmark,
  MapPinned,
  Building2,
  ScrollText,
} from "lucide-react";

const heritageTypes = [
  {
    title: "Historic Monuments",
    description:
      "Explore architectural landmarks, temples, forts and monuments shaped by centuries of history.",
    icon: Landmark,
  },
  {
    title: "Cultural Landscapes",
    description:
      "Discover places where geography, communities and cultural traditions have evolved together.",
    icon: MapPinned,
  },
  {
    title: "Architectural Heritage",
    description:
      "Understand architectural styles, construction traditions and the stories preserved within them.",
    icon: Building2,
  },
  {
    title: "Historical Knowledge",
    description:
      "Connect monuments with inscriptions, historical context and cultural narratives.",
    icon: ScrollText,
  },
];

export default function UNESCO() {
  return (
    <section
      id="heritage"
      className="relative mx-auto w-full max-w-7xl px-6 py-24 md:px-8 md:py-32"
    >
      <div className="grid gap-12 lg:grid-cols-[0.85fr_1.15fr] lg:items-center">
        <motion.div
          initial={{ opacity: 0, x: -24 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true, amount: 0.25 }}
          transition={{ duration: 0.7 }}
        >
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--heritage-gold-light)]">
            World Heritage
          </p>

          <h2 className="mt-4 text-3xl font-semibold tracking-tight text-[var(--heritage-ivory)] md:text-5xl">
            A deeper way to experience heritage.
          </h2>

          <p className="mt-5 max-w-xl text-sm leading-7 text-[var(--heritage-muted)] md:text-base">
            HeritageAI brings monuments, architecture, cultural landscapes and
            historical knowledge into one intelligent exploration experience.
          </p>

          <div className="mt-8 heritage-glass rounded-[var(--radius-card)] p-5">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-full border border-[var(--glass-border)] bg-[var(--heritage-charcoal)]">
                <Landmark className="h-5 w-5 text-[var(--heritage-gold)]" />
              </div>

              <div>
                <p className="text-sm font-semibold text-[var(--heritage-ivory)]">
                  Heritage-first intelligence
                </p>
                <p className="mt-1 text-xs text-[var(--heritage-muted)]">
                  Built around preservation, context and discovery.
                </p>
              </div>
            </div>
          </div>
        </motion.div>

        <div className="grid gap-4 sm:grid-cols-2">
          {heritageTypes.map((item, index) => {
            const Icon = item.icon;

            return (
              <motion.article
                key={item.title}
                initial={{ opacity: 0, y: 24 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.2 }}
                transition={{ duration: 0.55, delay: index * 0.08 }}
                whileHover={{ y: -5 }}
                className="heritage-glass rounded-[var(--radius-card)] p-6 transition-all duration-300 hover:border-[var(--glass-border-strong)]"
              >
                <div className="flex h-11 w-11 items-center justify-center rounded-xl border border-[var(--glass-border)] bg-[var(--heritage-charcoal)]">
                  <Icon className="h-5 w-5 text-[var(--heritage-gold-light)]" />
                </div>

                <h3 className="mt-6 text-lg font-semibold text-[var(--heritage-ivory)]">
                  {item.title}
                </h3>

                <p className="mt-3 text-sm leading-7 text-[var(--heritage-muted)]">
                  {item.description}
                </p>
              </motion.article>
            );
          })}
        </div>
      </div>
    </section>
  );
}