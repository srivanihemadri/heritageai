"use client";

import HeroBackground from "./HeroBackground";
import HeroBadge from "./HeroBadge";
import HeroButtons from "./HeroButtons";
import HeroContent from "./HeroContent";
import HeroFeatureCards from "./HeroFeatureCards";
import HeroGlobe from "./HeroGlobe";
import HeroStats from "./HeroStats";

export default function Hero() {
  return (
    <section className="relative overflow-hidden bg-black">
      <HeroBackground />

      <div className="relative mx-auto flex min-h-screen max-w-7xl flex-col items-center px-6 py-24">

        <HeroBadge />

        <div className="mt-10">
          <HeroContent />
        </div>

        <HeroButtons />

        <HeroStats />

        <HeroGlobe />

        <HeroFeatureCards />

      </div>
    </section>
  );
}