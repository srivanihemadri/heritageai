"use client";

import Image from "next/image";
import {
  ChevronLeft,
  ChevronRight,
  MapPin,
  ShieldCheck,
  X,
} from "lucide-react";
import { useEffect, useState } from "react";

import type {
  HeritageSite,
  HeritageSiteMedia,
} from "@/services/heritage";

interface HeritageDetailHeroProps {
  site: HeritageSite;
  media: HeritageSiteMedia[];
}

export default function HeritageDetailHero({
  site,
  media,
}: HeritageDetailHeroProps) {
  const location = [site.city, site.state, site.country]
    .filter(Boolean)
    .join(", ");

  const images = media
    .filter(
      (item) =>
        item.media_type === "IMAGE" &&
        item.is_active,
    )
    .sort((a, b) => {
      if (a.is_primary !== b.is_primary) {
        return a.is_primary ? -1 : 1;
      }

      return a.display_order - b.display_order;
    });

  const [selectedImageId, setSelectedImageId] = useState(
    images[0]?.id ?? null,
  );

  const [isViewerOpen, setIsViewerOpen] = useState(false);

  const selectedIndex = Math.max(
    0,
    images.findIndex(
      (image) => image.id === selectedImageId,
    ),
  );

  const selectedImage =
    images[selectedIndex] ??
    images[0] ??
    null;
function openViewer() {
    if (selectedImage) {
      setIsViewerOpen(true);
    }
  }

  function closeViewer() {
    setIsViewerOpen(false);
  }

  function showPreviousImage() {
    if (images.length < 2) {
      return;
    }

    const previousIndex =
      selectedIndex === 0
        ? images.length - 1
        : selectedIndex - 1;

    const previousImage = images[previousIndex];

    if (previousImage) {
      setSelectedImageId(previousImage.id);
    }
  }

  function showNextImage() {
    if (images.length < 2) {
      return;
    }

    const nextIndex =
      selectedIndex === images.length - 1
        ? 0
        : selectedIndex + 1;

    const nextImage = images[nextIndex];

    if (nextImage) {
      setSelectedImageId(nextImage.id);
    }
  }

  useEffect(() => {
    if (!isViewerOpen) {
      return;
    }

    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        closeViewer();
      }

      if (event.key === "ArrowLeft") {
        const previousIndex =
          selectedIndex === 0
            ? images.length - 1
            : selectedIndex - 1;

        const previousImage = images[previousIndex];

        if (previousImage) {
          setSelectedImageId(previousImage.id);
        }
      }

      if (event.key === "ArrowRight") {
        const nextIndex =
          selectedIndex === images.length - 1
            ? 0
            : selectedIndex + 1;

        const nextImage = images[nextIndex];

        if (nextImage) {
          setSelectedImageId(nextImage.id);
        }
      }
    }

    document.addEventListener(
      "keydown",
      handleKeyDown,
    );

    const previousOverflow =
      document.body.style.overflow;

    document.body.style.overflow = "hidden";

    return () => {
      document.removeEventListener(
        "keydown",
        handleKeyDown,
      );

      document.body.style.overflow =
        previousOverflow;
    };
  }, [isViewerOpen, selectedIndex, images]);

  return (
    <>
      <header className="heritage-glass overflow-hidden rounded-[var(--radius-card)]">
        <div className="grid lg:grid-cols-[0.72fr_1.28fr]">
          <div className="flex flex-col items-center justify-center p-5 md:p-7 lg:p-8">
            {selectedImage ? (
              <>
                <button
                  type="button"
                  onClick={openViewer}
                  aria-label={`Open ${site.name} image in fullscreen viewer`}
                  className="group relative aspect-[4/3] w-full max-w-[420px] overflow-hidden rounded-2xl border border-[var(--heritage-gold-dark)]/50 bg-black/20 text-left shadow-[0_0_35px_rgba(212,175,55,0.12)] focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--heritage-gold)] focus-visible:ring-offset-2 focus-visible:ring-offset-[var(--heritage-black)]"
                >
                  <Image
                    src={selectedImage.url}
                    alt={
                      selectedImage.alt_text ??
                      selectedImage.title ??
                      site.name
                    }
                    fill
                    priority
                    sizes="(max-width: 1024px) 90vw, 35vw"
                    className="object-cover transition-transform duration-700 group-hover:scale-[1.025]"
                  />

                  <div className="pointer-events-none absolute inset-0 rounded-2xl ring-1 ring-inset ring-white/10" />

                  <div className="pointer-events-none absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-black/45 to-transparent" />

                  <span className="absolute bottom-4 right-4 rounded-full border border-white/15 bg-black/45 px-3 py-1.5 text-[10px] font-medium tracking-wide text-white/80 backdrop-blur-md opacity-0 transition-opacity duration-300 group-hover:opacity-100">
                    Open fullscreen
                  </span>
                </button>

                {images.length > 1 && (
                  <div className="mt-4 w-full max-w-[420px]">
                    <div className="mb-2 flex items-center justify-between">
                      <span className="text-[10px] font-medium uppercase tracking-[0.18em] text-[var(--heritage-muted)]">
                        Gallery
                      </span>

                      <span className="text-[10px] font-medium text-[var(--heritage-gold)]">
                        {selectedIndex + 1} / {images.length}
                      </span>
                    </div>

                    <div
                      className="flex gap-3 overflow-x-auto pb-1"
                      aria-label={`${images.length} heritage images`}
                    >
                      {images.map((image) => {
                        const isSelected =
                          image.id === selectedImage.id;

                        return (
                          <button
                            key={image.id}
                            type="button"
                            onClick={() =>
                              setSelectedImageId(image.id)
                            }
                            aria-label={`View ${image.title ?? site.name} image`}
                            aria-pressed={isSelected}
                            className={[
                              "relative h-16 w-20 shrink-0 overflow-hidden rounded-xl border transition-all duration-300 focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--heritage-gold)] focus-visible:ring-offset-2 focus-visible:ring-offset-[var(--heritage-black)]",
                              isSelected
                                ? "border-[var(--heritage-gold)] opacity-100 shadow-[0_0_18px_rgba(212,175,55,0.16)]"
                                : "border-[var(--glass-border)] opacity-55 hover:border-[var(--glass-border-strong)] hover:opacity-100",
                            ].join(" ")}
                          >
                            <Image
                              src={image.url}
                              alt={
                                image.alt_text ??
                                image.title ??
                                site.name
                              }
                              fill
                              sizes="80px"
                              className="object-cover"
                            />

                            {isSelected && (
                              <span className="pointer-events-none absolute inset-0 rounded-xl ring-1 ring-inset ring-[var(--heritage-gold)]/60" />
                            )}
                          </button>
                        );
                      })}
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div className="flex aspect-[4/3] w-full max-w-[420px] items-center justify-center rounded-2xl border border-[var(--glass-border)] bg-white/[0.025]">
                <div className="text-center">
                  <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full border border-[var(--glass-border)] bg-white/[0.03]">
                    <MapPin className="h-6 w-6 text-[var(--heritage-gold)]" />
                  </div>

                  <p className="mt-4 text-sm text-[var(--heritage-muted)]">
                    Heritage site image unavailable
                  </p>
                </div>
              </div>
            )}
          </div>

          <div className="flex flex-col justify-center border-t border-[var(--glass-border)] p-7 md:p-10 lg:border-l lg:border-t-0 lg:p-12">
            <div className="flex flex-wrap items-center gap-3">
              <span className="rounded-full border border-[var(--glass-border)] bg-white/[0.03] px-3 py-1 text-[11px] font-medium tracking-wide text-[var(--heritage-gold-light)]">
                {site.category}
              </span>

              {site.is_verified && (
                <span className="inline-flex items-center gap-1.5 text-xs font-medium text-[var(--heritage-gold)]">
                  <ShieldCheck className="h-4 w-4" />
                  Verified
                </span>
              )}
            </div>

            <h1 className="mt-5 text-4xl font-black tracking-tight text-[var(--heritage-ivory)] md:text-5xl">
              {site.name}
            </h1>

            {location && (
              <div className="mt-4 flex items-center gap-2 text-sm text-[var(--heritage-muted)]">
                <MapPin className="h-4 w-4 shrink-0 text-[var(--heritage-gold-dark)]" />
                <span>{location}</span>
              </div>
            )}

            {site.short_description && (
              <p className="mt-7 max-w-2xl text-sm leading-7 text-[var(--heritage-muted)] md:text-base md:leading-8">
                {site.short_description}
              </p>
            )}
          </div>
        </div>
      </header>

      {isViewerOpen && selectedImage && (
        <div
          className="fixed inset-0 z-[100] flex items-center justify-center bg-black/90 p-4 backdrop-blur-md md:p-8"
          role="dialog"
          aria-modal="true"
          aria-label={`${site.name} image viewer`}
          onClick={closeViewer}
        >
          <button
            type="button"
            onClick={closeViewer}
            aria-label="Close image viewer"
            className="absolute right-5 top-5 z-20 flex h-10 w-10 items-center justify-center rounded-full border border-white/15 bg-white/[0.06] text-white/80 backdrop-blur-md transition-colors hover:bg-white/[0.12] hover:text-white focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--heritage-gold)]"
          >
            <X className="h-5 w-5" />
          </button>

          {images.length > 1 && (
            <>
              <button
                type="button"
                onClick={(event) => {
                  event.stopPropagation();
                  showPreviousImage();
                }}
                aria-label="Previous image"
                className="absolute left-4 top-1/2 z-20 flex h-11 w-11 -translate-y-1/2 items-center justify-center rounded-full border border-white/15 bg-white/[0.06] text-white/80 backdrop-blur-md transition-colors hover:bg-white/[0.12] hover:text-white focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--heritage-gold)] md:left-8"
              >
                <ChevronLeft className="h-5 w-5" />
              </button>

              <button
                type="button"
                onClick={(event) => {
                  event.stopPropagation();
                  showNextImage();
                }}
                aria-label="Next image"
                className="absolute right-4 top-1/2 z-20 flex h-11 w-11 -translate-y-1/2 items-center justify-center rounded-full border border-white/15 bg-white/[0.06] text-white/80 backdrop-blur-md transition-colors hover:bg-white/[0.12] hover:text-white focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--heritage-gold)] md:right-8"
              >
                <ChevronRight className="h-5 w-5" />
              </button>
            </>
          )}

          <div
            className="relative h-full max-h-[88vh] w-full max-w-6xl"
            onClick={(event) => event.stopPropagation()}
          >
            <Image
              src={selectedImage.url}
              alt={
                selectedImage.alt_text ??
                selectedImage.title ??
                site.name
              }
              fill
              sizes="95vw"
              className="object-contain"
            />

            <div className="absolute bottom-3 left-1/2 -translate-x-1/2 rounded-full border border-white/10 bg-black/50 px-4 py-2 text-[10px] font-medium tracking-wide text-white/75 backdrop-blur-md">
              {site.name}
              {images.length > 1 &&
                ` ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â· ${selectedIndex + 1} / ${images.length}`}
            </div>
          </div>
        </div>
      )}
    </>
  );
}