import { FC, useState } from 'react';

/**
 * HeroVisual — Ultra-premium editorial showcase replacing the distorted 3D mesh.
 * Features a serene, sun-drenched home interior visual, layered frosted-glass
 * live status badges, smooth interactive mouse parallax tilt, and warm organic halos.
 */
export const HeroVisual: FC = () => {
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [isHovered, setIsHovered] = useState(false);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width - 0.5;
    const y = (e.clientY - rect.top) / rect.height - 0.5;
    setMousePos({ x, y });
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
    setMousePos({ x: 0, y: 0 });
  };

  return (
    <div
      onMouseMove={handleMouseMove}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={handleMouseLeave}
      style={{
        position: 'relative',
        width: '100%',
        maxWidth: 540,
        margin: '0 auto',
        perspective: 1200,
      }}
      aria-label="SmartServe home care preview"
    >
      {/* Warm Ambient Glow Rings */}
      <div
        aria-hidden="true"
        style={{
          position: 'absolute',
          top: '10%',
          right: '-8%',
          width: '75%',
          height: '75%',
          borderRadius: '50%',
          background: 'radial-gradient(circle, rgba(122, 158, 110, 0.28) 0%, rgba(201, 161, 90, 0.12) 50%, transparent 70%)',
          filter: 'blur(40px)',
          zIndex: 0,
          pointerEvents: 'none',
          transform: `translate(${mousePos.x * 20}px, ${mousePos.y * 20}px)`,
          transition: 'transform 0.4s ease-out',
        }}
      />
      <div
        aria-hidden="true"
        style={{
          position: 'absolute',
          bottom: '-5%',
          left: '-10%',
          width: '65%',
          height: '65%',
          borderRadius: '50%',
          background: 'radial-gradient(circle, rgba(47, 82, 51, 0.15) 0%, rgba(242, 237, 225, 0.6) 60%, transparent 75%)',
          filter: 'blur(35px)',
          zIndex: 0,
          pointerEvents: 'none',
        }}
      />

      {/* Main Architectural Card Container */}
      <div
        style={{
          position: 'relative',
          zIndex: 1,
          borderRadius: 32,
          overflow: 'hidden',
          boxShadow: isHovered
            ? '0 32px 72px -18px rgba(31, 42, 30, 0.22), 0 12px 30px -10px rgba(47, 82, 51, 0.15)'
            : '0 24px 56px -16px rgba(31, 42, 30, 0.16), 0 8px 24px -8px rgba(47, 82, 51, 0.08)',
          border: '1.5px solid rgba(255, 255, 255, 0.85)',
          background: '#F2EDE1',
          transform: `rotateY(${mousePos.x * 8}deg) rotateX(${-mousePos.y * 8}deg) scale(${isHovered ? 1.015 : 1})`,
          transition: 'transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.35s ease',
          transformStyle: 'preserve-3d',
        }}
      >
        {/* Curated Home Photo */}
        <div
          style={{
            position: 'relative',
            width: '100%',
            aspectRatio: '1 / 1',
            overflow: 'hidden',
          }}
        >
          <img
            src="/hero-home.jpg"
            alt="Warm sunlit home interior cared for by SmartServe"
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              transform: `scale(${isHovered ? 1.05 : 1.0}) translate(${-mousePos.x * 12}px, ${-mousePos.y * 12}px)`,
              transition: 'transform 0.6s cubic-bezier(0.16, 1, 0.3, 1)',
            }}
          />

          {/* Gentle warm photographic lighting vignette */}
          <div
            aria-hidden="true"
            style={{
              position: 'absolute',
              inset: 0,
              background: 'linear-gradient(180deg, rgba(250, 247, 240, 0.08) 0%, rgba(31, 42, 30, 0.25) 100%)',
              pointerEvents: 'none',
            }}
          />
        </div>
      </div>

      {/* ── Floating Badge 1: Verified Specialist (Top-Right) ── */}
      <div
        style={{
          position: 'absolute',
          top: '-16px',
          right: '-16px',
          zIndex: 3,
          background: 'rgba(255, 255, 255, 0.88)',
          backdropFilter: 'blur(16px)',
          WebkitBackdropFilter: 'blur(16px)',
          border: '1px solid rgba(255, 255, 255, 0.95)',
          borderRadius: 20,
          padding: '0.85rem 1.15rem',
          boxShadow: '0 16px 36px -10px rgba(31, 42, 30, 0.15)',
          display: 'flex',
          alignItems: 'center',
          gap: '0.85rem',
          transform: `translate(${mousePos.x * 15}px, ${mousePos.y * 15}px)`,
          transition: 'transform 0.25s ease-out',
          animation: 'lp-float-card-1 6s ease-in-out infinite',
        }}
      >
        {/* Avatar with gold ring */}
        <div
          style={{
            position: 'relative',
            width: 44,
            height: 44,
            borderRadius: '50%',
            background: 'linear-gradient(135deg, #2F5233 0%, #7A9E6E 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#FAF7F0',
            fontWeight: 700,
            fontSize: '1rem',
            boxShadow: '0 4px 12px rgba(47, 82, 51, 0.25)',
            flexShrink: 0,
          }}
        >
          EV
          {/* Verified green shield indicator */}
          <span
            style={{
              position: 'absolute',
              bottom: -2,
              right: -2,
              width: 16,
              height: 16,
              borderRadius: '50%',
              background: '#2F5233',
              border: '2px solid #FFFFFF',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" strokeWidth="3.5" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="20 6 9 17 4 12" />
            </svg>
          </span>
        </div>

        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <span
              style={{
                fontFamily: 'var(--lp-font-body)',
                fontWeight: 700,
                fontSize: '0.9rem',
                color: 'var(--lp-ink)',
              }}
            >
              Elena Vance
            </span>
            <span
              style={{
                fontSize: '0.725rem',
                fontWeight: 600,
                color: '#C9A15A',
                background: 'rgba(201, 161, 90, 0.12)',
                padding: '0.15rem 0.45rem',
                borderRadius: 999,
              }}
            >
              ★ 4.99
            </span>
          </div>

          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              marginTop: '0.2rem',
            }}
          >
            <span
              style={{
                width: 7,
                height: 7,
                borderRadius: '50%',
                background: '#10B981',
                boxShadow: '0 0 0 3px rgba(16, 185, 129, 0.2)',
                animation: 'lp-pulse-subtle 2s infinite',
              }}
            />
            <span
              style={{
                fontFamily: 'var(--lp-font-body)',
                fontSize: '0.75rem',
                fontWeight: 500,
                color: 'rgba(31, 42, 30, 0.7)',
              }}
            >
              Master Housekeeper • Arriving 10:00 AM
            </span>
          </div>
        </div>
      </div>

      {/* ── Floating Badge 2: Care Guarantee (Bottom-Left) ── */}
      <div
        style={{
          position: 'absolute',
          bottom: '-20px',
          left: '-20px',
          zIndex: 3,
          background: 'rgba(250, 247, 240, 0.94)',
          backdropFilter: 'blur(16px)',
          WebkitBackdropFilter: 'blur(16px)',
          border: '1px solid rgba(255, 255, 255, 0.95)',
          borderRadius: 22,
          padding: '1rem 1.35rem',
          boxShadow: '0 20px 40px -12px rgba(31, 42, 30, 0.18)',
          transform: `translate(${mousePos.x * -12}px, ${mousePos.y * -12}px)`,
          transition: 'transform 0.25s ease-out',
          animation: 'lp-float-card-2 7s ease-in-out infinite 1s',
          maxWidth: 290,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.4rem' }}>
          <span
            style={{
              fontFamily: 'var(--lp-font-body)',
              fontWeight: 700,
              fontSize: '0.85rem',
              color: 'var(--lp-forest)',
              letterSpacing: '0.04em',
              textTransform: 'uppercase',
            }}
          >
            Living Space Care
          </span>
          <span
            style={{
              fontFamily: 'var(--lp-font-body)',
              fontSize: '0.725rem',
              fontWeight: 600,
              color: 'var(--lp-sage)',
            }}
          >
            100% Guaranteed
          </span>
        </div>

        <p
          style={{
            margin: 0,
            fontFamily: 'var(--lp-font-body)',
            fontSize: '0.8125rem',
            lineHeight: 1.45,
            color: 'var(--lp-ink)',
            fontWeight: 500,
          }}
        >
          🌿 Plant-based botanicals, child & pet safe. Every surface handled with thoughtful detail.
        </p>

        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.6rem',
            marginTop: '0.65rem',
            paddingTop: '0.5rem',
            borderTop: '1px solid rgba(31, 42, 30, 0.08)',
          }}
        >
          <span style={{ fontSize: '0.75rem', color: '#C9A15A' }}>✦</span>
          <span
            style={{
              fontFamily: 'var(--lp-font-body)',
              fontSize: '0.75rem',
              color: 'rgba(31, 42, 30, 0.65)',
              fontWeight: 500,
            }}
          >
            Over 50,000 homes restored
          </span>
        </div>
      </div>
    </div>
  );
};
