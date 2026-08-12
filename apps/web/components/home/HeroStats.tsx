"use client";

import { motion } from "framer-motion";

const stats = [
  {
    value: "1,100+",
    label: "UNESCO Sites",
  },
  {
    value: "50K+",
    label: "AI Analyses",
  },
  {
    value: "25K+",
    label: "Images Restored",
  },
  {
    value: "100+",
    label: "Countries",
  },
];

export default function HeroStats() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 25 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.8 }}
      className="mt-16 grid w-full max-w-5xl grid-cols-2 gap-4 md:grid-cols-4 md:gap-5"
    >
      {stats.map((item, index) => (
        <motion.div
          key={item.label}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{
            delay: 0.9 + index * 0.1,
            duration: 0.5,
          }}
          whileHover={{
            y: -5,
            scale: 1.01,
          }}
          className="heritage-glass group rounded-[var(--radius-card)] border border-[var(--glass-border)] p-5 text-center transition-all duration-300 hover:border-[var(--glass-border-strong)] hover:bg-white/[0.06] md:p-6"
        >
          <p className="heritage-gold-gradient text-2xl font-bold tracking-tight md:text-3xl">
            {item.value}
          </p>

          <p className="mt-2 text-xs font-medium tracking-wide text-[var(--heritage-muted)] md:text-sm">
            {item.label}
          </p>

          <div className="mx-auto mt-4 h-px w-10 bg-[var(--heritage-gold)]/30 transition-all duration-300 group-hover:w-16 group-hover:bg-[var(--heritage-gold)]/60" />
        </motion.div>
      ))}
    </motion.div>
  );
}