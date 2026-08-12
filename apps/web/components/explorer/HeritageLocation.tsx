import {
  ExternalLink,
  MapPin,
  Navigation,
} from "lucide-react";

import type { HeritageSite } from "@/services/heritage";

interface HeritageLocationProps {
  site: HeritageSite;
}

export default function HeritageLocation({
  site,
}: HeritageLocationProps) {
  const location = [site.city, site.state, site.country]
    .filter(Boolean)
    .join(", ");

  const hasCoordinates =
    site.latitude !== null &&
    site.longitude !== null;

  const googleMapsUrl = hasCoordinates
    ? `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
        `${site.latitude},${site.longitude}`,
      )}`
    : null;

  if (!location && !hasCoordinates) {
    return null;
  }

  return (
    <section
      aria-labelledby="heritage-location"
      className="heritage-glass overflow-hidden rounded-[var(--radius-card)]"
    >
      <div className="border-b border-[var(--glass-border)] px-6 py-5 md:px-8">
        <p className="text-[10px] font-medium uppercase tracking-[0.2em] text-[var(--heritage-gold)]">
          Discover the place
        </p>

        <h2
          id="heritage-location"
          className="mt-2 text-2xl font-semibold tracking-tight text-[var(--heritage-ivory)]"
        >
          Location
        </h2>
      </div>

      <div className="grid gap-6 p-6 md:p-8 lg:grid-cols-[1fr_auto] lg:items-center">
        <div className="flex items-start gap-4">
          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl border border-[var(--glass-border)] bg-white/[0.025]">
            <MapPin className="h-5 w-5 text-[var(--heritage-gold)]" />
          </div>

          <div>
            <p className="text-sm font-medium text-[var(--heritage-ivory)]">
              {location || "Location coordinates available"}
            </p>

            {hasCoordinates && (
              <div className="mt-2 flex items-center gap-2 text-xs text-[var(--heritage-muted)]">
                <Navigation className="h-3.5 w-3.5 text-[var(--heritage-gold-dark)]" />

                <span>
                  {site.latitude}, {site.longitude}
                </span>
              </div>
            )}
          </div>
        </div>

        {googleMapsUrl && (
          <a
            href={googleMapsUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex w-fit items-center gap-2 rounded-full border border-[var(--heritage-gold-dark)]/60 bg-[var(--heritage-gold)]/[0.06] px-5 py-3 text-xs font-semibold text-[var(--heritage-gold-light)] transition-all duration-300 hover:border-[var(--heritage-gold)] hover:bg-[var(--heritage-gold)]/[0.12] hover:shadow-[0_0_24px_rgba(212,175,55,0.12)] focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--heritage-gold)]"
          >
            <MapPin className="h-3.5 w-3.5" />
            Open in Google Maps
            <ExternalLink className="h-3.5 w-3.5" />
          </a>
        )}
      </div>
    </section>
  );
}