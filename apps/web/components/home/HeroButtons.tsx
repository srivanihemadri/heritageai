"use client";

import Link from "next/link";
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
      <Link
        href="/explorer"
        className="heritage-gold-glow inline-flex items-center gap-2 rounded-[var(--radius-button)] border border-[var(--heritage-gold)]/50 bg-[var(--heritage-gold)] px-7 py-3 font-semibold text-[var(--heritage-black)] transition-all duration-300 hover:-translate-y-0.5 hover:bg-[var(--heritage-gold-light)]"
      >
        Explore Heritage
        <ArrowRight className="h-4 w-4" />
      </Link>

      <button
        type="button"
        className="heritage-glass inline-flex items-center gap-2 rounded-[var(--radius-button)] px-7 py-3 font-medium text-[var(--heritage-ivory)] transition-all duration-300 hover:-translate-y-0.5 hover:border-[var(--glass-border-strong)] hover:bg-white/10"
      >
        <PlayCircle className="h-4 w-4 text-[var(--heritage-gold)]" />
        Watch Demo
      </button>
    </motion.div>
  );
}