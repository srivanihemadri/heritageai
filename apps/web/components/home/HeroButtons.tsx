"use client";

import Link from "next/link";
import { ArrowRight, Sparkles } from "lucide-react";

export default function HeroButtons() {
  return (
    <div className="flex flex-col gap-3 sm:flex-row">
      <Link
        href="/explorer"
        className="heritage-button heritage-button-gold heritage-gold-glow group min-h-12 px-6"
      >
        Explore Heritage
        <ArrowRight
          className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-1"
          aria-hidden="true"
        />
      </Link>

      <Link
        href="/chat"
        className="heritage-button heritage-button-glass group min-h-12 px-6"
      >
        <Sparkles
          className="h-4 w-4 text-[var(--heritage-gold)]"
          aria-hidden="true"
        />
        Ask HeritageAI
      </Link>
    </div>
  );
}
