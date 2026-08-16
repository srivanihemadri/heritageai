"use client";

import { motion, useReducedMotion } from "framer-motion";
import { Camera, Compass, Sparkles } from "lucide-react";

const features = [
  {
    icon: Compass,
    title: "Explore",
    description: "Discover remarkable heritage places and stories.",
  },
  {
    icon: Camera,
    title: "Identify",
    description: "Use visual intelligence to understand what you see.",
  },
  {
    icon: Sparkles,
    title: "Ask",
    description: "Get answers grounded in HeritageAI knowledge.",
  },
];

export default function HeroFeatureCards() {
  const reduceMotion = useReducedMotion();

  return (
    <div className="grid gap-3 sm:grid-cols-3">
      {features.map((feature, index) => {
        const Icon = feature.icon;

        return (
          <motion.div
            key={feature.title}
            initial={{
              opacity: 0,
              y: reduceMotion ? 0 : 14,
            }}
            animate={{
              opacity: 1,
              y: 0,
            }}
            transition={{
              duration: reduceMotion ? 0 : 0.5,
              delay: reduceMotion ? 0 : 0.15 + index * 0.08,
            }}
            className="heritage-glass rounded-2xl p-4"
          >
            <div className="flex h-9 w-9 items-center justify-center rounded-xl border border-[var(--glass-border)] bg-[rgba(212,175,90,0.07)]">
              <Icon
                className="h-4 w-4 text-[var(--heritage-gold-light)]"
                aria-hidden="true"
              />
            </div>

            <h3 className="mt-3 text-sm font-semibold text-[var(--heritage-ivory)]">
              {feature.title}
            </h3>

            <p className="mt-1 text-xs leading-5 text-[var(--heritage-muted)]">
              {feature.description}
            </p>
          </motion.div>
        );
      })}
    </div>
  );
}
