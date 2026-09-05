import { FC, ReactNode, useEffect, useRef } from 'react';

interface ScrollRevealProps {
  children: ReactNode;
  delay?: number;      // ms delay, for stagger effects
  className?: string;
  threshold?: number;  // IntersectionObserver threshold 0–1
}

/**
 * ScrollReveal — wraps children in an IntersectionObserver that adds
 * `.is-visible` when the element enters the viewport, triggering the
 * `.lp-reveal` CSS transition (upward fade, 0.65s expo ease).
 *
 * Respects `prefers-reduced-motion`: CSS already handles this by making
 * `.lp-reveal` immediately visible when motion is reduced.
 */
export const ScrollReveal: FC<ScrollRevealProps> = ({
  children,
  delay = 0,
  className = '',
  threshold = 0.15,
}) => {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      (entries) => {
        const entry = entries[0];
        if (!entry) return;
        if (entry.isIntersecting) {
          el.style.transitionDelay = `${delay}ms`;
          el.classList.add('is-visible');
          observer.unobserve(el); // fire once
        }
      },
      { threshold, rootMargin: '0px 0px -40px 0px' }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, [delay, threshold]);

  return (
    <div ref={ref} className={`lp-reveal ${className}`}>
      {children}
    </div>
  );
};
