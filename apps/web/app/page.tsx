import Footer from "../components/layout/Footer";
import Hero from "../components/home/Hero";
import FeaturedHeritageCarousel from "../components/home/FeaturedHeritageCarousel";
import AppDownloadSection from "../components/home/AppDownloadSection";
import HowItWorks from "../components/sections/HowItWorks";
import Stats from "../components/sections/Stats";
import FAQ from "../components/sections/FAQ";

export default function HomePage() {
  return (
    <>

      <main>
        <Hero />
        <FeaturedHeritageCarousel />
        <HowItWorks />
        <Stats />
        <AppDownloadSection />
        <FAQ />
      </main>

      <Footer />
    </>
  );
}