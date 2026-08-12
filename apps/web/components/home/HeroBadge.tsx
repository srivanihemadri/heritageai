"use client";

import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";

export default function HeroBadge() {
  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.7 }}
      className="heritage-glass inline-flex items-center gap-2 rounded-full px-5 py-2 text-xs font-medium tracking-wide text-[var(--heritage-gold-light)] md:text-sm"
    >
      <Sparkles className="h-4 w-4 text-[var(--heritage-gold)]" />
      AI-Powered Heritage Preservation Platform
    </motion.div>
  );
}
