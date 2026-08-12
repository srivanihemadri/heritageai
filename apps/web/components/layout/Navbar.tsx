"use client";

import { useState } from "react";
import Link from "next/link";
import { Menu, X } from "lucide-react";

const navigation = [
  { label: "Home", href: "/" },
  { label: "Explorer", href: "/explorer" },
  { label: "AI Chat", href: "/chat" },
  { label: "About", href: "/about" },
];

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full px-4 pt-4 sm:px-6">
      <nav className="heritage-nav-glass mx-auto flex max-w-7xl items-center justify-between rounded-[24px] px-4 py-3 sm:px-6">
        <Link href="/" onClick={() => setIsOpen(false)} className="shrink-0 text-xl font-semibold tracking-tight text-[var(--heritage-ivory)]">Heritage<span className="text-[var(--heritage-gold)]">AI</span></Link>
        <div className="hidden items-center gap-1 md:flex">
          {navigation.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="rounded-xl px-4 py-2 text-sm font-medium text-[var(--heritage-muted)] transition-colors hover:bg-white/5 hover:text-[var(--heritage-ivory)]">{item.label}</Link>
          ))}
        </div>
        <div className="hidden items-center gap-2 md:flex">
          <Link href="/login" className="rounded-xl border border-[var(--glass-border)] px-4 py-2 text-sm font-medium text-[var(--heritage-ivory)] transition-all hover:border-[var(--glass-border-strong)] hover:bg-white/5">Login</Link>
          <Link href="/login" className="heritage-gold-glow rounded-xl border border-[var(--heritage-gold)]/50 bg-[var(--heritage-gold)] px-5 py-2 text-sm font-semibold text-[var(--heritage-black)] transition-all hover:bg-[var(--heritage-gold-light)]">Get Started</Link>
        </div>
        <button type="button" aria-label={isOpen ? "Close navigation menu" : "Open navigation menu"} aria-expanded={isOpen} onClick={() => setIsOpen((open) => !open)} className="rounded-xl border border-[var(--glass-border)] p-2 text-[var(--heritage-ivory)] transition-colors hover:bg-white/5 md:hidden">{isOpen ? <X size={22} /> : <Menu size={22} />}</button>
      </nav>
      {isOpen && (
        <div className="heritage-glass mx-auto mt-2 max-w-7xl rounded-[24px] p-3 md:hidden">
          <div className="flex flex-col gap-1">
            {navigation.map((item) => (
              <Link key={item.href} href={item.href} onClick={() => setIsOpen(false)} className="rounded-xl px-4 py-3 text-sm font-medium text-[var(--heritage-muted)] transition-colors hover:bg-white/5 hover:text-[var(--heritage-ivory)]">{item.label}</Link>
            ))}
          </div>
          <div className="mt-2 grid grid-cols-2 gap-2 border-t border-[var(--glass-border)] pt-3">
            <Link href="/login" onClick={() => setIsOpen(false)} className="rounded-xl border border-[var(--glass-border)] px-4 py-3 text-center text-sm font-medium text-[var(--heritage-ivory)]">Login</Link>
            <Link href="/login" onClick={() => setIsOpen(false)} className="rounded-xl bg-[var(--heritage-gold)] px-4 py-3 text-center text-sm font-semibold text-[var(--heritage-black)]">Get Started</Link>
          </div>
        </div>
      )}
    </header>
  );
}
