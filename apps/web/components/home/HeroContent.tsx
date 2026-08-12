"use client";

import { motion } from "framer-motion";

export default function HeroContent() {
  return (
    <>
      <motion.h1
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="mx-auto max-w-6xl text-center text-5xl font-black leading-[0.95] tracking-[-0.04em] text-[var(--heritage-ivory)] md:text-7xl xl:text-8xl"
      >
        Preserve The Worlds
        <span className="mt-3 block heritage-gold-gradient">
          Cultural Heritage
        </span>
      </motion.h1>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="mx-auto mt-8 max-w-3xl text-center text-base leading-8 text-[var(--heritage-muted)] md:text-lg"
      >
        Discover historical monuments, restore ancient artifacts, detect
        structural damage, translate inscriptions, and explore world heritage
        through cutting-edge Artificial Intelligence.
      </motion.p>
    </>
  );
}
