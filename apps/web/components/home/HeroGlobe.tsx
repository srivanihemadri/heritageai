"use client";

import { motion } from "framer-motion";

const markers = [
  { top: "20%", left: "30%" },
  { top: "35%", left: "70%" },
  { top: "65%", left: "55%" },
  { top: "75%", left: "25%" },
];

export default function HeroGlobe() {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 1 }}
      className="relative mx-auto mt-16 flex h-[360px] w-[360px] items-center justify-center"
    >
      {/* Outer Glow */}
      <div className="absolute h-[360px] w-[360px] rounded-full bg-cyan-500/10 blur-3xl" />

      {/* Globe */}
      <motion.div
        animate={{ rotate: 360 }}
        transition={{
          duration: 30,
          repeat: Infinity,
          ease: "linear",
        }}
        className="relative h-[300px] w-[300px] rounded-full border border-cyan-400/30 bg-gradient-to-br from-cyan-500/10 to-blue-500/10 backdrop-blur-xl"
      >
        {/* Latitude Lines */}
        <div className="absolute left-1/2 top-1/2 h-[280px] w-[280px] -translate-x-1/2 -translate-y-1/2 rounded-full border border-white/10" />
        <div className="absolute left-1/2 top-1/2 h-[220px] w-[280px] -translate-x-1/2 -translate-y-1/2 rounded-full border border-white/10" />
        <div className="absolute left-1/2 top-1/2 h-[160px] w-[280px] -translate-x-1/2 -translate-y-1/2 rounded-full border border-white/10" />

        {/* Longitude Lines */}
        <div className="absolute left-1/2 top-0 h-full w-px -translate-x-1/2 bg-white/10" />
        <div className="absolute left-1/3 top-0 h-full w-px bg-white/10" />
        <div className="absolute right-1/3 top-0 h-full w-px bg-white/10" />

        {/* Heritage Markers */}
        {markers.map((marker, index) => (
          <motion.div
            key={index}
            animate={{
              scale: [1, 1.4, 1],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              delay: index * 0.5,
            }}
            className="absolute h-3 w-3 rounded-full bg-cyan-400 shadow-lg shadow-cyan-400/60"
            style={{
              top: marker.top,
              left: marker.left,
            }}
          />
        ))}
      </motion.div>
    </motion.div>
  );
}