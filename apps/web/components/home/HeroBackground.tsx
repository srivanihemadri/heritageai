"use client";

import { motion } from "framer-motion";

export default function HeroBackground() {
  return (
    <>
      {/* Central warm heritage atmosphere */}
      <motion.div
        aria-hidden="true"
        animate={{
          scale: [1, 1.08, 1],
          opacity: [0.12, 0.2, 0.12],
        }}
        transition={{
          duration: 14,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="pointer-events-none absolute left-1/2 top-20 h-[560px] w-[560px] -translate-x-1/2 rounded-full bg-[var(--heritage-gold)] blur-[200px]"
      />

      {/* Left bronze atmosphere */}
      <motion.div
        aria-hidden="true"
        animate={{
          x: [-20, 20, -20],
          opacity: [0.035, 0.075, 0.035],
        }}
        transition={{
          duration: 12,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="pointer-events-none absolute -left-32 top-72 h-[340px] w-[340px] rounded-full bg-[var(--heritage-gold-dark)] blur-[150px]"
      />

      {/* Right bronze atmosphere */}
      <motion.div
        aria-hidden="true"
        animate={{
          x: [20, -20, 20],
          opacity: [0.03, 0.065, 0.03],
        }}
        transition={{
          duration: 15,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="pointer-events-none absolute -right-28 top-56 h-[320px] w-[320px] rounded-full bg-[var(--heritage-bronze)] blur-[150px]"
      />

      {/* Subtle vertical light */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute left-1/2 top-0 h-[700px] w-px -translate-x-1/2 bg-gradient-to-b from-[var(--heritage-gold)]/10 via-[var(--heritage-gold)]/[0.03] to-transparent"
      />

      {/* Cinematic vignette */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_0%,rgba(11,9,7,0.16)_48%,rgba(11,9,7,0.78)_100%)]"
      />

      {/* Bottom fade into the next section */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-x-0 bottom-0 h-40 bg-gradient-to-t from-[var(--heritage-black)] to-transparent"
      />
    </>
  );
}