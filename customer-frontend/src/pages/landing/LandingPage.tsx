import { FC, useEffect, useRef, useState } from 'react';
import Lenis from 'lenis';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { LandingNav } from '../../components/landing/LandingNav';
import { HeroSection } from '../../components/landing/HeroSection';
import { TrustStrip } from '../../components/landing/TrustStrip';
import { ServicesGrid } from '../../components/landing/ServicesGrid';
import { ProcessSteps } from '../../components/landing/ProcessSteps';
import { TestimonialSection } from '../../components/landing/TestimonialSection';
import { ClosingCTA } from '../../components/landing/ClosingCTA';
import { CustomCursor } from '../../components/landing/CustomCursor';

gsap.registerPlugin(ScrollTrigger);

export const LandingPage: FC = () => {
  const [navScrolled, setNavScrolled] = useState(false);
  const lenisRef = useRef<Lenis | null>(null);

  useEffect(() => {
    // ── Lenis smooth scroll ────────────────────────────────
    const lenis = new Lenis({
      lerp: 0.08,
      smoothWheel: true,
    });
    lenisRef.current = lenis;

    // Sync Lenis → GSAP ScrollTrigger
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((time) => lenis.raf(time * 1000));
    gsap.ticker.lagSmoothing(0);

    // ── Nav scroll state ───────────────────────────────────
    const onScroll = ({ scroll }: { scroll: number }) => {
      setNavScrolled(scroll > 48);
    };
    lenis.on('scroll', onScroll);

    // ── Reduced motion: kill Lenis smoothing ──────────────
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (mq.matches) {
      lenis.destroy();
    }

    return () => {
      lenis.destroy();
      gsap.ticker.remove((time) => lenis.raf(time * 1000));
      ScrollTrigger.getAll().forEach((t) => t.kill());
    };
  }, []);

  return (
    <div className="landing-page" id="landing-root">
      <CustomCursor />
      <LandingNav scrolled={navScrolled} />

      <main id="main-content">
        {/* 1. Hero — full-viewport */}
        <HeroSection />

        {/* 2. Trust strip */}
        <TrustStrip />

        {/* 3. Services grid */}
        <ServicesGrid />

        {/* 4. Process steps (01/02/03) */}
        <ProcessSteps />

        {/* 5. Testimonials */}
        <TestimonialSection />

        {/* 6. Closing CTA + Footer */}
        <ClosingCTA />
      </main>
    </div>
  );
};

export default LandingPage;
