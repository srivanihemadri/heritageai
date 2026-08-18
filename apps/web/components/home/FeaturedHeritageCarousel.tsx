"use client";

import { useEffect, useMemo, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { ArrowRight, MapPin } from "lucide-react";

import {
  getHeritageSiteMedia,
  getHeritageSites,
  resolveHeritageMediaUrl,
  type HeritageSite,
} from "@/services/heritage";

interface HeritageCard {
  site: HeritageSite;
  imageUrl: string | null;
}

export default function FeaturedHeritageCarousel() {
  const [items, setItems] = useState<HeritageCard[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function loadSites() {
      try {
        setError(null);

        const result = await getHeritageSites({
          page: 1,
          page_size: 12,
        });

        const cards = await Promise.all(
          result.sites.map(async (site) => {
            try {
              const media = await getHeritageSiteMedia(site.id);

              const primary =
                media.media.find(
                  (item) => item.is_active && item.is_primary,
                ) ??
                media.media.find((item) => item.is_active) ??
                null;

              return {
                site,
                imageUrl: primary
                  ? resolveHeritageMediaUrl(primary.url)
                  : null,
              };
            } catch {
              return {
                site,
                imageUrl: null,
              };
            }
          }),
        );

        if (!cancelled) {
          setItems(cards);
        }
      } catch {
        if (!cancelled) {
          setError("Unable to load featured heritage.");
        }
      }
    }

    void loadSites();

    return () => {
      cancelled = true;
    };
  }, []);

  const duplicatedItems = useMemo(
    () => [...items, ...items],
    [items],
  );

  if (error || items.length === 0) {
    return null;
  }

  return (
    <section className="relative overflow-hidden py-10 sm:py-14">
      <div className="heritage-container">
        <div className="mb-5 flex items-end justify-between gap-4">
          <div>
            <p className="text-[10px] font-semibold uppercase tracking-[0.24em] text-[var(--heritage-gold-light)]">
              Featured Heritage
            </p>

            <h2 className="mt-2 text-2xl font-semibold tracking-tight text-[var(--heritage-ivory)] sm:text-3xl">
              Explore extraordinary places
            </h2>
          </div>

          <Link
            href="/explorer"
            className="hidden items-center gap-2 text-sm font-medium text-[var(--heritage-gold-light)] transition hover:text-[var(--heritage-ivory)] sm:flex"
          >
            View all
            <ArrowRight className="h-4 w-4" />
          </Link>
        </div>

        <div className="relative overflow-hidden">
          <div className="heritage-feature-marquee flex w-max gap-4">
            {duplicatedItems.map(({ site, imageUrl }, index) => (
              <Link
                href={`/explorer/${site.id}`}
                key={`${site.id}-${index}`}
                className="group block w-[250px] shrink-0 sm:w-[280px]"
              >
                <article className="heritage-glass overflow-hidden rounded-[24px] border border-[var(--glass-border)] transition-all duration-300 group-hover:-translate-y-1 group-hover:border-[var(--glass-border-hover)]">
                  <div className="relative aspect-[1.18] overflow-hidden bg-[var(--heritage-charcoal)]">
                    {imageUrl ? (
                      <Image
                        src={imageUrl}
                        alt={site.name}
                        fill
                        sizes="280px"
                        className="object-cover transition-transform duration-700 group-hover:scale-105"
                      />
                    ) : (
                      <div className="flex h-full items-center justify-center bg-[var(--heritage-charcoal)] px-6 text-center">
                        <span className="text-sm text-[var(--heritage-muted)]">
                          {site.name}
                        </span>
                      </div>
                    )}

                    <div className="absolute inset-0 bg-gradient-to-t from-[rgba(11,9,7,0.88)] via-transparent to-transparent" />
                  </div>

                  <div className="p-4">
                    <span className="heritage-badge">
                      {site.category}
                    </span>

                    <h3 className="mt-3 line-clamp-1 text-base font-semibold text-[var(--heritage-ivory)]">
                      {site.name}
                    </h3>

                    <div className="mt-2 flex items-center gap-1.5 text-xs text-[var(--heritage-muted)]">
                      <MapPin className="h-3.5 w-3.5 text-[var(--heritage-gold)]" />
                      <span className="line-clamp-1">
                        {[site.city, site.country]
                          .filter(Boolean)
                          .join(", ")}
                      </span>
                    </div>
                  </div>
                </article>
              </Link>
            ))}
          </div>
        </div>

        <Link
          href="/explorer"
          className="heritage-button heritage-button-glass mt-5 inline-flex min-h-10 sm:hidden"
        >
          View all heritage
          <ArrowRight className="h-4 w-4" />
        </Link>
      </div>
    </section>
  );
}
