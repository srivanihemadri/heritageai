import Link from "next/link";

export interface LogoProps {
  href?: string;
  compact?: boolean;
  className?: string;
}

export default function Logo({
  href = "/",
  compact = false,
  className = "",
}: LogoProps) {
  const content = (
    <span
      className={`inline-flex items-center gap-2 ${className}`}
      aria-label="HeritageAI"
    >
      <span className="relative flex h-9 w-9 items-center justify-center overflow-hidden rounded-xl border border-[var(--glass-border-strong)] bg-[rgba(212,175,90,0.08)] shadow-[0_0_24px_rgba(212,175,90,0.10)]">
        <span className="absolute inset-0 bg-[radial-gradient(circle_at_35%_25%,rgba(240,207,122,0.24),transparent_55%)]" />

        <svg
          viewBox="0 0 32 32"
          fill="none"
          className="relative h-5 w-5 text-[var(--heritage-gold-light)]"
          aria-hidden="true"
        >
          <path
            d="M7 25V12.5L16 7L25 12.5V25"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          <path
            d="M11 25V15.5H21V25M16 15.5V25"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
          />
          <path
            d="M5 25H27"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinecap="round"
          />
        </svg>
      </span>

      {!compact && (
        <span className="text-lg font-semibold tracking-[-0.03em]">
          <span className="text-[var(--heritage-ivory)]">Heritage</span>
          <span className="heritage-gold-gradient">AI</span>
        </span>
      )}
    </span>
  );

  return (
    <Link
      href={href}
      className="rounded-xl outline-none focus-visible:ring-2 focus-visible:ring-[var(--heritage-gold)] focus-visible:ring-offset-2 focus-visible:ring-offset-[var(--heritage-black)]"
    >
      {content}
    </Link>
  );
}
