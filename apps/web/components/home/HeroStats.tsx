const stats = [
  {
    value: "AI",
    label: "Heritage Intelligence",
  },
  {
    value: "24/7",
    label: "Discovery",
  },
  {
    value: "∞",
    label: "Stories to Explore",
  },
];

export default function HeroStats() {
  return (
    <div className="grid max-w-xl grid-cols-3 divide-x divide-[var(--glass-border)] border-y border-[var(--glass-border)] py-4">
      {stats.map((stat) => (
        <div key={stat.label} className="px-3 first:pl-0 sm:px-5">
          <p className="text-lg font-semibold tracking-tight text-[var(--heritage-gold-light)] sm:text-xl">
            {stat.value}
          </p>

          <p className="mt-1 text-[10px] leading-4 text-[var(--heritage-muted)] sm:text-xs">
            {stat.label}
          </p>
        </div>
      ))}
    </div>
  );
}
