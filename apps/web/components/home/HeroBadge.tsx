import { Sparkles } from "lucide-react";

export default function HeroBadge() {
  return (
    <div className="heritage-badge w-fit">
      <span className="relative flex h-5 w-5 items-center justify-center rounded-full bg-[rgba(212,175,90,0.10)]">
        <Sparkles
          className="h-3 w-3 text-[var(--heritage-gold-light)]"
          aria-hidden="true"
        />
      </span>

      <span>AI-powered heritage intelligence</span>
    </div>
  );
}
