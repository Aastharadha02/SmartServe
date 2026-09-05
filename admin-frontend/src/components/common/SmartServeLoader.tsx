import React, { useId, useState, useEffect } from 'react';

export interface SmartServeLoaderProps {
  /**
   * Controls loader visibility. When set to false, smoothly fades out before unmounting.
   * Default is true.
   */
  loading?: boolean;

  /**
   * Predefined size variants or custom pixel size:
   * - 'sm': 36px (for inline, buttons, badges)
   * - 'md': 76px (for cards, modal sections)
   * - 'lg': 140px (default, for page loading, catalog loading)
   * - 'fullscreen': 150px centered in fixed ivory overlay
   */
  size?: 'sm' | 'md' | 'lg' | 'fullscreen' | number;

  /**
   * Optional loading caption / message to display below the loader
   */
  text?: string;

  /**
   * Additional container CSS classes
   */
  className?: string;

  /**
   * Whether to include the soft ambient ivory plate behind the S (default true)
   */
  showBackplate?: boolean;
}

/**
 * SmartServe Global Loading Animation
 *
 * Visual Inspiration: Elegant abstract orbital animation with thin golden irregular
 * curved lines continuously orbiting around a stationary, sharp, centered SmartServe S logo,
 * adorned with sparse floating golden particles.
 */
