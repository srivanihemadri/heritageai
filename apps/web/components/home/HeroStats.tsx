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
      className="mt-16 grid w-full max-w-5xl grid-cols-2 gap-5 md:grid-cols-4"
    >
      {stats.map((item) => (
        <div
          key={item.label}
          className="rounded-2xl border border-white/10 bg-white/5 p-6 text-center backdrop-blur-xl transition-all duration-300 hover:border-cyan-400 hover:bg-white/10"
        >
          <h3 className="text-3xl font-bold text-cyan-400">
            {item.value}
          </h3>

          <p className="mt-2 text-sm text-gray-400">
            {item.label}
          </p>
        </div>
      ))}
    </motion.div>
  );
}