"use client";

import { motion } from "framer-motion";
import { ArrowRight, PlayCircle } from "lucide-react";

export default function HeroButtons() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 25 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.5, duration: 0.6 }}
      className="mt-10 flex flex-wrap items-center justify-center gap-4"
    >
      <button className="group flex items-center gap-2 rounded-xl bg-cyan-500 px-7 py-3 font-semibold text-black transition-all duration-300 hover:scale-105 hover:bg-cyan-400">
        Explore Heritage
        <ArrowRight
          size={18}
          className="transition-transform group-hover:translate-x-1"
        />
      </button>

      <button className="group flex items-center gap-2 rounded-xl border border-white/15 bg-white/5 px-7 py-3 font-medium text-white backdrop-blur-lg transition-all duration-300 hover:border-cyan-400 hover:bg-white/10">
        <PlayCircle size={18} />
        Watch Demo
      </button>
    </motion.div>
  );
}