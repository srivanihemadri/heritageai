import Link from "next/link";
import { ArrowUpRight } from "lucide-react";

const footerLinks = [
  { label: "Home", href: "/" },
  { label: "Explorer", href: "/explorer" },
  { label: "AI Chat", href: "/chat" },
  { label: "About", href: "/about" },
];

export default function Footer() {
  return (
    <footer className="border-t border-[var(--glass-border)]">
      <div className="mx-auto max-w-7xl px-6 py-16 md:px-8">
        <div className="grid gap-10 md:grid-cols-[1.3fr_1fr_1fr]">
          <div>
            <Link
              href="/"
              className="text-xl font-semibold tracking-tight text-[var(--heritage-ivory)]"
            >
              Heritage
              <span className="text-[var(--heritage-gold)]">AI</span>
            </Link>

            <p className="mt-4 max-w-md text-sm leading-7 text-[var(--heritage-muted)]">
              An AI-powered heritage experience designed to help people
              discover, understand and preserve cultural history.
            </p>
          </div>

          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[var(--heritage-gold-light)]">
              Explore
            </p>

            <div className="mt-4 flex flex-col gap-3">
              {footerLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className="w-fit text-sm text-[var(--heritage-muted)] transition-colors hover:text-[var(--heritage-ivory)]"
                >
                  {link.label}
                </Link>
              ))}
            </div>
          </div>

          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[var(--heritage-gold-light)]">
              HeritageAI
            </p>

            <div className="mt-4 flex flex-col gap-3">
              <a
                href="#how-it-works"
                className="group flex w-fit items-center gap-1 text-sm text-[var(--heritage-muted)] transition-colors hover:text-[var(--heritage-ivory)]"
              >
                How It Works
                <ArrowUpRight className="h-3.5 w-3.5 transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5" />
              </a>

              <a
                href="#heritage"
                className="text-sm text-[var(--heritage-muted)] transition-colors hover:text-[var(--heritage-ivory)]"
              >
                World Heritage
              </a>

              <a
                href="#ai"
                className="text-sm text-[var(--heritage-muted)] transition-colors hover:text-[var(--heritage-ivory)]"
              >
                AI Intelligence
              </a>

              <a
                href="#faq"
                className="text-sm text-[var(--heritage-muted)] transition-colors hover:text-[var(--heritage-ivory)]"
              >
                FAQ
              </a>
            </div>
          </div>
        </div>

        <div className="mt-12 flex flex-col gap-3 border-t border-[var(--glass-border)] pt-6 text-xs text-[var(--heritage-muted)] sm:flex-row sm:items-center sm:justify-between">
          <p>
            © {new Date().getFullYear()} HeritageAI. Built for cultural
            preservation.
          </p>

          <p className="text-[var(--heritage-bronze)]">
            Discover · Understand · Preserve
          </p>
        </div>
      </div>
    </footer>
  );
}