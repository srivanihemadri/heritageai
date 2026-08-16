import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import Logo from "../ui/logo/Logo";

const footerLinks = [
  { label: "Home", href: "/" },
  { label: "Explorer", href: "/explorer" },
  { label: "AI Chat", href: "/chat" },
  { label: "About", href: "/about" },
];

export default function Footer() {
  return (
    <footer className="relative mt-12 overflow-hidden border-t border-[var(--glass-border)]">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,rgba(212,175,90,0.07),transparent_40%)]" />

      <div className="heritage-container relative py-16 sm:py-20">
        <div className="grid gap-12 lg:grid-cols-[1.4fr_0.8fr_0.8fr]">
          <div>
            <Logo />

            <p className="mt-5 max-w-md text-sm leading-7 text-[var(--heritage-muted)]">
              An AI-powered heritage experience designed to help people
              discover, understand and preserve cultural history.
            </p>

            <div className="heritage-badge mt-6">
              <span className="h-1.5 w-1.5 rounded-full bg-[var(--heritage-gold)] shadow-[0_0_10px_rgba(212,175,90,0.7)]" />
              Cultural intelligence platform
            </div>
          </div>

          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[var(--heritage-gold-light)]">
              Explore
            </p>

            <div className="mt-5 flex flex-col gap-3">
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
              Intelligence
            </p>

            <div className="mt-5 flex flex-col gap-3">
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

        <div className="heritage-divider mt-12" />

        <div className="mt-6 flex flex-col gap-3 text-xs text-[var(--heritage-muted)] sm:flex-row sm:items-center sm:justify-between">
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
