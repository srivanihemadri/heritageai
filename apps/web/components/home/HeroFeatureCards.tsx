"use client";

import { motion } from "framer-motion";
import {
  Globe2,
  Sparkles,
  ShieldCheck,
} from "lucide-react";

const cards = [
  {
    title: "Explore Heritage",
    description:
      "Discover UNESCO World Heritage Sites, monuments and historical landmarks.",
    icon: Globe2,
  },
  {
    title: "AI Restoration",
    description:
      "Restore damaged photographs and historical artifacts using advanced AI.",
    icon: Sparkles,
  },
  {
    title: "Damage Detection",
    description:
      "Identify cracks, erosion and vegetation using Computer Vision.",
    icon: ShieldCheck,
  },
];

export default function HeroFeatureCards() {
  return (
    <div className="mt-16 grid w-full max-w-6xl gap-5 md:grid-cols-3">
      {cards.map((card, index) => {
        const Icon = card.icon;

        return (
          <motion.div
            key={card.title}
            initial={{ opacity: 0, y: 25 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{
              delay: index * 0.2,
              duration: 0.6,
            }}
            whileHover={{
              y: -8,
              scale: 1.02,
            }}
            className="heritage-glass group rounded-[var(--radius-card)] p-7 transition-all duration-300 hover:border-[var(--glass-border-strong)] hover:shadow-[0_20px_60px_rgba(212,175,90,0.10)]"
          >
            <div className="mb-6 flex h-12 w-12 items-center justify-center rounded-xl border border-[var(--glass-border)] bg-[var(--glass-highlight)]">
              <Icon
                className="h-6 w-6 text-[var(--heritage-gold)] transition-transform duration-300 group-hover:scale-110"
                strokeWidth={1.7}
              />
            </div>

            <h3 className="mb-3 text-xl font-semibold text-[var(--heritage-ivory)]">
              {card.title}
            </h3>

            <p className="leading-7 text-[var(--heritage-muted)]">
              {card.description}
            </p>
          </motion.div>
        );
      })}
    </div>
  );
}