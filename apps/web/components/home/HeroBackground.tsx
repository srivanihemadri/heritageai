"use client";

import { motion } from "framer-motion";

export default function HeroBackground() {
  return (
    <div className="absolute inset-0 overflow-hidden">

      {/* Main Glow */}
      <motion.div
        animate={{
          scale: [1, 1.2, 1],
          opacity: [0.25, 0.45, 0.25],
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
        }}
        className="absolute left-1/2 top-20 h-[600px] w-[600px] -translate-x-1/2 rounded-full bg-cyan-500 blur-[180px]"
      />

      {/* Left Glow */}
      <motion.div
        animate={{
          y: [-20, 20, -20],
        }}
        transition={{
          duration: 6,
          repeat: Infinity,
        }}
        className="absolute left-0 top-60 h-[300px] w-[300px] rounded-full bg-sky-500/20 blur-[120px]"
      />

      {/* Right Glow */}
      <motion.div
        animate={{
          y: [20, -20, 20],
        }}
        transition={{
          duration: 7,
          repeat: Infinity,
        }}
        className="absolute right-0 top-40 h-[250px] w-[250px] rounded-full bg-blue-500/20 blur-[120px]"
      />

    </div>
  );
}