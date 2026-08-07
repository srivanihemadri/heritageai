"use client";

import Link from "next/link";
import { Menu } from "lucide-react";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-black/70 backdrop-blur-xl">
      <nav className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
        {/* Logo */}
        <Link href="/" className="text-2xl font-bold tracking-tight">
          <span className="text-cyan-400">Heritage</span>AI
        </Link>

        {/* Desktop Navigation */}
        <div className="hidden items-center gap-8 md:flex">
          <Link href="/">Home</Link>
          <Link href="/">Explorer</Link>
          <Link href="/">AI Chat</Link>
          <Link href="/">About</Link>
        </div>

        {/* Right Side */}
        <div className="hidden items-center gap-3 md:flex">
          <button className="rounded-lg border border-white/20 px-4 py-2 transition hover:border-cyan-400">
            Login
          </button>

          <button className="rounded-lg bg-cyan-500 px-5 py-2 font-semibold text-black transition hover:bg-cyan-400">
            Get Started
          </button>
        </div>

        {/* Mobile */}
        <button className="md:hidden">
          <Menu size={28} />
        </button>
      </nav>
    </header>
  );
}