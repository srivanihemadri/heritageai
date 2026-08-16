import {
  BookOpen,
  ExternalLink,
  FileText,
  Landmark,
  Library,
  ScrollText,
  ShieldCheck,
} from "lucide-react";

import type { HeritageSiteSource } from "@/services/heritage";

interface HeritageSourcesProps {
  sources: HeritageSiteSource[];
}

function getSourceIcon(sourceType: HeritageSiteSource["source_type"]) {
  switch (sourceType) {
    case "UNESCO":
      return Landmark;
    case "BOOK":
      return BookOpen;
    case "ACADEMIC":
      return ScrollText;
    case "MUSEUM":
    case "ARCHIVE":
      return Library;
    case "GOVERNMENT":
      return ShieldCheck;
    default:
      return FileText;
  }
}

function getSourceTypeLabel(
  sourceType: HeritageSiteSource["source_type"],
): string {
  return sourceType.charAt(0) + sourceType.slice(1).toLowerCase();
}

function formatPublicationDate(
  publicationDate: string | null,
): string | null {
  if (!publicationDate) {
    return null;
  }

  const parsed = new Date(publicationDate);

  if (Number.isNaN(parsed.getTime())) {
    return publicationDate;
  }

  return new Intl.DateTimeFormat("en", {
    year: "numeric",
    month: "short",
    day: "numeric",
  }).format(parsed);
}

export default function HeritageSources({
  sources,
}: HeritageSourcesProps) {
  if (sources.length === 0) {
    return null;
  }

  return (
    <section className="heritage-glass mt-6 rounded-[var(--radius-card)] p-8 md:p-10">
      <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div>
          <p className="text-[10px] font-medium uppercase tracking-[0.2em] text-[var(--heritage-gold)]">
            Sources &amp; Provenance
          </p>

          <h2 className="mt-2 text-2xl font-semibold tracking-tight text-[var(--heritage-ivory)]">
            Research sources
          </h2>

          <p className="mt-3 max-w-3xl text-sm leading-7 text-[var(--heritage-muted)] md:text-base">
            Reference material used to support the historical information
            presented for this heritage site.
          </p>
        </div>

        <div className="text-sm text-[var(--heritage-muted)]">
          {sources.length} {sources.length === 1 ? "source" : "sources"}
        </div>
      </div>

      <div className="mt-8 space-y-4">
        {sources.map((source) => {
          const Icon = getSourceIcon(source.source_type);
          const publicationDate = formatPublicationDate(
            source.publication_date,
          );

          const metadata = [
            source.author,
            source.organization,
            source.publisher,
          ].filter(Boolean);

          return (
            <article
              key={source.id}
              className="rounded-2xl border border-white/10 bg-white/[0.025] p-5 transition-colors duration-300 hover:bg-white/[0.04] md:p-6"
            >
              <div className="flex gap-4">
                <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-[var(--heritage-gold)]/20 bg-[var(--heritage-gold)]/[0.06] text-[var(--heritage-gold)]">
                  <Icon className="h-5 w-5" aria-hidden="true" />
                </div>

                <div className="min-w-0 flex-1">
                  <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                    <div>
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="rounded-full border border-white/10 px-2.5 py-1 text-[10px] font-medium uppercase tracking-[0.14em] text-[var(--heritage-muted)]">
                          {getSourceTypeLabel(source.source_type)}
                        </span>

                        {source.is_verified && (
                          <span className="inline-flex items-center gap-1 rounded-full border border-emerald-400/20 bg-emerald-400/[0.06] px-2.5 py-1 text-[10px] font-medium uppercase tracking-[0.14em] text-emerald-300">
                            <ShieldCheck
                              className="h-3 w-3"
                              aria-hidden="true"
                            />
                            Verified
                          </span>
                        )}
                      </div>

                      <h3 className="mt-3 text-base font-semibold text-[var(--heritage-ivory)] md:text-lg">
                        {source.title}
                      </h3>
                    </div>

                    {source.url && (
                      <a
                        href={source.url}
                        target="_blank"
                        rel="noreferrer noopener"
                        className="inline-flex shrink-0 items-center gap-2 text-sm font-medium text-[var(--heritage-gold-light)] transition-colors duration-300 hover:text-[var(--heritage-gold)]"
                      >
                        Open source
                        <ExternalLink
                          className="h-4 w-4"
                          aria-hidden="true"
                        />
                      </a>
                    )}
                  </div>

                  {metadata.length > 0 && (
                    <p className="mt-3 text-sm leading-6 text-[var(--heritage-muted)]">
                      {metadata.join(" • ")}
                    </p>
                  )}

                  {publicationDate && (
                    <p className="mt-2 text-xs uppercase tracking-[0.14em] text-[var(--heritage-muted)]/80">
                      Published {publicationDate}
                    </p>
                  )}

                  {source.citation_text && (
                    <p className="mt-4 rounded-xl border border-white/5 bg-black/10 p-4 text-sm leading-7 text-[var(--heritage-muted)]">
                      {source.citation_text}
                    </p>
                  )}
                </div>
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}
