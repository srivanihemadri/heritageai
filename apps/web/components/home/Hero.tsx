"use client";

import { useEffect, useState } from "react";
import { motion, useReducedMotion } from "framer-motion";
import Link from "next/link";
import { ArrowRight, ChevronLeft, ChevronRight, Sparkles } from "lucide-react";
import HeroBackground from "./HeroBackground";
import HeroBadge from "./HeroBadge";
import HeroStats from "./HeroStats";
import {
  getHeritageSiteMedia,
  getHeritageSites,
  resolveHeritageMediaUrl,
  type HeritageSite,
} from "@/services/heritage";

const HERO_EASE = [0.22, 1, 0.36, 1] as const;

export default function Hero() {
  const reduceMotion = useReducedMotion();

  interface HeroGalleryItem {
    site: HeritageSite;
    imageUrl: string;
  }

  const [gallery, setGallery] = useState<HeroGalleryItem[]>([]);
  const [galleryIndex, setGalleryIndex] = useState(0);

  useEffect(() => {
    let cancelled = false;

    async function loadGallery() {
      try {
        const result = await getHeritageSites({
          page: 1,
          page_size: 12,
        });

        const items = await Promise.all(
          result.sites.map(async (site) => {
            try {
              const mediaResult = await getHeritageSiteMedia(
                site.id,
              );

              const primary =
                mediaResult.media.find(
                  (media) =>
                    media.is_active &&
                    media.media_type === "IMAGE" &&
                    media.is_primary,
                ) ??
                mediaResult.media.find(
                  (media) =>
                    media.is_active &&
                    media.media_type === "IMAGE",
                ) ??
                null;

              if (!primary) {
                return null;
              }

              return {
                site,
                imageUrl: resolveHeritageMediaUrl(primary.url),
              };
            } catch {
              return null;
            }
          }),
        );

        const validItems = items.filter(
          (item): item is HeroGalleryItem => item !== null,
        );

        if (!cancelled) {
          setGallery(validItems);
          setGalleryIndex(0);
        }
      } catch {
        if (!cancelled) {
          setGallery([]);
        }
      }
    }

    void loadGallery();

    return () => {
      cancelled = true;
    };
  }, []);

  const currentGalleryItem =
    gallery[galleryIndex] ?? null;

  const currentGalleryImage =
    currentGalleryItem?.imageUrl ?? null;

  const currentGallerySite =
    currentGalleryItem?.site ?? null;

  const showPreviousImage = () => {
    setGalleryIndex((current) => Math.max(0, current - 1));
  };

  const showNextImage = () => {
    setGalleryIndex((current) =>
      Math.min(gallery.length - 1, current + 1),
    );
  };

  const fadeUp = {
    hidden: {
      opacity: 0,
      y: reduceMotion ? 0 : 24,
    },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: reduceMotion ? 0 : 0.7,
        ease: HERO_EASE,
      },
    },
  };

  return (
    <section className="relative isolate min-h-[calc(100svh-5rem)] overflow-hidden">
      <HeroBackground />

      <div className="heritage-container relative flex min-h-[calc(100svh-5rem)] items-center py-20 sm:py-24 lg:py-28">
        <div className="grid w-full items-center gap-14 lg:grid-cols-[1.08fr_0.92fr] lg:gap-16">
          <motion.div
            initial="hidden"
            animate="visible"
            variants={fadeUp}
            className="max-w-3xl"
          >
            <HeroBadge />

            <h1 className="mt-7 max-w-4xl text-balance text-[clamp(3.25rem,8vw,7rem)] font-semibold leading-[0.91] tracking-[-0.065em] text-[var(--heritage-ivory)]">
              Discover the
              <span className="block heritage-gold-gradient">
                stories behind history.
              </span>
            </h1>

            <p className="mt-7 max-w-2xl text-base leading-7 text-[var(--heritage-muted)] sm:text-lg sm:leading-8">
              Explore the world&apos;s cultural heritage with AI-powered
              discovery, visual understanding and historically grounded
              knowledge.
            </p>

            <div className="mt-9 flex flex-col gap-3 sm:flex-row">
              <Link
                href="/explorer"
                className="heritage-button heritage-button-gold heritage-gold-glow group min-h-12 px-6"
              >
                Explore Heritage
                <ArrowRight
                  className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-1"
                  aria-hidden="true"
                />
              </Link>

            </div>

            <div className="mt-10">
              <HeroStats />
            </div>
          </motion.div>

          <motion.div
            initial={{
              opacity: 0,
              y: reduceMotion ? 0 : 30,
              scale: reduceMotion ? 1 : 0.98,
            }}
            animate={{
              opacity: 1,
              y: 0,
              scale: 1,
            }}
            transition={{
              duration: reduceMotion ? 0 : 0.9,
              delay: reduceMotion ? 0 : 0.15,
              ease: HERO_EASE,
            }}
            className="relative mx-auto w-full max-w-md -translate-y-3 lg:ml-auto lg:-translate-y-8"
          >
            <div className="relative aspect-[0.95] overflow-hidden rounded-[32px] border border-[var(--glass-border-strong)] bg-[rgba(30,25,19,0.48)] p-2 shadow-[0_30px_100px_rgba(0,0,0,0.45)] backdrop-blur-2xl">
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_15%,rgba(240,207,122,0.18),transparent_42%)]" />

              <div className="relative h-full overflow-hidden rounded-[26px] border border-white/[0.08] bg-[var(--heritage-charcoal)]">
                <div className="absolute inset-0">
                  {currentGalleryImage ? (
                    <img
                      src={currentGalleryImage}
                      alt="Brihadeeswarar Temple"
                      className="h-full w-full object-cover transition-opacity duration-300"
                    />
                  ) : (
                    <div
                      className="h-full w-full bg-cover bg-center"
                      style={{
                        backgroundImage:
                          "url('/heritage/brihadeeswarar-temple.jpg')",
                      }}
                    />
                  )}
                </div>

                <div className="absolute inset-0 bg-gradient-to-t from-[rgba(11,9,7,0.96)] via-[rgba(11,9,7,0.20)] to-transparent" />

                {gallery.length > 1 && (
                  <>
                    {galleryIndex > 0 && (
                      <button
                        type="button"
                        onClick={showPreviousImage}
                        aria-label="Previous heritage site"
                        className="absolute left-4 top-1/2 z-20 flex h-10 w-10 -translate-y-1/2 items-center justify-center rounded-full border border-white/15 bg-[rgba(11,9,7,0.55)] text-[var(--heritage-ivory)] backdrop-blur-xl transition hover:bg-[rgba(11,9,7,0.78)]"
                      >
                        <ChevronLeft className="h-5 w-5" />
                      </button>
                    )}

                    {galleryIndex < gallery.length - 1 && (
                      <button
                        type="button"
                        onClick={showNextImage}
                        aria-label="Next heritage site"
                        className="absolute right-4 top-1/2 z-20 flex h-10 w-10 -translate-y-1/2 items-center justify-center rounded-full border border-white/15 bg-[rgba(11,9,7,0.55)] text-[var(--heritage-ivory)] backdrop-blur-xl transition hover:bg-[rgba(11,9,7,0.78)]"
                      >
                        <ChevronRight className="h-5 w-5" />
                      </button>
                    )}

                    <div className="absolute left-1/2 top-4 z-20 -translate-x-1/2 rounded-full border border-white/10 bg-[rgba(11,9,7,0.48)] px-3 py-1.5 text-[10px] font-semibold tracking-[0.18em] text-[var(--heritage-ivory)] backdrop-blur-xl">
                      {galleryIndex + 1} / {gallery.length}
                    </div>
                  </>
                )}

                <div className="absolute inset-x-5 bottom-5 sm:inset-x-7 sm:bottom-7">
                  <div className="heritage-glass-strong rounded-2xl p-5 sm:p-6">
                    <div className="flex items-center justify-between gap-4">
                      <div>
                        <p className="text-[10px] font-semibold uppercase tracking-[0.2em] text-[var(--heritage-gold-light)]">
                          Featured Heritage
                        </p>

                        <h2 className="mt-2 text-xl font-semibold tracking-tight text-[var(--heritage-ivory)] sm:text-2xl">
                          {currentGallerySite?.name ??
                            "Brihadeeswarar Temple"}
                        </h2>

                        <p className="mt-1 text-sm text-[var(--heritage-muted)]">
                          {currentGallerySite
                            ? [
                                currentGallerySite.city,
                                currentGallerySite.state,
                              ]
                                .filter(Boolean)
                                .join(", ")
                            : "Thanjavur, Tamil Nadu"}
                        </p>
                      </div>

                      <div className="hidden h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-[var(--glass-border)] bg-[rgba(212,175,90,0.08)] sm:flex">
                        <Sparkles
                          className="h-4 w-4 text-[var(--heritage-gold-light)]"
                          aria-hidden="true"
                        />
                      </div>
                    </div>

                    <div className="mt-5 flex flex-wrap gap-2">
                      <span className="heritage-badge">
                        {currentGallerySite?.category ??
                          "Temple"}
                      </span>

                      {currentGallerySite?.architectural_style && (
                        <span className="heritage-badge">
                          {currentGallerySite.architectural_style}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {!reduceMotion && (
              <>
                <div className="pointer-events-none absolute -right-5 top-12 h-24 w-24 rounded-full bg-[rgba(212,175,90,0.10)] blur-3xl" />
                <div className="pointer-events-none absolute -bottom-8 -left-8 h-32 w-32 rounded-full bg-[rgba(155,117,48,0.08)] blur-3xl" />
              </>
            )}
          </motion.div>
        </div>
      </div>
    </section>
  );
}
