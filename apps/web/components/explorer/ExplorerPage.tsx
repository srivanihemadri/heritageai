"use client";

import {
  Check,
  ChevronDown,
  Search,
} from "lucide-react";
import { useEffect, useState } from "react";

import {
  getHeritageSiteMedia,
  getHeritageSites,
  type HeritageSite,
  type HeritageSiteMedia,
} from "@/services/heritage";

import HeritageCard from "./HeritageCard";

function getPaginationItems(
  totalPages: number,
  currentPage: number,
): Array<number | "ellipsis"> {
  if (totalPages <= 5) {
    return Array.from(
      { length: totalPages },
      (_, index) => index + 1,
    );
  }

  const pages = new Set<number>([
    1,
    totalPages,
    currentPage,
    Math.max(2, currentPage - 1),
    Math.min(totalPages - 1, currentPage + 1),
  ]);

  const sortedPages = Array.from(pages).sort(
    (a, b) => a - b,
  );

  const items: Array<number | "ellipsis"> = [];

  for (const page of sortedPages) {
    const previousPage = items
      .filter(
        (item): item is number =>
          typeof item === "number",
      )
      .at(-1);

    if (
      previousPage !== undefined &&
      page - previousPage > 1
    ) {
      items.push("ellipsis");
    }

    items.push(page);
  }

  return items;
}