export const SmartServeLoader: React.FC<SmartServeLoaderProps> = React.memo(({
  loading = true,
  size = 'lg',
  text,
  className = '',
  showBackplate = true,
}) => {
  const rawId = useId();
  const uid = rawId.replace(/[^a-zA-Z0-9_-]/g, '');

  const isFullscreen = size === 'fullscreen';
  const numericSize =
    typeof size === 'number'
      ? size
      : size === 'sm'
      ? 36
      : size === 'md'
      ? 76
      : isFullscreen
      ? 150
      : 140;

  // Smooth unmount transition handling
  const [shouldRender, setShouldRender] = useState(loading);
  const [isFadingOut, setIsFadingOut] = useState(false);

  useEffect(() => {
    if (loading) {
      setShouldRender(true);
      setIsFadingOut(false);
    } else {
      setIsFadingOut(true);
      const timer = setTimeout(() => {
        setShouldRender(false);
      }, 300);
      return () => clearTimeout(timer);
    }
  }, [loading]);

  if (!shouldRender) {
    return null;
  }

  const containerClasses = isFullscreen
    ? `fixed inset-0 z-50 flex flex-col items-center justify-center bg-[#FAF7F0]/92 backdrop-blur-xs transition-opacity duration-300 ease-out ${
        isFadingOut ? 'opacity-0 pointer-events-none' : 'opacity-100'
      } ${className}`
    : `flex flex-col items-center justify-center transition-opacity duration-300 ease-out ${
        isFadingOut ? 'opacity-0 pointer-events-none' : 'opacity-100'
      } ${className}`;

  return (
    <div className={containerClasses} role="status" aria-label={text || 'Loading SmartServe...'}>
      <svg
        width={numericSize}
        height={numericSize}
        viewBox="0 0 200 200"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="shrink-0 select-none overflow-visible"
      >
        <defs>
          <filter id={`ss-glow-${uid}`} x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="1.2" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>

          <radialGradient id={`ss-center-aura-${uid}`} cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95" />
            <stop offset="65%" stop-color="#FAF7F0" stop-opacity="0.9" />
            <stop offset="100%" stop-color="#FAF7F0" stop-opacity="0" />
          </radialGradient>

          <linearGradient id={`ss-gold-grad-1-${uid}`} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#F5DFAB" stop-opacity="0.95" />
            <stop offset="45%" stop-color="#C9A15A" stop-opacity="0.85" />
            <stop offset="100%" stop-color="#B38D45" stop-opacity="0.3" />
          </linearGradient>

          <linearGradient id={`ss-gold-grad-2-${uid}`} x1="100%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#DFB972" stop-opacity="0.9" />
            <stop offset="55%" stop-color="#C9A15A" stop-opacity="0.75" />
            <stop offset="100%" stop-color="#FAF1D9" stop-opacity="0.25" />
          </linearGradient>

          <linearGradient id={`ss-gold-grad-3-${uid}`} x1="0%" y1="100%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#D4B06D" stop-opacity="0.85" />
            <stop offset="60%" stop-color="#C9A15A" stop-opacity="0.7" />
            <stop offset="100%" stop-color="#8C6E2E" stop-opacity="0.2" />
          </linearGradient>
        </defs>

        <style>{`
          @keyframes ss-spin-cw-${uid} {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
          }
          @keyframes ss-spin-ccw-${uid} {
            from { transform: rotate(0deg); }
            to { transform: rotate(-360deg); }
          }
          @keyframes ss-dash-cw-${uid} {
            0% { stroke-dashoffset: 0; }
            50% { stroke-dashoffset: -160; }
            100% { stroke-dashoffset: -320; }
          }
          @keyframes ss-dash-ccw-${uid} {
            0% { stroke-dashoffset: 0; }
            50% { stroke-dashoffset: 180; }
            100% { stroke-dashoffset: 360; }
          }
          @keyframes ss-dot-pulse-${uid} {
            0%, 100% { opacity: 0.2; transform: scale(0.8); }
            50% { opacity: 0.95; transform: scale(1.3); }
          }

          .ss-rot-1-${uid} {
            transform-origin: 100px 100px;
            animation: ss-spin-cw-${uid} 8.5s linear infinite;
          }
          .ss-rot-2-${uid} {
            transform-origin: 100px 100px;
            animation: ss-spin-ccw-${uid} 11.5s linear infinite;
          }
          .ss-rot-3-${uid} {
            transform-origin: 100px 100px;
            animation: ss-spin-cw-${uid} 14.5s linear infinite;
          }
          .ss-rot-4-${uid} {
            transform-origin: 100px 100px;
            animation: ss-spin-ccw-${uid} 9.8s linear infinite;
          }
          .ss-rot-5-${uid} {
            transform-origin: 100px 100px;
            animation: ss-spin-cw-${uid} 18s linear infinite;
          }

          .ss-stroke-1-${uid} {
            stroke-dasharray: 210 120;
            animation: ss-dash-cw-${uid} 4.8s ease-in-out infinite;
          }
          .ss-stroke-2-${uid} {
            stroke-dasharray: 190 140;
            animation: ss-dash-ccw-${uid} 6.2s ease-in-out infinite;
          }
          .ss-stroke-3-${uid} {
            stroke-dasharray: 240 100;
            animation: ss-dash-cw-${uid} 5.6s ease-in-out infinite;
          }
          .ss-stroke-4-${uid} {
            stroke-dasharray: 160 170;
            animation: ss-dash-ccw-${uid} 7.2s ease-in-out infinite;
          }
          .ss-stroke-5-${uid} {
            stroke-dasharray: 260 130;
            animation: ss-dash-cw-${uid} 8s ease-in-out infinite;
          }

          .ss-dot-1-${uid} {
            animation: ss-dot-pulse-${uid} 2.8s ease-in-out infinite;
            transform-origin: center;
          }
          .ss-dot-2-${uid} {
            animation: ss-dot-pulse-${uid} 3.5s ease-in-out infinite 0.8s;
            transform-origin: center;
          }
          .ss-dot-3-${uid} {
            animation: ss-dot-pulse-${uid} 4.2s ease-in-out infinite 1.5s;
            transform-origin: center;
          }
          .ss-dot-4-${uid} {
            animation: ss-dot-pulse-${uid} 3.1s ease-in-out infinite 2.1s;
            transform-origin: center;
          }
        `}</style>

        {/* Ambient Soft Center Aura */}
        <circle cx="100" cy="100" r="42" fill={`url(#ss-center-aura-${uid})`} />

        {/* ═════════ 5 ORGANIC IRREGULAR ORBITAL PATHS ═════════ */}

        {/* Orbit 1: Tilted -15deg, Clockwise */}
        <g transform="rotate(-15 100 100)">
          <g className={`ss-rot-1-${uid}`}>
            <ellipse
              cx="100"
              cy="100"
              rx="74"
              ry="63"
              className={`ss-stroke-1-${uid}`}
              stroke={`url(#ss-gold-grad-1-${uid})`}
              strokeWidth={1.6}
              strokeLinecap="round"
              fill="none"
              filter={`url(#ss-glow-${uid})`}
            />
            {/* Orbit 1 Particle */}
            <circle className={`ss-dot-1-${uid}`} cx="174" cy="100" r="1.8" fill="#F5DFAB" />
          </g>
        </g>

        {/* Orbit 2: Tilted +42deg, Counter-Clockwise */}
        <g transform="rotate(42 100 100)">
          <g className={`ss-rot-2-${uid}`}>
            <ellipse
              cx="100"
              cy="100"
              rx="66"
              ry="78"
              className={`ss-stroke-2-${uid}`}
              stroke={`url(#ss-gold-grad-2-${uid})`}
              strokeWidth={1.25}
              strokeLinecap="round"
              fill="none"
            />
            {/* Orbit 2 Particles */}
            <circle className={`ss-dot-2-${uid}`} cx="100" cy="22" r="1.5" fill="#C9A15A" />
            <circle className={`ss-dot-3-${uid}`} cx="100" cy="178" r="2.0" fill="#F5DFAB" />
          </g>
        </g>

        {/* Orbit 3: Tilted +80deg, Clockwise */}
        <g transform="rotate(80 100 100)">
          <g className={`ss-rot-3-${uid}`}>
            <ellipse
              cx="100"
              cy="100"
              rx="81"
              ry="60"
              className={`ss-stroke-3-${uid}`}
              stroke={`url(#ss-gold-grad-3-${uid})`}
              strokeWidth={1.75}
              strokeLinecap="round"
              fill="none"
            />
            {/* Orbit 3 Particle */}
            <circle className={`ss-dot-1-${uid}`} cx="19" cy="100" r="1.4" fill="#DFB972" />
          </g>
        </g>

        {/* Orbit 4: Tilted -50deg, Counter-Clockwise */}
        <g transform="rotate(-50 100 100)">
          <g className={`ss-rot-4-${uid}`}>
            <ellipse
              cx="100"
              cy="100"
              rx="62"
              ry="72"
              className={`ss-stroke-4-${uid}`}
              stroke="#D8B979"
              strokeWidth={1.0}
              strokeLinecap="round"
              strokeOpacity={0.6}
              fill="none"
            />
            {/* Orbit 4 Particle */}
            <circle className={`ss-dot-4-${uid}`} cx="162" cy="100" r="1.6" fill="#F5DFAB" />
          </g>
        </g>

        {/* Orbit 5: Tilted +115deg, Wide Halo Clockwise */}
        <g transform="rotate(115 100 100)">
          <g className={`ss-rot-5-${uid}`}>
            <ellipse
              cx="100"
              cy="100"
              rx="89"
              ry="76"
              className={`ss-stroke-5-${uid}`}
              stroke="#C9A15A"
              strokeWidth={1.1}
              strokeLinecap="round"
              strokeOpacity={0.45}
              fill="none"
            />
            {/* Orbit 5 Particle */}
            <circle className={`ss-dot-2-${uid}`} cx="100" cy="24" r="1.3" fill="#C9A15A" />
          </g>
        </g>

        {/* ═════════ STATIONARY CENTER: AUTHENTIC SMARTSERVE S ═════════ */}
        <g transform="translate(100, 100) scale(0.82) translate(-48, -48)">
          {/* Authentic SmartServe Squircle Backplate */}
          {showBackplate && (
            <path
              d="M 48 6 L 72 6 A 18 18 0 0 1 90 24 L 90 72 A 18 18 0 0 1 72 90 L 24 90 A 18 18 0 0 1 6 72 L 6 24 A 18 18 0 0 1 24 6 L 48 6 Z"
              stroke="#C9A15A"
              strokeWidth={2.2}
              strokeLinecap="round"
              strokeLinejoin="round"
              fill="#FAF7F0"
              fillOpacity={0.94}
            />
          )}
          {/* Authentic SmartServe Stationary S */}
          <path
            d="M 62 30 C 62 23, 34 22, 34 38 C 34 54, 62 48, 62 64 C 62 80, 34 78, 34 70"
            stroke="#2F5233"
            strokeWidth={7}
            strokeLinecap="round"
            strokeLinejoin="round"
            fill="none"
          />
        </g>
      </svg>

      {/* Optional Brand / Status Message */}
      {text && (
        <p
          className={`mt-4 text-center font-sans tracking-wide text-slate-700 ${
            numericSize <= 48
              ? 'text-[11px] font-medium'
              : numericSize <= 80
              ? 'text-xs font-semibold'
              : 'text-sm font-semibold'
          }`}
        >
          {text}
        </p>
      )}
    </div>
  );
});

SmartServeLoader.displayName = 'SmartServeLoader';
export default SmartServeLoader;
