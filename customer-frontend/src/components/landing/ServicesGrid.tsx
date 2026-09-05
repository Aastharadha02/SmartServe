import { FC } from 'react';
import { Link } from 'react-router-dom';
import { ScrollReveal } from './ScrollReveal';

/** Abstract organic SVG accents — leaf-curve and water-arc shapes.
 *  Explicitly NOT service icons — purely decorative form language. */
const LeafCurve: FC<{ color?: string }> = ({ color = 'var(--lp-sage)' }) => (
  <svg
    width="56"
    height="56"
    viewBox="0 0 56 56"
    fill="none"
    aria-hidden="true"
  >
    <path
      d="M8 48 C8 48 10 14 28 8 C46 2 52 24 44 36 C36 48 8 48 8 48Z"
      fill={color}
      opacity="0.18"
    />
    <path
      d="M10 46 C12 32 22 16 34 12"
      stroke={color}
      strokeWidth="2"
      strokeLinecap="round"
    />
  </svg>
);

const WaterArc: FC<{ color?: string }> = ({ color = 'var(--lp-sage)' }) => (
  <svg
    width="56"
    height="56"
    viewBox="0 0 56 56"
    fill="none"
    aria-hidden="true"
  >
    <path
      d="M8 40 Q28 4 48 40"
      stroke={color}
      strokeWidth="2"
      strokeLinecap="round"
      fill="none"
    />
    <circle cx="28" cy="22" r="6" fill={color} opacity="0.15" />
  </svg>
);

const FlowLine: FC<{ color?: string }> = ({ color = 'var(--lp-sage)' }) => (
  <svg
    width="56"
    height="56"
    viewBox="0 0 56 56"
    fill="none"
    aria-hidden="true"
  >
    <path
      d="M6 28 C14 10 28 10 28 28 C28 46 42 46 50 28"
      stroke={color}
      strokeWidth="2"
      strokeLinecap="round"
      fill="none"
    />
    <circle cx="28" cy="28" r="5" fill={color} opacity="0.2" />
  </svg>
);

const PetalArc: FC<{ color?: string }> = ({ color = 'var(--lp-sage)' }) => (
  <svg
    width="56"
    height="56"
    viewBox="0 0 56 56"
    fill="none"
    aria-hidden="true"
  >
    <path
      d="M28 8 C44 8 52 22 44 34 C36 46 16 46 12 34 C8 22 12 8 28 8Z"
      fill={color}
      opacity="0.12"
    />
    <path
      d="M20 38 C20 38 24 20 36 18"
      stroke={color}
      strokeWidth="2"
      strokeLinecap="round"
    />
  </svg>
);

const services = [
  {
    id: 'cleaning',
    name: 'Home Cleaning',
    description:
      'Deep cleans, regular upkeep, and post-event tidying — done with the care your home deserves.',
    accent: <LeafCurve />,
    href: '/explore',
  },
  {
    id: 'plumbing',
    name: 'Plumbing',
    description:
      'Leaks, fixtures, and pipe repairs handled fast by licensed pros who show up on time.',
    accent: <WaterArc />,
    href: '/explore',
  },
  {
    id: 'electrical',
    name: 'Electrical',
    description:
      'Safe, certified work — from a loose socket to a full wiring inspection. No guesswork.',
    accent: <FlowLine />,
    href: '/explore',
  },
  {
    id: 'beauty',
    name: 'Beauty & Wellness',
    description:
      'Salon-quality facials, haircuts, and spa treatments — in the comfort of your own space.',
    accent: <PetalArc />,
    href: '/explore',
  },
];

export const ServicesGrid: FC = () => {
  return (
    <section
      aria-label="Our services"
      className="lp-section"
      style={{ maxWidth: '100%' }}
    >
      <div style={{ maxWidth: 1280, margin: '0 auto' }}>
        {/* Section header */}
        <ScrollReveal>
          <div style={{ marginBottom: 'clamp(2.5rem, 5vw, 4rem)', maxWidth: 560 }}>
            <p
              style={{
                fontFamily: 'var(--lp-font-body)',
                fontWeight: 600,
                fontSize: '0.8rem',
                letterSpacing: '0.12em',
                textTransform: 'uppercase',
                color: 'var(--lp-sage)',
                marginBottom: '0.75rem',
              }}
            >
              What we do
            </p>
            <h2
              className="lp-display"
              style={{
                fontSize: 'clamp(2rem, 4vw, 3.25rem)',
                color: 'var(--lp-ink)',
                marginBottom: '1rem',
              }}
            >
              Every corner of your home, covered.
            </h2>
            <p
              style={{
                fontFamily: 'var(--lp-font-body)',
                fontSize: 'clamp(0.95rem, 1.4vw, 1.075rem)',
                lineHeight: 1.7,
                color: 'rgba(31, 42, 30, 0.65)',
              }}
            >
              Whether it's a surprise leak or a long-overdue refresh — we have
              the right person for the job.
            </p>
          </div>
        </ScrollReveal>

        {/* Grid */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(min(100%, 260px), 1fr))',
            gap: 'clamp(1rem, 2.5vw, 1.5rem)',
          }}
        >
          {services.map((svc, i) => (
            <ScrollReveal key={svc.id} delay={i * 100}>
              <Link
                to={svc.href}
                className="lp-service-card"
                style={{ display: 'block', textDecoration: 'none', color: 'inherit' }}
                data-cursor-interactive
                aria-label={`Learn more about ${svc.name}`}
              >
                {/* Organic accent */}
                <div style={{ marginBottom: '1.25rem' }}>{svc.accent}</div>

                <h3
                  style={{
                    fontFamily: 'var(--lp-font-body)',
                    fontWeight: 700,
                    fontSize: '1.125rem',
                    color: 'var(--lp-forest)',
                    marginBottom: '0.6rem',
                  }}
                >
                  {svc.name}
                </h3>
                <p
                  style={{
                    fontFamily: 'var(--lp-font-body)',
                    fontSize: '0.9rem',
                    lineHeight: 1.65,
                    color: 'rgba(31, 42, 30, 0.65)',
                  }}
                >
                  {svc.description}
                </p>

                {/* CTA arrow */}
                <div
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '0.35rem',
                    marginTop: '1.25rem',
                    fontFamily: 'var(--lp-font-body)',
                    fontWeight: 600,
                    fontSize: '0.85rem',
                    color: 'var(--lp-sage)',
                  }}
                >
                  Explore{' '}
                  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <path
                      d="M2 7h10M8 3l4 4-4 4"
                      stroke="currentColor"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </div>
              </Link>
            </ScrollReveal>
          ))}
        </div>
      </div>
    </section>
  );
};