export default function ExplorerPage() {
  const [sites, setSites] = useState<HeritageSite[]>([]);
  const [mediaBySiteId, setMediaBySiteId] = useState<Record<string, HeritageSiteMedia | null>>({});
  const [searchTerm, setSearchTerm] = useState("");
  const [debouncedSearchTerm, setDebouncedSearchTerm] = useState("");
  const [category, setCategory] = useState("");
  const [categoryOpen, setCategoryOpen] = useState(false);
  const [country, setCountry] = useState("");
  const [countryOpen, setCountryOpen] = useState(false);
const [currentPage, setCurrentPage] = useState(1);
const [totalPages, setTotalPages] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const dataTotalLabel =
    sites.length === 1
      ? "1 heritage site found"
      : `${sites.length} heritage sites found`;



  useEffect(() => {
    const timer = window.setTimeout(() => {
      setDebouncedSearchTerm(searchTerm);
    }, 400);

    return () => {
      window.clearTimeout(timer);
    };
  }, [searchTerm]);

  useEffect(() => {
    let cancelled = false;

    async function loadSites() {
      try {
        setIsLoading(true);
        setError(null);

        const data = await getHeritageSites({
          search: debouncedSearchTerm.trim() || undefined,
          category: category || undefined,
          country: country || undefined,
          page: currentPage,
          page_size: 12,
        });

        if (!cancelled) {
          setSites(data.sites);

        const mediaEntries = await Promise.all(
          data.sites.map(async (site) => {
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

        setMediaBySiteId(Object.fromEntries(mediaEntries));
      setTotalPages(data.total_pages);
        }
      } catch (err) {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : "Unable to load heritage sites.",
          );
        }
      } finally {
        if (!cancelled) {
          setIsLoading(false);
        }
      }
    }

    void loadSites();

    return () => {
      cancelled = true;
    };
  }, [debouncedSearchTerm, category, country, currentPage]);

  return (
    <main className="min-h-screen bg-[var(--heritage-background)] px-6 py-24 sm:px-8 xl:px-10">
      <div className="mx-auto max-w-[1440px]">
        <header>
          <p className="text-sm font-medium uppercase tracking-[0.2em] text-[var(--heritage-gold)]">
            Heritage Explorer
          </p>

          <h1 className="mt-4 text-4xl font-black tracking-tight text-[var(--heritage-ivory)] md:text-6xl">
            Explore the world&apos;s heritage
          </h1>

          <p className="mt-5 max-w-3xl text-base leading-8 text-[var(--heritage-muted)] md:text-lg">
            Discover monuments, temples, archaeological sites, forts,
            and historic places through the HeritageAI knowledge platform.
          </p>
        </header>

        <div className="mt-10 flex flex-col gap-4 lg:flex-row lg:items-start">
          <div className="w-full flex-1">
            <label
              htmlFor="heritage-search"
              className="sr-only"
            >
              Search heritage sites
            </label>

            <div className="heritage-glass flex min-h-[58px] items-center gap-3 rounded-[var(--radius-card)] px-5 py-4">
              <Search
                className="h-5 w-5 shrink-0 text-[var(--heritage-gold)]"
                aria-hidden="true"
              />

              <input
                id="heritage-search"
                type="search"
                value={searchTerm}
                onChange={(event) => { setSearchTerm(event.target.value); setCurrentPage(1); }}
                placeholder="Search heritage sites..."
                className="w-full bg-transparent text-sm text-[var(--heritage-ivory)] outline-none placeholder:text-[var(--heritage-muted)]"
              />

                {searchTerm && (
                  <button
                    type="button"
                    onClick={() => {
                      setSearchTerm("");
                      setCurrentPage(1);
                    }}
                    aria-label="Clear search"
                    className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-lg leading-none text-[var(--heritage-muted)] transition-colors duration-200 hover:bg-white/[0.05] hover:text-[var(--heritage-ivory)]"
                  >
                    ×
                  </button>
                )}
            </div>
          </div>

          <div className="relative w-full lg:w-56">
            <label
              id="heritage-category-label"
              className="sr-only"
            >
              Filter by category
            </label>

            <button
              type="button"
              aria-haspopup="listbox"
              aria-expanded={categoryOpen}
              aria-labelledby="heritage-category-label"
              onClick={() => setCategoryOpen((open) => !open)}
                className={`heritage-glass flex min-h-[58px] w-full items-center justify-between gap-4 rounded-[var(--radius-card)] px-5 py-4 text-left text-sm outline-none transition-all duration-300 hover:border-[var(--glass-border-strong)] focus:border-[var(--heritage-gold-dark)] ${category ? "border-[var(--heritage-gold-dark)] bg-[var(--heritage-gold)]/[0.06] text-[var(--heritage-gold-light)]" : "text-[var(--heritage-ivory)]"}`}
            >
              <span>
                {category || "All categories"}
              </span>

              <ChevronDown
                className={`h-4 w-4 shrink-0 text-[var(--heritage-gold)] transition-transform duration-300 ${
                  categoryOpen ? "rotate-180" : ""
                }`}
                aria-hidden="true"
              />
            </button>

            {categoryOpen && (
              <div
                role="listbox"
                aria-label="Heritage category"
                className="absolute left-0 right-0 top-full z-50 mt-2 overflow-hidden rounded-[var(--radius-card)] border border-[var(--glass-border-strong)] bg-[rgba(18,16,12,0.96)] p-2 shadow-2xl backdrop-blur-xl"
              >
                {[
                  "Temple",
                  "Fort",
                  "Archaeological Site",
                  "Monument",
                  "Historic Site",
                ].map((option) => (
                  <button
                    key={option}
                    type="button"
                    role="option"
                    aria-selected={category === option}
                    onClick={() => {
                      setCategory(option); setCurrentPage(1);
                      setCategoryOpen(false);
                    }}
                    className="flex w-full items-center justify-between rounded-xl px-4 py-3 text-left text-sm text-[var(--heritage-muted)] transition-all duration-200 hover:bg-white/[0.05] hover:text-[var(--heritage-ivory)]"
                  >
                    <span>{option}</span>

                    {category === option && (
                      <Check
                        className="h-4 w-4 text-[var(--heritage-gold)]"
                        aria-hidden="true"
                      />
                    )}
                  </button>
                ))}

                <div className="my-1 border-t border-[var(--glass-border)]" />

                <button
                  type="button"
                  role="option"
                  aria-selected={category === ""}
                  onClick={() => {
                    setCategory(""); setCurrentPage(1);
                    setCategoryOpen(false);
                  }}
                  className="flex w-full items-center justify-between rounded-xl px-4 py-3 text-left text-sm text-[var(--heritage-muted)] transition-all duration-200 hover:bg-white/[0.05] hover:text-[var(--heritage-ivory)]"
                >
                  <span>All categories</span>

                  {category === "" && (
                    <Check
                      className="h-4 w-4 text-[var(--heritage-gold)]"
                      aria-hidden="true"
                    />
                  )}
                </button>
              </div>
            )}
          </div>

          <div className="relative w-full lg:w-56">
            <label
              id="heritage-country-label"
              className="sr-only"
            >
              Filter by country
            </label>

            <button
              type="button"
              aria-haspopup="listbox"
              aria-expanded={countryOpen}
              aria-labelledby="heritage-country-label"
              onClick={() => setCountryOpen((open) => !open)}
                className={`heritage-glass flex min-h-[58px] w-full items-center justify-between gap-4 rounded-[var(--radius-card)] px-5 py-4 text-left text-sm outline-none transition-all duration-300 hover:border-[var(--glass-border-strong)] focus:border-[var(--heritage-gold-dark)] ${country ? "border-[var(--heritage-gold-dark)] bg-[var(--heritage-gold)]/[0.06] text-[var(--heritage-gold-light)]" : "text-[var(--heritage-ivory)]"}`}
            >
              <span>
                {country || "All countries"}
              </span>

              <ChevronDown
                className={`h-4 w-4 shrink-0 text-[var(--heritage-gold)] transition-transform duration-300 ${
                  countryOpen ? "rotate-180" : ""
                }`}
                aria-hidden="true"
              />
            </button>

            {countryOpen && (
              <div
                role="listbox"
                aria-label="Heritage country"
                className="absolute left-0 right-0 top-full z-50 mt-2 overflow-hidden rounded-[var(--radius-card)] border border-[var(--glass-border-strong)] bg-[rgba(18,16,12,0.96)] p-2 shadow-2xl backdrop-blur-xl"
              >
                {[
                  "India",
                  "Cambodia",
                  "Jordan",
                  "Greece",
                ].map((option) => (
                  <button
                    key={option}
                    type="button"
                    role="option"
                    aria-selected={country === option}
                    onClick={() => {
                      setCountry(option); setCurrentPage(1);
                      setCountryOpen(false);
                    }}
                    className="flex w-full items-center justify-between rounded-xl px-4 py-3 text-left text-sm text-[var(--heritage-muted)] transition-all duration-200 hover:bg-white/[0.05] hover:text-[var(--heritage-ivory)]"
                  >
                    <span>{option}</span>

                    {country === option && (
                      <Check
                        className="h-4 w-4 text-[var(--heritage-gold)]"
                        aria-hidden="true"
                      />
                    )}
                  </button>
                ))}

                <div className="my-1 border-t border-[var(--glass-border)]" />

                <button
                  type="button"
                  role="option"
                  aria-selected={country === ""}
                  onClick={() => {
                    setCountry(""); setCurrentPage(1);
                    setCountryOpen(false);
                  }}
                  className="flex w-full items-center justify-between rounded-xl px-4 py-3 text-left text-sm text-[var(--heritage-muted)] transition-all duration-200 hover:bg-white/[0.05] hover:text-[var(--heritage-ivory)]"
                >
                  <span>All countries</span>

                  {country === "" && (
                    <Check
                      className="h-4 w-4 text-[var(--heritage-gold)]"
                      aria-hidden="true"
                    />
                  )}
                </button>
              </div>
            )}
          </div>
        </div>

            {(searchTerm || category || country) && (
              <button
                type="button"
                onClick={() => {
                  setSearchTerm("");
                  setCategory("");
                  setCountry("");
                  setCurrentPage(1);
                  setCategoryOpen(false);
                  setCountryOpen(false);
                }}
                className="heritage-glass min-h-[58px] shrink-0 rounded-[var(--radius-card)] px-5 py-4 text-sm font-medium text-[var(--heritage-gold-light)] transition-all duration-300 hover:border-[var(--glass-border-strong)] hover:text-[var(--heritage-ivory)] focus:border-[var(--heritage-gold-dark)] focus:outline-none"
                aria-label="Clear active heritage filters"
              >
                Clear filters
              </button>
            )}

        <section className="mt-12">

      {isLoading && (
        <div
          className="grid items-stretch gap-6 sm:grid-cols-2 lg:grid-cols-3"
          aria-busy="true"
          aria-label="Loading heritage sites"
        >
          {Array.from({ length: 6 }).map((_, index) => (
            <div
              key={index}
              className="heritage-glass flex h-full flex-col overflow-hidden rounded-[var(--radius-card)]"
            >
              <div className="relative aspect-[16/10] shrink-0 overflow-hidden border-b border-[var(--glass-border)] bg-black/20">
                <div className="absolute inset-0 animate-pulse bg-white/[0.04]" />
              </div>

              <div className="flex flex-1 flex-col p-6">
                <div className="flex items-start justify-between gap-4">
                  <div className="h-6 w-20 animate-pulse rounded-full bg-white/[0.06]" />
                  <div className="h-4 w-14 animate-pulse rounded bg-white/[0.06]" />
                </div>

                <div className="mt-6 h-6 w-3/4 animate-pulse rounded bg-white/[0.06]" />

                <div className="mt-3 h-4 w-2/3 animate-pulse rounded bg-white/[0.06]" />

                <div className="mt-6 space-y-3">
                  <div className="h-4 w-full animate-pulse rounded bg-white/[0.06]" />
                  <div className="h-4 w-5/6 animate-pulse rounded bg-white/[0.06]" />
                  <div className="h-4 w-2/3 animate-pulse rounded bg-white/[0.06]" />
                </div>

                <div className="mt-auto border-t border-[var(--glass-border)] pt-5">
                  <div className="h-4 w-1/2 animate-pulse rounded bg-white/[0.06]" />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

          {!isLoading && error && (
            <div className="heritage-glass rounded-[var(--radius-card)] border-red-400/20 p-8">
              <p className="font-medium text-red-300">
                Unable to load heritage sites.
              </p>

              <p className="mt-2 text-sm text-[var(--heritage-muted)]">
                {error}
              </p>
            </div>
          )}

          {!isLoading && !error && sites.length === 0 && (
            <div className="heritage-glass rounded-[var(--radius-card)] p-8 text-[var(--heritage-muted)]">
              No heritage sites are currently available.
            </div>
          )}

            <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="text-base font-semibold tracking-tight text-[var(--heritage-ivory)]">
                  {dataTotalLabel}
                </p>
                <p className="mt-1 text-xs leading-6 text-[var(--heritage-muted)]">
                  Heritage sites matching your current exploration criteria
                </p>
              </div>

              {(searchTerm || category || country) && (
                <div className="flex flex-wrap items-center gap-2">
                  {searchTerm && (
                    <span className="rounded-full border border-[var(--glass-border)] bg-white/[0.025] px-3 py-1.5 text-xs text-[var(--heritage-muted)]">
                      Search: <span className="text-[var(--heritage-ivory)]">{searchTerm}</span>
                    </span>
                  )}

                  {category && (
                    <span className="rounded-full border border-[var(--heritage-gold-dark)]/40 bg-[var(--heritage-gold)]/[0.06] px-3 py-1.5 text-xs text-[var(--heritage-gold-light)]">
                      Category: {category}
                    </span>
                  )}

                  {country && (
                    <span className="rounded-full border border-[var(--heritage-gold-dark)]/40 bg-[var(--heritage-gold)]/[0.06] px-3 py-1.5 text-xs text-[var(--heritage-gold-light)]">
                      Country: {country}
                    </span>
                  )}
                </div>
              )}
            </div>


          {!isLoading && !error && sites.length > 0 && (

            <div className="grid items-stretch gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {sites.map((site) => (
                <HeritageCard
                    key={site.id}
                    site={site}
                    primaryImage={mediaBySiteId[site.id] ?? null}
                  />
              ))}
            </div>
          )}
      {!isLoading && !error && totalPages > 1 && (
        <nav
          className="mt-10 flex flex-col items-center justify-center gap-3 sm:flex-row sm:flex-wrap"
          aria-label="Heritage site pagination"
        >
          <button
            type="button"
            disabled={currentPage === 1}
            onClick={() =>
              setCurrentPage((page) => Math.max(1, page - 1))
            }
            aria-label="Go to previous page"
            className="heritage-glass min-w-24 rounded-xl px-4 py-2 text-sm text-[var(--heritage-muted)] transition-all duration-300 hover:border-[var(--glass-border-strong)] hover:text-[var(--heritage-ivory)] disabled:cursor-not-allowed disabled:opacity-40"
          >
            Previous
          </button>

          <div className="flex max-w-full items-center gap-1.5 overflow-x-auto px-1 py-1 sm:gap-2" aria-label="Page numbers">
            {getPaginationItems(totalPages, currentPage).map((item, index) =>
              item === "ellipsis" ? (
                <span
                  key={`ellipsis-${index}`}
                  aria-hidden="true"
                  className="px-1 text-sm text-[var(--heritage-muted)]"
                >
                  …
                </span>
              ) : (
                <button
                  key={item}
                  type="button"
                  aria-current={currentPage === item ? "page" : undefined}
                  aria-label={`Go to page ${item}`}
                  onClick={() => setCurrentPage(item)}
                  className={`h-10 min-w-10 rounded-xl px-3 text-sm transition-all duration-300 ${
                    currentPage === item
                      ? "border border-[var(--heritage-gold-dark)] bg-[var(--heritage-gold-dark)]/20 text-[var(--heritage-gold-light)]"
                      : "heritage-glass text-[var(--heritage-muted)] hover:border-[var(--glass-border-strong)] hover:text-[var(--heritage-ivory)]"
                  }`}
                >
                  {item}
                </button>
              ),
            )}
          </div>

          <button
            type="button"
            disabled={currentPage === totalPages}
            onClick={() =>
              setCurrentPage((page) => Math.min(totalPages, page + 1))
            }
            aria-label="Go to next page"
            className="heritage-glass min-w-24 rounded-xl px-4 py-2 text-sm text-[var(--heritage-muted)] transition-all duration-300 hover:border-[var(--glass-border-strong)] hover:text-[var(--heritage-ivory)] disabled:cursor-not-allowed disabled:opacity-40"
          >
            Next
          </button>
        </nav>
      )}
        </section>
      </div>
    </main>
  );
}
