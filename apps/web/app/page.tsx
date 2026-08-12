import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";
import Hero from "../components/home/Hero";
import HowItWorks from "../components/sections/HowItWorks";
import UNESCO from "../components/sections/UNESCO";
import AIShowcase from "../components/sections/AIShowcase";
import Stats from "../components/sections/Stats";
import FAQ from "../components/sections/FAQ";

export default function HomePage() {
  return (
    <>
      <Navbar />

      <main>
        <Hero />
        <HowItWorks />
        <UNESCO />
        <AIShowcase />
        <Stats />
        <FAQ />
      </main>

      <Footer />
    </>
  );
}