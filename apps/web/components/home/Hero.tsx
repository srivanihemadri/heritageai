"use client";

import HeroBackground from "./HeroBackground";
import HeroBadge from "./HeroBadge";
import HeroButtons from "./HeroButtons";
import HeroContent from "./HeroContent";
import HeroFeatureCards from "./HeroFeatureCards";
import HeroStats from "./HeroStats";
import LivingHeritage from "./LivingHeritage";

export default function Hero() {
  return (
    <section className="relative overflow-hidden">
      <HeroBackground />

      <div className="relative mx-auto flex min-h-screen max-w-7xl flex-col items-center px-6 pb-24 pt-16 md:px-8 md:pt-20">
        {/* Hero Introduction */}
        <HeroBadge />

        <div className="mt-8 md:mt-10">
          <HeroContent />
        </div>

        <HeroButtons />

        {/* Featured Heritage Experience */}
        <div className="mt-16 w-full md:mt-20">
          <LivingHeritage />
        </div>

        {/* Heritage Statistics */}
        <HeroStats />

        {/* Core Capabilities */}
        <HeroFeatureCards />
      </div>
    </section>
  );
}