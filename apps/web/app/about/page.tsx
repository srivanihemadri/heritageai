export default function AboutPage() {
  return (
    <main className="min-h-screen bg-[var(--heritage-black)] px-4 py-24 sm:px-6">
      <section className="mx-auto max-w-5xl text-center">
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--heritage-gold)]">
          About HeritageAI
        </p>

        <h1 className="mt-4 text-4xl font-semibold tracking-tight text-[var(--heritage-ivory)] sm:text-6xl">
          Preserving history through intelligence.
        </h1>

        <p className="mx-auto mt-6 max-w-3xl text-base leading-8 text-[var(--heritage-muted)]">
          HeritageAI is an AI-powered cultural heritage platform built to help
          people discover, understand, document and preserve historical places,
          artifacts and stories.
        </p>

        <div className="mt-12 grid gap-5 text-left md:grid-cols-3">
          <div className="heritage-glass rounded-[var(--radius-card)] p-6">
            <h2 className="text-lg font-semibold text-[var(--heritage-ivory)]">
              Discover
            </h2>
            <p className="mt-3 leading-7 text-[var(--heritage-muted)]">
              Explore heritage sites and historically grounded information.
            </p>
          </div>

          <div className="heritage-glass rounded-[var(--radius-card)] p-6">
            <h2 className="text-lg font-semibold text-[var(--heritage-ivory)]">
              Understand
            </h2>
            <p className="mt-3 leading-7 text-[var(--heritage-muted)]">
              Use AI-powered tools to interpret heritage imagery and history.
            </p>
          </div>

          <div className="heritage-glass rounded-[var(--radius-card)] p-6">
            <h2 className="text-lg font-semibold text-[var(--heritage-ivory)]">
              Preserve
            </h2>
            <p className="mt-3 leading-7 text-[var(--heritage-muted)]">
              Support the long-term preservation of cultural heritage.
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}
