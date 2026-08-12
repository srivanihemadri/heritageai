"use client";

import Image from "next/image";
import { MapPin, ShieldCheck, ImageOff } from "lucide-react";
import Link from "next/link";

import type { HeritageSite, HeritageSiteMedia } from "@/services/heritage";

interface HeritageCardProps {
  site: HeritageSite;
  primaryImage: HeritageSiteMedia | null;
}

export default function HeritageCard({
  site,
  primaryImage,
}: HeritageCardProps) {

  const location = [site.city, site.state, site.country]
    .filter(Boolean)
    .join(", ");

  return (
    <Link
      href={`/explorer/${site.id}`}
      className="group block"
      aria-label={`View details for ${site.name}`}
    >
      <article className="heritage-glass flex h-full flex-col overflow-hidden rounded-[var(--radius-card)] transition-all duration-300 hover:-translate-y-1 hover:border-[var(--glass-border-strong)] hover:shadow-[0_20px_60px_rgba(0,0,0,0.28)]">
        <div className="relative aspect-[16/10] shrink-0 overflow-hidden border-b border-[var(--glass-border)] bg-black/20">
          {primaryImage ? (
            <>
              <Image
                src={primaryImage.url}
                alt={
                  primaryImage.alt_text ??
                  primaryImage.title ??
                  site.name
                }
                fill
                sizes="(max-width: 768px) 100vw, (max-width: 1280px) 50vw, 33vw"
                className="object-cover transition-transform duration-700 ease-out group-hover:scale-[1.04]"
              />

              <div className="pointer-events-none absolute inset-0 bg-gradient-to-t from-black/65 via-black/10 to-black/5" />

              <div className="pointer-events-none absolute inset-0 ring-1 ring-inset ring-white/10" />
            </>
          ) : (
            <div className="flex h-full flex-col items-center justify-center gap-2 bg-white/[0.015]">
              <ImageOff className="h-7 w-7 text-[var(--heritage-gold-dark)]" />

              <span className="text-[10px] font-medium uppercase tracking-[0.16em] text-[var(--heritage-muted)]">
                Heritage image unavailable
              </span>
            </div>
          )}

          <div className="absolute left-4 right-4 top-4 flex items-start justify-between gap-3">
            <span className="rounded-full border border-white/15 bg-black/40 px-3 py-1.5 text-[10px] font-semibold uppercase tracking-[0.14em] text-[var(--heritage-gold-light)] shadow-[0_8px_24px_rgba(0,0,0,0.22)] backdrop-blur-lg">
              {site.category}
            </span>

            {site.is_verified && (
                <span className="inline-flex items-center gap-1.5 rounded-full border border-white/15 bg-black/40 px-3 py-1.5 text-[10px] font-semibold uppercase tracking-[0.12em] text-[var(--heritage-gold-light)] shadow-[0_8px_24px_rgba(0,0,0,0.22)] backdrop-blur-lg">
                <ShieldCheck className="h-3.5 w-3.5" />
                Verified
              </span>
            )}
          </div>
        </div>

        <div className="flex flex-1 flex-col p-6">
          <h2 className="text-xl font-semibold tracking-tight text-[var(--heritage-ivory)] transition-colors duration-300 group-hover:text-[var(--heritage-gold-light)]">
            {site.name}
          </h2>

          {location && (
            <div className="mt-2 flex items-center gap-1.5 text-xs text-[var(--heritage-muted)]">
              <MapPin className="h-3.5 w-3.5 shrink-0 text-[var(--heritage-gold-dark)]" />
              <span>{location}</span>
            </div>
          )}

          <p className="mt-5 line-clamp-3 min-h-[5.25rem] text-sm leading-7 text-[var(--heritage-muted)]">
            {site.short_description ??
              site.description ??
              "Historical heritage site."}
          </p>

          <div className="mt-auto flex items-center justify-between gap-4 border-t border-[var(--glass-border)] pt-5">
            <span className="text-xs text-[var(--heritage-muted)]">
              {site.historical_period ?? "Historical site"}
            </span>

            <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-[var(--heritage-gold)] transition-transform duration-300 group-hover:translate-x-1">
              <span>{site.established_year ?? "—"}</span>
              <span className="text-[10px] font-medium uppercase tracking-[0.14em] opacity-80">Established</span>
            </span>
          </div>
        </div>
      </article>
    </Link>
  );
}
