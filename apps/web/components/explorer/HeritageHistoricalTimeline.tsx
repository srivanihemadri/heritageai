"use client";

import {
  CalendarDays,
  CheckCircle2,
  Circle,
  History,
} from "lucide-react";

import type {
  HeritageSiteHistoricalEvent,
} from "@/services/heritage";

interface HeritageHistoricalTimelineProps {
  events: HeritageSiteHistoricalEvent[];
}

function formatEventDate(
  event: HeritageSiteHistoricalEvent,
): string {
  if (event.date_label) {
    return event.date_label;
  }

  if (!event.event_date) {
    return "Date unknown";
  }

  const date = new Date(`${event.event_date}T00:00:00`);

  if (Number.isNaN(date.getTime())) {
    return "Date unknown";
  }

  switch (event.date_precision) {
    case "DAY":
      return new Intl.DateTimeFormat("en", {
        day: "numeric",
        month: "long",
        year: "numeric",
      }).format(date);

    case "MONTH":
      return new Intl.DateTimeFormat("en", {
        month: "long",
        year: "numeric",
      }).format(date);

    case "YEAR":
      return new Intl.DateTimeFormat("en", {
        year: "numeric",
      }).format(date);

    case "APPROXIMATE":
      return `c. ${date.getUTCFullYear()}`;

    case "PERIOD":
      return String(date.getUTCFullYear());

    case "UNKNOWN":
    default:
      return String(date.getUTCFullYear());
  }
}

function getTimelineYear(
  event: HeritageSiteHistoricalEvent,
): string {
  if (event.date_label) {
    return event.date_label;
  }

  if (!event.event_date) {
    return "—";
  }

  const date = new Date(`${event.event_date}T00:00:00`);

  if (Number.isNaN(date.getTime())) {
    return "—";
  }

  return String(date.getUTCFullYear());
}

export default function HeritageHistoricalTimeline({
  events,
}: HeritageHistoricalTimelineProps) {
  const activeEvents = events
    .filter((event) => event.is_active)
    .sort((a, b) => {
      if (!a.event_date && !b.event_date) {
        return a.display_order - b.display_order;
      }

      if (!a.event_date) {
        return 1;
      }

      if (!b.event_date) {
        return -1;
      }

      const dateDifference =
        new Date(a.event_date).getTime() -
        new Date(b.event_date).getTime();

      if (dateDifference !== 0) {
        return dateDifference;
      }

      return a.display_order - b.display_order;
    });

  if (activeEvents.length === 0) {
    return null;
  }

  return (
    <section
      aria-labelledby="heritage-historical-timeline"
      className="heritage-glass mt-6 rounded-[var(--radius-card)] p-6 shadow-[0_18px_50px_rgba(0,0,0,0.18)] md:p-9"
    >
      <div className="flex items-end justify-between gap-4">
        <div>
          <p className="text-[10px] font-medium uppercase tracking-[0.2em] text-[var(--heritage-gold)]">
            The Journey
          </p>

          <h2
            id="heritage-historical-timeline"
            className="mt-2 text-2xl font-semibold tracking-tight text-[var(--heritage-ivory)]"
          >
            Historical Timeline
          </h2>
        </div>

        <div className="hidden h-10 w-10 items-center justify-center rounded-full border border-[var(--glass-border)] bg-white/[0.025] sm:flex">
          <History className="h-4 w-4 text-[var(--heritage-gold)]" />
        </div>
      </div>

      <div className="relative mt-10">
        <div className="absolute bottom-0 left-[15px] top-0 w-px bg-[var(--glass-border)] md:left-[119px]" />

        <div className="space-y-10">
          {activeEvents.map((event, index) => {
            const isLast = index === activeEvents.length - 1;

            return (
              <article
                key={event.id}
                className="relative grid gap-4 md:grid-cols-[96px_24px_1fr] md:gap-6"
              >
                <div className="pl-8 md:pl-0 md:pt-1 md:text-right">
                  <p className="text-sm font-semibold text-[var(--heritage-gold-light)]">
                    {getTimelineYear(event)}
                  </p>

                  <p className="mt-1 text-[10px] uppercase tracking-[0.12em] text-[var(--heritage-muted)]">
                    {event.date_precision}
                  </p>
                </div>

                <div className="absolute left-0 top-0 flex h-8 w-8 items-center justify-center md:static md:h-8 md:w-8">
                  <span className="flex h-7 w-7 items-center justify-center rounded-full border border-[var(--heritage-gold-dark)]/60 bg-[var(--heritage-black)]">
                    {event.is_verified ? (
                      <CheckCircle2 className="h-3.5 w-3.5 text-[var(--heritage-gold)]" />
                    ) : (
                      <Circle className="h-3 w-3 text-[var(--heritage-gold-dark)]" />
                    )}
                  </span>
                </div>

                <div
                  className={`rounded-2xl border border-[var(--glass-border)] bg-white/[0.025] p-5 shadow-[0_12px_32px_rgba(0,0,0,0.12)] transition-all duration-300 hover:-translate-y-0.5 hover:border-[var(--glass-border-strong)] hover:bg-white/[0.04] hover:shadow-[0_16px_40px_rgba(0,0,0,0.18)] ${
                    isLast ? "" : ""
                  }`}
                >
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <div>
                      <p className="text-[10px] font-medium uppercase tracking-[0.14em] text-[var(--heritage-muted)]">
                        {formatEventDate(event)}
                      </p>

                      <h3 className="mt-2 text-lg font-semibold tracking-tight text-[var(--heritage-ivory)]">
                        {event.title}
                      </h3>
                    </div>

                    <CalendarDays className="mt-1 h-4 w-4 shrink-0 text-[var(--heritage-gold-dark)]" />
                  </div>

                  {event.description && (
                    <p className="mt-4 text-sm leading-7 text-[var(--heritage-muted)]">
                      {event.description}
                    </p>
                  )}

                  {event.significance && (
                    <div className="mt-5 rounded-xl border border-[var(--glass-border)] bg-white/[0.02] p-4">
                      <p className="text-[10px] font-medium uppercase tracking-[0.14em] text-[var(--heritage-gold)]">
                        Significance
                      </p>

                      <p className="mt-2 text-sm leading-7 text-[var(--heritage-muted)]">
                        {event.significance}
                      </p>
                    </div>
                  )}
                </div>
              </article>
            );
          })}
        </div>
      </div>
    </section>
  );
}
