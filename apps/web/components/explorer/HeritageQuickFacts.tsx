import {
  CalendarDays,
  Landmark,
  MapPin,
  Navigation,
  ShieldCheck,
} from "lucide-react";

import type { HeritageSite } from "@/services/heritage";

interface HeritageQuickFactsProps {
  site: HeritageSite;
}

interface FactItem {
  label: string;
  value: string;
  icon: typeof MapPin;
}

export default function HeritageQuickFacts({
  site,
}: HeritageQuickFactsProps) {
  const location = [site.city, site.state, site.country]
    .filter(Boolean)
    .join(", ");

  const coordinates =
    site.latitude !== null &&
    site.longitude !== null
      ? `${site.latitude}, ${site.longitude}`
      : null;

  const facts: FactItem[] = [
    location
      ? {
          label: "Location",
          value: location,
          icon: MapPin,
        }
      : null,

    site.historical_period
      ? {
          label: "Historical Period",
          value: site.historical_period,
          icon: Landmark,
        }
      : null,

    site.established_year !== null
      ? {
          label: "Established",
          value: String(site.established_year),
          icon: CalendarDays,
        }
      : null,

    site.architectural_style
      ? {
          label: "Architectural Style",
          value: site.architectural_style,
          icon: Landmark,
        }
      : null,

    site.preservation_status
      ? {
          label: "Preservation",
          value: site.preservation_status,
          icon: ShieldCheck,
        }
      : null,

    coordinates
      ? {
          label: "Coordinates",
          value: coordinates,
          icon: Navigation,
        }
      : null,
  ].filter((fact): fact is FactItem => fact !== null);

  if (facts.length === 0) {
    return null;
  }

  return (
    <section
      aria-labelledby="heritage-quick-facts"
      className="heritage-glass rounded-[var(--radius-card)] p-6 md:p-8"
    >
      <div className="flex items-end justify-between gap-4">
        <div>
          <p className="text-[10px] font-medium uppercase tracking-[0.2em] text-[var(--heritage-gold)]">
            At a glance
          </p>

          <h2
            id="heritage-quick-facts"
            className="mt-2 text-2xl font-semibold tracking-tight text-[var(--heritage-ivory)]"
          >
            Quick Facts
          </h2>
        </div>

        <div className="hidden h-10 w-10 items-center justify-center rounded-full border border-[var(--glass-border)] bg-white/[0.025] sm:flex">
          <Landmark className="h-4 w-4 text-[var(--heritage-gold)]" />
        </div>
      </div>

      <div className="mt-7 grid gap-px overflow-hidden rounded-2xl border border-[var(--glass-border)] bg-[var(--glass-border)] sm:grid-cols-2 lg:grid-cols-3">
        {facts.map((fact) => {
          const Icon = fact.icon;

          return (
            <div
              key={fact.label}
              className="bg-[var(--heritage-bg)]/80 p-5 transition-colors duration-300 hover:bg-white/[0.035]"
            >
              <div className="flex items-start gap-3">
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-[var(--glass-border)] bg-white/[0.025]">
                  <Icon className="h-4 w-4 text-[var(--heritage-gold)]" />
                </div>

                <div className="min-w-0">
                  <p className="text-[10px] font-medium uppercase tracking-[0.14em] text-[var(--heritage-muted)]">
                    {fact.label}
                  </p>

                  <p className="mt-1.5 break-words text-sm leading-6 text-[var(--heritage-ivory)]">
                    {fact.value}
                  </p>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}