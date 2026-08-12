"use client";

import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";

import HeritageDetailHero from "@/components/explorer/HeritageDetailHero";
import RelatedHeritageSites from "@/components/explorer/RelatedHeritageSites";
import HeritageQuickFacts from "@/components/explorer/HeritageQuickFacts";
import HeritageLocation from "@/components/explorer/HeritageLocation";
import HeritageHistoricalTimeline from "@/components/explorer/HeritageHistoricalTimeline";

import {
  getHeritageSite,
  getHeritageSiteMedia,
  getResolvedHeritageSiteRelations,
  getHeritageSiteHistoricalEvents,
  type HeritageSite,
  type HeritageSiteMedia,
  type HeritageSiteHistoricalEvent,
} from "@/services/heritage";

interface HeritageDetailPageProps {
  params: Promise<{
    siteId: string;
  }>;
}

export default function HeritageDetailPage({
  params,
}: HeritageDetailPageProps) {
  const [site, setSite] = useState<HeritageSite | null>(null);
  const [media, setMedia] =
    useState<HeritageSiteMedia[]>([]);
  const [relatedSites, setRelatedSites] =
    useState<Awaited<
      ReturnType<typeof getResolvedHeritageSiteRelations>
    >>([]);
  const [historicalEvents, setHistoricalEvents] =
    useState<HeritageSiteHistoricalEvent[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function loadSite() {
      try {
        setIsLoading(true);
        setError(null);

        const { siteId } = await params;

        const [
          siteData,
          mediaData,
          relatedSiteData,
          historicalEventData,
        ] = await Promise.all([
          getHeritageSite(siteId),
          getHeritageSiteMedia(siteId),
          getResolvedHeritageSiteRelations(siteId),
          getHeritageSiteHistoricalEvents(siteId),
        ]);

        const activeMedia = mediaData.media
          .filter((media) => media.is_active)
          .sort((a, b) => {
            if (a.media_type !== b.media_type) {
              return a.media_type === "IMAGE" ? -1 : 1;
            }

            if (a.is_primary !== b.is_primary) {
              return a.is_primary ? -1 : 1;
            }

            return a.display_order - b.display_order;
          });

        if (!cancelled) {
          setSite(siteData);
          setMedia(activeMedia);
          setRelatedSites(relatedSiteData);
          setHistoricalEvents(
            historicalEventData.events,
          );
        }
      } catch (err) {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : "Unable to load heritage site.",
          );
        }
      } finally {
        if (!cancelled) {
          setIsLoading(false);
        }
      }
    }

    void loadSite();

    return () => {
      cancelled = true;
    };
  }, [params]);

  return (
    <main className="min-h-screen bg-[var(--heritage-bg)] px-6 py-28">
      <div className="mx-auto max-w-6xl">
        <Link
          href="/explorer"
          className="inline-flex items-center gap-2 text-sm text-[var(--heritage-muted)] transition-colors duration-300 hover:text-[var(--heritage-gold-light)]"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Explorer
        </Link>

        {isLoading && (
          <div className="mt-10">
            <div className="heritage-glass overflow-hidden rounded-[var(--radius-card)]">
              <div className="grid lg:grid-cols-[0.72fr_1.28fr]">
                <div className="p-8">
                  <div className="aspect-[4/3] w-full animate-pulse rounded-2xl bg-white/[0.04]" />
                </div>

                <div className="p-8 md:p-12">
                  <div className="h-6 w-24 animate-pulse rounded bg-white/[0.06]" />
                  <div className="mt-6 h-14 w-2/3 animate-pulse rounded bg-white/[0.06]" />
                  <div className="mt-5 h-5 w-1/3 animate-pulse rounded bg-white/[0.06]" />

                  <div className="mt-8 space-y-3">
                    <div className="h-4 w-full animate-pulse rounded bg-white/[0.06]" />
                    <div className="h-4 w-5/6 animate-pulse rounded bg-white/[0.06]" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {!isLoading && error && (
          <div className="heritage-glass mt-10 rounded-[var(--radius-card)] border-red-400/20 p-8">
            <p className="font-medium text-red-300">
              Unable to load heritage site.
            </p>

            <p className="mt-2 text-sm text-[var(--heritage-muted)]">
              {error}
            </p>
          </div>
        )}

        {!isLoading && !error && site && (
          <article className="mt-10">
            <HeritageDetailHero
              site={site}
              media={media}
            />

            <div className="mt-6">

              <HeritageQuickFacts site={site} />

            </div>


            <div className="mt-6">
                <HeritageLocation site={site} />
              </div>

              <section className="heritage-glass mt-6 rounded-[var(--radius-card)] p-8 md:p-10">
                <p className="text-[10px] font-medium uppercase tracking-[0.2em] text-[var(--heritage-gold)]">
                  The Story
                </p>

                <h2 className="mt-2 text-2xl font-semibold tracking-tight text-[var(--heritage-ivory)]">
                  About this heritage site
                </h2>

                <p className="mt-5 max-w-5xl text-sm leading-8 text-[var(--heritage-muted)] md:text-base">
                  {site.description ??
                    "No detailed description is available."}
                </p>

                {site.significance && (
                  <>
                    <h2 className="mt-10 text-xl font-semibold text-[var(--heritage-ivory)]">
                      Historical significance
                    </h2>

                    <p className="mt-5 max-w-5xl text-sm leading-8 text-[var(--heritage-muted)] md:text-base">
                      {site.significance}
                    </p>
                  </>
                )}
              </section>

              <HeritageHistoricalTimeline
                events={historicalEvents}
              />

              <RelatedHeritageSites
                relations={relatedSites}
              />
          </article>
        )}
      </div>
    </main>
  );
}