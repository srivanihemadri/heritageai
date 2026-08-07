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
    <div className="mt-16 grid gap-6 md:grid-cols-3">
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
            className="rounded-3xl border border-white/10 bg-white/5 p-8 backdrop-blur-xl transition-all duration-300 hover:border-cyan-400/40"
          >
            <Icon className="mb-5 h-10 w-10 text-cyan-400" />

            <h3 className="mb-3 text-xl font-semibold">
              {card.title}
            </h3>

            <p className="leading-7 text-gray-400">
              {card.description}
            </p>
          </motion.div>
        );
      })}
    </div>
  );
}