"use client";

import Image from "next/image";
import { motion } from "framer-motion";
import { CalendarDays, ShieldCheck, Landmark } from "lucide-react";

export default function LivingHeritage() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 1 }}
      className="relative mt-16 w-full max-w-6xl overflow-hidden rounded-[28px] border border-[var(--glass-border)] bg-black/30 shadow-[0_30px_100px_rgba(0,0,0,0.5)]"
    >
      <div className="relative min-h-[420px] overflow-hidden md:min-h-[520px]">

        <Image
          src="/heritage/brihadeeswarar-temple.jpg"
          alt="Brihadeeswarar Temple representing Indian cultural heritage"
          fill
          priority
          sizes="(max-width: 768px) 100vw, 1200px"
          className="object-cover object-center opacity-80 transition-transform duration-[12000ms] ease-out hover:scale-105"
        />

        {/* Cinematic dark overlay */}
        <div
          aria-hidden="true"
          className="absolute inset-0 bg-[linear-gradient(90deg,rgba(11,9,7,0.96)_0%,rgba(11,9,7,0.78)_34%,rgba(11,9,7,0.22)_72%,rgba(11,9,7,0.55)_100%)]"
        />

        {/* Gold atmosphere */}
        <div
          aria-hidden="true"
          className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_70%_48%,rgba(212,175,90,0.22),transparent_34%)]"
        />

        {/* Heritage scan markers */}
        <motion.span
          animate={{ scale: [1, 1.25, 1], opacity: [0.7, 1, 0.7] }}
          transition={{ duration: 2.5, repeat: Infinity }}
          className="absolute left-[63%] top-[35%] h-4 w-4 rounded-full border-2 border-[var(--heritage-gold-light)] bg-[var(--heritage-gold)]/30 shadow-[0_0_24px_rgba(240,207,122,0.8)]"
        />

        <motion.span
          animate={{ scale: [1, 1.25, 1], opacity: [0.7, 1, 0.7] }}
          transition={{ duration: 2.5, repeat: Infinity, delay: 0.8 }}
          className="absolute left-[73%] top-[55%] h-4 w-4 rounded-full border-2 border-[var(--heritage-gold-light)] bg-[var(--heritage-gold)]/30 shadow-[0_0_24px_rgba(240,207,122,0.8)]"
        />

        {/* Content */}
        <div className="relative z-10 flex min-h-[420px] items-end p-6 md:min-h-[520px] md:p-10">
          <div className="max-w-xl">
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--heritage-gold-light)]">
              Featured Heritage Site
            </p>

            <h2 className="mt-3 text-3xl font-semibold tracking-tight text-[var(--heritage-ivory)] md:text-5xl">
              Brihadeeswarar Temple
            </h2>

            <p className="mt-3 max-w-lg text-sm leading-7 text-[var(--heritage-muted)] md:text-base">
              A living monument of Chola architecture, brought into the HeritageAI preservation experience.
            </p>
          </div>
        </div>

        {/* Heritage Scan panel */}
        <motion.div
          initial={{ opacity: 0, x: 30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5, duration: 0.7 }}
          className="heritage-glass-strong absolute right-5 top-5 z-20 hidden w-64 rounded-2xl p-5 md:block lg:right-8 lg:top-8"
        >
          <div className="flex items-center justify-between">
            <p className="text-sm font-semibold tracking-wide text-[var(--heritage-gold-light)]">
              Heritage Scan
            </p>
            <span className="h-2 w-2 rounded-full bg-[var(--heritage-gold)] shadow-[0_0_12px_rgba(212,175,90,0.8)]" />
          </div>

          <div className="mt-5 space-y-4">
            <div className="flex items-center gap-3">
              <Landmark className="h-5 w-5 text-[var(--heritage-gold)]" />
              <div>
                <p className="text-xs text-[var(--heritage-muted)]">Site Type</p>
                <p className="text-sm text-[var(--heritage-ivory)]">Temple</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <CalendarDays className="h-5 w-5 text-[var(--heritage-gold)]" />
              <div>
                <p className="text-xs text-[var(--heritage-muted)]">Architectural Era</p>
                <p className="text-sm text-[var(--heritage-ivory)]">Chola Period</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <ShieldCheck className="h-5 w-5 text-[var(--heritage-gold)]" />
              <div>
                <p className="text-xs text-[var(--heritage-muted)]">Preservation</p>
                <p className="text-sm text-[var(--heritage-gold-light)]">Protected</p>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
}
