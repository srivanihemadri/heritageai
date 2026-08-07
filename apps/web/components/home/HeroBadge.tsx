"use client";

import { motion } from "framer-motion";

export default function HeroBadge() {
  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.7 }}
      className="inline-flex items-center gap-2 rounded-full border border-cyan-400/30 bg-cyan-500/10 px-5 py-2 text-sm font-medium text-cyan-300 backdrop-blur-xl"
    >
      <span>🚀</span>
      <span>AI Powered Heritage Preservation Platform</span>
    </motion.div>
  );
}