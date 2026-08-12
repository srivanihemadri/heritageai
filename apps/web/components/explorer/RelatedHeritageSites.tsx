"use client";

import React from "react";

import Image from "next/image";
import {
  ArrowRight,
  Link2,
  MapPin,
  ShieldCheck,
} from "lucide-react";
import Link from "next/link";

import {
  getHeritageSiteMedia,
  type HeritageSiteMedia,
  type ResolvedHeritageSiteRelation,
} from "@/services/heritage";

interface RelatedHeritageSitesProps {
  relations: ResolvedHeritageSiteRelation[];
}

function formatRelationType(
  relationType: ResolvedHeritageSiteRelation["relation"]["relation_type"],
): string {
  return relationType
    .toLowerCase()
    .replaceAll("_", " ")
    .replace(/\b\w/g, (character) => character.toUpperCase());
}

export default function RelatedHeritageSites({
  relations,
}: RelatedHeritageSitesProps) {
  const [mediaBySiteId, setMediaBySiteId] = React.useState<
    Record<string, HeritageSiteMedia | null>
  >({});

  React.useEffect(() => {
    let cancelled = false;

    async function loadRelatedSiteMedia() {
      const results = await Promise.all(
        relations.map(async ({ site }) => {
          try {
            const response = await getHeritageSiteMedia(site.id);

            const primaryImage =
              response.media
                .filter(
                  (media) =>
                    media.media_type === "IMAGE" &&
                    media.is_active,
                )
                .sort((a, b) => {
                  if (a.is_primary !== b.is_primary) {
                    return a.is_primary ? -1 : 1;
                  }

                  return a.display_order - b.display_order;
                })[0] ?? null;

            return [site.id, primaryImage] as const;
          } catch {
            return [site.id, null] as const;
          }
        }),
      );

      if (!cancelled) {
        setMediaBySiteId(Object.fromEntries(results));
      }
    }

    if (relations.length > 0) {
      void loadRelatedSiteMedia();
    } else {
      setMediaBySiteId({});
    }

    return () => {
      cancelled = true;
    };
  }, [relations]);

  if (relations.length === 0) {
    return null;
  }

  return (
    <section
      aria-labelledby="related-heritage-sites"
      className="mt-6 heritage-glass rounded-[var(--radius-card)] p-6 shadow-[0_18px_50px_rgba(0,0,0,0.18)] md:p-9"
    >
      <div className="flex items-end justify-between gap-4">
        <div>
          <p className="text-[10px] font-medium uppercase tracking-[0.2em] text-[var(--heritage-gold)]">
            Explore Further
          </p>

          <h2
            id="related-heritage-sites"
            className="mt-2 text-2xl font-semibold tracking-tight text-[var(--heritage-ivory)]"
          >
            Related Heritage Sites
          </h2>
        </div>

        <div className="hidden h-10 w-10 items-center justify-center rounded-full border border-[var(--glass-border)] bg-white/[0.025] sm:flex">
          <Link2 className="h-4 w-4 text-[var(--heritage-gold)]" />
        </div>
      </div>

      <div className="mt-8 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
        {relations.map(({ relation, site }) => {
          const location = [site.city, site.state, site.country]
            .filter(Boolean)
            .join(", ");

          const primaryImage = mediaBySiteId[site.id];

          return (
            <Link
              key={relation.id}
              href={`/explorer/${site.id}`}
              className="group block"
              aria-label={`View ${site.name}`}
            >
              <article className="h-full overflow-hidden rounded-2xl border border-[var(--glass-border)] bg-white/[0.025] shadow-[0_12px_32px_rgba(0,0,0,0.12)] transition-all duration-300 hover:-translate-y-1 hover:border-[var(--glass-border-strong)] hover:bg-white/[0.04] hover:shadow-[0_18px_42px_rgba(0,0,0,0.18)]">
                <div className="p-3">
                  <div className="relative aspect-[16/9] overflow-hidden rounded-xl border border-[var(--glass-border)] bg-black/20">
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
                          sizes="(max-width: 768px) 100vw, 50vw"
                          className="object-cover transition-transform duration-700 group-hover:scale-[1.025]"
                        />

                        <div className="pointer-events-none absolute inset-0 bg-gradient-to-t from-black/35 via-transparent to-transparent" />

                        <div className="pointer-events-none absolute inset-0 rounded-xl ring-1 ring-inset ring-white/10" />
                      </>
                    ) : (
                      <div className="flex h-full items-center justify-center">
                        <MapPin className="h-6 w-6 text-[var(--heritage-gold-dark)]" />
                      </div>
                    )}
                  </div>
                </div>

                <div className="p-5 pt-2">
                  <div className="flex items-start justify-between gap-4">
                    <span className="inline-flex items-center gap-1.5 rounded-full border border-[var(--heritage-gold-dark)]/40 bg-[var(--heritage-gold)]/[0.05] px-3 py-1 text-[10px] font-medium uppercase tracking-[0.12em] text-[var(--heritage-gold-light)]">
                      <Link2 className="h-3 w-3" />
                      {formatRelationType(relation.relation_type)}
                    </span>

                    {site.is_verified && (
                      <span className="inline-flex items-center gap-1 text-[10px] font-medium text-[var(--heritage-gold)]">
                        <ShieldCheck className="h-3 w-3" />
                        Verified
                      </span>
                    )}
                  </div>

                  <h3 className="mt-5 text-lg font-semibold tracking-tight text-[var(--heritage-ivory)] transition-colors duration-300 group-hover:text-[var(--heritage-gold-light)]">
                    {site.name}
                  </h3>

                  {location && (
                    <div className="mt-2 flex items-center gap-1.5 text-xs text-[var(--heritage-muted)]">
                      <MapPin className="h-3.5 w-3.5 shrink-0 text-[var(--heritage-gold-dark)]" />
                      <span>{location}</span>
                    </div>
                  )}

                  <p className="mt-4 line-clamp-3 text-sm leading-7 text-[var(--heritage-muted)]">
                    {site.short_description ??
                      site.description ??
                      "Explore this heritage site and discover its historical significance."}
                  </p>

                  {relation.description && (
                    <p className="mt-4 border-t border-[var(--glass-border)] pt-4 text-xs leading-6 text-[var(--heritage-muted)]">
                      {relation.description}
                    </p>
                  )}

                  <div className="mt-5 flex items-center justify-between border-t border-[var(--glass-border)] pt-4">
                    <span className="text-xs text-[var(--heritage-muted)]">
                      {site.historical_period ?? "Historical site"}
                    </span>

                    <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-[var(--heritage-gold)] transition-transform duration-300 group-hover:translate-x-1">
                      Explore
                      <ArrowRight className="h-3.5 w-3.5" />
                    </span>
                  </div>
                </div>
              </article>
            </Link>
          );
        })}
      </div>
    </section>
  );
}
